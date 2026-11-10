// @vitest-environment jsdom
import { describe, expect, it } from "vitest";

import {
  COMMENT_EVENT,
  commentFromMessage,
  deliverComment,
  type ViewComment,
} from "./viewMessage";

const params = (meta: unknown) => ({
  role: "user",
  content: [{ type: "text", text: "  Simpler.  ", _meta: meta }],
});

describe("commentFromMessage", () => {
  it("takes the text and where the teacher pointed", () => {
    const comment = commentFromMessage(
      params({
        highlight: {
          selected_text: "3/4",
          unit_id: "s2",
          path: "examples.0.solution",
          block_id: "b1",
          junk: "x",
        },
      }),
      "AT-1",
    );

    expect(comment).toEqual({
      contentId: "AT-1",
      text: "Simpler.",
      highlight: {
        selected_text: "3/4",
        unit_id: "s2",
        path: "examples.0.solution",
      },
    });
  });

  it("has no highlight when no text was selected", () => {
    expect(
      commentFromMessage(params({ highlight: null }), "AT-1")?.highlight,
    ).toBeNull();
    expect(commentFromMessage(params(undefined), "AT-1")?.highlight).toBeNull();
    expect(
      commentFromMessage(params({ highlight: { step_id: "s2" } }), "AT-1")
        ?.highlight,
    ).toBeNull();
  });

  it("is none without text or without content to name", () => {
    expect(
      commentFromMessage({ content: [{ type: "text", text: " " }] }, "AT-1"),
    ).toBeNull();
    expect(commentFromMessage(params(undefined), undefined)).toBeNull();
    expect(commentFromMessage("nope", "AT-1")).toBeNull();
  });
});

describe("deliverComment", () => {
  const comment = { contentId: "AT-1", text: "Simpler.", highlight: null };

  it("says no when no chat takes the comment", () => {
    expect(deliverComment(comment)).toBe(false);
  });

  it("says yes when the chat of the content takes it", () => {
    const take = (event: Event) => {
      (event as CustomEvent<ViewComment>).detail.taken = true;
    };
    window.addEventListener(COMMENT_EVENT, take);

    expect(deliverComment(comment)).toBe(true);

    window.removeEventListener(COMMENT_EVENT, take);
  });
});
