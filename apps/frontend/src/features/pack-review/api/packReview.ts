import { apiFetch } from "@/shared/api/client";

import {
  MissingPackStudent,
  PackArtefact,
  StudentPackGenerationStatusRow,
} from "../types";

const REVIEW_PACK = "/artefacts/post-class-review-packs";

/** List students who submitted this lesson's exit assessment but have no pack yet. */
export const listMissingPacks = (
  planVersionId: string,
): Promise<MissingPackStudent[]> =>
  apiFetch<MissingPackStudent[]>(
    `${REVIEW_PACK}/missing?plan_version_id=${encodeURIComponent(planVersionId)}`,
  );

/**
 * (Re)generate packs via the same worker that runs on submit. With a studentId,
 * regenerates that one; without, regenerates every student missing a pack.
 */
export const regenerateStudentPack = (
  planVersionId: string,
  studentId?: string,
): Promise<{ plan_version_id: string; queued_student_ids: string[] }> =>
  apiFetch(`${REVIEW_PACK}/regenerate`, {
    method: "POST",
    body: JSON.stringify({
      plan_version_id: planVersionId,
      student_id: studentId ?? null,
    }),
  });

/** The teacher's generation queue: each student's current attempt (queued/running/failed). */
export const listGenerationStatuses = (
  planVersionId: string,
): Promise<StudentPackGenerationStatusRow[]> =>
  apiFetch<StudentPackGenerationStatusRow[]>(
    `${REVIEW_PACK}/generation-statuses?plan_version_id=${encodeURIComponent(planVersionId)}`,
  );

/** List per-student packs awaiting teacher approval (optionally scoped to a lesson). */
export const listPendingPacks = (
  planVersionId?: string,
  status: "pending" | "approved" = "pending",
): Promise<PackArtefact[]> => {
  const params = new URLSearchParams();
  if (planVersionId) params.set("plan_version_id", planVersionId);
  if (status !== "pending") params.set("status", status);
  const query = params.toString();
  return apiFetch<PackArtefact[]>(
    `${REVIEW_PACK}/pending${query ? `?${query}` : ""}`,
  );
};

/** Fetch one pack artefact (manifest + review state) by id. */
export const getPackArtefact = (artefactId: string): Promise<PackArtefact> =>
  apiFetch<PackArtefact>(`${REVIEW_PACK}/${encodeURIComponent(artefactId)}`);

/**
 * Approve a pending pack so the student can see it (the teacher HITL gate).
 * The approver is taken from the signed-in actor server-side (x-teacher-code),
 * never sent from the client. ``expectedVersion`` is the version the teacher
 * reviewed; if the pack was revised since, the server rejects the approve with
 * 409 (``artefact_changed``) so they re-review rather than bless unseen content.
 */
export const approvePack = (
  artefactId: string,
  expectedVersion?: number | null,
): Promise<PackArtefact> =>
  apiFetch<PackArtefact>(
    `${REVIEW_PACK}/${encodeURIComponent(artefactId)}/approve`,
    {
      method: "POST",
      body: JSON.stringify({ expected_version: expectedVersion ?? null }),
    },
  );
