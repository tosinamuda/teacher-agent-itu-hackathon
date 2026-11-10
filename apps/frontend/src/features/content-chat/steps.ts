import type { Line } from "./transcript";

export type Step = Extract<Line, { from: "tool" | "thinking" }>;
export type Block =
  | { kind: "steps"; id: string; steps: Step[] }
  | { kind: "line"; line: Exclude<Line, Step> };

const isStep = (line: Line): line is Step =>
  line.from === "tool" || line.from === "thinking";

/**
 * The lines with every tool call and thought of a turn gathered into one block, placed where the
 * turn's first one came. A turn runs from the teacher's message to the next, so a reply in the
 * middle of the work does not split it.
 */
export function blocksOf(lines: readonly Line[]): Block[] {
  const blocks: Block[] = [];
  let card: Extract<Block, { kind: "steps" }> | null = null;
  for (const line of lines) {
    if (!isStep(line)) {
      if (line.from === "teacher") card = null;
      blocks.push({ kind: "line", line });
    } else if (card) {
      card.steps.push(line);
    } else {
      card = { kind: "steps", id: line.id, steps: [line] };
      blocks.push(card);
    }
  }
  return blocks;
}

/** How many of the steps are tool calls: a thought is not a step the agent took. */
export const toolCount = (steps: readonly Step[]): number =>
  steps.filter((step) => step.from === "tool").length;
