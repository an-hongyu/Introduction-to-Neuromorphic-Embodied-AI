# Exercise center maintenance

`question_bank.py` is the authored bank of 120 English multiple-choice questions.
Each row identifies a real source section and supplies one correct option,
three distractors, and an explanation. The builder rotates correct-option
positions; the browser shuffles question order without changing the answer key.

The chapter-end written exercises and book-end solutions remain the canonical
sources. `tools/build_exercise_center.py` extracts them, verifies one answer per
question, and produces the standalone exercise section with collapsed answers.
It also adds contextual practice links without removing or renumbering the
original exercises. Chapter 5 remains removed. Generated pages are overwritten
from these sources on every build; do not hand-edit them.

Build order:

1. `python tools/build_exercise_center.py`
2. Run the existing book build and spatial redirect publisher.
3. `python tools/build_exercise_center.py --post-build`
4. Run existing book checks, then `python tools/build_exercise_center.py --check`.

The app has no third-party scripts, account system, or answer-submission endpoint.
Progress stays in versioned browser localStorage; unavailable storage falls back
to memory. The first attempt is preserved across retries; revealing an answer
before attempting it cannot earn first-try credit. Answers are intentionally
available to the client: this is self-study, not secure examination software.

`assets/exercise-practice.template.html` implements native radio-button questions,
immediate feedback, explanations, topic/type filters, question navigation,
shuffle, scoped reset, and desktop/mobile layouts. `assets/exercise-resize.js`
accepts bounded resize messages only from the matching same-origin frame.
The readable question-bank page and original worked-answer dropdowns also work
without JavaScript. Existing images, videos, notebooks, and cover are unchanged.
