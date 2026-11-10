# Running generation through the DeepSeek Harness

An agent harness as a generator arm: the model is given a workspace and tools
rather than a single structured call. Kept here, in this repository, and loaded
into the **stock** runtime — nothing is forked, compiled, or vendored.

```
apps/backend/experiments/h1_condition_eval/dsh-harness/
├── adapters/
│   ├── bedrock-mantle.mjs   the adapter (plain JS, never built)
│   ├── package.json         its two dependencies, pinned to the runtime version
│   └── node_modules/        gitignored
├── mantle.cordis.yml        our composition; names the adapter by relative path
├── task.md                  what the agent is asked for, and the output contract
├── sections.rng             the grammar the output must satisfy
├── check_sections.py        copied into the workspace; the agent's own check
└── README.md
```

The SDK is a declared dependency, in its own group so it stays out of the API
and worker closure:

```sh
uv add --group harness deepseek-harness-sdk
```

## Why an adapter at all

`dsh-llm-deepseek`, the shipped adapter, cannot talk to Bedrock mantle. Its SSE
parser requires a literal `data: [DONE]` and raises `STREAM_CLOSED` without one.
That is deliberate, not a bug: without a terminal sentinel a connection dropped
mid-response is indistinguishable from a complete one.

Mantle never sends it. Verified on the wire — the last event carries
`finish_reason` and the socket closes:

```
data: {"choices":[{"delta":{},"finish_reason":"stop",...}],...}
<EOF>
```

So `bedrock-mantle.mjs` uses `finish_reason` as the end-of-stream marker and
**keeps the truncation check** in the weaker form the transport allows: EOF
having seen no `finish_reason` is still an error. A silently truncated
generation would score as a bad pack rather than a failed run, which is the
failure mode this study can least afford.

## Why it lives here and not in the harness repo

Three properties of the shipped runtime were tested against the pip-installed
binary before this was written, because the answer decides the whole shape:

| question | answer |
| --- | --- |
| Will the packaged exe mount a plugin named by absolute path in `cordis.yml`? | **yes** |
| Can such a plugin import the harness's own modules? | **no** — the closure is sealed, Node built-ins only |
| Can it register using its OWN copy of `@deepseek-ai/dsh-llm`? | **yes** — `registerAdapter` duck-types |

The third is what makes this work. `@deepseek-ai/dsh-llm` is published at the
exact version the bundled runtime uses, so `adapters/` installs its own copy and
registers against the runtime's `ctx.llm` without a rebuild.

**Keep those two versions equal.** If `deepseek-harness-runtime-bin` moves, move
`@deepseek-ai/dsh-llm` in `adapters/package.json` with it:

```sh
uv run python -c "import importlib.metadata as m; print(m.version('deepseek-harness-runtime-bin'))"
node -p "require('./adapters/node_modules/@deepseek-ai/dsh-llm/package.json').version"
```

The alternative — forking the adapter into the harness source and rebuilding the
runtime — was tried and rejected. It produces a compiled binary per target
platform (macOS arm64 for development, Linux x64 for the VPS), rebuilt on every
harness upgrade, version-locked to a release candidate. This route deploys as
plain files.

`repos/deepseek-harness` is a read-only clone for consulting the reference
implementation and the `StreamChunk` contract. It is gitignored and nothing here
depends on it.

## Running it

`mantle.cordis.yml` names the adapter by a path relative to itself, so the
composition works from any checkout with nothing injected. Only the endpoint
comes from the environment:

```python
os.environ["BEDROCK_MANTLE_BASE_URL"] = conn["api_base"]
os.environ["BEDROCK_MANTLE_API_KEY"] = conn["api_key"]

with DeepSeekHarness(
    provider="bedrock-mantle",
    model="openai.gpt-oss-120b",
    cwd=str(workspace),
    session_root=str(sessions),
    cordis=str(HERE / "mantle.cordis.yml"),
) as harness:
    result = harness.run(task, session_id=...)
```

`conn` comes from `app.infra.dspy_lm.custom_endpoint("generator")`, so the
harness and the DSPy path resolve the same endpoint from the same declaration
and cannot drift.

DeepSeek's own platform needs no adapter — `provider="deepseek-official"`,
`base_url="https://api.deepseek.com/v1"` works with the shipped composition,
because that endpoint does send `[DONE]`.

## What this is for, and what it is not

It is a **generator arm**: a candidate answer to "does a stronger harness use
the lesson plan better?" (issue #180). Holding the model fixed at
`openai.gpt-oss-120b` is the point — the existing `clean-six` generation used
that model, so a harness comparison against it changes one variable rather than
two. That is the only reason this adapter exists; DeepSeek's platform would
otherwise have done.

It is **not** a fix for the treatment definition. A harness executes C1; it does
not define it. Where C1 hands a unit an objective, a position and a list of
assessment questions, no harness recovers teaching that the plan never recorded.

## Output shape: `sections.xml`

**The raters never see a file.** `rater_packets.build()` reads `sections_json`
from `run.json` and renders the packet from it, so the pipeline's currency is
structured sections — `title`, `blocks[].text`, and
`practice[].{prompt, answer, worked_solution}`. A free-form `pack.md` cannot
enter the pipeline at all.

`task.md` therefore asks for that structure. It asks for it as **XML, not JSON**,
and the reason is the maths.

### JSON was tried and failed on the first attempt

Asked for `sections.json`, the agent wrote LaTeX with single backslashes:

```
\[ d = 2r = 2 \times 5\,\text{cm} = 10\,\text{cm} \]
```

JSON requires every one of those doubled. The file was unparseable — the same
defect as issue #162, *"LaTeX commands written with one backslash are eaten by
the JSON parse"*, arriving by a new route. The task's own validation step did
not catch it.

**DSPy is not immune to this, and its version is worse.** The DSPy model also
authors JSON — the ChatAdapter prompt says *"the value you produce must adhere to
the JSON schema"* and `parse_value` validates the string it wrote. Issue #162
records that path hitting the same defect **23 times across two runs**, and
failing silently rather than loudly: `\t` is a VALID JSON escape, so `\times`
parses cleanly into a tab plus `imes`, and two blinded judges marked packs down
for the garbled maths without knowing the cause.

So the difference between the arms is recovery, not immunity — dspy retries a
parse failure, and a valid-but-wrong escape is not a parse failure. Here the
agent's JSON attempt at least failed loudly.

### XML inverts which characters are dangerous

JSON makes the *most common* character in this content hazardous. XML makes only
`<` and `&` hazardous, and neither appears anywhere in the corpus.

The same lesson, regenerated against the XML contract:

| | JSON | XML |
| --- | --- | --- |
| raw LaTeX sequences carried | failed on the first bad escape | **65** |
| escaping required | every backslash doubled | **none — zero entities used** |
| parses | no | **yes** |
| `prompt`/`answer` kept separate | n/a | yes, 0 leaks |

There is project precedent: `lessons/*.xml` already carries
`\begin{tikzpicture}`, `\draw`, `\frac` and `\mathrm` raw, with no CDATA and
no escaping, and is parsed on every run by `lesson_document.py`.

`prompt` and `answer` remain separate elements. That is load-bearing: the
renderer places questions in the pack and collects answers into "Check your
work" at the end, and its own comment records what happened when placement was
left to the model — *"the answer sat under its own question in 9 of 12
lesson/condition cells and the raters marked it down for defeating
self-testing."*

### Validated twice, and only one of them is the gate

XML makes the failure gentler, not impossible: a bare `<` in "if x &lt; 5" still
breaks the parse. So the pack is checked in two places, and they are not
redundant.

**In the workspace — `check_sections.py`.** Copied in beside the task so the
agent can check its own output and repair it before finishing. Standard library
only, no imports from this repository and no lxml, so it cannot fail for reasons
unrelated to the pack. It reports the bare-`<` case with the cause named, since
`<` and `&` are the only characters XML reserves and everything else — every
backslash — is ordinary.

**On ingest — `sections_document.py validate`.** RELAX NG against `sections.rng`,
plus the cross-file checks a grammar cannot make. **This one is the gate.** An
agent that skips its own check, or misreads it, must still not get a bad pack to
a rater — the same reasoning as keeping the truncation check in the adapter.

### Why the shape must be held constant

With both arms emitting the same sections through the same packet builder, the
generator is the only thing that differs. Two different output shapes would
confound harness quality with format — and the format effect above is known to
be worth rubric points.
