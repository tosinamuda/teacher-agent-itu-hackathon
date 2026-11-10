import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  endExperiment,
  getExperimentRatings,
  getExperimentStatistics,
  getResearchDefaults,
  triggerSyntheticLoop,
  triggerSyntheticRate,
  triggerSyntheticStudents,
  triggerSyntheticTeacher,
} from "../lib/api";

/** Fetches the configured default lesson context (3rd-term subtopic) for the harness. */
export const useResearchDefaults = () =>
  useQuery({
    queryKey: ["researchDefaults"],
    queryFn: getResearchDefaults,
    staleTime: Infinity,
  });

/** Fetches rater-rating progress for a study (research results dashboard). */
export const useExperimentRatings = (experimentId: string | null) =>
  useQuery({
    queryKey: ["experimentRatings", experimentId ?? "empty"],
    queryFn: () => getExperimentRatings(experimentId ?? ""),
    enabled: Boolean(experimentId),
  });

/** Fetches H1/H2 hypothesis tests + inter-rater reliability for a study. */
export const useExperimentStatistics = (experimentId: string | null) =>
  useQuery({
    queryKey: ["experimentStatistics", experimentId ?? "empty"],
    queryFn: () => getExperimentStatistics(experimentId ?? ""),
    enabled: Boolean(experimentId),
  });

/** Queues synthetic students to answer the diagnostic (browser-triggered). */
export const useSyntheticStudents = (experimentId: string | null) =>
  useMutation({
    mutationFn: (n: number) => {
      if (!experimentId) throw new Error("experiment_not_selected");
      return triggerSyntheticStudents(experimentId, n);
    },
  });

/** Queues synthetic expert-teacher raters to score the experiment (browser-triggered). */
export const useSyntheticRate = (experimentId: string | null) =>
  useMutation({
    mutationFn: () => {
      if (!experimentId) throw new Error("experiment_not_selected");
      return triggerSyntheticRate(experimentId);
    },
  });

/** Queues the synthetic teacher to review/approve every pending pack (browser-triggered). */
export const useSyntheticTeacher = (experimentId: string | null) =>
  useMutation({
    mutationFn: () => {
      if (!experimentId) throw new Error("experiment_not_selected");
      return triggerSyntheticTeacher(experimentId);
    },
  });

/** Queues the full synthetic loop: teacher-review → export → rate (browser-triggered). */
export const useSyntheticLoop = (experimentId: string | null) =>
  useMutation({
    mutationFn: () => {
      if (!experimentId) throw new Error("experiment_not_selected");
      return triggerSyntheticLoop(experimentId);
    },
  });

/** Ends a study and refreshes the experiment detail cache. */
export const useEndExperiment = (experimentId: string | null) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => {
      if (!experimentId) {
        throw new Error("experiment_not_selected");
      }
      return endExperiment(experimentId);
    },
    onSuccess: () => {
      if (experimentId) {
        void queryClient.invalidateQueries({ queryKey: ["experiment", experimentId] });
      }
    },
  });
};
