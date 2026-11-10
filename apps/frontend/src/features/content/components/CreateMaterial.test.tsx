// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, expect, it, vi } from "vitest";

import { ContentTypeInfo } from "../types";
import { CreateMaterial } from "./CreateMaterial";

const generation = vi.hoisted(() => ({
  state: {
    create: vi.fn(),
    isPending: false,
    isError: false,
    failure: null as string | null,
  },
  lines: [] as { id: number; kind: string; data: Record<string, unknown> }[],
}));

vi.mock("../hooks/useContent", () => ({
  useGenerateContent: () => generation.state,
}));
vi.mock("../hooks/useGenerationProgress", () => ({
  useGenerationProgress: () => generation.lines,
}));

const deck = {
  type: "slide-deck",
  label: "Slides",
  engine: "mcp",
  spec: {
    revision: 30,
    material: "the slides for one step of a lesson",
    audience: "the class",
    structure: ["a cover"],
    requirements: ["at most four points"],
    adaptable: [],
  },
} as unknown as ContentTypeInfo;

beforeEach(() => {
  generation.state = {
    create: vi.fn(),
    isPending: false,
    isError: false,
    failure: null,
  };
  generation.lines = [];
});
afterEach(cleanup);

const row = () => (
  <ul>
    <CreateMaterial info={deck} planVersionId="LPV-1" noteApproved />
  </ul>
);

it("shows a name, a status and one button, with the rest out of the way", () => {
  render(row());

  expect(screen.getByText("Slides")).toBeTruthy();
  expect(screen.getByText("Not created")).toBeTruthy();
  expect(screen.getByRole("button", { name: "Create it" })).toBeTruthy();
  expect(screen.queryByRole("textbox")).toBeNull();
  expect(screen.getByText("Details")).toBeTruthy();
});

it("opens the instructions box only when asked, and sends what was typed", () => {
  render(row());

  fireEvent.click(screen.getByText("Add instructions"));
  fireEvent.change(screen.getByRole("textbox"), { target: { value: " shorter " } });
  fireEvent.click(screen.getByRole("button", { name: "Create it" }));

  expect(generation.state.create).toHaveBeenCalledWith({
    sources: undefined,
    instructions: "shorter",
  });
});

it("keeps the agent's work and says why it stopped, with a way to try again", () => {
  generation.state.failure =
    "the writer left issues: ['step02: slide 2 has 5 points']";
  generation.lines = [{ id: 1, kind: "agent_text", data: { part_id: "t", text: "One check is open." } }];

  render(row());

  expect(screen.getByText("The agent could not finish the slides")).toBeTruthy();
  expect(screen.getByText("The checks still found: step02: slide 2 has 5 points")).toBeTruthy();
  expect(screen.getByRole("button", { name: "Try again" })).toBeTruthy();
});

it("says only that it failed when the agent never started", () => {
  generation.state.isError = true;

  render(row());

  expect(screen.getByText("Couldn't create it. Try again.")).toBeTruthy();
});
