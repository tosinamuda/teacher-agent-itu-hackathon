# Artefact plugins

An artefact plugin adds one kind of learning material to the app. A plugin is a folder. The app reads the folder, checks it, and registers what it makes: a type, and the generators that write it. A plugin has one manifest, one `mcp.json` and one `skills/` folder, and an artefact file for each type or generator it makes.

A plugin is a valid [Agent Plugins 1.0.0](https://agent-plugins.org) package. Its skills and MCP servers are the standard files. The app's own data sits in a file in a folder named for its namespace, `com.tosinamuda.lpcg`, and `plugin.json` names the files under `extensions`, as the standard says. Other clients ignore both, so the same folder loads in them.

## Layout

```text
worked-examples/
├── plugin.json                    # the portable manifest
├── skills/
│   └── show-worked-solutions/
│       ├── SKILL.md               # instructions, with front matter
│       └── references/            # optional markdown the instructions send the writer to
├── mcp.json                       # the MCP servers the plugin links to, if any
└── com.tosinamuda.lpcg/           # the app's data
    └── worked-examples.json       # one artefact file for each thing the plugin makes
```

| File | Holds |
| --- | --- |
| `plugin.json` | `$schema` (`https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`), `name` (lowercase letters, digits, hyphens and periods, at most 64), and optional `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, `extensions`. No other field is allowed. The app needs `extensions.com.tosinamuda.lpcg.artefacts`, the paths of the artefact files, each as `./path` inside the plugin. |
| `skills/<name>/SKILL.md` | A skill: front matter with `name` and `description`, then the instructions. `name` is the folder name: lowercase words joined by single hyphens, at most 64 letters, with neither "anthropic" nor "claude" in it. A harness lists the name and the description in the model's prompt, so the name is an activity and its object, such as `showing-worked-solutions`. `description` says what the skill does and when to use it, in the imperative ("Use when …") and with the words a task would carry, in at most 1024 letters. Markdown files under `references/` are its reference files. |
| `mcp.json` | `$schema` (`https://agent-plugins.org/schemas/1.0.0/mcp.schema.json`) and `mcpServers`. The app connects to `streamable-http` servers only and skips the others with a warning. |
| `com.tosinamuda.lpcg/<name>.json` | One artefact: a type (`type`, `label`, `audience`, `spec`) or a generator for a type that exists (`implements`, `spec`), and the names of the skills and the tools it uses. Its schema is `apps/backend/src/app/domains/content/plugins/artefact.schema.json`. |

## Artefact files

`plugin.json` names the files:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "worked-examples",
  "version": "1.0.0",
  "extensions": {
    "com.tosinamuda.lpcg": { "artefacts": ["./com.tosinamuda.lpcg/worked-examples.json"] }
  }
}
```

The file holds the type:

```json
{
  "type": "worked-examples",
  "label": "Worked examples",
  "audience": "learner",
  "spec": {
    "material": "worked examples for one step of the lesson",
    "audience": "{reader} revising at home",
    "levels": ["class_level"],
    "requirements": ["Show every step of the working."],
    "unit": "plan_step",
    "parts": [
      {"name": "title", "description": "A heading for the learner", "type": "text"}
    ]
  },
  "skills": ["show-worked-solutions"],
  "servers": {"maths": ["solve"]}
}
```

- `name` says what the plugin calls the artefact. The installed row and a generator's binding carry it, and the API and the shell address an artefact by it. A plugin with one artefact may leave it out: the plugin's own name is used. A plugin with more must give each its own.
- `spec` has the fields of a [content type spec](content-types.md#register-a-type), without `skills` and `mcp`. The app fills those in.
- `skills` lists the skill folders. The spec pins them in this order. The first is the entry skill: a harness on native skills is told to load it before it writes anything, and it says which of its reference files to read and when. A type that holds one workflow, with its rules as reference files, is better than several skills that each have to be chosen from their descriptions. The app stores each skill under its folder name, so a skill name is global. Two plugins may carry the same skill with the same text, and it is stored once. The same name with different text is refused, and the message names the skill. A harness finds each skill in `.agents/skills/<name>/` of its workspace, the folder the plugin already has, with the same `SKILL.md` and reference files.
- `servers` lists, for each server in `mcp.json`, the tools the writer may use. Every listed server needs an entry, and the app refuses a tool the server does not have.
- `checks` lists, for each server in `mcp.json`, the tools the app calls to check a draft. See [check tools](#check-tools).
- `adds` lists, for each server in `mcp.json`, the tools the app calls when it saves a draft. See [adding tools](#adding-tools).
- `files` lists, for each server in `mcp.json`, the tools the app calls to make a file of saved content. See [file tools](#file-tools).

## Check tools

A rule that a program can check belongs to a tool of an MCP server. The plugin names the server in `mcp.json` and lists the tool in `checks`; it holds no code. This holds for every type: the lesson note, the revision note, the class test and the slide deck are each checked by a tool.

```json
{"mcpServers": {"lpcg": {"type": "streamable-http", "url": "/mcp"}}}
```

```json
{"checks": {"lpcg": ["check_slide_deck"]}}
```

When every part of a draft is written, and again when the writer submits, the app calls each listed check tool with the draft's ID: `{"draft_id": "…"}`. The tool answers `{"faults": ["…"]}`, one string for each fault, each naming its step. An empty list means the draft passes. The faults go back to the writer, and a draft that has any is not saved. The writer never sees a check tool, and a tool that fails, runs longer than 180 seconds, or answers anything else stops the draft with an error.

The app calls the check tools in the order listed and stops at the first that finds faults. List a tool that costs a model call, such as `class_test_second_reading`, last: it then reads only a draft the others pass.

- A link that is a path, such as `/mcp`, is the app's own MCP server. The app reaches it inside its own process, as itself, and the server lists checks, adds and files only. The app's server reads the draft, the approved note of each plan step, the lesson's objectives and the objective of each plan step from the shared database, and keeps its rules and limits with its code: `apps/backend/src/app/domains/content_engine/rules/`. A rule change is a change to that code.
- A link that is an `https` URL is another system. The app reaches it over streamable HTTP, with the token of the environment variable that the server's `Authorization` header names in `mcp.json`. For now that system reads the draft from the same database, so it needs the same data.
- The app's tools are `check_slide_deck`, `check_lesson_note`, `check_revision_note`, `check_class_test`, `check_lesson_plan` and `class_test_second_reading`. A caller other than the app reads only its own drafts.
- A rule about wording belongs in `SKILL.md`.

## Adding tools

Some content holds fields the writer does not write, because the app knows them from the lesson. A slide deck's cover is one: its title, subject line and objectives come from the lesson plan. The plugin lists a tool in `adds`, and the app calls it with the draft's ID when it saves the draft.

```json
{"adds": {"lpcg": ["slide_deck_cover"]}}
```

The tool answers `{"additions": {...}}`. The app saves those fields beside the writer's sections, and the fields of a later tool replace those of an earlier one with the same name. The tool of the app's own server is `slide_deck_cover`. The same rules as for check tools hold for the link, the time limit and who may read a draft.

## File tools

Content that is taken as a file, such as a slide deck as a PowerPoint file, is made by a tool. The plugin lists it in `files`, and the app calls it with the ID of the saved content when someone downloads the file.

```json
{"files": {"lpcg": ["build_slide_deck_file"]}}
```

The tool answers `{"file": {"extension": "pptx", "media_type": "…", "data": "<base64>"}}`. The app names no type: `GET /content/{id}/file` answers the file of any content whose plugin lists a file tool, with the media type and the extension the tool gave, and `has_file` on the content says whether its type has one. An MCP client reads the resource `content://{id}/file` or calls `get_content_file_link`; `submit_draft` hands back the download of content that has a file. Content made before its plugin listed a file tool is made into a file by the tool of the plugin the type has now. A type whose plugin lists no file tool answers `409 file_unavailable`. The app's own tool is `build_slide_deck_file`: its builder and its layout, the sizes and colours in `powerpoint.json`, are in `apps/backend/src/app/domains/content_engine/files/slide_deck/`.

## MCP servers

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "maths": {
      "type": "streamable-http",
      "url": "https://tools.example.org/mcp",
      "headers": { "Authorization": "Bearer ${MATHS_TOKEN}" }
    }
  }
}
```

- A `stdio` or `sse` server is skipped with a warning, so a plugin can also carry servers for other clients. It is an error only when an artefact file lists its tools.
- The URL is `https`. Plain `http` is allowed only for `localhost`.
- The only header a run can send is `Authorization: Bearer ${VARIABLE}`. The app reads the token from that environment variable. The file never holds a token.
- A harness never sees the URL or the token. See [External MCP servers](content-types.md#external-mcp-servers).

## Shipped plugins

The `plugins/` folder holds the plugins the app ships. A plugin is one folder for one kind of material: it has the skills for every artefact it makes, and `mcp.json` links the app's own server. Every deploy installs or updates each folder listed in `content_plugins` in `deploy/ansible/group_vars/all.yml`, and each artefact in it becomes its own row.

| Folder | Artefact | Makes | Unit |
| --- | --- | --- | --- |
| `lesson-plan` | `lesson-plan-writer` | A generator for the built-in lesson plan: the lesson's own part, then one section for each curriculum objective. | `curriculum_objective` |
| `lesson-note` | `lesson-note-writer` | A generator for the built-in lesson note: the teacher's note for one lesson step. | `plan_step` |
| `class-test` | `class-test-writer` | A generator for the built-in class test: multiple-choice questions with a key and a misconception code on each wrong option. | `lesson_objective` |
| `revision-note` | `revision-note-writer` | A generator for the built-in class revision note: explanation, worked examples and practice with answers. | `lesson_objective` |
| | `revision-note-learner-writer` | A generator for one learner's revision note: it adapts the approved class note to what the learner's marked work showed. Learner level only. | `lesson_objective` |
| `slide-deck` | `slide-deck` | The slides for one lesson step, to show the class: a title and at most five short points on each, with the teacher's words in speaker notes. Written from the lesson plan and the approved lesson note, with a picture where it teaches better than words. The app sets the deck's cover, from the lesson's title and objectives. `GET /content/{id}/file` saves the deck as a PowerPoint file, with the points and notes as editable text and each drawing as a picture. | `plan_step` |

The lesson plan, lesson note, class test and revision note are built-in types: the app reads, approves and shows what their generators write. A generator adds no type. The slide deck is the one plugin that adds a type.

A plugin that leaves `plugins/` is listed in `retired_plugins` in the same file. Each deploy runs `remove --if-installed` for it, which stops new drafts of its type and leaves content already made readable.

## Manage plugins in the app

A researcher opens **Plugins** in the researcher navigation (`/research/plugins`). The page has two tabs: **Plugins** lists the installed plugins, and **Generators** (`/research/plugins/generators`) lists how each kind of content can be made and which way new content uses.

- **Add a plugin:** choose its folder. The page sends the folder's text files, leaving out hidden files and `node_modules`, and lists every problem the app finds. A plugin that passes is installed at once, each of its artefacts as a row. A folder with an error installs nothing.
- **Update:** choose the folder again on an artefact's row. The app updates every artefact the folder holds and stores what changed. Content already made keeps the revision it was built with.
- **Remove:** stops new drafts of the plugin's type. Content already made stays readable, and a lesson shows no Generate button for the type.
- **System plugins:** the folders in `plugins/` ship with the app, and each deploy installs and updates them. The list marks them **System**, and the API refuses to install, update or remove one, because the next deploy would undo the change.

The same calls are `GET`, `POST`, `PUT /{name}` and `DELETE /{name}` on `/content/plugins`. A content type in `GET /content/types` has `retired: true` once its plugin is removed.

## Check a plugin

```bash
cd apps/backend
uv run python -m app.domains.content.plugins validate ../../plugins/worked-examples
```

The command prints one line for each problem, with the file and the fix, and exits with 1 when any is an error. It checks:

- `plugin.json` and `mcp.json` against the official Agent Plugins 1.0.0 JSON Schemas, kept in `apps/backend/src/app/domains/content/plugins/schemas/`
- each listed skill has a `SKILL.md` with front matter, a `name` equal to its folder, and a description of at most 1024 letters
- the servers, the URLs, the header and the tool lists
- the spec, as the API checks it when a type is registered

A skill folder that no spec pins is a warning. So is a `revision` in front matter: installing numbers the revisions. So is a reference file that the skill's instructions never name, since nothing then tells the writer when to read it.

## Install, update and remove

```bash
cd apps/backend
uv run python -m app.domains.content.plugins install ../../plugins/worked-examples
uv run python -m app.domains.content.plugins update ../../plugins/worked-examples
uv run python -m app.domains.content.plugins remove worked-examples
uv run python -m app.domains.content.plugins list
```

The API has the same operations. A body carries the plugin folder as `files`, a map of each path to its text.

| Route | Does |
| --- | --- |
| `GET /content/plugins` | Lists each plugin at its latest revision. |
| `POST /content/plugins` | Installs a plugin. |
| `PUT /content/plugins/{name}` | Updates it. |
| `DELETE /content/plugins/{name}` | Removes it. |

- Install and update need the permission to revise content types.
- Install refuses a plugin name or a type slug that is in use, and writes nothing then.
- Install stores each skill as a skill revision and pins it in the type's first spec revision.
- Update stores a new skill revision only when the skill's text or files changed. It stores a new spec revision only when the spec or a pinned skill changed. A folder that has not changed updates to nothing.
- Content keeps the spec revision it was built with, so an update never changes existing content.
- A plugin keeps its type. Update refuses a new slug, label or audience.
- Remove stops new drafts of the type. Content already made stays readable. Update installs a removed plugin again.
- Each install, update and removal is one row in `content_plugins`. The rows are never edited.
- Install and update keep the folder's files, as text, in the row. A plugin holds text files only, and hidden files and folders are left out. A file that is not text is an error that names it.

## Run

When OpenCode, DeepSeek Harness or pi writes a plugin's content with native skills, the engine copies the plugin's `skills/<name>/` folders, as installed, into `.agents/skills/<name>/` of the run's workspace. The copy is the plugin's own files, byte for byte, for the spec revision the draft was made with. The engine's server serves them as `plugin-skills://<type>`. A type that no plugin made has its skills written from their stored revisions.

## Where hooks go

Agent Plugins does not define hooks: each client defines its own. Hooks for this app go in a `com.tosinamuda.lpcg` folder, as the standard says for client files, and the app adds them in a later sprint.

## Other clients

- Claude Code reads its skills from the same `skills/` layout and needs no manifest of its own: `.claude-plugin/marketplace.json` lists the plugins and gives each its description and its `dependencies`. The `lpcg` plugin holds the connection to the app's MCP server in `.mcp.json`, and each type plugin depends on it. `integrations/claude-code/README.md` shows how to install them.
- Codex reads the portable `plugin.json`. A later sprint checks that a plugin loads there.
