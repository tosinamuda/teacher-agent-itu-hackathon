import { apiFetch } from "@/shared/api/client";

import type { BlindingKeyRow, ExperimentAssignments, RaterOption } from "./types";

/** Every rater profile, alphabetically (admin picker dropdown). */
export const listRaters = async () =>
  apiFetch<RaterOption[]>("/evaluation/raters");

/** The consolidated assignment view for one experiment. */
export const getExperimentAssignments = async (experimentId: string) =>
  apiFetch<ExperimentAssignments>(
    `/evaluation/experiments/${encodeURIComponent(experimentId)}/assignments`
  );

/** Assign a rater to the experiment's H1 lesson (max 3 per lesson). */
export const assignRaterH1 = async (
  experimentId: string,
  raterId: string,
  lessonPeriodId: string
) =>
  apiFetch(
    `/evaluation/experiments/${encodeURIComponent(experimentId)}/assignments/h1`,
    {
      method: "POST",
      body: JSON.stringify({ rater_id: raterId, lesson_period_id: lessonPeriodId }),
    }
  );

/** Assign a rater to one H2 focal case (max 3 per case). */
export const assignRaterH2 = async (
  experimentId: string,
  raterId: string,
  focalCaseId: string
) =>
  apiFetch(
    `/evaluation/experiments/${encodeURIComponent(experimentId)}/assignments/h2`,
    {
      method: "POST",
      body: JSON.stringify({ rater_id: raterId, focal_case_id: focalCaseId }),
    }
  );

/** Assign a rater (or adjudicator) to a source-audit item. */
export const assignRaterAudit = async (
  auditItemId: string,
  raterId: string,
  isAdjudicator: boolean
) =>
  apiFetch(
    `/evaluation/audit-items/${encodeURIComponent(auditItemId)}/assignments`,
    {
      method: "POST",
      body: JSON.stringify({ rater_id: raterId, is_adjudicator: isAdjudicator }),
    }
  );

/** Assign one rater to the experiment's WHOLE scope (lesson + every focal case). */
export const assignRaterBundle = async (
  experimentId: string,
  raterId: string,
  includeAudit: boolean
) =>
  apiFetch<{ h1_assigned: number; h2_assigned: number; audit_assigned: number }>(
    `/evaluation/experiments/${encodeURIComponent(experimentId)}/assignments/bundle`,
    {
      method: "POST",
      body: JSON.stringify({ rater_id: raterId, include_audit: includeAudit }),
    }
  );

/** RESEARCHER-ONLY: the candidate-label -> condition key for offline transcription. */
export const getBlindingKey = async (experimentId: string) =>
  apiFetch<BlindingKeyRow[]>(
    `/evaluation/experiments/${encodeURIComponent(experimentId)}/blinding-key`
  );
