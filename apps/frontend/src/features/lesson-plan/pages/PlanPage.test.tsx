// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, expect, it, vi } from "vitest";

import type { PlanGenerationResponse } from "../hooks/usePlanGenerator";
import { PlanPage } from "./PlanPage";

const change = vi.hoisted(() => ({ value: null as unknown, undo: vi.fn() }));

const generator = vi.hoisted(() => ({
  planData: null as unknown,
  loadFailed: false,
  approve: vi.fn(),
  close: vi.fn(),
  reload: vi.fn(),
}));

vi.mock("../hooks/usePlanGenerator", () => ({
  usePlanGenerator: () => ({
    planData: generator.planData,
    approve: generator.approve,
    close: generator.close,
    isClosing: false,
    closeError: null,
    isApproving: false,
    isFetching: false,
    approveError: null,
    loadFailed: generator.loadFailed,
    reload: generator.reload,
  }),
}));
vi.mock("@/features/content-chat/ContentChat", () => ({
  ContentConversation: () => <p>The agent's chat</p>,
}));
vi.mock("../components/PlanHistory", () => ({ PlanHistory: () => null }));
vi.mock("../hooks/useLastChange", () => ({
  useLastChange: () => change.value,
}));
vi.mock("../components/PlanDocument", () => ({
  PlanDocument: () => <section data-testid="plan" />,
}));
vi.mock("@/features/lesson-home/components/CreationsInProgress", () => ({
  CreationsInProgress: () => <p>The agent at work</p>,
}));
vi.mock("@/features/lesson-home/components/LessonConversations", () => ({
  LessonConversations: () => <p>The lesson&apos;s conversations</p>,
}));
vi.mock("../components/WithdrawApproval", () => ({
  WithdrawApproval: ({
    onWithdraw,
  }: {
    onWithdraw: (reason: string) => void;
  }) => (
    <button type="button" onClick={() => onWithdraw("Wrong objective.")}>
      Confirm withdrawal
    </button>
  ),
}));
vi.mock("../hooks/useManualEdit", () => ({
  useManualEdit: () => ({
    mutate: change.undo,
    isPending: false,
    isError: false,
  }),
}));

afterEach(() => {
  cleanup();
  change.value = null;
  change.undo.mockClear();
  generator.approve.mockClear();
  generator.close.mockClear();
  generator.reload.mockClear();
  generator.loadFailed = false;
});

const plan = (
  status: string,
  unmet: string[] = [],
  closed_reason: string | null = null,
) =>
  ({
    plan_id: "LP-1",
    version_id: "LPV-1",
    session_id: "S-1",
    version_status: status,
    approved_at: status === "approved" ? "2026-11-04T10:00:00Z" : null,
    unmet_requirements: unmet,
    closed_reason,
    closed_at: closed_reason ? "2026-11-05T10:00:00Z" : null,
    session_plan: {
      subtopic: "Mixed fractions",
      week: 2,
      subject: "Mathematics",
      grade: "JSS1",
      steps: [],
    },
  }) as unknown as PlanGenerationResponse;

const open = (planData: PlanGenerationResponse) => {
  generator.planData = planData;
  return render(
    <MemoryRouter>
      <PlanPage planId="LP-1" />
    </MemoryRouter>,
  );
};

it("puts the decision beside a plan waiting for approval, and approving asks for that version", () => {
  open(plan("draft"));

  expect(screen.getByRole("heading", { name: "Mixed fractions" })).toBeTruthy();
  expect(screen.getByText("Approve the plan?")).toBeTruthy();
  fireEvent.click(screen.getByRole("button", { name: "Approve" }));

  expect(generator.approve).toHaveBeenCalledWith("LPV-1");
});

it("lists what the plan failed to meet next to the decision", () => {
  open(plan("draft", ["A step has no activity."]));

  expect(screen.getByText("A step has no activity.")).toBeTruthy();
});

it("sends the teacher to the agent to ask for changes", () => {
  open(plan("draft"));

  fireEvent.click(screen.getByRole("button", { name: "Ask for changes" }));

  expect(screen.getByText("The agent's chat")).toBeTruthy();
});

it("says an approved plan is approved, offers the class materials, and opens on the agent", () => {
  open(plan("approved"));

  expect(
    screen.getByText("Approved 2026-11-04. The class materials are unlocked."),
  ).toBeTruthy();
  expect(screen.getByText("Make the class materials")).toBeTruthy();
  expect(screen.getByText("The agent at work")).toBeTruthy();
  expect(screen.getByText("The agent's chat")).toBeTruthy();
  expect(screen.queryByRole("button", { name: "Approve" })).toBeNull();
});

it("rejects a draft with the reason the teacher gives", () => {
  open(plan("draft"));

  fireEvent.click(screen.getByRole("button", { name: "Reject" }));
  fireEvent.change(screen.getByLabelText(/Why\?/), {
    target: { value: "Too much lecturing." },
  });
  fireEvent.click(screen.getAllByRole("button", { name: "Reject" })[0]);

  expect(generator.close).toHaveBeenCalledWith({
    versionId: "LPV-1",
    reason: "Too much lecturing.",
  });
});

it("withdraws an approval from the menu, with the reason the teacher gives", () => {
  open(plan("approved"));

  fireEvent.click(screen.getByRole("button", { name: "More" }));
  fireEvent.click(screen.getByRole("menuitem", { name: "Withdraw approval" }));
  fireEvent.click(screen.getByRole("button", { name: "Confirm withdrawal" }));

  expect(generator.close).toHaveBeenCalledWith({
    versionId: "LPV-1",
    reason: "Wrong objective.",
  });
});

it("edits a draft by hand, and offers no editing of an approved plan", () => {
  open(plan("draft"));
  expect(screen.getByRole("button", { name: "Edit" })).toBeTruthy();

  cleanup();
  open(plan("approved"));
  expect(screen.queryByRole("button", { name: "Edit" })).toBeNull();
});

it("shows a closed plan with its reason, and the way on from it", () => {
  open(plan("rejected", [], "Too much lecturing."));

  expect(
    screen.getByText(
      /Rejected 2026-11-05\. Nothing can be made from this version\./,
    ),
  ).toBeTruthy();
  expect(screen.getByText("Plan rejected. What next?")).toBeTruthy();
  expect(screen.getByText("Too much lecturing.")).toBeTruthy();
  expect(
    screen.getByRole("button", { name: "Write a new version" }),
  ).toBeTruthy();
  expect(screen.queryByRole("button", { name: "Approve" })).toBeNull();
});

it("says a withdrawn approval leaves what was made as it is", () => {
  open(plan("withdrawn", [], "Wrong objective."));

  expect(
    screen.getByText(
      /Approval withdrawn 2026-11-05\. Nothing new can be made from this version\./,
    ),
  ).toBeTruthy();
  expect(
    screen.getByText(/Materials already made from it stay as they are/),
  ).toBeTruthy();
});

it("says the plan could not be loaded, rather than not found, when the server failed", () => {
  generator.loadFailed = true;
  generator.planData = null;
  render(
    <MemoryRouter>
      <PlanPage planId="LP-1" />
    </MemoryRouter>,
  );

  expect(screen.getByText("The plan could not be loaded.")).toBeTruthy();
  fireEvent.click(screen.getByRole("button", { name: "Try again" }));

  expect(generator.reload).toHaveBeenCalled();
});

it("says what the agent changed in a draft, and goes back to the version before when asked", () => {
  generator.planData = plan("draft");
  const previous = { steps: [] };
  change.value = {
    number: 2,
    previous,
    diff: {
      overall: [],
      steps: [{ stepId: "S1", title: "Step", kind: "changed", changes: [] }],
    },
  };
  render(
    <MemoryRouter>
      <PlanPage planId="LP-1" />
    </MemoryRouter>,
  );

  expect(screen.getByText(/Version 2 · 1 step changed/)).toBeTruthy();
  fireEvent.click(screen.getByRole("button", { name: "Undo" }));

  expect(change.undo).toHaveBeenCalledWith(previous);
});

it("does not offer to undo a change in a plan that is approved", () => {
  generator.planData = plan("approved");
  change.value = { number: 2, previous: {}, diff: { overall: [], steps: [] } };
  render(
    <MemoryRouter>
      <PlanPage planId="LP-1" />
    </MemoryRouter>,
  );

  expect(screen.queryByRole("button", { name: "Undo" })).toBeNull();
});
