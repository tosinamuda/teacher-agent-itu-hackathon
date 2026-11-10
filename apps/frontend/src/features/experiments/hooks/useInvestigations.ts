import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  createInvestigation,
  endInvestigation,
  getInvestigation,
  getInvestigationResults,
  listInvestigations,
} from "../lib/api";
import { InvestigationCreateRequest } from "../lib/experiments";

const investigationKey = (id: string) => ["investigation", id] as const;

/** Fetches the rolled-up rater results across an investigation's experiments. */
export const useInvestigationResults = (investigationId: string | null) =>
  useQuery({
    queryKey: ["investigationResults", investigationId ?? "empty"],
    queryFn: () => getInvestigationResults(investigationId ?? ""),
    enabled: Boolean(investigationId),
  });

/** Lists all investigations (studies). */
export const useInvestigations = () =>
  useQuery({
    queryKey: ["investigations"],
    queryFn: () => listInvestigations(),
  });

/** Fetches one investigation with its member experiments. */
export const useInvestigation = (investigationId: string | null) =>
  useQuery({
    queryKey: investigationId ? investigationKey(investigationId) : ["investigation", "empty"],
    queryFn: () => getInvestigation(investigationId ?? ""),
    enabled: Boolean(investigationId),
  });

/** Creates an investigation and refreshes the list cache. */
export const useCreateInvestigation = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: InvestigationCreateRequest) => createInvestigation(payload),
    onSuccess: (data) => {
      void queryClient.invalidateQueries({ queryKey: ["investigations"] });
      void queryClient.setQueryData(investigationKey(data.investigation_id), data);
    },
  });
};

/** Ends an investigation and refreshes its detail cache. */
export const useEndInvestigation = (investigationId: string | null) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => {
      if (!investigationId) {
        throw new Error("investigation_not_selected");
      }
      return endInvestigation(investigationId);
    },
    onSuccess: (data) => {
      void queryClient.invalidateQueries({ queryKey: ["investigations"] });
      if (investigationId) {
        void queryClient.setQueryData(investigationKey(investigationId), data);
      }
    },
  });
};
