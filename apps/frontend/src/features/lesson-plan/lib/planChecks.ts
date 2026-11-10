import type { StatusKind } from "@/shared/components/ui/StatusMark";

export type PlanCheck = { text: string; status: StatusKind };

/** What the plan was checked against, for the teacher deciding on it: each unmet requirement, or that all are met. */
export function planChecks(
  unmetRequirements: string[] | undefined,
): PlanCheck[] {
  const unmet = unmetRequirements ?? [];
  if (unmet.length === 0)
    return [
      {
        text: "The plan meets the lesson-plan requirements",
        status: "complete",
      },
    ];
  return unmet.map((text) => ({ text, status: "needsYou" }));
}
