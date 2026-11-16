"""Browser regression for the five-stage guided border-cell walkthrough."""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(ROOT/'assets')))
thread=Thread(target=server.serve_forever,daemon=True)
thread.start()
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':1300,'height':1000})
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(f'http://127.0.0.1:{server.server_port}/border-cell-guided.html')
        assert page.locator('#arena').is_visible()
        assert page.locator('#mode').input_value() == 'all'
        assert not page.locator('#wallPicker').is_visible()
        assert page.locator('#map').is_visible()
        assert 'Reveal stage 5' in page.locator('#mapStatus').inner_text() or 'Map hidden' in page.locator('#mapStatus').inner_text()
        page.locator('#explore').click()
        assert '25 movement steps' in page.locator('#status').inner_text()
        page.locator('[data-stage="4"]').click()
        assert page.locator('#i').inner_text().endswith('pA')
        assert page.locator('#hz').inner_text().endswith('Hz')
        assert 'numerical voltage integration' in page.locator('#traceStatus').inner_text()
        page.locator('[data-stage="5"]').click()
        page.locator('#explore').click()
        assert 'Observed rates' in page.locator('#mapStatus').inner_text()
        assert '50 movement steps' in page.locator('#status').inner_text()
        page.locator('#shape').select_option('circle')
        assert '0 movement steps' in page.locator('#status').inner_text()
        page.locator('#mode').select_option('single')
        assert page.locator('#wallPicker').is_visible()
        page.locator('#wall').select_option('east')
        page.locator('#explore').click()
        assert page.locator('#d').inner_text().endswith('m') is False  # still stage 1 after a reset
        page.locator('[data-stage="5"]').click()
        assert page.locator('#d').inner_text().endswith('m')
        page.locator('#seed').fill('98')
        page.locator('#seed').press('Tab')
        page.locator('#longExplore').click()
        assert '250 movement steps' in page.locator('#status').inner_text()
        route1=page.locator('#arena').evaluate('(c) => c.toDataURL()')
        page.locator('#reset').click()
        page.locator('#longExplore').click()
        route2=page.locator('#arena').evaluate('(c) => c.toDataURL()')
        assert route1 == route2
        page.locator('#newPath').click()
        page.locator('#longExplore').click()
        route3=page.locator('#arena').evaluate('(c) => c.toDataURL()')
        assert route1 != route3
        page.set_viewport_size({'width':390,'height':844})
        assert page.evaluate('document.body.scrollWidth <= window.innerWidth + 1')
        assert not errors,errors
        browser.close()
finally:
    server.shutdown()
    server.server_close()
print('Guided border-cell walkthrough browser checks passed (square, circle, five stages, mobile).')
