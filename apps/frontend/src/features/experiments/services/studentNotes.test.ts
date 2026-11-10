import { describe, expect, it } from "vitest";

import type { ContentSummary } from "@/features/content/types";

import { studentsWithNotes } from "./studentNotes";

const note = (overrides: Partial<ContentSummary>): ContentSummary => ({
  id: "AT-1",
  type: "revision-note",
  level: "learner",
  plan_version_id: "LPV-1",
  student_id: "ST-1",
  version: 1,
  review_status: "pending",
  review_reason: null,
  created_at: null,
  read_only: false,
  provenance: {},
  ...overrides,
});

describe("studentsWithNotes", () => {
  it("counts each student once per lesson, however many versions their note has", () => {
    const counts = studentsWithNotes([
      note({ id: "AT-1", student_id: "ST-1", review_status: "approved" }),
      note({ id: "AT-2", student_id: "ST-1" }),
      note({ id: "AT-3", student_id: "ST-2" }),
      note({ id: "AT-4", student_id: "ST-1", plan_version_id: "LPV-2" }),
    ]);

    expect(counts.get("LPV-1")).toBe(2);
    expect(counts.get("LPV-2")).toBe(1);
  });

  it("ignores the class's note", () => {
    const counts = studentsWithNotes([note({ level: "class", student_id: null })]);

    expect(counts.size).toBe(0);
  });
});
