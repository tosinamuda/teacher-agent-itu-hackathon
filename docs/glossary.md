# Glossary — terms, codes, and their code mapping

The vocabulary of the thesis and the code. The short codes `H1`, `H2`, `C0`–`C4` and `P0`–`P1` are the same everywhere. The research design, the database, the blinded packets and the Python enums all use them. Tables: [data-model.md](data-model.md). Experimental design: the pre-registration, which is not in this repository.

---

## A. Research question, hypotheses, codes

| Term | Meaning |
| --- | --- |
| **RQ** | Does a teacher-confirmed lesson plan, compared with curriculum objectives alone, improve LLM-generated revision notes? Can those notes be personalised for each learner inside the curriculum and teacher constraints? |
| **RQ1** | Class-level generation: does the lesson plan improve the class revision note? The C1 vs C0 contrast of H1. |
| **RQ2** | Grounding and review: do explicit source evidence, AI validation and teacher review improve reliability? The C2, C3 and C4 steps of H1. |
| **RQ3** | Personalisation: does objective-level learner evidence improve suitability over the same approved base note for every student? H2. |
| **H1** | Base-note quality. Notes generated from a lesson plan rate higher than notes from objectives alone. Grounding and validation add further gains. `Hypothesis.H1`. |
| **H2** | Personalised fit. Notes personalised from objective-indexed learner state suit the focal learner better than the unchanged base note, and keep the approved objectives. `Hypothesis.H2`. |

`Hypothesis` has two values: `H1` and `H2`.

---

## B. H1 conditions — C0…C4 (the ablation)

A `ConditionProfile` defines each condition. It sets the context the generator reads, the source evidence, the validation, and the teacher gate. Code: `experiments/review_pack_study/conditions/profiles.py`.

| Code | Name | Adds over the previous code | Profile |
| --- | --- | --- | --- |
| **C0** | Objective-only baseline | Subject, grade, topic and lesson objectives only | `context.generation_unit="objective"`, retrieval and validation off |
| **C1** | Lesson-plan specification | The frozen lesson plan: objectives, sequence, instructional events, assessment points, materials, entry behaviour, student tasks | `generation_unit="lesson_step"`, retrieval off |
| **C2** | + Source grounding | Scoped evidence from the approved lesson note, with required source references. A step with no note uses the plan's references. | `retrieval.enabled=True`, `evidence_scope="objective"`, up to 3 items per unit |
| **C3** | + AI validation | Structural checks, an LLM critic, and up to 2 repair rounds | `validation.enabled=True`, `max_retries=2` |
| **C4** | + Teacher validation | C3's note, put through the teacher's review gate | `teacher_validation.enabled=True`, `generated_by=C3` |

- The central comparison is C1 vs C0.
- `h1_main_condition_codes()` returns C0–C3. H1 rater packets and statistics use only these codes.
- C4 is teacher-governance evidence. The teacher's decision is the `review_status` of the C4 artefact.

Two different teacher actions:

- The teacher confirms the lesson plan before generation. All conditions from C1 to C4 read the same frozen plan.
- The teacher validates the generated note only in C4.

---

## C. H2 conditions — P0…P1 (personalisation)

| Code | Name | Behaviour | Profile |
| --- | --- | --- | --- |
| **P0** | Non-personalised base | The approved base note, unchanged. No LLM call. | `personalisation.mode="reuse_base"` |
| **P1** | Objective-indexed personalised note | The base note adapted to the learner's objective-indexed state. Keeps the base objectives. Calls the LLM. | `personalisation.mode="objective_indexed"`, validation checks `objective_preservation`, `source_refs_valid`, `learner_facing_register` |

---

## D. The shared base pack — how C4 relates to P0/P1

P0 and P1 start from one approved base note.

- In the condition study, the base is the C3 note of the experiment's first draw. The system approves it once its validation runs. Code: `experiments/application/h2_base_pack.py`.

- In the teacher's flow, the base is the C4 note after the teacher approves it. Learners' notes wait for that approval. Code: `experiments/application/c4_base_pack.py`, `post_class_review_pack/application/learner_pack_gate.py`.
- P0 is the base, unchanged. P1 is the base, personalised.

```text
H1:  C0   C1   C2   C3 ──► C4 (teacher gate over C3's note)
                    │
                    ▼  approved base note
H2:           P0 (base, no LLM)   vs   P1 (base + learner state, LLM)
```

---

## E. Curriculum & planning artefacts (the noun chain)

Detail: [curriculum-model.md](curriculum-model.md).

| Term | Meaning | Code mapping |
| --- | --- | --- |
| **Curriculum** | The NERDC curriculum: topics, subtopics and performance objectives. The binding constraint. | `curriculum_topics`, `curriculum_subtopics` |
| **Scheme of work** | The term's teaching sequence. It places each subtopic in a lesson period. | `scheme_of_work`, `lesson_periods` |
| **Curriculum objective** | A performance objective of a subtopic. What the lesson must cover. | `curriculum_performance_objectives.curriculum_objective_id` |
| **Atomic objective (AO)** | One teachable objective split from a curriculum objective. The unit of the textbook linkage. | `ao_textbook_objective_links.ao_id` |
| **Lesson-plan objective** | The objective in the plan, keyed `lopNN`, with its `curriculum_objective_id`. The unit of learner state and rating. | `plan_version_objectives.lesson_objective_id` |
| **Knowledge component (KC)** | One unit of knowledge under a subtopic. | `knowledge_components.kc_code` |
| **Lesson plan** | The teacher-confirmed specification for one lesson period. The model drafts it or the teacher enters it. The teacher approves it. | `lesson_plans`, `plan_versions`, kind `lesson_plan` |
| **Session plan** | The validated payload of a lesson plan: objectives, steps, assessments, references, materials. | `PlanVersion.session_plan` |
| **Lesson note** | The teacher's note for each plan step. The default source evidence for C2, C3 and P1. | kind `lesson_note` |
| **Class test** | The questions students answer after the lesson. The evidence for learner state. | kind `diagnostic`, `exit_ticket_items` |
| **Revision note** | The generated review material for learners. The thesis also calls it the (post-class) review study pack. | kind `post_class_review_pack`, `PostClassReviewPack` |
| **Class revision note** / **base pack** | The revision note for the whole class. H2 personalises it. | `scope="class_level"` |
| **Personal revision note** | One learner's adapted revision note. | `scope="learner_level"` |
| **Teaching content** / **learning material** | Content for the teacher (lesson plan, lesson note) and content for learners (class test, revision note). | `content.domain.types.Audience` |
| **Content specification** | The versioned rules for one content kind. | `content_specifications` |

---

## F. Learner state & personalisation

Detail: [learner-model.md](learner-model.md).

| Term | Meaning | Code mapping |
| --- | --- | --- |
| **Objective-indexed learner state** | One state record per lesson-plan objective. `LearnerStateService` derives it from the class-test submission. No table stores it. | `ObjectiveLearnerState` in `learner_state/domain/models.py` |
| **Band** | The instructional band of one objective: `remediate` (mastery < 0.50), `reinforce` (0.50 to < 0.75), `extend` (≥ 0.75). | `ObjectiveBand`, `_band_for_mastery` |
| **Focal learner** | A learner that an H2 execution personalises for. | `experiment_focal_cases` |
| **Focal case type** | The band mix of a focal learner. | `FocalCaseType`: `remediate`, `reinforce`, `extend`, `mixed_or_misconception` |
| **Misconception code** | A short code for one error. A wrong option carries one. The study's classwork coding carries one. | `exit_ticket_items.option_misconceptions`, `ObjectiveLearnerState.misconception_code`, `study_classwork_answers.misconception_code` |
| **Learner-state snapshot** | The frozen learner state that a P1 generation read. | `learner_state_snapshot` on `experiment_focal_cases` and `artefact_plans` |

---

## G. Assessment & diagnostic

| Term | Meaning | Code mapping |
| --- | --- | --- |
| **Class-test item** | One multiple-choice question for one lesson-plan objective, with a misconception code per wrong option. | `ExitTicketItem` |
| **Class-test submission** | One student's answers and survey for one plan version. | `exit_ticket_submissions.results` |
| **Student response** | The option a student chose. The chosen option names the misconception. | `student_item_responses`: `choice`, `is_correct`, `score` |
| **Post-class survey** | Confidence and perceived difficulty per objective, and interest and affect for the lesson, each 1–5. | `ObjectiveLearnerState.confidence_score`, `difficulty_score`, `SessionSurvey` |
| **Study classwork** | The MSc study's constructed-response classwork: questions, marked scripts, coded answers. | `study_classwork_questions`, `study_classwork_scripts`, `study_classwork_answers` |

---

## H. Textbook & grounding

Detail: [textbook-curriculum-linkage.md](textbook-curriculum-linkage.md).

| Term | Meaning | Code mapping |
| --- | --- | --- |
| **Textbook record** | One passage, figure or exercise from a source textbook, with its heading path, text and asset refs. | `textbook_records` |
| **AO↔textbook linkage** | The curated map from atomic objectives to textbook records, with a role per record and an assessment per objective. | `ao_textbook_linkages`, `ao_textbook_objective_links`, `ao_textbook_record_links` |
| **Source evidence** | The scoped excerpts a grounded condition may cite, each with a `source_ref`. | `SourceEvidenceItem` |
| **Expert sources** | What a revision note is grounded in: the lesson note (default), the plan's textbook references, or both. | `ExpertSources`: `lesson-note`, `textbook`, `both` |
| **Figure** | A TikZ drawing in stored content. The server draws it once and serves it as SVG. | `figures`, `/figures/<sha256>.svg` |

---

## I. Generation & optimisation

Detail: [revision-note-generation.md](revision-note-generation.md), [architecture.md](architecture.md).

| Term | Meaning | Code mapping |
| --- | --- | --- |
| **ConditionProfile** | The frozen config that defines a condition. DSPy holds no condition logic. | `experiments/review_pack_study/conditions/policies.py`, `profiles.py` |
| **Generation policy** | The product half of a profile: context, retrieval, validation, personalisation, execution. | `ReviewPackGenerationPolicy` in `post_class_review_pack/domain/generation_policy.py` |
| **Request builder** | Turns the lesson plan, the policy and the learner state into the request the DSPy modules read. | `BaseReviewPackRequestBuilder`, `PersonalisedReviewPackRequestBuilder` |
| **Validator** | The checks after generation, then repair. Structural checks: objective coverage, scope compliance, source references, objective preservation, checkable practice. Prose checks by an LLM critic: content grounding, internal consistency, learner-facing register. | `ReviewPackStructuralValidator`, `SectionCritic`, `ValidationCheck` |
| **Generation pipeline** | The dated version of the generation code that wrote a note. | `post_class_review_pack/domain/pipeline.py` |
| **GEPA** | A DSPy prompt optimiser. Its checkpoint drives the lesson-plan generator. It is separate from the C0–C4 ablation. | `lesson_plan/drafting/infrastructure/dspy/optimized/whole_lesson_gepa_nolinkage.json` |

`Policy` has two senses:

- In the thesis, a policy is a frozen config that defines a condition: `ContextPolicy`, `RetrievalPolicy`, `ValidationPolicy`, `TeacherValidationPolicy`, `PersonalisationPolicy`.
- In backend code, a policy is also a pure precondition with no I/O, for example `experiments/application/launch_policy.py`.
- [`code-vocabulary.md`](../apps/backend/docs/code-vocabulary.md) defines the code sense.

---

## J. Evaluation

Detail: the pre-registration, which is not in this repository.

| Term | Meaning | Code mapping |
| --- | --- | --- |
| **Artefact** | A stored generated output. It exists before any rater sees it. | `artefacts`: `manifest`, `review_status` |
| **Evaluation packet** | The blinded wrapper for one scoring unit. An H1 packet holds one note and a lesson reference sheet. An H2 packet holds the base note, the learner-state card and one candidate. | `evaluation_packets` (`evaluation` domain) |
| **Rater** | An expert who scores blinded packets. | `evaluation_raters` |
| **Rater assignment** | The packets one rater must score in one experiment. | `rater_assignments` |
| **Platform rubric** | H1: 4 criteria, 1–5 each (objective and curriculum alignment, taught-lesson alignment, scope and conceptual correctness, clarity and usefulness). H2: 5 criteria, 1–5 each (learner-state suitability, scaffolding, challenge calibration, misconception support, objective preservation). | `H1_RUBRIC`, `H2_RUBRIC` in `evaluation/application/constants.py`; `evaluation_ratings.rubric_scores` |
| **Study instrument** | The paper instrument of the MSc study. Part 1 scores each class note 1–5 per objective on 3 criteria. Part 2 compares a learner's two notes, A against B, on 3 criteria. | `evaluation/domain/study_instrument.py`; `study_criterion_scores`, `study_comparative_judgements`, `study_rating_documents` |
| **Source-grounding audit** | A separate check, for C2–C4 only, that the cited evidence supports the generated text. Four criteria, each 0 (fail), 1 (partial) or 2 (pass): source relevance, support sufficiency, faithfulness, scope correctness. | `evaluation_audit_items`, `evaluation_audit_ratings`, `SOURCE_AUDIT_CRITERIA` |
| **Audit item** | A generated excerpt with its cited source, lesson objective and scope boundary. | `EvaluationAuditItem` |
| **Teacher review** | The teacher approves, rejects or asks to regenerate a note. In the study, this is the C4 gate. The teacher reviewer is not an expert rater. | `artefacts.review_status`, `content_approvals` |
| **Revision-note reader** | The student page that shows a learner their revision note. | route `student/pack-runner`, `StudentReviewNotePage` |

---

## K. Study scale

`StudyDesignConfig` in `experiments/review_pack_study/conditions/study_design.py` sets the scale. H1 counts cover C0–C3 only.

| Config | Lessons × focal learners × raters | H1 packets | H1 ratings | H2 packets | H2 ratings |
| --- | --- | --- | --- | --- | --- |
| `PILOT_ONE_LESSON_CONFIG` | 1 × 4 × 3 | 4 | 12 | 8 | 24 |
| `PUBLICATION_CONFIG` | 12 × 4 × 3 | 48 | 144 | 96 | 288 |

---

## L. Roles & generation flows

| Actor | Does |
| --- | --- |
| **Teacher** | Approves the lesson plan, the lesson note, the class test and the class revision note. Reviews learners' notes. |
| **Student** | Takes the class test and the survey. Reads the personal revision note. |
| **Researcher** (`research_manager`) | Creates a study and its experiments, picks focal learners, and starts H1 and H2 executions. |
| **Rater** | Scores blinded packets. |
| **System** | Runs drafting and generation as background jobs. |

Two generation flows:

- **Experiment flow.** The job `experiments.run_conditioned_execution` generates every condition of one execution. It stores each as an `ExperimentConditionRun` and exports blinded packets.
- **Teacher flow.** The teacher approves the class revision note. Each learner's note then generates as the job `assessments.generate_student_pack` once that learner's evidence is complete.

---

## M. Identifier conventions (dual-key)

Each entity has a UUID `id` and a unique business key. Foreign keys, payloads, URLs and seeds use the business key. Keys and examples: [data-model.md §4](data-model.md#4-dual-key-identifier-pattern).

A record the app creates at run time has a business key of the form `<PREFIX>-<32 hex digits>`, made by `new_public_id` with a prefix from `PublicIdPrefix` (`apps/backend/src/app/shared/ids.py`). The prefix names the kind of record: `EXP` an experiment, `LPV` a lesson-plan version, `LP` a lesson plan, `AT` an artefact, `INV` an investigation. An experiment and an investigation also have a readable code (`EXP-PTRS-JSS1-MATH-T1-003`, `msc-study-2026-09`) for people to read. Routes take the id, not the code.

---

## N. Naming divergences (current code vs canonical term)

| Canonical term | Code name |
| --- | --- |
| Revision note | `post_class_review_pack`, `PostClassReviewPack`, `generated_pack` |
| Class test | artefact kind `diagnostic`, tables `exit_ticket_items` and `exit_ticket_submissions`, `diagnostic_id` |
| Study | `investigations`, `Investigation` |
| Learner | `student_profiles`, `LearnerProfile`, key `student_id` |
| Researcher | DB role `research_manager`, Casbin role `researcher` |
| Artefact kind | ORM attribute `artefact_type`, column `artefact_kind` |
| Artefact reference on an event | ORM attribute `Event.artefact_id`, column `events.pack_id` |

---

## O. Words that name more than one thing

### Prototype and study; everyday use and research flow

| Term | Meaning |
| --- | --- |
| **Prototype** / **everyday use** | The app that teachers and learners use. A teacher plans, writes, approves and teaches with it, and learners read what is approved. Its flow is the **teacher flow** ([L](#l-roles--generation-flows)). |
| **Study** / **research flow** | What a researcher runs on top of the prototype: experiments, the conditions C0–C4 and P0–P1, blinded packets and raters. Its flow is the **experiment flow** ([L](#l-roles--generation-flows)). Code: `experiments/`, `app/domains/experiments`, `scripts/`. |

Everyday use and the research flow are the same split as prototype and study, named by who is using it. The two share code on purpose: everyday lesson plans are held to the lesson spec the study used, and the study and the app serve the same prompts.

### Plugin plus an existing harness, or a custom DSPy harness

"Harness" and "DSPy" each mean more than one thing.

| Word | What it is | Code |
| --- | --- | --- |
| **Experiment harness** | The code that runs a study. | `experiments/` |
| **Engine loop** | The agent loop the content engine writes with: OpenCode (the default, and what staging uses), DeepAgents, dsh, pi, or a loop of ours built on DSPy. All five read the same plugin. | `EngineLoop` in `content_engine/infrastructure/harness/choice.py`. A run records it as `harness`. |
| **Generator kind** | What made a piece of content: `engine` (a plugin run by an engine loop) or `dspy-pipeline` (an older fixed program). | `GeneratorKind` in `content/domain/generators.py`. It is stored and sent as `harness`, in the column `content_type_generators.harness` and in a content record's provenance. |

The names `harness` in storage and in the API are older than the two enums. The enums are named for what they are, and the stored name stays so that content already made still reads.

"DSPy" also means two things:

- A **`dspy-pipeline` generator** is an older fixed program, such as the review-pack versions `2026-08-25` and `2026-09-02` and the GEPA plan programs. It carries its prompts in code and reads no plugin. The study used its prompts, so it stays runnable and can be pinned.
- The **DSPy engine loop** is one of the five engine loops. It reads a plugin like the others and is not used for everyday writing.
