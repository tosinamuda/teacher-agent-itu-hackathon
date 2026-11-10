# OpenReview submission fields — GlobalSouthAI @ NeurIPS 2026

Venue: `NeurIPS.cc/2026/Workshop/GlobalSouthAI`
Portal: https://openreview.net/group?id=NeurIPS.cc/2026/Workshop/GlobalSouthAI
Deadline: **2026-09-07 17:59 UTC** (hard expiry 18:29 UTC). Review is **double-blind**;
the PDF is anonymised. Non-archival — FAQ Q3 explicitly permits work under review
elsewhere, so this does not foreclose Africa in AI @ NeurIPS 2026.

## title
Which Component Carries the Effect? Ablating an ITS-Inspired Generation Framework

## authors
DECISION NEEDED — supervisor inclusion. Every listed author must already have an
OpenReview profile before the form will accept the submission.

## keywords
AI for education; dataset development; data-centric AI; human-centered AI;
participatory AI; intelligent tutoring systems; LLM evaluation; inter-rater reliability;
LLM-as-judge; Nigeria; low-resource settings

## TLDR (optional, <=250 chars)
A component-additive ablation of an ITS-inspired generation framework on a Nigerian JSS1
prototype: the lesson model carries the whole class-level effect; expert grounding and
automated validation add nothing on top.

## abstract (<=5000 chars)
We use Design Science Research to design and evaluate a reusable framework for generating
curriculum-constrained learning material at class and learner level. Inspired by
Intelligent Tutoring System (ITS) component models, it separates a curriculum model, a
lesson model, an expert model and a learner model, and combines them through a
generation-and-validation process. We instantiate it on Nigerian junior-secondary (JSS1)
mathematics and add one component at a time. We are aware of no published
component-additive ablation of an educational LLM generation system; it lets us ask which
component carries the effect.

The framework's intended applicability is generic; the evidence below is specific to the
evaluated instantiation. Each rung adds one component: C0 curriculum model, objectives
only; C1 plus lesson model, the teacher's lesson plan and its instructional specification;
C2 plus expert model, scoped retrieval over her lesson note, the subject knowledge that
realises the plan; C3 plus a validation-and-repair agent, a processing component rather
than a further knowledge model. All rungs share one generator, artefact specification and
output contract, so a rung's effect is that component's effect and not a change of system.
A second part adds the learner model: P1 personalises frozen class-level material (P0)
from a pupil's marked script -- score, written solution steps, errors and diagnosed
misconceptions.

Nigerian JSS1 mathematics: forty pupils, one teacher, no slack to differentiate revision
material by hand. Six lessons x 4 conditions x 3 draws gives 72 packs over 17 objectives, at temperature 0
with caching disabled. The primary comparison is the lesson-plan-based family (C1-C3)
against the objectives-only baseline.

A blinded LLM judge, run twice independently, is repeat-stable (mean absolute movement
0.076; 92.4% of 288 scores identical). The family beats C0 by +0.338, positive in all six
lessons (Wilcoxon p=.031). The component diagnostics locate it: the lesson model carries
all of it -- C1-C0 = +0.368 (6/6 lessons, p=.031), while C2-C1 = -0.042 (2/6) and C3-C2 =
-0.007 (1/6). It shows sharpest as a floor: 8 of 18 C0 packs carry at least one judged
score below 4, against 0 of 18 at each of C1, C2 and C3. Component execution is verified
without a rater: source references on 168 C2 and 157 C3 blocks against none at C0 or C1,
51 retrieved evidence items at C2 and C3 against none at C0 or C1, and a validator that
logged 4.22 findings per pack but closed its repair loop on only 6 of 18.

Four practising mathematics teachers, blinded and counterbalanced (ANOVA on delivery
position F=0.01, p=.998), returned 1,199 of 1,224 scores. On them every contrast is null,
including the pre-registered C1-C0 = +0.044 (95% CI [-0.195,+0.283]). That panel could not
have resolved the contrast either way: rater identity carries 25.9% of score variance
against the packet's 14.6%, ICC(1,1) = -0.163, 91% of scores are a 4 or a 5, and the
minimum detectable effect (about 0.34) exceeds the largest present (0.152). We report both
instruments rather than the one that separates.

We contribute (i) a reusable ITS-inspired framework separating curriculum, lesson, expert
and learner models behind one generation-and-validation process, with the
component-additive ablation that makes each separately measurable; (ii) a prototype built
from artefacts a Nigerian school already produces, with corpus and blinded protocol; and
(iii) the observation that none of COGENT, FACET or LecturaAgents reports inter-rater
reliability or validates its LLM judge -- a property the field assumes. The learner-model
rung is instantiated and under evaluation.

## Two mandatory radio confirmations on the form
- author emails shared with Program Chairs
- accepted submissions, with author names, released publicly after the conference

## Also on the venue page — check before submitting
**Reciprocal review:** authors with prior papers accepted at relevant venues may be
required to nominate an eligible co-author as a reviewer (up to four reviews).
"Failure to fulfill this requirement may result in desk rejection."
Reviewer sign-up: https://forms.gle/GsdmHeGBqkP3tmZC7
