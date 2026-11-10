import { describe, expect, it } from "vitest";

import { appendLines, type ProgressLine } from "./useProgressLines";

const line = (id: number): ProgressLine => ({
  id,
  kind: "tool",
  data: { tool: "add_part" },
});

describe("appendLines", () => {
  it("puts fresh lines after those already read", () => {
    expect(appendLines([line(1)], [line(2), line(3)]).map((l) => l.id)).toEqual(
      [1, 2, 3],
    );
  });

  it("never shows a line twice", () => {
    expect(
      appendLines([line(1), line(2)], [line(2), line(3)]).map((l) => l.id),
    ).toEqual([1, 2, 3]);
  });

  it("drops what came before a run that starts", () => {
    const start: ProgressLine = { id: 5, kind: "start", data: {} };

    expect(
      appendLines([line(1), line(2)], [start, line(6)]).map((l) => l.id),
    ).toEqual([5, 6]);
  });

  it("keeps only the latest few", () => {
    const many = Array.from({ length: 320 }, (_, index) => line(index + 1));

    const kept = appendLines([], many);

    expect(kept).toHaveLength(300);
    expect(kept[kept.length - 1]?.id).toBe(320);
  });
});
