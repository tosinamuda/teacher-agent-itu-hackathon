import type {
  ClassworkItemPayload,
  ExistingClassworkItem,
} from "./api/manualClasswork";

/** One MCQ option as edited in the form: a stable key (A, B, …) plus its text. */
export type OptionDraft = { key: string; text: string };

export type ClassworkItemDraft = {
  lessonObjectiveId: string;
  stem: string;
  options: OptionDraft[];
  correctOption: string;
  knowledgeComponentId: string;
  difficulty: string;
  // Wrong option key -> misconception code (FD-03: derived then teacher-edited).
  distractorMisconceptions: Record<string, string>;
};

export type ClassworkDraft = { items: ClassworkItemDraft[] };

const OPTION_KEYS = ["A", "B", "C", "D", "E", "F", "G", "H"];

export function nextOptionKey(options: OptionDraft[]): string {
  return OPTION_KEYS.find((key) => !options.some((option) => option.key === key)) ?? "";
}

export const emptyOptions = (): OptionDraft[] => [
  { key: "A", text: "" },
  { key: "B", text: "" },
  { key: "C", text: "" },
  { key: "D", text: "" },
];

export const emptyClassworkItem = (lessonObjectiveId = ""): ClassworkItemDraft => ({
  lessonObjectiveId,
  stem: "",
  options: emptyOptions(),
  correctOption: "",
  knowledgeComponentId: "",
  difficulty: "",
  distractorMisconceptions: {},
});

export const emptyClassworkDraft = (): ClassworkDraft => ({ items: [emptyClassworkItem()] });

/** Seed the form from items already entered, so re-opening edits them in place. */
export function draftFromExistingItems(items: ExistingClassworkItem[]): ClassworkDraft {
  if (items.length === 0) return emptyClassworkDraft();
  return {
    items: items.map((item) => ({
      lessonObjectiveId: item.lesson_objective_id ?? "",
      stem: item.stem,
      options: Object.entries(item.options).map(([key, text]) => ({ key, text })),
      correctOption: item.correct_option,
      knowledgeComponentId: item.knowledge_component_id ?? "",
      difficulty: item.difficulty ?? "",
      distractorMisconceptions: item.option_misconceptions ?? {},
    })),
  };
}

/** Drop blank options and serialise to the API payload (one item per draft item). */
export function buildManualClassworkPayload(draft: ClassworkDraft): {
  items: ClassworkItemPayload[];
} {
  return {
    items: draft.items.map((item) => ({
      lesson_objective_id: item.lessonObjectiveId,
      stem: item.stem,
      options: Object.fromEntries(
        item.options.filter((option) => option.text.trim()).map((option) => [option.key, option.text])
      ),
      correct_option: item.correctOption,
      knowledge_component_id: item.knowledgeComponentId || null,
      difficulty: item.difficulty || null,
      option_misconceptions: Object.fromEntries(
        item.options
          .filter((option) => option.text.trim() && option.key !== item.correctOption)
          .map((option) => [option.key, (item.distractorMisconceptions[option.key] ?? "").trim()])
          .filter(([, code]) => code)
      ),
    })),
  };
}

/** Teacher-facing reasons the classwork can't be saved yet (mirrors the server checks). */
export function manualClassworkIssues(
  draft: ClassworkDraft,
  objectiveIds: Set<string>
): string[] {
  const issues: string[] = [];
  if (draft.items.length === 0) {
    issues.push("Add at least one classwork item.");
  }
  draft.items.forEach((item, index) => {
    const label = `Item ${index + 1}`;
    if (!objectiveIds.has(item.lessonObjectiveId)) {
      issues.push(`${label}: tag it to a lesson objective.`);
    }
    if (!item.stem.trim()) {
      issues.push(`${label}: enter the question.`);
    }
    const filled = item.options.filter((option) => option.text.trim());
    if (filled.length < 2) {
      issues.push(`${label}: enter at least two options.`);
    }
    if (!filled.some((option) => option.key === item.correctOption)) {
      issues.push(`${label}: mark which option is correct.`);
    }
  });
  return issues;
}
