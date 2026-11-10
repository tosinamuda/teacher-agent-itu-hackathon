import { describe, expect, it } from "vitest";

import { withoutInternalIds } from "./revisionSummary";

describe("withoutInternalIds", () => {
  it.each([
    [
      'Replaced the pizza example in step "intro01" with a shaded bar of \\(\\frac{3}{5}\\).',
      "Replaced the pizza example with a shaded bar of \\(\\frac{3}{5}\\).",
    ],
    [
      "Replaced the improper mixed-number practice question in section step:step02 with a proper mixed number.",
      "Replaced the improper mixed-number practice question with a proper mixed number.",
    ],
    [
      "Added a second short worked example to the intro01 step.",
      "Added a second short worked example.",
    ],
    [
      "Added a second short worked example (common factors of 8 and 20) to the step01 section.",
      "Added a second short worked example (common factors of 8 and 20).",
    ],
    ["Simplified the wording of lop02 (core03).", "Simplified the wording."],
  ])("drops the ids from %j", (summary, readable) => {
    expect(withoutInternalIds(summary)).toBe(readable);
  });

  it("leaves a summary without ids as it is", () => {
    const summary =
      "Reduced step 2 to 18 minutes, keeping the 45-minute lesson.";
    expect(withoutInternalIds(summary)).toBe(summary);
  });

  it("leaves no empty bold behind when the id was a list item's label", () => {
    expect(
      withoutInternalIds(
        "- **intro01** — opens with the note's Example 1.\n- **step01** — the note's four steps.",
      ),
    ).toBe("- opens with the note's Example 1.\n- the note's four steps.");
  });

  it("keeps the bold of a label that is not an id", () => {
    expect(withoutInternalIds("- **step-evaluation** — the two rules.")).toBe(
      "- **step-evaluation** — the two rules.",
    );
  });

  it("keeps the line breaks that markdown needs for headings and lists", () => {
    expect(withoutInternalIds("Done.\n\n## What changed\n\n- one\n- two")).toBe(
      "Done.\n\n## What changed\n\n- one\n- two",
    );
  });
});
