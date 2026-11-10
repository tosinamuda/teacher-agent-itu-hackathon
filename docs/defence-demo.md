# Project defence demo

A 15-minute demo of the teacher's web app on **staging**. A teacher prepares one lesson end to end: she reuses a lesson plan and its lesson note, brings in the class's results from the evaluation, and asks for a revision note, learners' own notes and a slide deck. Then the panel sees the evidence the study produced.

The plan, the lesson note and the class results are reused, so they appear at once. The revision note, the learners' notes and the slides are written by a model while the demo runs, so they are started together and the study is shown while they finish (see [Waiting on a model](#waiting-on-a-model)). A screenshot walkthrough of these steps is in `docs/demo/defence-demo-walkthrough.pdf`.

## What the demo shows

| Part | # | Minutes | Segment |
| --- | --- | --- | --- |
| A | 1 | 1 | Frame |
| A | 2 | 2 | Reuse a lesson plan and approve it |
| A | 3 | 1 | Reuse its lesson note |
| A | 4 | 1 | Bring in the class's results |
| A | 5 | 2 | A revision note |
| A | 6 | 2 | Each learner's own note |
| A | 7 | 3 | Plugins: switch on slides, show the class deck |
| B | 8 | 3 | The study |

Say first: the framework (CLCG) is the design. The prototype is the software that applies it. The study is the prototype configured for JSS1 mathematics and scored by human raters. The lesson in the demo is one of the study's own lessons.

## Waiting on a model

A revision note, a learner's note and a slide deck each take a few minutes. Different materials run at the same time, so start the revision note and the slides together, then go on to the class results and the study while they finish. Only one run of a kind goes at a time for a lesson.

## Before the day

1. **Check both ends.**

   ```bash
   curl -s -o /dev/null -w "staging api %{http_code}\n" https://lpcg-staging-api.tosinamuda.com/api/health
   curl -s -o /dev/null -w "staging frontend %{http_code}\n" https://lpcg-staging.tosinamuda.com
   ```

2. **Choose the demo lesson**: a lesson in the class with no plan. Reusing the plan asks which curriculum objective each plan objective serves; choose the first for the first two and the second for the third. Leave the lesson untouched. Start it over first if it was used (see [Start a lesson again](#start-a-lesson-again)).
3. **In Settings**, turn **Slides** off so the demo can switch it on.
4. **Run the whole demo once** on the day before, so the models, the keys and the queue are known to work. Start the lesson over afterwards.
5. **Record a one-minute screen video** of segments 5 to 7 with the finished materials as the fallback.

Do not stand waiting on a model in the defence. If a page is slow, switch to the video.

## The sequence

### 1. Frame (1 minute)

Say the three levels above. Show one slide with them. Do not demo yet.

### 2. Reuse a lesson plan and approve it (2 minutes)

Sign in as the teacher. Open **Lessons**, pick the term, the week and the demo lesson. Its plan row reads **Create plan**, with the quiet link **Use an existing plan**.

1. Click **Use an existing plan**. The page names the lesson it is for. Choose **A plan file** and `docs/demo/study-week9-plan.json` from this repository, then **Use this plan**. (The page also takes an approved plan of another lesson.)
2. The plan opens as a draft. **Basis for the plan** is closed, and the steps open one at a time. Read the objectives and open a step.
3. In the right-hand panel, **Needs you** asks **Approve the plan?** Tick that the plan meets the lesson-plan requirements, then click **Approve**.

Say: the plan keeps the study's steps and the wording of its objectives. The teacher reads it and approves it as she would any plan. Approval unlocks the class materials.

### 3. Reuse its lesson note (1 minute)

On the lesson home, the lesson note row reads **Create**, with the link **Use an existing note**. Click it. Choose **The evaluation's lesson note**, pick **Simplification of algebraic expressions** (only a lesson whose note has every step of this plan is listed), and click **Use this note**. The note is the study's own lesson note, copied onto this lesson's plan. Read a step and approve it.

Say: this is the lesson note the study used, written by a teacher. It is reused, not written again. It has four teaching steps; the plan's fifth step is the evaluation, which has nothing to teach.

### 4. Bring in the class's results (1 minute)

The **Class evidence** row reads **Import class results**. Open it. Only the evaluation's lessons whose objectives match this lesson's plan are offered. Click **Import class results**.

Point at: each of the study's learners with a band, the marks, the teacher's total on the script and the misconception codes. The class evidence row now reads **Imported from the evaluation · 8 learners**.

Say: these are the study's own marks, matched to this plan's objectives.

### 5. A revision note (2 minutes)

On the lesson home, click **Create** on **Revision note**, and **Create** on **Slides** once they are switched on. The **In progress** panel names what is being made. Go on with segments 4 and 6 while they run. When the revision note finishes, open it, read a section and approve it.

Say: each section is written for one objective of the plan and checked against it, and the teacher approves the note before any learner sees it.

### 6. Each learner's own note (2 minutes)

Back on **Class evidence**, the panel under the imported results pairs three class learners with three study learners: a strength, a middle and a gap. The revision note must be approved first. Click **Make their notes**. Each learner takes those marks as their own, and their note is written.

On the lesson home, **Personalised notes** reads **0 approved · 3 to review**. Open one note from the extend band and one from the remediate band. They teach the same objective at different levels. Approve one.

Say: the learners are the class's own; the marks are the study's real marks. Each note starts from the class note the teacher approved and is adapted to those results.

### 7. Plugins: switch on slides and show the class deck (3 minutes)

Open **Settings**. Under **Plugins**, each material is a card. The built-in ones (lesson plan, lesson note, revision note, class test) are always on. **Slides** is off. Switch it on. Under **Available to add**, **Flashcards** has not been added yet; click **Add** to show it join the others.

Back on the lesson home, **Slides** is now listed under **Class materials**. Click **Create**, and open it when it finishes and move through three slides. Each has a title, at most five short points and speaker notes.

Say: a plugin holds no code. It names the checks and the writer, and the server runs them. A teacher switches a plugin on for herself alone. The deck is class-level. It is not personalised per student.

### 8. The study (3 minutes)

Sign out, then sign in with the **researcher** code: the teacher account cannot open the study pages. Open the study results: the four conditions compared on the three criteria. Then the walkthrough of the lessons the study used. Open one experiment. To show the rater's side, sign out and in with the rater code and open the rater's queue: the rater sees notes to review, not the condition that wrote them.

Do not quote a number that is not in the thesis. Read it off the page and match it to Chapter 6.

## If something fails

| Symptom | What to do |
| --- | --- |
| A page is slow or blank | Switch to the screen video. |
| A material is still running | Show the study (segment 8), then come back. Use the screen video if it is still not done. |
| **Make their notes** makes nothing | The class revision note is not approved. Approve it, then click again. |
| The import offers no lesson | The plan lacks the study's objectives. Use the plan file `docs/demo/study-week9-plan.json`. |

## Likely questions

| Question | Answer |
| --- | --- |
| Is this real or a recording? | It is real. The revision note, the learners' notes and the slides are written live by the engine, and each passes the same checks. |
| Was real student data used? | The class results are the study's own marks for its real, de-identified learners. The three class learners who stand in for them are seeded accounts. |
| Does it work outside mathematics? | The same plugins ran on English and Basic Science decks, which were not rated. See the thesis (Chapter 5, with Chapter 7's open work). |
| What stops the model writing something wrong? | The checks and the teacher's approval. A passing check is evidence about particular requirements, not a guarantee. |
| Why plugins and not code? | A new material needs a specification, skills and tool names, not new application code. `docs/artefact-plugins.md`. |
| Why OpenCode? | `apps/backend/experiments/lesson_note_engine/HARNESSES.md`. |
| What does "harness" mean here? | `docs/glossary.md`, section O. |

## Start a lesson again

To rehearse from an empty lesson, clear what was made for it. In the app, open the lesson and click **Start this lesson over** at the bottom of the lesson home. It says what would go and clears nothing until you click **Clear this lesson**. The lesson, the class and its learners stay.

From a terminal, `reset_lesson.py` does the same. Run it with no flag first: it lists what would go and clears nothing.

```bash
cd apps/backend
uv run python scripts/reset_lesson.py <lesson id>
uv run python scripts/reset_lesson.py <lesson id> --yes
```

Both refuse a lesson the study ran on. Both clear the logged model calls of the lesson's drafts with the rest.

## After the demo

The demo lessons are test data. Approved materials stay approved. No cleanup is needed.
