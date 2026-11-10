// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, expect, it } from "vitest";

import type { LessonStepStructured } from "@/shared/types/lesson-schema";

import { SessionPlanView, type SessionPlanData } from "./SessionPlanView";

afterEach(cleanup);

const step = (
  id: string,
  title: string,
  teacher: string,
): LessonStepStructured =>
  ({
    step_id: id,
    title,
    duration_minutes: 10,
    activities: [{ who: "teacher", what: teacher }],
  }) as unknown as LessonStepStructured;

const plan: SessionPlanData = {
  steps: [
    step(
      "intro01",
      "Activating prior knowledge",
      "Prompt students to recall fractions.",
    ),
    step(
      "step01",
      "Convert improper fractions",
      "Explain the four-step algorithm.",
    ),
    step("step02", "Convert mixed fractions", "Demonstrate the short method."),
  ],
  lesson_plan_objectives: [
    {
      lesson_objective_id: "lo1",
      objective_text: "Convert improper fractions to mixed fractions.",
      objective_order: 1,
      curriculum_objective_id: "c1",
      curriculum_objective_text: "Convert fractions",
      kc_type: "procedure",
      kc_focus: "conversion",
    },
  ],
  entry_behaviour: ["Classify fractions as proper or improper"],
  instructional_materials: ["Fraction charts"],
};

it("shows every step open, with what the teacher does, and no paging", () => {
  render(<SessionPlanView sessionPlan={plan} />);

  for (const title of [
    "Activating prior knowledge",
    "Convert improper fractions",
    "Convert mixed fractions",
  ]) {
    expect(screen.getByText(title)).toBeTruthy();
  }
  expect(screen.getByText("Explain the four-step algorithm.")).toBeTruthy();
  expect(screen.queryByRole("button", { name: "Next" })).toBeNull();
  expect(screen.queryByText(/Overview ·/)).toBeNull();
});

it("shows the objectives and the basis for the plan, with nothing folded away", () => {
  const { container } = render(<SessionPlanView sessionPlan={plan} />);

  expect(
    screen.getByText("Convert improper fractions to mixed fractions."),
  ).toBeTruthy();
  expect(container.querySelector("details")).toBeNull();
  const basis = screen.getByRole("region", { name: "Basis for the plan" });
  expect(basis.textContent).toContain("Students already know");
  expect(basis.textContent).toContain("Fraction charts");
});

it("says how many steps there are", () => {
  render(<SessionPlanView sessionPlan={plan} />);

  expect(screen.getByRole("heading", { name: /Steps/ }).textContent).toContain(
    "3",
  );
});
