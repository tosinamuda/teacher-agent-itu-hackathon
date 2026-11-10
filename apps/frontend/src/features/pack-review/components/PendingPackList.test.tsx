// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, expect, it } from "vitest";

import type { PackArtefact } from "../types";
import { PendingPackList } from "./PendingPackList";

afterEach(cleanup);

const pack = {
  artefact_id: "A-1",
  learner_name: "Adaeze O.",
  manifest: { subtopic: "Mixed fractions", subject: "Mathematics", grade: "JSS1", week: 9 },
} as unknown as PackArtefact;

const renderList = (packs: PackArtefact[], isLoading = false) =>
  render(
    <MemoryRouter>
      <PendingPackList packs={packs} isLoading={isLoading} />
    </MemoryRouter>,
  );

it("opens a note from the button on its learner's line", () => {
  renderList([pack]);

  expect(screen.getByText("Adaeze O.")).toBeTruthy();
  expect(screen.getByText("Week 9 · Mixed fractions · Mathematics · JSS1")).toBeTruthy();
  expect(screen.getByRole("link", { name: "Review" }).getAttribute("href")).toBe(
    "/research/teacher/pack-reviews/A-1",
  );
});

it("says no notes are waiting, and when they arrive", () => {
  renderList([]);

  expect(screen.getByText(/No notes are waiting/)).toBeTruthy();
});

it("lists approved notes with an Open button", () => {
  render(
    <MemoryRouter>
      <PendingPackList packs={[pack]} isLoading={false} kind="approved" />
    </MemoryRouter>,
  );

  expect(screen.getByRole("link", { name: "Open" }).getAttribute("href")).toBe("/research/teacher/pack-reviews/A-1");
});
