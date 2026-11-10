import { expect, it } from "vitest";

import { clock } from "./LiveWork";

it("shows seconds as minutes and seconds", () => {
  expect([0, 9, 65, 600, 3725].map(clock)).toEqual([
    "0:00",
    "0:09",
    "1:05",
    "10:00",
    "62:05",
  ]);
});
