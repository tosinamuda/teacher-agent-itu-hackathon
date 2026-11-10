import { LearnerFormState, LearnerProfile } from "../types";

export const emptyForm = (
  defaults?: Partial<LearnerFormState>
): LearnerFormState => ({
  student_id: "",
  code: "",
  full_name: "",
  grade: "SS1",
  track: "General",
  class_id: "",
  field_of_study: "",
  trade_subject: "",
  field_core_subjects: [],
  language_level: "",
  pace_preference: "",
  time_budget_minutes: "",
  ...defaults,
});

export const toApiPayload = (payload: LearnerFormState) => ({
  student_id: payload.student_id || null, // Allow backend to generate if empty
  code: payload.code,
  full_name: payload.full_name,
  grade: payload.grade,
  track: payload.track,
  class_id: payload.class_id || null,
  field_of_study: payload.field_of_study || null,
  trade_subject: payload.trade_subject || null,
  field_core_subjects: payload.field_core_subjects.length
    ? payload.field_core_subjects
    : null,
  language_level: payload.language_level || null,
  pace_preference: payload.pace_preference || null,
  time_budget_minutes: payload.time_budget_minutes
    ? Number(payload.time_budget_minutes)
    : null,
});

export const mapProfileToForm = (
  learner: LearnerProfile
): LearnerFormState => ({
  student_id: learner.student_id,
  code: learner.code ?? "",
  full_name: learner.full_name,
  grade: learner.grade,
  track: learner.track,
  class_id: learner.class_id ?? "",
  field_of_study: learner.field_of_study ?? "",
  trade_subject: learner.trade_subject ?? "",
  field_core_subjects: learner.field_core_subjects ?? [],
  language_level: learner.language_level ?? "",
  pace_preference: learner.pace_preference ?? "",
  time_budget_minutes: learner.time_budget_minutes?.toString() ?? "",
});
