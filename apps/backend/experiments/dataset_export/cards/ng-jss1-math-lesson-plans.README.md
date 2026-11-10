---
pretty_name: Nigerian JSS1 Mathematics Lesson Plans
license: cc-by-4.0
language:
- en
tags:
- education
- mathematics
- lesson-plans
- classroom-data
- nigeria
- junior-secondary
size_categories:
- $size_category
configs:
- config_name: lesson_steps
  data_files:
  - split: train
    path: lessons/steps.csv
  default: true

---

# Nigerian JSS1 Mathematics Lesson Plans

Six mathematics lessons that a practising teacher planned and taught to a Junior Secondary School 1
(JSS1) class in Nigeria in the 2025/26 school year, following the national NERDC curriculum.
Each lesson is here as the teacher wrote it, as a cleaned transcription, as structured JSON, and
as a declared XML document valid against a RELAX NG grammar. The three lessons that ended in a
class exercise also carry the learners' de-identified, marked answers.

This is one of four datasets released with the LPCG framework from the MSc study *Design and Evaluation of a Lesson-Plan-Driven Framework for Curriculum-Constrained Generation and Personalisation of Learning Materials: A Case Study of Nigerian Junior Secondary Mathematics* (University of Lagos, 2026). The framework generates revision material from
these lessons; `ng-jss1-math-alignment-ratings` holds what it generated.

$file_count files, $size.

## Lessons

| lesson | term, week | topic | objectives | steps | class work |
| --- | --- | --- | ---: | ---: | --- |
| `t2-w09` | second term, week 9 | Simplification of Algebraic Terms | 3 | 5 | yes |
| `t3-w02` | third term, week 2 | Plane Shapes (2-D Shapes) | 3 | 5 | yes |
| `t3-w04` | third term, week 4 | Three Dimensional Shapes | 2 | 4 | |
| `t3-w05` | third term, week 5 | Three dimensional shapes II | 2 | 4 | yes |
| `t3-w06` | third term, week 6 | Construction | 5 | 6 | |
| `t3-w09` | third term, week 9 | Need for statistic | 2 | 4 | |

## Contents

| path | what it holds |
| --- | --- |
| `lessons/steps.csv` | one row per lesson step: its lesson, objective, planned content and minutes, with the path to the lesson document, the step's note, the cleaned transcription and the class work. Built from the files below; it adds nothing to them |
| `lessons/<lesson>.xml`, `lessons/lesson.rng` | each lesson as a declared document — objectives, steps and activities, with the notes each step draws on pinned by SHA-256 — and the grammar it is valid against |
| `notes/<lesson>/` | the lesson notes as the generator read them: transcribed, then corrected by hand |
| `transcripts/<lesson>/teacher.md` | the teacher's plan, transcribed as written |
| `transcripts/<lesson>/teacher-cleaned.md` | the same plan cleaned for reading; how it was read and corrected is recorded beside it |
| `transcripts/<lesson>/session-plan.json` | the plan as structured JSON |
| `transcripts/<lesson>/note.md`, `transcripts/<lesson>/notes/` | the lesson note as transcribed |
| `transcripts/<lesson>/classwork.md`, `classwork.xml`, `student-NN.md` | for the three lessons with class work: the exercise, each learner's transcribed and marked answers, and the same structured as XML |
| `transcripts/_render/` | typeset renders of the transcriptions (PDF and PNG) |
| `transcripts/SCHEMA.md` | how a transcription is laid out |
| `coding/student_work.json` | 19 student activities coded for whether each sets work, with the reason and whether a second reading agreed |
| `coding/note_headings.json` | 45 note headings coded by kind, including whether the region sets work, with the steps each belongs to |
| `coding/selection_set.json` | four authored lessons, not the teacher's, on which design choices were made, so that none was tuned on the six lessons the study measures |
| `PROVENANCE.json` | every file with its SHA-256, the repository commits it was read from, and which files differ from the study's record |

## The XML is the authoritative form

The transcriptions are the master record, but the XML documents are what the study's generator
read. They declare `sets_work` — which student activities set work — and that judgement was never
in the transcriptions, so a plan rebuilt from the transcriptions alone differs from the one the
study used. Each declared document is a migration of its plan, not a copy: across the six lessons
there are 69 differences of format, 4 places where the declaration corrects the transcription,
and 11 where the two disagree. Only one lesson, the pilot `t3-w05`, projects exactly.

## What differs from the study's record

$rewritten_count of the $file_count files differ from the study's own record, and
`PROVENANCE.json` marks each one.

- The school is not named. Where the study's record carried its abbreviation — in session ids and
  in file references — this release has `sch`.
- Each `classwork.xml` states the basis on which it is released, in place of an internal note.
- Two images that set a photograph of a page beside its transcription are not released. Every
  image that is released is a typeset render.

## Consent and privacy

The school's permission covers the publication of the teacher's plans and of the class work. Learners appear only as `student-01` to
`student-09`: their names were covered before the work was photographed, and no key links an id to
a child. The photographs the class work was transcribed from are not released.

## Limitations

- One teacher, one class, six lessons, JSS1 mathematics only.
- Plans and class work were transcribed from photographs. Uncertain readings are marked in the
  transcriptions and should be read as uncertain.
- The three lessons with class work cover at most nine learners.

## Related datasets

- [`ng-jss1-math-curriculum`](https://huggingface.co/datasets/tosinamuda/ng-jss1-math-curriculum): the curriculum and scheme of work the lessons follow
- [`ng-jss1-math-textbook-linkage`](https://huggingface.co/datasets/tosinamuda/ng-jss1-math-textbook-linkage): an open JSS1 textbook linked to the curriculum's objectives
- [`ng-jss1-math-alignment-ratings`](https://huggingface.co/datasets/tosinamuda/ng-jss1-math-alignment-ratings): what the framework generated from these lessons, and how it was rated

## Citation

```bibtex
@mastersthesis{amuda2026lpcg,
  author = {Amuda, Tosin},
  title  = {Design and Evaluation of a Lesson-Plan-Driven Framework for Curriculum-Constrained Generation and Personalisation of Learning Materials: A Case Study of Nigerian Junior Secondary Mathematics},
  school = {University of Lagos},
  type   = {MSc dissertation},
  year   = {2026}
}
```
