import { describe, expect, it } from "vitest";

import type { ServerEvent } from "./sse";
import { reduce, transcriptOf } from "./transcript";

const kept = (
  seq: number,
  kind: string,
  data: Record<string, unknown>,
): ServerEvent => ({
  seq,
  kind,
  data,
});
const live = (kind: string, data: Record<string, unknown>): ServerEvent => ({
  seq: null,
  kind,
  data,
});

describe("transcript", () => {
  it("leaves out the agent's structured-answer tool, which is not something a person reads", () => {
    const state = transcriptOf([
      kept(1, "working_on", { tool: "StructuredOutput" }),
      kept(2, "tool", { tool: "StructuredOutput", status: "completed" }),
      kept(3, "tool", { tool: "read_draft", status: "completed" }),
    ]);

    expect(state.workingOn).toBeNull();
    expect(
      state.lines.map((line) => line.from === "tool" && line.tool),
    ).toEqual(["read_draft"]);
    expect(state.lastSeq).toBe(3);
  });

  it("draws a turn as the message, what the agent did, what it said, and what was saved", () => {
    const state = transcriptOf([
      kept(1, "user_message", {
        text: "Simpler.",
        highlight: { selected_text: "3/4" },
      }),
      kept(2, "tool", {
        tool: "revise_part",
        status: "completed",
        unit_id: "s2",
      }),
      kept(3, "agent_text", { part_id: "p1", text: "Simplified step 2." }),
      kept(4, "turn_done", {
        summary: "Simplified step 2.",
        changed: true,
        version: 3,
      }),
    ]);

    expect(state.lines.map((l) => l.from)).toEqual([
      "teacher",
      "tool",
      "agent",
      "note",
    ]);
    expect(state.lines[0]).toMatchObject({ pointed: "3/4" });
    expect(state.lines[1]).toMatchObject({
      tool: "revise_part",
      unit: "s2",
      failed: false,
    });
    expect(state.lines[3]).toMatchObject({ text: "Saved as version 3." });
    expect(state.working).toBe(false);
    expect(state.lastSeq).toBe(4);
  });

  it("shows the agent's text as it grows, and replaces it with the finished line", () => {
    let state = transcriptOf([kept(1, "user_message", { text: "Go." })]);
    state = reduce(state, live("partial", { part_id: "p1", text: "Simpl" }));
    state = reduce(
      state,
      live("partial", { part_id: "p1", text: "Simplified" }),
    );

    expect(state.partial).toEqual({ partId: "p1", text: "Simplified" });
    expect(state.working).toBe(true);

    state = reduce(
      state,
      kept(2, "agent_text", { part_id: "p1", text: "Simplified it." }),
    );

    expect(state.partial).toBeNull();
    expect(state.lines.at(-1)).toMatchObject({
      from: "agent",
      text: "Simplified it.",
    });
  });

  it("mutes the agent's text in a turn but for the last, which is what it tells the teacher", () => {
    const state = transcriptOf([
      kept(1, "user_message", { text: "Go." }),
      kept(2, "agent_text", { part_id: "a", text: "Working it out." }),
      kept(3, "agent_text", { part_id: "b", text: "Done: simpler." }),
      kept(4, "turn_done", {
        summary: "Done: simpler.",
        changed: true,
        version: 2,
      }),
      kept(5, "user_message", { text: "Again." }),
      kept(6, "agent_text", { part_id: "c", text: "Thinking." }),
    ]);

    const agents = state.lines.filter((line) => line.from === "agent");
    expect(agents.map((line) => line.from === "agent" && line.minor)).toEqual([
      true,
      undefined,
      undefined,
    ]);
  });

  it("holds what the agent thought before a tool call in that call's step, and leaves what it said on screen", () => {
    const state = transcriptOf([
      kept(1, "thinking", { part_id: "r", text: "Plan the parts." }),
      kept(2, "thinking", { part_id: "s", text: "Read the guidance first." }),
      kept(3, "tool", { tool: "read", status: "completed" }),
    ]);

    expect(state.lines.map((line) => line.from)).toEqual(["tool"]);
    expect(state.lines[0]).toMatchObject({
      said: "Plan the parts.\n\nRead the guidance first.",
    });
  });

  it("keeps the agent's words on screen when a tool call follows them", () => {
    const state = transcriptOf([
      kept(1, "agent_text", {
        part_id: "a",
        text: "Steps 1 and 2 are written.",
      }),
      kept(2, "tool", { tool: "write", status: "completed" }),
      kept(3, "agent_text", { part_id: "b", text: "All written." }),
    ]);

    expect(state.lines.map((line) => line.from)).toEqual([
      "agent",
      "tool",
      "agent",
    ]);
    expect(state.lines[0]).toMatchObject({
      text: "Steps 1 and 2 are written.",
    });
    expect(state.lines[1]).toMatchObject({ from: "tool", said: undefined });
  });

  it("adds the summary when the agent's last words came before its last tool call", () => {
    const state = transcriptOf([
      kept(1, "user_message", { text: "Go." }),
      kept(2, "agent_text", { part_id: "a", text: "I'll fix step 3." }),
      kept(3, "tool", { tool: "revise_part", status: "completed" }),
      kept(4, "turn_done", {
        summary: "Step 3 now has the example.",
        changed: true,
        version: 2,
      }),
    ]);

    const agent = state.lines.filter((line) => line.from === "agent");
    expect(agent).toHaveLength(2);
    expect(agent[0]).toMatchObject({ text: "I'll fix step 3.", minor: true });
    expect(agent[1]).toMatchObject({ text: "Step 3 now has the example." });
    expect(agent[1]).not.toHaveProperty("minor");
  });

  it("keeps a thought that no tool call follows as a line of its own", () => {
    const state = transcriptOf([
      kept(1, "tool", { tool: "read", status: "completed" }),
      kept(2, "thinking", { part_id: "r", text: "Last check." }),
    ]);

    expect(state.lines.map((line) => line.from)).toEqual(["tool", "thinking"]);
  });

  it("keeps what a tool call found on its line", () => {
    const state = transcriptOf([
      kept(1, "tool", {
        tool: "add_part",
        unit_id: "lesson",
        status: "completed",
        observed: "2 parts still to write",
      }),
    ]);

    expect(state.lines[0]).toMatchObject({
      from: "tool",
      observed: "2 parts still to write",
    });
  });

  it("ignores a kept event it has already seen, so a reconnect cannot repeat a line", () => {
    const once = transcriptOf([kept(1, "user_message", { text: "A" })]);

    const again = reduce(once, kept(1, "user_message", { text: "A" }));

    expect(again.lines).toHaveLength(1);
  });

  it("gives the summary as the agent's line only when the agent wrote no text", () => {
    const old = transcriptOf([
      kept(1, "user_message", { text: "Older." }),
      kept(2, "turn_done", { summary: "Did it.", changed: true }),
    ]);

    expect(old.lines.map((l) => l.from)).toEqual(["teacher", "agent", "note"]);
    expect(old.lines[1]).toMatchObject({ text: "Did it." });
    expect(old.lines[2]).toMatchObject({ text: "Saved." });
  });

  it("says when nothing changed, and carries the version to the view that follows", () => {
    const state = transcriptOf([
      kept(1, "turn_done", { summary: "", changed: false }),
      kept(2, "turn_done", { summary: "x", changed: true, version: 4 }),
      kept(3, "view", { tool: "show_content", input: { content_id: "AT-1" } }),
    ]);

    expect(state.lines[0]).toMatchObject({
      from: "note",
      text: "No change was made.",
    });
    expect(state.lines.at(-1)).toMatchObject({
      from: "view",
      tool: "show_content",
      input: { content_id: "AT-1" },
      version: 4,
    });
  });

  it("shows a stopped turn as stopped, with the agent idle and its half-written text gone", () => {
    let state = transcriptOf([kept(1, "user_message", { text: "Go." })]);
    state = reduce(state, live("partial", { part_id: "p1", text: "Simpl" }));
    state = reduce(state, live("working_on", { tool: "revise_part" }));

    state = reduce(state, kept(2, "turn_stopped", {}));

    expect(state.lines.at(-1)).toMatchObject({
      from: "note",
      text: "Stopped. Nothing was saved.",
    });
    expect(state).toMatchObject({
      working: false,
      workingOn: null,
      partial: null,
    });
  });

  it("shows a failure, and a tool the agent has started and not finished", () => {
    let state = transcriptOf([kept(1, "user_message", { text: "Go." })]);
    state = reduce(state, live("working_on", { tool: "revise_part" }));

    expect(state.workingOn).toBe("revise_part");

    state = reduce(
      state,
      kept(2, "turn_failed", { error: "the agent stopped" }),
    );

    expect(state.lines.at(-1)).toMatchObject({
      from: "error",
      text: "the agent stopped",
    });
    expect(state).toMatchObject({ working: false, workingOn: null });
  });
});
