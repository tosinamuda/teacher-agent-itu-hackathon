# Every tool call this project made was text, and nobody had checked

2026-08-24. Five DeepSeek runs over the same six lessons, each one changing a single
thing about how a tool call travels.

| harness | loops | abandoned | DSML markup |
|---|---:|---:|---:|
| chat completions, ChatAdapter | 102 | 1 | — |
| + 8,000-token output ceiling | 95 | **7** | — |
| `/responses`, JSONAdapter | 102 | 1 | 16 |
| + handle addressing | 151 | 2 | 16 |
| **+ native function calling** | **153** | **0** | **0** |

## What was actually wrong

`lm.supports_function_calling` is **False for every model in this project**. litellm reads
it from its own registry and our ids are not in it — `openai/deepseek-v4-flash`,
`openai/openai.gpt-oss-120b`. dspy's adapter gates the `tools` list on exactly that flag,
so it dropped it rather than sending it, silently, always.

So every tool call ever made here was **text**: `[[ ## tool_calls ## ]]` parsed out of
prose under ChatAdapter, a `tool_calls` field inside a JSON object under JSONAdapter. A
text channel is one a model can wander off, and DeepSeek wanders into its own
`<|DSML|tool_calls>` markup — 16 times in one run, twice fatally.

Declaring the capability per model, and registering it with litellm, sends real tools and
closes the class: **16 DSML occurrences to 0, and abandonment with them.**

## Three separate faults, found in order, each hiding the next

**A missing newline.** ChatAdapter anchors its field-marker regex at line start
(`field_header_pattern.match(line.strip())`). DeepSeek sometimes writes
`…and submit.[[ ## tool_calls ## ]]` with no break, so the marker is invisible and
`tool_calls` parses as absent. 13 failures in 30 loops, every one recovered by a second
call at the cost of that call. Moving to `/responses` took it to 0.

**Our own id contract.** A unit id is namespaced, so a practice item was
`step:step-t2w09-03:p0` — a leading `step:`, a nested `step-…`, two colons. `add_practice`
returned it; `revise_practice` rejected the obvious reading of it. One loop spent its
entire output budget asking what the id was, called `read_draft`, was told "call
read_draft", and returned nothing. Its reasoning trace is a correct diagnosis of our bug:
*"the returned id can be used for revision. But it didn't."* The tools now address by
`b3` / `p0` — the prefix is identical on every id in a draft, so it distinguished nothing
and existed only to be mistyped.

**The text channel itself**, above.

## A fix that made it worse, kept as a measurement

Reasoning and answer share one budget on `/responses`, where chat completions returned no
reasoning at all. An 8,000-token ceiling was added to leave room for both. It made
abandonment **seven times more likely** — 1 in 102 without, 7 in 102 with, every one "the
LM returned an empty or null response". The provider default is larger, so naming a number
tightened the budget rather than protecting it. Reverted, with the numbers left in the
code so it is not re-added on the same reasoning.

## What this does not touch

**gpt-oss stays on chat completions with ChatAdapter, unregistered.** It has produced no
parse failure in 306 loops. Changing the study's own generator to fix a problem it does
not have would invalidate every recorded comparison for nothing.

So no H1 result moves: the enrichment null, the lesson-by-lesson analysis and the
generator contrast all rest on gpt-oss runs and on the original DeepSeek pair, none of
which are affected.

## The lesson worth keeping

The `/responses` move was justified partly as "the tool call is a native `function_call`
object, so there is no marker to malform". The API does answer that way — measured
directly against it — but **dspy never asked**, so we never saw it. Testing the endpoint
is not testing the path the code takes, and the difference cost three runs to find.
