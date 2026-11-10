import { describe, expect, it } from "vitest";

import { objectiveStates } from "./learnerState";

describe("objectiveStates", () => {
  it("reads the learner state the app builds", () => {
    const snapshot = {
      student_id: "ST-1",
      objective_states: [
        {
          lesson_objective_id: "lo1",
          band: "remediate",
          questions_correct: 1,
          questions_total: 3,
          misconception_code: "M-ADD",
          misconception_description: "adds the denominators",
        },
        { lesson_objective_id: "lo2", band: "extend" },
      ],
    };

    expect(objectiveStates(snapshot)).toEqual([
      {
        objectiveId: "lo1",
        band: "remediate",
        mastery: "1 of 3 correct",
        misconception: "adds the denominators",
      },
      { objectiveId: "lo2", band: "extend", mastery: null, misconception: null },
    ]);
  });

  it("reads the per-objective map an imported study's generator read", () => {
    const snapshot = {
      "lo-t2w09-01": {
        lesson_objective_id: "lo-t2w09-01",
        mastery: "4 of 4 marked classwork questions correct",
        mastery_band: "extend",
        misconception: null,
      },
      "lo-t2w09-02": {
        mastery_band: "remediate",
        misconception: { code: "BRACKET", description: "drops the sign inside the bracket" },
      },
    };

    expect(objectiveStates(snapshot)).toEqual([
      {
        objectiveId: "lo-t2w09-01",
        band: "extend",
        mastery: "4 of 4 marked classwork questions correct",
        misconception: null,
      },
      {
        objectiveId: "lo-t2w09-02",
        band: "remediate",
        mastery: null,
        misconception: "drops the sign inside the bracket",
      },
    ]);
  });

  it("reads nothing from a missing snapshot", () => {
    expect(objectiveStates(null)).toEqual([]);
    expect(objectiveStates({})).toEqual([]);
  });
});
