// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, expect, it } from "vitest";

import type { LearnerResults } from "../types";
import { LearnerResultsView } from "./LearnerResultsView";

afterEach(cleanup);

const RESULTS: LearnerResults = {
  student_id: "S-1",
  full_name: "Adaeze O.",
  tests: [
    {
      lesson_period_id: "p2",
      lesson_title: "Mixed fractions",
      band: "remediate",
      correct: 2,
      out_of: 5,
      taken_at: "2026-11-05T00:00:00Z",
    },
    {
      lesson_period_id: "p1",
      lesson_title: "Intro to fractions",
      band: "reinforce",
      correct: 4,
      out_of: 5,
      taken_at: "2026-11-01T00:00:00Z",
    },
  ],
  objectives: [
    {
      objective_text: "Write a mixed number as an improper fraction",
      lesson_period_id: "p2",
      lesson_title: "Mixed fractions",
      band: "remediate",
      correct: 0,
      out_of: 2,
    },
    {
      objective_text: "Identify proper fractions",
      lesson_period_id: "p1",
      lesson_title: "Intro to fractions",
      band: "extend",
      correct: 3,
      out_of: 3,
    },
  ],
  lessons: [
    {
      lesson_period_id: "p2",
      lesson_title: "Mixed fractions",
      correct: 2,
      out_of: 5,
      band: "remediate",
      revision_note: "to_review",
      revision_note_id: "A-9",
    },
    {
      lesson_period_id: "p1",
      lesson_title: "Intro to fractions",
      correct: 4,
      out_of: 5,
      band: "reinforce",
      revision_note: "approved",
      revision_note_id: "A-8",
    },
    {
      lesson_period_id: "p3",
      lesson_title: "Equivalent fractions",
      correct: null,
      out_of: null,
      band: null,
      revision_note: "waiting_for_test",
      revision_note_id: null,
    },
  ],
};

const renderResults = (results: LearnerResults) =>
  render(
    <MemoryRouter>
      <LearnerResultsView results={results} />
    </MemoryRouter>,
  );

it("links each lesson back to the lesson", () => {
  renderResults(RESULTS);

  const links = screen.getAllByRole("link", { name: "Mixed fractions" });

  expect(links.length).toBe(3);
  expect(links[0].getAttribute("href")).toBe("/research/teacher/lessons/p2");
});

it("names the standing of each objective in words", () => {
  renderResults(RESULTS);

  expect(screen.getByText("Gap")).toBeTruthy();
  expect(screen.getByText("Strength")).toBeTruthy();
});

it("says where the scores are heading", () => {
  renderResults(RESULTS);

  expect(
    screen.getByText("Scores fell from 4 to 2 over the last 2 lessons."),
  ).toBeTruthy();
});

it("says so when the learner has not sat a test", () => {
  renderResults({ ...RESULTS, tests: [], objectives: [] });

  expect(screen.getByText(/has not sat a class test/)).toBeTruthy();
});

it("says where each lesson's revision note stands", () => {
  renderResults(RESULTS);

  expect(
    screen.getByRole("link", { name: "Review" }).getAttribute("href"),
  ).toBe("/research/teacher/pack-reviews/A-9");
  expect(screen.getByText("✓ Approved")).toBeTruthy();
  expect(screen.getByText("○ Waits for the class test")).toBeTruthy();
});
