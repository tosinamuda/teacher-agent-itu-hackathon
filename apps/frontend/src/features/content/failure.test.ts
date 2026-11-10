import { describe, expect, it } from "vitest";

import { failureLine } from "./failure";

describe("failureLine", () => {
  it("says the first check the agent left unfixed", () => {
    expect(
      failureLine(
        "the writer left issues: ['step02: slide 2 has 5 points; put the rest on the next slide']",
      ),
    ).toBe(
      "The checks still found: step02: slide 2 has 5 points; put the rest on the next slide",
    );
  });

  it("says how many more there are, and reads an issue quoted with double quotes", () => {
    expect(
      failureLine(
        `the writer left issues: ["step01: don't repeat", 'step02: too long', 'step03: no figure']`,
      ),
    ).toBe("The checks still found: step01: don't repeat (and 2 more)");
  });

  it("leaves any other reason as the server gave it", () => {
    expect(failureLine("the agent stopped")).toBe("the agent stopped");
  });
});
