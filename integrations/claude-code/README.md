# Plan-to-Tutor in Claude Code

A teacher can write and revise lesson content from Claude Code. Claude supplies the model. The
`lpcg` MCP server supplies the tools, and the plugins supply the skills.

## Install

1. Add the marketplace from this repository:

   ```bash
   claude plugin marketplace add tosinamuda/lpcg
   ```

2. Install the plugin for each type you need. `lpcg`, which holds the connection, comes with the
   first one:

   ```bash
   claude plugin install lesson-plan@plan-to-tutor
   claude plugin install lesson-note@plan-to-tutor
   claude plugin install class-test@plan-to-tutor
   claude plugin install revision-note@plan-to-tutor
   claude plugin install slide-deck@plan-to-tutor
   ```

3. Set your access code before you start Claude Code:

   ```bash
   export LPCG_ACCESS_CODE=<your access code>
   ```

   The server is `https://lpcg-staging-api.tosinamuda.com/api/mcp`. For another instance, set
   `LPCG_MCP_URL` to its `/api/mcp` address. For a server on your own machine, use
   `http://localhost:8000/mcp`.

## Use

Ask in plain words, such as "Use Plan-to-Tutor to write the slide deck for my lesson on types of
nouns." Claude finds the lesson, writes the draft part by part, and saves it for your review. You
approve it in the app. A slide deck needs the lesson's approved plan and note first.

## Try a plugin without installing it

```bash
claude --plugin-dir plugins/slide-deck --plugin-dir integrations/codex/lpcg
```

## What is here

| Path | Holds |
| --- | --- |
| `.claude-plugin/marketplace.json` | The marketplace: the six plugins below, with each one's description and dependencies. |
| `integrations/codex/lpcg/` | `lpcg`: the workflow skill and `.mcp.json`, the connection to the server. |
| `plugins/<type>/` | One plugin for each type, with its skills. It depends on `lpcg`. |

A plugin has one manifest, `plugin.json`. Claude Code needs no manifest of its own, so the marketplace
holds what only Claude Code reads. `tests/test_claude_code_plugins.py` fails when a plugin gains a
second manifest or its description differs from the marketplace's.
