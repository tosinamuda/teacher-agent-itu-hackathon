import { describe, expect, it } from "vitest";

import { cellOf, judgementLabel, ratersOf } from "./ratingGrid";
import { ComparativeJudgement } from "./types";

const judgement = (choice: string, favoured: string | null): ComparativeJudgement => ({
  rater: "rater-3",
  packet: "h2-pkt-002",
  shown_as: "B",
  other_note_id: "AT-P0",
  objective_index: 1,
  lesson_objective_id: "lo1",
  objective_text: null,
  criterion_id: "fit",
  choice,
  favoured_condition: favoured,
  comment: null,
});

describe("ratersOf and cellOf", () => {
  it("lists each rater once, in order, and finds a rater's row on a criterion", () => {
    const rows = [
      { rater: "rater-4", criterion_id: "a", score: 3 },
      { rater: "rater-2", criterion_id: "a", score: 5 },
      { rater: "rater-2", criterion_id: "b", score: 4 },
    ];

    expect(ratersOf(rows)).toEqual(["rater-2", "rater-4"]);
    expect(cellOf(rows, "rater-2", "b")?.score).toBe(4);
    expect(cellOf(rows, "rater-4", "b")).toBeUndefined();
  });
});

describe("judgementLabel", () => {
  it("names the favoured note and how strongly, whichever letter it had", () => {
    expect(judgementLabel(judgement("B slightly better", "P1"))).toBe("P1, slightly");
    expect(judgementLabel(judgement("A clearly better", "P0"))).toBe("P0, clearly");
    expect(judgementLabel(judgement("About the same", "neither"))).toBe("Same");
  });
});
