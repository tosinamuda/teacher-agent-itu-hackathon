# Runs

The run folders of `h1_condition_eval`, one for each run, and the reports on them.
[`MANIFEST.md`](MANIFEST.md) sorts every run into tiers.

## Folders

- A new run writes `<label>-<UTC start>`, for example `pre-20260925T183005Z` ([`run_folders.py`](../../run_folders.py)).
- `--resume <folder>` is the only way that a run writes into a folder that exists.
- The code finds a run at `RUNS_DIR / <folder>` ([`config.py`](../config.py)).
- `metrics.py` scores every `*/run.json` on disk, and the dataset export takes every file that git holds here.
- DVC versions each folder, and git holds its `<folder>.dvc` pointer ([Runs](../../README.md#runs)).
- `c0c3-prism-objective`, the study's Part 1 run, stays in git, because the tests and the dataset export read it.

## A label is not a draw

Generation is stochastic at temperature 0, the default in `config.py`.
`c0c3-worksheet-2026-08-11T1538` and `c0c3-worksheet-2026-08-11T1603` are two runs of `c0c3-worksheet` with one fingerprint.
58 of their 72 rating packets differ.
The three `c0c3-worksheet` folders share one `run.json`, so read each draw from its `rating/packets/`.
The packets of `c0c3-worksheet` match those of `…T1538`.

## What a run holds

```
<folder>/
├── run.json            # the run record and the generated documents
├── fingerprint.json    # a hash of each input, to compare runs
├── traces.jsonl        # the LLM calls
├── inputs/             # the prompts that each condition sends (inputs.py)
└── rating/
    ├── packets/        # the blinded candidates for the judge
    ├── worksheets/     # each packet as a PDF
    ├── _key.json       # candidate id to condition
    ├── judgments.json  # the judge's scores
    └── RATING-RESULTS.md
```

Git and DVC both ignore these paths, so they stay on the local machine:

| Path | Why |
| --- | --- |
| `workspace/`, `sessions/` | Agent scratch that the harness arm writes again on each run |
| `prompt-response-pairs/` | `uv run python -m scripts.prompt_snapshots.pairing <label>` writes it again from `run.json` |
| `blind-separability.json` | The output of `blind_separability.py` |
