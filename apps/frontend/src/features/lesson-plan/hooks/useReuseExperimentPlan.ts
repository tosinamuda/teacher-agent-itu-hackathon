import { useMutation, useQueryClient } from "@tanstack/react-query";

import { experimentKey } from "@/features/experiments/hooks/useExperiments";

import { reuseExperimentPlan, type PlanSource } from "../api/reusePlan";

/** Reuse an existing plan as an experiment's plan, and refresh what the lesson page shows. */
export const useReuseExperimentPlan = (experimentId: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (variables: {
      source: PlanSource;
      choices: Record<string, string>;
    }) =>
      reuseExperimentPlan(experimentId, variables.source, variables.choices),
    onSuccess: (result) => {
      if (result.status !== "reused") return;
      void queryClient.invalidateQueries({
        queryKey: experimentKey(experimentId),
      });
      void queryClient.invalidateQueries({ queryKey: ["experiments"] });
    },
  });
};
