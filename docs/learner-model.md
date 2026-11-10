# Learner Model

The learner model turns one student's class test and survey into a state per lesson objective. Personalization reads that state to adapt the class revision note into the student's own revision note. The `learner_state` and `assessments` domains hold it.

Terms: [glossary.md](glossary.md).

## The state

One record per lesson objective, for one student and one lesson:

```
Σ_i(u) = { σ_i(o) | o ∈ O(u) }                      # student i, lesson u, objective o
σ_i(o) = ⟨ band, mastery, misconception, confidence, perceived difficulty, evidence ⟩
band ∈ { remediate, reinforce, extend }
```

The model is `ObjectiveLearnerState`, held on `LearnerState.objective_states`:

| Field | Source |
|---|---|
| `lesson_objective_id` | the objective the class test questions are tagged with |
| `mastery_score`, `questions_correct`, `questions_total` | the marked class test |
| `band` | derived from `mastery_score` |
| `misconception_code`, `misconception_description` | the misconception codes of the wrong options chosen |
| `confidence`, `confidence_score` | the post-class survey, per objective |
| `perceived_difficulty`, `difficulty_score` | the post-class survey, per objective |
| `evidence` | each missed question: stem, options, correct option, chosen option, misconception code |

`LearnerState.session_survey` holds the two session-level answers: `interest` and `affect`.

## Deriving the state

The state comes from one lesson's class test and survey. It does not track the student across lessons.

### Mastery and band

```
mastery(o) = correct answers / questions tagged to o

remediate:  mastery < 0.50
reinforce:  0.50 ≤ mastery < 0.75
extend:     mastery ≥ 0.75
```

### Misconception

- Each class test option can carry a misconception code (`exit_ticket_items.option_misconceptions`).
- For each wrong answer, the scorer records the code of the chosen option.
- The objective's misconception is the most frequent code. A tie goes to the code seen first.
- An objective with every answer correct records no misconception.

### Survey

The student takes the class test first. The survey opens after the app marks the submitted answers.

| Level | Item | Scale |
|---|---|---|
| Per objective | How sure the student is that they can do the objective alone | 1–5 |
| Per objective | How difficult the objective felt | 1–5 |
| Per lesson | Interest in the subtopic | 1–5 |
| Per lesson | How the student feels at the end of the lesson (`affect`) | 1–5 |

- A lesson with `n` objectives gives `2n + 2` survey answers.
- The app stores each 1–5 answer as given. The scorer also derives a level: 1–2 is `low`, 3 is `medium`, 4–5 is `high`.
- The test shows the questions as one numbered list. The survey groups its items by objective ("About Objective N").

## Personalization

A student's revision note is the approved class revision note, adapted section by section. Each section teaches one objective.

```
approved class section + σ_i(o) + session survey ──► personalized section
```

For each section, the personalizer:

1. Finds the student's state for the section's objective.
2. Sends the base section, the state and the session survey to the model.
3. Keeps the base section when the student has no state for the objective, or when the model returns nothing a reader can use.

The instructions to the model (`SectionPersonalisation`) set what each band gets:

| Band | Explanation | Worked example | Practice | Hints | Feedback |
|---|---|---|---|---|---|
| `remediate` | full, step by step | required | easier than the base | generous | full |
| `reinforce` | moderate | — | at the lesson's target | optional | standard |
| `extend` | minimal | — | above the target | — | concise |

A dash means that the instructions set nothing for that band.

Other signals adapt the section as follows:

| Signal | Effect on the section |
|---|---|
| Low confidence or high perceived difficulty | more worked support and more hints |
| High confidence with strong mastery | less repetition, more challenge |
| A chosen wrong option | explains why that option is tempting and wrong, as "a common slip here is …", never "you chose …" |
| Low interest | shorter, more direct sections |
| A confused end-of-lesson feeling | less load, more reassurance |

What personalization keeps and what it adapts:

| Can adapt | Cannot adapt |
|---|---|
| explanation depth, worked support, hints, feedback, practice difficulty, tone | the lesson objective, the section order, the sources the base section cites |

- The model receives the base section, the lesson context, the state and the session survey.
- The model also receives the source evidence that the base section cites. When the base section cites none, it receives all the evidence of the section.
- The model does not receive the full lesson plan or the teacher's edit history.
- The `objective_preservation` check confirms that each section keeps its base objective. See [revision-note-generation.md](revision-note-generation.md).

## Flow

```text
class test answers (chosen options)          post-class survey
            │                                       │
            ▼                                       ▼
   mastery + misconception per objective ──► ObjectiveLearnerState per objective
                                                    │
approved class revision note ──────────────────────►├──► personalized revision note (pending)
                                                    │
                                          teacher approves ──► the student reads it
```

## Code

| Concern | Path |
|---|---|
| State models | `apps/backend/src/app/domains/learner_state/domain/models.py` |
| Band thresholds, state building | `apps/backend/src/app/domains/learner_state/application/service.py` |
| Scoring and survey levels | `apps/backend/src/app/domains/assessments/application/scoring.py` |
| State as the model reads it | `apps/backend/src/app/domains/artefacts/types/post_class_review_pack/application/learner_state_input.py` |
| Personalization instructions | `apps/backend/src/app/domains/artefacts/types/post_class_review_pack/infrastructure/dspy/contracts/personalise_section.py` |
| Survey screen | `apps/frontend/src/features/student/components/ExitAssessmentObjectiveCard.tsx` |
