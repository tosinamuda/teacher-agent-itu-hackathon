# The analyses as they were actually run

Verbatim copies of the scripts that produced the estimates in
`reproduction/reported_results.csv`, including the ones later withdrawn. They are kept
unchanged so a reader can reproduce a retracted number and see why it was retracted —
not tidied to reflect the current view.

| script | produces |
| --- | --- |
| `permutation_and_bootstrap.py` | P2-01 to P2-04: the four separated targets, the stratified learner bootstrap, and the exact permutation test |
| `agreement.py` | P2-07: weighted kappa and the rater-pair breakdown |
| `criterion_grid.py` | the fourteen-specification sensitivity grid (criterion subsets x scale coding) |

**These read the live Google Drive folder, not the exported CSVs.** They are evidence of
what was run, not a reproduction path. To re-derive the numbers from the bundle alone,
work from `part2/ratings_long.csv`; `validation_report.md` shows the aggregation route.

The mixed model behind P2-06 used `statsmodels.formula.api.mixedlm` with
`y ~ top`, `groups=student`, and variance components for lesson and rater, fitted REML
via lbfgs. It is recorded here rather than scripted because its inference method is not
defended — see the note on P2-06.
