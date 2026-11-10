import { describe, expect, it } from "vitest";

import type { EditableSessionPlan } from "../api/manualEdit";
import { changeCount, editedStepIds } from "./planEdits";

const plan = (
  over: Partial<Record<string, unknown>> = {},
): EditableSessionPlan =>
  ({
    lesson_plan_objectives: [
      { lesson_objective_id: "O1", objective_text: "Simplify." },
    ],
    entry_behaviour: ["Knows symbols"],
    instructional_materials: [],
    references: [],
    steps: [
      {
        step_id: "S1",
        title: "Recall",
        content: "Recall the symbols.",
        estimated_minutes: 5,
        activities: [
          { who: "teacher", what: "Reviews the symbols." },
          { who: "student", what: "Share an example.", sets_work: false },
        ],
      },
      {
        step_id: "S2",
        title: "Translate",
        content: "",
        estimated_minutes: 15,
        activities: [],
      },
    ],
    ...over,
  }) as unknown as EditableSessionPlan;

const withStep = (index: number, change: Record<string, unknown>) => {
  const next = plan();
  const steps = next.steps as unknown as Record<string, unknown>[];
  steps[index] = { ...steps[index], ...change };
  return next;
};

describe("plan edits", () => {
  it("counts nothing when nothing was changed", () => {
    expect(changeCount(plan(), plan())).toBe(0);
    expect(editedStepIds(plan(), plan())).toEqual([]);
  });

  it("finds the steps whose title, minutes, content or activities changed", () => {
    const before = plan();

    expect(editedStepIds(before, withStep(0, { title: "Recap" }))).toEqual([
      "S1",
    ]);
    expect(
      editedStepIds(before, withStep(1, { estimated_minutes: 20 })),
    ).toEqual(["S2"]);
    expect(editedStepIds(before, withStep(0, { content: "New." }))).toEqual([
      "S1",
    ]);
    expect(
      editedStepIds(
        before,
        withStep(0, {
          activities: [
            { who: "teacher", what: "Reviews the symbols aloud." },
            { who: "student", what: "Share an example.", sets_work: false },
          ],
        }),
      ),
    ).toEqual(["S1"]);
  });

  it("counts each changed objective, step and list once", () => {
    const after = plan({
      lesson_plan_objectives: [
        { lesson_objective_id: "O1", objective_text: "Simplify well." },
      ],
      entry_behaviour: ["Knows symbols", "Knows brackets"],
    });
    (after.steps as unknown as Record<string, unknown>[])[0] = {
      ...(after.steps as unknown as Record<string, unknown>[])[0],
      title: "Recap",
      estimated_minutes: 6,
    };

    expect(changeCount(plan(), after)).toBe(3);
  });
});
