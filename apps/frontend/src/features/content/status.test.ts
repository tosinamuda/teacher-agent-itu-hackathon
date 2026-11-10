import { describe, expect, it } from "vitest";

import {
  audienceLine,
  currentContent,
  contentStatus,
  groundingLine,
} from "./status";
import { ContentSummary } from "./types";

const item = (overrides: Partial<ContentSummary>): ContentSummary => ({
  id: "AT-1",
  type: "revision-note",
  level: "class",
  plan_version_id: "LPV-1",
  student_id: null,
  version: 1,
  review_status: "pending",
  review_reason: null,
  created_at: null,
  read_only: false,
  provenance: {},
  ...overrides,
});

describe("currentContent", () => {
  it("takes the class-level content of the type, never a learner's", () => {
    const learner = item({ id: "AT-L", level: "learner", student_id: "ST-1" });
    const classPack = item({ id: "AT-C" });
    const test = item({ id: "AT-T", type: "class-test" });

    expect(
      currentContent([learner, classPack, test], "revision-note")?.id,
    ).toBe("AT-C");
    expect(currentContent([learner], "revision-note")).toBeUndefined();
  });
});

describe("contentStatus", () => {
  it("is not created until it exists", () => {
    expect(contentStatus(undefined).label).toBe("Not created");
  });

  it("reads a rejected or withdrawn item as rejected", () => {
    expect(
      contentStatus(
        item({ review_status: "rejected", review_reason: "Wrong rule." }),
      ).label,
    ).toBe("Rejected");
  });

  it("awaits review until approved", () => {
    expect(contentStatus(item({})).label).toBe("Awaiting your review");
  });

  it("reads an approved class test as sent to students", () => {
    expect(contentStatus(item({ review_status: "approved" })).label).toBe(
      "Approved",
    );
    expect(
      contentStatus(item({ type: "class-test", review_status: "approved" }))
        .label,
    ).toBe("Sent to students");
  });
});

describe("audienceLine", () => {
  it("names the reader in words, never the placeholder", () => {
    expect(audienceLine("{reader} who sat in this lesson")).toBe(
      "a learner who sat in this lesson",
    );
    expect(audienceLine("the teacher who will teach this lesson")).toBe(
      "the teacher who will teach this lesson",
    );
  });
});

describe("groundingLine", () => {
  const note = { id: "AT-N", version: 2, origin: "teacher" as const };

  it("names the lesson note a revision note read, and the textbook where it read that too", () => {
    expect(
      groundingLine({ expert_sources: "lesson-note", lesson_note: note }),
    ).toBe("Grounded in lesson note version 2");
    expect(groundingLine({ expert_sources: "both", lesson_note: note })).toBe(
      "Grounded in lesson note version 2 and the textbook",
    );
    expect(
      groundingLine({ expert_sources: "textbook", lesson_note: null }),
    ).toBe("Grounded in the textbook");
  });

  it("says so when there was no approved note to read, and nothing when none is recorded", () => {
    expect(
      groundingLine({ expert_sources: "lesson-note", lesson_note: null }),
    ).toBe("Grounded in the textbook: the lesson had no approved lesson note");
    expect(groundingLine({ pipeline: "2026-09-02" })).toBeNull();
  });
});
