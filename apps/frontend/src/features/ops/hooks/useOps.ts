import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { opsApi } from "../api";

const OPS_KEY = ["ops"] as const;
const POLL_MS = 5000;

export function useOpsHealth() {
  return useQuery({
    queryKey: [...OPS_KEY, "health"],
    queryFn: opsApi.health,
    refetchInterval: POLL_MS,
  });
}

export function useOpsJobs(state?: string | null) {
  return useQuery({
    queryKey: [...OPS_KEY, "jobs", state ?? "all"],
    queryFn: () => opsApi.jobs(state),
    refetchInterval: POLL_MS,
  });
}

export function useOpsExecutions(status?: string | null) {
  return useQuery({
    queryKey: [...OPS_KEY, "executions", status ?? "all"],
    queryFn: () => opsApi.executions(status),
    refetchInterval: POLL_MS,
  });
}

/** Mutations for the action buttons; each refreshes every ops query on success. */
export function useOpsActions() {
  const queryClient = useQueryClient();
  const invalidate = () => {
    void queryClient.invalidateQueries({ queryKey: OPS_KEY });
  };
  return {
    cancelJob: useMutation({ mutationFn: opsApi.cancelJob, onSuccess: invalidate }),
    redispatch: useMutation({ mutationFn: opsApi.redispatch, onSuccess: invalidate }),
    cancel: useMutation({ mutationFn: opsApi.cancel, onSuccess: invalidate }),
  };
}
