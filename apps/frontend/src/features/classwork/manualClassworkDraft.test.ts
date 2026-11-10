import { describe, expect, it } from "vitest";

import type { ExistingClassworkItem } from "./api/manualClasswork";
import {
  buildManualClassworkPayload,
  draftFromExistingItems,
  emptyClassworkItem,
  manualClassworkIssues,
  type ClassworkDraft,
} from "./manualClassworkDraft";

const OBJECTIVE_IDS = new Set(["lop01", "lop02"]);

function validItem() {
  return {
    ...emptyClassworkItem("lop01"),
    stem: "What is 2 + 2?",
    options: [
      { key: "A", text: "3" },
      { key: "B", text: "4" },
      { key: "C", text: "" },
      { key: "D", text: "" },
    ],
    correctOption: "B",
  };
}

describe("buildManualClassworkPayload", () => {
  it("drops blank options and serialises options to a key→text map", () => {
    const draft: ClassworkDraft = { items: [validItem()] };
    const payload = buildManualClassworkPayload(draft);
    expect(payload.items).toHaveLength(1);
    expect(payload.items[0].options).toEqual({ A: "3", B: "4" });
    expect(payload.items[0].correct_option).toBe("B");
    expect(payload.items[0].knowledge_component_id).toBeNull();
    expect(payload.items[0].difficulty).toBeNull();
  });

  it("emits option_misconceptions for wrong options only (FD-03)", () => {
    const draft: ClassworkDraft = {
      items: [
        { ...validItem(), distractorMisconceptions: { A: "off_by_one", B: "ignored_correct" } },
      ],
    };
    // B is the correct option (dropped); A is the only filled wrong option.
    expect(buildManualClassworkPayload(draft).items[0].option_misconceptions).toEqual({
      A: "off_by_one",
    });
  });
});

describe("manualClassworkIssues", () => {
  it("is empty for a fully valid item", () => {
    expect(manualClassworkIssues({ items: [validItem()] }, OBJECTIVE_IDS)).toEqual([]);
  });

  it("flags an untagged objective", () => {
    const draft: ClassworkDraft = { items: [{ ...validItem(), lessonObjectiveId: "" }] };
    expect(manualClassworkIssues(draft, OBJECTIVE_IDS).some((i) => /objective/i.test(i))).toBe(true);
  });

  it("flags fewer than two filled options", () => {
    const draft: ClassworkDraft = {
      items: [{ ...validItem(), options: [{ key: "A", text: "3" }, { key: "B", text: "" }] }],
    };
    expect(manualClassworkIssues(draft, OBJECTIVE_IDS).some((i) => /two options/.test(i))).toBe(true);
  });

  it("flags a correct option that is blank or unset", () => {
    const draft: ClassworkDraft = { items: [{ ...validItem(), correctOption: "" }] };
    expect(manualClassworkIssues(draft, OBJECTIVE_IDS).some((i) => /correct/i.test(i))).toBe(true);
  });

  it("flags a blank stem", () => {
    const draft: ClassworkDraft = { items: [{ ...validItem(), stem: "   " }] };
    expect(manualClassworkIssues(draft, OBJECTIVE_IDS).some((i) => /question/i.test(i))).toBe(true);
  });
});

describe("draftFromExistingItems", () => {
  it("seeds the form from persisted items for edit-in-place", () => {
    const existing: ExistingClassworkItem[] = [
      {
        item_id: "ECR-1",
        lesson_objective_id: "lop02",
        stem: "Solve x",
        options: { A: "1", B: "2" },
        correct_option: "A",
        difficulty: "easy",
      },
    ];
    const draft = draftFromExistingItems(existing);
    expect(draft.items).toHaveLength(1);
    expect(draft.items[0].lessonObjectiveId).toBe("lop02");
    expect(draft.items[0].options).toEqual([
      { key: "A", text: "1" },
      { key: "B", text: "2" },
    ]);
    expect(draft.items[0].correctOption).toBe("A");
    expect(draft.items[0].difficulty).toBe("easy");
  });

  it("seeds distractor misconceptions from a persisted item (FD-03)", () => {
    const existing: ExistingClassworkItem[] = [
      {
        item_id: "ECR-2",
        lesson_objective_id: "lop01",
        stem: "Solve x",
        options: { A: "1", B: "2" },
        correct_option: "B",
        option_misconceptions: { A: "off_by_one" },
      },
    ];
    expect(draftFromExistingItems(existing).items[0].distractorMisconceptions).toEqual({
      A: "off_by_one",
    });
  });

  it("falls back to a single empty item when none exist", () => {
    expect(draftFromExistingItems([]).items).toHaveLength(1);
  });
});
