import { expect, it } from "vitest";

import { summariseStartOver } from "./startOver";

it("names what is cleared in words, leaving out what is not there", () => {
  expect(
    summariseStartOver({ plan_versions: 1, artefacts: 7, exit_ticket_submissions: 3, content_drafts: 6 }),
  ).toBe("1 plan, 7 materials, 3 learners' results");
});

it("says nothing when the lesson holds nothing", () => {
  expect(summariseStartOver({})).toBe("");
});
