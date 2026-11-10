# Taking a prompt change to the frozen eval

The path from an edit to a defensible number. Follow it whole; the steps exist because
each one has been skipped before.

## 1. Make the change, and see it

```bash
uv run python -m scripts.prompt_snapshots
git diff tests/snapshots/prompts/
```

The diff is the change. If it touches arms you did not intend, stop here — that is the
finding, and it is free. `test_rendered_prompt_snapshots.py` fails until the snapshots are
regenerated, so this step cannot be skipped by accident.

Commit the snapshot diff **with** the change that caused it. A reviewer reads them together
or reads neither.

## 2. Run one candidate, not two

```bash
uv run python -m experiments.h1_condition_eval.runner \
    --label <what-changed> \
    --notes "one sentence: what this change is meant to move"
```

Defaults matter: `--generator packed` and `--signatures shared` are what production binds,
so a run left at defaults measures the served prompt. Naming the label after the change
rather than the date is what makes the log readable a month later.

Two changes in one run cannot be attributed. If you edited two things, run them separately.

## 3. Read the Comparison sheet against the floor

`experiment-log.xlsx` rebuilds its `Comparison` sheet from the two most recent labels.
Colour is only applied where a direction was actually measured:

| Metric | Scored? | Floor | Why |
| --- | --- | --- | --- |
| `recall` | yes | **0.094** | A regression screen on the prose, not a quality score — see below. Floor is the median same-condition movement across four runs on unchanged data; t3-w09 moved 0.182 |
| `inline_ref_markers` | yes | 0 | A blinding leak, not a score — one marker is one too many |
| `invention` | no | — | Shares recall's scale but its own spread was never measured, so it is not given a borrowed floor |
| `evidence_items`, `evidence_chars`, `chars`, `blocks` | no | — | These say what a run did, not whether it did better |

**Grey means inside the noise.** A recall delta of ±0.094 or less is run-to-run movement
and is not a result, however much it looks like one. Green and red are only painted outside
the floor.

`findings` is not in the sheet at all: it moved sd 2.03 on a mean of 1.53 across fifteen
identical draws, which makes it unusable for comparing anything. Read findings text
qualitatively instead.

### What recall is not

It is textual overlap with one document, and nothing else. It is a **regression screen**:
it catches a change that made the prose stop drawing on its source. It is not a measure of
quality, and it is not curriculum alignment.

Two limits to hold it to, both structural rather than statistical:

- **It scores the prose only.** `pack_text` collects section titles, block text and block
  captions — never `practice`. In the run H1a was judged on, the quantities living only in
  practice were 45.4% of C0's pack, 33.8% of C1's, 19.6% of C2's and 22.8% of C3's. The
  unmeasured share is arm-correlated, so an arm comparison on recall compares different
  fractions of the artefact.
- **It rewards copying.** A revision pack whose practice reuses the lesson's own numbers
  lets the learner recall an answer instead of running the method. Producing an isomorphic
  item instead — same objective, same procedure, new operands — lowers recall and raises
  invention at once, if practice were scored at all.

**Quality lives in the rating instrument, not here.** Curriculum alignment is
`objective_curriculum_alignment` in `H1_RUBRIC`; unsupported claims are `faithfulness` and
`support_sufficiency` in `SOURCE_AUDIT_CRITERIA`. Do not build a deterministic proxy for
either — a proxy that disagrees with the rubric is a second, unblinded instrument measuring
the same construct worse.

## 4. Know which arms your metric can speak for

This is the step most likely to produce a wrong conclusion.

**Recall and invention mean nothing for C0 and C1.** Both are scored against the teacher's
note, and neither arm ever receives it — so "the note's quantities that reach the pack" can
only measure coincidence. On t3-w05 a C1 pack scored 0.412 whose every match was a
one-digit number, while missing 48, 27, 75 and 7.5: the answers to all four worked
examples.

So:

- **A change touching C2/C3 only** — the Comparison sheet can carry the claim.
- **A change touching C0/C1** — recall is a dud screen and nothing more. A real comparison
  needs a rater, against the measured judge floor: a re-rate of identical prose moved more
  than half of every arm's scores by about 0.45, so a margin under 0.5 from one judge is
  not a finding.
- **A change touching every arm** — which both candidates in `CANDIDATE-CHANGES.md` do —
  needs both, and the deterministic half cannot stand in for the rated half.

## 5. Write down what happened, including nothing

Record the result in the story that made the change, whether or not it moved anything. A
cheap change that moved nothing is a finding about how much that part of the prompt is
worth, and it is only a finding if someone wrote it down.

## What this path does not do

It does not re-freeze the eval set, and it does not move the preregistered H1a endpoint. A
prompt change produces a new labelled run alongside the frozen record; it never edits it.
