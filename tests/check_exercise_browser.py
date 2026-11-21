"""Exercise the real built quiz and chapter embeds in a browser over HTTP.

Use the self-contained player plus actual book pages, not a duplicate UI. This
suite sends no student data anywhere and does not require an external account.
"""
from __future__ import annotations
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import tempfile
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BUILT = ROOT / '_build/html'
OUT = ROOT / '_build/exercise-qa'
PREFIX = os.environ.get('BASE_URL', '/Introduction-to-Neuromorphic-Embodied-AI').strip('/')
OUT.mkdir(parents=True, exist_ok=True)


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def answer_adaptive(player, question, *, correct):
    assert player.locator('#adaptive-question').inner_text() == question['prompt']
    choice = question['answer'] if correct else (question['answer'] + 1) % len(question['options'])
    player.locator(f'#adaptive-options input[value="{choice}"]').check()
    player.locator('#adaptive-submit').click()
    assert player.locator('#adaptive-feedback').get_attribute('data-result') == ('correct' if correct else 'wrong')
    assert player.locator('#adaptive-source').get_attribute('href') == question['sourceHref']


def check_adaptive_practice(browser, base, data):
    context = browser.new_context(viewport={'width': 1400, 'height': 960})
    try:
        book = context.new_page()
        player_page = context.new_page()
        chapters = data['adaptive']
        for topic, objectives in chapters.items():
            # The entry point for every numbered chapter is its own chapter-end iframe.
            chapter_path = objectives[0]['questions'][0]['sourceHref'].split('#')[0]
            origin = base.removesuffix('/' + PREFIX)
            response = book.goto(f'{origin}{chapter_path}#adaptive-practice-{topic}')
            assert response and response.ok, topic
            selector = 'iframe[src*="mode=adaptive"]'
            assert book.locator(selector).count() == 1, topic
            player = book.frame_locator(selector)
            player.locator('#adaptive-question').wait_for()
            assert player.locator('#adaptive-question').inner_text() == objectives[0]['questions'][0]['prompt']

            practice_url = base + f'/exercise-practice.html?topic={topic}&mode=adaptive'
            player_page.goto(practice_url)
            player_page.locator('#adaptive-content').wait_for()
            for index, objective in enumerate(objectives):
                questions = objective['questions']
                # For every concept, two misses yield two lessons and two fresh follow-ups.
                for question_index in range(2):
                    answer_adaptive(player_page, questions[question_index], correct=False)
                    lesson = objective['lessons'][question_index]
                    assert lesson['title'] in player_page.locator('#adaptive-lesson-title').inner_text()
                    assert player_page.locator('#adaptive-lesson-body').inner_text() == lesson['body']
                    assert player_page.locator('#adaptive-progress').get_attribute('value') == str(index)
                    if topic == 'ch1' and index == 0 and question_index == 0:
                        player_page.reload()
                        player_page.locator('#adaptive-lesson').wait_for()
                        assert player_page.locator('#adaptive-lesson-body').inner_text() == lesson['body']
                    player_page.get_by_role('button', name='Try a new question').click()

                answer_adaptive(player_page, questions[2], correct=True)
                assert player_page.locator('#adaptive-progress').get_attribute('value') == str(index)
                player_page.get_by_role('button', name='Check with another question').click()
                answer_adaptive(player_page, questions[3], correct=True)
                assert player_page.locator('#adaptive-feedback-title').inner_text() == 'Concept mastered'
                assert player_page.locator('#adaptive-progress').get_attribute('value') == str(index + 1)
                player_page.get_by_role('button', name='Continue chapter').click()
            assert player_page.locator('#adaptive-summary-title').inner_text() == 'Chapter practice mastered'
            player_page.reload()
            player_page.locator('#adaptive-summary-title').wait_for()
            assert player_page.locator('#adaptive-progress').get_attribute('value') == str(len(objectives))

        # In a new profile, a miss breaks the streak, and exhausting the bank does not grant mastery.
        fresh = browser.new_context(viewport={'width': 390, 'height': 844})
        try:
            mobile = fresh.new_page()
            target = next(o for o in chapters['ch8'] if o['id'] == 'border-readout')
            chapter_path = target['questions'][0]['sourceHref'].split('#')[0]
            mobile.goto(origin + chapter_path + '#adaptive-practice-ch8')
            mobile.locator(selector).wait_for()
            player = mobile.frame_locator(selector)
            player.get_by_text('Concepts in this chapter').click()
            player.get_by_role('button', name=target['title'], exact=False).click()
            for idx, question in enumerate(target['questions']):
                answer_adaptive(player, question, correct=idx in (0, len(target['questions']) - 1))
                if idx < len(target['questions']) - 1:
                    player.locator('#adaptive-next').click()
            assert player.locator('#adaptive-summary-title').inner_text() == 'More review needed'
            assert player.locator('#adaptive-progress').get_attribute('value') == '0'
            child = next(frame for frame in mobile.frames if 'mode=adaptive' in frame.url)
            child.wait_for_function('document.querySelector("main").getBoundingClientRect().height <= innerHeight + 3')
            assert child.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
            player.locator('#adaptive-repeat').click()
            assert player.locator('#adaptive-question').inner_text() == target['questions'][0]['prompt']
        finally:
            fresh.close()
    finally:
        context.close()
    return sum(map(len, chapters.values()))


def run_checks(base: str) -> dict:
    with sync_playwright() as pw:
        launch = dict(headless=True, args=['--no-sandbox'])
        if os.environ.get('PLAYWRIGHT_CHROMIUM_PATH'):
            launch['executable_path'] = os.environ['PLAYWRIGHT_CHROMIUM_PATH']
        browser = pw.chromium.launch(**launch)
        try:
            context = browser.new_context(viewport={'width': 1100, 'height': 1000})
            page = context.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/exercise-practice.html?topic=all')
            data = page.evaluate('practiceTestData')
            assert len(data['questions']) == 120
            for q in data['questions']:
                page.select_option('#jump', q['id'])
                page.locator('#options input').nth(q['answer']).check()
                assert page.locator('#feedback-title').inner_text() == 'Correct', q['id']
                assert page.locator('#explanation').inner_text() == q['explanation']
                assert page.locator('#source').get_attribute('href') == q['sourceHref']
                assert page.locator('label[data-state="correct"]').count() == 1
            assert 'First try: 120 / 120 attempted' in page.locator('#stats').inner_text()
            page.select_option('#filter', 'unanswered')
            assert page.locator('#empty').is_visible()
            page.locator('#show-all').click()
            assert page.locator('#jump option').count() == 120
            for q in data['questions']:
                page.select_option('#jump', q['id'])
                page.locator('#options input').nth((q['answer'] + 1) % 4).check()
                assert page.locator('#feedback-title').inner_text() == 'Not quite', q['id']
                assert page.locator('label[data-state="wrong"]').count() == 1
                assert page.locator('label[data-state="correct"]').count() == 1
            assert 'First try: 120 / 120 attempted' in page.locator('#stats').inner_text()
            assert not errors, errors

            # Independent profile: retries must not inflate the first-try score.
            c2 = browser.new_context(viewport={'width': 1000, 'height': 900})
            p2 = c2.new_page()
            p2.goto(base + '/exercise-practice.html?topic=ch8&q=ch8-001')
            q = next(q for q in data['questions'] if q['id'] == 'ch8-001')
            p2.locator('#options input').nth((q['answer'] + 1) % 4).check()
            assert p2.locator('#feedback-title').inner_text() == 'Not quite'
            assert '15 m' in p2.locator('#correct-answer').inner_text()
            p2.locator('#retry').click()
            assert p2.locator('#feedback').is_hidden()
            p2.locator('#options input').nth(q['answer']).check()
            assert 'First try: 0 / 1 attempted' in p2.locator('#stats').inner_text()
            p2.reload()
            assert p2.locator('#feedback-title').inner_text() == 'Correct'
            assert 'First try: 0 / 1 attempted' in p2.locator('#stats').inner_text()
            p2.locator('#next').click()
            p2.locator('#reveal').click()
            assert p2.locator('#feedback-title').inner_text() == 'Answer revealed'
            assert 'Revealed before trying: 1' in p2.locator('#stats').inner_text()
            p2.select_option('#filter', 'missed')
            assert p2.locator('#jump option').count() == 2
            p2.select_option('#filter', 'all')
            p2.select_option('#topic', 'ch1')
            assert p2.locator('#jump option').count() == 12
            p2.locator('#options input').first.check()
            p2.select_option('#topic', 'ch8')
            p2.once('dialog', lambda d: d.accept())
            p2.locator('#reset').click()
            assert 'Progress: 0 / 16' in p2.locator('#stats').inner_text()
            p2.select_option('#topic', 'ch1')
            assert 'Progress: 1 / 12' in p2.locator('#stats').inner_text()
            p2.select_option('#topic', 'ch8')
            p2.select_option('#filter', 'calculation')
            assert p2.locator('#jump option').count() == 9
            before = sorted(p2.locator('#jump option').evaluate_all('(xs)=>xs.map(x=>x.value)'))
            p2.locator('#shuffle').click()
            after = sorted(p2.locator('#jump option').evaluate_all('(xs)=>xs.map(x=>x.value)'))
            assert before == after

            # Missing or restricted browser storage must not disable self-study.
            blocked = browser.new_context()
            blocked.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked')}})")
            b = blocked.new_page()
            b.goto(base + '/exercise-practice.html?topic=ch2')
            assert b.locator('#storage-warning').is_visible()
            b.locator('#options input').first.check()
            assert b.locator('#feedback').is_visible()

            # Verify the actual book page and its responsive same-origin iframe.
            display = browser.new_context(viewport={'width': 1500, 'height': 1000})
            book = display.new_page()
            response = book.goto(base + '/exercises/ch8/')
            assert response and response.status == 200
            frame_element = book.locator('iframe[src*="exercise-practice.html"]')
            frame_element.wait_for()
            fr = book.frame_locator('iframe[src*="exercise-practice.html"]')
            fr.locator('#options input').nth(q['answer']).check()
            assert fr.locator('#feedback-title').inner_text() == 'Correct'
            book.wait_for_timeout(600)
            frame_element.scroll_into_view_if_needed()
            book.screenshot(path=str(OUT / 'exercise-center-desktop.png'), full_page=False)
            for width in [390, 320]:
                book.set_viewport_size({'width': width, 'height': 844})
                book.wait_for_timeout(600)
                frame_element.scroll_into_view_if_needed()
                metrics = book.evaluate("""()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,offenders:[...document.querySelectorAll('body *')].map(e=>({e,r:e.getBoundingClientRect()})).filter(({e,r})=>r.right>innerWidth+1&&r.width>0).slice(0,25).map(({e,r})=>({tag:e.tagName,cls:String(e.className),text:e.innerText?.slice(0,80),left:r.left,right:r.right,width:r.width}))})""")
                (OUT / f'layout-{width}.json').write_text(json.dumps(metrics, indent=2))
                book.screenshot(path=str(OUT / f'book-{width}.png'), full_page=False)
                assert metrics['scroll'] <= width + 1, json.dumps(metrics)
                child = next(f for f in book.frames if 'exercise-practice.html' in f.url)
                assert child.evaluate('document.documentElement.scrollWidth <= innerWidth+1'), width
                assert child.evaluate('document.querySelector("main").getBoundingClientRect().height <= innerHeight+3'), width
                if width == 390:
                    book.screenshot(path=str(OUT / 'exercise-center-mobile.png'), full_page=False)
                    child.locator('main').screenshot(path=str(OUT / 'practice-card-mobile.png'))
            book.set_viewport_size({'width': 1500, 'height': 1000})
            book.wait_for_timeout(300)
            assert book.locator('details').count() == 16
            first = book.locator('details').first
            assert first.get_attribute('open') is None
            first.locator('summary').click()
            assert first.get_attribute('open') is not None
            first.screenshot(path=str(OUT / 'written-answer-expanded.png'))
            assert book.locator('.katex-error').count() == 0

            # Static answer dropdowns remain useful when scripting is disabled.
            nojs = browser.new_context(java_script_enabled=False)
            readable = nojs.new_page()
            r = readable.goto(base + '/exercises/question-bank/')
            assert r and r.status == 200
            assert readable.locator('details').count() == 120
            readable.locator('details summary').first.click()
            assert readable.locator('details').first.get_attribute('open') is not None
            assert readable.locator('.katex-error').count() == 0
            home = book.goto(base + '/exercises/')
            assert home and home.status == 200
            assert book.locator('iframe[src*="exercise-practice.html"]').count() == 1
            book.screenshot(path=str(OUT / 'exercise-center-home.png'), full_page=False)
            assert not errors, errors
            adaptive_count = check_adaptive_practice(browser, base, data)
            return {
                'correct_answer_paths': 120, 'incorrect_answer_paths': 120,
                'written_exercise_count': 96, 'readable_choice_answers': 120,
                'adaptive_concepts_verified': adaptive_count,
                'verified': ['source links', 'retry', 'reveal', 'first-attempt accounting',
                             'reload persistence', 'topic-scoped reset', 'filters', 'shuffle',
                             'storage unavailable fallback', 'actual chapter iframe resizing',
                             '390px and 320px overflow', 'collapsed answers', 'no-JavaScript answers'],
                'page_errors': errors,
            }
        finally:
            browser.close()


if __name__ == '__main__':
    assert (BUILT / 'exercise-practice.html').is_file(), 'Build the textbook first'
    with tempfile.TemporaryDirectory(prefix='neai-practice-http-') as directory:
        link = Path(directory) / PREFIX
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(BUILT, target_is_directory=True)
        server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=directory))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            result = run_checks(f'http://127.0.0.1:{server.server_port}/{PREFIX}')
            (OUT / 'report.json').write_text(json.dumps(result, indent=2) + '\n')
            print('Interactive browser QA passed:', json.dumps(result))
        finally:
            server.shutdown()
            server.server_close()
