import { apiFetch, apiFetchBlob } from "@/shared/api/client";

import {
  EvaluationHypothesis,
  EvaluationMeta,
  EvaluationPacketDetail,
  EvaluationPacketQueueItem,
  EvaluationRating,
  EvaluationRatingSaveRequest,
  MyQueue,
  SourceAuditItemDetail,
  SourceAuditQueueItem,
  SourceAuditRating,
  SourceAuditRatingSaveRequest,
} from "./types";

const lane = (hypothesis: EvaluationHypothesis) => hypothesis.toLowerCase();

/** Loads the study identity (institution + title) for the rater workspace header. */
export const getEvaluationMeta = async () => apiFetch<EvaluationMeta>("/evaluation/meta");

/** Lists packets awaiting review for a hypothesis lane. */
export const listEvaluationPackets = async (
  hypothesis: EvaluationHypothesis,
  raterId: string
) =>
  apiFetch<EvaluationPacketQueueItem[]>(
    `/evaluation/${lane(hypothesis)}/packets?rater_id=${raterId}`
  );

/** Loads a single packet detail for the current rater. */
export const getEvaluationPacket = async (
  hypothesis: EvaluationHypothesis,
  packetId: string,
  raterId: string
) =>
  apiFetch<EvaluationPacketDetail>(
    `/evaluation/${lane(hypothesis)}/packets/${packetId}?rater_id=${raterId}`
  );

/** Saves or updates one packet rating. Rater identity comes from the auth header. */
export const saveEvaluationRating = async (
  hypothesis: EvaluationHypothesis,
  packetId: string,
  payload: EvaluationRatingSaveRequest
) =>
  apiFetch<EvaluationRating>(
    `/evaluation/${lane(hypothesis)}/packets/${packetId}/ratings`,
    {
      method: "PUT",
      body: JSON.stringify(payload),
    }
  );

const filenameFromDisposition = (headerValue: string | null, fallback: string) => {
  if (!headerValue) {
    return fallback;
  }
  const match = /filename="?([^"]+)"?/i.exec(headerValue);
  return match?.[1] ?? fallback;
};

/** Lists source-grounding audit items awaiting review for the current rater. */
export const listAuditItems = async (raterId: string) =>
  apiFetch<SourceAuditQueueItem[]>(`/evaluation/audit/items?rater_id=${raterId}`);

/** Loads one source-grounding audit item (excerpt + cited source + criteria). */
export const getAuditItem = async (auditItemId: string, raterId: string) =>
  apiFetch<SourceAuditItemDetail>(
    `/evaluation/audit/items/${auditItemId}?rater_id=${raterId}`
  );

/** Saves one audit rater's 0/1/2 scores. Rater identity comes from the auth header. */
export const saveAuditRating = async (
  auditItemId: string,
  payload: SourceAuditRatingSaveRequest
) =>
  apiFetch<SourceAuditRating>(
    `/evaluation/audit/items/${auditItemId}/ratings`,
    {
      method: "PUT",
      body: JSON.stringify(payload),
    }
  );

/** Downloads one H1 worksheet PDF for offline expert rating. */
export const downloadH1PacketWorksheet = async (packetId: string, raterId: string) => {
  const { blob, response } = await apiFetchBlob(
    `/evaluation/h1/packets/${packetId}/worksheet.pdf?rater_id=${raterId}`
  );
  return {
    blob,
    filename: filenameFromDisposition(
      response.headers.get("Content-Disposition"),
      `${packetId}-worksheet.pdf`
    ),
  };
};

/** Downloads one H2 personalised-reading-note worksheet PDF for offline expert rating. */
export const downloadH2PacketWorksheet = async (packetId: string, raterId: string) => {
  const { blob, response } = await apiFetchBlob(
    `/evaluation/h2/packets/${packetId}/worksheet.pdf?rater_id=${raterId}`
  );
  return {
    blob,
    filename: filenameFromDisposition(
      response.headers.get("Content-Disposition"),
      `${packetId}-h2-worksheet.pdf`
    ),
  };
};

/** Fetches the actor-rater's assignments grouped by hypothesis (Phase H). */
export const getMyQueue = async () => apiFetch<MyQueue>("/evaluation/my-queue");
