import { expect, it } from "vitest";

import { closingError } from "./closingError";

it("says nothing when nothing failed", () => {
  expect(closingError(null)).toBeNull();
});

it("says why a plan frozen into a running study cannot be withdrawn", () => {
  const error = new Error(
    '{"detail":"lesson_plan_is_frozen_into_a_running_study"}',
  );

  expect(closingError(error)).toBe(
    "A running study froze this plan, so it cannot be changed.",
  );
});

it("says a plain thing for a reason it does not know", () => {
  expect(closingError(new Error("boom"))).toBe(
    "It could not be done. Try again.",
  );
});
