"""Check lecture provenance, media integrity, exact examples, and rendered Chapter 8."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import hashlib,json,re
import numpy as np
from PIL import Image

root=Path(__file__).resolve().parents[1]
source=root/'chapters/08-lidar-encoding.md'
s=source.read_text()
manifest=json.loads((root/'assets/lidar-lecture/manifest.json').read_text())
assert len(manifest['images'])==24
assert sum(r['frames']>1 for r in manifest['images'])==2
assert len(manifest['videos'])==3
for r in manifest['images']:
    path=root/'assets/lidar-lecture'/r['file']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==r['sha256'],path
    with Image.open(path) as im:
        assert list(im.size)==r['size']
        assert getattr(im,'n_frames',1)==r['frames']
    assert '../assets/lidar-lecture/'+r['file'] in s
    assert 'fig-lidar-'+Path(r['file']).stem in s
assert 'sensor-course-lidar.png' in s and ':label: fig-sensor-lidar' in s
assert '(85-exercises)=' in s
assert '## 8.12 Additional Reading Materials' in s
questions=s.split('## 8.13 Exercises',1)[1].split('## References',1)[0]
assert len(re.findall(r'^\d+\. ',questions,re.M))==16
solutions=(root/'chapters/solutions-embodied.md').read_text()
answers=solutions.split('## Chapter 8',1)[1].split('## Chapter 9',1)[0]
assert len(re.findall(r'^\d+\. ',answers,re.M))==16
assert '(lidar-solutions)=' in solutions
ns={'__name__':'__chapter8_examples__'}
blocks=re.findall(r'```python\n(.*?)\n```',s,re.S)
assert len(blocks)==2
for i,code in enumerate(blocks):exec(compile(code,f'Chapter8-example-{i+1}','exec'),ns)
encode=ns['sector_encode'];sample=ns['poisson_bin_counts']
d,r,m=encode([.8,3,np.nan,5],np.deg2rad([0,90,0,179]))
assert np.array_equal(np.flatnonzero(m),[18,27,35])
assert np.allclose(d[m],[.8,3,5]) and np.allclose(r[m],[42.8,23,5])
assert np.isnan(d[~m]).all() and (r[~m]==0).all()
for angle,index in [(-180,0),(-175,0),(0,18),(90,27),(179,35),(180,0)]:
    dd,rr,mm=encode([1],[np.deg2rad(angle)]);assert np.flatnonzero(mm).tolist()==[index]
with np.errstate(all='raise'):
    dd,rr,mm=encode([np.nan,np.inf,0.01,6,1],[0,0,0,0,np.nan])
assert not mm.any()
dd,rr,mm=encode([4,1,4],[0,0,0]);assert dd[18]==1
c1,m1=sample(r,m,seed=8);c2,m2=sample(r,m,seed=8)
assert np.array_equal(c1,c2) and c1.shape==(36,500)
assert (c1[~m]==0).all() and np.array_equal(m1,m)
assert np.isclose(3e8*100e-9/2,15)
assert np.isclose(3e8*1e-9/2,.15)
assert np.isclose(42.8*.5,21.4)
assert np.isclose(1-np.exp(-42.8*.001),0.041897,atol=1e-6)
for call in [lambda:encode([1,2],[0]),lambda:encode([1],[0],sectors=0),lambda:encode([1],[0],range_min=6),lambda:sample([-1],[True]),lambda:sample([1],[True],duration_s=.5001)]:
    try:call()
    except ValueError:pass
    else:raise AssertionError('Invalid encoder input was accepted')

class Page(HTMLParser):
    def __init__(self):super().__init__();self.images=[];self.frames=[];self.ids=set();self.links=[];self.text=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.add(a['id'])
        if tag=='img':self.images.append(a.get('src',''))
        if tag=='iframe':self.frames.append(a.get('src',''))
        if tag=='a':self.links.append(a.get('href',''))
    def handle_data(self,s):self.text.append(s)
htmlroot=root/'_build/html';page=htmlroot/'chapters/lidar-encoding/index.html'
assert page.is_file()
p=Page();p.feed(page.read_text())
assert {'85-exercises','id-85-exercises'} & p.ids
assert 'fig-sensor-lidar' in p.ids
base='/Introduction-to-Neuromorphic-Embodied-AI'
for rec in manifest['images']:
    key=Path(rec['file']).stem
    assert 'fig-lidar-'+key in p.ids
    # MyST may truncate filenames; compare the actual published bytes instead.
    found=False
    for src in p.images:
        u=urlsplit(src);path=unquote(u.path)
        if u.scheme or u.netloc:continue
        if path.startswith(base+'/'):path=path[len(base):]
        q=htmlroot/path.lstrip('/') if path.startswith('/') else page.parent/path
        if q.is_file() and hashlib.sha256(q.read_bytes()).hexdigest()==rec['sha256']:found=True;break
    assert found,'Image missing from rendered page: '+key
for video in manifest['videos']:
    assert any('lidar-lecture-media.html?v='+video['id'] in u for u in p.frames)
    assert any(video['watch_url'] in u for u in p.links)
player=htmlroot/'lidar-lecture-media.html'
assert player.is_file()
player_text=player.read_text()
assert 'youtube-nocookie.com/embed/' in player_text
assert 'addEventListener' in player_text and 'data:image/jpeg;base64' in player_text
for v in manifest['videos']:assert v['id'] in player_text
assert 'Neural Encoding and the ANN' not in page.read_text()
solution_html=htmlroot/'chapters/solutions-embodied/index.html'
q=Page();q.feed(solution_html.read_text())
assert 'lidar-solutions' in q.ids
exercise_links = [x for x in q.links if 'lidar-encoding' in x and 'exercises' in x]
assert exercise_links
assert all(unquote(urlsplit(x).fragment) in p.ids for x in exercise_links)
print('Chapter 8 verified: 22 original static figure groups, two intact GIFs, three source video links/players, 16 exercises/answers, encoder examples, and published asset bytes.')
