# Plan-to-Tutor in Codex

A teacher can write and revise lesson content from Codex. Codex supplies the model. The `lpcg`
MCP server supplies the tools, and the plugins supply the skills.

## Install

1. Add the marketplace from this repository:

   ```bash
   codex plugin marketplace add tosinamuda/lpcg
   ```

2. Install the workflow plugin and the plugins for the types you need:

   ```bash
   codex plugin add lpcg@plan-to-tutor
   codex plugin add lesson-plan@plan-to-tutor
   codex plugin add lesson-note@plan-to-tutor
   codex plugin add class-test@plan-to-tutor
   codex plugin add revision-note@plan-to-tutor
   codex plugin add slide-deck@plan-to-tutor
   ```

3. Set your access code, and add the server:

   ```bash
   export LPCG_ACCESS_CODE=<your access code>
   codex mcp add lpcg --url https://lpcg-staging-api.tosinamuda.com/api/mcp --bearer-token-env-var LPCG_ACCESS_CODE
   ```

   For a server on your own machine, use `--url http://localhost:8000/mcp`.

## Use

Ask in plain words, such as "Find my lesson on LCM and write its lesson plan." A slide deck needs the lesson's approved plan and note first. The model finds
the lesson, writes the draft part by part, and saves it for your review. You approve it in the
app.

## What is here

| Path | Holds |
| --- | --- |
| `.agents/plugins/marketplace.json` | The marketplace: the six plugins below. |
| `integrations/codex/lpcg/` | The workflow skill, `drafting-lesson-content`. |
| `plugins/<type>/` | One plugin for each type. Each has the skills that say how to write that type. |

The server asks for an access code and not for OAuth, so a plugin cannot carry the connection
yet. Step 3 adds it by hand.
