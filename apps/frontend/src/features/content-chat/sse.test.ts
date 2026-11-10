import { describe, expect, it } from "vitest";

import { SseParser } from "./sse";

describe("SseParser", () => {
  it("reads a frame with its id, kind and data", () => {
    const parser = new SseParser();

    const events = parser.push(
      'id: 7\nevent: turn_done\ndata: {"summary":"Done."}\n\n',
    );

    expect(events).toEqual([
      { seq: 7, kind: "turn_done", data: { summary: "Done." } },
    ]);
  });

  it("gives an event the server did not keep no sequence number", () => {
    const events = new SseParser().push(
      'event: partial\ndata: {"text":"Hi"}\n\n',
    );

    expect(events).toEqual([
      { seq: null, kind: "partial", data: { text: "Hi" } },
    ]);
  });

  it("waits for the rest of a frame that arrives in pieces", () => {
    const parser = new SseParser();

    expect(parser.push("id: 1\nevent: agent_")).toEqual([]);
    expect(parser.push('text\ndata: {"text":"A"}\n')).toEqual([]);
    expect(parser.push("\nid: 2\nevent: tool\ndata: {}\n\n")).toEqual([
      { seq: 1, kind: "agent_text", data: { text: "A" } },
      { seq: 2, kind: "tool", data: {} },
    ]);
  });

  it("drops keep-alive lines and frames it cannot read", () => {
    const parser = new SseParser();

    const events = parser.push(
      ': keep-alive\n\nevent: x\ndata: not json\n\nevent: y\ndata: [1]\n\nevent: ok\ndata: {"a":1}\n\n',
    );

    expect(events).toEqual([{ seq: null, kind: "ok", data: { a: 1 } }]);
  });

  it("reads a frame ended with carriage returns", () => {
    const events = new SseParser().push('event: a\r\ndata: {"n":1}\r\n\r\n');

    expect(events).toEqual([{ seq: null, kind: "a", data: { n: 1 } }]);
  });
});
