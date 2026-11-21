function shuffle(items) {
  for (let i = items.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [items[i], items[j]] = [items[j], items[i]];
  }
  return items;
}

function isCorrect(objective, answers, index) {
  return index >= 0 && answers[index] === objective.questions[index].answer;
}

function conceptStatus(objective, answers) {
  const last = answers.length - 1;
  if (last >= 1 && isCorrect(objective, answers, last) && isCorrect(objective, answers, last - 1)) {
    return 'mastered';
  }
  return answers.length === objective.questions.length ? 'review' : 'active';
}

function sameAnswers(a, b) {
  return a.length === b.length && a.every((answer, index) => answer === b[index]);
}

export function startAdaptivePractice(topic, objectives, params) {
  const get = (name) => document.getElementById(`adaptive-${name}`);
  const storageKey = `neai-adaptive-practice-v1:${topic}`;
  let storageAvailable = true;
  let records = {};
  let objective;
  let showResult;
  let currentQuestionId;
  let choiceOrder;

  function loadRecords() {
    if (!storageAvailable) return records;
    try {
      const raw = JSON.parse(localStorage.getItem(storageKey) || '{}');
      return Object.fromEntries(objectives.flatMap((item) => {
        const record = raw?.[item.id];
        if (record?.sig !== item.sig || !Array.isArray(record.answers)) return [];
        if (record.answers.length > item.questions.length || !record.answers.every((answer) =>
          Number.isInteger(answer) && answer >= 0 && answer < 4)) return [];
        return [[item.id, record]];
      }));
    } catch (error) {
      if (error instanceof SyntaxError) return {};
      storageAvailable = false;
      return records;
    }
  }

  function answersFor(item) {
    return records[item.id]?.answers ?? [];
  }

  function nextActive() {
    return objectives.find((item) => conceptStatus(item, answersFor(item)) === 'active');
  }

  function resumeResult() {
    if (!objective) return false;
    const answers = answersFor(objective);
    return answers.length > 0 && !isCorrect(objective, answers, answers.length - 1);
  }

  function recordAnswers(answers) {
    const prior = answersFor(objective);
    records = loadRecords();
    const latest = answersFor(objective);
    if (!sameAnswers(prior, latest)) {
      showResult = resumeResult();
      render(true);
      return false;
    }
    records[objective.id] = { sig: objective.sig, answers };
    if (storageAvailable) {
      try {
        localStorage.setItem(storageKey, JSON.stringify(records));
      } catch {
        storageAvailable = false;
      }
    }
    return true;
  }

  function openConcept(item, focus = false) {
    objective = item;
    showResult = resumeResult();
    currentQuestionId = undefined;
    const url = new URL(location.href);
    if (item) url.searchParams.set('concept', item.id);
    else url.searchParams.delete('concept');
    history.replaceState(null, '', url);
    render(focus);
  }

  function renderProgress() {
    const statuses = objectives.map((item) => conceptStatus(item, answersFor(item)));
    const mastered = statuses.filter((status) => status === 'mastered').length;
    get('progress-label').textContent = `${mastered} of ${objectives.length} concepts mastered`;
    get('progress').max = objectives.length;
    get('progress').value = mastered;
    get('concept-list').replaceChildren(...objectives.map((item, i) => {
      const li = document.createElement('li');
      const button = document.createElement('button');
      const status = document.createElement('span');
      const answers = answersFor(item);
      button.type = 'button';
      if (item === objective) button.setAttribute('aria-current', 'step');
      status.className = 'concept-status';
      status.dataset.status = statuses[i];
      if (statuses[i] === 'mastered') status.textContent = 'Mastered';
      else if (statuses[i] === 'review') status.textContent = 'Ready to review';
      else status.textContent = answers.length ? 'In progress' : 'To do';
      button.append(item.title, status);
      button.addEventListener('click', () => openConcept(item, true));
      li.append(button);
      return li;
    }));
    return mastered;
  }

  function renderChoices(question, selected) {
    if (question.id !== currentQuestionId) {
      currentQuestionId = question.id;
      choiceOrder = shuffle(question.options.map((_, index) => index));
    }
    get('question').textContent = question.prompt;
    get('options').replaceChildren(...choiceOrder.map((index) => {
      const label = document.createElement('label');
      const input = document.createElement('input');
      const text = document.createElement('span');
      label.className = 'option';
      input.type = 'radio';
      input.name = 'adaptive-choice';
      input.value = String(index);
      input.required = true;
      input.checked = index === selected;
      text.className = 'option-text';
      text.textContent = question.options[index];
      if (showResult && (index === selected || index === question.answer)) {
        const correct = index === question.answer;
        label.dataset.state = correct ? 'correct' : 'wrong';
        const note = document.createElement('span');
        note.className = 'state-text';
        note.textContent = correct ? 'Correct answer' : 'Your choice';
        text.append(note);
      }
      label.append(input, text);
      return label;
    }));
  }

  function render(focus = false) {
    const mastered = renderProgress();
    const answers = objective ? answersFor(objective) : [];
    const status = objective ? conceptStatus(objective, answers) : null;
    const index = showResult ? answers.length - 1 : answers.length;
    const question = (showResult || status === 'active') ? objective?.questions[index] : null;
    const correct = Boolean(showResult && isCorrect(objective, answers, index));
    get('storage-warning').hidden = storageAvailable;
    get('concept').hidden = !objective;
    get('form').hidden = !question;
    get('choices').disabled = showResult;
    get('submit').parentElement.hidden = showResult;
    get('feedback').hidden = !showResult;
    get('lesson').hidden = !showResult || correct;
    get('summary').hidden = Boolean(question);
    get('next').hidden = !showResult && (!objective || status === 'active');
    get('repeat').hidden = status !== 'review' && (status !== 'mastered' || showResult);

    if (objective) {
      const number = objectives.indexOf(objective) + 1;
      get('concept').textContent = `Concept ${number} of ${objectives.length} · ${objective.title}`;
    }
    if (!question) {
      if (objective) {
        get('summary-title').textContent = status === 'mastered' ? 'Concept mastered' : 'More review needed';
        get('summary-text').textContent = status === 'mastered'
          ? 'You answered two different questions in a row correctly.'
          : 'You have tried every question for this concept. Restart it to practice again.';
        get('next').textContent = 'Continue chapter';
      } else {
        get('summary-title').textContent = mastered === objectives.length ? 'Chapter practice mastered' : 'Chapter practice summary';
        get('summary-text').textContent = mastered === objectives.length
          ? 'You mastered every concept in this chapter.'
          : 'Open the concept list to revisit the topics marked Ready to review.';
      }
      if (focus) get('summary-title').focus();
      return;
    }

    renderChoices(question, answers[index]);
    if (!showResult) {
      if (focus) get('question').focus();
      return;
    }
    get('feedback').dataset.result = correct ? 'correct' : 'wrong';
    get('feedback-title').textContent = status === 'mastered' ? 'Concept mastered' : correct ? 'Correct' : 'Not quite';
    const answer = question.options[question.answer];
    get('explanation').textContent = correct ? question.explanation : `Correct answer — ${answer}. ${question.explanation}`;
    get('source').href = question.sourceHref;
    get('source').textContent = question.sourceLabel;
    if (correct) {
      get('next').textContent = status === 'active' ? 'Check with another question' : 'Continue chapter';
    } else {
      const misses = answers.filter((_, i) => !isCorrect(objective, answers, i)).length;
      const lessonIndex = Math.min(misses, objective.lessons.length) - 1;
      const lesson = objective.lessons[lessonIndex];
      get('lesson-title').textContent = `Mini-lesson ${lessonIndex + 1} · ${lesson.title}`;
      get('lesson-body').textContent = lesson.body;
      get('next').textContent = status === 'active' ? 'Try a new question' : 'Continue chapter';
    }
    if (status === 'review') {
      get('summary').hidden = false;
      get('summary-title').textContent = 'More review needed';
      get('summary-text').textContent = 'You have tried every question for this concept. Restart it to practice again.';
    }
    if (focus) get('feedback-title').focus();
  }

  get('form').addEventListener('submit', (event) => {
    event.preventDefault();
    const choice = get('form').querySelector('input:checked');
    if (!choice || !objective || showResult) return;
    if (recordAnswers([...answersFor(objective), Number(choice.value)])) {
      showResult = true;
      render(true);
    }
  });
  get('next').addEventListener('click', () => {
    if (conceptStatus(objective, answersFor(objective)) === 'active') {
      showResult = false;
      render(true);
    } else {
      openConcept(nextActive(), true);
    }
  });
  get('repeat').addEventListener('click', () => {
    if (recordAnswers([])) openConcept(objective, true);
  });
  window.addEventListener('storage', (event) => {
    if (event.key !== storageKey && event.key !== null) return;
    const prior = objective ? answersFor(objective) : null;
    records = loadRecords();
    if (objective) {
      if (sameAnswers(prior, answersFor(objective))) renderProgress();
      else {
        showResult = resumeResult();
        render();
      }
    } else {
      openConcept(nextActive());
    }
  });

  records = loadRecords();
  get('content').hidden = false;
  openConcept(objectives.find((item) => item.id === params.get('concept')) ?? nextActive());
}
