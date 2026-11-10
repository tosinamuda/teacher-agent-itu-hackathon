import { expect, it } from "vitest";

import type { LessonStepStructured } from "@/shared/types/lesson-schema";

import type { SessionPlanData } from "../components/SessionPlanView";
import { diffPlans, isUnchanged } from "./planDiff";

const step = (
  id: string,
  title: string,
  teacher: string[] = [],
  minutes = 10,
): LessonStepStructured => ({
  step_id: id,
  type: "explain",
  title,
  duration_minutes: minutes,
  activities: teacher.map((what) => ({ who: "teacher" as const, what })),
});
const plan = (
  steps: LessonStepStructured[],
  over: Partial<SessionPlanData> = {},
): SessionPlanData => ({ steps, ...over });

it("sees nothing when two versions are the same", () => {
  const same = plan([step("s1", "Intro", ["Recall the definitions."])]);

  expect(isUnchanged(diffPlans(same, same))).toBe(true);
});

it("says which field of which step changed, with what it was and what it became", () => {
  const before = plan([
    step("s1", "Convert", ["Model 26/3 with the textbook."]),
  ]);
  const after = plan([
    step("s1", "Convert", ["Model 26/3 on the chart, then with the textbook."]),
  ]);

  const { steps } = diffPlans(before, after);

  expect(steps).toEqual([
    {
      stepId: "s1",
      title: "Convert",
      kind: "changed",
      changes: [
        {
          label: "Teacher",
          before: "• Model 26/3 with the textbook.",
          after: "• Model 26/3 on the chart, then with the textbook.",
        },
      ],
    },
  ]);
});

it("names a step that was added, and one that was removed", () => {
  const before = plan([step("s1", "Intro"), step("s2", "Old step")]);
  const after = plan([
    step("s1", "Intro"),
    step("s3", "New step", ["Ask a question."]),
  ]);

  const { steps } = diffPlans(before, after);

  expect(steps.map((s) => [s.stepId, s.kind])).toEqual([
    ["s3", "added"],
    ["s2", "removed"],
  ]);
});

it("sees a change in the time of a step", () => {
  const { steps } = diffPlans(
    plan([step("s1", "Intro", [], 5)]),
    plan([step("s1", "Intro", [], 8)]),
  );

  expect(steps[0].changes).toEqual([
    { label: "Time", before: "5 min", after: "8 min" },
  ]);
});

it("sees a change in the plan's basis", () => {
  const { overall } = diffPlans(
    plan([], { entry_behaviour: ["Know proper fractions"] }),
    plan([], { entry_behaviour: ["Know proper fractions", "Read a chart"] }),
  );

  expect(overall).toEqual([
    {
      label: "Students already know",
      before: "• Know proper fractions",
      after: "• Know proper fractions\n• Read a chart",
    },
  ]);
});
