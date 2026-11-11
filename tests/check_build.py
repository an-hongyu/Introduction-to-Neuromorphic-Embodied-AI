"""Smoke-check published content, equation rendering, images, and local URLs."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

root = Path(__file__).resolve().parents[1] / '_build/html'
base = '/Introduction-to-Neuromorphic-Embodied-AI'
html_files = list(root.rglob('*.html'))
assert (root / 'index.html').is_file(), 'Homepage was not generated'
assert len(html_files) >= 11, f'Expected eleven book pages, found {len(html_files)}'
all_html = '\n'.join(p.read_text() for p in html_files)
for text in ['Introduction to Neuromorphic Embodied AI', 'Closed-Loop Overview',
             'Neuroscience Background', 'Spatial Cells', 'Computational Models of Neurons',
             'Hebbian Learning', 'Place Cell', 'Curriculum and Development Roadmap', 'colab.research.google.com']:
    assert text in all_html, f'Missing published content: {text}'
assert 'katex' in all_html or 'MathJax' in all_html or '<math' in all_html, 'No rendered mathematics'
assert len(list(root.rglob('*.ipynb'))) >= 3, 'Expected three downloadable laboratories'
assert len(list(root.rglob('*.png'))) >= 6, 'Expected at least six notebook figure outputs'

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.urls = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and attrs.get('href'): self.urls.append(attrs['href'])
        if tag in ('img', 'script') and attrs.get('src'): self.urls.append(attrs['src'])
        if tag == 'link' and attrs.get('href'): self.urls.append(attrs['href'])

checked = set()
for page in html_files:
    parser = Links(); parser.feed(page.read_text())
    for url in parser.urls:
        parts = urlsplit(url)
        if parts.scheme or parts.netloc: continue
        path = unquote(parts.path)
        if path == base or path.startswith(base + '/'):
            path = path[len(base):] or '/'
        target = page if not path else (root / path.lstrip('/') if path.startswith('/') else page.parent / path)
        candidates = [target, target.with_suffix('.html'), target / 'index.html']
        assert any(p.is_file() for p in candidates), f'Broken local URL in {page.relative_to(root)}: {url}'
        resolved = next(p for p in candidates if p.is_file())
        if parts.fragment and resolved.suffix == '.html':
            anchor = unquote(parts.fragment)
            text = resolved.read_text()
            assert f'id="{anchor}"' in text or f"id='{anchor}'" in text, f'Missing anchor in {page}: {url}'
        checked.add(url)
print(f'Verified {len(html_files)} HTML pages, equations, notebook, figures, and {len(checked)} local URLs.')
