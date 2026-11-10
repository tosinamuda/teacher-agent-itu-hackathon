// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { CreationsInProgress } from "./CreationsInProgress";

const state = vi.hoisted(() => ({ creations: [] as unknown[] }));

vi.mock("../hooks/useCreationsInProgress", () => ({
  useCreationsInProgress: () => state.creations,
}));
vi.mock("@/features/content/hooks/useContent", () => ({
  useGenerateContent: () => ({ failure: "job_failed" }),
}));
vi.mock("@/features/content/hooks/useGenerationProgress", () => ({
  useGenerationProgress: () => [],
}));
vi.mock("@/features/content-chat/LiveWork", () => ({
  LiveWork: ({ title }: { title: string }) => <p>{title}</p>,
}));

afterEach(() => {
  cleanup();
  state.creations = [];
});

const creation = (type: string, label: string, over: object = {}) => ({
  info: { type, label },
  running: true,
  stopped: false,
  ...over,
});

it("shows nothing when the agent is writing nothing", () => {
  const { container } = render(<CreationsInProgress planVersionId="LPV-1" />);

  expect(container.textContent).toBe("");
});

it("lists each material being written, with the first open and the rest only named", () => {
  state.creations = [
    creation("slide-deck", "Slides"),
    creation("exam-questions", "Exam questions"),
  ];
  render(<CreationsInProgress planVersionId="LPV-1" />);

  expect(screen.getAllByRole("button").map((row) => row.textContent)).toEqual([
    "SlidesWriting",
    "Exam questionsWriting",
  ]);
  expect(screen.getByText("The agent is writing the slides")).toBeTruthy();
  expect(
    screen.queryByText("The agent is writing the exam questions"),
  ).toBeNull();
});

it("opens one row at a time, and closes the open one when it is chosen again", () => {
  state.creations = [
    creation("slide-deck", "Slides"),
    creation("exam-questions", "Exam questions"),
  ];
  render(<CreationsInProgress planVersionId="LPV-1" />);

  fireEvent.click(screen.getByRole("button", { name: /Exam questions/ }));

  expect(
    screen.getByText("The agent is writing the exam questions"),
  ).toBeTruthy();
  expect(screen.queryByText("The agent is writing the slides")).toBeNull();

  fireEvent.click(screen.getByRole("button", { name: /Exam questions/ }));

  expect(
    screen.queryByText("The agent is writing the exam questions"),
  ).toBeNull();
});

it("says a material the agent stopped on, with the reason when opened", () => {
  state.creations = [
    creation("slide-deck", "Slides", { running: false, stopped: true }),
  ];
  render(<CreationsInProgress planVersionId="LPV-1" />);

  expect(screen.getByText("Stopped")).toBeTruthy();
  expect(
    screen.getByText("The agent could not finish the slides"),
  ).toBeTruthy();
});
