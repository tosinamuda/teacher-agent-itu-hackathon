// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, expect, it } from "vitest";

import { Status, StatusMark } from "./StatusMark";

afterEach(cleanup);

it("names a lone mark so a screen reader can read the state", () => {
  render(<StatusMark kind="needsYou" />);

  expect(screen.getByRole("img", { name: "Needs you" })).toBeTruthy();
});

it("lets a caller word the lone mark for its own column", () => {
  render(<StatusMark kind="complete" label="Approved" />);

  expect(screen.getByRole("img", { name: "Approved" })).toBeTruthy();
});

it("hides the mark beside a word so the state is read once", () => {
  render(<Status kind="waiting">Waiting for students</Status>);

  expect(screen.getByText("Waiting for students")).toBeTruthy();
  expect(screen.queryByRole("img")).toBeNull();
});
