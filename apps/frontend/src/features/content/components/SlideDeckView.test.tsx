// @vitest-environment jsdom
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it } from "vitest";

import { slidesOf } from "../slideDeck";
import { EngineManifest } from "../types";
import { SlideDeckView } from "./SlideDeckView";

afterEach(cleanup);

const manifest = (sections: EngineManifest["sections"]): EngineManifest => ({
  content_type: "slide-deck",
  plan_version_id: "LPV-1",
  unit: "plan_step",
  sections,
});

const step = (id: string, label: string, ...titles: string[]) => ({
  unit_id: id,
  label,
  part: {
    slides: titles.map((title) => ({
      title,
      points: [{ point: `${title} point` }],
      speaker_notes: `${title} notes for the teacher`,
    })),
  },
});

const deck = manifest([
  step("s1", "Introduction", "What we learn", "What it builds on"),
  step("s2", "Core teaching", "The rule"),
]);

it("flattens the steps' slides in the order they are shown, each knowing its step", () => {
  expect(slidesOf(deck).map((slide) => [slide.title, slide.step])).toEqual([
    ["What we learn", "Introduction"],
    ["What it builds on", "Introduction"],
    ["The rule", "Core teaching"],
  ]);
});

it("starts with the cover the app set, its objectives on it", () => {
  const covered: EngineManifest = {
    ...deck,
    cover: {
      title: "Estimating distances",
      subtitle: "Mathematics · JSS1",
      objectives: ["Estimate a distance from steps"],
    },
  };

  const [cover, first] = slidesOf(covered);

  expect(cover).toEqual({
    title: "Estimating distances",
    points: ["Mathematics · JSS1"],
    figure: null,
    notes: "",
    step: "Cover",
    cover: true,
    objectives: ["Estimate a distance from steps"],
  });
  expect(first.title).toBe("What we learn");
  expect(slidesOf(deck)).toHaveLength(3);
});

it("shows one slide at a time with its notes, and moves across steps with Next", () => {
  render(
    <QueryClientProvider client={new QueryClient()}>
      <SlideDeckView manifest={deck} />
    </QueryClientProvider>,
  );

  expect(screen.getByText("Slide 1 of 3 · Introduction")).toBeTruthy();
  expect(screen.getByRole("heading", { name: "What we learn" })).toBeTruthy();
  expect(screen.getByText("What we learn notes for the teacher")).toBeTruthy();
  expect(screen.queryByRole("heading", { name: "The rule" })).toBeNull();

  fireEvent.click(screen.getByText("Next"));
  fireEvent.click(screen.getByText("Next"));

  expect(screen.getByText("Slide 3 of 3 · Core teaching")).toBeTruthy();
  expect(screen.getByRole("heading", { name: "The rule" })).toBeTruthy();
});

it("lists every slide as a thumbnail, marks the one shown, and shows the one picked", () => {
  render(
    <QueryClientProvider client={new QueryClient()}>
      <SlideDeckView manifest={deck} />
    </QueryClientProvider>,
  );
  const thumbnails = screen.getAllByRole("button", { name: /^Slide \d: / });

  expect(thumbnails).toHaveLength(3);
  expect(thumbnails[0].getAttribute("aria-current")).toBe("true");

  fireEvent.click(thumbnails[2]);

  expect(screen.getByText("Slide 3 of 3 · Core teaching")).toBeTruthy();
  expect(thumbnails[2].getAttribute("aria-current")).toBe("true");
  expect(thumbnails[0].getAttribute("aria-current")).toBeNull();
});

it("says so when the deck has no slides", () => {
  render(
    <QueryClientProvider client={new QueryClient()}>
      <SlideDeckView manifest={manifest([])} />
    </QueryClientProvider>,
  );

  expect(screen.getByText("This deck has no slides yet.")).toBeTruthy();
});

it("shows the cover as a title slide with its objectives", () => {
  const covered: EngineManifest = {
    ...deck,
    cover: {
      title: "Estimating distances",
      subtitle: "Mathematics · JSS1",
      objectives: ["Estimate a distance from steps"],
    },
  };
  render(
    <QueryClientProvider client={new QueryClient()}>
      <SlideDeckView manifest={covered} />
    </QueryClientProvider>,
  );

  expect(screen.getByText("Slide 1 of 4 · Cover")).toBeTruthy();
  expect(
    screen.getByRole("heading", { name: "Estimating distances" }),
  ).toBeTruthy();
  expect(screen.getByText("Mathematics · JSS1")).toBeTruthy();
  expect(screen.getByText("Estimate a distance from steps")).toBeTruthy();
});

it("draws the maths in a slide's title instead of showing its dollar signs", () => {
  const maths = manifest([
    step(
      "s1",
      "Core teaching",
      String.raw`Convert $5\frac{3}{4}$ to an improper fraction`,
    ),
  ]);

  const { container } = render(
    <QueryClientProvider client={new QueryClient()}>
      <SlideDeckView manifest={maths} />
    </QueryClientProvider>,
  );

  const heading = container.querySelector("h2");
  expect(heading?.querySelector(".katex")).not.toBeNull();
  expect(heading?.textContent).not.toContain("$");
});

it("shows a window of thumbnails that keeps the slide being read in view", async () => {
  const { windowOf } = await import("./SlideThumbnails");

  expect(windowOf(20, 0)).toEqual({ from: 0, to: 7 });
  expect(windowOf(20, 11)).toEqual({ from: 8, to: 15 });
  expect(windowOf(20, 19)).toEqual({ from: 13, to: 20 });
  expect(windowOf(3, 1)).toEqual({ from: 0, to: 3 });
});
