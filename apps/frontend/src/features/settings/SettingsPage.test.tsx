// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { SettingsPage } from "./SettingsPage";

const state = vi.hoisted(() => ({
  switchMaterial: vi.fn(),
  addPlugin: vi.fn(),
  library: [
    {
      folder: "flashcards",
      description: "Flashcards on each objective.",
      version: "1.0.0",
      adds: ["Flashcards"],
      installed: false,
    },
    {
      folder: "homework",
      description: "Homework.",
      version: "1.0.0",
      adds: ["Homework"],
      installed: true,
    },
  ],
  preferences: {
    materials: [
      {
        type: "lesson-note",
        label: "Lesson note",
        description: "A lesson note.",
        core: true,
        enabled: true,
      },
      {
        type: "slide-deck",
        label: "Slides",
        description: "Slides.",
        core: false,
        enabled: false,
      },
      {
        type: "exam-questions",
        label: "Exam questions",
        description: "Exam questions.",
        core: false,
        enabled: true,
      },
    ],
  },
}));

vi.mock("./usePreferences", () => ({
  usePreferences: () => ({
    preferences: state.preferences,
    isLoading: false,
    isError: false,
    isSaving: false,
    library: state.library,
    adding: null,
    addFailed: false,
    addPlugin: state.addPlugin,
    switchMaterial: state.switchMaterial,
  }),
}));

afterEach(() => {
  cleanup();
  state.switchMaterial.mockClear();
  state.addPlugin.mockClear();
});

it("shows the built-in materials without a switch, and the others with one", () => {
  render(<SettingsPage />);

  expect(screen.getByText("Lesson note")).toBeTruthy();
  expect(screen.getByText("Built in")).toBeTruthy();
  expect(screen.queryByRole("switch", { name: "Lesson note" })).toBeNull();
  expect(
    screen.getByRole("switch", { name: "Slides" }).getAttribute("aria-checked"),
  ).toBe("false");
  expect(
    screen
      .getByRole("switch", { name: "Exam questions" })
      .getAttribute("aria-checked"),
  ).toBe("true");
});

it("turns a material on", () => {
  render(<SettingsPage />);

  fireEvent.click(screen.getByRole("switch", { name: "Slides" }));

  expect(state.switchMaterial).toHaveBeenCalledWith({
    type: "slide-deck",
    enabled: true,
  });
});

it("offers the plugins on hand that are not added, and adds one", () => {
  render(<SettingsPage />);

  expect(screen.getByText("Flashcards on each objective.")).toBeTruthy();
  expect(screen.queryByText("Homework.")).toBeNull();

  fireEvent.click(screen.getByRole("button", { name: "Add Flashcards" }));

  expect(state.addPlugin).toHaveBeenCalledWith("flashcards");
});
