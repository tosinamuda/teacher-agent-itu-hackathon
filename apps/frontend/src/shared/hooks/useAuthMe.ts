import { useQuery, useQueryClient } from "@tanstack/react-query";

import { type AuthMe, fetchAuthMe } from "@/shared/api/auth";

/** React Query key for the current caller's resolved identity. */
export const AUTH_ME_QUERY_KEY = ["auth", "me"] as const;

/**
 * Loads the caller's role so the UI can gate research-manager surfaces.
 *
 * `retry: 1` keeps a single transient-network retry but stops React Query
 * from hammering the backend three times on every failure (which floods
 * the console with `ERR_CONNECTION_REFUSED` when the backend is down and
 * delays the error state reaching the gate UI).
 */
export function useAuthMe() {
  return useQuery<AuthMe>({
    queryKey: AUTH_ME_QUERY_KEY,
    queryFn: fetchAuthMe,
    staleTime: 60_000,
    retry: 1,
  });
}

/** Returns a callback that refetches the cached identity (after a sign-in/out). */
export function useRefreshAuthMe(): () => void {
  const queryClient = useQueryClient();
  return () => {
    void queryClient.invalidateQueries({ queryKey: AUTH_ME_QUERY_KEY });
  };
}
