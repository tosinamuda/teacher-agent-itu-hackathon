import type { EditableSessionPlan } from "../api/manualEdit";
import type { SessionPlanData } from "../components/SessionPlanView";
import { diffPlans, type PlanDiff } from "../lib/planDiff";
import { lastRevision, savedByHand } from "../lib/lastRevision";
import { versionsOfPlan } from "../lib/planVersions";
import type { PlanGenerationResponse } from "./usePlanGenerator";
import { usePlanVersion } from "./usePlanVersion";
import { useSessionPlans } from "./useSessionPlans";

export type LastChange = {
  /** The version the agent's revision made. */
  number: number;
  /** What the plan was before it, to go back to. */
  previous: EditableSessionPlan;
  diff: PlanDiff;
};

/** What the agent's latest revision of this plan changed, once both versions are read. */
export function useLastChange(
  plan: PlanGenerationResponse | null,
): LastChange | null {
  const summaries = useSessionPlans(plan?.session_id);
  const revision = lastRevision(
    versionsOfPlan(summaries.data ?? [], plan?.plan_id ?? ""),
  );
  const after = usePlanVersion(revision?.latest.version_id);
  const was = usePlanVersion(revision?.before.version_id);
  if (!revision || !after.data || !was.data) return null;
  // Going back, or editing by hand, is not something the agent changed.
  if (savedByHand(after.data.run_metadata)) return null;
  return {
    number: revision.latest.number,
    previous: was.data.session_plan,
    diff: diffPlans(
      was.data.session_plan as SessionPlanData,
      after.data.session_plan as SessionPlanData,
    ),
  };
}
