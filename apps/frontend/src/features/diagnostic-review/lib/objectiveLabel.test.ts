import { describe, expect, it } from "vitest";

import { humaniseMisconceptionCode } from "@/shared/utils/misconception";

import { objectiveLabel } from "./objectiveLabel";

const OBJECTIVES = [
  { lesson_objective_id: "lop01", objective_text: "Name the parts of a fraction.", objective_order: 1 },
  { lesson_objective_id: "lop02", objective_text: "Tell proper from improper fractions." },
];

describe("a class test question's labels", () => {
  it("names the objective by its number and text, never its id", () => {
    expect(objectiveLabel(OBJECTIVES, "lop01")).toBe("Objective 1: Name the parts of a fraction.");
    expect(objectiveLabel(OBJECTIVES, "lop02")).toBe(
      "Objective 2: Tell proper from improper fractions."
    );
  });

  it("names no objective the plan does not have", () => {
    expect(objectiveLabel(OBJECTIVES, "lop09")).toBeNull();
  });

  it("reads a misconception code as words", () => {
    expect(humaniseMisconceptionCode("fraction_equal_one_misconception")).toBe(
      "Fraction equal one misconception"
    );
  });
});
