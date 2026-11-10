// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import type { PlanDiff } from "../lib/planDiff";
import { AgentChangeBanner } from "./AgentChangeBanner";

afterEach(cleanup);

const diff: PlanDiff = {
  overall: [],
  steps: [
    {
      stepId: "S3",
      title: "Use brackets",
      kind: "changed",
      changes: [
        { label: "Teacher", before: "Models it.", after: "Models it twice." },
      ],
    },
  ],
};

it("says how many steps changed", () => {
  render(
    <AgentChangeBanner
      number={2}
      diff={diff}
      onUndo={vi.fn()}
      isUndoing={false}
    />,
  );

  expect(screen.getByText(/Version 2 · 1 step changed/)).toBeTruthy();
});

it("shows the change beside the old words only when asked", () => {
  render(
    <AgentChangeBanner
      number={2}
      diff={diff}
      onUndo={vi.fn()}
      isUndoing={false}
    />,
  );
  expect(screen.queryByText("Models it twice.")).toBeNull();

  fireEvent.click(screen.getByRole("button", { name: "Compare" }));
  expect(screen.getByText("Models it twice.")).toBeTruthy();

  fireEvent.click(screen.getByRole("button", { name: "Hide" }));
  expect(screen.queryByText("Models it twice.")).toBeNull();
});

it("goes back when asked, and says when it could not", () => {
  const onUndo = vi.fn();
  render(
    <AgentChangeBanner
      number={2}
      diff={diff}
      onUndo={onUndo}
      isUndoing={false}
      error="Couldn't undo."
    />,
  );

  fireEvent.click(screen.getByRole("button", { name: "Undo" }));

  expect(onUndo).toHaveBeenCalledTimes(1);
  expect(screen.getByRole("alert").textContent).toBe("Couldn't undo.");
});
