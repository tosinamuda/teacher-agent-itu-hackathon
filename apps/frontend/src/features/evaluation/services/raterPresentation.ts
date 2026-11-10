import { humaniseMisconceptionCode } from "@/shared/utils/misconception";

import { EvaluationLearnerStateCard } from "../types";

export type CompactLearnerTrait = {
  key: string;
  value: string;
};

const PRIMARY_TRAIT_KEYS = [
  "language_level",
  "pace_preference",
  "time_budget_minutes",
] as const;

const labelize = (value: string) => value.replaceAll("_", " ");

const titleize = (value: string) =>
  value
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");

/**
 * Rater-friendly labels for the focal-case / objective-state band enum.
 * The thesis taxonomy (`remediate` / `reinforce` / `extend`) is hidden;
 * raters see the suggested study direction in plain English.
 */
const FOCAL_PROFILE_LABELS: Record<string, string> = {
  remediate: "Needs more practice",
  reinforce: "On track",
  extend: "Ready for extension",
};

function friendlyFocalProfile(focalCaseType: string): string {
  return FOCAL_PROFILE_LABELS[focalCaseType.toLowerCase()] ?? labelize(focalCaseType);
}

/** Builds a compact learner summary from the focal-case payload. */
export function getLearnerSummary(focalLearner: EvaluationLearnerStateCard) {
  const masteredCount = focalLearner.mastered_sections.length;
  return `${friendlyFocalProfile(focalLearner.focal_case_type)} · ${masteredCount} mastered section${
    masteredCount === 1 ? "" : "s"
  }`;
}

/** Formats one mastered section into a short rater-facing label. */
export function formatMasteredSection(section: Record<string, unknown>) {
  return String(
    section.section_title ??
      section.title ??
      section.objective_text ??
      section.lesson_objective_text ??
      section.section_id ??
      "Mastered section"
  );
}

/** Formats the stored rater name into a display-friendly heading form. */
export function formatRaterDisplayName(displayName: string) {
  return titleize(displayName) || "Rater";
}

/** Selects the most important learner traits for compact packet navigation. */
export function getCompactLearnerTraits(
  preferences: Record<string, unknown> | null | undefined
) {
  const entries = Object.entries(preferences ?? {}).filter(
    ([, value]) => value !== null && value !== ""
  );
  const chosen: CompactLearnerTrait[] = [];
  const seenKeys = new Set<string>();

  for (const key of PRIMARY_TRAIT_KEYS) {
    const match = entries.find(([entryKey]) => entryKey === key);
    if (!match) {
      continue;
    }
    seenKeys.add(match[0]);
    chosen.push({
      key: labelize(match[0]),
      value: String(match[1]),
    });
  }

  for (const [key, value] of entries) {
    if (chosen.length >= 3) {
      break;
    }
    if (seenKeys.has(key)) {
      continue;
    }
    seenKeys.add(key);
    chosen.push({
      key: labelize(key),
      value: String(value),
    });
  }

  return chosen;
}

/**
 * Resolve a learner-state misconception into rater-facing prose. Distractors
 * carry only a snake_case code; older snapshots have no description — derive
 * "Missing factor of two" from the code rather than claiming none is recorded.
 */
export const misconceptionText = (state?: {
  misconception_description?: string | null;
  misconception_code?: string | null;
}): string | null => {
  if (!state) return null;
  if (state.misconception_description) return state.misconception_description;
  if (state.misconception_code) return humaniseMisconceptionCode(state.misconception_code);
  return null;
};
