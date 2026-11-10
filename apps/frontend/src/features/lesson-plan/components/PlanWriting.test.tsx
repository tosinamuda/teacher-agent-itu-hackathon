// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, expect, it } from "vitest";

import { PlanWriting } from "./PlanWriting";

afterEach(cleanup);

const open = (outline: Parameters<typeof PlanWriting>[0]["outline"]) =>
  render(
    <MemoryRouter>
      <PlanWriting title="Quantitative reasoning" outline={outline} />
    </MemoryRouter>,
  );

it("shows only the title and what is still to come before anything is written", () => {
  open(null);

  expect(
    screen.getByRole("heading", { name: "Quantitative reasoning" }),
  ).toBeTruthy();
  expect(screen.queryByRole("heading", { name: "Objectives" })).toBeNull();
  expect(screen.queryByRole("heading", { name: "Steps" })).toBeNull();
});

it("shows the objectives and steps as they are written, with their minutes", () => {
  open({
    objectives: ["Translate word problems."],
    steps: [
      { title: "Recall", minutes: 5 },
      { title: "Translate", minutes: null },
    ],
    written: 2,
    total: 3,
  });

  expect(screen.getByText("• Translate word problems.")).toBeTruthy();
  expect(screen.getByText("Recall")).toBeTruthy();
  expect(screen.getByText("5 min")).toBeTruthy();
  expect(screen.getByText("Translate")).toBeTruthy();
  expect(screen.getAllByRole("listitem").length).toBeGreaterThan(3);
});
