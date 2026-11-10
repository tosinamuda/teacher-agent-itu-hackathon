import { expect, it } from "vitest";

import { planChecks } from "./planChecks";

it("says the requirements are met when none is unmet", () => {
  expect(planChecks(undefined)).toEqual([
    { text: "The plan meets the lesson-plan requirements", status: "complete" },
  ]);
  expect(planChecks([])[0].status).toBe("complete");
});

it("lists each unmet requirement as something to look at", () => {
  expect(planChecks(["A step has no activity."])).toEqual([
    { text: "A step has no activity.", status: "needsYou" },
  ]);
});
