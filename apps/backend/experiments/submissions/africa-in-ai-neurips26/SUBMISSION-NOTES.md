# Africa in AI @ NeurIPS 2026 — submission notes

**Deadline: 10 September 2026, 11:59 PM AoE** (= 11 Sep 11:59 UTC).
Format: 8 pages of content + up to 2 pages of references. This draft is 8 pages total,
with references beginning partway down page 8 — inside both limits.
**Double-blind**: names, affiliations, websites, funding sources and identifying
acknowledgements are all absent. Verified: no author, institution or repository string
appears in the extracted text; PDF Title/Author metadata are empty.

## Every number, and where it is verified

All re-derived from `experiments/human_rating/ratings/2026-09-07-ratings.xlsx` and the run
record at `experiments/h1_condition_eval/runs/c0c3-prism-objective/`.

| Claim in paper | Source |
| --- | --- |
| 72 packs, 6 lessons, 17 objectives, 3 draws | Generation record; H1 scores sheet |
| Source refs 168 (C2) / 157 (C3) / 0 / 0; 59.6%, 57.9% | Generation record |
| 51 evidence items at C2 and C3, 0 at C0/C1 | Generation record |
| Validation ran 18/18 C3; 4.22 findings mean; 6 passed | Generation record |
| Composite: family +0.338 (6/6, p=.031); C1−C0 +0.368 (6/6, p=.031) | Judge scores |
| Primary construct: family +0.750 (6/6, p=.031); C1−C0 +0.694 (5/6, p=.063) | Judge scores |
| Primary: C2−C1 +0.111 (3/6); C3−C2 −0.056 (0/6) | Judge scores |
| Flags by construct: fidelity 8/18, curriculum 1/18, correctness 1/18, clarity 0/18 | Judge scores |
| Failure floor 8/18 C0 vs 0/54 plan; Fisher p=3.7e−6; per-rung 8,0,0,0 | Judge scores |
| Judge repeat: movement 0.076; 92.4% of 288 identical; 0/288 identical prose | Judge scores |
| 1,199 of 1,224; missingness χ² p=.44; ANOVA on position F=0.01 p=.998 | H1 scores |
| C1 +0.044 [−0.195,+0.283]; C2 +0.098; C3 +0.152 [−0.086,+0.390] p=.209 | `reanalysis.py` |
| Variance: residual 38.9%, rater 25.9%, lesson 17.8%, packet 14.6% | `reanalysis.py` |
| ICC(1,1) = −0.163; 587 shared cells; 46.2% vs 46.6%; κ=0.048 [−0.027,+0.127] | H1 scores |
| 91% of scores are 4 or 5 (1,087/1,199) | H1 scores |
| MDE ≈ 0.34; largest effect 0.152 | Derived from mixed-model SEs |
| judge–human r = −0.033 | `reanalysis.py` |
| Redraw floor 0.479; displacement 8.5% (medians 6.9%); MW two-sided p=.018 | `blind_separability.py` |

**All p-values reported two-sided.**

**Analysis status.** The endpoint frozen 2026-07-26 was C1 vs C0 on the human panel, in an
internally recorded plan — *not* a public registration, so the paper says "prespecified",
never "pre-registered". The family contrast was adopted after judge scores had been
inspected and is reported as **exploratory**, as are the component diagnostics. Do not
restate it as confirmatory.

**The lexical overlap check is reported descriptively only.** Pairwise overlaps reuse the
same packs across comparisons, so the pairs are not independent and the earlier
Mann-Whitney p-value has been removed rather than reported under a violated assumption.

## Figures

- **Figure 1** (TikZ, in `paper.tex`): the framework — four knowledge models feeding one
  generation-and-validation process, with each rung labelled and the shared region marked.
- **Figure 2** (`results.pdf`): left panel, judge score at each rung with one grey line per
  lesson and the mean in black; right panel, the failure tail (8, 0, 0, 0 of 18). Generated
  by the script kept alongside these notes; the failure counts re-derive from the workbook
  on every run rather than being hard-coded.

## Deliberate scope decisions

- **H2 (workflow efficiency) and H3 (verification and trust) are excluded.** No timing,
  revision-count, verification-time, trust or acceptance instrument exists in the
  repository; `app/domains/evaluation/domain/study_instrument.py` defines three H1 and three H2 quality criteria and
  nothing else. Stated as out of scope in Limitations.
- **The learner-model rung (P1) reports no results.** Material is generated but rating is
  untouched (52/52). Stated in Instantiation and Limitations.
- **C2 is scoped retrieval over the teacher's lesson note**, not a textbook knowledge base.
  The docstring at `conditions/profiles.py` still says "textbook" and is stale — worth
  fixing in the repo.
- **"We are aware of no published component-additive ablation"** is stated as a knowledge
  claim, not a verified fact. If challenged, the supporting search must be reproducible.
- **The primary comparison (family vs C0) is not the pre-registered endpoint.** The
  2026-07-26 registration named C1 vs C0 as sole endpoint; the paper reports that one
  explicitly as pre-registered and null on the human panel.

## The worked example (Table 2) — provenance

Both unit_context strings are verbatim from `experiments/h1_condition_eval/wire/v3.json`,
the rendered prompt actually sent to the generator for lesson `t2-w09`, objective
`lo-t2w09-01`. The practice items are from `runs/c0c3-prism-objective/run.json`, draw 1.
C1's items are the teacher's own `student_tasks` reproduced verbatim; C0's are invented.
This is the prototype's real representation (`SectionGenerationUnit` plus the frozen
`ContextPolicy` gates), not the schema proposed in the March presentation.

## Open discrepancy: what the expert model retrieves

The March presentation shows the **Expert Model as the approved textbook** ("Curriculum
Linked RAG (Textbook)"), and `conditions/profiles.py` still describes C2 as "scoped
textbook grounding". But the code that generated the 72 packs retrieves over the
**teacher's lesson notes**: `source_workspace.py` materialises note files and exposes
`list_notes`/`read_note`, and `SOURCE-BOUNDARY.md` refers to "the note the model receives at
C2". The paper describes what ran (lesson-note retrieval). **Design intent and
implementation diverged here and the thesis needs to resolve which is correct**, because it
changes what the expert model means.

## Bug found in `reanalysis.py::missingness()` — fix before the thesis uses it

The function counts only *partial-criterion* gaps inside (rater, packet, objective) panels
that appear in the data at all. It cannot see a whole objective omitted from a returned
packet, nor a packet never returned. It reported 7 missing marks and chi-square p=.44; the
true figure is **25**, distributed 5/12/2/6 across C0-C3.

Verified decomposition: **19 marks** missing inside returned packets, plus **6** from one
packet never returned (rater-3, lesson `t3-w09`, C1, draw 1 — that lesson has 2 objectives
x 3 criteria). The paper now reports the counts and no test, because missing marks cluster
within packets and objectives.

## Ethics and data handling — MISSING, and only you can supply it

The paper has no ethics or data-handling statement. It uses school materials, four
practising-teacher raters, and the marked work of nine pupils who are minors. A reviewer
will look for: approval or exemption status and the granting body, permission to use the
school's materials, rater consent, and how identifiable pupil information was handled before
any external model processed it. **Do not let anyone draft this from assumption** — it has to
match the real record.

## No supplement exists — the paper no longer promises one

An earlier draft said prompts, rubrics and the model specification were "in the
supplementary material". There is no supplement. The mixed-model formula is now stated
inline, and the remaining artefacts are described as released with the code. **If you add an
appendix, check first whether Africa in AI counts it against the 8 content pages** — the call
says 8 pages of content plus up to 2 of references, and says nothing about appendices.

## The call, checked at source (2026-09-08)

Fetched from https://africainai.mailab.io/ . Verbatim: **"8 pages of content plus up to 2 pages
of references, submitted as a PDF."** Double-blind: "remove names, affiliations, websites,
funding sources and identifying acknowledgements". Original work only, "must not have appeared
in another venue, proceeding or journal". Eligibility: **"at least one researcher working or
studying in Africa"**. Deadline 10 Sep, 11:59 PM AoE; decisions 20 Sep. Submission through
OpenReview (`NeurIPS.cc/2026/Workshop/Africa_in_AI`); that page carries no further instructions.

**The call says nothing about appendices or supplementary material** — not permitted, not
forbidden. NeurIPS main-track convention allows an appendix after the references and the
workshop's "content + references" phrasing mirrors it, so an appendix after the references is
probably fine. That is inference, not a rule anyone stated.

## No appendix: 8 pages of content, 2 of references

Decided after checking the call at source. It permits 8 pages of content plus up to 2 of
references and says nothing about appendices, so the paper carries none rather than resting on
a convention nobody stated. The PDF is 10 pages: content ends on page 8, references run 9-10.

Table 1 (one objective traced through the prototype) is in section 4, in a two-row form: the
projection and the C1/C0 output contrast. A third row saying the task instruction is identical
across conditions was dropped, since section 3.2 already fixes Sigma, G and the output contract.
Its numbers come from `runs/c0c3-prism-objective/run.json` (lesson `t2-w09`, C0 and C1) and the
rendered request in `experiments/h1_condition_eval/wire/v3.json`.

Room for it came from four places, none of them evidence: the step representation is inlined
rather than displayed, the manipulation checks were described in section 5 and reported again
in 6.1 and are now only reported, and the cost paragraph, the conclusion's opening and the
criteria list are shorter.

An earlier draft carried an appendix of six exhibits (plan, target-material specification, note,
marked class work, generated pack, projection trace) built from
`Dataset/transcripts/t2-w09/` and the run record; it is in git history at `d67e5bba` and
`4c312e5f` if the material is ever wanted for the thesis.

## Gagné coding is deterministic, not annotation

`app/domains/artefacts/types/lesson_plan/drafting/domain/instructional_events.py` maps the
teacher's Presentation activity text to Gagné events by an ordered rule set: one code per
activity, weak evidence uncoded, consecutive duplicates collapsed, actor disambiguating verbs
that differ by who performs them. Five of the nine events occur; four are never inferred.
The paper states this, since a reviewer would otherwise assume LLM extraction.

## Before submitting

- [ ] Fill in the 11 placeholder references marked with bare years — titles and venues are
      from the thesis intro and several need full bibliographic details
- [ ] Confirm FACET's year (2025 in the thesis intro, 2026 in the related-work file)
- [ ] Decide authorship; confirm OpenReview profiles exist for all authors
- [ ] Re-read Table 1 claims against the three source papers before submission

## Text-overlap check (2026-09-08)

`check_overlap.py <dir> [N]` prints every run of N or more consecutive words shared between
`paper.pdf` (body only, references excluded) and each PDF in a directory. Re-run it after any
edit that adds prose.

Checked against 15 sources — the six comparators plus every reference obtainable without a
subscription (arXiv: Cho, Instructional Agents, DSPy, ReAct, Leinonen; open access: Ayanwale,
Zheng, Olaniyan, Li \& Zhang) — and against the thesis:

| corpus | runs >= 8 words |
| --- | --- |
| 15 cited/comparator papers | **0** |
| Chapter 2 literature review | 1 (9 words: "the subject matter and what counts as correct performance", the ITS domain-model definition taken from that chapter) |
| MSc dissertation | 0 |

At N=6 the only hits are "conference on neural information processing systems" — this template's
own footer, matched against other NeurIPS papers' footers. Not text reuse.

**What this does NOT cover.** Paywalled or offline references, roughly eighteen of thirty-seven:
Hevner, Peffers, Biggs, Bernacki, Nwana, Wenger, Gagne, Tomlinson, Yinger, Seo, Celik,
Nikolaidis, Dennison, Wang, Zhang, Sharma, Kasneci, Holstein, Moundridou, Ranawat, Jury, and the
three Nigerian journal articles (Ajayi, Ayo-Vaughan, Musingafi) with no reliable digital copy.
Those are exactly what an institutional Turnitin or iThenticate pass covers and this cannot.
Also not covered: Turnitin's stored student-paper repository.

If a Turnitin draft submission is possible, ask for a **no-repository** submission so the paper
is not stored and then matched against the thesis later.

## Part 2 (H2) is now rated — every number re-derived (2026-09-09)

Source: `~/Downloads/part2_analysis_handoff_v3.zip` -> `handoff3/part2/ratings_long.csv`,
`objective_generation_audit.csv`, `learners.csv`. Re-derived here, not copied from the handoff's
own report.

| Claim in paper | Re-derived value |
| --- | --- |
| 26 cases, 9 pupils, 3 lessons, 35 panels, 2 raters each | 26 / 9 / 3 / 35 / 70 rater-panels |
| 199 of 210 assigned criterion cells answered | 210 assigned, 199 answered, 11 blank (all rater-4) |
| P1 changed exactly the 35 objectives it held state for | audit: (state_present, changed)=35, (state_absent, unchanged)=34 |
| P1 - P0 = +0.045 | equal weight per pupil over the collapsed +1/0/-1 coding: +0.0453 |
| interval [-0.106, +0.199] | my own stratified cluster bootstrap, 20000 reps, seed 20260908, resampling the 9 pupils within reconstructed attainment thirds. The handoff reports [-0.108, +0.198] from the same design; the small difference is Monte Carlo noise |
| P1 chosen 38/67, 25/67, 20/65 | adaptive_calibration 38 P1 / 22 P0 / 7 neither; learner_evidence 25/24/18; instructional_integrity 20/25/20 |
| opposite winners 11 of 32 | adaptive_calibration: 32 doubly rated, 11 opposite-sign |

**What the bootstrap does and does not model.** It resamples pupils within attainment thirds.
Lessons (3) and raters (4) are crossed with pupils and are NOT modelled. The interval therefore
describes pupil-level sampling variability only. The paper names the resampling unit for that
reason.

**A correction inherited from the handoff, worth knowing.** An earlier export read each panel's
objective from its ordinal rather than its printed heading; 108 of 210 rows carried the wrong
objective id, which had produced a claim that 108 cells concerned objectives with no learner
evidence. Corrected: every objective shown had learner state. The paper never carried the wrong
version.

**Attainment strata are reconstructed.** `learners.csv` records
`group_recorded_at_sampling: no` and `original_sampling_stratum: unknown` — sampling was
stratified over the teacher's ability categories, but those categories were not recorded, and
the top/middle/lower thirds in the data are reconstructed post hoc from the marks. Section 5 now
says the categories were not recorded, and the paper reports no stratum-level result.

## NOT adopted from the 2026-09-09 review, and why

- **The H1 packet-bootstrap figures** (family +0.180 [-0.009,+0.378]; C3-C0 +0.283
  [+0.051,+0.514]) and the mixed-model p=.027. Nothing on this machine reproduces them, and they
  would turn the paper's reported null into a significant result. Section 6.3 still reports the
  crossed mixed model that was re-derived from the workbook. Adopting them needs the analysis
  script and a check that the resampling preserves the lesson pairing and the crossed raters.
- **The three-RQ / four-claim / EP table structure.** Thesis scaffolding. The paper is narrated,
  and an earlier instruction was explicitly against sectioned hypothesis/claim headings.

## Section 6.3 rebuilt on the focal criterion (2026-09-09)

Re-derived from `experiments/human_rating/ratings/2026-09-07-ratings.xlsx`, sheet `H1 scores`
(1,199 scored rows, 72 packets), collapsing the `-c\d` copy suffix, taking one mean per pack,
then one difference per lesson. Criterion 2 is lesson-specification fidelity — the construct the
protocol already names as primary and as the operationalisation of H1.

| contrast | mean | lessons +ve | negative lessons | exact signed-rank | lesson bootstrap |
| --- | ---: | ---: | ---: | ---: | --- |
| C1 - C0 | +0.049 | 3/6 | 3 | p = 1.000 | [-0.177, +0.301] |
| C2 - C0 | +0.190 | 4/6 | 2 | p = .1562 | [-0.051, +0.419] |
| C3 - C0 | +0.281 | 5/6 | 0 | p = .0625 | [+0.140, +0.403] |
| family - C0 | +0.174 | 4/6 | 2 | p = .1562 | [-0.022, +0.350] |

Per-lesson C3-C0: [+0.444, +0.267, +0.139, +0.417, +0.422, 0.000].

Ceiling check, share of scores at 4-5: criterion 1 is 90.1 / 91.8 / 92.1 / 94.0 across C0-C3 —
near ceiling in every condition, which is why the three-criterion composite dilutes. Criterion 2
moves 81.0 -> 92.1.

**The bootstrap interval on C3 is not a test, and the paper says so.** All six lesson
differences are >= 0, so every resample has a non-negative mean and the lower bound could not
have been negative. This is the same artefact the Part 2 handoff withdrew under P2-04. The
distribution-free floor with six lessons and one tie is p = .0625, which is where C3 lands, and
that is the inferential statement the paper makes.

`alignment_contrast.py` on `tosin/part2-analysis-handoff` implements the same estimator and
agrees to ~0.01 on every contrast, but **run against this worktree's
`experiments/human_rating/delivered/` it reports 53 packets and 498 ratings and different
numbers** — that folder holds only part of the returned work. The workbook is the source of
record; anything computed from `delivered/` here should be checked against it first.

Consequential corrections this forced elsewhere: the first limitation said every positive
finding came from the judge, which is no longer true, and the abstract and conclusion said the
human comparison established no advantage.

## Revision-map review, and what was taken from it (2026-09-09)

Sources read: `~/Downloads/lesson_plan_paper/revision-map/REVISION_MAP.md`, the aggregate export
`private_inputs/part1_absolute_quality.txt` and `data/*.csv`, plus `Result/Paper.md` and
`Result/Contribution.md` in the Obsidian vault.

**Part 1 coverage was wrong in the paper and is corrected.** The workbook
`2026-09-07-ratings.xlsx` holds **1,199** scored rows; the aggregate export totals **1,212** over
the same twelve condition-by-criterion cells. Recomputed cell by cell, the whole difference is
13 late ratings: C1 gains 3 on each criterion and C3 gains 1, 1 and 2. C0 and C2 are identical.
The paper now says 1,212 of 1,224.

Consequence, stated in the paper: the per-lesson paired contrast is still computed on the 1,199
rows, because **no row-level export of the 1,212 exists here** — `part1_absolute_quality.txt` is
an aggregate with by-condition, by-lesson, by-rater and paired-section breakdowns but no
lesson-by-condition cells. If the row-level 1,212 export appears, rerun the contrast; the level
means move by at most 0.01 (C1 4.316 -> 4.34, C3 4.574 -> 4.58).

**Adopted from the revision map / Contribution.md**

- Part 1 count 1,212 of 1,224.
- Absolute usefulness, which the paper lacked entirely: C3 has 95 of 101 instructional-quality
  ratings at 4-5, both raters favourable on 44 of 50 doubly rated sections; C0 93 of 100.
- Lesson-context levels: means 4.26 / 4.34 / 4.53 / 4.58, favourable 81.0% -> 92.2%, both-raters-
  favourable sections 33/49 -> 44/51, either-rater-at-2-or-below 5 / 2 / 1 / 0. All from
  `part1_counts.csv` and `part1_paired.csv`, which trace to the aggregate export.
- The three-contribution list, replacing four bullets. In particular "isolating each input's
  contribution" was an overclaim - no single rung is separately established - and is now
  "comparing cumulative configurations". The four-rater-panel bullet leaves the headline list;
  the reliability result stays in section 6.
- Replacing "the panel agrees at chance" with the weak-pooled-agreement wording, now that the
  paired-section progression is reported.

**Not adopted**

- The packet-bootstrap contrasts. `data/part1_reported_bootstrap_not_reproduced.csv` marks all
  six "Not independently reproduced; lesson/rater resampling and multiplicity unresolved" - the
  revision map's own verification agrees with the decision already recorded above.
- The RQ/EP table structure and the 13-page reconstruction: the reconstruction is not the NeurIPS
  template and this paper is 8 pages by the call.

## The row-level 1,212 export exists — point the tools at Google Drive

`experiments/human_rating/delivered/` in the repo is a **partial** copy: the exporter reads 53
packets and 498 ratings from it and produces wrong contrasts. The returned rater work lives at

    ~/Library/CloudStorage/GoogleDrive-<account>/My Drive/Revision Material Evaluation

with `Part 1 - Class revision material/Rater 1..4` (37 files each) and the Part 2 equivalent.
Run against that folder the exporter reads **72 packets and 1,212 ratings**, and the paper's
figures are computed from it:

    uv run python -m experiments.human_rating.alignment_contrast \
      "$HOME/Library/CloudStorage/GoogleDrive-.../My Drive/Revision Material Evaluation"

Criterion 2, lesson-paired, on all 1,212:

| contrast | mean | lessons +ve | negative lessons | exact signed-rank |
| --- | ---: | ---: | ---: | ---: |
| C1 - C0 | +0.068 | 3/6 | 3 | p = .8438 |
| C2 - C0 | +0.190 | 4/6 | 2 | p = .1562 |
| C3 - C0 | +0.283 | 5/6 | 0 | p = .0625 |
| family - C0 | +0.180 | 4/6 | 2 | p = .1562 |

Per-lesson C3-C0: [+0.444, +0.267, +0.139, +0.417, +0.433, 0.000]. These reproduce the
investigator-supplied table exactly. The earlier values in this file (+0.049, +0.281, +0.174)
were computed on the 1,199-row workbook and are superseded.

The bootstrap point is unchanged: C3 still has no negative lesson, so a lesson-cluster interval
could not have contained zero, and the paper reports the signed-rank floor instead.

**Nothing in the paper now rests on the 1,199 export.**
