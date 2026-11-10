---
pretty_name: Nigerian JSS1 Mathematics Textbook and Objective Linkage
license: other
license_name: cc-by-3.0-and-cc-by-4.0
license_link: LICENSE.md
language:
- en
tags:
- education
- mathematics
- open-textbook
- curriculum-alignment
- nigeria
- junior-secondary
size_categories:
- n<1K
configs:
- config_name: linked_records
  data_files:
  - split: train
    path: textbook/jsonl/linked/records.jsonl
  default: true
---

# Nigerian JSS1 Mathematics Textbook and Objective Linkage

Siyavula's open textbook *Mathematics JSS-1*, digitised into chapters and records, and a linkage
from the atomic objectives of the Nigerian JSS1 mathematics curriculum to the textbook records
that teach them. The LPCG prototype is seeded from this linkage.

This is one of four datasets released with the LPCG framework from the MSc study *Design and Evaluation of a Lesson-Plan-Driven Framework for Curriculum-Constrained Generation and Personalisation of Learning Materials: A Case Study of Nigerian Junior Secondary Mathematics* (University of Lagos, 2026).

449 files, 19.8 MB.

## Contents

| path | what it holds |
| --- | --- |
| `textbook/Table of Content.md`, `textbook/markdown/` | the book as Markdown, one file for each of its 17 chapters |
| `textbook/jsonl/linked/` | the book as 1,500 records in 90 packets, each record linked to a curriculum subtopic, with `records.jsonl`, the subtopic catalogue and a validation report |
| `linkage/jss1-math-*.json` | 78 rows, one per curriculum subtopic: its atomic objectives and the records that teach each, shared foundation records, excluded records, review items, candidate objectives, and the row's status with its reasons |
| `linkage/manifest.json` | the rows, and the objective, record and prompt-template paths they were produced from |
| `linkage/review_triage.json` | the review categories, counted across rows |
| `linkage/review_audit/` | the audit behind each status: a file per subtopic (78), per atomic objective (158) and per chapter (18), with 45 candidate atomic objectives proposed for expert review |
| `LICENSE.md` | the two licences, and what each covers |
| `PROVENANCE.json` | every file with its SHA-256, and the repository commit it was read from |

## How far to trust a row

Every row states its status and the reasons for it. Of the 78 rows, **31 are mapped, 44 need
review, and 3 have no records** in the textbook for their subtopic. Across 2,031 source records,
243 are shared foundation, 512 are excluded and 279 are held for review. Rely on a `mapped` row;
read a `needs_review` row as a proposal, with the review audit giving the evidence either way.

The prototype's seed reads the 78 row files and skips `manifest.json` and `review_triage.json`.
Seeded, the linkage gives 78 rows, 158 atomic objectives and 997 record links.

The subtopic and atomic objective ids are those of the curriculum dataset
(`ng-jss1-math-curriculum`), where each objective's source wording and specification are kept.

## Licence and credit

Two licences apply; `LICENSE.md` sets out which covers what.

- `textbook/`: adapted from *Mathematics JSS-1* by
  [Siyavula](https://ng.siyavula.com/read/ng/mathematics/jss-1), under
  [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). Siyavula confirmed in writing that its
  Nigerian JSS1–3 mathematics content may be used under this licence.
- `linkage/`: this work's, under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## Limitations

- 44 of the 78 rows still need expert review, and 3 subtopics have no textbook records at all.
- The Markdown and the records are a conversion of the book; for anything that matters, check the
  book itself.
- JSS1 mathematics only.

## Related data

- [`ng-jss1-math-curriculum`](../ng-jss1-math-curriculum/): the curriculum and scheme of work these objectives come from

## Citation

```bibtex
@mastersthesis{amuda2026lpcg,
  author = {Amuda, Tosin},
  title  = {Design and Evaluation of a Lesson-Plan-Driven Framework for Curriculum-Constrained Generation and Personalisation of Learning Materials: A Case Study of Nigerian Junior Secondary Mathematics},
  school = {University of Lagos},
  type   = {MSc dissertation},
  year   = {2026}
}
```
