import { expect, it } from "vitest";

import { runningLine, toolLine } from "./toolLine";
import type { Line } from "./transcript";

const tool = (
  fields: Partial<Extract<Line, { from: "tool" }>>,
): Extract<Line, { from: "tool" }> => ({
  id: "e1",
  from: "tool",
  tool: "add_part",
  failed: false,
  ...fields,
});

it("names the lesson's own part and an objective's part", () => {
  expect(toolLine(tool({ unit: "lesson" }))).toBe(
    "Wrote the lesson's own part",
  );
  expect(
    toolLine(
      tool({ tool: "revise_part", unit: "jss1-math-whole-numbers-po02" }),
    ),
  ).toBe("Revised objective 2's part");
});

it("names the skill loaded and the file read", () => {
  expect(
    toolLine(tool({ tool: "skill", detail: "writing-lesson-plans" })),
  ).toBe("Loaded the skill \u201cwriting-lesson-plans\u201d");
  expect(
    toolLine(
      tool({
        tool: "read",
        detail: "writing-lesson-plans/references/steps.md",
      }),
    ),
  ).toBe("Read writing-lesson-plans/references/steps.md");
});

it("keeps another content type's unit and says what it does not know as it is named", () => {
  expect(toolLine(tool({ unit: "s2" }))).toBe("Wrote part s2");
  expect(toolLine(tool({ tool: "other" }))).toBe("other");
});

it("says a running tool in the present tense", () => {
  expect(runningLine("revise_part")).toBe("Revising a part");
  expect(runningLine("something_new")).toBe("something_new");
});

it("says a text search as a person would", () => {
  expect(runningLine("locate_text")).toBe("Looking for the selected text");
});
