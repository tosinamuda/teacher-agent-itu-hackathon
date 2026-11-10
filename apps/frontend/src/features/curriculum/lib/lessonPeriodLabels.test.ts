import { describe, expect, it } from "vitest";

import { lessonPeriodSubtitle } from "./lessonPeriodLabels";

describe("lessonPeriodSubtitle", () => {
  it("drops a subtopic that only differs from the title in capitals", () => {
    expect(
      lessonPeriodSubtitle({
        title: "Meaning of Fraction",
        subtopic_title: "Meaning of fraction",
        subtopic_id: "jss1-math-fractions-meaning-of-fraction",
      })
    ).toBeNull();
  });

  it("keeps a subtopic that names more than the title", () => {
    expect(
      lessonPeriodSubtitle({
        title: "Millions",
        subtopic_title: "Millions and billions",
        subtopic_id: "jss1-math-whole-numbers-millions-and-billions",
      })
    ).toBe("Millions and billions");
  });

  it("falls back to the subtopic id, then to a note that none is assigned", () => {
    expect(
      lessonPeriodSubtitle({ title: "Period 1", subtopic_title: null, subtopic_id: "st-1" })
    ).toBe("st-1");
    expect(
      lessonPeriodSubtitle({ title: "Period 1", subtopic_title: null, subtopic_id: null })
    ).toBe("No subtopic assigned");
  });
});
