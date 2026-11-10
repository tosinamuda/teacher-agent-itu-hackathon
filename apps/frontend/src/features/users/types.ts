/** Onboardable roles surfaced by the admin "Add user" form. A student login is
 *  paired to an existing StudentProfile (pick the profile in the form). */
export type OnboardableRole = "research_manager" | "teacher" | "rater" | "admin" | "student";

export const ONBOARDABLE_ROLES: readonly OnboardableRole[] = [
  "research_manager",
  "teacher",
  "rater",
  "admin",
  "student",
] as const;

/** One row in the admin user list. Role-linked public ids are populated only
 *  for the role that owns them (rater_id for raters, student_id for students). */
export type UserSummary = {
  id: string;
  auth_id: string;
  email: string | null;
  full_name: string | null;
  role: string;
  created_at: string | null;
  rater_id: string | null;
  student_id: string | null;
};

export type UserCreateRequest = {
  code: string;
  email: string;
  full_name: string | null;
  role: OnboardableRole;
  /** Required for role=student: the StudentProfile (public id) to bind. */
  student_id?: string | null;
};

/** A slim learner row for the student-login picker (from GET /learners). */
export type PickableLearner = {
  student_id: string;
  full_name: string;
  class_name: string | null;
  code: string | null;
};
