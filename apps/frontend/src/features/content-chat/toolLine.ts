import type { Line } from "./transcript";

type Tool = Extract<Line, { from: "tool" }>;

const VERBS: Record<string, string> = {
  add_part: "Wrote",
  revise_part: "Revised",
};

const FIXED: Record<string, string> = {
  start_draft: "Opened a draft",
  read_draft: "Read the draft back",
  locate_text: "Looked for the selected text",
  submit_draft: "Saved the draft",
};

/** A part of a lesson plan, said as a person would: the lesson's own, or an objective's. */
function partOf(unit: string | undefined): string {
  if (!unit) return "a part";
  if (unit === "lesson") return "the lesson's own part";
  const objective = /-po(\d+)$/.exec(unit);
  return objective
    ? `objective ${Number(objective[1])}'s part`
    : `part ${unit}`;
}

/** What a tool call says to a person: what the agent did, and to what. */
export function toolLine(line: Tool): string {
  const verb = VERBS[line.tool];
  if (verb) return `${verb} ${partOf(line.unit)}`;
  if (line.tool === "skill")
    return line.detail
      ? `Loaded the skill \u201c${line.detail}\u201d`
      : "Loaded a skill";
  if (line.tool === "read")
    return line.detail ? `Read ${line.detail}` : "Read a file";
  return FIXED[line.tool] ?? line.tool;
}

const RUNNING: Record<string, string> = {
  add_part: "Writing a part",
  revise_part: "Revising a part",
  start_draft: "Opening a draft",
  read_draft: "Reading the draft back",
  locate_text: "Looking for the selected text",
  submit_draft: "Saving the draft",
  skill: "Loading a skill",
  read: "Reading a file",
};

/** What a tool says to a person while it runs. */
export const runningLine = (tool: string): string => RUNNING[tool] ?? tool;
