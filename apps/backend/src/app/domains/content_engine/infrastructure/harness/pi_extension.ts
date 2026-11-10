// The run's pi extension. pi connects the run's MCP servers itself, from the mcp.json the run
// wrote. This extension confines pi's `read` tool to the skills it was given, stops the run
// before a model call over its budget and once an answer tool has been answered, and makes the
// prompt the run's own text plus the skills pi lists.
import { resolve, sep } from "node:path"
import { formatSkillsForPrompt, type ExtensionAPI } from "@earendil-works/pi-coding-agent"

export default function (pi: ExtensionAPI) {
  const skillsDir = process.env.ENGINE_SKILLS_DIR ? resolve(process.env.ENGINE_SKILLS_DIR) + sep : ""
  const answers = new Set((process.env.ENGINE_ANSWER_TOOLS ?? "").split(",").filter(Boolean))
  const budget = Number(process.env.ENGINE_MAX_MODEL_CALLS ?? "0")
  let calls = 0
  let answered = false

  pi.on("turn_start", async (_event, ctx) => {
    if (answered || (budget > 0 && ++calls > budget)) ctx.abort()
  })

  pi.on("tool_result", async (event) => {
    if (answers.has(event.toolName) && !event.isError) answered = true
  })

  pi.on("before_agent_start", async (event) => {
    const { customPrompt, skills } = event.systemPromptOptions
    const listed = skills.length > 0 ? `\n\n${formatSkillsForPrompt(skills, "read").trim()}` : ""
    return { systemPrompt: `${customPrompt ?? ""}${listed}` }
  })

  pi.on("tool_call", async (event) => {
    if (event.toolName !== "read") return
    const path = resolve(String((event.input as { path?: string }).path ?? ""))
    if (!skillsDir || !path.startsWith(skillsDir)) {
      return { block: true, reason: "read only loads the skills you were given" }
    }
  })
}
