import { apiFetch } from "@/shared/api/client";

import type { PickableLearner, UserCreateRequest, UserSummary } from "./types";

/** Lists every user; optional ``role`` and ``experimentId`` filter server-side. */
export const listUsers = async (
  role?: string | null,
  experimentId?: string | null
) => {
  const params = new URLSearchParams();
  if (role) params.set("role", role);
  if (experimentId) params.set("experiment_id", experimentId);
  const query = params.size > 0 ? `?${params.toString()}` : "";
  return apiFetch<UserSummary[]>(`/auth/users${query}`);
};

/** Onboards a user. For role=rater the server also creates the EvaluationRater. */
export const createUser = async (payload: UserCreateRequest) =>
  apiFetch<UserSummary>("/auth/users", {
    method: "POST",
    body: JSON.stringify(payload),
  });

/** Lists learner profiles for the student-login picker (first 200 by name). */
export const listPickableLearners = async () => {
  const response = await apiFetch<{ data: PickableLearner[] }>(
    "/learners?page=1&page_size=200"
  );
  return response.data;
};
