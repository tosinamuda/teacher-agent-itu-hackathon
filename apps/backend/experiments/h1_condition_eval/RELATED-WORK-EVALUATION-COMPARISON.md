# How the comparable systems were evaluated

Three published systems generate educational content from an LLM and evaluate it with
expert raters. This records how each did it, against how this study did, because the
comparison is the clearest statement of where this study's measurement work sits.

Compiled 2026-09-07 by reading each paper. Claims marked **(verifiable)** can be checked
by anyone against the published text — a venue, or the absence of a reliability
statistic. Claims marked **(reading)** are an interpretation of the paper and should be
re-checked before being cited.

## The three systems

| | COGENT | FACET | LectūraAgents |
| --- | --- | --- | --- |
| Citation | Liu, Yin, Goh & Chen (2025) | Gonnermann-Müller, Haase, Fackeldey & Pokutta (2026) | Sesay, Yu, Dong & Karlsson (2026) |
| Where | BEA 2025 workshop at ACL, peer-reviewed | arXiv:2508.11401, preprint, 5 versions, no venue | arXiv:2606.16428, preprint, Comments field reads "LecturaAgents TR" |
| Artefact | science reading passages, grades 1–5 | one-page worksheet | whole lecture package with embodied teaching actions |
| Curriculum input | NGSS concept → core ideas → outcomes | one seed word problem | none — generates its own syllabus |
| Teacher's lesson plan | no | no | no |
| Learner input | none | simulated: two binary traits | a free-text self-description |

## How each was evaluated

| | COGENT | FACET | LectūraAgents | This study |
| --- | --- | --- | --- | --- |
| Human raters | 6 | 5 | 5 | 4 |
| Ratings collected | ~450 (inferred; never stated) | ~80 | not reported | 1,199 |
| Artefacts rated by humans | 15 | 4 | 20 per comparison | 72 |
| Blinding | not reported | not reported | not reported | enforced |
| Order counterbalanced | not reported | not reported | not reported | verified, F = 0.00 |
| **Inter-rater reliability** | **none reported** | **none reported** | **none, and not computable — one rater per item** | κ = 0.05, CI [−0.03, 0.13] |
| LLM judge | Claude 3.5 Sonnet | GPT-4o | GPT-5.2, Stage 1 of 2 | Claude Sonnet 4.6 |
| Judge validated against humans | one sentence, no numbers | no | no | two independent passes, 92.4% repeat |
| Judge distinct from generator | **no — also one of the three generators** | n/a | GPT-5.2 judging GPT-5.1 among others | refused in code |
| Statistical test | Mann-Whitney, Bonferroni | **none** | **none** | crossed mixed model, Wilcoxon, Fisher |
| Clustering handled | no | no | no | yes |
| Pre-registration | no | no | no | yes, 2026-07-26 |
| Learner outcome | no | no | 45 students, no pre-test, no retention | no |

**(verifiable)** None of the three reports an inter-rater reliability statistic. None
validates its LLM judge against its humans. Two report no statistical test of any kind.

## What this study does that they do not

**Real teacher artefacts as input.** COGENT sends curriculum standards. FACET sends one
seed problem. LectūraAgents writes its own syllabus. This study sends the lesson plan a
practising teacher wrote for a lesson she taught, and the note she taught it from.

**Real learner evidence.** FACET's learner is simulated from two binary traits.
LectūraAgents takes a typed self-description. COGENT has no learner. This study reads a
child's marked class work.

**One variable at a time.** COGENT's headline contrast changes three things at once — it
injects the curriculum text, adds a readability instruction its baseline never receives,
and adds objective-directed framing, with no ablation separating them **(reading)**. The
C0→C1 contrast here changes the input context and nothing else: same generator, same
loop, same repair pass, same artefact spec, same output contract.

**A measured instrument.** The reliability of the human panel and the repeat-stability of
the judge are both quantities this study reports and none of the three does.

## Why the null matters more read against these

The finding here is that four practising teachers, rating on a 1–5 scale, agree at
chance, and that the design's smallest detectable effect (0.34) exceeds the largest
difference present (0.145). If that generalises, the positive results in these three
papers rest on instruments with the same problem, unmeasured: six teachers on fifteen
passages, five on four worksheets, five each rating different lectures alone.

That is the contribution to state plainly. Not "we failed to find an effect" but "we
measured what this instrument can resolve, and the field has been assuming it".

## A trap to avoid, learned from LectūraAgents

Its head-to-head table scores Instructional Agents on personalisation while its own
capability table marks that system as not having personalisation; it compares against
Learn Your Way using samples scraped from a website with one-line learner profiles
against its own multi-sentence ones; its stated N of 20 does not match the 19 and 17
lectures its appendix lists; and its released dataset contains the generated artefacts
but no scores, no rubric judgements and no baseline outputs, so none of it can be checked
**(reading)**.

Every one of those follows from benchmarking other people's systems on a rubric you wrote
yourself. If this study ever compares against an external system, the rubric has to be
one the comparison does not own.

## Sources

- COGENT — https://aclanthology.org/2025.bea-1.10/ · arXiv:2506.09367
- FACET — https://arxiv.org/abs/2508.11401
- LectūraAgents — https://arxiv.org/abs/2606.16428
