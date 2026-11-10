import { describe, expect, it } from "vitest";

import type { ExperimentSummary } from "../lib/experiments";
import { isOpen } from "./useLessonsToPrepare";

const lesson = (lifecycle_status?: string) => ({ lifecycle_status }) as ExperimentSummary;

describe("isOpen", () => {
  it("keeps a lesson that is active or has no state recorded", () => {
    expect(isOpen(lesson("active"))).toBe(true);
    expect(isOpen(lesson(undefined))).toBe(true);
  });

  it("leaves out a lesson that has ended", () => {
    expect(isOpen(lesson("ended"))).toBe(false);
  });
});
