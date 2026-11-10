import { useMutation, useQuery } from "@tanstack/react-query";

import {
  getResearchLearnerExperimentContext,
  listResearchLearners,
} from "@/features/learners/api";

import {
  enterOnBehalfResponses,
  fetchOnBehalfContext,
  type OnBehalfRequest,
} from "../api/onBehalf";

/** Items + objectives to record choices against, and who already submitted. */
export function useOnBehalfContext(planVersionId: string) {
  return useQuery({
    queryKey: ["onBehalfContext", planVersionId],
    queryFn: () => fetchOnBehalfContext(planVersionId),
    enabled: Boolean(planVersionId),
  });
}

/** The experiment's class, so the roster can be scoped to its learners. */
export function useExperimentClass(experimentId: string) {
  return useQuery({
    queryKey: ["experimentClass", experimentId],
    queryFn: () => getResearchLearnerExperimentContext(experimentId),
    enabled: Boolean(experimentId),
  });
}

/** Learners enrolled in a class — the students to record results for. */
export function useClassRoster(classId: string | null | undefined) {
  return useQuery({
    queryKey: ["classRoster", classId],
    queryFn: () => listResearchLearners({ classId: classId ?? undefined }),
    enabled: Boolean(classId),
  });
}

export function useEnterOnBehalfResponses() {
  return useMutation({
    mutationFn: (input: { planVersionId: string; request: OnBehalfRequest }) =>
      enterOnBehalfResponses(input.planVersionId, input.request),
  });
}
