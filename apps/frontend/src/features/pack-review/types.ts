import { ContentBlock } from "@/shared/types/lesson-schema";

/** One learner-facing section of a personalised study pack. */
export type PackStep = {
  step_id: string;
  type?: string | null;
  title?: string | null;
  estimated_minutes?: number | null;
  lesson_objective_id?: string | null;
  personalisation_band?: string | null;
  blocks: ContentBlock[];
};

/** The rendered study-pack manifest (a PostClassReviewPack). */
export type PackManifest = {
  artefact_id: string;
  plan_version_id: string;
  subject?: string | null;
  grade?: string | null;
  topic?: string | null;
  subtopic?: string | null;
  term?: string | null;
  week?: number | null;
  student_id?: string | null;
  steps: PackStep[];
};

/** A per-student pack artefact with its review state and rendered manifest. */
export type PackArtefact = {
  artefact_id: string;
  plan_version_id: string;
  learner_id?: string | null;
  learner_name?: string | null;
  manifest: PackManifest;
  review_status?: string | null;
  reviewed_at?: string | null;
  created_at?: string | null;
  // Optimistic-concurrency token echoed back on approve; a stale value yields a 409.
  version?: number | null;
};

/** A student who submitted a lesson's exit assessment but has no pack yet. */
export type MissingPackStudent = {
  student_id: string;
  full_name: string;
};

/** One student's current generation attempt for a lesson (the teacher's generation queue). */
export type StudentPackGenerationStatusRow = {
  student_id: string;
  full_name: string;
  status: "queued" | "running" | "succeeded" | "failed" | string;
  attempt_number: number;
  error_category?: string | null;
  produced_artefact_id?: string | null;
  updated_at?: string | null;
};
