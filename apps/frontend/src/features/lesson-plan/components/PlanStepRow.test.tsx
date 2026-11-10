// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, expect, it } from "vitest";

import type { LessonStepStructured } from "@/shared/types/lesson-schema";

import { PlanStepRow } from "./PlanStepRow";

afterEach(cleanup);

const step = {
  step_id: "S3",
  type: "core",
  title: "Use brackets",
  estimated_minutes: 20,
  activities: [],
} as LessonStepStructured;

const open = (mark?: "changed" | "revising") =>
  render(
    <PlanStepRow
      step={step}
      number={3}
      share={40}
      open={false}
      onToggle={() => undefined}
      mark={mark}
    />,
  );

it("says nothing more about a step the agent has not touched", () => {
  open();

  expect(screen.queryByText("Changed")).toBeNull();
  expect(screen.queryByText("The agent is changing this")).toBeNull();
});

it("marks a step the agent changed", () => {
  open("changed");

  expect(screen.getByText("Changed")).toBeTruthy();
});

it("marks the step the agent is changing now", () => {
  open("revising");

  expect(screen.getByText("The agent is changing this")).toBeTruthy();
});
