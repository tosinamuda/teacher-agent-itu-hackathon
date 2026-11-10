// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, expect, it } from "vitest";

import { LiveWork } from "./LiveWork";

afterEach(cleanup);

it("draws what the agent says and does as the chat does, under the title it is given", () => {
  render(
    <LiveWork
      title="The agent is writing the class test"
      footer="It takes a few minutes."
      events={[
        { id: 1, kind: "start", data: {} },
        {
          id: 2,
          kind: "agent_text",
          data: { part_id: "t", text: "Reading the lesson." },
        },
        {
          id: 3,
          kind: "tool",
          data: { tool: "read_draft", status: "completed" },
        },
      ]}
    />,
  );

  expect(screen.getByText("The agent is writing the class test")).toBeTruthy();
  expect(screen.getByText("Working on it")).toBeTruthy();
  expect(screen.getByText("Read the draft back")).toBeTruthy();
  expect(screen.getByText("It takes a few minutes.")).toBeTruthy();
});

it("says the agent is starting before it has done anything", () => {
  render(<LiveWork title="Writing" footer="Wait." events={[]} />);

  expect(screen.getByText("Starting the agent…")).toBeTruthy();
});
