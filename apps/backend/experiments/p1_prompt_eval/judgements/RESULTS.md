# Manual judging — label-evidence vs excerpt-evidence (same prompt), 2026-06-11

Judge: manual read of all 15 blinded compare files, scored with reward.py
(max 12). Judgements: study_pack_v2-69ac0e90__vs__p1-69ac0e909e.json.

| run | evidence | mean reward (38 sections) |
|---|---|---|
| p1-69ac0e909e | REAL textbook excerpts | **11.29** |
| study_pack_v2-69ac0e90 | citation labels | 11.16 |

Per-criterion deltas (excerpt − label): grounding_fidelity +0.06,
tone_audience +0.03 (the label run produced one "the learner chose 300,000"
third-person echo), actionable_practice +0.05; targeting/support/preservation
identical. Verdict: **no regression, slight edge to real excerpts** — several
excerpt-run outputs quote the textbook definitions verbatim with correct refs.

Residual hallucinations found (both runs):
1. **False provenance of generated problems** — "All items are drawn from the
   textbook exercise set (REF-3)" attached to invented practice items; appeared
   in 2 cases per run. NOT caught by `no_invented_source_claims` (it targets
   solution/answer claims, not provenance claims) — candidate for the
   source-grounding audit lane or a further validator extension.
2. Sloppy maths in defusal prose (label run): "3 ÷ 12 … give whole-number
   results" (inverted), "90 = 8 + 12 + 15 + ...?"; (excerpt run): malformed
   numeral "0,840,000".
3. Loose method attribution (excerpt run): citing a definition excerpt for
   "the textbook's step-by-step method".
4. Base-content error surfaced (NOT a personaliser fault): the approved base
   claims 1,000,000 km ≈ Earth–Moon round trip ×3 (actually ≈1.3×) — flag for
   teacher review of the millions/billions base pack.

Dataset caveats: 8/15 cases are near-duplicate all-extend profiles from two
lessons (outputs nearly identical across cases) — effective diversity is ~6
distinct situations; retro-enriched evidence can mix submissions when a student
submitted the same lesson twice (Aisha case shows "2 of 2 correct" alongside
missed-item evidence). Production evidence recording (at grading time) does not
have this problem.
