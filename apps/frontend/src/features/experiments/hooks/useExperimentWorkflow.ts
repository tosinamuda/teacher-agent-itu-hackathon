import { useQuery } from "@tanstack/react-query";

import { getExperimentWorkflow } from "../lib/api";

/**
 * React Query wrapper around the backend `/experiments/{id}/workflow`
 * endpoint. One round-trip replaces the previous detail + statistics +
 * client-side derivation pair — the Overview now consumes the snapshot
 * directly and the `services/workflow.ts` file collapses to presentation
 * helpers (status icons, fallback labels).
 */
export const useExperimentWorkflow = (experimentId: string | null) =>
  useQuery({
    queryKey: ["experimentWorkflow", experimentId ?? "empty"],
    queryFn: () => getExperimentWorkflow(experimentId ?? ""),
    enabled: Boolean(experimentId),
  });
