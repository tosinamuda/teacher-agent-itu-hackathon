# Harness redesign — from patched loop to staged contracts

Every defect the blind rounds surfaced traces to one of four design retrofits.
This is the failure→cause map and the contracts that replace them.

## What actually failed, and why

| observed failure (round) | design cause |
|---|---|
| Repair corrupted her stopping rule ("touches point Q" → "touches the line", R4); repair stripped figure-anchor sentences (R5); repair mangled a correct definition (calibration) | **Patch-in-place with no acceptance test.** Repair is a blind text editor given quoted complaints; the only re-check is the same critic that flagged, so collateral edits ship. |
| 11-findings over-fire on one lesson (R5); findings that changed between runs on identical packs | **Critic has no precision guard.** Nothing verifies a finding's quote even exists in the learner view, and no cap decides when a section is "beyond patching". |
| Figures invisible (uncaptioned), reverse-ordered, dumped after answers, cited-but-absent, "picture above" with nothing above (R3-R5) | **Figures bolted on post-hoc.** The model composes text with no knowledge of where figures land; attachment is a post-processor fighting the composition. |
| Raters repeatedly spent deductions on phantom "Total column", "Example 2(b)" with no 2(a), "space provided", figures-after-answers | **The only quality signal is the expensive end-to-end rater.** Mechanically detectable defects reach the €€€ stage because there is no free lint stage. |
| DeepSeek arm: couldn't tell whether 11 findings meant bad generator or chatty critic without a rater round | **Modes are not isolated.** The model override is process-global, so the critic silently changes model with the generator; an arm is not an explicit tuple. |

## The contracts

1. **Stage artefacts, not one blob.** compose → attach → lint → critique → revise → final;
   every stage's output persisted per run. A score change then has a stage diff, not
   archaeology.
2. **Anchored figures.** The composer receives the figure manifest (labels + captions)
   and MUST place `[[fig-NN]]` anchors in its text. Attachment substitutes real figures
   at anchors. Lint fails on: manifest figure never anchored; anchor with no manifest
   figure; prose pointing at unlabelled pictures. This one contract kills the whole
   figure defect family.
3. **Lint before critique.** Deterministic checks, zero LLM cost, run on EVERY arm as
   metrics and on validated arms as gates: phantom figure references, register phrases
   ("the teacher", "the lesson note", "the source", "space provided"), example-label
   gaps (2(b) with no 2(a)), practice without answers, "above/below" pointers that
   point at nothing. Raters then judge only what needs judgment.
4. **Bounded revision, never blind patching.**
   - Critic findings are dropped unless their quote occurs verbatim in the learner view
     (precision filter — mechanical).
   - ≤3 findings per section → repair, then an ACCEPTANCE DIFF: only flagged spans may
     change; quoted phrases must be gone; lint must still pass. Fail → keep original.
   - >3 findings → the section is beyond patching: REGENERATE it with the findings as
     constraints instead of patching prose eleven times.
5. **An arm is an explicit tuple** `{generator_model, generator_impl, critic_model,
   repair_policy, effort}`, fingerprinted as named inputs. The critic is pinned to one
   reference model across arms so validation is a constant, not a covariate.
6. **One renderer.** `learner_view` is THE pack→text renderer, used by the critic, the
   rater packets, and (eventually) the app. Three renderers = three definitions of
   "what the learner sees" = unattributable diffs.

## Build order

1. critic precision filter + findings cap with regenerate-fallback  (kills repair damage)
2. lint module + per-run lint columns for every arm                  (kills rater waste)
3. figure anchors in the composition contract                        (kills figure family)
4. arm tuple with pinned critic model                                (kills confounds)
5. stage-artefact persistence + single renderer                      (kills archaeology)
