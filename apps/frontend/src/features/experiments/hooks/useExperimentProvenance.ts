import { useQuery } from "@tanstack/react-query";

import { getExperimentProvenance } from "../lib/provenance";

export function useExperimentProvenance(experimentId: string) {
  return useQuery({
    queryKey: ["experimentProvenance", experimentId],
    queryFn: () => getExperimentProvenance(experimentId),
  });
}
