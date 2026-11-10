# clean-six, judged — 2026-08-20

72 packs, six lessons, C0–C3, three draws, rated blind **twice** by
`openrouter/anthropic/claude-sonnet-4.5` (not the generator's `gpt-oss-120b`). One
candidate per call, opaque ids, judge cache off so the second pass is independent.

## The endpoint, pooled over both judges

C1 − C0, per lesson, on the frozen rubric. Two-sided Wilcoxon signed-rank, n = 6.

| dimension | mean | direction | p |
| --- | ---: | --- | ---: |
| Objective and curriculum alignment | +0.389 | 3 up, 3 tied, 0 down | 0.25 |
| **Taught-lesson alignment** | **+0.917** | **6 up, 0 tied, 0 down** | **0.0312** |
| Scope and conceptual correctness | +0.194 | 4 up, 1 tied, 1 down | 0.375 |
| Student-facing clarity and usefulness | +0.389 | 4 up, 2 tied, 0 down | 0.125 |

0.0312 is the two-sided floor for n = 6, so on this test taught-lesson alignment is as
strong as the design can report. **Note the test direction**: the floor is 0.0312
two-sided but **0.0156 one-sided**, and STATUS.md, HANDOFF.md and BLIND-RATING-REPORT.md
all describe the analysis as ONE-sided while quoting the two-sided floor. Which one the
frozen protocol registered needs settling before any p is reported.

> **SUPERSEDED, 2026-08-20.** A fourth pass on `claude-sonnet-4.6` returns
> 3 up / 2 tied / 1 down, p = 0.3125 — the first pass with a lesson going backwards.
> The result below does not replicate. See FINDING-JUDGE-DEPENDENT-H1A.md.

### It does NOT survive a fourth pass

The judge model was inherited, not chosen — `claude-sonnet-4.5`, two generations behind
what OpenRouter now serves. So the run was judged a third time with `claude-opus-5`:

| pass | judge | C1 − C0 | direction | p |
| --- | --- | ---: | --- | ---: |
| A | sonnet-4.5 | +1.056 | 6 up, 0 down | 0.0312 |
| B | sonnet-4.5 | +0.778 | 4 up, 2 tied, 0 down | 0.125 |
| C | opus-5 | +0.778 | 4 up, 2 tied, 0 down | 0.125 |
| **D** | **sonnet-4.6** | **+0.611** | **3 up, 2 tied, 1 down** | **0.3125** |
| pooled A–C | | +0.870 | 6 up, 0 down | 0.0312 |

**Only pass A reaches the floor.** B, C and D do not, and D is the first with a lesson
going backwards, so the sentence this section used to carry — "not one lesson where C1
scores below C0" — is no longer true.

The pooled A–C row is kept for the record but should not be quoted as a result: pooling
averages the passes per lesson, so A's margins break B's and C's ties upward and
manufacture a 6/6 that no single pass produced. Two passes agreeing is evidence; one pass
outvoting two ties is not.

Note also that B's 0.125 was not a near miss. Its two ties drop n to 4, where the best
attainable p is 0.0625 — **pass B could not have reached significance whatever the packs
contained.**

## What this is NOT

**It is not the note correction.** C1 receives no note, and the raw→clean swap was checked
directly: C0's and C1's requests are byte-identical under both, on all six lessons. Only
C2 changes, on the three lessons whose notes were edited. Whatever moved this, the notes
did not.

**The judge got much steadier, and that is the likelier story.** On identical prose the
August replication moved more than half of every arm's scores, mean 0.38–0.49. Here 54 of
288 scores moved — 19% — mean shift **0.19**. Same judge model. What changed is the packet
the judge reads: its reference sheet now carries **0 raw TikZ and 0 bare LaTeX commands**,
where the reference sheet is precisely what "taught-lesson alignment" is scored against. A
judge shown `\begin{tikzpicture}` instead of the question the teacher set cannot see what
was taught, and will score every arm low and noisily.

So the honest reading is that **C1 did not get better; the instrument got clearer.** That
is a finding about the measurement, not about conditioning.

**It cannot be proved directly.** The August packets are not on disk — `runs/*/rating/`
is untracked — so the reference sheets the earlier judges read cannot be re-examined. The
noise drop is evidence; it is not the same as showing the old sheet.

**And it is still a manipulation check.** An LLM judge asking whether the plan's
information is *visible* in the pack. The registered endpoint is the expert raters'.

## What would settle it

Rebuild packets for `c0c3-worksheet` with today's `rater_packets` and re-judge that
generation. Same packs, same judge, only the packet code differing — which isolates the
instrument from the generation. Everything needed is on disk.

## Housekeeping

`runs/*/rating/` should not be untracked. The packets are what a judged number means, and
two passes of them have already been lost.
