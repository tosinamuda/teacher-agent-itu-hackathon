/** Shared chart palette aligned to the app's warm editorial design tokens. */
export const CHART = {
  accent: "#c0551f",
  accentBright: "#d9692e",
  accentDeep: "#a8481a",
  info: "#46546b",
  success: "#4a7a45",
  warning: "#8a6300",
  danger: "#a3243f",
  ink: "#1c1917",
  muted: "#6f6862",
  line: "#e7e4dd",
  surface: "#ffffff",
} as const;

/** Ordered series palette for grouped bars / multiple lines. */
export const SERIES = [CHART.accent, CHART.info, CHART.success, CHART.accentDeep, CHART.warning];

/** Short human labels for the H1 rubric dimension ids (for grouped-bar legends). */
export const H1_DIMENSION_LABELS: Record<string, string> = {
  objective_curriculum_alignment: "Objective/curriculum",
  taught_lesson_alignment: "Taught-lesson alignment",
  scope_conceptual_correctness: "Scope/correctness",
  clarity_usefulness: "Clarity/usefulness",
};

/** Short human labels for the source-grounding audit criterion ids. */
export const AUDIT_CRITERION_LABELS: Record<string, string> = {
  source_relevance: "Source relevance",
  support_sufficiency: "Support sufficiency",
  faithfulness: "Faithfulness",
  scope_correctness: "Scope correctness",
};

/** A readable label for any id, falling back to a title-cased form. */
export const labelFor = (map: Record<string, string>, id: string): string =>
  map[id] ?? id.replace(/_/g, " ");
