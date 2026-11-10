import {
  EvaluationH2StoredSectionScore,
  H2PacketDetail,
} from "../types";

/** A valid 1-5 Likert point on an H2 dimension. */
export type H2ScaleValue = 1 | 2 | 3 | 4 | 5;

/** Misconception support may also be "na" (no recorded misconception applies). */
export type H2MisconceptionValue = H2ScaleValue | "na";

/** One section's in-progress draft across the five H2 dimensions. */
export type H2SectionDraft = {
  learner_state_suitability?: H2ScaleValue;
  scaffolding_appropriateness?: H2ScaleValue;
  challenge_calibration?: H2ScaleValue;
  misconception_support?: H2MisconceptionValue;
  objective_preservation?: H2ScaleValue;
};

/** All sections' drafts for the blinded candidates: candidateKey -> sectionKey -> draft. */
export type H2CandidateDrafts = Record<string, Record<string, H2SectionDraft>>;

/**
 * Form state for the blinded H2 rubric. `candidate_scores` holds one draft per
 * anonymous candidate per section — the form never knows which candidate is the
 * class pack and which is personalised.
 */
export type H2RubricFormValues = {
  candidate_scores: H2CandidateDrafts;
  notes: {
    strengths: string;
    concerns: string;
    recommendation: string;
  };
};

/** Field-name prefix addressing one candidate's draft for one section. */
export type H2SectionFieldPrefix = `candidate_scores.${string}`;

/**
 * Path-safe react-hook-form key for a section, derived from its position.
 *
 * Section ids can contain characters RHF treats as path separators (e.g. the
 * colon in `step:step01`), which corrupts nested field paths and collapses
 * distinct sections onto one key. We therefore key the form drafts by section
 * index (`s0`, `s1`, …) and map back to the real `section_id` only when building
 * the save payload.
 */
export const sectionFormKey = (index: number): string => `s${index}`;

/** Path-safe react-hook-form key for a candidate, derived from its display order. */
export const candidateFormKey = (displayOrder: number): string => `c${displayOrder}`;

/** Selectable 1-5 options for the five-dimension rating strip. */
export const H2_SCORE_OPTIONS = [
  { value: 1, label: "1 Poor" },
  { value: 2, label: "2 Weak" },
  { value: 3, label: "3 Adequate" },
  { value: 4, label: "4 Good" },
  { value: 5, label: "5 Excellent" },
];

/** Misconception support adds an N/A option ahead of the 1-5 scale. */
export const H2_MISCONCEPTION_OPTIONS = [{ value: "na", label: "N/A" }, ...H2_SCORE_OPTIONS];

/** Teacher-friendly label + helper text for each of the five H2 dimensions. */
export const H2_FIELD_COPY = {
  learner_state_suitability: {
    label: "Fit for this learner",
    description: "Does this section match the learner's objective-level need?",
  },
  scaffolding_appropriateness: {
    label: "Teaching support",
    description: "Is the amount of help, explanation, worked example, hint, or feedback suitable?",
  },
  challenge_calibration: {
    label: "Challenge level",
    description: "Is the difficulty too easy, too hard, or appropriate for this learner?",
  },
  misconception_support: {
    label: "Misconception help",
    description:
      "Does the section address the recorded misconception? Use N/A only when none applies.",
  },
  objective_preservation: {
    label: "Keeps the lesson goal",
    description: "Does this candidate keep the original lesson goal and scope intact?",
  },
} as const;

/** Single-word gloss for each score value, used in dense status summaries. */
export const SCORE_WORD = {
  1: "Poor",
  2: "Weak",
  3: "Adequate",
  4: "Good",
  5: "Excellent",
  na: "N/A",
} as const;

/** Type guard: is `value` a valid 1-5 score? */
export const isValidScore = (value: unknown): value is H2ScaleValue =>
  value === 1 || value === 2 || value === 3 || value === 4 || value === 5;

/** Type guard: is `value` a valid misconception score (1-5 or "na")? */
export const isValidMisconceptionScore = (value: unknown): value is H2MisconceptionValue =>
  value === "na" || isValidScore(value);

/** Has the rater entered at least one dimension on this draft? */
export const isSectionStarted = (draft?: H2SectionDraft) =>
  Boolean(
    draft &&
      (draft.learner_state_suitability !== undefined ||
        draft.scaffolding_appropriateness !== undefined ||
        draft.challenge_calibration !== undefined ||
        draft.misconception_support !== undefined ||
        draft.objective_preservation !== undefined)
  );

/** Are all five dimensions on this draft valid? */
export const isSectionComplete = (draft?: H2SectionDraft) =>
  Boolean(
    draft &&
      isValidScore(draft.learner_state_suitability) &&
      isValidScore(draft.scaffolding_appropriateness) &&
      isValidScore(draft.challenge_calibration) &&
      isValidMisconceptionScore(draft.misconception_support) &&
      isValidScore(draft.objective_preservation)
  );

/**
 * Overlay an override draft onto a base draft, keeping the base value for any
 * dimension the override leaves `undefined`. Used to fold the active section's
 * live (possibly partial) edits over its prefilled seed without wiping unedited
 * dimensions — react-hook-form surfaces prefilled defaults through the field
 * but not always through `getValues`/`useWatch`, so a blind overwrite would
 * blank the untouched dimensions.
 */
export const mergeDraft = (
  base: H2SectionDraft | undefined,
  override: H2SectionDraft | undefined
): H2SectionDraft => {
  const result: H2SectionDraft = { ...base };
  if (!override) {
    return result;
  }
  if (override.learner_state_suitability !== undefined) {
    result.learner_state_suitability = override.learner_state_suitability;
  }
  if (override.scaffolding_appropriateness !== undefined) {
    result.scaffolding_appropriateness = override.scaffolding_appropriateness;
  }
  if (override.challenge_calibration !== undefined) {
    result.challenge_calibration = override.challenge_calibration;
  }
  if (override.misconception_support !== undefined) {
    result.misconception_support = override.misconception_support;
  }
  if (override.objective_preservation !== undefined) {
    result.objective_preservation = override.objective_preservation;
  }
  return result;
};

/** Compact human status line summarising one draft's per-dimension progress. */
export const sectionStatusSummary = (draft?: H2SectionDraft) => {
  if (!draft || !isSectionStarted(draft)) {
    return "Not rated yet";
  }

  const summary = [
    isValidScore(draft.learner_state_suitability)
      ? `Fit ${SCORE_WORD[draft.learner_state_suitability]}`
      : null,
    isValidScore(draft.scaffolding_appropriateness)
      ? `Support ${SCORE_WORD[draft.scaffolding_appropriateness]}`
      : null,
    isValidScore(draft.challenge_calibration)
      ? `Challenge ${SCORE_WORD[draft.challenge_calibration]}`
      : null,
    isValidMisconceptionScore(draft.misconception_support)
      ? `Misconception ${SCORE_WORD[draft.misconception_support]}`
      : null,
    isValidScore(draft.objective_preservation)
      ? `Goal ${SCORE_WORD[draft.objective_preservation]}`
      : null,
  ].filter(Boolean);

  if (summary.length === 0) {
    return "Not rated yet";
  }
  if (!isSectionComplete(draft)) {
    return `In progress · ${summary.join(" · ")}`;
  }
  return summary.join(" · ");
};

/** Short status across all candidates' drafts for one section, by candidate label. */
export const sectionCandidatesStatus = (
  drafts: Array<{ label: string; draft?: H2SectionDraft }>
) => {
  if (drafts.every(({ draft }) => isSectionComplete(draft))) {
    return "All candidates rated";
  }
  if (drafts.every(({ draft }) => !isSectionStarted(draft))) {
    return "Not rated yet";
  }
  const parts = drafts.map(
    ({ label, draft }) => `${label} ${isSectionComplete(draft) ? "done" : "pending"}`
  );
  return `In progress · ${parts.join(" · ")}`;
};

/**
 * Build the initial candidate-keyed drafts from the blinded packet detail.
 *
 * The existing rating's section scores arrive keyed by `candidate_id` (the backend
 * re-keys the stored roles), so each candidate's draft prefills independently
 * without revealing which candidate is which.
 */
export const buildInitialDrafts = (detail: H2PacketDetail): H2CandidateDrafts => {
  const drafts: H2CandidateDrafts = {};
  for (const candidate of detail.candidates) {
    const perSection: Record<string, H2SectionDraft> = {};
    detail.sections.forEach((section, index) => {
      const stored = detail.existing_rating?.section_scores?.[section.section_id];
      perSection[sectionFormKey(index)] = toDraft(stored?.[candidate.candidate_id]);
    });
    drafts[candidateFormKey(candidate.display_order)] = perSection;
  }
  return drafts;
};

/** Convert one stored pack score into an editable draft (null misconception → "na"). */
const toDraft = (stored?: EvaluationH2StoredSectionScore | null): H2SectionDraft => ({
  learner_state_suitability: isValidScore(stored?.learner_state_suitability)
    ? stored.learner_state_suitability
    : undefined,
  scaffolding_appropriateness: isValidScore(stored?.scaffolding_appropriateness)
    ? stored.scaffolding_appropriateness
    : undefined,
  challenge_calibration: isValidScore(stored?.challenge_calibration)
    ? stored.challenge_calibration
    : undefined,
  misconception_support:
    stored?.misconception_support === null
      ? "na"
      : isValidScore(stored?.misconception_support)
      ? stored.misconception_support
      : undefined,
  objective_preservation: isValidScore(stored?.objective_preservation)
    ? stored.objective_preservation
    : undefined,
});
