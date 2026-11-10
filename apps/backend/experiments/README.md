# Experiments

The research harnesses of the Plan-to-Tutor study. Run each one from `apps/backend`, with the command in its module docstring.

| Package | Harness |
| --- | --- |
| `content_repair` | A `dspy.ReAct` agent that repairs lesson-step content, scored by a separate deterministic gate |
| `dataset_export` | Builds the four LPCG datasets for publication |
| `h1_condition_eval` | Runs C0 to C3 over the frozen lesson set: the study's Part 1 |
| `h2_personalisation_eval` | Runs P0 and P1 for each transcribed learner: the study's Part 2 |
| `human_rating` | Builds the evaluation set that each human rater gets |
| `lesson_note_engine` | Compares the lesson note's own generator with the content engine over a frozen lesson set, blinded for review |
| `p1_cot_v2_rules` | A `ChainOfThought` arm with the ReAct-v2 rules and no tool |
| `p1_evidence_prompt` | Compares the distilled learner-state card with an evidence-rich P1 input |
| `p1_prompt_eval` | Evaluates P1 prompt versions over a frozen set, one versioned run each |
| `p1_react_personaliser` | A `dspy.ReAct` personaliser that must read a source before it cites it |
| `sequencing_bakeoff` | Compares four ways to order source assets and LLM prose |
| `source_transclusion` | Compares a regenerated source table with a verbatim splice |
| `strategy_bakeoff` | Compares lesson-plan generation strategies under a pre-registered protocol |
| `study_import` | Imports the published study into the app as a concluded, read-only study |

`submissions/` holds two workshop papers.
[`run_folders.py`](run_folders.py) names the run folders.

## Runs

- Each run writes its own folder under `<package>/runs/`, named `<label>-<UTC start>`, for example `pre-20260925T183005Z`.
- `--resume <folder>` continues an interrupted run in its folder.
- DVC versions the run folders of `h1_condition_eval`, `h2_personalisation_eval` and `p1_prompt_eval`, and `runs/.gitignore` keeps them out of git.
- Git holds one `<folder>.dvc` pointer for each run, which names the exact files in the DVC remote.
- Two study runs stay in git, because the tests and the dataset export read them:
  `h1_condition_eval/runs/c0c3-prism-objective` and `h2_personalisation_eval/runs/h2-deepseek-clean`.

### Set up a checkout

The remote and the cache are per machine, in `.dvc/config.local` at the repository root.
The remote is a folder in the private study data, which Google Drive syncs.

```bash
# From apps/backend
uv run dvc remote add -d --local thesis "$HOME/Documents/Unilag/Masters/Thesis/Dataset/private/experiment-runs"
uv run dvc cache dir --local "$HOME/.cache/dvc/plan-to-tutor"   # one cache for every checkout and worktree
uv run dvc status -q                                          # no output and exit 0: each run matches its pointer
```

### Keep a run

Check an H2 run against the five checks in [`apps/backend/.gitignore`](../.gitignore) first.

```bash
# From apps/backend
uv run dvc add experiments/h1_condition_eval/runs/<folder>
uv run dvc push
git add experiments/h1_condition_eval/runs/<folder>.dvc
```

### Get a run back

```bash
# From apps/backend
uv run dvc pull experiments/<package>/runs/<folder>.dvc
```

After `dvc push`, you can delete the local files of a run and pull them again later.
