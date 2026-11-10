import { apiFetch } from "@/shared/api/client";

/** The resolved caller behind the current request, as reported by the backend. */
export type AuthMe = {
  role: string;
  auth_id: string;
  email: string | null;
  full_name?: string | null;
  teacher_id?: string | null;
  is_research_manager: boolean;
  /** Public scope ids — populated per role; null for other roles. */
  rater_id?: string | null;
  student_id?: string | null;
};

/** Tags every UI place that branches on role, so the union stays one source of truth. */
export type ResearchRole =
  | "research_manager"
  | "admin"
  | "teacher"
  | "rater"
  | "student"
  | "anonymous";

export const KNOWN_ROLES: readonly ResearchRole[] = [
  "research_manager",
  "admin",
  "teacher",
  "rater",
  "student",
  "anonymous",
] as const;

/** Fetches the caller's resolved identity + role (driven by the stored access code). */
export async function fetchAuthMe(): Promise<AuthMe> {
  return apiFetch<AuthMe>("/auth/me");
}
