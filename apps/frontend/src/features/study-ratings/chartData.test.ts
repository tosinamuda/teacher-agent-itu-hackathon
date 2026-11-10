import { describe, expect, it } from "vitest";

import { conditionRows, objectiveSeries, part1Rows, part2Rows } from "./chartData";
import { InstrumentCriterion, LessonResults } from "./types";

const criterion = (id: string, name: string): InstrumentCriterion => ({
  id,
  name,
  question: "",
  descriptors: [],
  notes: [],
  better: "",
});

/** Two scores of the same value, from two raters of one cell. */
const scored = (condition: string, criterion_id: string, score: number) => ({
  condition,
  criterion_id,
  mean: score,
  n: 2,
  score_counts: [1, 2, 3, 4, 5].map((point) => (point === score ? 2 : 0)),
  double_rated: 1,
  both_favourable: score >= 4 ? 1 : 0,
});

describe("part1Rows", () => {
  it("puts each condition's mean under its criterion, then all criteria weighted by scores", () => {
    const results: LessonResults = {
      part_1: [
        scored("C0", "curriculum_objective_alignment", 4),
        scored("C3", "curriculum_objective_alignment", 5),
        scored("C3", "custom", 3),
      ],
      part_2: [],
    };

    const rows = part1Rows(results, [
      criterion("curriculum_objective_alignment", "Addresses the objective"),
      criterion("custom", "A criterion with no short name"),
    ]);

    expect(rows).toEqual([
      { criterion: "Objective", C0: 4, C3: 5 },
      { criterion: "A criterion with no short name", C3: 3 },
      { criterion: "All criteria", C0: 4, C3: 4 },
    ]);
  });
});

describe("part2Rows", () => {
  it("gives each outcome's share of a criterion's comparisons", () => {
    const results: LessonResults = {
      part_1: [],
      part_2: [
        { criterion_id: "adaptive_calibration", favoured: "P1", strength: "clearly", count: 3 },
        { criterion_id: "adaptive_calibration", favoured: "neither", strength: null, count: 1 },
      ],
    };

    const [row] = part2Rows(results, [criterion("adaptive_calibration", "Support")]);

    expect(row.criterion).toBe("Support & challenge");
    expect(row.total).toBe(4);
    expect(row["P1 clearly better"]).toBe(75);
    expect(row["About the same"]).toBe(25);
    expect(row["P0 clearly better"]).toBe(0);
  });
});

describe("objectiveSeries and conditionRows", () => {
  it("follows each objective across conditions, and averages objectives equally", () => {
    const series = objectiveSeries([
      {
        lesson: "t3-w05",
        objective_id: "lo2",
        objective_text: "volume",
        condition: "C0",
        mean: 3,
        n: 12,
      },
      {
        lesson: "t3-w05",
        objective_id: "lo1",
        objective_text: null,
        condition: "C0",
        mean: 5,
        n: 2,
      },
      {
        lesson: "t3-w05",
        objective_id: "lo1",
        objective_text: null,
        condition: "C3",
        mean: 4,
        n: 2,
      },
    ]);

    expect(series.map((each) => [each.key, each.text, each.means])).toEqual([
      ["t3-w05 · lo1", "lo1", { C0: 5, C3: 4 }],
      ["t3-w05 · lo2", "volume", { C0: 3 }],
    ]);
    expect(conditionRows(series)).toEqual([
      { condition: "C0", mean: 4, "t3-w05 · lo1": 5, "t3-w05 · lo2": 3 },
      { condition: "C3", mean: 4, "t3-w05 · lo1": 4 },
    ]);
  });
});
