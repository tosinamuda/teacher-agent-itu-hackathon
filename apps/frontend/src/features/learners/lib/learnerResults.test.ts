import { expect, it } from "vitest";

import type { LearnerTest } from "../types";
import { recentTests, scoreText, trendSentence } from "./learnerResults";

const test = (correct: number | null, out_of: number | null = 5): LearnerTest => ({
  lesson_period_id: "p",
  lesson_title: "Fractions",
  band: "reinforce",
  correct,
  out_of,
  taken_at: "2026-11-04T00:00:00Z",
});

it("reads the latest three tests oldest first", () => {
  const newestFirst = [test(1), test(2), test(3), test(4)];

  expect(recentTests(newestFirst).map((t) => t.correct)).toEqual([3, 2, 1]);
});

it("says scores fell when the newest is below the oldest", () => {
  expect(trendSentence([test(4), test(3), test(2)])).toBe("Scores fell from 4 to 2 over the last 3 lessons.");
});

it("says scores rose, or held", () => {
  expect(trendSentence([test(2), test(4)])).toBe("Scores rose from 2 to 4 over the last 2 lessons.");
  expect(trendSentence([test(3), test(3)])).toBe("Scores held at 3 over the last 2 lessons.");
});

it("says nothing when there is one test or the tests are out of different totals", () => {
  expect(trendSentence([test(3)])).toBeNull();
  expect(trendSentence([test(3, 5), test(2, 4)])).toBeNull();
  expect(trendSentence([test(null, null), test(2)])).toBeNull();
});

it("writes a score, or says the test was taken without one", () => {
  expect(scoreText(2, 5)).toBe("2 of 5");
  expect(scoreText(null, null)).toBe("Taken");
});
