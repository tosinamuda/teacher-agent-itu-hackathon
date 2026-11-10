import { describe, expect, it } from "vitest";

import { cleaningsOf } from "./studyData";

describe("cleaningsOf", () => {
  it("reads a stated change and its source", () => {
    const header = {
      cleaned: [{ field: "presentation", change: "second line reads 7.5m^2 x 10m", source: "Her line" }],
    };
    expect(cleaningsOf(header)).toEqual([
      { what: "presentation", change: "second line reads 7.5m^2 x 10m", why: "Her line" },
    ]);
  });

  it("reads a from and to, with what was dropped, licensed by a reason", () => {
    const header = {
      cleaning_applied: [
        {
          field: "lesson_plan_objectives",
          from: "3 objectives",
          to: 2,
          dropped: "(iii) calculate capacity",
          reason: "No step teaches it.",
        },
      ],
    };
    expect(cleaningsOf(header)).toEqual([
      {
        what: "lesson plan objectives",
        change: "3 objectives → 2, dropping (iii) calculate capacity",
        why: "No step teaches it.",
      },
    ]);
  });

  it("is empty for a header that lists no changes", () => {
    expect(cleaningsOf({ lesson_key: "t3-w05" })).toEqual([]);
  });
});
