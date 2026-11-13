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
                assert book.evaluate('document.documentElement.scrollWidth <= innerWidth+1'), width
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
            home = book.goto(base + '/exercises/index/')
            assert home and home.status == 200
            assert book.locator('iframe[src*="exercise-practice.html"]').count() == 1
            book.screenshot(path=str(OUT / 'exercise-center-home.png'), full_page=False)
            assert not errors, errors
            return {
                'correct_answer_paths': 120, 'incorrect_answer_paths': 120,
                'written_exercise_count': 96, 'readable_choice_answers': 120,
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
