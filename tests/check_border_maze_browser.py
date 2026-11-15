"""Exercise the textbook border-cell maze in Chromium, both arenas and mobile."""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
DEST = ROOT / '_build' / 'exercise-qa'
DEST.mkdir(parents=True, exist_ok=True)
server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(ASSETS)))
thread = Thread(target=server.serve_forever, daemon=True)
thread.start()
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1400, 'height': 1250})
        page_errors = []
        page.on('pageerror', lambda err: page_errors.append(str(err)))
        page.goto(f'http://127.0.0.1:{server.server_port}/border-cell-maze.html')
        assert 'border-cell-like' in page.title().lower()
        assert page.locator('#mazeCanvas').is_visible()
        assert page.locator('#mapCanvas').is_visible()
        assert page.locator('#distanceMetric').inner_text() != ''
        assert page.locator('#visitedText').inner_text() == '0 visited bins'
        page.locator('#batch').click()
        page.locator('#batch').click()
        assert '200 steps' in page.locator('#timeText').inner_text()
        assert page.locator('#visitedText').inner_text() != '0 visited bins'
        assert page.locator('#spikeMetric').inner_text() != '0'
        page.screenshot(path=str(DEST / 'border-square-desktop.png'), full_page=True)
        page.locator('#rotate').click()
        result = page.locator('#rotationOutput').inner_text()
        assert '180°' in result and 'World-wall distance' in result and 'Forward LiDAR' in result
        page.locator('#arena').select_option('circle')
        page.locator('#batch').click()
        page.locator('#batch').click()
        assert '200 steps' in page.locator('#timeText').inner_text()
        assert '0 visited bins' != page.locator('#visitedText').inner_text()
        page.screenshot(path=str(DEST / 'border-circle-desktop.png'), full_page=True)
        page.locator('#wall').select_option('east')
        page.locator('#batch').click()
        page.locator('#rotate').click()
        assert 'World-wall distance' in page.locator('#rotationOutput').inner_text()
        for n in [1, 2, 3, 4]:
            page.locator(f'[data-stage="{n}"]').click()
            assert page.locator(f'[data-stage="{n}"]').get_attribute('aria-pressed') == 'true'
        page.set_viewport_size({'width': 390, 'height': 850})
        page.screenshot(path=str(DEST / 'border-maze-mobile.png'), full_page=True)
        assert page.evaluate('document.body.scrollWidth <= window.innerWidth + 1')
        assert not page_errors, page_errors
        browser.close()
finally:
    server.shutdown()
    server.server_close()
print('Border maze browser checked: square and circle rate maps, rotation invariance, staged reveal, mobile layout, and 3 screenshots.')
