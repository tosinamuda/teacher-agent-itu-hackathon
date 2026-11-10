# Working brief — what to fix, what to generate, what to decide

For me, not the supervisor. Written 2026-08-05.

---

## 0. Done: week 5 is now real data

Transcribed from `GTC Data/week 5 - 3rd Term/` and re-frozen. The capacity objective was
**dropped**, against the recommendation below: no step teaches it — Step 1 gives properties
of cylinders and spheres, Step II derives `V = lbh` — and capacity is a distinct quantity
from volume, so no step covers it by implication. Same rule as `t3-w04`, where four planned
objectives were trimmed to the two delivered, and the opposite of `t3-w06`, where the
compound objective was **split** because both of its constructions do have steps. The
reasoning is recorded in the transcript's own frontmatter. Evaluation Q5 was omitted: the
photograph does not show enough of the shape to state the question.

The original brief follows.



`GTC Data/week 5 - 3rd Term/` has her actual handwritten plan, 4 pages. Until now `t3-w05`
used a **Siyavula-derived supplement**, not her note. That is the weakest data claim in the
whole study and it can now be removed.

What the real plan contains, read off the photographs:

| | in the real plan | in our eval set today |
|---|---|---|
| Topic | THREE DIMENSIONAL SHAPES II | same |
| Objectives | **3** — properties of cylinders/spheres; volume of cube and cuboid; **calculate capacity** | **2** — the capacity objective is missing |
| Step 1 | properties of cylinder (4) and sphere (3), **+ Student Activity, 2 questions** | no activities |
| Step 2 | derivation of `V = lbh` and `V = l³`, **3 worked examples**, + a prism worked example | present via the supplement |
| Evaluation | **5 questions** (cuboid 8×4×3, cuboid 5×2×3, cube 4×4×4, a tank depth problem, a shape) | **no evaluation step at all** |

Three consequences, all good:

1. **It fixes the worst C1 lesson.** `t3-w05` is one of the two lessons where C1 adds
   nothing, precisely because it has no evaluation step. The real plan has five evaluation
   questions. After transcription, 4 of 5 lessons carry evaluation questions into C1.
2. **It confirms the prism formula.** Her own words: *"Volume of prism = Area of base ×
   height"*. That is the formula the supplement announced and then left blank, which I
   restored from the supplement's own later usage. Her handwriting now confirms it.
3. **A third objective appears** — "calculate capacity". Adding it changes the objective
   count for that lesson, so the unit count changes with it.

**Where to do the work.** Transcribe to
`~/Documents/Unilag/Masters/Thesis/Dataset/transcripts/t3-w05/`, following `SCHEMA.md`, the
same as the other transcripts — `teacher.md` archival, `teacher-cleaned.md` derived. Then
rebuild the eval-set entry, re-export `notes-clean/t3-w05/`, and re-declare the digests.
By hand, file by file, as with everything else in `notes-clean/`.

**Decide:** whether the 3rd objective ("calculate capacity") stays. It changes `t3-w05`
from 2 units to 3, which changes packet counts. Her plan states it, so I would keep it.

---

## 1. Problematic data, and where each is fixed

| lesson | problem | where to fix | state |
|---|---|---|---|
| t3-w05 | note is a textbook supplement, not hers; 1 objective missing; no evaluation step | transcribe `GTC Data/week 5 - 3rd Term/` | **done — §0** |
| t3-w06 | objective (i) named two constructions in one clause; Step 2 coded to nothing | split into parallel and perpendicular: 5 objectives, 6 steps | **done** |
| — | C0 read `entry_behaviour: []`, so the control was told what it was denied | `prompt_lesson` in `generation.py`; issue #161 | **done** |
| t3-w02 | 14 figures, **0 captions** — the pack cannot name a figure it must refer to | `notes-clean/t3-w02/`, add `**fig-NN.**` captions by hand | **done — 14 labelled, 10 descriptions written from the compiled drawings; t3-w04's 7 too. 38/38 named** |
| t3-w04, t3-w09 | evaluation questions are **researcher-assembled**, not her Evaluation line — t3-w09's sets work from the textbook by reference ("Exercise 17a No 3 and 4 page 158 NGM"), so that text is nowhere in the plan | recorded as `plan-content/@author` on the documents; needs saying in the writeup | open, disclose |
| t3-w02, t3-w09 | a core step's `content` is its title repeated, and `t3-w09-03` — the step teaching the four collection methods — has no activities either | source pages | **done 2026-08-24 — 8 of 17 core steps said ≤4 words beyond their objective; each now names what her own note covers. The two she never narrated carry a researcher sentence in the binding, not the body. See each lesson's `_cleaning-log.md`** |
| t3-w06 | no evaluation step at all, so `assessment_points` is empty for the lesson | see the row below | open |
| t3-w02 | pack carries about half the lesson; it is the largest lesson against the smallest pack | not a data fix — pack length or split the lesson | open, decide |
| t3-w06 | fig-03/fig-05 set squares had no right angle; mark on a 62° corner | `notes-clean/t3-w06/step-t3w06-02.md` | **done** |
| t3-w06 | bisection steps stopped before joining P–Q | `step-t3w06-03.md`, steps 5–6 + midpoint `M` | **done** |
| t3-w06 | 90° construction had no written procedure | `step-t3w06-04.md`, reconstructed from the photograph | **done** |
| t3-w06 | no evaluation step → C1 gets nothing | check the `not-picked` source photos for an evaluation section | open |
| t3-w09 | objective 2 ("analyse and interpret") is never taught | leave it — a real property of the data | won't fix |
| t2-w09 | BODMAS never stated; bracket insertion never taught | leave it — same reason | won't fix |
| all | classroom narration was reaching the model | `profiles.py`, `include_teacher_student_activities=False` | **done** |
| t3-w06 | all five construction steps read "explains"; she **draws** each one on the board step by step, explaining aloud, while the class replicates | teacher, via researcher | **done 2026-08-24 — step 3 also gained the student activity it never had, so C1 now receives a task for it** |

---

## 2. The one blocking decision: what C1 is

C1 must beat C0 in **all five** lessons for H1's main test to reach significance. It
currently leads in none. Three changes, in order of expected effect:

1. **Give C1 the position of each section in the lesson** — "this is step 2 of 4; step 1
   covered X; step 3 covers Y". The plan genuinely specifies it, every lesson has it, and it
   is not teaching content so it does not blur C1 into C2. This is the substantive change.
2. **Drop `estimated_minutes`.** A learner revising at home does not need the step's
   duration. Same category as the narration already removed.
3. **Resolve `explain_only`.** It describes how the lesson ran, but the pack applies it to
   itself and writes fewer practice questions. The pack specification requires practice in
   every section. Either stop sending the tag, or state in the specification that it
   describes the lesson and not the pack.

After §0, evaluation questions reach C1 in 4 of 5 lessons instead of 3, which also helps.

**Then freeze.** Once rating starts, C1 cannot change.

---

## 3. Packets, raters, and the arithmetic

### H1 — five lessons, C2/C3 on all five (my decision, 2026-08-05)

| condition | lessons | generations each | packets |
|---|---|---|---|
| C0 | 5 | 3 | 15 |
| C1 | 5 | 3 | 15 |
| C2 | 5 | 1 | 5 |
| C3 | 5 | 1 | 5 |
| | | **total** | **40** |

40 packets × 3 ratings = **120 H1 ratings**. That is 8 packets per lesson.
*(The frozen design said C2/C3 on 3 lessons = 36 packets / 108 ratings. Five lessons is a
change to record, not to hide.)*

### H2 — three lessons with marked classwork

Classwork exists for **4 weeks** and all 9 students: `week 9 - 2nd Term` (t2-w09),
`week-2 - 3rd Term` (t3-w02), `week-4 - 3rd Term` (t3-w04), `week-6 - 3rd Term` (t3-w06).
Of these, **t3-w04 has no plan in the eval set**, so H2 uses t2-w09, t3-w02 and t3-w06.

3 lessons × 9 students × 2 conditions = **54 packets** → **162 H2 ratings**.

### Totals

| | packets | ratings |
|---|---|---|
| H1 | 40 | 120 |
| H2 | 54 | 162 |
| **total** | **94** | **282** |

### Per rater

| raters | ratings each | at ~10 min per rating |
|---|---|---|
| 5 | 56 | ~9 hours |
| 6 | 47 | ~8 hours |
| 8 | 35 | ~6 hours |

**Recruit 6 if possible.** Nine hours is a lot to ask of a volunteer; eight is still a lot.
This is the number to quote when asking, and it argues for paying them.

### Assignment rules — do not break these

- **H1: assign whole lessons.** A rater who takes a lesson rates all 8 packets for it
  (C0×3, C1×3, C2, C3). Never assign by condition — that mixes rater severity with the
  condition under test.
- **H2: assign whole learners.** Whoever rates P0 for a learner also rates P1 for that
  learner. Never split P0 and P1 across raters — the test is paired.
- **Calibration:** 4–8 packets rated by everyone, to measure agreement.

---

## 4. H2 — the classwork does not match the objectives

This is the real H2 problem and it is already decided (D12/D15); this is the operational
version.

**What is wrong.** The classwork does not assess the lesson's stated objectives:

- the source differs every time — sometimes the Step-1 Student Activity, sometimes the
  Evaluation with the numbers changed, sometimes the textbook by reference;
- coverage is partial — usually about **one** objective out of three to five;
- `t3-w02`'s classwork assesses **none** of its five stated objectives;
- some classwork reaches into the **next** topic.

**Why it cannot be patched.** The lesson's objective list is not a reliable index of what
the learner was actually assessed on. If P1 personalises against the plan's objectives, it
personalises against evidence that does not exist.

**The rule to apply:**

> Bind learner state to the **curriculum subtopic**, not to the lesson's stated objectives.
> Identify what was assessed from the **scripts**, never from the plan.

**What that means to do, per lesson:**

1. Read the marked scripts. For each question, record which curriculum subtopic it assesses.
   The plan does not decide this; the question does.
2. Build the learner's state against those subtopics — mastered, partial, or a named
   misconception read from the learner's own working.
3. Generate P1 only for the subtopics the learner has evidence for. Where there is no
   evidence, P1 must fall back to the base pack content rather than invent a weakness.
4. Where classwork reaches into the next topic, that evidence belongs to the next topic's
   subtopic. Keep it — it is real learner evidence — but it only drives P1 when that
   subtopic appears in the pack being personalised.
5. **Objective preservation is still judged against the lesson's objectives.** The learner
   evidence is subtopic-indexed, but P1 must not drop a lesson objective. That is rubric
   dimension 5 and it stays as it is.

**State this as a limitation, not a defect.** Classwork in a real classroom assesses what
the teacher chose to assess that day. A system that requires classwork to map one-to-one
onto the plan's objectives would not work in this school. Deriving the assessed set from
the scripts is the design response, and it is the more honest one.

---

## 5. Order of work

1. Transcribe week 5 (§0). Rebuild the eval set. Re-declare digests.
2. Decide the third objective for `t3-w05`.
3. Implement C1: sequence position; drop timing; resolve `explain_only` (§2).
4. Re-run C0/C1 on 5 lessons × 3, check whether C1 now leads.
5. Caption `t3-w02`'s 14 figures.
6. Freeze the conditions. Record the freeze.
7. Re-run all conditions; export the 40 H1 packets.
8. Teacher approves the base pack — H2 is gated on this.
9. Build subtopic-indexed learner state from the scripts (§4).
10. Run P0/P1; export the 54 H2 packets.
11. Raters: recruit 6, assign by lesson (H1) and by learner (H2).
