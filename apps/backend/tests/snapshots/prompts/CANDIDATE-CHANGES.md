# Candidate prompt changes

Changes the snapshots have made visible, recorded here rather than applied. Sprint 14 is
diagnosis: a prompt edit made mid-investigation would be measured against a different
system than the one that produced the H1a null, and H1a is preregistered against a frozen
set. Each entry below waits on two gates.

**Gate 1 — PROMPT-001D.** The documented path from snapshot diff to a run over the frozen
eval set, compared on a metric with known variance. Recall carries sd .041; findings-count
moved sd 2.03 on a mean of 1.53 across identical draws and cannot be compared on. A judged
margin under 0.5 is inside the re-rate noise floor and is not a finding.

**Gate 2 — PROMPT-002B.** What the pipeline actually loaded for the frozen cohort, C0 vs C1
explicit. Everything below was found against the synthetic fixture. If C1's fields arrived
empty or identical to C0's for the real learners, wording was never the cause, and a
reworded prompt that scored better could not be told apart from the data fix.

Nothing here is applied. Adding an entry costs nothing; applying one costs a frozen-eval
run and a defence in the thesis.

---

## CAND-1 — Say what is being made, in words the model has priors for

**Status:** proposed · **Arms touched:** all six · **Found by:** reading `C1.md`

The objective opens by pointing at a field rather than naming the thing:

> Write one section of the artefact described in artefact_spec, for its audience.

Both nouns are indirections; the model resolves "the artefact" only after reading another
field. What that field then says is concrete — `"one section of a take-home revision pack"`
for `"a junior secondary student aged about 11-13 who sat in this lesson and is revising
alone at home"` — so the information exists, just not in the sentence that frames the task.

`artefact` is also internal domain vocabulary. It is the right word in the tree and the
wrong word in a prompt: a generic build noun where "learning material" and "revision pack"
carry teaching priors. The value is already built by a function named `revision_pack_spec`
and handed over as `artefact_spec`, so the factory uses the product noun and only the
model-facing name does not.

**Proposed:** rename the model-facing fields to `learning_material_type` and
`learning_material_guideline`, and open with the noun rather than the pointer.

**Four render sites, one edit each — a pydantic alias covers only the last:**

| Site | × | Driven by |
| --- | --- | --- |
| `1. \`artefact_spec\` (…)`, `[[ ## artefact_spec ## ]]` ×2 | 3 | the DSPy signature field name — rename the attribute, and the matching key in `prompt_projection.py` |
| `(ArtefactSpec)` | 1 | the pydantic class name, printed as the annotation |
| task line ×2, `Follow every requirement in artefact_spec`, and 3 in the codebook | 6 | docstring prose |
| `{"artefact": "one section of a take-home revision pack", …}` | 1 | a field inside the value |

`ReviewPackRequest.artefact_spec` and the whole artefact domain vocabulary
(`artefact_id`, `artefact_type`, the census rows) stay as they are: `shared_inputs` in
`prompt_projection.py` is the seam, and mapping a domain attribute to a model-visible key
is the job that module already has.

**Not proposed:** a persona ("you are a teacher…"). `audience` pins the reader harder than
a persona would, and a second source of register could contradict it.

---

## CAND-2 — Type the two dicts that carry the whole manipulation

**Status:** proposed · **Arms touched:** all six · **Found by:** measuring the docstring

`lesson_context` and `unit_context` are annotated `dict`, so DSPy emits no schema for
them — contrast `ArtefactSpec` and the `DraftSection` output, which get full JSON schemas.
The two fields that carry the entire C0/C1 manipulation are described in 55 and 180
characters, and the per-key guidance had nowhere to go but the docstring:

| | lines | chars |
| --- | --- | --- |
| Docstring: task statement | 7 | 424 |
| Docstring: `LESSON_PLAN_FIELD_CONTRACT` | 49 | 2459 |
| All five `InputField` descriptions combined | — | 436 |

Typing them as pydantic models would move each key's paragraph to where DSPy renders it
beside the value, make absence explicit in a schema rather than a silently missing key, and
take ~2.5KB out of the instruction block an optimizer would later have to evolve around.

**Interacts with a deliberate design choice.** The codebook is constant across arms so that
instructional-design prose cannot explain a C1 advantage; C0 reads all 49 lines and
receives none of the six fields. Typing the dicts is the way to cut C0's dilution without
reintroducing that confound — but it changes what every arm reads, so it needs the full
comparison.

---

## CAND-3 — Smaller items, same gates

- **The task statement is buried.** It sits at lines 34-40 of a 91-line system message,
  after the input list, the field template and a ~2.5KB inline output schema, introduced by
  `In adhering to this structure, your objective is: ` and indented 8 spaces by the adapter.
  The indent is DSPy's, not ours — the stored instructions are flush-left.
- **`policy` is thin and partly redundant in C0/C1.** It renders as two booleans announcing
  what is *not* required plus an `instruction_summary` of "Generate the section from the
  context supplied for this unit.", which says nothing the docstring has not.
- **Sibling-section blindness.** The codebook says "assume what precedes it, leave what
  follows to its own section", but sections are independent concurrent calls and no field
  carries what any sibling wrote. The model can bound its scope from the ordered objective
  list; it cannot avoid duplicating content.
- **Cosmetic, in every call:** a trailing space after `your objective is: `, and
  `reasoning (str):` renders with an empty description.

---

## Recorded, not a candidate

**C2 and C3 send byte-identical prompts.** The only difference between `C2.md` and `C3.md`
is the header line naming the condition. C3's entire difference is the post-generation
validate-and-repair loop, so nothing that separates C3 from C2 is a prompt change at all.
