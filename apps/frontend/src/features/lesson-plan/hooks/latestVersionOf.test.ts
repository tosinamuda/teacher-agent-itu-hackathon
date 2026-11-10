import { afterEach, expect, it, vi } from "vitest";

import { apiFetch } from "@/shared/api/client";

import { latestVersionOf } from "./usePlanGenerator";

vi.mock("@/shared/api/client", () => ({ apiFetch: vi.fn() }));

afterEach(() => vi.mocked(apiFetch).mockReset());

const plan = (version_id: string) => ({ plan_id: "LP-1", version_id });

it("shows a plan opened by its own id as it is", async () => {
  vi.mocked(apiFetch).mockResolvedValueOnce(plan("LPV-2"));

  expect(await latestVersionOf("LP-1")).toEqual(plan("LPV-2"));
  expect(apiFetch).toHaveBeenCalledTimes(1);
});

it("shows the plan's latest version when opened by an older version's id", async () => {
  vi.mocked(apiFetch)
    .mockResolvedValueOnce(plan("LPV-1"))
    .mockResolvedValueOnce(plan("LPV-2"));

  expect(await latestVersionOf("LPV-1")).toEqual(plan("LPV-2"));
  expect(vi.mocked(apiFetch).mock.calls[1]?.[0]).toBe(
    "/artefacts/lesson-plans/LP-1",
  );
});
