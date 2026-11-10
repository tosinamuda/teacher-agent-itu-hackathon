import { useQuery } from "@tanstack/react-query";

import { getExperimentStory } from "../lib/api";

/** Loads an experiment's log-traceable pipeline (for the story's per-step trace). */
export const useExperimentStory = (experimentId: string | null | undefined) =>
  useQuery({
    queryKey: ["experimentStory", experimentId ?? "empty"],
    queryFn: () => getExperimentStory(experimentId ?? ""),
    enabled: Boolean(experimentId),
  });
