// @vitest-environment jsdom
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { PlanSourcePicker } from "./PlanSourcePicker";

vi.mock("@/features/experiments/hooks/useExperiments", () => ({
  useExperimentWorkspaces: () => ({
    isError: false,
    data: [
      {
        teacher_workspace_id: "W-1",
        class_name: "JSS1",
        subject_name: "Mathematics",
        term: "Second Term",
        academic_year: "2024/2025",
      },
    ],
  }),
  useExperimentWorkspaceLessons: () => ({
    isLoading: false,
    data: [
      {
        lesson_period_id: "P-1",
        week_number: 9,
        period_number: 3,
        lesson_title: "Coefficients",
        latest_approved_version_id: "LPV-1",
      },
    ],
  }),
}));

afterEach(cleanup);

it("offers another lesson's plan first and a plan file as the other choice", () => {
  render(<PlanSourcePicker onChange={vi.fn()} />);

  expect(
    screen
      .getByRole("button", { name: /Another lesson's plan/ })
      .getAttribute("aria-pressed"),
  ).toBe("true");
  expect(
    screen
      .getByRole("button", { name: /A plan file/ })
      .getAttribute("aria-pressed"),
  ).toBe("false");
  expect(screen.getByLabelText("Class")).toBeTruthy();
  expect(screen.queryByRole("button", { name: "Choose a file" })).toBeNull();
});

it("shows only the file chooser for a plan file, and clears the chosen source when the choice changes", () => {
  const onChange = vi.fn();
  render(<PlanSourcePicker onChange={onChange} />);

  fireEvent.click(screen.getByRole("button", { name: /A plan file/ }));

  expect(screen.getByRole("button", { name: "Choose a file" })).toBeTruthy();
  expect(screen.getByText("No file chosen")).toBeTruthy();
  expect(screen.queryByLabelText("Class")).toBeNull();
  expect(onChange).toHaveBeenLastCalledWith(null);
});

it("gives the plan file as the source and names it", async () => {
  const onChange = vi.fn();
  render(<PlanSourcePicker onChange={onChange} />);
  fireEvent.click(screen.getByRole("button", { name: /A plan file/ }));

  const file = new File(['{"steps":[]}'], "study-week9-plan.json", {
    type: "application/json",
  });
  fireEvent.change(screen.getByLabelText("Plan file"), {
    target: { files: [file] },
  });

  await waitFor(() =>
    expect(onChange).toHaveBeenLastCalledWith({
      kind: "file",
      sessionPlan: { steps: [] },
      fileName: "study-week9-plan.json",
    }),
  );
  expect(screen.getByText("study-week9-plan.json")).toBeTruthy();
  expect(
    screen.getByRole("button", { name: "Choose another file" }),
  ).toBeTruthy();
});

it("gives the chosen lesson's approved plan version as the source", () => {
  const onChange = vi.fn();
  render(<PlanSourcePicker onChange={onChange} />);

  fireEvent.change(screen.getByLabelText("Class"), {
    target: { value: "W-1" },
  });
  fireEvent.change(screen.getByLabelText("Lesson"), {
    target: { value: "P-1" },
  });

  expect(onChange).toHaveBeenLastCalledWith({
    kind: "version",
    planVersionId: "LPV-1",
  });
});

it("has no file choice where only a saved plan can be used", () => {
  render(<PlanSourcePicker allowFile={false} onChange={vi.fn()} />);

  expect(screen.queryByRole("button", { name: /A plan file/ })).toBeNull();
  expect(screen.getByLabelText("Class")).toBeTruthy();
});
