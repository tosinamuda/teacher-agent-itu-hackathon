import { describe, expect, it } from "vitest";

import { ExperimentExecution } from "./experiments";
import { studyDraws, studyRunOf } from "./studyRecord";

const execution = (
  attempt: number,
  runtime_snapshot: Record<string, unknown> | null,
): ExperimentExecution => ({
  execution_id: `EX-${attempt}`,
  experiment_id: "EXP-1",
  hypothesis: "H1",
  attempt_number: attempt,
  status: "succeeded",
  runtime_snapshot,
});

const imported = (attempt: number) => execution(attempt, { study_run: "c0c3-prism-objective" });

describe("studyRunOf", () => {
  it("names the study run an imported execution came from", () => {
    expect(studyRunOf(imported(1))).toBe("c0c3-prism-objective");
  });

  it("is null for an execution generated in the app", () => {
    expect(studyRunOf(execution(1, { trigger: "teacher_create_review_note" }))).toBeNull();
    expect(studyRunOf(execution(1, null))).toBeNull();
  });
});

describe("studyDraws", () => {
  it("lists every imported draw, oldest first", () => {
    const draws = studyDraws([imported(3), imported(1), imported(2)]);
    expect(draws?.map((draw) => draw.attempt_number)).toEqual([1, 2, 3]);
  });

  it("is null when any execution was generated in the app", () => {
    expect(studyDraws([imported(1), execution(2, null)])).toBeNull();
  });

  it("is null when there are no executions", () => {
    expect(studyDraws([])).toBeNull();
  });
});
