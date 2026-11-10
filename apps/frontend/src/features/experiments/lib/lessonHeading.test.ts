import { describe, expect, it } from "vitest";

import type { ExperimentSummary } from "./experiments";
import { lessonHeading } from "./lessonHeading";

const lesson = (fields: Partial<ExperimentSummary>): ExperimentSummary =>
  ({
    experiment_id: "EXP-1",
    experiment_code: "EXP-CODE",
    subject_name: "Mathematics",
    grade_level: "JSS1",
    term: "Second Term",
    ...fields,
  }) as ExperimentSummary;

describe("lessonHeading", () => {
  it("keeps the lesson's name for the heading and says the rest once, under it", () => {
    const heading = lessonHeading(
      lesson({
        lesson_title:
          "JSS1 Mathematics Week 9 Session 4: Basic arithmetic operations applied to algebraic expressions",
      }),
    );

    expect(heading.name).toBe(
      "Basic arithmetic operations applied to algebraic expressions",
    );
    expect(heading.where).toBe(
      "Mathematics · JSS1 · Second Term · Week 9 · Session 4",
    );
  });

  it("keeps a colon inside the lesson's own name", () => {
    const heading = lessonHeading(
      lesson({
        lesson_title:
          "JSS1 Mathematics Week 2 Session 1: Plane shapes: types and perimeter",
      }),
    );

    expect(heading.name).toBe("Plane shapes: types and perimeter");
  });

  it("leaves a title with no week and session as it is, with the class and subject under it", () => {
    const heading = lessonHeading(
      lesson({ lesson_title: "Prime numbers", term: null }),
    );

    expect(heading).toEqual({
      name: "Prime numbers",
      where: "Mathematics · JSS1",
    });
  });
});
