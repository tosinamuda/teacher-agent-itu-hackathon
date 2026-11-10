import { expect, it } from "vitest";

import type { PlanVersionSummary } from "../hooks/useSessionPlans";
import { sourceLabel, statusWord, versionsOfPlan } from "./planVersions";

const summary = (
  version_id: string,
  plan_id: string,
  created_at: string,
): PlanVersionSummary =>
  ({ version_id, plan_id, created_at, status: "draft" }) as PlanVersionSummary;

it("numbers one plan's versions from the oldest, leaving out another plan's", () => {
  const all = [
    summary("V3", "P1", "2026-11-03T00:00:00Z"),
    summary("X1", "P2", "2026-11-02T00:00:00Z"),
    summary("V1", "P1", "2026-11-01T00:00:00Z"),
  ];

  expect(
    versionsOfPlan(all, "P1").map((v) => [v.version_id, v.number]),
  ).toEqual([
    ["V1", 1],
    ["V3", 2],
  ]);
});

it("says how a version came to be", () => {
  expect(sourceLabel("generated")).toBe("Written by the agent");
  expect(sourceLabel("revised")).toBe("Revised");
  expect(sourceLabel("experiment_manual")).toBe("Written for a study");
  expect(sourceLabel(null)).toBe("");
});

it("says where a version stands in words", () => {
  expect(statusWord("withdrawn")).toBe("Approval withdrawn");
  expect(statusWord("odd")).toBe("odd");
});
