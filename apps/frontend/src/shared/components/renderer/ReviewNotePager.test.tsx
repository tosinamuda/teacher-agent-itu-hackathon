// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it } from "vitest";

import { ReviewNoteSection } from "@/shared/types/review-note";

import { ReviewNotePager } from "./ReviewNotePager";

afterEach(cleanup);

const section = (
  id: string,
  title: string,
  text: string,
): ReviewNoteSection => ({
  step_id: id,
  title,
  blocks: [{ id: `${id}:b0`, type: "explanation", content: text }],
});

it("shows one section at a time and moves with Next and Previous", () => {
  render(
    <ReviewNotePager
      sections={[
        section("s1", "Place value", "First section text."),
        section("s2", "Rounding", "Second section text."),
      ]}
    />,
  );

  expect(screen.getByText("Section 1 of 2")).toBeTruthy();
  expect(screen.getByText("First section text.")).toBeTruthy();
  expect(screen.queryByText("Second section text.")).toBeNull();
  expect(
    (screen.getByRole("button", { name: "Previous" }) as HTMLButtonElement)
      .disabled,
  ).toBe(true);

  fireEvent.click(screen.getByRole("button", { name: "Next" }));

  expect(screen.getByText("Section 2 of 2")).toBeTruthy();
  expect(screen.getByText("Second section text.")).toBeTruthy();
  expect(screen.queryByText("First section text.")).toBeNull();
  expect(
    (screen.getByRole("button", { name: "Next" }) as HTMLButtonElement)
      .disabled,
  ).toBe(true);

  fireEvent.click(screen.getByRole("button", { name: "Previous" }));

  expect(screen.getByText("First section text.")).toBeTruthy();
});

it("has no controls for a note of one section", () => {
  render(<ReviewNotePager sections={[section("s1", "Only", "Just this.")]} />);

  expect(screen.queryByRole("button", { name: "Next" })).toBeNull();
  expect(screen.queryByText(/Section 1 of/)).toBeNull();
  expect(screen.getByText("Just this.")).toBeTruthy();
});
