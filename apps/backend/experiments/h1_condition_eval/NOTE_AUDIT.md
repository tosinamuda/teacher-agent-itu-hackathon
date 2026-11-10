# Source-note audit (2026-08-04)

Five independent auditors, one per lesson, each reading **exactly the evidence the
generator receives** (note with TikZ replaced by figure references), unprimed.

## Why this was run

Round 8 (`compose` vs `packed` at C3) came out a wash: overall 3.40 vs 3.47, per-lesson
2–3. The rater rationales kept naming defects that looked like model failures. They are
mostly not.

## What the notes contain

| lesson | note errors | figures unlabelled | objective with no written method | round 8 |
|---|---|---|---|---|
| t2-w09 | 1 | 0 / 0 | obj 2 insertion, obj 3 "solve" | compose 3–0 |
| t3-w05 | 0 | 2 / 15 | prism formula absent from the text | compose 3–0 |
| t3-w02 | 5+ | **14 / 14** | obj 1 comparisons, half of obj 2 | packed 2–1 |
| t3-w09 | 0 | 0 / 0 | **obj 2 entirely untaught** | packed 3–0 |
| t3-w06 | 4 | 0 / 14 | **obj 3 has zero procedure** | packed 3–0 |

`compose` swept the two cleanest notes and lost the three broken ones. n=5, so
suggestive rather than proven — but it is the most parsimonious reading of a result
that otherwise looks like noise.

## Defect classes

**1. Errors in her note.** t2-w09's `(6x-y)-(4x-5y) = 6x-y+4x+5y` (recovered silently on
the next line). t3-w02's "length of the rope = circumference" (contradicted three lines
later), "divide both side by 44r" (the working divides by 44), rectangle "2 opposite
sides are equal", parallelogram and trapezium "no line of symmetry" (contradicting the
same document's square/rectangle rows). Fidelity and correctness are in direct conflict
wherever these appear.

**2. Editorial commentary reaching the model.** Caption prose carries remarks about what
drawings fail to show — "The point Q named in the instruction is not marked on the
drawing", "The four intermediate strokes are placed approximately", "No procedure is
written for this step". TikZ-internal comments (`%`, `_lesson-notes.md`) are stripped by
the pipeline; caption prose is not. 5 of 12 critic findings in round 8 were spent
removing this class.

**3. Missing method.** t3-w06 obj 3: no procedure at all. t3-w06 obj 2: stops before
joining P–Q, never states PQ meets AB at the midpoint. t3-w09 obj 2 ("analyse and
interpret"): the note builds tables and asks nothing of them. t3-w05: the prism formula
is announced ("calculated using this formula:") and then absent. t2-w09: BODMAS is never
stated; bracket *insertion* never taught.

**4. Absent figures carrying load-bearing data.** 16 of 43 drawing references reach the
model as `unlabelled` — all 14 on t3-w02. Three t3-w02 worked examples state their
dimensions only inside the solution; Example 10 never names its shape. On t3-w05 the
3 cm of Worked example 13.9 and the 24/192 of the packing derivation exist **only**
inside figure captions.

**5. Pipeline-side (ours, not hers).** `_drawings_as_references` emits
`[drawing attached to this section as unlabelled]` when a figure has no fig-NN label —
ambiguous between "the drawing is named unlabelled" and "the drawing has no labels".
Step titles ship curriculum tags (`*(core → objective 1)*`) to the model, and at least
one is wrong: t3-w09 step 3 is tagged objective 2, but it teaches construction while
objective 2 is interpretation.

**6. Spec forces invention where the note is silent.** `artefact_spec` requires every
practice question to carry its answer. t2-w09's three activities have no answers and
t3-w09 has no exercises at all, so the model must invent — and correctness scoring then
penalises the invention.

## Consequences for the experiment

- **Correctness scores partly measure note quality.** Six of round 8's most-cited defects
  trace to source gaps, including both arms' identical broken 90° construction.
- **Recall is scored against a target that is partly wrong, partly missing, and partly
  editorial commentary.** Copying a caption that says a drawing lacks a label counts as
  carrying the note through.
- **Lessons where an objective has no written method carry no signal** about which arm is
  better. Both arms invent; the comparison measures improvisation.

## Fix order (data, not prompts)

1. Split the caption field: description the model needs vs editorial commentary it must
   never see.
2. Restore or inline the absent figure data (t3-w02's dimensions especially), or mark
   those examples excluded from scoring.
3. Write the missing methods, or record per-objective that the note is silent and drop
   those objectives from fidelity/correctness scoring.
4. Fix the five mathematical errors, keeping a record of the originals — the
   fidelity/correctness conflict is a thesis finding worth reporting, not just a bug.
5. Strip curriculum tags from `title`; fix the t3-w09 step-3 mapping.
6. Replace the `unlabelled` fallback with something unambiguous.
7. Re-run the arms. Round 8 should be treated as measuring note quality as much as
   output channel.

## Addendum — independent geometry audit of t3-w06 (2026-08-04)

A second auditor was given `t3-w06`'s note and its objectives, with no access to this
document or to any pack, and asked only whether the geometry holds. It worked from the
TikZ coordinates, so its findings are computed rather than impressionistic. Full text:
`geometry_audit/findings.md`.

It reports four captions that assert what the drawing does not show — fig-13 names an arc
the figure has no arc commands for and whose four strokes are not equidistant from $C$;
fig-03 and fig-05 mark a right angle on a corner measuring ~62°, an arrangement that
cannot exist (if the two edges meet at 90° the ruler cannot lean); fig-08 shows no ruler
though the step refers to one; fig-14's arc starts above the line and never reaches $BC$.
It also confirms the bisection procedure stops before joining $P$ to $Q$, which this
document already recorded.

**These findings stay here.** They are about the transcription, and an earlier attempt
put them into the generation copies as honest captions — where they reached the model,
were paraphrased toward the learner, and were correctly flagged by the C3 critic as
meta-commentary. `notes-clean/` carries learner-facing text only; every paragraph it adds
to the frozen note is now declared and digested (`note_editorial declare`).

**It validated the reconstructed 90° procedure.** Steps 1–6 are "complete and correct,
including its step-3 justification that arcs of radius $DC$ struck from $D$ and $E$ are
externally tangent and meet only at $C$." That justification is what finally made the
tangency error detectable: for four rounds both arms silently produced same-radius arcs
that never meet, and no critic saw it, because nothing in the note contradicted it.
Written down, it becomes a self-contradiction the critic can catch.

## Addendum — the two "missing method" gaps that were transcription losses (2026-08-04)

Of the six objectives this audit recorded as having no written method, two turned out to
be recoverable from the documents themselves rather than absent from her teaching. Both
are now filled, and both are declared in `note_editorial.DECLARED_ADDITIONS`.

**t3-w06 obj 2 — bisection.** Her numbered steps end at "cut the first arc at P and Q";
executed literally they leave the segment unbisected. But **fig-12 already draws the
completion** — the join, the crossing at the middle, the right-angle mark. The prose
stopped one step short of her own diagram. Steps 5–6 now say what the drawing shows, and
the crossing is labelled $M$, which the figure marks but never named. This was the
largest single source of C3 findings: 5 of 12, in all three draws, all of them the model
filling the gap by claiming the arcs "intersect the line" when they intersect each other.

**t3-w05 — the prism formula.** The note announces "The volume of a prism is calculated
using this formula:" and the next line is blank. The same blank is in the source markdown
(line 357) and in the rendered PDF, so the formula was lost before transcription, not by
our split. It is fully determined by the sentence immediately above it ("multiplying the
area of the base of the prism by the height of the prism") and the note writes it out in
full twice later in the same file, so it was restored in the note's own notation:
`\text{Volume} = \text{area of base} \times \text{height of the prism}`.

**The other four stay open, deliberately.** t3-w09 obj 2 ("analyse and interpret"),
t2-w09 obj 2 (bracket insertion), t2-w09's unstated BODMAS, t2-w09 obj 3 (word problems)
and t3-w02 obj 1 (properties of plane shapes) have nothing on the page to recover — she
did not teach them. Filling them would be writing curriculum, and the eval set would stop
being real teacher notes. They remain a declared property of the dataset, and they are the
argument for fix-and-flag: the system should report that the note is silent rather than
improvise a lesson, which is the behaviour raters ranked highest (flag > reproduce >
invent).

## Addendum — fig-03 and fig-05 redrawn (2026-08-04)

The geometry audit's fig-03/fig-05 finding turned into output: three C3 findings, e.g. *"the
ruler's edge meets the set square at a right-angle — but the ruler is aligned with that edge,
so they are collinear."* The model was faithfully reproducing a contradiction in the drawing.

**What was wrong.** Both set squares were drawn with angles 62/94/24 — no right angle anywhere —
and the right-angle mark was placed at the ruler/set-square junction instead of at the set
square's own corner. The arrangement cannot exist: if those two edges met at $90^\circ$, the
ruler could not lean.

**The reading that fixed it** (researcher's, from the notebook page): fig-02/fig-04 and
fig-03/fig-05 are **the same construction, not two methods**. The ruler simply rests against a
different edge of the set square — the upright edge (ruler vertical) or the sloping edge (ruler
leaning). The slanted line is the guide ruler, never the parallel line being constructed. Her
notebook is confusing because it never labels the two drawings as alternative ruler positions.

**Both are now drawn from a right-angled triangle**, with the mark at the corner where the edge
on $AB$ meets the upright edge, and the ruler a hairline clear of the sloping edge so the set
square stays visible — her original layered them into one line. fig-03 is fig-02's set square
unmoved, only the ruler changed edge. fig-05's two positions are one pure translation apart:
every vertex moves by exactly (3.850, 2.200), parallel to the ruler, angles identical — sliding
along a held ruler cannot rotate it, and the figure now demonstrates that rather than asserting
it. Verified by computing the angles and by rendering through pdflatex; pinned by
`test_the_redrawn_set_squares_carry_a_real_right_angle`.

**Still open:** her prose steps (a)/(b)/(c) lack a starting condition, the "hold the ruler
firmly" instruction, and the concluding $PQ \parallel AB$. A corrected 7-step procedure exists
but rewriting her procedure text is a larger change than remaking a figure and has not been made.
