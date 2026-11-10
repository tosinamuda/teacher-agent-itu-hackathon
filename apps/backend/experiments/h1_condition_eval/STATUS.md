# H1/H2 pilot status — open issues and what remains

Written 2026-08-05, after the pilot round that re-established the C0–C3 ladder on a
working generator. Everything here is measured, not estimated; run labels are given so
each number can be re-derived.

## 1. Where the study stands

The analysis plan is frozen (2026-07-26). The **condition operationalisation is not**, and
that is what the current pilot is for. No expert ratings exist yet, so C1's definition can
still change; once rating begins it cannot.

| | frozen design | built? |
|---|---|---|
| H1 C0, C1 | 5 lessons × 3 generations = 30 packets | yes — runs clean |
| H1 C2, C3 | 3 lessons × 1 generation = 6 packets | yes, but on 5 lessons (see §3.5) |
| H1 total | 36 packets, 108 ratings @ 3 raters | not yet exported |
| H2 P0/P1 | 3 lessons × 8–9 students × 2 = 48–54 packets, 144–162 ratings | pipeline exists; not run at this scale |

H1a (C1 vs C0, one-sided Wilcoxon, n = 5 lesson-level pairs) has a floor of **p = .0312**
and therefore **requires a clean 5/5 sweep**. At 4/5 the best attainable is .0625.
H2 (P1 vs P0, paired at the learner level, n ≈ 24–27) is comfortably powered, p ≈ 10⁻⁷.

## 2. What is working

- **The generator.** `compose-v2` (native tool calling) completes 100/100 cells with zero
  failures. Its predecessor failed 5 of 6 on the same workload (§3.1).
- **The C2 grounding effect is large and consistent.** Mean recall C1 0.444 → C2 0.819
  (`h1-dfb6998a9b`). Adding her note is what puts her material into the pack.
- **The deterministic proxy.** `metrics.py` recall — the fraction of the note's quantities
  reaching the pack. Stable at sd ≈ 0.04, ~50× tighter than the critic's finding count.
- **Data repairs verified.** Bisection method completed from her own fig-12; t3-w05's
  prism formula recovered; fig-03/fig-05 redrawn with real right angles. Each is declared
  with a digest in `note_editorial.DECLARED_ADDITIONS`.

## 3. Open issues

### 3.1 `dspy.ReAct` silently discarded most generations — FIXED, but invalidates old numbers
**What.** A half-adopted dspy 3.1.3 → 3.3.0b1 upgrade made adapter parsing strict while the
compose arm still used the prompt-parsed `ReAct` loop. On the real workload the model
echoes the tool call and its observation back as concatenated JSON, which no adapter reads.
**Evidence.** Same model, same inputs, only the loop differing: `ReAct` **5/6 failures**
at ~30 LM calls per section; `ReActV2` **0/6** at 6–8 calls.
**Effect on the test.** Every compose result predating 2026-08-04 is **self-selected** —
only the cells that happened to parse were recorded. Those numbers cannot be quoted.
**Status.** Fixed (arm `compose-v2`, dspy pinned 3.3.0). Old runs must be re-generated.

### 3.2 The critic's finding-count cannot compare conditions
**What.** 15 draws, identical inputs, zero failures: `0 2 0 2 7 1 0 0 4 3 3 0 0 1 0`.
Mean 1.53, **sd 2.03** — larger than the mean. Seven of fifteen draws return zero.
Three consecutive 5-draw blocks average **2.2 / 1.6 / 0.8** from unchanged inputs.
**Effect on the test.** Detecting a 1-finding/draw difference needs ~64 draws per arm.
Any comparison at n = 5 is noise. Recall (sd 0.04) is the screening instrument; findings
text is read qualitatively for *what* went wrong, never counted.

### 3.3 C1 is barely distinguishable from C0 — the confirmatory endpoint is at risk
**What.** The plan's *narration* is classroom choreography or a bare step label, never
teaching. On the 9 core steps that carry activities it is "Teacher solves some questions in
order of operation on the board while students listen, contribute … copy worked examples
into their notes"; on the other 5 it is a heading — "Step IV — perimeter of plane shapes",
`**Objective:** Find the volume of a cube and a cuboid`. The only mathematical notation
anywhere in it is t3-w06's two angle measures ($90^\circ$, $60^\circ$), and those are in
that lesson's objectives too, so C0 already has them. Across the 14 core steps of the
frozen plans, `content` totals 1,835 chars against the note's 50,005 — a ratio of **1:27**
(per step, 35–336 vs 369–18,359).
C0 and C1 already share an identical `lesson_context` including the full objectives list,
so the C0→C1 delta is step title (≈ the objective restated), `instructional_type`,
`estimated_minutes`, materials — plus `assessment_points`.
**The one real exception is `assessment_points`,** which carries her *evaluation questions*
verbatim ("Simplify (a) $14pq \times r$", "How many triangles can an octagon be divided
into…"). Those are
mathematics, and they do reach C1 — but **only in 3 of the 5 lessons**: t2-w09 (5),
t3-w02 (9), t3-w09 (3), and **zero** for t3-w05 and t3-w06, which have no evaluation step.
**Evidence.** C1 never clears C0 on recall: **0 of 5** lessons in `h1-dfb6998a9b` (100
cells, choreography still in) and **0 of 5** after it was removed (`h1-0df0443b86`, 30
cells) — never the 5/5 the endpoint needs. Aggregate by the **median** across generations,
as the frozen plan specifies; on the mean, t3-w05 flips to C1 by 0.009 (0.257 vs 0.248) and
the count reads 1 of 5. That flip is an artefact of the aggregation rule, not a result, and
the pre-specified rule is the median. Section counts are identical
because step↔objective is 1:1 in her plans (3/3, 3/3, 2/2, 4/4, 2/2). Measured on the whole
rendered prompt across the 14 units, C1 sends **+154 to +1,309 characters** more than C0
(3.1%–25.9%, mean +322 / 6.5%). The one large increment is the single t3-w02 step carrying
8 of that lesson's 9 evaluation questions, one of which embeds a TikZ figure; the other 13
units sit between +154 and +380 (3.1%–7.7%).
**Why the non-uniformity matters more than the thinness.** H1a needs a clean 5/5 sweep, and
C1's one substantive increment is missing from two lessons *by construction*: t3-w05 and
t3-w06 have no evaluation step, so they get structure only. Recall cannot settle which
lessons those are — C1 has never swept, and which lessons tie or lose moves between runs
(t3-w05 0.277 = 0.277 and t3-w06 0.337 vs 0.358 in `h1-dfb6998a9b`; t3-w05 0.257 vs 0.248
and t3-w06 0.368 = 0.368 in `h1-0df0443b86`), because C1 never sees the note the proxy
scores against (§3.7). A condition that is substantive in three lessons and near-empty in
two cannot reliably sweep five.
**Effect on the test.** H1a needs 5/5 in C1's favour. As operationalised, C1 adds almost
nothing, so a null result would measure the thinness of the condition rather than the
hypothesis.
**Partly fixed.** Choreography removed (`include_teacher_student_activities=False`) —
justified independently because the artefact spec forbids writing about the lesson as an
event. It narrowed the gaps without closing them: re-running C0/C1 after the change
(`h1-0df0443b86`, medians) leaves C1 tied in three lessons (t3-w05 0.231, t3-w06 0.368,
t3-w09 0.727) and behind in two (t2-w09 0.591 vs 0.727, t3-w02 0.410 vs 0.436). t3-w09's
deficit closed from 0.145 to zero and t3-w06's from 0.021 to zero, so the choreography was
doing real harm — but ties do not win a one-sided test.
**Still to decide (§4.1).**

### 3.4 `instructional_type: explain_only` fights the artefact spec
**What.** The tag describes how the *lesson* was delivered, but is applied to how the
*pack* is built. The spec requires every section to carry practice questions with answers.
**Evidence.** In C1, `explain_only` yields 3.06 blocks/section vs 3.52 for
`explain_example_practice`. C0, which never sees the tag, shows no such gap (3.83 vs 3.90).
**Effect on the test.** Suppresses practice in a revision pack, and depresses C1 relative
to C0 — the wrong direction for the confirmatory endpoint.

### 3.5 C2/C3 evidence source differs from the frozen design
**What.** The freeze restricts C2/C3 to 3 lessons because evidence resolves to *ingested
textbook* records (Ch 10, 12, 13). The harness instead feeds C2/C3 from **her note**, which
is why all five lessons produce evidence.
**Effect on the test.** Two different operationalisations of "explicit source grounding".
The thesis must state which one it claims. Note-grounding is defensible and gives 5 lessons
instead of 3; textbook-grounding matches the original wording.
**Decision:** proceed on note-grounding for the pilot (researcher's call, 2026-08-05).

### 3.6 Replication is not seeded
**What.** The 3 generations per lesson differ only by provider non-determinism at
temperature 0. Nothing is declared or reproducible.
**Effect on the test.** A confirmatory endpoint's replication should be reproducible.
dspy threads `rollout_id` into the cache key for exactly this; it is not yet used.

### 3.7 Recall cannot separate correction from loss
**What.** Recall measures how much of *her* material reaches the pack. A pack that
correctly fixes her error scores **lower**, because the corrected line carries different
numbers.
**Effect on the test.** Recall is a fidelity screen, not a quality judgement. It is why the
blind expert rating exists, and it should be stated as a limitation rather than fixed.

### 3.8 Repair can destroy more than it fixes — mitigated
**What.** A one-word grammar finding ("statistic" should be "statistics") triggered a
whole-section rewrite that halved recall, 1.000 → 0.545, deleting the lesson's tally data
while making the pack *longer*.
**Fix.** Span-local editing (`--repair edit`). t3-w09 sd 0.18 → **0.00**; t2-w09
0.991 → 1.000. Means barely move (0.808 → 0.824) because catastrophes are rare — the point
is that they stop happening.

### 3.9 t3-w02's 14 drawings have no captions
**What.** 14 TikZ figures, **0 `fig-NN` captions** — the only lesson in that state
(t3-w06 has 14/14, t3-w05 13/15). The pack cannot cite a figure it cannot name.
**Effect on the test.** Real but *not* the cause of t3-w02's low recall — that is pack
size (6.6k chars for a 13.5k-char lesson with 39 quantities). Recall tracks the pack/note
ratio across all five lessons.

## 4. To complete H1

1. **Decide what C1 is** (§3.3). Recommended: plan structure **+ sequence position** — each
   section told it is step 2 of 4, what preceded, what follows. Uniform across all five
   lessons, uses only plan content, and gives C1 a mechanism a rater can see (sections that
   build rather than four islands). Also drop `estimated_minutes` (lesson-event metadata)
   and resolve `explain_only` (§3.4).
2. **Freeze the condition definitions** and re-run the full ladder.
3. **Seed replication** with `rollout_id` (§3.6).
4. Re-run C0/C1 at 5 × 3 and C2/C3 at 5 × 1; export blinded rater packets.
5. **Recruit raters** — 3 ratings per packet, 108 H1 ratings (§5).

## 5. To complete H2

1. P0/P1 over the approved C4 base pack, 3 lessons × 8–9 students × 2 conditions.
2. H2 is gated on C4 teacher approval; the base pack must be approved first.
3. Learner evidence comes from the marked scripts (constructed response, teacher-marked),
   with misconceptions derived from student *working*.
4. Blinding invariant: raters must see P0/P1 **before** any teacher edit, or H2 becomes
   "teacher-mediated".
5. 144–162 ratings at 3 per packet.

## 6. Raters — the binding external constraint

Everything above is code and data work that can be finished locally. The study cannot
conclude without **expert human ratings**:

- **H1:** 36 packets × 3 = **108 ratings**
- **H2:** 48–54 packets × 3 = **144–162 ratings**
- **Total ≈ 250–270 rating submissions**

The rubric is section-level, 1–5, five dimensions. Raters do not need to rate everything —
the queue is assignment-scoped, and the design only requires that a rater who takes a
lesson rates all of C0–C3 for it (H1), or both P0 and P1 for a learner (H2), so that rater
severity is not confounded with condition. A shared calibration set of 4–8 packets rated by
everyone lets inter-rater consistency be estimated.

**Ask:** whether post-graduate education students (ideally mathematics education) can be
recruited and paid for rating, or whether the supervisor knows practising/trainee maths
teachers willing to take a block. 5–6 raters would comfortably cover the workload.
