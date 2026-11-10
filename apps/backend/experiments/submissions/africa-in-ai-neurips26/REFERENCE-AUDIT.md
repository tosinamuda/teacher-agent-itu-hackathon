# Reference audit — checked against your own `references.bib` and against source records

Sources: `~/Documents/Unilag/Masters/Thesis/Chapter 2/references.bib` (171 entries), plus
publisher/repository records. Checked 2026-09-08.

## The headline problem, now fixed

**Ten references in the paper did not exist in your bibliography.** They came from the
Chapter 1 draft with author and year only, and the titles in the paper were paraphrases I had
written. Verification showed how badly that fails: `cho2024` was cited as "A review of
artificial intelligence in education: toward end-to-end classroom-usable systems". The real
paper is **"A Systematic Review of Knowledge Tracing and Large Language Models in Education"**
(Yongwan Cho, Rabia AlMamlook, Tasnim Gharaibeh, arXiv:2412.09248) — a different subject.

Every fabricated entry has been replaced with a real one from your bibliography:

| Removed (did not exist) | Replaced with |
| --- | --- |
| `nketsia2025`, `karner2021`, `bach2025` | `musingafi2015` (curriculum → syllabus → scheme → plan), `ajayi2015` and `ayovaughan2022` (Nigerian lesson preparation and plan-format use) |
| `joshi2025`, `oner2025`, `kim2025` | `leinonen2023` (LLM code explanations), `jury2024` (LLM worked examples), `li2024` (controllable question generation) |
| `luna2026` | `moundridou2024`, `sharma2025` |
| `cevikbas2024` | `biggs1996` retained; `celik2026` added |
| `zheng2023` | citation dropped — the sentence describes our implementation |

## A whole line of related work was missing

Your bibliography contains **seven systems that generate lesson plans**, none of which the
paper cited: `ranawat2021` (CollectiveTeach), `moundridou2024`, `olaniyan2025`, `zhang2025`
(EduPlanner), `zheng2025`, `celik2026`, and `dennison2026` (Shiksha Copilot — teacher–AI
collaboration on lesson plans **in low-resource schools**, the closest work to this setting).

A reviewer who knows this literature would have rejected the paper's framing outright. Related
work now has two lines, and the novelty claim is stated precisely and more strongly: **those
systems produce a lesson plan as output; we consume an existing one as input.**

## Corrected from source records (6)

| Key | Was | Is |
| --- | --- | --- |
| `li2026` | X. Li, 2026 | **Z.** Li et al., "Customizing Learning Recommendations with Knowledge Tracing and RAG", INTERACT **2025** |
| `wang2025` | S. Wang, "GenMentor: …" | **T.** Wang et al., **"LLM-powered Multi-agent Framework for Goal-oriented Learning in ITS"**, WWW 2025, pp. 510–519 |
| `zhao2025` | L. Zhao | **R.** Zhao et al., EMNLP 2025 Demos, arXiv:2507.04295 |
| `dspy` | 3 authors | 13 authors (matches your `khattab2023`) |
| `react` | 3 authors | Yao, Zhao, Yu, Du, Shafran, Narasimhan, Cao |
| `hevner2004` | 75–105 | **75–106**, per MIS Quarterly |

## Verified exact (8)

Biggs 1996 (Higher Education 32(3):347–364) · Nwana 1990 (AI Review 4(4):251–277) ·
Yinger 1980 (Elementary School Journal 80(3):107–127) · Kasneci 2023 (Learning and Individual
Differences 103:102274) · Peffers 2007 (JMIS 24(3):45–77) · COGENT (BEA 2025, pp. 129–143) ·
FACET (arXiv:2508.11401) · LectūraAgents (arXiv:2606.16428).

## Citation practice

- **Nine references were never cited in the body** — Hevner, Peffers, Nwana, Biggs, Yinger,
  Kasneci, Cho, Cevikbas, Luna Chontal. The design science framing had disappeared from the
  text entirely while Hevner and Peffers sat in the bibliography. All entries are now cited.
- **Citation form was 16 parenthetical to 0 narrative.** It is now 10 parenthetical to 21
  narrative, with reporting verbs distinguishing commitment: *propose*, *present*, *describe*,
  *report*, *find*, *argues*, *survey*, *review*, *frame*, *model*, *compare*, *evaluate*.

## Still outstanding — only you can settle these

**1. The NERDC citation.** "In the Nigerian NERDC curriculum a unit is a subtopic and objectives
are performance objectives" still has no citation. It needs the specific curriculum edition
used. Your `references.bib` has no NERDC entry.

**2. Ethics.** `Ethics Review/` holds a complete UNILAGREC application — full protocol, parental
consent, teacher and expert-rater consent, school authorisation, supervisor letter. **I found no
approval certificate**, and `plan/issue-41-prepare-and-submit-ethics-approval-application…`
reads as still open. The paper therefore has no ethics statement, because I will not write one
asserting approval I cannot see. Supply the actual status and I will add it.

**3. The Cho quotation.** Chapter 1 quotes Cho et al. calling for "an end-to-end model… enabling
educators to effectively apply them in real-world classrooms." That is **not in the abstract**.
Locate it in the body before quoting it in the thesis.
