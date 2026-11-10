# Superseded frozen plans

One file per lesson version that a recorded run was generated against and the
current `eval_set.json` no longer holds, named `<lesson>-<plan_sha256>.json`.

A run records the content hash of every plan it used, and `pairing.py` refuses to
rebuild a prompt against a plan that has since changed — pairing a response with
inputs it never saw is worse than not pairing it. That guard is right, and on its
own it makes the corpus uncorrectable: the first fix to a lesson orphans every
run before it.

So a superseded version is archived here rather than lost, and the digest a run
recorded resolves to the plan it names. Correcting a lesson costs a file, not a
run.

Nothing is ever edited here. A file appears when a lesson is re-frozen and is
read only by digest.

| file | superseded | why |
|---|---|---|
| `t3-w02-c46e1987c4b4fe87.json` | 2026-08-23 | evaluation question 4 disambiguated — "How many triangles has an octagon" resolved from her own Polygons table to name the diagonal decomposition it means. C1 receives the question and not the table, so under C1 it was unanswerable as she meant it. See the cleaning log. |
| `t2-w09-1c2db992c7c3f40d.json` | 2026-08-24 | the eight declared step enrichments carried into the model-visible copy (`30cb68c6`). |
| `t3-w02-1ef76c8f953798c8.json` | 2026-08-24 | the same enrichments (`30cb68c6`). |
| `t3-w06-a0c7d9ae15955d5d.json` | 2026-08-24 | the same enrichments (`30cb68c6`). |
| `t3-w09-15eace555a066ade.json` | 2026-08-24 | the same enrichments (`30cb68c6`). |
| `t3-w05-44e83716d510b74c.json` | 2026-08-24 | the prism declaration carried into the model-visible copy (`3fd9ddce`). |
| `t3-w05-d4fead605b3ec6c0.json` | 2026-08-25 | the prism objective carried into the model-visible copy (`d04fa7c7`). |

`c1-corrected` also records `t3-w06-fbda90b9dded4a74`, a plan that was never committed, so that
run cannot be paired.
