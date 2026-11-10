import { describe, expect, it } from "vitest";

import { blocksOf, toolCount } from "./steps";
import type { Line } from "./transcript";

const tool = (id: string): Line => ({
  id,
  from: "tool",
  tool: "read",
  failed: false,
});

describe("blocksOf", () => {
  it("gathers every tool call and thought of a turn into one block, past a reply", () => {
    const lines: Line[] = [
      { id: "1", from: "teacher", text: "Go." },
      { id: "2", from: "thinking", text: "Plan." },
      tool("3"),
      { id: "4", from: "agent", text: "Half done." },
      tool("5"),
    ];

    const blocks = blocksOf(lines);

    expect(blocks.map((block) => block.kind)).toEqual([
      "line",
      "steps",
      "line",
    ]);
    expect(blocks[1]).toMatchObject({
      steps: [{ id: "2" }, { id: "3" }, { id: "5" }],
    });
  });

  it("starts a new block at the teacher's next message", () => {
    const blocks = blocksOf([
      tool("1"),
      { id: "2", from: "teacher", text: "Again." },
      tool("3"),
    ]);

    expect(blocks.map((block) => block.kind)).toEqual([
      "steps",
      "line",
      "steps",
    ]);
  });

  it("counts the tool calls but not the thoughts", () => {
    const [block] = blocksOf([
      { id: "1", from: "thinking", text: "Plan." },
      tool("2"),
    ]);

    expect(block.kind === "steps" && toolCount(block.steps)).toBe(1);
  });
});
