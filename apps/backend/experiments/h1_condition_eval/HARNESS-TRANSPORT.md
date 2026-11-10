# What actually works: endpoint, adapter, tool channel, output contract

Every row measured against the live API on 2026-08-24, and every configuration column
captured off the wire rather than read from a docstring. The facts were previously spread
across `llm_models.py`, `dspy_lm.py`, two findings and a decision record, and one of those
was wrong.

## The configuration matrix, as the code builds it

| model | endpoint | adapter | tools sent | output contract |
|---|---|---|---|---|
| **deepseek-v4-flash** | **`/responses`** | **JSONAdapter** | **native** | **json_schema** |
| deepseek-v4-flash | chat | JSONAdapter | native | a pydantic schema — **400s** |
| deepseek-v4-flash | chat | ChatAdapter | none | field markers |
| **gpt-oss-120b** | **chat** | **ChatAdapter** | **none** | **field markers** |
| gpt-oss-120b | chat | JSONAdapter | none | json_object, then dropped |

**Bold rows are what the study runs.** The others are reachable and recorded so nobody
has to rediscover why they were not taken.

## What the endpoints will and will not do

| | DeepSeek `/v1/chat/completions` | DeepSeek `/responses` | mantle `/v1/chat/completions` | mantle `/v1/responses` |
|---|---|---|---|---|
| `json_object` | 200, valid JSON | — | 200, valid conforming JSON | **200 in 1.0s, PROSE — ignored** |
| `json_schema` | **400** `"This response_format type is unavailable now"` | **200, enforced** — flat and nested alike | 200, then ```json fences that do not parse | **HANGS** — 100s against a 1.1s control |
| native `tools` | — | **200, `function_call{name, arguments}`** | — | **200, `function_call`** |

Two things this settles that were previously guessed:

* DeepSeek's rejection of `response_format` is **endpoint-shaped, not schema-shaped**. The
  old note said a small schema passes and a nested one does not. Neither passes on chat;
  both are enforced on `/responses`, including one shaped like a real section.
* **Mantle does serve `/responses`.** A finding claimed it did not, and used that to excuse
  a transport confound. It does, and gpt-oss does native tool calls there — but its
  structured output is broken, so going there would trade a working contract for a broken
  one.

## The tool channel, and the gate nobody had checked

`ReActV2` asks for the turn as a `tool_calls` field. Whether that arrives as a **native
tool call** or as **text the model must format** is decided by one flag:

    lm.supports_function_calling

litellm answers that from its own model registry, and **our ids are not in it** —
`openai/deepseek-v4-flash`, `openai/openai.gpt-oss-120b`. dspy's adapter gates the `tools`
list on exactly that flag, so it dropped the list rather than sending it, silently, always.

So **every tool call this project made before 2026-08-24 was text**: `[[ ## tool_calls ## ]]`
parsed out of prose under ChatAdapter, a `tool_calls` field inside a JSON object under
JSONAdapter. A text channel is one a model can wander off, and DeepSeek wanders into its
own `<|DSML|tool_calls>` markup.

`_declare_native_tools` in `dspy_lm.py` registers the capability for models that declare
`supports_native_tools`. **DeepSeek only.** gpt-oss stays unregistered: it has produced no
parse failure in 306 loops, and changing the study's own generator to fix a problem it does
not have would invalidate every recorded comparison.

## Sampling and reasoning, as configured today

Captured off the wire, DeepSeek on `/responses`:

| parameter | value | why |
|---|---|---|
| `temperature` | **0.0** | pinned per run, not left to a provider default |
| `cache` | **`{no-cache, no-store}`** | dspy caches to disk by default; in an experiment that replays the first sample and a stochastic arm reports as perfectly reproducible |
| `max_tokens` | **not sent** | see below — naming a number made things worse |
| `reasoning` | **not sent** | no `effort`, no cap; the provider default is what runs |
| `timeout` | 300s | one call, not a whole loop |
| `num_retries` | 8 | rate limits only |

Three draws per cell is what makes a run stochastic. Temperature 0 does not make it
deterministic — the provider still varies — which is why the noise floor is measured from
re-draws rather than assumed to be zero.

## The reasoning budget, and a fix that made it worse

On `/responses`, **reasoning and answer are billed from the same budget**. Chat completions
returns no `reasoning_content` at all, so nothing needed a ceiling before. Left to the
provider default, a hard section can be reasoned about until nothing is left to answer
with, and the turn returns `text: None` and is abandoned.

The obvious fix was an explicit ceiling. It made things **seven times worse**:

| output ceiling | loops | abandoned |
|---|---|---:|
| none — provider default | 102 | **1** |
| `max_tokens = 8000` | 95 | **7** |

Every one of the seven was *"the LM returned an empty or null response"*. **Reasoning
expands to fill whatever budget it is given**, and the provider's own default is larger
than anything worth naming, so a ceiling tightens the budget rather than protecting it.
Reverted. Do not add one back without measuring the default first.

`max_tokens` does reach the wire correctly — litellm translates it to `max_output_tokens`,
verified — so the failure was the value, not the plumbing.

### What the reasoning controls actually do

Single probes against the live API, one prompt, DeepSeek `/responses`:

| setting | budget | reasoning | text |
|---|---|---:|---:|
| default | 600 | 189 ch | 248 ch ✓ |
| `effort: none` | 600 | **0** | 573 ch ✓ |
| `effort: minimal` | 600 | 1,292 ch | 488 ch ✓ |
| **`effort: low`** | 600 | 2,400 ch | **0 — the failure** |
| default | 8000 | 2,250 ch | 5,358 ch ✓ |
| **`reasoning.max_output_tokens: 1500`** | 8000 | **10,410 ch** | 5,330 ch |
| `effort: none` | 8000 | 0 | 6,570 ch ✓ |

Two things worth knowing before reaching for these:

* **`reasoning.max_output_tokens` is not honoured.** Asked for 1,500 it produced 10,410
  characters of reasoning. It is in DeepSeek's documented schema; it did not bind.
* **`effort: none` is the only reliable control**, and it removes reasoning entirely rather
  than bounding it. That is a change to how the model works, not a guard rail, so it is not
  set — the abandonment it would prevent now runs at 0 in 153 loops with native tools.

The failure these were chasing turned out not to be a budget problem at all. It was our own
tool contract and the text tool channel; once both were fixed, abandonment went to zero with
no reasoning parameter set.

## What it cost to find out, in order

| harness | loops | abandoned | DSML markup |
|---|---:|---:|---:|
| chat, ChatAdapter | 102 | 1 | — |
| + an 8,000-token output ceiling | 95 | **7** | — |
| `/responses`, JSONAdapter | 102 | 1 | 16 |
| + handle addressing | 151 | 2 | 16 |
| **+ native function calling** | **153** | **0** | **0** |

Three faults, each hiding the next: a **missing newline** before a field marker; **our own
id contract**, where `add_practice` returned an id `revise_practice` rejected; and the
**text tool channel** itself. Plus one fix reverted — the output ceiling made abandonment
seven times worse, because reasoning expands to fill whatever budget it is given and the
provider default is larger than anything worth naming.

## ReAct against ReActV2

`ReActV2` is what the study runs, and the reason predates all of this: its predecessor
parses tool calls out of prompt text and produced 5 duds in 6 against 0 in 6 for `ReActV2`
(`HARNESS-DECISION.md`, arm `compose-v2`).

But note what that decision record claims and what is true. It says "native tool calling,
not prompt-parsed". `ReActV2` **models** the turn as a typed `tool_calls` field, which is
the improvement over parsing free prose. It does not follow that the call travels
natively — that needs `supports_function_calling`, and for gpt-oss it is still False. The
study's generator parses its tool calls out of text to this day.

## The rule this keeps proving

An endpoint's capability and the code path's behaviour are different questions, and this
project has answered the easy one four times: `/responses` returns a native `function_call`
but dspy never asked; `json_object` works on DeepSeek chat but `json_schema` 400s;
`json_object` works on mantle chat and is ignored on mantle `/responses`; mantle was said
not to serve `/responses` without anyone calling it.

Test the path the code takes, not the endpoint.
