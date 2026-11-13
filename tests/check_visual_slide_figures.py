"""Verify source-attributed original slide figures in Chapter 6 and its HTML."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import hashlib
import json
from PIL import Image

root = Path(__file__).resolve().parents[1]
assets = root / 'assets/visual-perception-slides'
records = json.loads((assets / 'manifest.json').read_text())['figures']
chapter = (root / 'chapters/06-visual-perception.md').read_text()
assert len(records) == 24
assert len({r['name'] for r in records}) == len(records)

for r in records:
    path = root / r['path']
    assert path.is_file(), f'Missing original slide asset: {path}'
    assert hashlib.sha256(path.read_bytes()).hexdigest() == r['sha256'], path
    with Image.open(path) as im:
        assert list(im.size) == r['size']
        im.verify()
    assert r['sources'], f'Missing source record: {path}'
    assert f'```{{figure}} ../{r["path"]}' in chapter
    assert f':label: fig-vision-slide-{r["name"]}' in chapter
    for src in r['sources']:
        assert src['part'] in (1, 2)
        assert 1 <= src['slide'] <= (79 if src['part'] == 1 else 66)

htmlroot = root / '_build/html'
page = htmlroot / 'chapters/visual-perception/index.html'
if page.exists():
    class Parsed(HTMLParser):
        def __init__(self):
            super().__init__()
            self.images = []
            self.ids = set()
        def handle_starttag(self, tag, attrs):
            a = dict(attrs)
            if 'id' in a:
                self.ids.add(a['id'])
            if tag == 'img':
                self.images.append(a)
    parsed = Parsed()
    parsed.feed(page.read_text())
    base = '/Introduction-to-Neuromorphic-Embodied-AI'
    image_bytes = {}
    for im in parsed.images:
        src = im.get('src', '')
        url = urlsplit(src)
        if url.scheme or url.netloc:
            continue
        p = unquote(url.path)
        if p.startswith(base + '/'):
            p = p[len(base):]
        target = htmlroot / p.lstrip('/') if p.startswith('/') else page.parent / p
        if target.is_file():
            image_bytes[hashlib.sha256(target.read_bytes()).hexdigest()] = im
    for r in records:
        assert 'fig-vision-slide-' + r['name'] in parsed.ids, r['name']
        assert r['sha256'] in image_bytes, f'Original image not referenced by HTML: {r["name"]}'
        assert image_bytes[r['sha256']].get('alt'), r['name']
    assert any('sensor-course-vision' in x.get('src','') for x in parsed.images), 'Existing LIF example figure lost'
    assert 'Neural Encoding and the ANN' not in page.read_text(), 'Removed chapter restored'
    print('Verified all 24 original slide figures in built HTML, including exact bytes, anchors, alt text, and the existing LIF figure.')
else:
    print('Verified all 24 source figures, hashes, citations, dimensions, and chapter references; no built HTML present yet.')
