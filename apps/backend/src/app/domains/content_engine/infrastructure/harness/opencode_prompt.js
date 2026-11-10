// OpenCode adds a model line, an <env> block, project instructions and the list of skills to
// an agent's prompt. The engine's harness runs one agent per server, so its prompt is the whole
// system prompt, and the skills the agent may load are the one part kept.
const SKILLS = "Skills provide specialized instructions"

export const EnginePrompt = async () => ({
  "experimental.chat.system.transform": async (_input, output) => {
    const added = output.system.join("\n")
    const at = added.indexOf(SKILLS)
    const skills = at < 0 ? "" : `\n${added.slice(at)}`
    output.system.splice(0, output.system.length, (process.env.ENGINE_SYSTEM_PROMPT ?? "") + skills)
  },
})
