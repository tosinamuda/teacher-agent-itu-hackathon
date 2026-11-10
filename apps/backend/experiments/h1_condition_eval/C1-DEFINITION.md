# C1 — the lesson-plan condition

**Version 2, frozen before confirmatory expert evaluation.** This file defines what C1
receives, what each field means to the generator, and how the teacher's Presentation
narration is coded. C2 and C3 are defined by reference to it.

The three generation runs that preceded this version were **manipulation checks** — used
to verify that the treatment was implemented as defined, not to test the hypothesis. Each
corrected a construct-implementation defect found by rendering the real prompt, and each
recorded its prediction in the run notes before it ran.

| version | change | why |
| --- | --- | --- |
| 1 | initial | — |
| 1a | codebook no longer says "add nothing merely because it is usually good practice" | it suppressed artefact_spec requirements in C1 only; worked examples fell 2.3 to 1.0 on t3-w04 |
| 2 | C0 and C1 share ONE signature | C1's said "teach this part and leave the rest to its own section" — a narrowing instruction the baseline never saw |
| 2 | synthetic per-step `estimated_minutes` removed | the derivation apportioned them; a length cue C0 never received |
| 2 | `instructional_materials` moved to lesson scope | lesson-level in every plan she writes; per unit it read as step-scoped |
| 2 | `lesson_sequence` collapsed into `current_step` | core steps match the objective order one-for-one on all six lessons |
| 2 | every plan field given a defined meaning | one field had a codebook and five were bare JSON keys, so the study partly measured whether a model can guess our key names |
| 2 | the objective is stated as authoritative over `assessment_points` | an evaluation item may not redefine the objective it was written to check |
| 2 | `_instruction_summary` no longer branches on condition | latent: it reached no run, but the packed generator carries the field it would travel on |

Version 3 adds one field-reading change to `student_tasks`, argued below and measured in
`FINDING-C1-DELIVERY.md`. No other C0/C1 prompt changes.

**None of those runs measured whether C1 is better.** The deterministic recall proxy
scores overlap with the teacher's NOTE, which neither C0 nor C1 receives, so between those
two arms it can only measure coincidence — on `t3-w05` a C1 pack scored 0.412 with every
match a one-digit number while missing every worked example's answer. It also moves 0.094
(median) between runs of the SAME condition on unchanged data. It remains a dud screen,
and a real fidelity measure for C2/C3, which do get the note.

The C0-vs-C1 question is answered by the frozen H1 rubric and by nothing here.
`taught_lesson_alignment` — *"does it reflect the taught lesson: its sequence, emphasis,
activities, and expected depth?"* — IS the C1 construct, and the pre-registered mechanism
prediction already says the C0-C1 gap should be largest there and smallest on
`objective_curriculum_alignment`. The rater packet carries the plan's objectives,
curriculum objectives, materials and steps, so the dimension is ratable.

## The ladder

```
C0   the curriculum specification    objectives, subject, grade, topic, subtopic
C1   C0 + the lesson plan's design   the fields enumerated below
C2   C1 + the teacher's note         her note, verbatim, as scoped evidence
C3   C2 + validation and repair
```

C2 needs no provenance boundary of its own. It is C1 plus the note passed whole, so
anything C1 already carries stays and the note is added on top. The only definition the
study needs is a positive enumeration of C1 — everything not listed below is absent from
C1 by construction.

## What C1 receives

Each field names the place in her document it is read from. A field with no such place in
a given lesson is absent for that lesson; nothing is supplied to fill it.

### Lesson level — shared by every generation unit

| field | read from |
| --- | --- |
| `subject`, `grade_level`, `topic`, `subtopic`, `term`, `week` | plan header |
| `lesson_objectives` | Behavioural objectives (also in C0) |
| `entry_behaviour` | the Previous knowledge list |
| `instructional_materials` | the Instructional materials line — lesson-level in every plan she writes |
| `lesson_opening` | the intro step's Gagné codes, where the plan has one |

No lesson duration. Her header gives one figure and it is **40 minutes on all six lessons**,
so it discriminates nothing; and no per-step split exists to derive one from.

Order travels as the unit's `current_step` read against the ordered `lesson_objectives`.
Every unit is a separate concurrent LM call and would otherwise have no way to know what
precedes or follows it. A separate sequence object was tried and dropped: the core steps
match the objective order one-for-one on all six lessons, so it only restated the list.

`lesson_opening` is delivered to the **first core unit only** — a single planned recall
activity must not become four recall sections in one pack.

### Unit level — one per core step

| field | read from |
| --- | --- |
| `current_step` | the step's position against the ordered objectives |
| `instructional_events` | the step's Teacher/Student activity narration, Gagné-coded (below) |
| `student_tasks` | the work the step sets: her Student Activity questions as statements, plus a Student Activity her Gagné coder reads as performance (see below) |
| `assessment_points` | the Evaluation questions for this step's objective, statements only |

There is no per-step time field. Her plans give one Duration line for the lesson and
allocate nothing to individual steps; the 10/10/10 and 20/20 splits in the current eval
set were apportioned by the derivation. Sending them would be the system inventing
instructional design, which is the one thing C1 exists not to do.

## What C1 does not receive

- Anything in the note: definitions, property lists, derivations, worked examples,
  figures, explanatory prose.
- Any answer to any question. She wrote none; where the derivation computed one it does
  not travel.
- The raw **teacher** activity narration, and any student activity that is reception.
  Only its Gagné code travels — the artefact spec forbids writing about the lesson as an
  event, and "the teacher explains the drawing" or "they take notes in their notebooks" is
  exactly that.

  **The one slice of the column that does cross** is a *student* activity the coder reads
  as `elicit_performance`. That is not narration about the room, it is the work she set,
  and it is the same content class as the question text beside it. It crosses because
  reading question-shaped blocks alone said she set no work on four of the cohort's
  seventeen steps — *construct parallel lines*, *construct angle 90 degrees*, *identify
  their properties* — all of them on the two lessons that are mostly construction. The
  boundary is enforced rather than asserted: the leakage suite carries a token for each
  half of the column and proves the performance half reaches C1 and the reception half
  reaches nothing.

  **Version 3, and the one change after version 2's freeze.** It raises `student_tasks`
  delivery from 4/17 calls to 8/17. Recorded here rather than folded in silently: the
  measurement that prompted it is in `FINDING-C1-DELIVERY.md`, and any run before this
  carries the 4/17 definition.
- `instructional_type`. It is derived from `blocks`, which on a field plan is a parse of
  the note, so it is note evidence sitting inside the no-note condition.
- Editorial annotation. Transcription markers such as `*(objective (iii))*` and
  `*(core → objective 2)*` are the transcriber's, not hers, and describe the derivation
  rather than the lesson.
- `step_title`. She writes a bare label and runs the narration on the same line, so the
  descriptors in the transcripts are the transcriber's — see below.

## The one ambiguous case, and the rule that settles it

Her documents interleave plan and note. t3-w04 has a `## Note` section; t3-w05 has none at
all, and its property lists and four worked examples sit inside `## Presentation`. So no
structural feature of the documents can carry the distinction, and a heading-based rule
would give t3-w05 an empty C2 for reasons unconnected to her teaching.

The rule is about instructional role, not location:

> **Learner-directed tasks occurring in a lesson-plan activity or evaluation role are C1.
> Teacher-authored mathematical exposition and solution content is C2.**

So *"How many circular faces does a solid cylinder have?"*, written under Student
Activity, is C1; *"It has two circular faces and one curved face"* is C2. A worked example
is a question fused to its solution and is therefore C2 whole.

The qualifier is load-bearing. "Any question is C1" would promote a rhetorical question
inside explanatory prose; it is the activity or evaluation role that qualifies it, not the
question mark.

This is an operational rule for these hybrid documents, not a distinction drawn by Gagné
or the lesson-plan literature, and is reported as such.

`student_tasks` and `assessment_points` are separate fields because they carry different
instructional roles — in-step practice and end-of-lesson assessment — not because they
come from different documents.

---

# The Gagné codebook

The teacher's Presentation narration is coded against Gagné's Nine Events of Instruction.
The codebook is the coding vocabulary. It is never a source of instructional decisions.

## Codes

| code | Gagné event | licensed by | realised in the pack as |
| --- | --- | --- | --- |
| `stimulate_recall` | 3. Stimulate recall of prior learning | an activity that asks about or rehearses earlier material | brief recall prompts before the new material |
| `present_content` | 4. Present the content or stimulus | an activity that explains, displays, draws, writes up or introduces | learner-facing exposition, or an object to inspect |
| `provide_learning_guidance` | 5. Provide learning guidance | an activity that solves, demonstrates, or supplies worked examples | support before the learner works alone — a worked solution, demonstration, scaffold or cue. Gagné's category is broader than a worked solution; naming only that turned a general construct into a mathematics-specific realisation |
| `elicit_performance` | 6. Elicit performance | an activity in which the learner answers, solves, constructs or identifies | practice the learner attempts |
| `provide_feedback` | 7. Provide feedback | an activity that marks, corrects, or responds to learner work | answers and corrections the learner can check against |

## Codes out of scope

- `gain_attention` (1), `inform_objectives` (2), `enhance_transfer` (9) — no activity in
  the corpus licenses them.
- `assess_performance` (8) — the function is present, but it is carried structurally by
  `assessment_points` rather than as an event code, so the model is not told the same
  thing twice.

Reported as: *five event types occurred in the coded presentation sequences; assessment
was represented separately by the lesson-plan evaluation field.*

## Coding rules

1. **One activity, at most one code.** Where an activity entry carries several verbs, code
   its dominant function. No double-coding.
2. **Code only what the text says.** An event Gagné recommends but she did not plan is
   never added. The codebook describes her lesson; it does not improve it.
3. **Weak evidence takes no code.** "Listen", "contribute", "ask questions", "take notes"
   are reception and are left uncoded.
4. **`entry_behaviour` never licenses `stimulate_recall`.** Listing prior knowledge is not
   planning a recall activity. Only an activity licenses the code. t3-w04 plans one
   (*"Teacher asks the students some questions based on their previous knowledge"*);
   t3-w05 lists prior knowledge and plans none. That difference is signal.
5. **Codes name instructional functions, not actors.** Gagné's events are functions of
   instruction, so a code attaches to the function the activity text describes, whichever
   column names it. *"They copy worked examples into their notes"* states that the
   worked-example function operates in that step, and codes
   `provide_learning_guidance` — not by inferring an unstated teacher action, but by
   reading the function off the text. It changes the coding in exactly one place:
   t3-w05's Step II, where no teacher-side activity mentions the examples. Without it that
   step — four worked examples and a prism — codes as pure exposition, which misrepresents
   her plan more badly than the alternative over-codes it.
6. **Consecutive duplicates collapse**, after uncoded activities are dropped.
7. **Frozen before generation.** The codebook is fixed in advance and applied identically
   to every lesson.

## The codebook reaches every condition

The definitions above go into the shared generation contract, not into a C1-only
signature. Signatures are selected per condition (`signature_for(request.profile)`) and
dspy REPLACES a parent docstring rather than extending it, so a codebook written into the
step-level signature alone would put instructional-design prose in the C1 prompt and none
in C0's — and that prose, not the lesson plan, could then explain a C1 advantage.

`INSTRUCTIONAL_EVENTS_CODEBOOK` is therefore appended to all four signatures, C0's
included. C0 receives the legend and never receives the field, which costs it nothing: the
text does no work unless a unit actually carries events.

## Implemented

| field | model | source |
| --- | --- | --- |
| `entry_behaviour` | `LessonContextForGeneration` | the Previous knowledge list |
| `instructional_materials` | `LessonContextForGeneration` | the Instructional materials line |
| `current_step` | `SectionGenerationUnit` | position against the ordered objectives |
| `instructional_events` | `SectionGenerationUnit` | `PlanStep.activities`, via `instructional_events.py` |
| `student_tasks` | `SectionGenerationUnit` | the work the step sets — her questions, and a performance-coded Student Activity |

Removed on the way: `step_title` (transcriber's), evaluation answers (computed), and
`instructional_type`. The last was note-derived and, on `t3-w05`'s volume step, actively
wrong — the parse read her four worked examples as explanations and emitted `explain_only`
beside `instructional_events: ["present_content", "provide_learning_guidance"]`, the two
fields contradicting each other in one prompt.

C1 is now 2.3x–3.9x C0 by prompt size across the six lessons, and every lesson carries
instructional events.

### Absent means absent

"A field with no such place in a given lesson is absent for that lesson" is stated above,
and until the `c1-clean-control` run it was not true of the prompt. The profile decided
each field's *contents*, but the whole `LessonContextForGeneration` was serialised, so the
key survived with an empty value and C0 read

```json
"curriculum_scope": null, "entry_behaviour": [], "instructional_materials": []
```

— the control arm being told that prior knowledge and materials exist for this lesson and
were withheld from it. `prompt_unit` had dropped empty fields from the unit since it was
written; nothing did the same for the lesson. `prompt_lesson` now does, and every
generation signature takes `lesson_context` as a `dict` so a typed field cannot quietly
reinstate the full serialisation. The two conditions differ by what C1 carries in
addition, never by C0 carrying the same keys emptied out.

---

# The coded corpus

Six lessons, 16 core steps, 13 of them carrying activity narration. `—` is a step whose
plan carries none.

### t2-w09 — Simplification of Algebraic Terms

| step | events |
| --- | --- |
| 1. order of operations | `provide_learning_guidance` → `elicit_performance` → `provide_feedback` |
| 2. insertion and removal of brackets | `provide_learning_guidance` → `elicit_performance` → `provide_feedback` |
| 3. word problems | `provide_learning_guidance` → `elicit_performance` → `provide_feedback` |

The only lesson with no `present_content` anywhere: she never expounds, she teaches
entirely by worked example. Also the only lesson whose core steps carry `provide_feedback`
— all three do, through "moves round to … mark their notes and mark correction".

### t3-w02 — Plane Shapes

| step | events |
| --- | --- |
| II. types of plane shapes and properties | `present_content` → `elicit_performance` → `present_content` |
| III. parts of a circle | `present_content` |
| IV. perimeter of plane shapes | — |

### t3-w05 — Three Dimensional Shapes II *(from the 2026-08 capture, not the superseded supplement)*

| step | events |
| --- | --- |
| Step 1 | `present_content` → `elicit_performance` → `present_content` |
| Step II | `present_content` → `provide_learning_guidance` |

Her headings carry no descriptor, so the titles are bare. Six activities across the two
steps, from the capture.

### t3-w06 — Construction

| step | events |
| --- | --- |
| 2. parallel and perpendicular lines | — |
| 3. construction of line segments | `present_content` → `elicit_performance` |
| 4. angle 90° | `present_content` → `elicit_performance` |
| 5. angle 60° | `present_content` → `elicit_performance` |

### t3-w09 — Need for Statistics

| step | events |
| --- | --- |
| 2. purpose and meaning of statistics | `present_content` |
| 3. collecting, tallying and tabulating data | — |

### t3-w04 — Three Dimensional Shapes

| step | events |
| --- | --- |
| I. questions on previous knowledge *(intro)* | `stimulate_recall` → `elicit_performance` → `provide_feedback` |
| II. properties of cubes and cuboids | `present_content` |

## What the coded corpus shows

The lessons differ in instructional design, and the coding makes the difference explicit:
t2-w09 teaches by worked example and marks the work; t3-w06 and t3-w09 are exposition;
t3-w02 and t3-w05 open by eliciting properties from an object before formalising them.
That variation is what C1 exists to transmit and what a single `instructional_type` word
erased.

`stimulate_recall` fires once in the corpus, on **t3-w04's intro step** — and intro steps
are filtered out of the generation units (`_build_units` keeps `step_kind == "core"`). So
the one place prerequisite activation is planned reaches no unit. This is why
`entry_behaviour` is carried on the shared lesson context: prior knowledge reaches every
unit even though the step that would rehearse it does not.

An intro step's own codes travel as `lesson_opening`, to the **first core unit only**. One
planned opening activity must produce one opening in the pack; broadcasting it to every
unit would turn t3-w04's single recall step into a recall section in each of them.

---

# Data fidelity — fixed 2026-08-09

Four defects in the frozen eval set, all of which altered the treatment. Fixed at the
source that produces the plans, not in the plans themselves, so a rebuild keeps them
fixed.

1. **Derived answers reached C1.** She wrote no answer to any evaluation question in any
   lesson. t3-w02's binding declared nine computed ones and `_assessment_points` rendered
   each into the plan conditions as *"(expected answer: 32cm)"* — solved mathematics
   entering the no-note condition, on one lesson and no other. The binding no longer
   declares them (`answers_are: none_written`), and `_assessment_points` no longer renders
   an answer even if one is present.
2. **`entry_behaviour` lost its content.** `_labelled_sentence` stopped at the first blank
   line, so t2-w09 — the only plan whose Previous knowledge is a numbered list — carried
   the stem *"Students have been taught:"* and neither item. It now returns the list where
   one follows the label.
3. **t3-w05 was built from the superseded supplement.** It now builds from the 2026-08
   capture: both core steps carry her activities, the Evaluation is her own five
   questions, and `entry_behaviour` names the two prior topics. `dataset.py` points at
   `Dataset/transcripts/t3-w05/session-plan.json`.
4. **Editorial annotation in step titles.** Six core-step titles ended in a transcription
   marker — `*(objective (iii))*`, `*(core → objective 2)*` — describing how the
   transcript maps onto the schema, and `step_title` reaches the generator. The builder
   now strips the parenthetical on the way into the plan and leaves it in the transcript.

## Settled against the page images: a step title is not plan evidence

Stripping the annotation did not settle the titles, so the pages were read. She writes a
**bare step label and runs the narration on the same line**:

| lesson | on the page |
| --- | --- |
| t2-w09 | `PRESENTATION: Teacher present the lesson through the following steps:` then `STEP 1: Teacher solve some question in order of operation on the board…` |
| t3-w06 | `Presentation:` then `Step 1: Teacher draws intersecting lines and ask stude…` |
| t3-w09 | `Step 1 Teacher asks questions such as`, `Step 2: Teacher introduces the concept…`, and — the sole exception in the corpus — `Step 3: Meaning of statistics` |
| t3-w05 | `Step 1`, `Step II`, bare (recorded in `teacher.md`) |

Every other descriptor in the transcripts is the transcriber's summary, and each
paraphrases the step's **objective** — which the unit already carries verbatim as
`objective_text`. So the field has no source in her document and adds nothing that is not
already present from a field she did write. It is dropped from the plan conditions
entirely (`include_step_title=False`), pinned by
`test_no_condition_receives_a_step_title`.

The transcripts keep their descriptors: there they are declared derivations and useful for
navigation. `t3-w09` and `t3-w06` both declare their step-boundary restructures in
`cleaning_applied` with a source, and both are accurate — `t3-w09`'s second core step is
named from her own unlabelled headings *Collection of Data*, *Tally Marks* and *Frequency
Table*; `t3-w06`'s merge follows her own compound objective wording. The defect was never
the transcription. It was sending a transcription artefact to the generator as if it were
her plan.

## Validator state after the rebuild

`t2-w09`, `t3-w04` and `t3-w09` validate clean. `t3-w02` (2) and `t3-w05` (2) raise the
same pair — a procedure step whose practice lives in the Evaluation, and an objective the
Evaluation does not assess — and `t3-w06` raises 5, having no Evaluation section at all.
All are the pre-existing app-level constraints analysed in `../../../../Dataset/transcripts/_pipeline-entry.md`
§7, not cleaning failures.

Any earlier finding that C1 does not outperform C0 is pilot evidence from the previous
implementation and does not bear on the corrected condition.
