import { describe, expect, it } from "vitest";

import { outcomeCounts, overallMeans } from "./lessonResults";

const described = (
  condition: string,
  criterion_id: string,
  mean: number,
  score_counts: number[],
  double_rated = 0,
  both_favourable = 0,
) => ({
  condition,
  criterion_id,
  mean,
  n: score_counts.reduce((sum, count) => sum + count, 0),
  score_counts,
  double_rated,
  both_favourable,
});

describe("overallMeans", () => {
  it("weights each criterion by the scores behind it, and pools their counts", () => {
    const overall = overallMeans([
      described("C3", "a", 4, [0, 0, 0, 3, 0], 1, 1),
      described("C3", "b", 2, [0, 1, 0, 0, 0], 1, 0),
      described("C0", "a", 3, [0, 0, 2, 0, 0]),
    ]);

    expect(overall.get("C3")).toEqual(described("C3", "all", 3.5, [0, 1, 0, 3, 0], 2, 1));
    expect(overall.get("C0")?.mean).toBe(3);
  });
});

describe("outcomeCounts", () => {
  it("counts one criterion's comparisons in outcome order, P1's side first", () => {
    const counts = outcomeCounts(
      [
        { criterion_id: "fit", favoured: "P0", strength: "clearly", count: 2 },
        { criterion_id: "fit", favoured: "neither", strength: null, count: 1 },
        { criterion_id: "fit", favoured: "P1", strength: "clearly", count: 4 },
        { criterion_id: "other", favoured: "P1", strength: "slightly", count: 9 },
      ],
      "fit"
    );

    expect(counts).toEqual([4, 0, 1, 0, 2]);
  });
});
