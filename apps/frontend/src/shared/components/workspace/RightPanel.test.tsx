// @vitest-environment jsdom
import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
} from "@testing-library/react";
import { afterEach, expect, it } from "vitest";

import { OPEN_AGENT_EVENT, RightPanel } from "./RightPanel";

afterEach(cleanup);

/** On screen: there, and not in a tab that is hidden. */
const visible = (text: string): boolean => {
  const found = screen.queryByText(text);
  return found !== null && found.closest("[hidden]") === null;
};

const ITEMS = [
  {
    id: "a",
    title: "Approve the plan?",
    actions: <button type="button">Approve</button>,
  },
  { id: "b", title: "Class test" },
];

it("opens on the agent unless the page is a decision", () => {
  render(<RightPanel needs={ITEMS} agent={<p>Ask me anything</p>} />);

  expect(visible("Ask me anything")).toBe(true);
  expect(visible("Approve the plan?")).toBe(false);
});

it("opens on needs-you for a decision page and counts what is waiting", () => {
  render(
    <RightPanel
      needs={ITEMS}
      agent={<p>Ask me anything</p>}
      defaultTab="needs"
    />,
  );

  expect(
    screen
      .getByRole("tab", { name: "Needs you · 2" })
      .getAttribute("aria-selected"),
  ).toBe("true");
  expect(screen.getByRole("button", { name: "Approve" })).toBeTruthy();
});

it("keeps both tabs, in the same order, when nothing is waiting", () => {
  render(<RightPanel needs={[]} agent={<p>Chat</p>} defaultTab="needs" />);

  expect(screen.getAllByRole("tab").map((tab) => tab.textContent)).toEqual([
    "Agent",
    "Needs you",
  ]);
  expect(screen.getByText("Nothing is waiting for you here.")).toBeTruthy();
});

it("switches tabs without losing the other tab's content", () => {
  render(<RightPanel needs={ITEMS} agent={<p>Chat</p>} defaultTab="needs" />);

  fireEvent.click(screen.getByRole("tab", { name: "Agent" }));
  expect(screen.getByText("Chat")).toBeTruthy();

  fireEvent.click(screen.getByRole("tab", { name: "Needs you · 2" }));
  expect(screen.getByText("Class test")).toBeTruthy();
});

it("lets a decision send the teacher to the agent", () => {
  const item = {
    id: "a",
    title: "Approve the plan?",
    actions: ({ openAgent }: { openAgent: () => void }) => (
      <button type="button" onClick={openAgent}>
        Ask for changes
      </button>
    ),
  };
  render(<RightPanel needs={[item]} agent={<p>Chat</p>} defaultTab="needs" />);

  fireEvent.click(screen.getByRole("button", { name: "Ask for changes" }));

  expect(screen.getByText("Chat")).toBeTruthy();
});

it("brings the agent forward when asked from the page", () => {
  render(
    <RightPanel
      needs={ITEMS}
      agent={<p>Ask me anything</p>}
      defaultTab="needs"
    />,
  );
  expect(visible("Ask me anything")).toBe(false);

  act(() => {
    window.dispatchEvent(new Event(OPEN_AGENT_EVENT));
  });

  expect(visible("Ask me anything")).toBe(true);
});

it("keeps the agent's tab mounted while it is not shown, so its chat keeps what it has", () => {
  render(
    <RightPanel
      needs={ITEMS}
      agent={<p>Ask me anything</p>}
      defaultTab="needs"
    />,
  );

  expect(screen.getByText("Ask me anything")).toBeTruthy();
});
