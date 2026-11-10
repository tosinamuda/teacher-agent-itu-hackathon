// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, expect, it } from "vitest";

import { PlanDiffView } from "./PlanDiffView";

afterEach(cleanup);

it("says when two versions do not differ", () => {
  render(<PlanDiffView diff={{ overall: [], steps: [] }} />);

  expect(
    screen.getByText("Nothing differs between these two versions."),
  ).toBeTruthy();
});

it("sets what a step was beside what it became", () => {
  render(
    <PlanDiffView
      diff={{
        overall: [],
        steps: [
          {
            stepId: "s1",
            title: "Convert",
            kind: "changed",
            changes: [{ label: "Teacher", before: "Old.", after: "New." }],
          },
        ],
      }}
    />,
  );

  expect(screen.getByText("Convert", { exact: false }).textContent).toContain(
    "Changed",
  );
  expect(screen.getByText("Old.")).toBeTruthy();
  expect(screen.getByText("New.")).toBeTruthy();
});

it("names a step that was removed, with nothing to compare", () => {
  render(
    <PlanDiffView
      diff={{
        overall: [],
        steps: [
          { stepId: "s2", title: "Old step", kind: "removed", changes: [] },
        ],
      }}
    />,
  );

  expect(screen.getByText("Old step", { exact: false }).textContent).toContain(
    "Removed",
  );
});
