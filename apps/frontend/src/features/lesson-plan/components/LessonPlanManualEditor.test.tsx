// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import type { EditableSessionPlan } from "../api/manualEdit";
import { LessonPlanManualEditor } from "./LessonPlanManualEditor";

afterEach(cleanup);

const plan = {
  lesson_plan_objectives: [
    { lesson_objective_id: "O1", objective_text: "Simplify." },
  ],
  entry_behaviour: [],
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
  ],
} as unknown as EditableSessionPlan;

const open = (onSave = vi.fn()) => {
  render(
    <LessonPlanManualEditor
      sessionPlan={plan}
      onSave={onSave}
      onCancel={vi.fn()}
      isSaving={false}
    />,
  );
  return onSave;
};

it("cannot save until something is changed", () => {
  open();

  expect(screen.getByText("No changes")).toBeTruthy();
  expect(
    (screen.getByRole("button", { name: "Save edits" }) as HTMLButtonElement)
      .disabled,
  ).toBe(true);
});

it("marks an edited step and counts the change", () => {
  open();

  fireEvent.change(screen.getByLabelText("Step 1 title"), {
    target: { value: "Recap" },
  });

  expect(screen.getByText("Edited")).toBeTruthy();
  expect(screen.getByText("1 change")).toBeTruthy();
});

it("saves the edited minutes and activity text, keeping what was not touched", () => {
  const onSave = open();

  fireEvent.change(screen.getByLabelText("Step 1 minutes"), {
    target: { value: "8" },
  });
  fireEvent.change(screen.getByLabelText("Teacher does, 1"), {
    target: { value: "Reviews the symbols aloud." },
  });
  fireEvent.click(screen.getByRole("button", { name: "Save edits" }));

  const saved = onSave.mock.calls[0][0] as unknown as {
    steps: {
      estimated_minutes: number;
      activities: { what: string; sets_work?: boolean }[];
    }[];
  };
  expect(saved.steps[0].estimated_minutes).toBe(8);
  expect(saved.steps[0].activities[0].what).toBe("Reviews the symbols aloud.");
  expect(saved.steps[0].activities[1]).toMatchObject({
    what: "Share an example.",
    sets_work: false,
  });
});
