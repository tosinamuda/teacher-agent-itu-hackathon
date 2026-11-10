# Curriculum Model

The curriculum sets the scope of every lesson plan and of all content made from it. The source is the NERDC Nigerian curriculum for JSS1 Mathematics. The `curriculum`, `school` and `teaching` domains hold it.

Terms: [glossary.md](glossary.md). Tables: [data-model.md](data-model.md).

## Hierarchy

```
Subject ─< Topic (one week) ─< Subtopic (the content of a lesson) ─< Session (one 40-minute lesson)
                                         ├─< Performance objective
                                         └─< Knowledge component (KC)
```

| Level | NERDC column | Model (table) | Key | Example |
|---|---|---|---|---|
| Subject | — | `CurriculumSubject` (`curriculum_subjects`) | `name` | `Mathematics` |
| Topic | TOPIC | `CurriculumTopic` (`curriculum_topics`) | `topic_key` | `jss1-math-estimation` |
| Subtopic | CONTENT | `CurriculumSubtopic` (`curriculum_subtopics`) | `subtopic_id` | "Graphical presentation of data" |
| Session | — | `ClassSession` (`class_sessions`) | `session_id` | `session-jss1-math-whole-numbers-quantitative-reasoning` |
| Performance objective | PERFORMANCE OBJECTIVES | `CurriculumPerformanceObjective` (`curriculum_performance_objectives`) | `curriculum_objective_id` | `…-place-values-po01` |
| Knowledge component | EVALUATION GUIDE | `KnowledgeComponent` (`knowledge_components`) | `kc_code` | `JSS1-GMATH-ASF-004` |

- A topic carries `subject`, `track`, `grade`, `term` and `week`. Each is a foreign key to a catalogue table (`curriculum_subjects`, `curriculum_tracks`, `curriculum_grades`, `curriculum_terms`).
- A topic can belong to a theme (`CurriculumTheme`, through `theme_id`).
- A subtopic also stores the NERDC teacher activities, student activities, materials and evaluation guide as JSON.
- A KC has a `description` (the testable outcome), a `bloom_level`, and a UUID `id` for joins.

## Objectives

Three kinds of objective, from the curriculum to the lesson:

```
Performance objective  →  Atomic objective (AO)  →  Lesson-plan objective
(NERDC, per subtopic)     (one teachable unit)      (in the plan, lop01, lop02, …)
```

| Objective | Where it lives | Key |
|---|---|---|
| Performance objective | `curriculum_performance_objectives`, one row per objective | `curriculum_objective_id` |
| Atomic objective | `ao_textbook_objective_links` (`expert_content`) | `ao_id`, with its `curriculum_objective_id` |
| Lesson-plan objective | the plan's `lesson_plan_objectives`, and `plan_version_objectives` | `lesson_objective_id`, with its `curriculum_objective_id` |

- Each lesson-plan objective names the curriculum objective it teaches.
- The AO is the unit that links a curriculum objective to textbook records. See [textbook-curriculum-linkage.md](textbook-curriculum-linkage.md).
- A class test question names the lesson-plan objective it tests (`exit_ticket_items.lesson_objective_id`). It can also name a KC.

## Knowledge components

- The `knowledge_components` table holds the curriculum's KCs, one set per subtopic.
- Lesson-plan drafting derives its own candidate KCs for each atomic objective (`CandidateKC`).
- A candidate KC lists `prerequisite_kc_ids`. The drafter checks that these form a DAG inside one plan.
- The learner model keys on lesson-plan objectives, not on KCs. See [learner-model.md](learner-model.md).

## Teaching schedule

The `school` and `teaching` domains record when a subtopic is taught:

```
TermClassSubject ─< SchemeOfWork (one week) ─< LessonPeriod ─▶ CurriculumSubtopic
                                                    │
                                                    └─< LessonDelivery ─▶ PlanVersion
```

| Model | Table | Domain |
|---|---|---|
| `TermClassSubject` | `term_class_subjects` | `school` |
| `SchemeOfWork` | `scheme_of_work` | `teaching` |
| `LessonPeriod` | `lesson_periods` | `teaching` |
| `LessonDelivery` | `lesson_deliveries` | `teaching` |

A lesson delivery joins a teacher workspace, a lesson period and the plan version taught in it.

## How the curriculum limits generation

- A lesson plan must cover the curriculum objectives of its subtopic.
- Content made from the plan stays inside the plan's objectives. The `scope_compliance` check enforces this for revision notes. See [revision-note-generation.md](revision-note-generation.md).
- When a subtopic has no textbook linkage, the plan drafter works from the curriculum text alone (`curriculum_only`).

## Code

| Concern | Path |
|---|---|
| Curriculum models | `apps/backend/src/app/domains/curriculum/models/` |
| Teaching schedule models | `apps/backend/src/app/domains/teaching/models/syllabus.py` |
| Subject offerings | `apps/backend/src/app/domains/school/models/subject_offerings.py` |
| Plan objective schema | `apps/backend/src/app/domains/artefacts/types/lesson_plan/drafting/schemas/session_plan.py` |
