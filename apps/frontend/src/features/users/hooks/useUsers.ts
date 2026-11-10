import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { createUser, listPickableLearners, listUsers } from "../api";
import type { UserCreateRequest } from "../types";

/** Lists users with optional role + experiment filters (admin-only on the backend). */
export function useUsers(role: string | null, experimentId: string | null) {
  return useQuery({
    queryKey: ["users", role ?? "all", experimentId ?? "any"],
    queryFn: () => listUsers(role, experimentId),
    staleTime: 30_000,
  });
}

/** Creates a user and invalidates the cached list so the new row appears. */
export function useCreateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: UserCreateRequest) => createUser(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });
}

/** Lists learner profiles for the student-login picker. */
export function usePickableLearners(enabled: boolean) {
  return useQuery({
    queryKey: ["pickableLearners"],
    queryFn: listPickableLearners,
    enabled,
    staleTime: 30_000,
  });
}
