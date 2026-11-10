import { describe, expect, it } from "vitest";

import { bothFavourable, favourable, favourableRows, shareOf, spreadRows } from "./proportions";
import { ConditionMean, InstrumentCriterion, LessonResults } from "./types";

const described = (
  condition: string,
  criterion_id: string,
  score_counts: number[],
  double_rated = 0,
  both_favourable = 0,
): ConditionMean => {
  const n = score_counts.reduce((sum, count) => sum + count, 0);
  const total = score_counts.reduce((sum, count, i) => sum + count * (i + 1), 0);
  return { condition, criterion_id, mean: total / n, n, score_counts, double_rated, both_favourable };
};

const criterion = (id: string): InstrumentCriterion => ({
  id,
  name: id,
  question: "",
  descriptors: [],
  notes: [],
  better: "",
});

describe("shares", () => {
  it("counts 4s and 5s as favourable, to one decimal place", () => {
    // The thesis's C0 lesson-context share: 81 of 100 ratings at 4–5.
    expect(favourable(described("C0", "lca", [2, 3, 14, 30, 51]))).toEqual({
      count: 81,
      of: 100,
      percent: 81,
    });
    expect(shareOf(94, 102).percent).toBe(92.2);
  });

  it("reads both raters' favourable cells out of the double-rated ones", () => {
    expect(bothFavourable(described("C3", "lca", [0, 0, 1, 1, 3], 51, 44)).percent).toBe(86.3);
  });

  it("is zero, not a division by zero, with nothing to share", () => {
    expect(shareOf(0, 0).percent).toBe(0);
  });
});

describe("favourableRows", () => {
  it("gives each criterion's favourable percentage by condition, then all criteria pooled", () => {
    const results: LessonResults = {
      part_1: [described("C0", "a", [0, 0, 1, 1, 0]), described("C0", "b", [0, 0, 0, 0, 2])],
      part_2: [],
    };

    expect(favourableRows(results, [criterion("a"), criterion("b")])).toEqual([
      { criterion: "a", C0: 50 },
      { criterion: "b", C0: 100 },
      { criterion: "All criteria", C0: 75 },
    ]);
  });
});

const spread = (...percents: number[]) =>
  Object.fromEntries(percents.map((percent, i) => [`Score ${i + 1}`, percent]));

describe("spreadRows", () => {
  it("gives each score's percentage of a condition's scores, criteria pooled", () => {
    const results: LessonResults = {
      part_1: [described("C3", "a", [0, 0, 1, 1, 2]), described("C0", "a", [1, 0, 0, 0, 1])],
      part_2: [],
    };

    expect(spreadRows(results)).toEqual([
      { condition: "C0", n: 2, ...spread(50, 0, 0, 0, 50) },
      { condition: "C3", n: 4, ...spread(0, 0, 25, 25, 50) },
    ]);
  });
});
