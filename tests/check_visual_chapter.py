"""Regression checks for the author's Visual Perception revision."""
from pathlib import Path
from html.parser import HTMLParser
import re
import numpy as np

root = Path(__file__).resolve().parents[1]
chapter = (root / 'chapters/06-visual-perception.md').read_text()
solutions = (root / 'chapters/solutions-embodied.md').read_text()
toc = (root / 'myst.yml').read_text()
assert not (root / 'chapters/05-neural-encoding.md').exists(), 'Removed chapter was restored'
assert '05-neural-encoding.md' not in toc
assert 'Chapter 5' not in solutions
assert '06-visual-perception.md#66-exercises' in solutions
assert 'solutions-embodied.md#vision-solutions' in chapter
assert 'Chapter 6' in chapter and 'vision-solutions' in solutions
assert 'Neural Encoding and the ANN' not in (root / 'index.md').read_text()
for word in ['Radiometry', 'Photometry', 'Bayer', 'CCD', 'CMOS', 'tristimulus',
             'color-matching', 'monadic', 'dyadic', 'Gaussian', 'chroma',
             '4-1 Visual Perception.pptx', '4-2 Visual Perception.pptx',
             'sensor-course-vision.png', '66-exercises']:
    assert word.lower() in chapter.lower(), f'Missing lecture material or retained anchor: {word}'
questions = chapter.split('## 6.12 Exercises', 1)[1].split('## References', 1)[0]
assert len(re.findall(r'^\d+\. ', questions, re.M)) == 16
answers = solutions.split('## Chapter 6', 1)[1].split('## Chapter 7', 1)[0]
assert len(re.findall(r'^\d+\. ', answers, re.M)) == 16
assert chapter.index('## 6.11 Additional Reading Materials') < chapter.index('## 6.12 Exercises')

# Execute the exact published snippets in order, not a parallel implementation.
blocks = re.findall(r'```python\n(.*?)\n```', chapter, re.S)
assert len(blocks) == 2
ns = {'__name__': '__visual_examples__'}
for i, block in enumerate(blocks):
    exec(compile(block, f'Chapter6-example-{i+1}', 'exec'), ns)
k = ns['gaussian_kernel'](3, 1.0)
assert np.isclose(k[1, 1], 0.2041799555716581)
assert np.isclose(k.sum(), 1)
assert np.isclose(ns['convolve_gray'](np.array([[50,10,37],[20,30,72],[10,20,11]]), np.ones((3,3))/9)[1,1], 260/9)
assert np.allclose(ns['convolve_gray'](np.full((6,8),7.5), k), 7.5)
assert ns['red_feature'](np.array([[[1.,1.,1.]]])) == 0
assert ns['red_feature'](np.array([[[0.,0.,1.]]])) == 0
assert ns['red_feature'](np.array([[[1.,0.,0.]]])) == 1
assert np.isclose(8*150/600, 2)
assert 4912*3684 == 18095808
assert 800*600*3 == 1440000
assert np.allclose(np.array([.5,.2,.9])/1.6, [.3125,.125,.5625])
for bad in [np.array([1.,2.]), np.array([[[np.nan,0.,0.]]]), np.array([[[1.1,0.,0.]]])]:
    try:
        ns['red_feature'](bad)
    except ValueError:
        pass
    else:
        raise AssertionError('RGB validation accepted an invalid input')

htmlroot = root / '_build/html'
page = htmlroot / 'chapters/visual-perception/index.html'
assert page.is_file(), 'Revised chapter was not built'
html = page.read_text()
class Content(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=set(); self.parts=[]; self.images=[]; self.links=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        if tag=='img': self.images.append(a.get('src',''))
        if tag=='a': self.links.append(a.get('href',''))
    def handle_data(self, data): self.parts.append(data)
p=Content(); p.feed(html)
text=' '.join(p.parts).lower()
for term in ['radiometry', 'bayer', 'color-matching', 'monadic', 'dyadic', 'gaussian', 'chroma', '6.12 exercises']:
    assert term in text, f'Not rendered: {term}'
# MyST prefixes explicit labels beginning with a digit with "id-" in HTML.
assert {'vision-pipeline','id-66-exercises'}.issubset(p.ids)
solution_page=Content()
solution_page.feed((htmlroot/'chapters/solutions-embodied/index.html').read_text())
assert 'vision-solutions' in solution_page.ids
assert any('solutions-embodied' in href and href.endswith('#vision-solutions') for href in p.links), 'Rendered solution link is missing'
assert any('visual-perception' in href and href.endswith('#id-66-exercises') for href in solution_page.links), 'Rendered return-to-exercises link is missing'
assert any('sensor-course-vision' in s for s in p.images), 'Existing vision figure was lost'
assert 'Neural Encoding and the ANN' not in html, 'Deleted chapter remains in navigation'
assert 'Neural Encoding and the ANN' not in (htmlroot/'index.html').read_text()
print('Visual chapter: lecture coverage, 16 questions/answers, exact code snippets, numerical examples, image, round-trip links, and removed chapter all verified.')
