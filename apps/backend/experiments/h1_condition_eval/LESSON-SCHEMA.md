# A schema for the lesson document — 2026-08-19

Written after reading the corpus rather than from a template: all 26 evaluation questions,
all 26 teacher and 22 student activities, and the 38,353 characters of note across 20 steps.

**The problem it solves.** Every surface that consumes her lesson is a *parser*. Six of them
re-derive the same structure from one markdown blob, each with its own regex, and this week
each of those regexes was wrong at least once. With structure declared, a surface becomes a
*projection* — a selection over a document — and the defect class stops being representable.

**Content stays markdown.** Her prose is prose, the study needs it verbatim, and her maths is
already correctly delimited — `$…$`, 348 of them, and not one of the delimiting defects we
found came from her note. They came from *generated* text. The schema declares structure and
leaves leaves alone.

---

## What the corpus actually contains

Counted, not assumed:

| structure | count | today's carrier |
| --- | ---: | --- |
| inline maths `$…$` | 348 | markdown, correct as written |
| markdown table rows | 51 | pipe table |
| numbered lines | 50 | `1.` prefix — collides with renderer numbering |
| bold lead-ins | 48 | `**Term:**` — definitions, hints, example labels |
| `####` section headings | 46 | markdown heading |
| TikZ drawings | 38 | `\begin{tikzpicture}` inline |
| `Solution` markers | 22 | `**Solution**` or `Solution:` |
| `**fig-NN.**` captions | 17 | present on 2 lessons, absent on 2 others |
| `Example N.` labels | 6 | `**Example 1.**` or `##### 1.` |

Two inconsistencies visible only by reading: figures are labelled `**fig-NN.**` on `t3-w05`
and `t3-w06` and left as unlabelled prose on `t3-w02` and `t3-w04`; and set work is headed
`Activity`, `Students activity` and `Student activity` in three steps of the same lesson.

## What each surface consumes today

| surface | what it reads | how |
| --- | --- | --- |
| generation `in_prompt` | note verbatim as `source_evidence` | serialised into the prompt |
| generation `read_tools` | note as documents | `list_documents()`, `read_document(doc, start, end)` — **line-addressed** |
| generation `workspace_files` | note as `<step_id>.md` on disk | file tools |
| generation, all arms | activities → Gagné codes; practice blocks → `student_tasks`; evaluation blocks → `assessment_points` | regex + projection |
| judge reference sheet | objectives, entry behaviour, materials, **core activities verbatim**, practice and evaluation questions | direct read |
| judge candidate + worksheet | generated sections | rendered |

`read_document` addresses **lines**. A line number over a markdown blob is an address that
moves whenever anyone edits a word above it. Over a structured document the address is an
element id, which survives editing — the tool surface gets better, not merely tidier.

---

## The schema

**The note is not in it.** Her prose stays in `notes-clean/`, one hand-edited file per
step, and a `<section>` addresses a region of it by the heading the note itself carries.
That is not tidiness. `notes-clean/` is the model-visible copy and the rule on it is
hand-edited, never scripted — so inlining the note would force one of two bad things: a
script that generates the document from her files, or a second copy of her writing that
drifts from them. Referencing keeps exactly one copy of every sentence she wrote.

```xml
<lesson id="t3-w05" subject="Mathematics" grade="JSS1" term="Third Term" week="5"
        topic="Three dimensional shapes II"
        subtopic="Three dimensional figures: properties of cylinders and spheres, and volume">

  <curriculum>
    <objective id="jss1-math-...-po01">Identify the properties of cylinders and spheres</objective>
  </curriculum>

  <objectives>
    <objective id="lo-t3w05-01" kc-type="concept"
               curriculum="jss1-math-...-po01">identify properties of cylinders and spheres</objective>
  </objectives>

  <entry-behaviour><item>properties of cubes and cuboid</item></entry-behaviour>
  <materials><item>shapes of cylinders and spheres.</item></materials>

  <step id="step-t3w05-02" kind="core" objective="lo-t3w05-01" minutes="15"
        title="Step 1" instructional-type="explain_practice">
    <teacher-prose>Teacher displays shapes of cylinders and spheres while the students
identify the properties.</teacher-prose>
    <activities>
      <activity who="teacher" event="present_content">displays shapes of cylinders and spheres</activity>
      <activity who="student" event="elicit_performance" sets-work="true">identify the properties</activity>
    </activities>

    <!-- Where her writing is, what it hashed to when this structure was declared,
         and which of its regions carry which role. No prose. -->
    <note src="../notes-clean/t3-w05/step-t3w05-02.md"
          sha256="a3b51c9c8337622a17531924815eb4ff696bca77a4363b77be26109c79903667">
      <section id="b1" role="explanation" heading="Properties of a cylinder">
        <figure ref="fig-01"/>
      </section>
      <section id="b2" role="explanation" heading="Properties of sphere">
        <figure ref="fig-02"/>
      </section>
      <section id="b3" role="set-work" heading="Student activity"/>
    </note>
  </step>

  <step id="step-t3w05-04" kind="evaluation" minutes="5" title="Evaluation">
    <questions>
      <question id="q1" objective="lo-t3w05-02">Calculate the volume of a cuboid 8cm long,
        4cm wide and 3cm high.</question>
      <question id="q2" objective="lo-t3w09-02"><part label="b">State three methods of
        collecting data.</part></question>
    </questions>
  </step>
</lesson>
```

An evaluation question has nowhere external to live — it is in her plan, not her note —
so it is declared here. The rule is one line: **anything that exists in the note is
referenced; anything that exists only in the plan is declared.**

### Rules it enforces

The grammar (`app/domains/artefacts/types/lesson_plan/domain/lesson.rng`) fixes shape. Cross-document facts a grammar cannot
see are checked by the loader, and both run under `validate`, so both fail at authoring
time:

- `objective` resolves into the declared set — a question tagged to an objective the
  lesson does not declare is refused, as is a core step that teaches nothing nameable.
- The note still hashes to what was declared. Hand-edit a note and the document refuses
  until someone re-reads the sections and runs `reseal`.
- A `heading` occurs in the file **exactly once**, or it addresses nothing.
- **Every character of the note lands in exactly one region**, and no region swallows a
  sibling heading. A region may contain its own sub-headings; it may not absorb a
  section that should have been declared beside it.
- A declared `<figure>` label is actually carried by its region, which retires both the
  caption/no-caption split and the TikZ regex that put `\begin{tikzpicture}` into the
  judge's reference sheet.
- `<task>`/`<question>` carry **no number**. Numbering is the renderer's, always — the
  277 duplicate-enumerator problem stated as a rule instead of repaired downstream.
- `<part label="b">` makes an answer's labels derivable from its question, so `1. 2. 3.`
  answered `a. b. c.` is unrepresentable rather than merely fixed.
- `sets-work` is an attribute, read and confirmed against the source page. The Gagné
  coder becomes a *proposal* checked at authoring time; `student_work.json` disappears.
- A `<section>`'s role must agree with the role **her own heading** proposes, or carry a
  `role-note` saying why not. This is the only check on a role that the role does not
  decide for itself.
- Ids are local NCNames (`b1`, `q1`) and compose to `step-t3w05-02:b1` in the
  projection. The colon that has already corrupted a dot-path in the rater form is a
  serialisation detail now, not an identity.

### What it does not fix

Undelimited maths in **generated** text. That is model output, not her document, and
`reader_ready` still owns it. Her note's maths was correct throughout.

Nor does it dedupe her plan's own prose: four of the five evaluation steps restate their
questions inside `<teacher-prose>`, because she wrote them there. The addressable form
is authoritative; the narration is kept verbatim because it is hers.

---

## The pilot

`lessons/t3-w05.xml` — 116 lines, **zero characters of her prose**, referencing 3,241
characters across three note files.

```bash
uv run python -m experiments.h1_condition_eval.lesson_document validate lessons/t3-w05.xml
uv run python -m experiments.h1_condition_eval.lesson_plan_projection diff lessons/t3-w05.xml
```

| module | job |
| --- | --- |
| `app/domains/artefacts/types/lesson_plan/domain/lesson.rng` | the grammar, which the app holds its own lesson plans to |
| `lesson_document.py` | read, validate, resolve regions; `validate` and `reseal` |
| `lesson_plan_projection.py` | document + notes → the plan dict the surfaces already read |
| `lesson_selections.py` | the migration table, executable |
| `lesson_delivery.py` | role → channel → condition, resolved from `profiles.py` and measured; `check` |
| `tests/test_lesson_document.py` | 22 tests holding all of it to its claims |

**Lossless.** `diff` reports *the projection equals the frozen plan exactly*. Every
field of `eval_set.json`'s t3-w05 entry is reproduced from the document plus her three
note files, so the JSON copy is redundant rather than merely duplicated.

**Nothing downstream changes.** The judge's reference sheet, the worksheet detail, the
evaluation questions and the lesson sequence are byte-identical whether `rater_packets`
is handed the frozen plan or the projection. The surfaces read the document without
knowing they do.

**The selections return what the parsing returns.** `student_tasks`, `assessment_points`
and the figure list are each asserted equal to today's regex path. `question_as_asked`
still runs — turning drawing source into a readable reference is rendering, and it
stays. What goes is the structural guessing.

**The refusals are tested as refusals.** A note edited since the structure was declared,
a swallowed sibling heading, a preamble no section claims, a dangling objective, a core
step with no objective, a figure the region does not label, work declared as prose, prose
declared as work — eight defects attempted against the format, eight errors.

---

## The role is the condition boundary

Measured on the pilot, by looking for each region's own sentences in the rendered
request rather than by reading the profile:

| region role | C0 | C1 | C2/C3 |
| --- | :---: | :---: | :---: |
| `recall` (her intro note) | — | — | — |
| `explanation` | — | — | ✓ `source_evidence` |
| `worked-example` | — | — | ✓ `source_evidence` |
| `set-work` | — | **✓ `student_tasks`** | ✓ |

So "the note is C2" is not quite the rule. A task she set the students is *plan*
evidence and travels with C1; the mathematics that answers it does not. `profiles.py`
says so in as many words — "a learner-directed task written into a lesson-plan activity
field is plan evidence; the mathematics answering it is not" — and this is the same rule
stated per region of her document.

That matters because **the C1 leaks found so far arrived through fields that did not look
like the note.** `include_lesson_step_structure` was switched off because
`instructional_type` is derived from `blocks`, which on a field plan are a parse of her
note; `include_step_content` was switched off because a step's `content` restates the
activities and, the reason records, carried her note on four of fourteen core steps.

Both gates are right and both stay. The second reason is now measured rather than
remembered: `source_boundary.py` looks for every sentence of every core step's `content`
and `activities` in the note the model receives at C2, writes `SOURCE-BOUNDARY.md`, and
fails if it finds one. On the seventeen-step corpus it finds none — every sentence is her
Presentation narration, and where she wrote none the researcher-supplied title stands in.
`test_source_boundary` plants a note sentence in each field and checks it is caught, so a
clean result is a finding and not a silent detector.

That is the honest measure of what the region check buys. `lesson_delivery.py check`
compares where each region's own sentences land against what its role allows, through the
real builder, and it catches **the builder disagreeing with the policy**. It does not
catch a mis-roled region — the role drives the projection, so the measurement moves with
the mistake — and it does not catch a restatement, only a verbatim copy.

The mis-role is caught somewhere else, by the one piece of evidence the document did not
author: **her own heading.** All 45 distinct headings in the corpus, over 47 heading
lines, are read and recorded in `note_headings.json` — three of them head work she set.
The heading proposes the role, and a disagreement is refused unless `role-note` records
the reading that overrules it. A heading nobody has read yet proposes nothing and refuses
nothing; `validate` counts those so they stay visible.

`role="recall"` earns its keep here too: her intro note reaches no condition at all —
the intro step is filtered out of the generation units — so the document records
`delivered="false"` rather than leaving that to be rediscovered.

## The corpus, migrated

All six lessons are documents: **38 regions, 39,030 characters of her note referenced and
none copied.**

```bash
cd apps/backend && uv run python -m experiments.h1_condition_eval.lesson_document validate lessons/t3-w02.xml
```

Each surface is now a selection:

| surface | today | with the schema |
| --- | --- | --- |
| `student_tasks` | practice blocks, else a Gagné regex over the activity column | `//set-work` ∪ `//activity[@sets-work='true']` |
| `assessment_points` | evaluation blocks grouped by objective | `//question[@objective=$o]` |
| reference sheet questions | raw text, TikZ and all | `//question`, `//set-work` |
| figures | `\begin{tikzpicture}` regex, captions matched by position | `//figure`, one per drawing, declared |
| `read_document` | line ranges over a blob | region ids that survive editing |

`diff` separates a **format change** — one the migration makes on purpose and states as a
rule — from a **disagreement**, where the frozen plan and her note say different things.
Twenty-seven and eleven respectively, pinned per lesson in the tests so neither can grow
quietly:

| lesson | format | corrections | disagree |
| --- | ---: | ---: | ---: |
| t3-w05 | 0 | 0 | 0 |
| t3-w04 | 9 | 0 | 0 |
| t3-w09 | 0 | 0 | 1 |
| t3-w02 | 28 | 0 | 2 |
| t2-w09 | 5 | 3 | 3 |
| t3-w06 | 8 | 0 | 5 |

A **correction** is the third bucket: a frozen value a reader established was wrong. So
far there is one kind. ``final_answer`` is the body's last line in the frozen corpus,
and eight of the nineteen worked examples are lettered (a), (b), (c) — their recorded
"final answer" is the last part's. The document declares the answer where there is one
and declares none where there are several, so t2-w09 Example 1 no longer claims that
$= 0$ is its answer. The field is inert (a worked-example block reaches no condition),
which is why the fix is safe and why nobody had noticed.

The format changes are three rules: block ids are sequential within a step (the corpus
nests worked examples as `b1e1`); an intro step with no note file carries `note:''`; and
the document references `notes-clean/`, which is what generation actually reads — that
last one is all five of t3-w06's, where the hand-edited figure captions differ from the
transcription they were edited from.

### The eleven disagreements, read

**Eight are the same thing: the step's own prose, filed a second time as a note block.**
On t2-w09's three core steps and all five of t3-w06's, block `b0` holds `step.content`
verbatim — "Teacher explains the steps in constructing parallel lines to the students
while the students construct parallel lines." The document has `<teacher-prose>` for
that, so the projection does not emit a second copy.

**Two are content the block decomposition dropped.** `t3-w09-02`'s note opens with
*statistics is the science of collecting, organizing, presenting, analyzing and
interpreting data* — the definition of the subject, and no block holds it.
`t2-w09-03`'s opens with `**Hints**` and three rules about what `+` and `-` signs do to
the terms inside a bracket — the substance of the lesson, and no block holds that either.
Both are preambles, above her first heading, and the transcription started at the heading.

**One is a label dropped** — `**Worked examples**` on `t3-w02-04` — and **one is a label
invented**: the frozen block for that lesson's fourth example carries
`label: "Solution"`, and her note has no solution marker there at all.

Nothing that reaches the model is affected by any of the eight: `for_step` sends the note
when a step has one, so those `b0` blocks are never read. The two dropped preambles do
reach C2/C3, inside the whole note. What they cost is a block-shaped consumer, which is
what the packet renderer is.

### What reading the files found that reading the code did not

The six documents were generated, validated by code, and never opened. Opening them:

- **Researcher commentary filed as the teacher's prose.** `t3-w04` and `t3-w09`'s
  evaluation steps carry, in the plan's `content` field, a note explaining how their
  questions were assembled — *"Assembled from the plan's own two in-lesson activity sets…
  This is **not** the classwork the students sat"*. The element is renamed
  `<plan-content>` and those two carry `author="researcher"`, because calling it
  `<teacher-prose>` was a lie the document was telling.
- **Two lessons' evaluation questions are researcher-assembled**, which that same
  commentary states plainly and nothing else records. `t3-w09`'s real evaluation sets work
  from the textbook by reference — *"Exercise 17a No 3 and 4 page 158 NGM"* — so the
  question text is nowhere in the plan. This is a fact about the study's inputs that
  deserves to be somewhere other than a prose field nobody reads.
- **`content` is the step title again** on `t3-w02-04` and `t3-w09-03`. Both are core
  steps; `t3-w09-03` is the step that teaches the four data-collection methods, and it has
  no activities either.
- **`t3-w06` has no evaluation step at all** — six steps, five of them core, no questions.
  So `assessment_points` is empty for that whole lesson.
- **`<part label>` is designed and unused.** `t3-w09`'s three questions are her `(a)`,
  `(b)`, `(c)` sub-parts of one question, and the drafter put the markers in the text
  instead. The guarantee that an answer's labels follow its question's is documented but
  not yet realised.
- **The schema has no nesting.** `t3-w04-03`'s `##### Properties` is a subsection of
  `#### Pyramids` in her document and a sibling region here, because a region is flat.
  The frozen decomposition made the same choice, so nothing is lost — but the model is
  coarser than her file.

### The reading ledger, closed

Every population is now read as a file, with each claim put beside the source it makes a
claim about — and, where the claim is about a drawing, the drawing compiled and looked at.

| population | read | what it cost |
| --- | ---: | --- |
| the six documents | 6/6 | researcher commentary filed as the teacher's prose; two core steps whose `content` is their own title; t3-w06 has no evaluation step |
| note files | 20/20, 39,030 chars | two captions describing the wrong drawing |
| figures | 38/38 | 21 unlabelled, now named; fig-08 and fig-14 redrawn |
| heading verdicts | 45/45 | all confirmed; recorded in `note_headings.json` with the reason |
| `sets_work` verdicts | 18/18 | five cite the block, so they are not independent of it |

**Four caption errors across 38 figures, and not one was machine-catchable.** `validate`
checks that a label sits above the drawing it names; it cannot check what the label says.
Two were mine — fig-09 called arrowheads ticks, written off a 110dpi render — and two were
pre-existing and had survived a declared correction pass: fig-03's parallelogram had its
arrow convention inverted, and fig-02 put the set square's right angle on an edge "rising"
from a square drawn entirely below the line.

**A second signal fell out of the reading.** The four regions that set work are exactly the
four containing a task with no working. Every other task-shaped region — all 21 worked
examples, including the ten imperative "Calculate the perimeter of…" headings — ends in its
own answer. So her heading vocabulary and the absence of working agree on all four,
independently.

**Role and content agree on 44 of 47 headings.** The three that part are all
`t3-w05-03`, where she headed a worked example by its topic — `Volume of cube` is Example 3
entire. Both roles feed the same channel, so nothing about the C1 boundary turns on it, and
the three are pinned in the tests with the reason rather than quietly reconciled.

### Nothing decides by pattern

Four regexes in this code were *resolving* a fact about her document rather than locating
one, and each is now a reading:

| was | is |
| --- | --- |
| `re.compile("activity", re.I)` deciding whether a heading set work | `note_headings.json` — all 45 headings, read, three of them work |
| a pattern finding the solution marker | `<section solution="**Solution.**">`, her marker verbatim |
| `^\d+[.)]\s+` stripping a heading's number | `<section enumerator="1.">`, declared |
| labels paired to drawings by position | `<figure>` per drawing, and the loader checks each label sits above the drawing it names |

Heading addressing is a literal line comparison now — a heading is her line with the
hashes taken off — so there is nothing to escape and the drafter and the loader cannot
disagree about where a region begins. `lesson_document`, `lesson_plan_projection`,
`lesson_selections` and `lesson_delivery` import `re` **zero** times between them; the
one survivor is in the drafter, wrapping attributes of the XML it just generated.

The delivery probe is checked rather than assumed: it takes one of her sentences and
confirms it occurs exactly once in the note it came from, so finding it in a request
means that region's text is in that request.

Every count above is unchanged by the removal — the same 27 format changes, the same 11
disagreements, the same 22 worked examples reproduced. That is the evidence the read
verdicts say what the patterns said, on the one corpus where both can be compared.


### What migrating surfaced

**21 drawings with no `**fig-NN.**` label — now closed.** `<figure>` is declared per
drawing whether or not she labelled it, so `validate` reported the gap instead of
`figures_in_text` returning `caption: None` and nobody counting. All 21 have been fixed by
hand, file by file:

- **11 labels.** Each drawing already carried a description of what is marked on it — *"A
  pentagonal based pyramid. The base is drawn as a pentagon standing on one side with its
  fifth vertex uppermost…"*. Only the label was missing.
- **10 descriptions**, all on `t3-w02-04`, where six drawings sat directly under their
  problem heading and four under a `**Solution**` marker. Each TikZ was compiled with
  `pdflatex`, the rendered figure read, and the caption written from what it shows.

`validate` now reports no gap on any lesson and the corpus is **38 of 38 named**. Each
edit is declared in `DECLARED_ADDITIONS`, which is what caught them: the additions guard
failed on all five files the moment the captions went in, by name and without a
blocklist.

This changes what C2 and C3 read — `t3-w02`'s evidence grows 1,390 characters (**+10.3%**)
and `t3-w04`'s 84 (+1.8%) — so those two lessons need regenerating before a human rater
sees a packet. That was already the reason the item was open.

**A bug in the migration's own regex.** Her solution markers have four spellings across
the corpus — `**Solution**` ×17, `Solution:` ×3, `Solution` ×1, `**Solution.**` ×1 — and
the first version knew three of them. The one it missed is a single example on t3-w02,
found because the projection disagreed with the frozen block that got it right. Counted
now, not remembered.

---

## Switching the source of truth

`eval_set.json` can now be frozen from the documents:

```bash
cd apps/backend && uv run python -m experiments.h1_condition_eval.dataset --from-documents
```

This is deliberately not a judgement call. `test_lesson_document` builds every H1 request
twice — once from the documents, once from the transcripts with `clean_plan` applied,
which is what the runner actually feeds — and asserts they are identical: **24 of 24,
six lessons across C0–C3.** The eleven disagreements are duplicates the format drops and
decompositions the transcription lost, and none of them reaches a condition.

What re-freezing costs is a **generation run**, not a decision — and two lessons need one
regardless, because labelling their figures added 1,390 and 84 characters of evidence.
