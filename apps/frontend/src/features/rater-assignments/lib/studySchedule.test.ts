import { describe, expect, it } from "vitest";

import type { RatedSet } from "@/features/study-ratings/types";

import { candidateOrder, part1Grid, part2ByLearner, raterLoads } from "./studySchedule";

const set = (overrides: Partial<RatedSet>): RatedSet => ({
  part: 1,
  rater: "rater-1",
  rater_name: "Study rater 1",
  packet: "h1-pkt-001",
  delivery_order: 1,
  note_id: "AT-1",
  condition: "C0",
  draw: 1,
  other_note_id: null,
  learner_id: null,
  state: "complete",
  date_completed: null,
  ...overrides,
});

describe("part1Grid", () => {
  it("places each note's raters by condition and draw, in rater order", () => {
    const grid = part1Grid([
      set({ rater_name: "Study rater 3", condition: "C1", draw: 2 }),
      set({ rater_name: "Study rater 1", condition: "C1", draw: 2 }),
      set({ condition: "C0", draw: 3 }),
    ]);

    expect(grid.conditions).toEqual(["C0", "C1"]);
    expect(grid.draws).toEqual([2, 3]);
    expect(grid.ratedBy("C1", 2).map((rated) => rated.rater_name)).toEqual([
      "Study rater 1",
      "Study rater 3",
    ]);
    expect(grid.ratedBy("C0", 2)).toEqual([]);
  });

  it("leaves out Part 2 sets", () => {
    expect(part1Grid([set({ part: 2, condition: "P1" })]).conditions).toEqual([]);
  });
});

describe("raterLoads", () => {
  it("counts each rater's notes, those that came back short, and the dates they wrote", () => {
    const loads = raterLoads([
      set({ date_completed: "03/09/2026" }),
      set({ state: "partial", date_completed: "03/09/2026" }),
      set({ rater_name: "Study rater 2" }),
    ]);

    expect(loads).toEqual([
      { rater: "Study rater 1", notes: 2, short: 1, dates: ["03/09/2026"] },
      { rater: "Study rater 2", notes: 1, short: 0, dates: [] },
    ]);
  });
});

describe("part2ByLearner", () => {
  it("groups each learner's comparisons, in rater order", () => {
    const learners = part2ByLearner([
      set({ part: 2, learner_id: "ST-1", rater_name: "Study rater 4" }),
      set({ part: 2, learner_id: "ST-1", rater_name: "Study rater 2" }),
      set({ part: 1 }),
    ]);

    expect([...learners.keys()]).toEqual(["ST-1"]);
    expect(learners.get("ST-1")?.map((rated) => rated.rater_name)).toEqual([
      "Study rater 2",
      "Study rater 4",
    ]);
  });
});

describe("candidateOrder", () => {
  it("names both candidates, from the note shown as A", () => {
    expect(candidateOrder(set({ part: 2, condition: "P1" }))).toBe("A: P1 · B: P0");
    expect(candidateOrder(set({ part: 2, condition: "P0" }))).toBe("A: P0 · B: P1");
    expect(candidateOrder(set({ condition: "C0" }))).toBeNull();
  });
});
