# Content types

A content type is one kind of lesson content: a lesson plan, a lesson note, a class test, a revision note, or a type a researcher registers.
Each type has a spec: what the content is, who reads it, and what it must do.

## Two engines

| Engine | Types | How content is made |
| --- | --- | --- |
| `builtin` | `lesson-note`, `class-test`, `revision-note` | Each type has its own generator. |
| `builtin` | `lesson-plan` | The content engine drafts it, like an `mcp` type, and saves it as a plan version. |
| `mcp` | Every type registered through the API | The content engine builds it part by part through MCP tools. |

Every type is stored, listed, revised and approved the same way. A teacher approves content in the app before anyone else sees it. A teacher can also reject a pending version, or withdraw an approved one, with `POST /content/{id}/rejections` (`expected_version` and a `reason` of 3 to 500 characters). The status becomes `rejected` and the reason is kept in `review_reason`. A rejected item is not the lesson's class note, so the lesson can take a new one, and revising it returns it to pending. Withdrawing an approved class revision note withdraws the learners' notes made from it. A class test already sent to students is not withdrawn, and a lesson plan is revised, not rejected.

A revision note records beside it the checks its version passed and the passages it was given (`artefact_refs.review`, returned as `review` on `GET /content/{id}`). The native generator and the engine writer's save step both write it, and a teacher's revision rewrites it for the new version. The review page shows the checks, the passages each section cites, and, collapsed, the requirements the note was written to: the app checks some of them, and the teacher reads the note against the rest.

The content engine writes a lesson plan with the same MCP tools as for an `mcp` type. It writes from the curriculum and the textbook, or from a teacher's document. A teacher revises the plan in a chat.

## Register a type

A researcher registers a type with its first spec. A teacher can generate it at once.

```bash
curl -X POST "$API/content/types" \
  -H "x-teacher-code: researcher" -H "content-type: application/json" \
  -d @worked-examples.json
```

`worked-examples.json`:

```json
{
  "type": "worked-examples",
  "label": "Worked examples",
  "audience": "learner",
  "spec": {
    "material": "worked examples for one step of the lesson",
    "audience": "{reader} revising at home",
    "levels": ["class"],
    "requirements": ["Show every step of the working."],
    "unit": "plan_step",
    "parts": [
      {"name": "title", "description": "A heading for the learner", "type": "text"},
      {"name": "examples", "description": "Worked examples, each solved step by step", "type": "items",
       "fields": [
         {"name": "problem", "description": "The problem", "type": "markdown"},
         {"name": "solution", "description": "The working and answer", "type": "markdown"}
       ]}
    ]
  }
}
```

| Spec field | Meaning |
| --- | --- |
| `unit` | What one part covers: `lesson`, `curriculum_objective`, `lesson_objective` or `plan_step`. The content has one part for each unit of the lesson. |
| `parts` | The fields of one part. |
| `lesson_parts` | Optional. The fields of one more part, written once for the whole lesson before the other parts. |
| `levels` | `["class"]`. Content drafted part by part is class level only. |
| `structure` | Optional. The app writes it from `parts` and `lesson_parts` when it is left out. |
| `skills` | Optional. The skills the content is written with, each as `{"skill": slug, "revision": n}`. |
| `mcp` | Optional. The external MCP servers the content is written with. See [External MCP servers](#external-mcp-servers). |

| Field type | Holds |
| --- | --- |
| `text` | One line of text. `options` limits it to a list of values. |
| `tikz` | One `tikzpicture` environment. The app draws it with TeX before the draft is saved, and reports a drawing that does not draw as an issue. |
| `markdown` | Text with markdown and maths. The app refuses text with a `$` that is never closed, or with `\n`, `\t`, `\;`, `\,` or `\!` outside a formula, because each would reach a learner as those characters. |
| `maths` | One line of mathematics in LaTeX between `$` signs, such as a line of a worked solution. The app refuses a line without a formula, and a line that is a sentence in `\text{}`. It checks the text as `markdown` does. |
| `whole_number` | A number such as minutes. |
| `yes_no` | `true` or `false`. |
| `list` | A list of text. |
| `group` | One object with `fields` of its own. |
| `items` | A list of objects with `fields` of their own. With `kinds` instead, each item is one of several shapes, named by its `kind`. |

A field is required unless it has `"required": false`. A `list` or `items` field holds one entry or more; `"min_items": 0` lets it be empty. Groups and items nest at most 4 deep.

- The API refuses a slug that is already used, and a spec with no `unit` and `parts`.
- The API refuses a spec that pins a skill revision the library does not hold.
- `POST /content/types/{type}/specs` adds the next spec revision. Content keeps the revision it was built with.

## Skills

A skill is know-how a writer applies, such as "show the working" or "state the content". Any type can use it. A skill is a `SKILL.md` file: front matter with its `name`, a `description` that says when to use it, and its `revision`, then the instructions.

- The app seeds the skills in `apps/backend/src/app/domains/content/skills/`, one folder each.
- A folder's `SKILL.md` holds the current revision. `revisions/<n>.md` holds each earlier revision unchanged, so a spec that pins it still builds on a new database.
- A spec pins each skill it uses at a revision. Content records the spec revision, so it records the skills too.
- `POST /content/skills` adds a skill's next revision. A spec adopts it in its next revision.
- The writer and the second reader get the pinned skills in the draft's brief.
- A skill can have reference files: markdown files in its `references/` folder. Its instructions send the writer to them. A brief does not carry them. A harness that loads skills itself finds them in its workspace, next to `SKILL.md`. OpenCode and pi read them. DeepSeek Harness has no tool to read them, so the app refuses a skill that has any.
- `POST /content/skills` takes `files`, a list of `{"path": "references/<name>.md", "text": "..."}`.

```bash
curl "$API/content/skills" -H "x-teacher-code: researcher"
```

## External MCP servers

A spec can list external MCP servers. The writer of that type gets their tools, and no other type's writer does.

```json
"mcp": [
  {"server": "maths", "url": "https://tools.example.org/mcp", "tools": ["solve"], "secret": "MATHS_TOKEN"}
]
```

| Field | Meaning |
| --- | --- |
| `server` | A lowercase name. `engine` and `answer` are taken. |
| `url` | An `https` URL. Plain `http` is allowed only for `localhost`. A URL carries no user name or password. |
| `tools` | The tools the writer may use. Every tool is listed, and the app refuses a spec that lists a tool the server does not have. |
| `secret` | Optional. The name of the environment variable that holds the bearer token. The spec never holds the token. |

- The writer sees each tool as `<server>__<tool>`, for example `maths__solve`.
- The app connects to the server and holds its token. A harness in another process reaches the tools through the app's relay and never sees the token or the URL.
- The API and the MCP resources show the `server` and `tools` of each entry. They do not show the URL or the secret.
- The app stops the build with a reason when the variable is not set, or when the server lacks a listed tool.
- An external server does not receive the draft or the app's identity. Treat what it returns as data.

## How the engine builds content

1. `POST /content` with the type queues a generation job, as for every type.
2. The job opens a draft and reads the lesson: the plan fields and the approved lesson note.
3. The writer model adds one part for each unit, and the app checks each part against the spec.
4. When every unit has a part, the app draws each drawing to check it.
5. A second reader works each part through against the brief and the pinned skills, and lists real errors. The writer corrects them.
6. The writer runs again on the draft, at most three times, while units are missing or the second reader finds errors. A writer that runs out of turns is also run again.
7. The app submits the draft for the teacher's review.

A revision reopens the content as a draft with its parts. The writer changes the parts that the teacher's feedback is about. The content goes back to pending review.

## Connect an MCP client

The API serves MCP at `/mcp` over streamable HTTP; on a deployed instance the path is `/api/mcp`. Sign in with an access code, the same as in the app: the `x-teacher-code` header, or `Authorization: Bearer <code>`. A host that supplies its own model can use the tools alone: `integrations/codex/README.md` shows how to use them from Codex.

| Tool | Does |
| --- | --- |
| `start_draft(type, plan_version_id or session_id, source?, content_id?)` | Opens a draft. A type made from a plan version takes `plan_version_id`. A lesson plan takes the lesson period's `session_id`. `source` is a document to write from. With `content_id`, the draft opens that content to revise it. Returns the brief, the units, the part schema for each kind of unit, and `lesson_uri`. |
| `add_part(draft_id, unit_id, part)` | Stores the part for a unit. Returns the units still missing. When no unit is missing, it also returns the issues that stop the draft being saved. |
| `revise_part(draft_id, unit_id, part)` | Replaces the part for a unit. Returns the same as `add_part`. |
| `list_content_types()` | Lists the types, what each is made from, and whether it is drafted with these tools. |
| `find_lessons(query?)` | Finds the lessons of the caller's own classes by words such as a topic, a week or a class. Each has a `lesson_id`, which is the `session_id` of `start_draft`, and a `plan_id` when it has a plan. |
| `read_lesson(draft_id)` | Returns what the draft's `lesson_uri` holds, for a client that reads only tools. |
| `read_draft(draft_id, fields?)` | Returns the draft, the units still missing and the issues. Name `fields` to get only those. |
| `locate_text(draft_id, text)` | Finds where text the teacher selected is in the draft. Returns the unit and the field path of each part field that holds the text, the line of the field it is on when the field has several lines, and the text around it. It reads the parts as plain data, so it works for every type. |
| `submit_draft(draft_id)` | Saves the draft for the teacher's review. Returns what it is saved as. |
| `show_draft(draft_id)` | Returns what the draft saves as so far. A host with MCP Apps shows it as a page. |
| `show_content(content_id)` | Returns the content. A host with MCP Apps shows it as a page (`ui://content/viewer.html`) drawn for its type: a plan's steps, a class test's questions and key, a note's sections, a revision note's practice with its answers. |

| Resource | Returns |
| --- | --- |
| `content-types://` | Every type, each with its spec. `?engine=mcp` lists the engine types only. |
| `content-type://{type}` | One type, its current spec and its part schemas. |
| `lesson://{plan_version_id}` | What a writer may read about a planned lesson. |
| `lesson-period://{session_id}` | A lesson period that has no plan yet: its subject, topic and curriculum objectives. |
| `content://{content_id}` | Content and its review status. |
| `skills://` | Every skill with its name and when to use it. `?search=` narrows the list. |
| `skill://{slug}` | One skill with its instructions and reference files. `?revision=` picks a revision. |

A teacher works only on the lessons of their own classes. A draft belongs to whoever started it.

## Show content in the app

The app is an MCP Apps host. For engine content, the content page connects to `/mcp` with the teacher's access code and reads the tool `show_content`. The tool's metadata names a `ui://` page. The app loads that page and draws it in a frame, then gives it the tool's result.

- **The frame has no access to the app.** It is sandboxed with `allow-scripts` only, so it has no access to the app's storage, cookies or page. It talks to the app over `postMessage`.
- **The page reaches only what its resource declares.** The app builds a Content-Security-Policy from the origins in the resource's `_meta.ui.csp` and puts it at the head of the page. Anything else is refused, and an origin that is not a plain `https`, `http`, `wss` or `ws` origin is left out.
- **The page can ask the host for little.** The app does not pass the page's tool or resource requests on to the server. The page can ask the app to open a web link, to report its height, and to send a comment to the content's chat as a message (`ui/message`). The app tells the page it takes messages, so the page offers only the comment on selected text and draws no conversation of its own.
- **The page sizes its own frame.** It reports its height and the frame follows.
- **The page follows the item.** The page is loaded again when the item's version or review status changes.
- **Field order comes from the spec.** Storage does not keep the order of an object's keys, so `show_content` returns the `parts` of the spec the content was built with, and the page draws each part's fields in that order.
- **When there is no page,** the app draws the content with its own components, for a server that has no page for the tool or cannot be reached.

The frontend code is in `apps/frontend/src/features/mcp-app/`. `cypress/e2e/mcp_app_view.cy.ts` runs it against the real stack.

## Create content by describing it

A lesson's content card shows a box on each engine type: "Tell the agent what you want". The words go with `POST /content` as `instructions`, up to 4000 characters, and the writer reads them with its brief. A built-in type refuses them (`instructions_apply_to_engine_types_only`).

The agent that makes the content keeps its session. When the content exists, what the agent did becomes the content's own chat (slot 0, titled "Creation"), with the agent's key, so the first comment on it goes to the same agent, which continues with what it already did. Content made without instructions gets the same chat.

## Chats on content

Content has any number of chats. The first is its own (slot 0): the creation chat, or the one the first comment opens. Each chat started after it has an agent of its own, with its own session, and sees the content as it is now. Anyone who may read the content may read any of its chats.

| Call | Does |
| --- | --- |
| `GET /content/{id}/chats` | Lists the chats: `chat_id`, `slot`, `title`, who started it, and whether its agent is working. |
| `POST /content/{id}/chats` | Starts a chat. The first chat on content takes slot 0. |
| `POST /content/{id}/chats/{chat}/messages` | Sends a message. It is taken at once (`202`) and answered in the background. |
| `POST /content/{id}/chats/{chat}/stop` | Stops what the chat's agent is doing and drops the messages waiting. Nothing is saved: the content stays as it was, and the agent keeps what it did, so the next message goes on from there. Says whether a turn was running and how many messages were dropped. A turn cannot be stopped while its version is being saved. |
| `GET /content/{id}/chats/{chat}/events?after=N` | The chat as a server-sent stream: the events kept after sequence number `N`, then what happens next. |

Chats on one content take turns where the work is done, because each turn starts from the version the one before made.

An event has a `kind` and `data`. The app keeps these, and gives each a sequence number (`id` in the frame), so a page that lost its connection asks for what came after the last one it saw:

| Kind | Holds |
| --- | --- |
| `user_message` | The message, and where it pointed. |
| `agent_text` | A piece of the agent's text, when it is finished. |
| `tool` | A tool the agent used: its name, its status, and the unit it worked on. |
| `turn_done` | The agent's summary, whether the content changed, and its version. |
| `view` | The content to draw in the chat: the tool `show_content` and its input. A page that is an MCP App host draws it inline. |
| `turn_failed` | Why the turn failed. |
| `turn_stopped` | The teacher stopped the turn. |

A page that is watching also gets, without sequence numbers and never kept: `partial` (the agent's text so far), `working_on` (a tool just started) and `status` (the agent is busy or idle). A chat made before events were kept sends its turns as events on the first connection. The stream sends `: keep-alive` lines when quiet, and follows a chat worked on in another process by reading what was kept every second.

## Comment on content

The content page has **Chat with the agent** for every kind of content. It opens a panel that lists the content's chats, any of which can be opened, with **+ New chat** to start another. The open chat is followed over its event stream: the messages, what the agent does ("Revised a part · lop02"), its text as it is written, and "Saved as version 3". The agent's text in a turn is muted but for the last. When the content changes, the content is drawn inline by the MCP server's own page, with only the latest open. **Stop** appears while the agent works or a message waits. A dropped connection is followed again from the last event, so nothing is missed. Engine content is answered by its chat's agent. The other kinds are answered by their own reviser.

The content page lets a teacher select text, write a comment and send it. The page sends the comment to the app as a message. The app files it in the chat that is open, or starts one, as a message from the teacher with the selected text quoted, and the agent revises the content from there. The message carries the selected text, and the unit and field path where the page draws the parts from the spec. When it has no place, the engine searches the draft for the selected text after it opens the draft, and tells the agent the unit and field of each place the text is in. The search reads the parts as plain data, so it works for every type; the agent can also call `locate_text` itself. The page shows "Sent to the chat." and leaves the answer to the chat.

- **One session per item.** The first comment opens an agent session. Later comments continue it, so the agent keeps its history, including the tool calls it made. A follow-up message holds the new draft, the comment and the selected text, and does not repeat the brief.
- **Each comment makes a new version.** The agent opens a draft of the latest version, revises it, and submits it. The page reloads to the new version. The revision thread records each comment, the selected text, and the versions before and after.
- **The session outlives the agent's process.** OpenCode keeps a session's messages in its data folder. The app keeps that folder and the agent's workspace in `apps/backend/var/engine-sessions/<agent key>/`, with the session id beside them, under the key the chat holds. When the agent has been idle for 600 seconds, has made room for another, or the API restarts, the next comment starts a new process on the same folder and continues the same session. The app removes a thread's folder after 30 days without a comment.
- **Limits.** The app keeps at most 3 agent processes running. A comment that arrives while every one is working is refused until one finishes. A comment in progress when the API restarts is lost, and the teacher sends it again. Turns on one thread run one at a time, whether they come from the page or from the revise request.

The code is in `apps/backend/src/app/domains/content_engine/` (`infrastructure/live.py`, `application/comments.py`, `mcp/comment_tools.py` and `mcp/viewer_conversation.js`). A host that does not take messages, but lets the page call the server's tools, gets the page's own conversation panel through `comment_on_content` and `conversation_state`.

## Write a lesson plan

The content engine writes a lesson plan in two ways. Both save a draft plan version for the teacher to review and approve.

| From | Request | Recorded as |
| --- | --- | --- |
| The curriculum and the textbook | `POST /artefacts/lesson-plans/generate` with `session_id` | `generated` |
| A teacher's document (`.txt`, `.md`, `.docx` or `.pdf`) | `POST /plan-imports` with `session_id` and `file` or `text` | `document_import` |

```bash
curl -X POST "$API/plan-imports" -H "x-teacher-code: teacher-1" \
  -F session_id=<lesson_period_id> -F file=@plan.docx
```

Each request queues a job and returns its `job_id`. The job's result names the new plan. Add `-F experiment_id=<id>` to an import to make the plan the experiment's plan. An experiment's own plan is drafted the same way, from the curriculum.

The job drafts the plan with the tools above: `start_draft("lesson-plan", session_id=..., source=...)`, with no `source` when it writes from the curriculum. The lesson plan's spec (revision 4) gives it two kinds of part, and pins the skill `writing-lesson-plans`. The spec's brief is the one the study's plans were asked:

| Unit | The part holds |
| --- | --- |
| `lesson` | The introduction and the evaluation steps, and the entry behaviour, materials, misconceptions, references and assessments. |
| Each `curriculum_objective` | The lesson objectives that teach it. Each has its core step and the questions that check it in the evaluation. An empty list means the lesson does not teach it. |

The writer reads the lesson's resource, `lesson-period://{session_id}`. It holds the lesson's facts, the curriculum objectives, the curriculum's own notes for the lesson (`curriculum`), and every textbook record the lesson has, with the records each objective links to and their roles (`textbook`).

The app puts the parts together into the plan. Every ID, and every link from an objective to the steps that teach and check it, comes from where a part sits. The writer does not write an ID.

The issues are the checks a teacher's own plan passes: the plan schema, the drafting rules, the lesson context and the plan model. A plan the app writes from the curriculum must also meet the spec's requirements. These are the lesson document grammar, the order of the steps, the work each student activity sets and the minutes. Every reference must name a source the lesson has. Each issue names the part and the place in it, for example `the cur_obj01 part, at lesson_objectives.0.core_step`.

While the job runs, `GET /artefacts/lesson-plans/drafting-progress?session_id=...&after=<n>` returns what the agent is doing, from the latest run's start. When the plan is saved, the agent's work is the plan's first chat.

Content that the engine writes from a plan version reports the same way. While its job runs, `GET /content/generation-progress?plan_version_id=...&type=...&after=<n>` returns what the agent is doing, and the lesson's content card draws it as the agent's chat. When the content is saved, that work is the content's first chat.

### Reuse a plan that already exists

A plan that already exists, such as the study's, can become an experiment's plan without being written again. The plan keeps its steps and the wording of its objectives. `POST /experiments/{experiment_id}/plan/reuse` takes either a saved plan version (`source_plan_version_id`) or a plan's content (`session_plan`).

- The server reads the plan's field names as it reads a stored plan, so a plan written before the renames (`step_role`, `knowledge_type`) is accepted.
- Each lesson objective is pointed at a curriculum objective of the lesson it now sits in. An objective takes the one chosen for it in `curriculum_choices`, then the one it already names when the lesson has it, then the lesson's only curriculum objective. When an objective still has none, nothing is saved and the response lists the choices to make (`needs_curriculum_choice`).
- The plan passes the same checks as a plan entered by hand, and is saved as a draft for the teacher to accept. It is recorded as `experiment_reused`, with the plan version it came from in the version's `run_metadata.imported_from`.
- A teacher can reuse a plan of a lesson they teach. A research manager can reuse any plan.

The page is the **or reuse an existing plan →** link on the lesson's plan step. It is separate from writing a plan from a document (`POST /plan-imports`), where the engine writes the plan.

### Revise a lesson plan

A teacher revises a plan in its chat (`ContentChat`). The teacher may select text on the plan to point at a step or block. The engine reopens the plan as a draft with its parts (`split_plan`, the inverse of the assembly). The agent changes the parts the message concerns, and the next draft version is saved. A message that changes nothing saves no version. A figure is not a part. It stays in its step when a revision saves.

## Generators

A type can have more than one generator. `content_type_generators` holds one row for each generator of a type at a level: its harness (`dspy-pipeline` or `engine`), where its schema lives (`code` or `spec`), a `ref` (a pipeline name such as `2026-09-02`), and a status (`default`, `available` or `retired`). The database allows one default for each type and level.

`ContentCatalogue.generator` resolves a request. A pinned `ref` wins if the row is not retired. The request's `pipeline` field is that pin for every type: a plugin's name, `builtin` for the original program, or a revision note's version by date. That is how an experiment names the original generator while a plugin is the default. Otherwise the default row applies. An engine type with no row resolves to the engine at the type's current spec. Seeding adds the generators in use today, and a stored row keeps its status.

Each generated item records the generator in `provenance.generator` (`harness`, `schema`, `ref`, and `spec_revision` for the engine).

### Add a generator to a type

An artefact file of a plugin has `type` (a new slug) or `implements` (a slug that exists), never both. A plugin with `implements` has no `label`, `audience` or `made_from_a_plan_version`. The lesson plan, the lesson note, the class test and the revision note accept a generator today (`TAKES_GENERATORS`).

Installing stores the plugin's spec under the plugin's name (`content_specifications.generator`), so the type's own current spec does not change. The generator is `available`, never the default. The spec may change the skills and the requirements. It may not change `unit`, `parts` or `lesson_parts`, and it is class level only. `ContentCatalogue.make_default` makes a generator the default, and a new draft is written to the default generator's spec. A lesson plan generator keeps the type's `unit`, `parts` and `lesson_parts`, because the plan is read part by part. A lesson note generator writes one part for each `plan_step` in any fields of its own: when the draft is saved, `part_as_markdown` sets each part down as headed markdown, and the note is stored as every lesson note is (`LessonNoteDestination`), so revision, approval and the revision note read it unchanged. When a lesson note generator is the default, `ContentService` builds the note with the engine; with a native default it uses the pipeline. A lesson note, from either generator, carries no textbook record id from the plan (`without_record_ids`, such as ch01-b044-i01) and no second thought left in the text (`corrects_itself`): the pipeline draws the step again, up to three times, and the agent is told. A naira sign typed as `\u20a6` inside a formula decodes. A step's note must hold at least 300 characters of text (`MIN_NOTE_CHARS`), or the agent is told to add substance. The shipped `lesson-note-writer` writes the teacher's note the way the pipeline's does: teaching points in order, worked examples, questions for the class with expected answers, and what stays on the board. It is available, not the default, and `lesson-note-engine` stays until the default is flipped on evidence.

A class test generator keeps the question fields grading reads (`class_test_parts.json`): for each lesson objective, questions with a stem, four options, the correct letter, a misconception code on each wrong option and a difficulty. The plugin's check tools check every question (the options differ, the key is one of them, each wrong option has a snake_case code, and the tool `class_test_second_reading` has a second reader find only the key right). `ClassTestDestination` then replaces the lesson's `exit_ticket_items` and the class test's record, so grading and learner state read it unchanged. A question must also print its numbers in the stem (`says_what_it_asks`), an objective that names a size (thousand to trillion) is tested at that size in at least one question (`reaches_scale`: the pipeline redraws, the agent is told), and a label is raised to what the stem allows (`labelled`: mixed sizes or a decimal size is at least medium). The shipped `class-test-writer` is such a generator. It is available, not the default.

A revision note generator writes one section for each lesson objective in the fields of `revision_note_parts.json`: a title, an explanation, drawings, worked examples with their working, and practice with answers. `RevisionNoteDestination` hands the sections to `EngineBasePack.store`, which builds the class pack as the pipeline does: the same units and source evidence, the same section assembly, and the policy's structural checks (objective coverage, source references, checkable practice). A pack that fails them is refused with the reasons and nothing is stored. The critic's prose checks are not run, and a drawing stays in the explanation as TikZ so a later revision keeps it. Only the class level takes a plugin; learner packs stay on the pipeline, the two native pipelines stay locked, and a request that names `sources` uses the pipeline. The shipped `revision-note-writer` is available, not the default.

A default generator cannot be removed; make another the default first.

`GET /content/types` lists each type's `generators`. `PUT /content/types/{type}/default-generator` (`{level, generator}`) makes one the default. A researcher can, through the policy wildcard, and an admin can, through `content_type:*, set_default`. Installing or changing a plugin stays with the researcher. A plugin can take the default from a native pipeline and the pipeline can take it back, but the route never makes one native pipeline the default in place of another (`native_generator_is_locked`), and each change is logged with who made it. The Plugins page shows the generators and the button.

A lesson plan version records its generator in `run_metadata.generator`, and a plan item shows it as `provenance.generator`. Engine content records it in `artefact_refs.generator`. A draft's `spec_revision` names the plugin's spec.

## Code

| Part | Path |
| --- | --- |
| Types, specs and generators | `apps/backend/src/app/domains/content/` (`domain/generators.py`, `infrastructure/generator_store.py`) |
| The part schema | `apps/backend/src/app/domains/artefacts/core/domain/parts.py`, `part_fields.py`, `part_check.py` |
| Drafts and the engine | `apps/backend/src/app/domains/content_engine/` |
| The MCP server | `apps/backend/src/app/domains/content_engine/mcp/server.py` |
| Where a finished draft is saved | `apps/backend/src/app/domains/content_engine/application/content_destination.py`, `plan_destination.py` |
| A plan put together from its parts, and split back into them | `apps/backend/src/app/domains/artefacts/types/lesson_plan/domain/plan_sections.py` |
| The lesson's sources for a writer | `apps/backend/src/app/domains/content_engine/infrastructure/plan_grounding.py` |
| Drafting a plan as a job | `apps/backend/src/app/domains/content_engine/infrastructure/plan_generator.py`, `jobs.py` |
| The skill the writer follows | `apps/backend/src/app/domains/content/skills/writing-lesson-plans/` |
| Engine content in the app | `apps/frontend/src/features/content/components/EngineContentView.tsx` |

## A generator at learner level

A plugin that implements the revision note can write one learner's note instead of the class note. Its spec says `levels: ["learner_level"]`, keeps the class note's parts and adds `misconception_repair`, and its `adaptable` list is the one the type declares: depth of explanation, worked support, hints, feedback, practice difficulty and misconception repair. Installing it registers an available generator at the learner level, and `ContentCatalogue.make_default` with `Level.LEARNER` makes it the one the job uses.

The job that makes a learner's note (`generate_student_pack`) reads the default learner generator. A native default runs the pipeline as before. An engine default runs `EngineLearnerGenerator`:

1. `start_draft` takes `student_id`. The draft lists a unit for each objective the learner has enough marked work to adapt (`min_marked_questions`, 2). The other sections stay as the class note has them and are recorded `thin_evidence`. A learner with no objective to adapt gets the class note as it stands, and no agent runs.
2. The writer reads `learner://{draft_id}`, merged into the lesson it is given: the approved class note's section and the learner's state for each objective (band, misconception, wrong answers, survey).
3. The draft is held to the class note's checks, to the limits of adaptation (`adaptation_limits`: the title and drawings stay, a misconception is repaired where the state names one and nowhere else), and to the structural checks of a learner's note (`PERSONALISED_REVIEW_PACK_POLICY`).
4. The note is stored pending, as the pipeline stores one: it records the class note version it was made from, its checks and passages, and what became of each section.

A misconception repair is stored as its own block, opening with `**A common slip**`, so it can be counted and found.
