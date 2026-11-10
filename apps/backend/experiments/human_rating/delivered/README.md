# Delivered

The copy of the raters' Drive folder: the instrument they were actually given, one
document per assignment per rater, in delivery order. The `.docx` files are not committed:
`scripts/fetch_datasets.py` fetches them from the ratings dataset on the Hub at the revision
`dataset/datasets.lock.json` pins, and checks every file's SHA-256.

## Which builds these are

Each part went to the raters' Drive once and was not reissued, so each comes from its own
build. The documents' own properties (`docProps/core.xml`, `created`) date them:

| part | documents | written | build |
| --- | --- | --- | --- |
| Part 1 | 148 (144 rating documents, 4 instruction sheets) | 2026-09-02 10:17:55 to 10:19:47 UTC | right after `4876ac81` (10:17:15 UTC); its build record is not in the repository |
| Part 2 | 56 (52 rating documents, 4 instruction sheets) | 2026-09-04 05:09:06 to 05:11:14 UTC | `build.json` beside this file, commit `3efd361c`, copied out of `builds/2026-09-04T050905Z/` (gitignored, regenerable); the 52 are byte-identical to it |

So `build.json` describes Part 2's build only. The Part 1 build predates `4dcb8290`, which
turns the HTML a model wrote into markdown; the packs' HTML reached Part 1's raters rendered
as formatting through markdown, HTML and docx, and none of the 144 documents shows a tag.

## The runs the study reports

| | run | model |
| --- | --- | --- |
| Part 1, the condition ladder | `c0c3-prism-objective` | `openai/deepseek-v4-flash` |
| Part 2, personalisation | `h2-deepseek-clean` | `openai/deepseek-v4-flash` |

Part 2's base is `c0c3-prism-objective` **C3, repeat 1** — the automatically validated
pack and its first draw, not a teacher-approved one, because the approval gate was not
exercised. The rest of the Part 1 arm is in `build.json`: `compose-v2` over DSPy 3.3.0,
`ComposeSection` under a `ReActV2` loop, `rewrite` repair, `leveled` signatures, the
corrected notes, source figures, context variant `v7-full`.

`c0c3-prism-objective` is the only Part 1 run any of this rests on. The other labels under
`h1_condition_eval/runs/` are development and bake-off runs, and one of them,
`c0c3-worksheet`, was drawn three times under one fingerprint — see that directory's
README before reading any of them as the study's data.

## What this snapshot holds

Both parts as the raters returned them, taken from Drive on 2026-09-13 (`0517aced`). Part 1
yields all 1,212 scores; Part 2 yields 199 comparisons, with 11 of its 210 cells left blank.
