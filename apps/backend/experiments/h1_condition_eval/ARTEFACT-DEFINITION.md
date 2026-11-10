# The artefact: what it is, what grounds it, and where the code does not yet match

The artefact existed only as `revision_pack_spec()` and `AuthoredBlockType` in code. This is
the design that should govern it, written literature-first.

Two rules throughout:

1. **The literature supplies the constructs; this framework supplies the operationalisation.**
   Citations must not be used to legitimise an enum that already exists.
2. **Where an element is ours, say so.** A defensible operationalisation assembled from
   research-backed functions is a contribution. A borrowed name that implies more
   establishment than it has is a liability.

---

## The empirical precedent

The core anchor is **Ziegler et al.**, whose instructional worksheet was organised as
**worked examples → example generation → practice**, one worksheet per lesson, with
self-explanation prompts against contrasted worked examples and practice carrying corrective
feedback. That is the closest published thing to what this system generates, and deviations
from it should be justified against the post-class Nigerian use case rather than assumed.

Supporting strands, each established independently:

| element | basis |
| --- | --- |
| instructional worksheet as a genre | Ziegler et al.; FACET |
| worked / modelled examples | worked-example research (Atkinson, Derry, Renkl & Wortham) |
| self-explanation and contrasted examples | Ziegler et al. and the comparison literature |
| example generation | Ziegler et al. — **optional here, see scope decision below** |
| practice | Ziegler et al.; the worksheet genre generally |
| incorrect / correct comparison | Durkin & Rittle-Johnson, where applicable |
| conceptual–procedural interdependence | Rittle-Johnson, Schneider & Star — bidirectional relations |
| corrective instruction from evidence of difficulty | Bloom; Guskey — **H2 only** |
| answers for unsupervised checking | this study's independent-home-use requirement |
| **lesson structural alignment** | **this study's operational contribution** |

---

## The artefact

```
ARTEFACT GENRE
instructional worksheet

CASE-STUDY PURPOSE
independent post-class review and practice

GENERATION UNIT
one section per learning objective

REQUIRED INSTRUCTIONAL ELEMENTS          per learning objective
├── concise instructional support
├── worked / modelled example
└── learner practice

OPTIONAL INSTRUCTIONAL ACTIVITIES
└── example generation / self-explanation

INDEPENDENT-USE REQUIREMENT
└── answers / worked solutions, after the learner activities
```

**Every condition is asked for exactly this.** The specification is held constant and the
grounding source is what varies — which is the whole design of H1.

### The definition

> **Class-level post-class instructional worksheet.** The case-study artefact is a
> learner-facing instructional worksheet associated with a single taught lesson and intended
> for independent review and practice after classroom instruction.
>
> The worksheet is organised around the lesson's learning objectives. For each objective it
> provides:
>
> - **concise instructional support**, presenting the principles, relationships, rules,
>   representations or other information necessary to review the target content;
> - **one or more worked or modelled examples**, demonstrating the target knowledge or
>   procedure;
> - **learner practice**, providing opportunities to apply the target knowledge or procedure
>   independently.
>
> Example-generation or self-explanation activities may additionally be included where
> appropriate.
>
> Because the worksheet is intended for independent post-class use, **answers or worked
> solutions** are provided separately after the learner activities so that students can check
> their responses after attempting them.
>
> This structure is the operational design of the present mathematics case study. It is
> informed by contemporary instructional-worksheet and mathematics-learning research and is
> not proposed as a universal component taxonomy for instructional worksheets.

Rendered, that is simply:

```
Objective 1
───────────
Key explanation
Worked example
Practice

Objective 2
───────────
Key explanation
Worked example
Practice

CHECK YOUR WORK
───────────────
Answers · worked solutions
```

### Structure is not the same thing as the properties being measured

The single most important rule in this document, and the one that keeps H1 from being
circular.

The definition above says worked examples **demonstrate the target knowledge or procedure**.
It does *not* say they preserve the structure, procedure, scope or cognitive demand of the
taught lesson — even though that is exactly what lesson-plan grounding is hoped to buy. Those
are **properties measured of the output**, never requirements written into the artefact both
arms are asked for. Bake them into the definition and the finding becomes:

> the lesson-plan-grounded condition produced more lesson-aligned worksheets because the
> definition required worksheets to be lesson-aligned.

Instead: both conditions are asked for the same defined worksheet, and how well each output
aligns with the lesson is then measured. The same reasoning bars *"lesson-isomorphic where
lesson-plan evidence permits"* from the specification — see the wording trap below.

**The measurement side is already frozen and is not reopened here.** The H1 rubric, frozen
2026-07-26 with H1a (C1 vs C0) as the sole endpoint, is:

| criterion | what it asks |
| --- | --- |
| `objective_curriculum_alignment` | does it cover the intended objectives and curriculum target |
| `taught_lesson_alignment` | does it reflect the taught lesson — sequence, emphasis, activities, expected depth |
| `scope_conceptual_correctness` | does it stay inside the lesson boundary and avoid errors |
| `clarity_usefulness` | can a JSS1 learner use it as take-home review |

Scope preservation, procedure preservation and cognitive-demand preservation are already
inside `taught_lesson_alignment` and `scope_conceptual_correctness` — they are not missing
metrics. **Example structural similarity (lesson-isomorphism) is the one genuinely new
property**, and adding it changes a frozen analysis plan. That is a deliberate decision to
take, not a documentation edit to slip in.

### Instructional support is required, and there is no conditional gate

An earlier draft made instructional support conditional and proposed keying it to the
objective's verb — *explain / distinguish / justify / relate* against *calculate / construct
/ execute*. **That rule is dropped.** It is a plausible operationalisation and it is ours: a
classifier invented to justify a schema, which is the same retrofit the rest of this document
exists to avoid. Adopting it would also have obliged the study to establish and validate a
conceptual-versus-procedural objective classifier that nothing in the research question needs.

It is unnecessary on the evidence. Measured on `c1-clean-payload`:

| element | C0 (51 sections) | C1 (51 sections) |
| --- | --- | --- |
| explanation | 51/51 (100%) | 51/51 (100%) |
| worked example | 51/51 (100%) | 50/51 (98%) |
| practice | 51/51 (100%) | 51/51 (100%) |
| reflection | 9/51 (18%) | 6/51 (12%) |

Instructional support is already present in every section of both arms. Making it required
**describes what the system does** rather than changing it, and it removes the risk that C0
and C1 come to differ in package structure on top of differing in grounding — which would be
an uncontrolled second difference between the arms.

**Required does not mean a paragraph per objective.** It means: *every objective receives
enough learner-facing instructional support to make the worksheet usable without a teacher.*
The amount follows the objective naturally.

```
"Why is the angle 90°?"                several sentences on the relationship
"Construct a perpendicular through P."  one concise rule, then straight to the worked example
```

**One implementation caveat.** The artefact spec's five requirements say nothing about
instructional support today, so writing the requirement into that text *is* a prompt change
and needs its own labelled comparison — even though the observed rate is already 100% and the
expected behavioural delta is nil. Recording it in this document is free; changing the brief
is not.

### Scope decisions, recorded rather than dropped quietly

- **Example generation is not required.** Ziegler used it; this study makes it optional. That
  removes roughly a third of their instructional-worksheet design and the omission is
  deliberate.
- **Classwork review is removed from the H1 artefact entirely**, on two grounds. It is not
  consistently available — four of six frozen lessons carry no student task and one carries
  neither task nor assessment point — so some lessons could instantiate it and others could
  not. And it would confound H1: C0 cannot reach classwork by construction, so a
  specification that asked for a classwork section would build part of C1's advantage into
  the artefact instead of measuring it as better grounding. Correction moves to H2.
- **Reflection is dropped from the authored vocabulary.** It was a peer of explanation and
  practice in the enum while being an integration strategy, and the model reached for it in
  15 of 102 sections.
- **"Knowledge component" is not used.** The unit is the *learning objective*. Nothing
  in the framework formally models knowledge components, and naming one implies a
  decomposition that does not exist. If objectives are later decomposed into skills, that is
  a separate model introduced explicitly.

## Two corrections to claims that were nearly made

### The generation unit is the learning objective, not the lesson-plan step

A lesson-plan step is a teacher-planning unit — *introduce the lesson*, *distribute
materials*, *pupils respond*. Those do not map one-to-one onto units a learner should review
at home. The unit must be the **learning objective**, with traceability back to the
step that taught it:

```
learning objective
        ↓
corresponding lesson-plan step(s)
        ↓
worksheet section
```

**The code already does this**, despite the `step:` prefix on C1's unit ids, and it is worth
recording because the id reads the other way. Verified across the frozen set:

| lesson | objectives | core steps | C0 units | C1 units | same objectives | traced to a step |
| --- | ---: | ---: | ---: | ---: | :--: | :--: |
| t2-w09 | 3 | 3 | 3 | 3 | yes | yes |
| t3-w02 | 3 | 3 | 3 | 3 | yes | yes |
| t3-w04 | 2 | 2 | 2 | 2 | yes | yes |
| t3-w05 | 2 | 2 | 2 | 2 | yes | yes |
| t3-w06 | 5 | 5 | 5 | 5 | yes | yes |
| t3-w09 | 2 | 2 | 2 | 2 | yes | yes |

Core steps correspond one-to-one with objectives on all six lessons; the intro step is
excluded and evaluation steps become assessment points rather than sections. C0 and C1
generate the same number of sections against the same objectives, so the granularity is not
a confound between the arms. `source_step_id` carries the traceability.

The 1:1 correspondence is a property of *these* plans, not a guarantee. A plan whose core
steps split an objective across two steps would break it, and the unit must stay
objective-keyed if that happens.

### This is not productive failure

The claim that putting correction first buys a productive-failure ordering is wrong and has
been removed. In Ziegler's PS-I condition learners attempt problems **before** the relevant
formal instruction. The observed sequence here is:

```
teacher teaches → student does classwork → teacher marks → correction
```

The unsuccessful attempt happens *after* instruction. For H2 the right literature is
corrective feedback and mastery learning. For class-level correction, Durkin &
Rittle-Johnson support comparing incorrect with correct examples — they found it reduced
misconceptions and improved both conceptual and procedural learning on decimal magnitude.
That licenses

```
common error → why it is wrong → correct solution
```

with no appeal to productive failure.

---

## Lesson-isomorphism — our term, defined

Ziegler uses *isomorphic* for a later problem-solving test whose problems assess the same
principles practised during instruction. There is **no established construct** called "a
worked example isomorphic to the teacher's lesson note". The operationalisation is ours and
has to be stated:

> A generated worked example is **lesson-isomorphic** when it preserves the mathematical
> structure, the required procedure, and the cognitive demand of an example used in the
> lesson, while varying surface features such as numbers or context.

This is worth more than a definition — it makes H1 concrete and measurable:

```
curriculum-only grounding      →  topic-aligned
lesson-plan grounding          →  additionally preserves
                                    the taught procedure
                                    the example structure
                                    the lesson's scope
                                    its cognitive demand
```

That is a sharper H1 claim than generic curriculum alignment. It is also **the one property
in that list the frozen rubric does not already capture** — scope, procedure and cognitive
demand sit inside `taught_lesson_alignment` and `scope_conceptual_correctness`; example
structural similarity does not.

So adopting it is a **change to a frozen analysis plan**, not a documentation change, and it
carries two obligations. It has to be pre-registered before any output is scored against it,
and it must never enter the artefact specification — a spec that asks for lesson-isomorphism
both tells C0 that lesson evidence exists and makes the measurement circular. It is measured
of the output or it is not used.

---

## Where the code does not match, and what it costs

**1. Component vocabulary.** `AuthoredBlockType` is `explanation | worked_example | practice
| reflection` — a flat engineering enum. `reflection` sits as a peer of `explanation` while
being an integration strategy, and appears in 15 of 102 sections (0.15 per section) against
~1.0 for each of the others. Nothing in the schema requires any of them.

**2. Activity, evaluation and feedback are fused.** A `practice` block's text holds the
questions *and* the answers, so "answers at the end" is a sentence in the brief that no check
can enforce — [issue #163](https://github.com/tosinamuda/lpcg/issues/163), which the blinded
judges hit in 9 of 12 cells. Separating checking support from the activity makes it
structural.

**3. Classwork is not available, which is why it is out of scope rather than a gap.** The
plan carries no classwork field, and the in-lesson task material C1 receives is uneven:

| lesson | student_tasks | assessment_points |
| --- | ---: | ---: |
| t2-w09 | 3 | 5 |
| t3-w02 | 0 | 9 |
| t3-w04 | 0 | 5 |
| t3-w05 | 1 | 4 |
| t3-w06 | 0 | 0 |
| t3-w09 | 0 | 3 |

Four of six lessons supply no student task; t3-w06 supplies neither. This is *grounding*
that C1 receives and C0 does not — a legitimate part of the manipulation — but it is not a
basis for an artefact section, because a section every condition is asked for must be one
every condition can attempt.

**The artefact spec is already condition-invariant, and must stay so.** `revision_pack_spec`
takes only the grade band, not the profile, so all four conditions receive a byte-identical
brief; none of its five requirements names classwork, a lesson plan or a correction. That
invariance is the thing to protect.

**A wording trap on lesson-isomorphism.** "Worked examples that are lesson-isomorphic where
lesson-plan evidence permits" cannot go into the specification, even though it is a fair
description of what is hoped for. The spec is read verbatim by C0, and it would tell the
control arm that lesson-plan evidence exists and was withheld from it — the same defect as
[issue #161](https://github.com/tosinamuda/lpcg/issues/161), in the one object guaranteed to
reach every condition. Lesson-isomorphism is a **property measured of the output**, not an
instruction given to the generator. The spec stays condition-neutral: *preserve the
structure, procedure, scope and cognitive demand of the material being taught.*

**Cost of the change.** It alters the output schema, therefore the prompt, therefore every
run. `c1-clean-payload` and its 36 judgments become the last measurement of the old artefact.
Both arms change identically so H1a is not biased, and no human rater has seen anything yet —
which makes now the only cheap moment to do it.

---

## H1 and H2, stated

**H1.** Does grounding generation in the teacher's lesson plan improve alignment to the
lesson actually planned, while preserving curriculum alignment, compared with generation
grounded in the curriculum statement alone?

```
official curriculum      intended curriculum
        ↓
teacher's lesson plan    planned curriculum    ← what C1 adds
        ↓
generated worksheet
```

Both alignments are needed. A pack can be curriculum-relevant and lesson-misaligned —
curriculum says *fractions*, the lesson taught *addition with like denominators*, the pack
teaches *multiplication and equivalence*. Closing that gap is the claim.

**COGENT is not a naive baseline.** It is explicitly curriculum-grounded, decomposing
standards into concepts, core ideas and objectives, and reports curriculum-alignment gains
over its own BASE condition. It is the rung below, not a strawman:

| condition | curriculum | lesson plan |
| --- | --- | --- |
| direct / BASE | no or minimal | no |
| curriculum-grounded (COGENT) | yes | no |
| **lesson-plan-grounded (this study)** | yes | **yes** |

**H2.** Does conditioning lesson-plan-grounded generation on individual learner-performance
evidence produce material better targeted to the learner's demonstrated needs than reuse of
the class-level worksheet?

> The H2 instantiation retains the same instructional worksheet genre but conditions
> generation on learner-performance evidence, allowing instructional support, worked
> examples and practice to be adapted to demonstrated learner needs.

**The input is learner-performance evidence, not classwork.** Marked classwork is what that
evidence happens to be in this Nigerian case; the framework does not depend on a setting
having classwork, or calling it that. Quiz responses, homework, an exit ticket, an assessment
or a diagnostic task all serve.

```
learner-performance evidence
        ↓
map the wrong response to its objective
        ↓
adapt: strengthen conceptual support · add a worked example · change scaffolding
       select bridging practice · address the demonstrated error
```

**Correction is one adaptation strategy, not a mandatory section.** That is more general than
"generate a correction section", and it keeps the artefact genre identical between P0 and P1
so the manipulation is the evidence and nothing else.

Each adaptation still needs its own pedagogical justification; varying the
worked-example-to-problem ratio by proficiency, for instance, rests on expertise reversal.

Only P1 receives learner state:

```
H1  C0–C4   personalisation.mode = none               uses_learner_state = False
H2  P0      personalisation.mode = reuse_base         uses_learner_state = False
H2  P1      personalisation.mode = objective_indexed  uses_learner_state = True
```

**The H1 artefact is therefore not corrective.** Corrective instruction in Bloom's and
Guskey's sense depends on learner-performance evidence identifying individual difficulty. No
H1 condition receives such evidence. H1 generates a common post-class review-and-practice
worksheet; learner-responsive correction is introduced by H2.

**And P0 versus P1 is not a complete test of mastery learning.** Guskey's cycle runs
instruction → formative assessment → identify non-mastery → *different* corrective activity →
**reassessment**, with the corrective engaging the material differently from the original
instruction. P0 reissues the class worksheet, which is already downstream of the classroom
instruction rather than being it, and H2 carries no subsequent mastery check. State it as:

> P0 versus P1 operationalises a central corrective-instruction distinction — reusing common
> review material versus generating targeted material from evidence of individual
> non-mastery. P1 is **informed by** mastery-learning correctives; the study evaluates
> corrective-material generation, not the full mastery-learning intervention cycle.

**Individualised, not personalised.** P1's learner model holds objective-indexed mastery and
the distractors chosen. *Individualised* describes adaptation on current performance
evidence; *personalised* is reserved for a broader model — prior mastery, prerequisites,
language, motivation, interests, agency. The distinction is operational and narrower than the
inconsistent usage in the literature. FACET is prior work rather than a baseline: it models
prior knowledge, motivation and learning differences beyond performance and frames its output
as differentiated material.

---

**Citations are named by author and not yet verified against sources.** Ziegler et al.;
Atkinson, Derry, Renkl & Wortham; Durkin & Rittle-Johnson; Rittle-Johnson, Schneider & Star;
Bloom; Guskey; Merrill; Rosenshine. Each needs checking before it reaches the thesis.
