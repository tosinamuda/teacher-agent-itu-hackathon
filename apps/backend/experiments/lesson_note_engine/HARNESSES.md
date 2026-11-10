# Harnesses for the content engine's loop (#208)

Checked on 2026-09-27 against each project's source, docs and package registry. "Run here" means it was confirmed by running the adapter against a local stand-in for the OpenAI-compatible endpoint, not against Bedrock.

## What each supports

| | DeepAgents 0.7.7 | OpenCode 1.18.32 | DeepSeek Harness (dsh 0.1.5-rc.3) | pi 0.99.1 |
| --- | --- | --- | --- | --- |
| How Python drives it | In process (LangGraph) | `opencode serve` over HTTP; the PyPI SDK (0.1.0a36, Aug 2025) is stale, so plain httpx | `dsh --profile acp` as a subprocess, over ACP (JSON-RPC on stdio) through the `agent-client-protocol` SDK (run here). The `deepseek-harness-sdk` is prerelease only | Subprocess, JSONL RPC (`pi --mode rpc`); needs Node; no Python SDK |
| MCP over streamable HTTP with an auth header | Only through `langchain-mcp-adapters`, which pins `mcp<2` and calls the 1.x API; unusable with our `mcp` 2.2. The tools are bridged in code instead | Yes, `type: remote` with `headers` (run here) | Yes, `mcpServers` of type `http` with headers on `session/new` (run here) | Yes, since 0.99.0: `mcpServers` in `mcp.json` with a `url` and `headers` whose values name environment variables, and `exposure: direct` to declare the tools to the model (run here) |
| MCP resources | Adapters load them as blobs, not tools | Yes, as `list_mcp_resources` and `read_mcp_resource` tools, only when the server offers resources | Yes, as the same three tools | Not offered; the writer has none |
| Native tool calls on an OpenAI-compatible endpoint | Yes, `ChatOpenAI` (run here) | Yes, `@ai-sdk/openai-compatible` (run here) | Yes, its pi-ai `openai-completions` provider, set in a patch (run here) | Yes, `openai-completions` in `models.json`; untested |
| Only our tools | `excluded_tools` in a harness profile (beta API); `delete` leaks unless named (run here) | Per-agent `permission` `{"*": "deny"}` (run here) | A patch disables its tool rows: shell, files, web, subagents, plans, goals and skills (run here) | `--tools` names the only tools: ours, and `read` when it has skills (run here) |
| Our system prompt only | Yes (run here) | No: it adds a model line and an `<env>` block. A plugin hook replaces the whole prompt (run here) | Yes: `includeHarnessIdentity` and `includeRuntimeContext` off, and the prompt as `personaPrefix` (run here) | `--system-prompt` replaces it, but pi adds the date and its working directory; an extension removes them (run here) |
| Tokens per call | Callback `on_llm_end` (run here) | Per step, `input`/`output`/`reasoning`/`cache` (run here); cached input and reasoning are split out | Per `assistant/message` event in its session log (run here) | Per assistant message, `usage.input` and `usage.output` (run here) |
| Structured final answer | `response_format` (a tool) | `format: json_schema` (a `StructuredOutput` tool) | None. The checker answers through a one-tool MCP server (run here) | None. The checker answers through a one-tool MCP server; the tool ends the run with `terminate: true` (run here) |
| Maturity | Stable package; profiles are beta | Stable releases, weekly | Developer preview. Its telemetry reports to DeepSeek unless it is turned off | Stable; no MCP client |

## Chosen and built

DeepAgents (in process), OpenCode (a server in its own process) and DeepSeek Harness (an ACP agent in its own process) and pi (an RPC agent in its own process). pi connects the run's MCP servers from an `mcp.json` the run writes; a small extension of ours keeps the prompt, confines `read`, and stops the run.

All three adapters change only the loop. The system prompt is the DSPy signature's own instructions, the message is the same inputs with the skills pinned in the brief, and the model is offered exactly `add_part`, `revise_part` and `read_draft`. Resources are not offered, since the DSPy writer has none.

## Found while building

- OpenCode reaches the draft through a relay. A draft belongs to whoever started it and the engine starts it as the app, so a separate process cannot work on it as itself. The relay listens on localhost, answers only its bearer token, and forwards each call in the engine's context.
- OpenCode names MCP tools `<server>_<tool>`, so the model sees `engine_add_part`.
- OpenCode 1.18.32 cannot list a session's messages once a prompt asked for structured output: the stored `format` fails to encode (HTTP 400). Steps are read from the event stream instead, as its own `run` command does.
- OpenCode sends `max_tokens` (32,000 unless a model limit is set), `stream: true` and `tool_choice`. DeepAgents sends none of them. It makes an extra title call per session unless the session is opened with a title.
- A local plugin costs OpenCode about 10 s per launch while it installs the plugin's dependencies; a stable private config folder brings a launch back to about 2 s.
- LangChain drops the `title` keywords from a tool's JSON Schema. The part schema itself travels in the brief, unchanged.

## DeepSeek Harness

dsh is driven as the haas project drives it: `dsh --profile acp`, spoken to over ACP. The client is the protocol's own Python SDK, `agent-client-protocol`.

- A patch configures each run. A row's `config` replaces that row's whole config, so the session log's `root` must be given again with its `compression`.
- By default, telemetry goes to `harness-telemetry.deepseeksvc.com`. The patch turns it off. It also turns off session titles, which cost a model call.
- dsh names MCP tools `mcp__<server>__<tool>`, so the model sees `mcp__engine__add_part`.
- dsh asks the client before it runs a tool. The client allows the engine's tools. It refuses requests for files, a terminal or a person's answer.
- dsh has no limit on model calls. It reports context use once after each call, so the client counts those reports and cancels the turn at the DSPy writer's `max_iters`.
- dsh puts `Error: ` before a refusal from the server.
- Like OpenCode, dsh streams, and it sends the model's reasoning back in the history.

## Traced on Bedrock (2026-09-27)

One draft per loop of the tests' two-step lesson, with the lesson-note candidate, on gpt-oss-120b. The traces and reports are on branches `tosin/harness-trace-dspy`, `-deepagents` and `-opencode`. A toy lesson answers what goes over the wire, not how good the notes are.

| | DSPy (ReActV2) | DeepAgents | OpenCode |
| --- | --- | --- | --- |
| Tools on the wire | None: no `tools` field in any of 19 requests; calls written as `[[ ## tool_calls ## ]]` text | Native, exactly our three | Native, exactly our three, prefixed `engine_` |
| Part schema | In the prompt, as text | In the message | In the message |
| Reasoning sent back in history | No | No | Yes, as `reasoning_content` |
| Checker answer | Parsed from text | Through `Verdict` once in four calls; `tool_choice: required` ignored three times | Through `StructuredOutput` every time; once as objects, not strings |
| Rounds, calls | 4, 19 | 2, 9 (cut short, see below) | 4, 19 |
| Tokens (prompt / completion) | 108,512 / 25,792 | 30,622 / 7,713 | 76,894 / 15,177 |
| Seconds | 219 | 48 | 170 |

The traces found three faults in the adapters, fixed since, each with a test:

- A DeepAgents tool call with arguments that are not JSON (a `\(` escape) ended the writer silently, with its revision unsent. It now goes back to the model as a refusal.
- A checker answer outside its schema counted as "no errors": text or nothing where the `Verdict` tool was required, and objects where strings belong. An answer now counts only when it is a list of strings, as text or through the tool. Anything else goes back to the model once, with the reason, and then stops the checker.
- The trace summary read only native tools, so it missed DSPy's schema and text calls. It reads both now.

Found in the engine, on every loop alike, and not changed here: the last round's parts are saved without a check (`RESUMES`); the checker asks the writer to change the plan's `step_kind`, which a part cannot; and it contradicts itself between rounds on where commentary goes.

## Traced on a real lesson (2026-09-29)

One draft per loop of the validation lesson `LPV-STUDY-t2-w09` (5 plan steps), with the lesson-note candidate, on gpt-oss-120b. Cost uses Bedrock's rate for gpt-oss-120b: $0.15 per million prompt tokens and $0.60 per million completion tokens.

| | DSPy (ReActV2) | DeepAgents | OpenCode | DeepSeek Harness |
| --- | --- | --- | --- | --- |
| Rounds, calls | 4, 32 | 4, 55 | 4, 52 | 4, 45 |
| Tokens (prompt / completion) | 257,658 / 40,070 | 660,425 / 69,957 | 708,290 / 73,749 | 525,142 / 53,503 |
| Seconds | 376 | 711 | 798 | 606 |
| Cost | $0.06 | $0.14 | $0.15 | $0.11 |
| Tool calls | Written as text, in 16 calls | Native, in 36 calls | Native, in 48 calls | Native, in 37 calls |
| Reasoning sent back in history | No | No | Yes | Yes |

Every loop used all four rounds: the checker found errors until the last round, and the last round's parts are saved without a check.

The traces found two faults, fixed since, each with a test:

- gpt-oss answered the checker with objects where the `Verdict` schema asks for strings, on every loop's answer channel. On DeepAgents it wrote them as text past the required tool, so DeepAgents' own retry never saw them, and the draft stopped after one round. Each checker now sends a refused answer back once, with the reason. The DeepAgents draft above used it and finished.
- `run.py` and `trace.py` left DSPy's disk cache on. An earlier DSPy trace of this lesson took 5 of its 32 calls from the cache, and a repeated control run would replay its first samples. Both now pin the cache off.

OpenCode fixes an agent's step limit per prompt, so its checker asks again only while it has steps left. The answer it gives then is not capped at the steps left, as DeepAgents' and dsh's are.

## Compared on the test lessons (2026-09-29)

Each loop wrote the first three lessons of `frozen_set_test.json` once (13 steps), with the lesson-note candidate on gpt-oss-120b, and DSPy wrote them twice. Three Sonnet judges ranked, for each of the 8 steps that have a teacher's note, three notes in a blind packet: the teacher's, DSPy's first run and the loop's. Each loop is judged against the same DSPy run, in the same packet, so one judge sees both. The second DSPy run is judged against the first the same way, and is the noise floor. Cost uses Bedrock's rate for gpt-oss-120b.

| | DSPy run 1 | DSPy run 2 | DeepAgents | OpenCode | DeepSeek Harness |
| --- | --- | --- | --- | --- | --- |
| Drafts finished | 3 of 3 | 3 of 3 | 3 of 3 | 3 of 3 | 3 of 3 |
| Rounds, calls | 12, 100 | 12, 86 | 11, 135 | 12, 157 | 12, 142 |
| Tokens (prompt / completion) | 1.29M / 189k | 0.88M / 155k | 2.37M / 234k | 2.59M / 236k | 2.26M / 195k |
| Cost | $0.31 | $0.22 | $0.50 | $0.53 | $0.46 |
| Minutes | 30 | 25 | 43 | 43 | 31 |
| Words in the notes | 2,619 | 2,612 | 3,130 | 3,175 | 3,245 |
| Steps where its note scored higher, lower | | 3, 4 | 6, 2 | 5, 3 | 6, 2 |
| Sign test by step | | p = 1.00 | p = 0.29 | p = 0.73 | p = 0.29 |
| Mean step difference, spread | | -0.18, 0.91 | +0.17, 0.56 | 0.00, 0.63 | +0.31, 0.89 |

The runs are `batch-dspy-a-20260929T073647Z` (DSPy run 1, on all five test lessons), `cmp-deepagents-20260929T084113Z`, `cmp-opencode-20260929T093511Z`, `cmp-dsh-20260929T101832Z` and `cmp-dspy-b-20260929T104934Z`. Each has a `-vs-control` folder with its blind packets, keys and verdicts. The traces of the validation lesson are `trace-*-20260929T*`. DVC versions them: `uv run dvc pull experiments/lesson_note_engine/runs/<folder>.dvc`. Use `compare_harnesses.py report` to print the table again.

The step is the unit. A step's three verdicts are not independent, and a test over the 24 verdicts reads p = 0.035 for DeepAgents and 0.052 for DeepSeek Harness where the steps give 0.29.

- No loop scores differently from DSPy. Two runs of DSPy differ from each other as much: by half a point or more on 5 of 8 steps, and by 0.91 in the spread of step differences. The loops' spreads are 0.56 to 0.89.
- The same DSPy notes scored 3.57, 3.71, 3.87 and 3.94 on average across the four judge panels, so a panel alone moves a mean by 0.37.
- Every loop writes about 20% longer notes than DSPy's first run, and DSPy's second run matches the first in length. Model judges tend to reward longer notes, so a small preference for a loop may be length.
- Every loop costs more than DSPy: 1.7 to 2.0 times the mean of its two runs ($0.27).
- The judges named the teacher's note in 23 or 24 of 24 verdicts in every packet, so they are not blind to it. They did not always prefer it: it ranked first in 15, 7, 9 and 13 of the 24 verdicts of the four packets.
- The comparison reaches only differences of about a point per step. It is one draft per loop, 8 judged steps, three model judges, and three of the five test lessons. The other two were written and judged for DSPy only.

Two faults in the adapters, found while running and fixed with tests, would have decided the comparison:

- The OpenCode checker dropped a verdict the model wrote as text. gpt-oss often writes `{"errors": [...]}` in its reply and does not call the answer tool. OpenCode reports that as a `StructuredOutputError`, and the adapter stopped on it, so 2 of its first 2 drafts failed on a valid verdict. One helper now reads a written verdict on every loop.
- The lesson-note runs left DSPy's disk cache on.

## Decision (2026-09-30)

The engine's production loop is OpenCode. No loop wrote better notes than DSPy within what these comparisons can see, and every loop finished every draft. The choice rests on what a harness supplies and on maturity:

- OpenCode supplies remote MCP with headers, skills with a `skill` tool that loads one on demand, a permission model that denies everything but our tools, and per-step token counts. It reads `.agents/skills`, `.claude/skills` and `.opencode/skills`. It has stable releases.
- DeepAgents has no working MCP client here: its adapter package pins `mcp<2`.
- DeepSeek Harness is a developer preview. Its telemetry reports to DeepSeek unless turned off, and it has no structured answer and no limit on model calls.
- pi has supported MCP since 0.99.0 only. It loads a skill by reading its file, needs Node, and cost the most of the native runs ($0.49).
- OpenCode with native skills was the cheapest native run ($0.43 on three lessons, against $0.22 and $0.31 for DSPy), which is 2.0 times the mean of two DSPy runs.

OpenCode's native notes are 28% shorter than its pinned notes. The margin is inside the noise, and the size of the notes is the thing to watch.

`ENGINE_LOOP` stays DSPy until OpenCode with native skills has written the three test lessons through an installed plugin, with the plugin's skills copied into the workspace, and its cost and notes are judged against the DSPy control. DSPy stays the control.

This comparison switched the harness's own skills, MCP client and hooks off for the runs that compare the loops. `## What a harness supplies` below is what is verified for using them.

## What a harness supplies` below is what is verified so far.

`ENGINE_LOOP` stays DSPy until that is tried.

## What a harness supplies

| | The engine builds it today | DeepAgents 0.7.7 | OpenCode 1.18.32 | DeepSeek Harness 0.1.5-rc.3 | pi 0.99.1 |
| --- | --- | --- | --- | --- | --- |
| Skills | `SKILL.md` files seeded as versioned rows; a type's spec pins a revision, and the whole text of each pinned skill goes into the brief of every model call | `skills=[paths]`: metadata first, the full skill on demand | Finds `SKILL.md` in `.opencode/skills`, `.claude/skills` and `.agents/skills`; the model loads one with its `skill` tool | Finds `SKILL.md` in `<project>/.agents/skills` (run here); it also scans `~/.agents/skills` | Finds `SKILL.md` in `.agents/skills` from its working directory, and lists them in its prompt; the model loads one by reading the file with `read` (run here) |
| MCP client | The engine's own `/mcp` server; its `skills://` and `skill://` resources serve the skills | Adapter package pins `mcp<2`, so the tools are bridged in code | Remote server with headers, natively | `mcpServers` of type `http` with headers, natively | Yes, since 0.99.0: `mcp.json`, tools named `mcp__<server>__<tool>`; resource tools when a server offers resources |
| Hooks | Middleware and callbacks written in each adapter: model-call cap, token log, refusal of unreadable calls | LangChain middleware | Plugin hooks such as `tool.execute.before` and `tool.execute.after` | Runs a Claude Code `hooks.json`: SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop | Extension events in TypeScript: `tool_call` can block a call and `tool_result` can change one (run here: `read` is blocked outside the skills), `turn_start` can abort (run here: the model-call budget) |

What the adapters had to build anyway:

- A relay, because the engine starts a draft as the app and a harness in another process cannot open it as itself.
- A cap on model calls and a token log for each loop.
- A retry of a refused verdict, and a reader of a verdict written as text.
- A patch that turns off each harness's own tools, and a prompt that replaces its own.

The six pinned skills are 4,398 of the 20,730 characters of the first writer call (21%). The lesson is 11,406 (55%). A harness that loads a skill on demand would send at most that fifth less, and would leave the choice of which skill to the model. That changes the note and needs its own comparison.

## Native skills (2026-09-29)

`--skills native` (run.py, trace.py) writes the type's pinned skills as `SKILL.md` files under `.agents/skills` in a workspace of the run's own, and starts OpenCode, DeepSeek Harness or pi there. The run reads the skills from the engine's server at their pinned revision before it starts the harness. The brief then carries no skill text, and the relay leaves the skills out of every tool result, so the only way the text reaches the model is the harness's own loader. The writer's prompt tells the model to load a skill before it writes a part the skill applies to. The run's log records each skill file's hash. The checker still gets the pinned skills in its brief. DSPy and DeepAgents refuse the flag.

Found while building:

- OpenCode lists the skills in the system prompt, and the prompt plugin that replaces that prompt removed the list, so no skill was offered. The plugin now keeps the list.
- OpenCode lists a skill of its own, `customize-opencode`. A permission hides it.
- DeepSeek Harness also scans `~/.agents/skills`: on the first run 21 of the developer's own skills reached the model. Its agents home is now the run's own directory.
- A verdict on the last allowed model call of a DeepSeek Harness turn was lost: the agent reports a call before it runs that call's tools, and the turn was cancelled between the two. The turn now ends once the last call's tools have finished.
- `read_draft` returns the draft's brief, and the brief carries the skills' text. The relay now removes it in native mode. On a real lesson the text then reaches the model only in the `skill` tool's result.
- pi (0.99.1) has no `skill` tool: it loads a skill by reading its file, and its extension blocks a `read` outside the skills. Since 0.99.0 it loads a project's skills only when the project is trusted, and a run has no one to ask, so the command line passes `--approve`. OpenCode reads reference files under the same limit. DeepSeek Harness has no tool to read them.

## Native skills on the test lessons (2026-09-29)

OpenCode, DeepSeek Harness and pi each wrote the first three test lessons once with `--skills native`, and three Sonnet judges scored each run's notes against the DSPy control's and the teacher's, blind, as in the comparison above. Each pairing has its own judges, so the scores of different rows are not comparable; the margin of the run's engine note over the control's is. The step is the unit: 8 steps.

| Run | Finished | Steps higher / lower | Margin over the control | Notes (words) | Prompt tokens | Calls | Cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DSPy, second run (the noise floor) | 3/3 | 3 / 4 | −0.18 | 2,612 | 0.88M | 86 | $0.22 |
| OpenCode, pinned | 3/3 | 5 / 3 | 0.00 | 3,175 | 2.59M | 157 | $0.53 |
| OpenCode, native | 3/3 | 3 / 5 | −0.14 | 2,281 | 2.15M | 157 | $0.43 |
| DeepSeek Harness, pinned | 3/3 | 6 / 2 | +0.31 | 3,245 | 2.26M | 142 | $0.46 |
| DeepSeek Harness, native | 3/3 | 2 / 5 (one equal) | −0.18 | 2,675 | 2.16M | 173 | $0.44 |
| pi, native | 3/3 | 4 / 4 | +0.01 | 3,296 | 2.36M | 162 | $0.49 |

- Every draft finished in 4 rounds. No native run failed.
- Every margin lies within 0.31 of the control, and the native margins lie inside the spread of the two DSPy runs and the pinned runs. Native skills do not measurably change the note's quality.
- Native skills cost 19% less than pinned on OpenCode and 4% less on DeepSeek Harness, which made 31 more calls. The pinned skills are 21% of the first call. A run still costs 2.0 to 2.2 times a DSPy run.
- OpenCode's native notes are 28% shorter than its pinned notes, and shorter than the control's. Judges tend to reward length.
- One run of each, on three lessons, with judges who name the teacher's note: this bounds a difference and cannot show a small one.

## OpenCode native through an installed plugin (2026-09-30)

OpenCode 1.18.32 wrote the first three test lessons (13 steps) with native skills through the installed lesson note plugin, with the plugin's skill files copied into the workspace as installed. Three Sonnet judges scored each run blind against the DSPy control (`batch-dspy-a-20260929T073647Z`), as above. The control's engine score differs by pairing, since each has its own judges.

| Plugin | Steps higher / lower | Sign test by step | Engine score, control's | Weakest: `states_content` | Words | Calls | Cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Six skills | 2 / 6 | p = 0.289 | 3.65, 3.97 | 3.79, 4.46 | 2,650 | 157 | $0.40 |
| One skill, `read` not offered | 0 / 8 | p = 0.008 | 3.38, 3.99 | 2.62, 4.25 | 2,141 | 148 | $0.37 |
| One skill, `read` offered | 2 / 5 (one equal) | p = 0.453 | 3.49, 3.77 | 3.46, 4.25 | 2,579 | 170 | $0.47 |
| One skill, four rules in `SKILL.md` | 3 / 5 | p = 0.727 | 3.81, 3.88 | 4.46, 4.38 | 2,015 | 133 | $0.30 |

What the traces of one draft showed:

- Six skills: the model loaded 3 of the 6 from their descriptions (`matching-content-to-step-type`, `creating-learning-content-from-teacher-provided-material`, `drawing-lesson-figures`). It never loaded `writing-pupil-facing-content`, `showing-worked-solutions` or `using-classroom-context`.
- One skill, `read` not offered: the model loaded `create-lesson-note` and could not open its reference files. The adapter offered `read` only when a skill had stored reference files, and a skill copied from a plugin keeps them elsewhere. The adapter now counts both.
- One skill, `read` offered: the model loaded the skill and read `teacher-material.md` and `step-types.md` three times each, `figures.md` twice and `pupil-facing-content.md` once. It never read `worked-solutions.md` or `classroom-context.md`.

With the four rules that apply to every part in `SKILL.md` (the teacher's material, the step types, writing for the pupils and the classroom), and only `figures.md` and `worked-solutions.md` left as reference files, the last row is the closest to the control of any OpenCode run: the engine's score is 0.07 below, `states_content` is above it, and the run cost the same as the control ($0.30 against $0.31) in 20 minutes against 30. Limits:

- The judged difference lies inside the noise of the comparison: one run, 8 judged steps, three judges, and a panel moves a mean by about 0.37.
- The run's notes are 23% shorter than the control's (2,015 words against 2,619), and `fit` is below it (3.38 against 3.71).
- The cost is not stable run to run: four runs of this harness with this plugin, in different layouts, cost $0.30 to $0.47.
- The model made 133 calls against the control's 100.

Always-applicable rules held in reference files depend on the model choosing to read them, so rules that apply to every part belong in `SKILL.md`, and the reference files hold what only some parts need.

The condition for changing the default is met: OpenCode with native skills wrote the three test lessons through an installed plugin, with the plugin's skills copied into the workspace, and its notes and cost are within the noise of the DSPy control's. `ENGINE_LOOP` is OpenCode with native skills (#245), and the ansible `opencode` role installs release 1.18.32 on the server. DSPy stays the control for experiments.
