/** One rater currently sitting in an assignment slot. */
export type AssignedRater = {
  assignment_id: string;
  rater_id: string;
  display_name: string;
  is_adjudicator: boolean;
};

/** The single H1 slot — one lesson, up to ``capacity`` raters. */
export type H1AssignmentSlot = {
  lesson_period_id: string;
  lesson_title: string | null;
  raters: AssignedRater[];
  capacity: number;
};

/** One H2 slot — a focal learner's P0+P1 pair, up to ``capacity`` raters. */
export type H2AssignmentSlot = {
  focal_case_id: string;
  student_id: string;
  student_full_name: string | null;
  focal_case_type: string;
  raters: AssignedRater[];
  capacity: number;
};

/** One audit slot — 2 raters + 1 optional adjudicator. */
export type AuditAssignmentSlot = {
  audit_item_id: string;
  raters: AssignedRater[];
  adjudicators: AssignedRater[];
  capacity: number;
  adjudicator_capacity: number;
};

/** The consolidated view: every assignment slot for one experiment. */
export type ExperimentAssignments = {
  experiment_id: string;
  h1: H1AssignmentSlot | null;
  h2: H2AssignmentSlot[];
  audit: AuditAssignmentSlot[];
};

/** A rater profile as it appears in the admin picker dropdown. */
export type RaterOption = {
  rater_id: string;
  display_name: string;
};

/** RESEARCHER-ONLY: one candidate-label -> condition fact for one rater's view. */
export type BlindingKeyRow = {
  rater_id: string;
  rater_name: string;
  hypothesis: string;
  group: string;
  packet_code: string;
  evaluation_packet_id: string;
  candidate_label: string;
  condition_code: string;
};
