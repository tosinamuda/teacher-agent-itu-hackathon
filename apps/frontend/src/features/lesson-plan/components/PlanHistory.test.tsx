// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import type { PlanGenerationResponse } from "../hooks/usePlanGenerator";
import type { PlanVersionSummary } from "../hooks/useSessionPlans";
import { PlanHistory } from "./PlanHistory";

const state = vi.hoisted(() => ({ summaries: [] as unknown[] }));

vi.mock("../hooks/useSessionPlans", () => ({
  useSessionPlans: () => ({ data: state.summaries }),
}));
vi.mock("../hooks/usePlanVersion", () => ({
  usePlanVersion: (id: string) => ({
    data: {
      session_plan: {
        steps: [
          {
            step_id: "s1",
            type: "explain",
            title: "Convert",
            activities: [
              {
                who: "teacher",
                what: id === "V1" ? "Use the textbook." : "Use the chart.",
              },
            ],
          },
        ],
      },
    },
  }),
}));

afterEach(cleanup);

const version = (
  version_id: string,
  created_at: string,
  source_type: string,
  status = "approved",
) =>
  ({
    plan_id: "P1",
    version_id,
    created_at,
    source_type,
    status,
  }) as unknown as PlanVersionSummary;
const plan = {
  plan_id: "P1",
  version_id: "V2",
  session_id: "S1",
} as PlanGenerationResponse;

it("shows nothing for a plan with one version", () => {
  state.summaries = [version("V1", "2026-11-01T00:00:00Z", "generated")];
  const { container } = render(<PlanHistory plan={plan} />);

  expect(container.textContent).toBe("");
});

it("lists the versions newest first, saying how each came to be", () => {
  state.summaries = [
    version("V1", "2026-11-01T00:00:00Z", "generated"),
    version("V2", "2026-11-02T00:00:00Z", "revised", "draft"),
  ];
  render(<PlanHistory plan={plan} />);

  const rows = screen.getAllByRole("listitem").map((row) => row.textContent);

  expect(rows[0]).toContain("Version 2 · current");
  expect(rows[0]).toContain("Revised · Draft · 2026-11-02");
  expect(rows[1]).toContain("Written by the agent");
});

it("shows what a version changed against the one before it", () => {
  state.summaries = [
    version("V1", "2026-11-01T00:00:00Z", "generated"),
    version("V2", "2026-11-02T00:00:00Z", "revised"),
  ];
  render(<PlanHistory plan={plan} />);

  fireEvent.click(screen.getByRole("button", { name: "What changed" }));

  expect(screen.getByText("• Use the textbook.")).toBeTruthy();
  expect(screen.getByText("• Use the chart.")).toBeTruthy();
  expect(screen.getByText("Version 1 to version 2")).toBeTruthy();
});
