# P1 prompt-version evaluation harness

The standing rule for ANY change to the personalisation prompt — the
signature docstring, LM-facing field names, or the mapper's value rendering:
**no prompt change ships on vibes.** Freeze a dataset, run both versions,
compare blinded, judge manually, then decide.

## The loop

```bash
cd apps/backend

# 1. Freeze the dataset (once; re-freeze deliberately, never implicitly).
#    One case per focal case with an approved/succeeded base: base sections,
#    session plan, and the learner's domain state rebuilt from their real
#    diagnostic, enriched with missed-item answer evidence.
uv run python -m experiments.p1_prompt_eval.dataset

# 2. Baseline run of the CURRENT production prompt. The label is a hash of
#    the signature's instruction block — git is the version history, the
#    hash is the id; two different prompts can never share a label.
uv run python -m experiments.p1_prompt_eval.runner

# 3. Author the CANDIDATE prompt under experiments/ (same input/output
#    fields as SectionPersonalisation) and run it:
uv run python -m experiments.p1_prompt_eval.runner \
  --variant experiments.my_prompt_idea.signature:PersonaliseV3

# 4. Blinded side-by-side for manual judgement (Candidate A/B per case,
#    de-blinding map only in key.json — judge first, then open the key).
uv run python -m experiments.p1_prompt_eval.compare <production-label> <candidate-label>

# 5. If the candidate wins: promote it into the production signature in one
#    commit. Condition runs record the prompt fingerprint automatically.
```

Each run exercises the REAL production path (request builder → learner-state
mapper → personaliser → validator + repair) and captures the rendered prompts,
so `runs/<label>/run.json` is a complete provenance record. `runs/<label>/cases/`
holds one readable markdown per case (learner state as the model saw it, base
vs personalised per objective, validation outcome).

## Judging guide (manual)

Per case, per objective, ask in order:
1. **Objective preserved** — same thing taught, scope unchanged?
2. **Misconception targeting** — does it defuse the learner's ACTUAL chosen
   distractors ("a common slip…"), or re-teach generically / chase a label?
3. **Support calibration** — depth/hints/practice match the band + the
   learner's own survey answers?
4. **Tone** — gentle, impersonal (never "you chose…"), suited to the session
   signals?
5. **Grounding honesty** — no invented source claims, refs only where content
   is actually drawn from evidence.

Record A/B/tie + a sentence in the markdown, then de-blind with `key.json`.

## Provenance

- Dataset frozen from the dev DB focal cases (dress rehearsal + earlier test
  experiments). Session surveys are included only where the learner answered
  one for that lesson — no borrowed signals.
- Agent-judged precursor (one case, evidence-rich vs distilled-card):
  `experiments/p1_evidence_prompt/REPORT.md`.
