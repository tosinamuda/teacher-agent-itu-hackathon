// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { createMemoryRouter, RouterProvider } from "react-router";
import { afterEach, beforeEach, expect, it, vi } from "vitest";

import { RouteErrorPage } from "./RouteErrorPage";

const reload = vi.fn();

function Crash({ error }: { error: Error }): never {
  throw error;
}

function renderCrash(error: Error, path = "/research/teacher/content/C-1/review") {
  const router = createMemoryRouter(
    [{ path: "*", element: <Crash error={error} />, errorElement: <RouteErrorPage /> }],
    { initialEntries: [path] },
  );
  render(<RouterProvider router={router} />);
}

function loadEntryScript(name: string) {
  const script = document.createElement("script");
  script.setAttribute("src", `/assets/${name}`);
  document.head.append(script);
}

function publishIndex(entry: string) {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue(new Response(`<script src="/assets/${entry}"></script>`)),
  );
}

beforeEach(() => {
  vi.spyOn(console, "error").mockImplementation(() => {});
  vi.stubGlobal("location", { ...window.location, reload });
});

afterEach(() => {
  cleanup();
  reload.mockClear();
  sessionStorage.clear();
  document.head.innerHTML = "";
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

it("shows a plain message, the technical error under Details, and a lesson link", () => {
  renderCrash(new Error("boom"));
  expect(screen.getByText("Something went wrong on this page")).toBeTruthy();
  expect(screen.getByText("Reload to get the latest version.")).toBeTruthy();
  expect(screen.getByText("boom").closest("details")).toBeTruthy();
  expect(screen.getByRole("link", { name: "Back to the lesson page" }).getAttribute("href")).toBe(
    "/research/teacher/content/C-1",
  );
});

it("links to the workspace when the failing page is not a lesson", () => {
  renderCrash(new Error("boom"), "/somewhere-else");
  expect(screen.getByRole("link", { name: "Back to the lesson page" }).getAttribute("href")).toBe(
    "/research",
  );
});

it("reloads the page when Reload is pressed", () => {
  renderCrash(new Error("boom"));
  fireEvent.click(screen.getByRole("button", { name: "Reload" }));
  expect(reload).toHaveBeenCalledTimes(1);
});

it("reloads once on a failed chunk import and not again", async () => {
  const chunkError = new TypeError("Failed to fetch dynamically imported module: /assets/x-1.js");
  renderCrash(chunkError);
  await waitFor(() => expect(reload).toHaveBeenCalledTimes(1));
  cleanup();
  renderCrash(chunkError);
  await new Promise((resolve) => setTimeout(resolve, 20));
  expect(reload).toHaveBeenCalledTimes(1);
});

it("reloads on a TypeError when a newer build is published", async () => {
  loadEntryScript("index-old.js");
  publishIndex("index-new.js");
  renderCrash(new TypeError("Cannot destructure property 'actor' of 'x' as it is undefined"));
  await waitFor(() => expect(reload).toHaveBeenCalledTimes(1));
});

it("does not reload on a TypeError when the loaded build is the newest", async () => {
  loadEntryScript("index-same.js");
  publishIndex("index-same.js");
  renderCrash(new TypeError("real bug"));
  await waitFor(() => expect(fetch).toHaveBeenCalled());
  await new Promise((resolve) => setTimeout(resolve, 20));
  expect(reload).not.toHaveBeenCalled();
});

it("does not reload on an error that is neither a chunk failure nor a TypeError", async () => {
  renderCrash(new Error("plain"));
  await new Promise((resolve) => setTimeout(resolve, 20));
  expect(reload).not.toHaveBeenCalled();
});
