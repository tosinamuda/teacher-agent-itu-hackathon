import { describe, expect, it } from "vitest";

import {
  checkLabel,
  passageFor,
  sectionCitations,
  specRevisionOf,
} from "./evidence";
import { ContentItem, ReviewRecord } from "./types";

const item = (content: Record<string, unknown>): ContentItem => ({
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
  review: null,
  has_file: false,
  content,
});

describe("checkLabel", () => {
  it("says a known check in words and an unknown one by its own name", () => {
    expect(checkLabel("explanation_present")).toBe(
      "Every section explains the idea in full",
    );
    expect(checkLabel("some_new_check")).toBe("some new check");
  });
});

describe("sectionCitations", () => {
  it("lists each reference once per section, and keeps a section that cites none", () => {
    const found = sectionCitations(
      item({
        steps: [
          {
            title: "Place value",
            blocks: [
              { source_refs: ["REF-1", "REF-2"] },
              { source_refs: ["REF-1"] },
            ],
          },
          { title: "No sources", blocks: [{}] },
          { blocks: [{ source_refs: ["REF-3"] }] },
        ],
      }),
    );

    expect(found).toEqual([
      { title: "Place value", refs: ["REF-1", "REF-2"] },
      { title: "No sources", refs: [] },
      { title: "Section 3", refs: ["REF-3"] },
    ]);
  });
});

describe("passageFor", () => {
  it("finds the passage a reference names", () => {
    const record: ReviewRecord = {
      version: 1,
      checks: [],
      passages: [
        {
          source_ref: "REF-1",
          title: "Textbook",
          excerpt: "A million is 1,000,000.",
        },
      ],
    };

    expect(passageFor(record, "REF-1")?.excerpt).toBe(
      "A million is 1,000,000.",
    );
    expect(passageFor(record, "REF-9")).toBeUndefined();
  });
});

describe("specRevisionOf", () => {
  it("is the spec its generator wrote to when it has one, else the type's", () => {
    const written = item({});
    written.provenance = {
      specification: { kind: "post_class_review_pack", revision: 1 },
      generator: {
        harness: "engine",
        schema: "spec",
        ref: "revision-note-learner-writer",
        spec_revision: 5,
      },
    };
    expect(specRevisionOf(written)).toBe(5);

    written.provenance = {
      specification: { kind: "post_class_review_pack", revision: 1 },
    };
    expect(specRevisionOf(written)).toBe(1);
  });
});
