// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { PlanDocument } from "./PlanDocument";
import type { SessionPlanData } from "./SessionPlanView";

vi.mock("../hooks/useTypesetMath", () => ({ useTypesetMath: () => undefined }));
vi.mock("@/shared/components/references/SourceReferences", () => ({
  SourceReferences: ({ references }: { references: string[] }) => (
    <span>{references.join("; ")}</span>
  ),
}));

afterEach(cleanup);

const PLAN = {
  lesson_plan_objectives: [
    {
      lesson_objective_id: "O1",
      objective_text: "Convert improper fractions.",
    },
  ],
  entry_behaviour: ["Proper fractions", "Fraction charts"],
  instructional_materials: ["Charts", "Textbook p. 42"],
  references: ["Scheme of work, week 1"],
  steps: [
    {
      step_id: "s1",
      type: "intro",
      title: "Activate prior knowledge",
      duration_minutes: 5,
      activities: [
        { who: "teacher", what: "Prompt students to recall." },
        { who: "student", what: "Classify three fractions." },
      ],
    },
    {
      step_id: "s2",
      type: "core",
      title: "Improper to mixed",
      duration_minutes: 20,
      activities: [],
    },
  ],
} as unknown as SessionPlanData;

it("sets out the objectives and what the plan is based on", () => {
  render(<PlanDocument sessionPlan={PLAN} />);

  expect(screen.getByText("Convert improper fractions.")).toBeTruthy();
  expect(screen.getByText("Proper fractions, Fraction charts")).toBeTruthy();
  expect(screen.getByText("Charts, Textbook p. 42")).toBeTruthy();
  expect(screen.getByText("Scheme of work, week 1")).toBeTruthy();
});

it("puts what the teacher does beside what the students do, step by step", () => {
  render(<PlanDocument sessionPlan={PLAN} />);

  expect(screen.getByText("Prompt students to recall.")).toBeTruthy();
  expect(screen.getByText("Classify three fractions.")).toBeTruthy();
  expect(screen.getAllByText("5 min").length).toBeGreaterThan(0);
});

it("opens the first step and leaves the others closed", () => {
  const { container } = render(<PlanDocument sessionPlan={PLAN} />);
  const steps = [
    ...container.querySelectorAll<HTMLDetailsElement>("details[data-step-id]"),
  ];

  expect(steps.map((step) => step.open)).toEqual([true, false]);
});

it("opens every step, then closes them, from one control", () => {
  const { container } = render(<PlanDocument sessionPlan={PLAN} />);
  const steps = () => [
    ...container.querySelectorAll<HTMLDetailsElement>("details[data-step-id]"),
  ];

  fireEvent.click(screen.getByRole("button", { name: "Expand all" }));
  expect(steps().map((step) => step.open)).toEqual([true, true]);

  fireEvent.click(screen.getByRole("button", { name: "Collapse all" }));
  expect(steps().map((step) => step.open)).toEqual([false, false]);
});

it("keeps what the plan is based on closed until it is asked for", () => {
  const { container } = render(<PlanDocument sessionPlan={PLAN} />);
  const basis = container.querySelector<HTMLDetailsElement>(
    'details[aria-label="Basis for the plan"]',
  );

  expect(basis?.open).toBe(false);
});
