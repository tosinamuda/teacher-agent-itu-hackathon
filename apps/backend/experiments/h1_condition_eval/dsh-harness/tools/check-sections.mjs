/**
 * A model-facing tool that checks `sections.xml` against the pack contract.
 *
 * The agent can already run `check_sections.py` through bash. This exists so the
 * check is a described capability rather than an instruction to remember from
 * the task file, and so the verdict returns as a tool result the loop acts on.
 *
 * IT SHELLS OUT rather than reimplementing the rules. Node has no XML parser, so
 * a JS version would need a dependency AND would be a second implementation of
 * the same contract, free to drift from the one that matters. `check_sections.py`
 * is standard-library Python and already sits in the workspace, so this stays a
 * thin wrapper over it: one set of rules, no dependencies.
 *
 * NO DEPENDENCIES, and that is deliberate. `defineTool` from
 * `@deepseek-ai/dsh-tools` is a convenience wrapper — it converts a friendly
 * parameter spec to JSON Schema and wraps `execute` with argument validation —
 * and `ctx.tools.register` accepts the plain object it produces. Verified
 * against the shipped runtime: a hand-written object registers, and the model
 * invokes it. That matters because installing `dsh-tools` pulls `dsh-agent` and
 * a peer graph that does not resolve at the runtime's own version; forcing it
 * with --legacy-peer-deps deleted five packages the LLM adapter needs.
 *
 * This is the agent's own check, not the gate. `sections_document.py` validates
 * again on ingest against the RELAX NG grammar, and that one is authoritative:
 * an agent that ignores this result must still not get a bad pack to a rater.
 */

import { execFile } from 'node:child_process'
import { existsSync } from 'node:fs'
import { join } from 'node:path'

/**
 * `execFile`, promised explicitly rather than through `util.promisify`.
 *
 * `promisify(execFile)` returns `{stdout, stderr}` ONLY because execFile carries
 * a `util.promisify.custom` implementation. That symbol does not survive into
 * the harness's bundled runtime, so promisify falls back to its generic wrapper,
 * resolves with the bare stdout string, and `const { stdout } = await run(...)`
 * destructures a string into undefined. The tool then died on `undefined.trim()`
 * and reported "the check itself failed to run" on every call — the agent's own
 * gate answering an error instead of a verdict, in every draw of every run.
 */
function run(command, args, options) {
  return new Promise((resolve, reject) => {
    execFile(command, args, options, (error, stdout, stderr) => {
      const output = { stdout: String(stdout ?? ''), stderr: String(stderr ?? '') }
      if (error) reject(Object.assign(error, output))
      else resolve(output)
    })
  })
}



export const name = 'check-sections-tool'
export const inject = ['tools']

export function apply(ctx, config = {}) {
  const workspace = config.workspace ?? process.env.DSH_CWD ?? process.cwd()
  const python = config.python ?? 'python3'

  ctx.tools.register({
    name: 'check_sections',
    description:
      'Check the revision pack in sections.xml against the required contract: that it ' +
      'is well-formed XML, that every objective has exactly one section in objective ' +
      'order, that each section has an explanation block and a worked_example block, ' +
      'and that no answer has been written inside its own prompt. Returns OK, or the ' +
      'list of problems to fix. Call it before finishing, and again after any repair.',
    // NO PARAMETERS, deliberately. There is one pack, in one place, and an
    // optional `path` was an invitation to guess: across two runs the model sent
    // "sections.xml", "/sections.xml", "./sections.xml", the real absolute path,
    // null and "" — nine calls a run, and one turn took 539s against 68s with no
    // tool at all. A tool with nothing to get wrong cannot be got wrong.
    parameters: { type: 'object', properties: {}, required: [] },
    output: {
      schema: { type: 'string' },
      render: (_args, value) => [{ type: 'text', text: value }],
    },
    async execute(_args, exec) {
      const xmlPath = join(workspace, 'sections.xml')
      if (!existsSync(xmlPath)) {
        return 'sections.xml does not exist yet — write the pack in the workspace root first.'
      }

      const checker = join(workspace, 'check_sections.py')
      if (!existsSync(checker)) return `cannot check: ${checker} is missing from the workspace`

      const curriculum = join(workspace, 'inputs', 'curriculum.json')
      try {
        const { stdout } = await run(python, [checker, xmlPath, curriculum], {
          cwd: workspace,
          signal: exec?.signal,
          maxBuffer: 1024 * 1024,
        })
        return stdout.trim() || 'OK'
      } catch (error) {
        // The checker exits non-zero when the pack has problems, and that is the
        // normal path: its stdout IS the answer the model needs, so report it
        // rather than surfacing a process failure.
        const reported = String(error?.stdout ?? '').trim()
        if (reported) return reported
        return `the check itself failed to run: ${error?.message ?? error}`
      }
    },
  })
}
