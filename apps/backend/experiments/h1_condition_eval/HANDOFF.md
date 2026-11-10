# Handoff — where the H1 evaluation stands, 2026-08-11

Two blinded passes over one generation: 6 lessons × C0–C3 × 3 draws = 72 packs, judged
twice = **144 judgments, 576 dimension-scores.** Runs `c0c3-worksheet` and
`c0c3-renumbered` (same `run.json` byte-for-byte, re-rated after a packet fix).

---

## 1. The result

Every arm's score, pooled over 6 lessons × 3 draws × 2 judges (36 judgments per arm):

| arm | what it is given | Objective | Taught-lesson | Scope/correctness | Clarity | **mean** |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| C0 | curriculum objective only | 4.11 | 3.08 | 2.94 | 3.11 | **3.31** |
| C1 | + the lesson plan's design | 3.92 | 3.14 | 3.47 | 3.14 | **3.42** |
| C2 | + her lesson note verbatim | 4.22 | 3.58 | 3.08 | 3.14 | **3.51** |
| C3 | + validation and repair | **4.28** | **3.61** | **3.64** | **3.42** | **3.74** |

**The ladder is monotonic on the overall mean: 3.31 → 3.42 → 3.51 → 3.74.** Each rung adds
something a blinded reader can see, and C3 is top of every column.

As gains over the control, with the registered test:

| dimension | C1−C0 | p | C2−C0 | C3−C0 | p (C3) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Objective and curriculum alignment | −0.19 | .812 | +0.11 | +0.17 | .359 |
| Taught-lesson alignment | +0.06 | .500 | **+0.50** | **+0.53** | **.125** |
| Scope and conceptual correctness | +0.53 | .156 | +0.14 | **+0.69** | .156 |
| Student-facing clarity and usefulness | +0.03 | .500 | +0.03 | +0.31 | .219 |

One-sided Wilcoxon over six lessons; the floor at n=6 is p=.0312, so **nothing here could
have been significant** — a detectable effect must win all six lessons.

**Read it this way.** The registered endpoint (C1−C0) is null and negative on the dimension
the framework's claim rests on. What the ladder does show is that **the gain comes from the
evidence step, not the plan step**: C2 and C3 both clear both no-evidence arms on
taught-lesson alignment, and C3 — C2 plus validation and repair — is the only arm in which
no judge found a mathematical error (C0 5, C1 3, C2 5, C3 0).

---

## 2. Pending data issues, by kind

### Source error — a mistake in her actual plan or note

**None open. None new found in 144 judgments.**

Two findings that look like gaps in her material were checked against the page images and
the note and are **real properties of what she wrote**, so they belong in the thesis as
findings rather than corrections:

- `t3-w06`: perpendicular lines is the only objective with no recorded student-construction
  step — her plan says "Teacher explains the drawing…" where every other step adds "while
  the students construct…".
- `t3-w09`: her evaluation asks for three methods of collecting data, which no step teaches;
  the four methods are in her **note**. This is the ladder working — C1 cannot answer it, C2
  holds the answer.

### Pipeline error — source carried into the model or onto the page wrongly

**All four now closed.** They pushed in opposite directions, so leaving them was never neutral.

| defect | C0 | C1 | C2 | C3 | who it hurt | now |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| LaTeX command outside any math delimiter | 29 | **39** | 0 | 4 | the **no-evidence** arms | **0** |
| a field carrying its JSON punctuation in | 0 | 0 | 2 | **9** | the **grounded** arms | **0** |
| a degree sign inside maths, drawn as a gamma | 2 | **7** | 4 | 0 | the **no-evidence** arms | **0** |
| LaTeX the typesetter does not implement | 3 | 0 | 2 | **13** | the **grounded** arms | **1** |

- **Bare LaTeX, 72 occurrences.** The model wrote `Perimeter = 4 \times side` in plain
  prose with no `\(…\)` around it, so arithmatex never marked it and the learner read the
  backslash. C2 scored 0 because it copies her note, which delimits its maths properly;
  C0/C1 invent notation and get it wrong. **It was the mirror of the numbering confound —
  it penalised the control and the treatment arm, C1 worst of all.**
- **Stray quote residue, 11 fields.** Answers ending `32 + 4x",` — the field over-running
  its own closing quote and carrying the rest of the JSON object in. Concentrated on C3.
- **Degree signs drawn as gammas, 13 fields.** The silent one, and it was found by
  reading a rendered page rather than by any check: Computer Modern maps U+00B0 to the
  same outline as `\gamma`, so `\((n-2)\times180°\)` reached the page as *180γ*. Nothing
  reported it — the glyph is not missing, it is the wrong one, so the missing-glyph
  watcher never fired. `math_svg` now rewrites it to `^\circ`, which is how the teacher's
  own notes write it. Directional again: C1 7, C0 2, C2 4, C3 0.
- **18 expressions the typesetter refused, 13 of them C3.** mathtext is a subset of
  LaTeX, so `\displaystyle`, `\boxed{…}`, the `\big` family and `\tfrac` all raised and
  the expression fell back to its own raw source on the page. Rewritten to the nearest
  thing mathtext does implement: **18 → 1** across 2,467 math runs, and the survivor is a
  bare `\sqrt` with no argument, which is malformed whatever renders it.

[`app/shared/llm_markup.py`](../../src/app/shared/llm_markup.py) supplies the markup the model
left off — wrapping a bare command **where it stands**, so `4 \times side` typesets as
`4 × side` and the words either side stay prose. Substituting the Unicode `×` would have
been worse: the vendored Computer Modern has no glyph for it, so a visible backslash would
have become a missing-glyph box.

It is applied at generation, at render, **and where a frozen run's packets are built**, so
both judged runs render clean without regenerating and `run.json` still describes the text
that was actually judged. Every step is idempotent. Measured on the frozen packs: **72 → 0**
bare commands and **11 → 0** residues, in both passes.

Two consequences worth carrying:

- `raw_latex_markers` in the run metrics counted every `\times` and `\text{` whether
  delimited or not, so a correctly typeset pack scored as badly as a broken one. It now
  counts what reaches the reader as a backslash. **Figures either side of this are not
  comparable.**
- The guard is a render-level assertion that *no* backslash-command reaches the page, not a
  list of the commands we happen to have met.

**Closed and confirmed on real data:** control characters where `\times` belonged (issue
#162) — **0** across all 72 packs. Answers printed under their own question (#163) — **0**,
where the previous artefact had them in 9 of 12 cells.

### Leakage error — the model shown what it must not see

**None. Probed directly on all 72 packs' learner-facing text, not inferred from judge
wording:**

| probe | hits |
| --- | ---: |
| step ids (`step-t3w06-02`) | 0 |
| objective ids (`lo-t3w06-01`) | 0 |
| section/block ids (`objective:…`) | 0 |
| source refs (`REF-1`) | 0 |
| Gagné event names (`elicit_performance`, …) | 0 |
| planning jargon ("lesson plan", "entry behaviour", "assessment point", …) | 0 |
| teacher narration ("the teacher explains…") | 0 |

The leakage guards from the wire-leakage suite hold on real output.

### Judging error — the instrument rather than the pack

**The measured one, and it is the biggest single caveat in the study.** The two passes rated
**prose-identical packs**, so movement between them is judge noise with generation held
constant:

| arm | scores that moved | of | mean size of a move |
| --- | ---: | ---: | ---: |
| C0 | 13 | 24 | 0.44 |
| C1 | 15 | 24 | 0.49 |
| C2 | 15 | 24 | 0.38 |
| C3 | 15 | 24 | 0.44 |

**More than half of every arm's scores moved, by about half a point, on identical text.** A
margin under ~0.5 from one judge per candidate is not a finding. Objective alignment's
C1−C0 went +0.06 → −0.44 across the passes: a sign flip well inside that floor.

No evidence of systematic harshness or of the wrong rubric being applied — scores use the
full 1–5 range, and three cells cite the rubric's own "Goes beyond this lesson" flag
correctly.

### Unnecessary-information error — ids, ordering, things the model cannot use

**Closed.** Practice items were numbered twice on the page — 51%/56% of C2/C3 prompts already
began with their own number (copied from her numbered task lists) against 17%/18% for C0/C1,
so the page read `1. 1. Simplify 4n+3n×10.` Twenty judgments flagged it, 17 on C2/C3.

Fixed by `app/shared/item_numbering.py`: 277 duplicate numbers dropped, 63 genuine sub-step
runs kept and re-lettered. **21 complaints in pass 1, 0 in pass 2.**

It was worth only **+0.06** on grounded-arm clarity — an eighth of the noise floor. Real,
directional, and nearly worthless. Worth knowing before human raters see the packets; not
worth reinterpreting a result over.

---

## 2b. The code path, entry point to model call

Which call happens for C0–C4 and P1, what is in it, and which `ConditionProfile` field
decided: [`docs/generation-call-stack.md`](../../docs/generation-call-stack.md).

## 3. What to do next, in order

1. **Done — the two directional rendering defects are closed** (§2, *Pipeline error*).
   Packets built from either judged run now render with no bare LaTeX and no JSON residue,
   without regenerating the run.
2. **Two judges per candidate is now the floor, not an aspiration.** The 0.38–0.49 movement
   is what one judge costs. Any future pass should be ≥2, and the pooled figures in §1 are
   the ones to quote.
3. **n=6 cannot return significance.** Either accept the manipulation check as descriptive
   and let the expert raters carry the endpoint, or widen the lesson set.
4. **The interesting result is the evidence step.** C2/C3 clearing C0/C1 on taught-lesson
   alignment, and C3's clean sheet on mathematical error, are the findings with a mechanism
   behind them. C1-only is not visible to a blinded reader on this rubric now that it
   carries the plan's design rather than its prose.

## 4. The specs — what C0–C3 and the artefact are defined to be

### The conditions

The ladder is one added ingredient per rung, and each rung keeps everything below it:

| rung | what it adds | spec |
| --- | --- | --- |
| **C0** | the curriculum specification alone — objectives, subject, grade, topic, subtopic | [C1-DEFINITION.md § The ladder](C1-DEFINITION.md#the-ladder) |
| **C1** | the lesson plan's **design**: entry behaviour, materials, step order, Gagné-coded instructional events, her student tasks and assessment questions as statements | [C1-DEFINITION.md](C1-DEFINITION.md) — the positive enumeration, field by field, each naming the place in her document it is read from |
| **C2** | her lesson **note**, verbatim, as scoped evidence | C1-DEFINITION.md §*The ladder* — C2 needs no boundary of its own; it is C1 plus the note passed whole |
| **C3** | **validation and repair** — structural checks plus an LLM critic reading the pack against what she taught, then repair of what either flags | [profiles.py](../../src/app/domains/experiments/review_pack_study/conditions/profiles.py) `_FULL_VALIDATION` |
| C4 | a teacher-approval gate over C3's actual pack (not in H1's rating set) | [profiles.py](../../src/app/domains/experiments/review_pack_study/conditions/profiles.py) |

**The executable spec is [`profiles.py`](../../src/app/domains/experiments/review_pack_study/conditions/profiles.py)** —
`H1_CONDITION_PROFILES` maps each code to a frozen `ConditionProfile` of
`ContextPolicy` / `RetrievalPolicy` / `ValidationPolicy`. The DSPy modules carry **no**
condition logic; a condition is a data record, so what an arm receives can be diffed rather
than traced. `C1-DEFINITION.md` is the prose that governs it, and
**[C0-C1-INPUTS.md](C0-C1-INPUTS.md) is the payload itself** — every lesson's real prompt
fields, dumped by [`dump_inputs.py`](dump_inputs.py) through the same two functions the
generator calls, so a field that is silently empty shows up as empty.

Design rationale for the whole ladder, including why C2 differs from C1 by *explicit source
evidence at generation time* rather than by textbook history:
the pre-registration (not in this repository), §3 *H1 conditions* and §5 *Condition profiles*.

### The artefact being rated

A **take-home revision pack**: per learning objective, explanation → worked examples →
practice with answers, rendered as a worksheet PDF.

| what | where |
| --- | --- |
| the design, literature-first, with its deviations argued | [ARTEFACT-DEFINITION.md](ARTEFACT-DEFINITION.md) |
| the executable spec handed to the generator | [`revision_pack_spec()`](../../src/app/domains/artefacts/types/post_class_review_pack/application/request/artefact.py) |
| the four frozen rating dimensions | [`H1_RUBRIC`](../../src/app/domains/evaluation/application/constants.py) |
| the worksheet renderer a judge actually reads | [`worksheet_html/`](../../src/app/domains/evaluation/application/worksheet_html/) |

The rubric is frozen: `objective_curriculum_alignment`, `taught_lesson_alignment`,
`scope_conceptual_correctness`, `clarity_usefulness`, each 1–5. The analysis plan
(2026-07-26, H1a = C1 vs C0 as the sole endpoint) is in the pre-registration, which is not in this
repository.

---

## 5. Reproducing it

Everything below runs from `apps/backend`. The generation costs real API calls; the rating
costs one judge call per candidate.

### 5.1 Generate C0–C3

This is the exact command behind `runs/c0c3-worksheet`, the run both passes rated:

```bash
uv run python -m experiments.h1_condition_eval.runner --label c0c3-worksheet --conditions C0 C1 C2 C3 --generator compose-v2 --signatures leveled --note-source clean --figures source --repeats 3 --notes "full C0-C3 on the worksheet artefact"
```

> **The judged run did not use this command.** `c0c3-worksheet`'s fingerprint records
> `raw` / `reference` / `shared`, and its stored prompts carry the raw note's `**layered**`
> editorial 18 times with none of the clean copy's corrections. It was launched without
> these three flags and generated from the frozen transcription. See
> [FINDING-JUDGED-RUN-USED-RAW-NOTES.md](FINDING-JUDGED-RUN-USED-RAW-NOTES.md); `clean-six`
> is the first full run on the hand-edited notes.

72 packs (6 lessons × 4 conditions × 3 draws), about 50 minutes. It writes
`runs/<label>/run.json` — every case's sections, plus recall/invention/finding counts — and
`fingerprint.json`, which pins the code and flags the run was made with.

What each flag is doing, and why it is not the default:

| flag | value used | why |
| --- | --- | --- |
| `--generator` | `compose-v2` | native tool calling. The `compose` arm parses tool calls out of prompt text and produced 5/6 duds on the dspy 3.3.0b1 stack — **do not use it**; every pre-2026-08-04 `compose` number is self-selected |
| `--signatures` | `leveled` | per-level signatures, unused fields absent. `shared` leaves C0 reading present-but-empty plan keys |
| `--repeats` | `3` | every arm is stochastic; one draw per cell is not a margin |
| `--note-source` | `clean` (default) | the hand-edited note files. `raw` still carries transcription commentary |
| `--figures` | `source` (default) | her drawings travel as TikZ. On a construction lesson the drawing **is** the method |
| `--repair` | `rewrite` (default) | whole-section repair |
| `--temperature` | `0.0` (default) | pinned and fingerprinted rather than left to the provider |
| *(no `--lessons`)* | all six | `t2-w09 t3-w02 t3-w04 t3-w05 t3-w06 t3-w09` |

Useful narrower forms — one lesson to smoke-test, and two runs' inputs diffed:

```bash
uv run python -m experiments.h1_condition_eval.runner --label smoke --lessons t3-w06 --conditions C0 C3 --generator compose-v2 --signatures leveled --repeats 1
```

```bash
uv run python -m experiments.h1_condition_eval.runner --diff c0c3-worksheet smoke
```

### 5.2 The blind review

Four steps. The blinding lives in steps 1 and 2 and is easy to break by hand, which is why
steps 1 and 3 are code.

**1 — Build the packets.**

```bash
uv run python -m experiments.h1_condition_eval.rater_packets c0c3-worksheet
```

One packet per candidate under an opaque id — `cand-3f9a2c`, a SHA-256 of
`run-label|lesson|condition|repeat`, so neither the arm nor any ordering is recoverable and
a rerun addresses the same candidate. Each packet is: the lesson as its teacher planned it
(her own words for the activities, never the Gagné codes — the coding is the study's
instrument), then one candidate pack, then the rubric. Nothing names the condition and
nothing hints that conditions exist. The de-anonymisation key is written to
`rating/_key.json`, **outside** the packet directory: reading it unblinds all 72 at once.

Packets and worksheet PDFs are deliberately **not committed** — 9 MB, and reproducible from
`run.json`.

**2 — Dispatch one judge per candidate.**

One subagent per candidate. **Never several candidates to one agent** — a judge holding two
packs rates them side by side, which invites it to decide which is meant to win and breaks
the pairing the frozen analysis assumes. Cap concurrency around 20 and keep a
dispatched-ids ledger: the concurrency error does not say which calls it dropped.

The prompt each judge receives, verbatim:

> You are an experienced JSS1 mathematics teacher in Nigeria, asked to rate a take-home
> revision pack that a student would use alone at home.
>
> Read the rating packet at `runs/<label>/rating/packets/<cand-id>.md`
>
> It contains: the lesson as its teacher planned it, then a revision pack produced for that
> lesson, then a rubric.
>
> Rate the pack on each of the four rubric dimensions, 1-5 (5 is best).
>
> Return ONLY a JSON object — no prose before or after, no code fence — in exactly this shape:
> ```json
> {"candidate_id": "<the id in the packet heading>",
>  "objective_curriculum_alignment": {"score": 0, "evidence": ["..."], "rationale": "..."},
>  "taught_lesson_alignment":        {"score": 0, "evidence": ["..."], "rationale": "..."},
>  "scope_conceptual_correctness":   {"score": 0, "evidence": ["..."], "rationale": "..."},
>  "clarity_usefulness":             {"score": 0, "evidence": ["..."], "rationale": "..."}}
> ```
>
> For each dimension: `score` is an integer 1-5; `evidence` is 1-3 short concrete
> observations of what you actually saw in the packet; `rationale` is one or two sentences.
>
> Judge only what is in front of you. Do not speculate about how the pack was produced.

Each judge writes its JSON to one file in a collection directory outside the run. When
waiting on completion, **count `*.json`, not all files** — a judge once wrote a stray
`.txt` into that directory and inflated the count while three candidates were unjudged.

**3 — Collect, with the guards.**

```bash
uv run python -m experiments.h1_condition_eval.collect_judgments c0c3-worksheet /path/to/judged --judge-model "claude-sonnet (fixed; deliberately not the generator's model)" --judges-per-candidate 1 --generation-draw "all 3 repeats"
```

This is the step where a mistake is invisible — a missing candidate reads as a smaller run,
a duplicate reads as agreement — so the checks are **refusals, not warnings**: every
candidate in the key judged, none judged twice, no unknown id, every frozen dimension
scored 1–5 with a rationale behind it.

**4 — Build the report.**

```bash
uv run python -m experiments.h1_condition_eval.rating_report c0c3-worksheet
```

Writes `rating/RATING-RESULTS.md`: per-arm means, the C1−C0 endpoint under the one-sided
Wilcoxon, the C0→C3 ladder, within-arm spread, and every judgment's evidence.

### 5.3 Rating the same generation twice

What produced `c0c3-renumbered`, and how to measure the judge rather than the generator.
Copy `run.json` byte-for-byte under a new label, then rebuild packets: candidate ids are
hashed with the run label, so a new label mints ids no judge has seen, over identical prose.

```bash
uv run python -c "import shutil, pathlib; r = pathlib.Path('experiments/h1_condition_eval/runs'); (r/'NEW').mkdir(exist_ok=True); shutil.copy(r/'OLD'/'run.json', r/'NEW'/'run.json')"
```

Then steps 1–4 again with the new label, and compare the two passes:

```bash
uv run python -m experiments.h1_condition_eval.rating_report c0c3-renumbered --against c0c3-worksheet
```

`--against` prints both passes' C1−C0 margins side by side and the movement per arm on
identical text — which is the noise measurement in §2.

---

## 6. Where things live

| what | where |
| --- | --- |
| the two judged runs | `runs/c0c3-worksheet/`, `runs/c0c3-renumbered/` |
| per-judgment evidence | each run's `rating/RATING-RESULTS.md` |
| the written report | [BLIND-RATING-REPORT.md](BLIND-RATING-REPORT.md) |
| what the artefact is | [ARTEFACT-DEFINITION.md](ARTEFACT-DEFINITION.md) |
| what each condition is | [C1-DEFINITION.md](C1-DEFINITION.md), [profiles.py](../../src/app/domains/experiments/review_pack_study/conditions/profiles.py) |
| exactly what C0/C1 receive | [C0-C1-INPUTS.md](C0-C1-INPUTS.md) |
| the teacher's notes, model-visible | `notes-clean/` — **hand-edited only, never scripted** |
| generate | [`runner.py`](runner.py) |
| build blinded packets | [`rater_packets.py`](rater_packets.py) |
| collect judgments | [`collect_judgments.py`](collect_judgments.py) (refuses partial/duplicate sets) |
| build the report | [`rating_report.py`](rating_report.py) `<run> [--against <run>]` |
