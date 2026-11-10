import { describe, expect, it } from "vitest";

import { problemsOf } from "./problems";

describe("problemsOf", () => {
  it("lists each problem the API found", () => {
    const error = new Error(
      JSON.stringify({ detail: ["plugin.json: missing", "mcp.json: bad"] }),
    );

    expect(problemsOf(error)).toEqual([
      "plugin.json: missing",
      "mcp.json: bad",
    ]);
  });

  it("says a refusal code as a sentence", () => {
    const error = new Error(
      JSON.stringify({
        detail: "plugin_ships_with_the_app:lesson-note-writer",
      }),
    );

    expect(problemsOf(error)).toEqual([
      "lesson-note-writer ships with the app, so only a deploy changes it.",
    ]);
  });

  it("shows a code it does not know as it is", () => {
    const error = new Error(JSON.stringify({ detail: "something_new:x" }));

    expect(problemsOf(error)).toEqual(["something_new:x"]);
  });

  it("shows text that is not JSON as it is", () => {
    expect(problemsOf(new Error("Bad gateway"))).toEqual(["Bad gateway"]);
  });
});
