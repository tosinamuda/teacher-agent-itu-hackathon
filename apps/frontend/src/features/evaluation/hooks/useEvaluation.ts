import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  downloadH1PacketWorksheet,
  downloadH2PacketWorksheet,
  getAuditItem,
  getEvaluationMeta,
  getEvaluationPacket,
  listAuditItems,
  listEvaluationPackets,
  saveAuditRating,
  saveEvaluationRating,
} from "../api";
import {
  EvaluationHypothesis,
  EvaluationRatingSaveRequest,
  SourceAuditRatingSaveRequest,
} from "../types";

/** Loads the study identity for the workspace header (cached; it rarely changes). */
export const useEvaluationMeta = () =>
  useQuery({
    queryKey: ["evaluationMeta"],
    queryFn: getEvaluationMeta,
    staleTime: Infinity,
  });

/** Lists packet queue items for the active rater and hypothesis lane. */
export const useEvaluationQueue = (
  hypothesis: EvaluationHypothesis,
  raterId?: string
) =>
  useQuery({
    queryKey: ["evaluationQueue", hypothesis, raterId ?? "empty"],
    queryFn: () => listEvaluationPackets(hypothesis, raterId ?? ""),
    enabled: Boolean(raterId),
  });

/** Loads packet detail for one queue item. */
export const useEvaluationPacket = (
  hypothesis: EvaluationHypothesis,
  packetId?: string,
  raterId?: string
) =>
  useQuery({
    queryKey: ["evaluationPacket", hypothesis, packetId ?? "empty", raterId ?? "empty"],
    queryFn: () => getEvaluationPacket(hypothesis, packetId ?? "", raterId ?? ""),
    enabled: Boolean(packetId && raterId),
    // A packet outside the rater's queue stays outside it; only transient failures retry.
    retry: (failures, error) =>
      failures < 3 && !(error instanceof Error && error.message.includes("_not_found")),
  });

/** Saves one H1 or H2 packet rating. */
export const useSaveEvaluationRating = (
  hypothesis: EvaluationHypothesis,
  packetId?: string,
  raterId?: string
) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: EvaluationRatingSaveRequest) =>
      saveEvaluationRating(hypothesis, packetId ?? "", payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["evaluationQueue", hypothesis, raterId ?? "empty"],
      });
      void queryClient.invalidateQueries({
        queryKey: ["evaluationPacket", hypothesis, packetId ?? "empty", raterId ?? "empty"],
      });
    },
  });
};

/** Triggers a local browser save for a downloaded worksheet blob. */
const saveWorksheetBlob = ({ blob, filename }: { blob: Blob; filename: string }) => {
  const objectUrl = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = objectUrl;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(objectUrl);
};

/** Downloads the H1 worksheet PDF and triggers a local browser save. */
export const useDownloadH1Worksheet = (packetId?: string, raterId?: string) =>
  useMutation({
    mutationFn: async () => downloadH1PacketWorksheet(packetId ?? "", raterId ?? ""),
    onSuccess: saveWorksheetBlob,
  });

/** Downloads the H2 personalised-reading-note worksheet PDF and triggers a local save. */
export const useDownloadH2Worksheet = (packetId?: string, raterId?: string) =>
  useMutation({
    mutationFn: async () => downloadH2PacketWorksheet(packetId ?? "", raterId ?? ""),
    onSuccess: saveWorksheetBlob,
  });

/** Lists source-grounding audit items for the active rater. */
export const useAuditQueue = (raterId?: string) =>
  useQuery({
    queryKey: ["auditQueue", raterId ?? "empty"],
    queryFn: () => listAuditItems(raterId ?? ""),
    enabled: Boolean(raterId),
  });

/** Loads one source-grounding audit item's detail. */
export const useAuditItem = (auditItemId?: string, raterId?: string) =>
  useQuery({
    queryKey: ["auditItem", auditItemId ?? "empty", raterId ?? "empty"],
    queryFn: () => getAuditItem(auditItemId ?? "", raterId ?? ""),
    enabled: Boolean(auditItemId && raterId),
  });

/** Saves one source-grounding audit rating (0/1/2 per criterion). */
export const useSaveAuditRating = (auditItemId?: string, raterId?: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: SourceAuditRatingSaveRequest) =>
      saveAuditRating(auditItemId ?? "", payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["auditQueue", raterId ?? "empty"] });
      void queryClient.invalidateQueries({
        queryKey: ["auditItem", auditItemId ?? "empty", raterId ?? "empty"],
      });
    },
  });
};
