---
pretty_name: Nigerian JSS1 Mathematics Curriculum and Lagos State Scheme of Work
license: cc-by-4.0
language:
- en
tags:
- education
- mathematics
- curriculum
- learning-objectives
- nigeria
- junior-secondary
size_categories:
- n<1K
configs:
- config_name: atomic_objectives
  data_files:
  - split: train
    path: curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl
  default: true
---

# Nigerian JSS1 Mathematics Curriculum and Lagos State Scheme of Work

The Nigerian national mathematics curriculum for Junior Secondary School 1 (JSS1), issued by the
Nigerian Educational Research and Development Council (NERDC), and the scheme of work the Lagos
State Ministry of Education uses to pace it across the three terms of the school year. Both are
here as readable Markdown and as structured JSON, with the curriculum's performance objectives
split into atomic objectives.

This is one of four datasets released with the LPCG framework from the MSc study *Design and Evaluation of a Lesson-Plan-Driven Framework for Curriculum-Constrained Generation and Personalisation of Learning Materials: A Case Study of Nigerian Junior Secondary Mathematics* (University of Lagos, 2026). Its subtopic and objective ids are what the other
three join on.

88 files, 0.5 MB.

## Contents

| path | what it holds |
| --- | --- |
| `curriculum/JSS1 Math Curriculum.md` and the five theme files | the curriculum as written, in five themes from Number and Numeration to Everyday Statistics; each topic with its performance objectives, teacher and student activities, teaching and learning materials, and evaluation guide |
| `curriculum/jss1_themes.json` | the five themes and the topics under each |
| `curriculum/jss1_topics.json`, `curriculum/topics/` | the 24 topics as JSON: objectives, subtopics, activities, materials (`tlm`) and evaluation guide |
| `curriculum/jss1_topics_enriched.json`, `curriculum/topics_enriched/` | the same 24 topics organised by subtopic, the form the LPCG prototype seeds its curriculum from |
| `curriculum/jss1_knowledge_components.json` | 118 knowledge components, each tied to a subtopic and given a Bloom level |
| `curriculum/manual_authoring/` | atomic objectives by topic and combined, with the specification they follow |
| `scheme-of-work/` | the Lagos State scheme of work for each term, as Markdown and as `jss1_scheme.json` |
| `PROVENANCE.json` | every file with its SHA-256, and the repository commit it was read from |

## Atomic objectives

An atomic objective is the smallest teachable, observable and assessable learner outcome that
traces to exactly one of the curriculum's performance objectives. The split keeps the source
wording and adds nothing to it: no new actions, representations, tools or constraints. The rules
are in `curriculum/manual_authoring/atomic_objective_spec.md`.

Subtopic ids take the form `jss1-math-<topic>-<subtopic>`. They and the atomic objective ids join
this dataset to the textbook linkage (`ng-jss1-math-textbook-linkage`), where each objective is
linked to the textbook records that teach it.

## Source and credit

The curriculum is NERDC's, and the scheme of work is the Lagos State Ministry of Education's.
Both are public documents from public institutions, reproduced here with credit so that they can
be used in machine-readable form. The structuring — the JSON, the knowledge components and the
atomic objectives — is this work's, released under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## Limitations

- JSS1 mathematics only.
- This is a transcription into a new form. For anything official, NERDC's and the Lagos State
  Ministry of Education's own editions govern.
- The atomic objectives and knowledge components are this work's reading of the curriculum, not
  NERDC's.

## Related data

- [`ng-jss1-math-textbook-linkage`](../ng-jss1-math-textbook-linkage/): an open JSS1 textbook, linked to these objectives

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
