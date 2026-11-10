# Revision-Note Generation

How the app writes a revision note: the class revision note for a lesson, and a personalized revision note for each student. The code is the `post_class_review_pack` artefact type. Terms: [glossary.md](glossary.md). Learner state: [learner-model.md](learner-model.md).

## Place in the lesson

A lesson makes its content in this order. Teaching content is for the teacher. Learning material is for students.

| Order | Content | Kind | Level | Made from | Gate before use |
|---|---|---|---|---|---|
| 1 | Lesson plan | teaching content | class | the curriculum subtopic | teacher approves; the version freezes |
| 2 | Lesson note | teaching content | class | the approved plan, one section per step | teacher approves |
| 3 | Class revision note | learning material | class | the approved plan and the approved lesson note | teacher approves |
| 4 | Class test | learning material | class | the approved plan | teacher approves; approval sends it to students |
| 5 | Student revision note | learning material | learner | the approved class revision note and the student's learner state | teacher approves; then the student can read it |

- The API names these types `lesson-plan`, `lesson-note`, `revision-note` and `class-test` (`/content`).
- The app stores a revision note as an artefact of kind `post_class_review_pack`, and a class test as kind `diagnostic`.
- A teacher can revise any content by instruction before approval (`POST /content/{id}/revisions`).

## Background jobs

Generation runs as background jobs. The API writes a row to the MySQL `jobs` table and returns `202`. A job runner claims the row and runs the handler in its own process.

| Job kind | What it makes |
|---|---|
| `content.generate` | a lesson note, a class test, or a class revision note |
| `lesson_plans.generate` | a lesson plan |
| `assessments.generate_student_pack` | one student's revision note |
| `experiments.run_conditioned_execution` | the study conditions of one experiment |

A student's job starts only when both of these are true:

- The teacher has approved the class revision note.
- The student has submitted the class test, and the survey where the lesson asks for one.

A submission that arrives first waits. Approval of the class revision note starts the job of each waiting student.

## The revision note

The specification (`content_specifications`, seeded from `artefacts/specifications/seed.json`) sets the structure:

- One section per lesson objective, in the plan's order.
- Each section has a title, explanation blocks, worked examples, and practice.
- Each practice item carries the answer that the student checks against.

```python
class ReviewPackSection(BaseModel):
    section_id: str
    title: str
    lesson_objective_id: str
    blocks: list[ReviewPackBlock]             # block_type: explanation | worked_example | visual
    practice: list[ReviewPackPracticeItem]    # prompt, answer, worked_solution
    source_refs: list[str]
```

- The model writes only `explanation` and `worked_example` blocks.
- The generator attaches `visual` blocks from the lesson's own figures. It discards any visual block that the model writes.
- A visual block is an `image` (`url`, `caption`, `source_record_id`) or a `diagram_tikz` (`source_tikz`, `caption`).

## What a note is grounded in

A teacher chooses the expert sources for a class revision note (`ExpertSources`):

| Value | Evidence for each plan step |
|---|---|
| `lesson-note` (default) | the step's section of the approved lesson note; the plan's references for a step without one |
| `textbook` | the plan's references only |
| `both` | the lesson note section and the plan's references |

- A plan reference names a textbook record. The generator reads that record's text from `textbook_records`.
- Generation does no search. It reads only the lesson note and the records that the plan cites.
- The note records its grounding in its `artefact_refs`: the sources, the lesson note ID and version, the specification revision and the pipeline version.
- A student's revision note uses the grounding of the class revision note it adapts.

## Class revision note

```text
lesson plan + lesson note ─▶ request builder ─▶ write each section ─▶ checks + critic ─▶ repair ─▶ pending note
                             (one unit per       (concurrent model      (structural +        (up to 2
                              core plan step)     calls)                 prose)               retries)
```

1. The request builder makes one unit for each core step of the plan.
2. Each unit carries the step's objective, context and evidence (`BASE_REVIEW_PACK_POLICY`).
3. The generator writes all sections at the same time, with `ComposeSection` over `dspy.ReActV2`.
4. The generator attaches the step's figures to each section.
5. `FinaliseReviewPack` runs the checks and repairs the failed sections, up to `max_retries` times.
6. The note lands as `pending` until the teacher approves it.

## Student revision note

1. The personalizer reads the approved class revision note and the student's learner state.
2. It adapts each section to the state of the section's objective (`PERSONALISED_REVIEW_PACK_POLICY`).
3. It keeps the base section when the student has no state for that objective, or when fewer than two of their questions were marked for it (`thin_evidence`).
4. It runs its own checks, with one retry.
5. The note lands as `pending` until the teacher approves it.
6. It records the class note version it was made from (`artefact_refs.made_from`). A learner sees the note only while the class note stands approved at that version. When the teacher revises the class note, the learners' notes made from the old version are withheld, and approving the new version queues a new note for each of those learners.

The band rules and the model inputs are in [learner-model.md](learner-model.md).

## Checks

| Check | Meaning | Class | Student |
|---|---|---|---|
| `objective_coverage` | every objective has a section | yes | — |
| `scope_compliance` | no section for an objective outside the plan | yes | — |
| `source_refs_present` | each section cites a source | yes | — |
| `source_refs_valid` | each citation names evidence the section was given | yes | yes |
| `practice_is_checkable` | each section has practice, and each item has an answer | yes | — |
| `explanation_present` | each section's explanation blocks hold at least 300 characters | yes | — |
| `objective_preservation` | each section keeps its base objective | — | yes |
| `no_added_objectives` | no section serves an objective the base note lacks | — | yes |
| `content_grounding` | the critic finds no claim outside the evidence | yes | — |
| `internal_consistency` | the critic finds no contradiction | yes | — |
| `learner_facing_register` | the critic finds no text unfit for a student | yes | yes |

The first eight are structural checks in code. The last three come from a model critic (`SectionCritique`).

The study's rated notes passed the checks without `explanation_present` and `no_added_objectives`; the product added both afterwards. The study's own condition profiles do not run them.

## Pipeline versions

A pipeline version names the generation code by the date the team froze it. The specification is data and stays the same across versions.

| Version | Use |
|---|---|
| `2026-08-25` | the code that wrote the study's Part 1 notes |
| `2026-09-02` | the latest; the default for a new note |

A student's note uses the version that wrote its class revision note. Details: `apps/backend/docs/pipeline-versions.md`.

## Study conditions

The study uses the same pipeline. A `ConditionProfile` sets what each condition sends to the model.

| Condition | Context | Evidence | Checks and repair | Teacher gate |
|---|---|---|---|---|
| C0 | objectives only | — | — | — |
| C1 | + the plan's structure | — | — | — |
| C2 | + the plan's structure | lesson note | — | — |
| C3 | + the plan's structure | lesson note | yes | — |
| C4 | C3's note | lesson note | yes | yes |
| P0 | the approved base note, unchanged | — | — | — |
| P1 | the approved base note, personalized | cited evidence | yes | — |

- C4 makes no model call. It takes C3's note and waits for the teacher.
- P0 makes no model call.
- In a lesson under study, the C4 note is the class revision note that the teacher reviews.

The trace from an API call to the model call is in `apps/backend/docs/generation-call-stack.md`.

## Code

All paths are under `apps/backend/src/app/`.

| Concern | Path |
|---|---|
| Policies for class and student notes | `domains/artefacts/types/post_class_review_pack/domain/generation_policy.py` |
| Section schema | `domains/artefacts/types/post_class_review_pack/domain/section/schemas.py` |
| Grounding | `domains/artefacts/types/post_class_review_pack/application/grounding.py` |
| Units and evidence | `domains/artefacts/types/post_class_review_pack/application/request/` |
| Model modules | `domains/artefacts/types/post_class_review_pack/infrastructure/generation_wiring.py` |
| Checks and repair | `domains/artefacts/types/post_class_review_pack/application/revision/finalise_pack.py` |
| Student notes | `domains/artefacts/types/post_class_review_pack/application/student_pack_service.py` |
| Student job gate | `domains/artefacts/types/post_class_review_pack/application/learner_pack_gate.py` |
| Content API | `domains/content/api/routes.py` |
| Job kinds | `infra/jobs/kinds.py` |
| Study conditions | `domains/experiments/review_pack_study/conditions/profiles.py` |
