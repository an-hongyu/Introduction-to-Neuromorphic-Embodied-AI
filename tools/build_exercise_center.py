"""Build the exercise section from the live chapters and an authored quiz bank.

Run before `jupyter book build`; run with --post-build afterward, then --check.
Existing chapter prose/exercise lists and the end-of-book solutions remain the
single source for written questions. Generated copies are never hand-edited.
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import runpy
from html.parser import HTMLParser
import yaml

ROOT = Path(__file__).resolve().parents[1]
BASE = '/' + os.environ.get('BASE_URL', 'Introduction-to-Neuromorphic-Embodied-AI').strip('/')
# Topic id, reader-facing title, chapter filename, solution file, solution heading prefix.
TOPICS = [
 ('ch1', 'Chapter 1 - Neurons and Synapses', '01-neuroscience-background', 'solutions-foundations', 'Chapter 1 '),
 ('ch2', 'Chapter 2 - Computational Models of Neurons', '03-computational-neuron-models', 'solutions-foundations', 'Chapter 2 '),
 ('ch3', 'Chapter 3 - Hebbian Learning and Synaptic Plasticity', '04-hebbian-learning', 'solutions-foundations', 'Chapter 3 '),
 ('ch4', 'Chapter 4 - Spatial Cells and Their Models', '02-spatial-cells', 'solutions-foundations', 'Chapter 4 '),
 ('ch6', 'Chapter 6 - Visual Perception', '06-visual-perception', 'solutions-embodied', 'Chapter 6 '),
 ('ch7', 'Chapter 7 - Inertial Sensing', '07-inertial-sensing', 'solutions-embodied', 'Chapter 7 '),
 ('ch8', 'Chapter 8 - Neural Encoding for LiDAR Sensing', '08-lidar-encoding', 'solutions-embodied', 'Chapter 8 '),
 ('ch9', 'Chapter 9 - Nengo, ROS 2, and Gazebo', '09-nengo-ros-gazebo', 'solutions-embodied', 'Chapter 9 '),
 ('ch10', 'Chapter 10 - Associative Learning Robot', '10-associative-learning-robot', 'solutions-embodied', 'Chapter 10 '),
 ('overview', 'Overview - Embodied AI', '01-introduction', 'solutions-foundations', 'Overview '),
 ('labs', 'Computational Laboratories', 'computational-neuron-models-lab', 'solutions-laboratories', 'Laboratory 1 '),
]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding='utf-8')


def write(path: str, content: str) -> None:
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding='utf-8')


def section_body(document: str, prefix: str | None = None) -> tuple[str, str]:
    heads = list(re.finditer(r'^## ([^\n]+)\n', document, re.M))
    for i, m in enumerate(heads):
        heading = m.group(1)
        if (prefix and heading.startswith(prefix)) or (prefix is None and re.search(r'\bExercises\b', heading, re.I)):
            end = heads[i+1].start() if i+1 < len(heads) else len(document)
            return heading, document[m.end():end]
    raise ValueError(f'Missing exercise/answer section: {prefix}')


def numbered_items(body: str) -> list[str]:
    matches = list(re.finditer(r'^(\d+)\. ', body, re.M))
    assert [int(m.group(1)) for m in matches] == list(range(1, len(matches)+1)), 'Nonconsecutive exercise numbers'
    result = []
    for i, m in enumerate(matches):
        end = matches[i+1].start() if i+1 < len(matches) else len(body)
        item = body[m.end():end]
        item = re.split(r'^\[Worked solutions\]', item, flags=re.M)[0]
        item = re.sub(r'^\([\w-]+\)=\s*$', '', item, flags=re.M).strip()
        assert item, 'Empty question or answer'
        result.append(item)
    assert result, 'Exercise list is empty'
    return result


def source_group(stem: str, sol: str, prefix: str) -> dict:
    chapter = text(f'chapters/{stem}.md')
    h, body = section_body(chapter)
    sh, sb = section_body(text(f'chapters/{sol}.md'), prefix)
    qs, answers = numbered_items(body), numbered_items(sb)
    assert len(qs) == len(answers), (stem, len(qs), len(answers))
    return dict(stem=stem, solution=sol, heading=h, solution_heading=sh, questions=qs, answers=answers)


def groups_for(topic: tuple) -> list[dict]:
    _, _, stem, sol, prefix = topic
    groups = [source_group(stem, sol, prefix)]
    if topic[0] == 'labs':
        groups.append(source_group('04-place-cells', sol, 'Laboratory 2 '))
    return groups


def source_for(topic: tuple, section: str) -> str:
    if topic[0] == 'labs' and section.startswith('L2'):
        return '04-place-cells'
    return topic[2]


def chapter_url(stem: str) -> str:
    return BASE + '/chapters/' + re.sub(r'^\d+-', '', stem) + '/'


def relocate(content: str, stem: str) -> str:
    # Relocate only relative Markdown links. Keep formulas and question wording.
    def move(match):
        label, url = match.group(1), match.group(2)
        if url.startswith('#'):
            url = '../chapters/' + stem + '.md' + url
        elif not re.match(r'(?:[a-z]+:|/|\.\./)', url):
            url = '../chapters/' + url
        return '[' + label + '](' + url + ')'
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', move, content)


def iframe(topic_id: str) -> str:
    return f'''```{{iframe}} {BASE}/exercise-practice.html?topic={topic_id}
:label: practice-player-{topic_id}
:class: exercise-playground
:title: Interactive practice questions for {topic_id}
:width: 100%
```

[Open practice in a full page]({BASE}/exercise-practice.html?topic={topic_id}) | [Readable question bank](question-bank.md)
'''


def add_portal(stem: str, topic_id: str) -> None:
    path = f'chapters/{stem}.md'
    doc = text(path)
    marker = f'<!-- exercise-center:{topic_id} -->'
    if marker in doc:
        return
    heading, _ = section_body(doc)
    target = '## ' + heading + '\n'
    portal = f'\n{marker}\n[Interactive questions and expandable worked answers](../exercises/{topic_id}.md) are available in the dedicated exercise section.\n'
    assert doc.count(target) == 1
    write(path, doc.replace(target, target + portal, 1))


def data_and_groups() -> tuple[dict, dict]:
    rows = runpy.run_path(str(ROOT / 'exercises/question_bank.py'))['QUESTION_ROWS']
    assert set(rows) == {t[0] for t in TOPICS}
    all_questions, metadata, all_groups = [], [], {}
    for ti, t in enumerate(TOPICS):
        tid, title, _, _, _ = t
        groups = groups_for(t)
        all_groups[tid] = groups
        metadata.append(dict(id=tid, title=title, choiceCount=len(rows[tid]), writtenCount=sum(len(g['questions']) for g in groups)))
        for qi, row in enumerate(rows[tid], 1):
            section, kind, prompt, options, explanation = row
            assert len(options) == 4 and len(set(options)) == 4
            assert kind in ('Concept', 'Calculation', 'Application')
            stem = source_for(t, section)
            source = text(f'chapters/{stem}.md')
            assert re.search(r'^#{2,4} '+re.escape(section)+r'(?:\s|$)', source, re.M), (tid, section)
            offset = (qi-1+ti) % 4
            displayed = options[-offset:] + options[:-offset] if offset else list(options)
            sig = hashlib.sha256(json.dumps(row, ensure_ascii=True).encode()).hexdigest()[:16]
            all_questions.append(dict(id=f'{tid}-{qi:03d}', topic=tid, kind=kind, prompt=prompt, options=displayed,
                                      answer=offset, explanation=explanation, sourceStem=stem, sourceSection=section,
                                      sourceHref=chapter_url(stem), sourceLabel=f'Review section {section}', sig=sig))
    assert len(all_questions) == 120
    assert len({q['id'] for q in all_questions}) == 120
    return dict(version=1, base=BASE, topics=metadata, questions=all_questions), all_groups


def generate() -> None:
    data, groups = data_and_groups()
    count = sum(t['writtenCount'] for t in data['topics'])
    template = text('assets/exercise-practice.template.html')
    assert template.count('__QUESTION_DATA__') == 1
    payload = json.dumps(data, ensure_ascii=True, separators=(',', ':')).replace('</', '<\\/')
    write('assets/exercise-practice.html', template.replace('__QUESTION_DATA__', payload))
    index = f'''---
title: "Exercises & Interactive Questions"
---

# Exercises & Interactive Questions

Practice the concepts, calculations, and experimental decisions in this book. This section brings together **120 interactive multiple-choice questions** and **{count} original written exercises**, organized by chapter and laboratory.

Select an option for immediate feedback and an explanation. Use **Try again**, **First-try misses / revealed**, or **Shuffle question order** for another pass. Progress is stored only in this browser; this is a self-study tool, not a secure or submitted examination.

## Choose a topic

| Topic | Interactive questions | Original written exercises |
|---|---:|---:|
'''
    for t in data['topics']:
        index += f"| [{t['title']}]({t['id']}.md) | {t['choiceCount']} | {t['writtenCount']} |\n"
    index += '\n## Start practicing\n\n' + iframe('all')
    index += '\n## How the exercise section is organized\n\nThe original chapter-end questions remain available for reading in context. The topic pages here reproduce them directly from the current chapters, with answers drawn from the existing end-of-book solution pages. Open an answer only after trying the problem. Computational experiments still require running the relevant notebook; a reference protocol is not a claimed experimental result.\n\n[Read the complete multiple-choice bank and answer explanations](question-bank.md). The original [foundation solutions](../chapters/solutions-foundations.md), [sensor and robotics solutions](../chapters/solutions-embodied.md), and [laboratory solutions](../chapters/solutions-laboratories.md) remain available.\n'
    write('exercises/index.md', index)
    review = '''---
title: "Question Bank and Explanations"
---

# Question Bank and Explanations

This readable version contains the same 120 questions and answer explanations as the interactive player. Each answer is initially collapsed. These are new self-checks adapted from the book's stated concepts and model assumptions, not additional empirical findings.

[Return to the exercise center](index.md)
'''
    for t in data['topics']:
        tid = t['id']
        doc = f'''---
title: "{t['title']} - Exercises"
---

# {t['title']}: Exercises

[Exercise center](index.md) | [Readable choice questions](question-bank.md#practice-bank-{tid})

## Interactive questions

This topic has **{t['choiceCount']} multiple-choice questions**. Choose one option to receive a correctness check, the correct answer, an explanation, and a link to the relevant chapter section.

'''+iframe(tid)+'\n## Original written exercises and worked answers\n\nThese questions and answers are drawn from the existing book. Calculations use the original model conventions. Open-ended experiment questions provide a suggested method rather than invented measurements.\n'
        for gi, group in enumerate(groups[tid], 1):
            stem, sol = group['stem'], group['solution']
            doc += f"\n### {group['heading']}\n\n[Read the original context](../chapters/{stem}.md) | [Book-end solutions](../chapters/{sol}.md)\n"
            for i, (question, answer) in enumerate(zip(group['questions'], group['answers']), 1):
                doc += f'\n(practice-{tid}-{gi}-written-{i})=\n#### Exercise {i}\n\n'+relocate(question,stem)+'\n\n:::{admonition} Show answer and reasoning\n:class: dropdown\n\n'+relocate(answer,sol)+'\n:::\n'
            add_portal(stem,tid)
        write(f'exercises/{tid}.md',doc)
        review += f"\n(practice-bank-{tid})=\n## {t['title']}\n\n[Interactive practice]({tid}.md)\n"
        for q in (q for q in data['questions'] if q['topic']==tid):
            review += f"\n### {q['id'].upper()} - {q['kind']}\n\n{q['prompt']}\n\n"
            for letter, option in zip('ABCD',q['options']):
                review += f'- **{letter}.** {option}\n'
            review += '\n:::{admonition} Show answer and explanation\n:class: dropdown\n\n'
            review += f"**Correct answer: {'ABCD'[q['answer']]}. {q['options'][q['answer']]}**\n\n{q['explanation']}\n\n[Review section {q['sourceSection']}](../chapters/{q['sourceStem']}.md)\n:::\n"
    write('exercises/question-bank.md', review)
    manifest = dict(interactive_count=120, original_count=count, topics=data['topics'])
    write('exercises/generated-manifest.json',json.dumps(manifest,indent=2)+'\n')
    config=yaml.safe_load(text('myst.yml'))
    static=config['project'].setdefault('static_files',[])
    for path in ['assets/exercise-practice.html','assets/exercise-resize.js']:
        if path not in static:static.append(path)
    toc=config['project']['toc']
    toc[:]=[x for x in toc if x.get('title')!='Exercises & Interactive Questions']
    group=dict(title='Exercises & Interactive Questions',children=[dict(file='exercises/index.md')]+[dict(file=f"exercises/{t['id']}.md") for t in data['topics']]+[dict(file='exercises/question-bank.md')])
    at=next((i for i,x in enumerate(toc) if x.get('title')=='Solutions to Exercises'),len(toc))
    toc.insert(at,group)
    write('myst.yml',yaml.safe_dump(config,sort_keys=False,allow_unicode=True))
    home=text('index.md')
    if '<!-- exercise-center-home -->' not in home:
        marker='## Citation'
        assert marker in home
        home=home.replace(marker,'<!-- exercise-center-home -->\n## Exercises and interactive questions\n\n[Open the exercise center](exercises/index.md) for 120 interactive multiple-choice questions, immediate feedback and explanations, and the original chapter and laboratory exercises with expandable worked answers.\n\n'+marker,1)
        write('index.md',home)
    print(f'Generated exercise center: 120 interactive questions, {count} original questions/answers, {len(data["topics"])} topic pages.')


class Headings(HTMLParser):
    def __init__(self):
        super().__init__(); self.heads=[]; self.active=None; self.parts=[]; self.ids=set(); self.details=0; self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag in ('h1','h2','h3','h4'):
            self.active=(tag,a.get('id'));self.parts=[]
        if tag=='details':self.details+=1
        if tag=='a' and a.get('href'):self.links.append(a['href'])
    def handle_data(self,s):
        if self.active:self.parts.append(s)
    def handle_endtag(self,tag):
        if self.active and tag==self.active[0]:
            self.heads.append((self.active[1],''.join(self.parts).strip()));self.active=None


def get_built_data() -> tuple[Path,str,dict]:
    p=ROOT/'_build/html/exercise-practice.html'
    s=p.read_text()
    m=re.search(r'<script id="question-data" type="application/json">(.*?)</script>',s,re.S)
    assert m
    return p,s,json.loads(m.group(1))


def post_build() -> None:
    root=ROOT/'_build/html'
    p,s,data=get_built_data()
    cache={}
    for q in data['questions']:
        stem=q['sourceStem'];slug=re.sub(r'^\d+-','',stem)
        if stem not in cache:
            parser=Headings();parser.feed((root/'chapters'/slug/'index.html').read_text());cache[stem]=parser
        match=[hid for hid,label in cache[stem].heads if re.match(re.escape(q['sourceSection'])+r'\s',label)]
        assert len(match)==1 and match[0], (q['id'],q['sourceSection'],match)
        q['sourceHref']=chapter_url(stem)+'#'+match[0]
    payload=json.dumps(data,ensure_ascii=True,separators=(',',':')).replace('</','<\\/')
    s=re.sub(r'(<script id="question-data" type="application/json">).*?(</script>)',lambda m:m.group(1)+payload+m.group(2),s,flags=re.S)
    p.write_text(s)
    # Install on all entry routes so client-side navigation can discover new frames.
    script=f'<script defer src="{BASE}/exercise-resize.js"></script>'
    for page in root.rglob('*.html'):
        if page.name=='exercise-practice.html':continue
        h=page.read_text()
        if 'exercise-resize.js' not in h and '</body>' in h:
            page.write_text(h.replace('</body>',script+'</body>'))
    print('Resolved all 120 source-section anchors and installed same-origin iframe resizing.')


def check() -> None:
    expected,groups=data_and_groups()
    _,s,data=get_built_data()
    assert len(data['questions'])==120
    assert [q['id'] for q in data['questions']]==[q['id'] for q in expected['questions']]
    assert sum(t['writtenCount'] for t in data['topics'])==96
    root=ROOT/'_build/html'
    assert (root/'exercise-resize.js').is_file()
    assert '__QUESTION_DATA__' not in s
    assert 'fetch(' not in s and 'XMLHttpRequest' not in s, 'Practice should not send responses to a server'
    assert 'localStorage' in s and 'aria-live="polite"' in s
    answers=[q['answer'] for q in data['questions']]
    assert all(answers.count(i)>=20 for i in range(4))
    for q,e in zip(data['questions'],expected['questions']):
        assert q['options']==e['options'] and q['answer']==e['answer']
        assert q['explanation']==e['explanation']
        url,anchor=q['sourceHref'].split('#')
        rel=url.removeprefix(BASE).lstrip('/')
        h=Headings();h.feed((root/rel/'index.html').read_text());assert anchor in h.ids,(q['id'],anchor)
    for topic in data['topics']:
        tid=topic['id'];page=root/'exercises'/tid/'index.html'
        assert page.is_file(),str(page)
        parser=Headings();parser.feed(page.read_text())
        assert parser.details==topic['writtenCount'],(tid,parser.details,topic['writtenCount'])
        for gi,g in enumerate(groups[tid],1):
            for i in range(1,len(g['questions'])+1):
                assert f'practice-{tid}-{gi}-written-{i}' in parser.ids
        assert 'exercise-practice.html?topic='+tid in page.read_text()
    review=Headings();review.feed((root/'exercises/question-bank/index.html').read_text())
    assert review.details==120,review.details
    assert not (ROOT/'chapters/05-neural-encoding.md').exists()
    # Independent arithmetic checks for the specified teaching examples.
    import math
    assert math.isclose(6*math.exp(-1),2.207276647)
    assert 200/10==20 and -65+100/10==-55 and 10*(-50+65)==150
    assert math.isclose(1-math.exp(-50*.002),.095162581964)
    assert math.isclose(5+45*(1-1.5/5),36.5)
    assert math.isclose(3e8*100e-9/2,15) and math.isclose(42.8*.5,21.4)
    assert 800*600*3==1440000
    print('Exercise checks passed: 120 choices/explanations, 96 original questions/answers, all topic pages, numerical examples, and 120 exact source links.')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--post-build',action='store_true');ap.add_argument('--check',action='store_true');args=ap.parse_args()
    if args.post_build:post_build()
    elif args.check:check()
    else:generate()
