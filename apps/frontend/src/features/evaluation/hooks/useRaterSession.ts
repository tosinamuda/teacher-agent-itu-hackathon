import { useAuthMe } from "@/shared/hooks/useAuthMe";

import { RaterSession } from "../types";

/**
 * The active rater identity — derived from the signed-in access code, exactly
 * like every other role (teacher / student / researcher). There is no
 * "type your name" step or "switch rater": each rater has their own code, so the
 * code IS the identity.
 */
export function useRaterSession() {
  const { data: actor, isLoading } = useAuthMe();
  const session: RaterSession | null = actor?.rater_id
    ? { rater_id: actor.rater_id, display_name: actor.full_name ?? "Rater" }
    : null;
  return { session, isHydrated: !isLoading };
}
