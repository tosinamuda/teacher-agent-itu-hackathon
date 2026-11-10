import { ContentBlock } from "@/shared/types/lesson-schema";

export type EvaluationHypothesis = "H1" | "H2";

export type RaterSession = {
  rater_id: string;
  display_name: string;
};

/** Study identity shown in the rater workspace header (mirrors the print packs). */
export type EvaluationMeta = {
  institution_name: string;
  study_title: string;
  textbook_name: string;
};

export type EvaluationRubricCriterion = {
  criterion_id: string;
  label: string;
  /** Teacher-friendly alias shown to raters; falls back to `label`. */
  display_label?: string;
  description: string;
  scale_min: number;
  scale_max: number;
};

export type EvaluationNoteFields = {
  strengths?: string;
  concerns?: string;
  recommendation?: string;
  /** Protocol §3.4 major-issue flags ticked by the rater (H1 only). */
  major_issues?: string[];
  /** Free-text detail when the "Other" major-issue flag is ticked. */
  major_issue_other?: string;
};

/** A selectable H1 major-issue flag (Protocol §3.4 failure-mode tag). */
export type EvaluationMajorIssueFlag = {
  key: string;
  label: string;
  /** Plain one-line gloss explaining what the flag means. */
  description?: string;
};

export type EvaluationH2StoredSectionScore = {
  learner_state_suitability: number;
  scaffolding_appropriateness: number;
  challenge_calibration: number;
  misconception_support?: number | null;
  objective_preservation: number;
  section_score: number;
};

/**
 * Per-section scores as the BLINDED H2 detail endpoint returns them: keyed by
 * anonymous `candidate_id` (never by pack role) — the backend re-keys the stored
 * rating so the form can prefill without learning which candidate is which.
 */
export type EvaluationH2BlindedSectionScores = Record<string, EvaluationH2StoredSectionScore>;

export type EvaluationRating = {
  rating_id: string;
  evaluation_packet_id: string;
  rater_id: string;
  hypothesis: EvaluationHypothesis;
  overall_score: number;
  rubric_scores: Record<string, number | null>;
  section_scores?: Record<string, EvaluationH2BlindedSectionScores> | null;
  diagnostic_scores?: Record<string, number | null> | null;
  notes?: Record<string, unknown> | null;
  created_at?: string | null;
  updated_at?: string | null;
  submitted_at?: string | null;
};

export type EvaluationPacketQueueItem = {
  evaluation_packet_id: string;
  packet_code: string;
  hypothesis: EvaluationHypothesis;
  status: string;
  created_at?: string | null;
  rating?: EvaluationRating | null;
  /** H1 blinding: the anonymous per-lesson label ("Candidate A…D"); null for H2. */
  candidate_label?: string | null;
  /** Opaque lesson-group key so H1 rows can render as lesson blocks. */
  group_key?: string | null;
};

export type EvaluationObjective = {
  lesson_objective_id: string;
  objective_text?: string | null;
};

export type EvaluationReferenceSheet = {
  subject?: string | null;
  grade?: string | null;
  term?: string | null;
  week?: number | null;
  topic?: string | null;
  subtopic?: string | null;
  theme?: string | null;
  curriculum_objectives: string[];
  /** The teacher's previous-knowledge line. */
  entry_behaviour: string[];
  /** One line per core step: its objective, her activities in her words, the work set. */
  lesson_sequence: string[];
  instructional_materials: string[];
  /** The questions the teacher assessed the lesson with. */
  evaluation: string[];
  // Textbook references are not shown to H1/H2 raters — they live in the
  // separate source-grounding audit.
};

export type EvaluationReviewPackStep = {
  step_id: string;
  step_kind?: string | null;
  instructional_type?: string | null;
  type?: string | null;
  title?: string | null;
  estimated_minutes?: number | null;
  blocks?: ContentBlock[];
  status?: string | null;
};

export type EvaluationReviewPackManifest = {
  scope?: string;
  subject?: string | null;
  track?: string | null;
  grade?: string | null;
  term?: string | null;
  week?: number | null;
  topic?: string | null;
  subtopic?: string | null;
  theme?: string | null;
  curriculum_objectives?: Record<string, unknown>[];
  lesson_plan_objectives?: Record<string, unknown>[];
  misconceptions?: string[];
  steps: EvaluationReviewPackStep[];
  instructional_materials?: string[];
  references?: string[];
};

export type EvaluationReviewPack = {
  scope: string;
  manifest: EvaluationReviewPackManifest;
};

/**
 * Per-objective learner-state row carried by the H2 packet payload.
 *
 * Mirrors the backend's `objective_states_payload` in
 * `apps/backend/src/app/domains/evaluation/application/packet_payloads.py` —
 * one row per lesson objective, with the assigned band, confidence,
 * perceived difficulty, and any recorded misconception.
 */
export type EvaluationObjectiveState = {
  lesson_objective_id: string;
  objective_text?: string | null;
  band?: string | null;
  mastery_score?: number | null;
  confidence?: string | null;
  perceived_difficulty?: string | null;
  misconception_code?: string | null;
  misconception_description?: string | null;
  evidence_refs?: string[];
};

export type EvaluationLearnerStateCard = {
  focal_case_type: string;
  curriculum_profile?: Record<string, unknown> | null;
  preferences?: Record<string, unknown> | null;
  mastered_sections: Array<Record<string, unknown>>;
  objective_states?: EvaluationObjectiveState[];
  selection_metadata?: Record<string, unknown> | null;
};

/**
 * One anonymous rateable candidate in a blinded packet: a stable id, the rater-facing
 * label ("Candidate A/B"), its randomised position, and its pack content. The
 * candidate -> condition (P0/P1) mapping never reaches the client.
 */
export type EvaluationBlindedCandidate = {
  candidate_id: string;
  label: string;
  display_order: number;
  pack: { manifest: EvaluationReviewPackManifest };
};

export type EvaluationH2SectionContext = {
  section_id: string;
  step_id: string;
  title?: string | null;
  step_kind?: string | null;
  instructional_type?: string | null;
  lesson_objective_id: string;
  objective_text?: string | null;
  /**
   * Per-candidate step content keyed by `candidate_id`; null when that candidate
   * has no section for this objective (penalise its lesson-goal score).
   */
  candidate_steps: Record<string, EvaluationReviewPackStep | null>;
};

export type H1PacketDetail = {
  evaluation_packet_id: string;
  packet_code: string;
  hypothesis: "H1";
  status: string;
  /** Blinded position in the lesson block ("Candidate B" of candidate_count). */
  candidate_label?: string | null;
  candidate_count?: number;
  lesson_title?: string | null;
  lesson_subtitle?: string | null;
  objectives: EvaluationObjective[];
  reference_sheet: EvaluationReferenceSheet;
  candidate_pack: EvaluationReviewPack;
  rubric: EvaluationRubricCriterion[];
  /** Shown beside the rubric on every H1 rating surface. */
  rating_guidance?: string[];
  major_issue_flags: EvaluationMajorIssueFlag[];
  existing_rating?: EvaluationRating | null;
};

export type H2PacketDetail = {
  evaluation_packet_id: string;
  packet_code: string;
  hypothesis: "H2";
  status: string;
  lesson_title?: string | null;
  lesson_subtitle?: string | null;
  objectives: EvaluationObjective[];
  focal_learner: EvaluationLearnerStateCard;
  /** Anonymous candidates in randomised per-rater order (Protocol §4 blinding). */
  candidates: EvaluationBlindedCandidate[];
  sections: EvaluationH2SectionContext[];
  rubric: EvaluationRubricCriterion[];
  existing_rating?: EvaluationRating | null;
};

export type EvaluationPacketDetail = H1PacketDetail | H2PacketDetail;

export type H1RatingSaveRequest = {
  rubric_scores: Record<string, number>;
  notes?: EvaluationNoteFields | null;
};

export type H2SectionRatingSaveRequest = {
  section_id: string;
  learner_state_suitability: number;
  scaffolding_appropriateness: number;
  challenge_calibration: number;
  misconception_support?: number | null;
  objective_preservation: number;
};

/** One anonymous candidate's full set of section scores (blinded save path). */
export type H2CandidateScoresSaveRequest = {
  candidate_id: string;
  section_scores: H2SectionRatingSaveRequest[];
};

export type H2RatingSaveRequest = {
  /**
   * Scores keyed by anonymous `candidate_id` — must cover every candidate in the
   * packet (422 `h2_candidate_scores_incomplete` otherwise). The backend
   * de-anonymises to the real conditions server-side.
   */
  candidate_section_scores: H2CandidateScoresSaveRequest[];
  notes?: EvaluationNoteFields | null;
};

export type EvaluationRatingSaveRequest = H1RatingSaveRequest | H2RatingSaveRequest;

// --- Source-grounding audit (C2-C4) ---

/** One queue entry in the source-grounding audit lane. */
export type SourceAuditQueueItem = {
  audit_item_id: string;
  condition_code: string;
  lesson_objective_id?: string | null;
  objective_text?: string | null;
  source_ref?: string | null;
  status: string;
  rated: boolean;
};

/** One audit rater's 0/1/2 scores for an audit item. */
export type SourceAuditRating = {
  rating_id: string;
  source_relevance: number;
  support_sufficiency: number;
  faithfulness: number;
  scope_correctness: number;
  source_grounding_score: number;
  submitted_at?: string | null;
};

/** Full detail for one audit item: the generated excerpt + its cited source. */
export type SourceAuditItemDetail = {
  audit_item_id: string;
  condition_code: string;
  lesson_objective_id?: string | null;
  objective_text?: string | null;
  generated_excerpt: string;
  source_ref?: string | null;
  source_record_id?: string | null;
  source_excerpt?: string | null;
  /**
   * Cited textbook figure (the cached image URL + its caption) when the cited
   * source record is a VisualBlock — populated alongside `source_excerpt` so
   * the rater can see the figure beside its caption text. NULL when the cited
   * record is text-only; the page falls back to text-only rendering.
   */
  figure_url?: string | null;
  figure_caption?: string | null;
  scope_boundary?: string | null;
  criteria: EvaluationRubricCriterion[];
  existing_rating?: SourceAuditRating | null;
};

/** Payload to save a source-grounding audit rating (each criterion 0/1/2). */
export type SourceAuditRatingSaveRequest = {
  source_relevance: number;
  support_sufficiency: number;
  faithfulness: number;
  scope_correctness: number;
  notes?: EvaluationNoteFields | null;
};

/** One line in the rater's queue (Phase H — actor-derived assignments). */
export type MyQueueLine = {
  assignment_id: string;
  hypothesis: string;
  scope_id: string;
  is_adjudicator: boolean;
};

/** The current rater's assignments grouped by hypothesis. Empty arrays for
 *  a rater with no assignments yet, or for a researcher/admin who has no
 *  bound rater profile. */
export type MyQueue = {
  rater_id: string;
  h1: MyQueueLine[];
  h2: MyQueueLine[];
  audit: MyQueueLine[];
};
