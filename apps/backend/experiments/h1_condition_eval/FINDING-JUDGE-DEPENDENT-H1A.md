# The taught-lesson result is judge-dependent

**2026-08-20.** `clean-six`, the corrected-notes generation, has now been judged **four**
times over byte-identical packets: twice by `claude-sonnet-4.5`, once by `claude-opus-5`
and once by `claude-sonnet-4.6`. Only the judge changed between them.

## C1 − C0, the registered endpoint

Taught-lesson alignment, the dimension the claim rested on, across all four:

| pass | judge | C1 − C0 | direction | p |
| --- | --- | ---: | --- | ---: |
| A | sonnet-4.5 | +1.06 | 6 up, 0 down | **0.0312** |
| B | sonnet-4.5 | +0.78 | 4 up, 2 tied | 0.125 |
| C | opus-5 | +0.78 | 4 up, 2 tied | 0.125 |
| D | sonnet-4.6 | +0.61 | 3 up, 2 tied, **1 down** | 0.3125 |

And every dimension, for the three passes with per-lesson detail to hand:

| dimension | sonnet-4.6 | 4.5 pass A | 4.5 pass B |
| --- | --- | --- | --- |
| Objective and curriculum alignment | +0.67 (3up/3tie/**0dn**) | +0.44 (3up/3tie/**0dn**) | +0.33 (2up/4tie/**0dn**) |
| Taught-lesson alignment | +0.61 (3up/2tie/1dn) | **+1.06 (6up/0tie/0dn)** | +0.78 (4up/2tie/0dn) |
| Scope and conceptual correctness | +0.50 (5up/0tie/1dn) | +0.28 (5up/0tie/1dn) | +0.11 (3up/1tie/2dn) |
| Student-facing clarity and usefulness | **−0.06** (3up/0tie/3dn) | +0.39 (4up/2tie/0dn) | +0.39 (4up/2tie/0dn) |

## What this changes

**The "6 of 6, p = .0312" on taught-lesson alignment was one pass of four.**
Pass B, the same model over the same packets, returned 4 up / 2 tied / 0 down — not the
6/6 the one-sided Wilcoxon floor needs at n = 6. The pooled 6/6 recorded earlier survives
only because pass A breaks pass B's two ties upward, so it is an artefact of averaging,
not two independent confirmations. A better judge does not reproduce it at all: 4.6
returns 3 up / 2 tied / 1 down.

**Clarity reverses.** +0.39 under both 4.5 passes, −0.06 under 4.6. A dimension whose sign
depends on the judge cannot carry a claim.

**The margins sit inside the noise.** `RATING-RESULTS.md` reports the within-arm spread
across generation draws at 0.33–0.67 per dimension, against C1−C0 margins of 0.50–0.67.
By the report's own standard — *"a margin smaller than this is not distinguishable from
re-running the same condition"* — most of the ladder is not distinguishable from re-running
C1 against itself.

## What survives

**Objective and curriculum alignment is the one dimension that never goes backwards.**
Three passes, two judge models, eighteen lesson-level comparisons: **zero** lessons where
C0 beats C1. It is small (+0.33 to +0.67) and only 2–3 lessons of 6 move at all, but the
direction never inverts, which is more than any other dimension can claim.

That is a defensible descriptive statement. It is not p < .05 on the registered endpoint,
and it should not be dressed as one.

## What to do next

1. **Do not report the 6/6 result.** If it appears in a draft, it needs replacing with the
   three-pass table above.
2. **Characterise 4.6's noise before trusting its margins**, the same way 4.5 was
   characterised: judge the identical packets twice and measure how much moves. The
   existing figure — 19% of scores moving, mean 0.19 — belongs to 4.5 and does not
   transfer.
3. **The endpoint is n = 6, and that is the binding constraint — not the judge.** The test
   counts direction, not size, so six lessons all agreeing is the strongest evidence
   available: p = 0.0156 one-sided, 0.0312 two-sided. Nothing below that is reachable at
   n = 6 however large the effect. Ties make it worse by dropping pairs: pass B's two ties
   took n to 4, where the best attainable p is 0.0625, so it could not have reached
   significance whatever the packs contained. Eight lessons would put the floor at 0.0039.
   More lessons, or a redefined pair that raises n, is the only route to a p-value.

4. **Settle one-sided vs two-sided.** STATUS.md, HANDOFF.md and BLIND-RATING-REPORT.md
   describe the analysis as one-sided but quote 0.0312, which is the two-sided floor. The
   one-sided floor is 0.0156. This has to match whatever was frozen.

See [[project-bedrock-model-access-2026-08-20]] for why 4.6 rather than Sonnet 5, and
`RATING-RESULTS.md` in `runs/clean-six/rating/` for every judgment with its evidence.
