# P1 prompt-evidence experiment — v1 (state card) vs v2 (evidence-rich)

**Date:** 2026-06-11 · **Case:** real dress-rehearsal focal case
`EFC-caa170f9905345e1aff3cb06d0e3a658` (JSS1-ngozi-f738, lesson "LCM of whole
numbers", approved C4 base, 2 sections) · **Model:** same for both arms
(`CONFIG.dspy_model`) · **Artifacts:** `out/run-20260611T051254Z.json`
(paired outputs + captured rendered prompts), `out/assess-v1.json`,
`out/assess-v2.json`, `out/compare-blinded.json` + `out/compare-key.json`.

## Arms

| | learner-state input to the personalisation LM |
|---|---|
| **v1 (production today)** | distilled card: band, mastery float, **bucketed** confidence/difficulty (low/med/high), modal misconception **code** (`missing_factor_of_two`), no evidence items, no session signals |
| **v2 (learner-model spec §"internal LLM input")** | card **plus**: per-item answer evidence (question, options, correct option, the learner's chosen distractor, its humanised rationale), canonical 1-5 confidence/difficulty, misconception in plain words, session signals (interest 4/5, end-of-lesson feeling 2/5) with tone/depth rules |

Method: 1 assessor agent per arm (scored against the learner's TRUE needs,
blind to the other arm), then a third comparer agent judging label-shuffled
pairs (Output-X/Y per section, key withheld).

## Result — v2 wins both sections

| objective | band | blinded winner | margin |
|---|---|---|---|
| lop01 (identify common multiples) | remediate, mastery 0.0 | **v2** | **decisive** |
| lop02 (find the LCM) | extend, mastery 1.0 | **v2** | clear |

**lop01 (the case personalisation exists for):** v1 scored 2/5 on
misconception targeting — it *keyword-matched the label* ("missing factor of
two") into mathematically muddled "factor 2" patter the judge said "could
deepen a confused student's confusion", and never addressed why the learner's
actual choices (9 for {2,3}; 16 for {4,6}) were tempting. v2 scored 5/5: it
reused both missed items, defused each chosen distractor, and taught the
transferable check ("divisible by EACH original number"). The blinded judge
reproduced this diagnosis without knowing the arms.

**lop02 (control: no evidence items, signals only):** v2 still preferred —
kept the approved base intact, added a genuinely unsolved challenge problem,
and its reflection spoke to the learner's confidence; v1 printed full
solutions inside its "practice" blocks, leaving nothing to solve.

## Risks found in v2 (must-fix in any production port)

1. **Provenance hallucination on net-new content:** v2's new lop02 blocks
   self-cited REF-2/REF-3 and claimed the textbook contains solutions to
   *generated* problems. The objective-preservation/source-ref validator +
   repair loop must explicitly cover net-new blocks, and the policy text needs
   "never claim a generated problem or its solution exists in the source".
2. **Echoing raw test data to the student:** one phrase ("the number 16 that
   was chosen earlier") points at the learner's own wrong answer. Audience
   rule for the signature: misconceptions are addressed as "a common slip is
   …", never "you chose …".

> **PORTED TO PRODUCTION 2026-06-11** (same day, user decision): the v2 shape
> now lives in the real request schema (`requests.ObjectiveLearnerState` +
> `SessionSignals`), `SectionPersonalisation` carries the
> audience rule ("a common slip is …", never "you chose …") and the provenance
> rule, and the new deterministic `no_invented_source_claims` check gates P1
> (with repair). `PROMPT_VERSION = "study_pack_v2"`. This runner's "v1 arm"
> therefore now exercises the ported production path, not the pre-port card.

## Recommendation

Adopt the v2 evidence shape for the production P1 request
(`ObjectiveLearnerState` + evidence items + 1-5 scores + humanised
misconception + session signals), with the two mitigations above baked into
the signature instructions and validator. Port via the real request schema +
`SectionPersonalisation` (LM-facing aliases at the boundary),
not by importing from this experiment package. n=1 focal case — before
adopting for the 12-lesson run, replay 2-3 more focal cases (one per band)
with the same harness.

Re-run: `uv run python -m experiments.p1_evidence_prompt.runner`
