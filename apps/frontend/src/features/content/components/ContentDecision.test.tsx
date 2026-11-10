// @vitest-environment jsdom
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import type { ContentItem } from "../types";
import { decisionOf } from "./ContentDecision";

vi.mock("@/shared/api/client", () => ({ apiFetch: vi.fn() }));

afterEach(cleanup);

const item = (over: Partial<ContentItem>): ContentItem =>
  ({ id: "C-1", type: "lesson-note", level: "class", version: 2, review_status: "pending", read_only: false, ...over }) as ContentItem;

const renderActions = (decision: NonNullable<ReturnType<typeof decisionOf>>, openAgent = vi.fn()) => {
  const actions = typeof decision.actions === "function" ? decision.actions({ openAgent }) : decision.actions;
  render(<QueryClientProvider client={new QueryClient()}>{actions}</QueryClientProvider>);
  return openAgent;
};

it("asks to approve a version waiting for review, naming the material", () => {
  const decision = decisionOf(item({}), "lesson note", null);

  expect(decision?.title).toBe("Approve the lesson note?");
});

it("says a class test, once approved, goes to students and cannot be revised", () => {
  const decision = decisionOf(item({ type: "class-test" }), "class test", null);

  expect(decision?.title).toBe("Approve and send to students?");
  expect(decision?.detail).toBe("Once sent, it can no longer be revised.");
});

it("has nothing to decide on an approved or a read-only version", () => {
  expect(decisionOf(item({ review_status: "approved" }), "lesson note", null)).toBeNull();
  expect(decisionOf(item({ read_only: true }), "lesson note", null)).toBeNull();
});

it("shows why a rejected version was rejected, and offers the agent", () => {
  const decision = decisionOf(item({ review_status: "rejected", review_reason: "Too long. " }), "lesson note", null);

  expect(decision).toMatchObject({ title: "The lesson note was rejected", detail: "Too long" });
  const openAgent = renderActions(decision!);
  fireEvent.click(screen.getByRole("button", { name: "Ask for changes" }));

  expect(openAgent).toHaveBeenCalledOnce();
});

it("offers to reject, ask for changes and approve a version waiting for review", () => {
  renderActions(decisionOf(item({}), "lesson note", null)!);

  for (const name of ["Reject", "Ask for changes", "Approve"]) {
    expect(screen.getByRole("button", { name })).toBeTruthy();
  }
});

it("offers a feedback box to revise a material, but not a class test that is to be sent", () => {
  expect(decisionOf(item({}), "lesson note", null)?.body).toBeTruthy();
  expect(decisionOf(item({ type: "class-test" }), "class test", null)?.body).toBeUndefined();
});

it("labels the feedback box so a teacher can find it", () => {
  const body = decisionOf(item({}), "lesson note", null)!.body;
  render(<QueryClientProvider client={new QueryClient()}>{body}</QueryClientProvider>);

  expect(screen.getByText("Revise with feedback")).toBeTruthy();
  expect(screen.getByRole("button", { name: "Send revision" })).toBeTruthy();
});
