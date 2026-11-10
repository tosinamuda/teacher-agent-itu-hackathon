import type { PlanVersionSummary } from "../hooks/useSessionPlans";

export type NumberedVersion = PlanVersionSummary & { number: number };

/** One plan's versions, oldest first and numbered, from every version of the lesson's plans. */
export function versionsOfPlan(
  summaries: PlanVersionSummary[],
  planId: string,
): NumberedVersion[] {
  return summaries
    .filter((summary) => summary.plan_id === planId)
    .sort((a, b) => a.created_at.localeCompare(b.created_at))
    .map((summary, index) => ({ ...summary, number: index + 1 }));
}

const SOURCES: Record<string, string> = {
  generated: "Written by the agent",
  manual: "Written by hand",
  revised: "Revised",
  document_import: "Imported from a document",
};

/** How a version came to be, as a teacher reads it. */
export function sourceLabel(sourceType: string | null | undefined): string {
  if (!sourceType) return "";
  return (
    SOURCES[sourceType] ??
    (sourceType.startsWith("experiment") ? "Written for a study" : "")
  );
}

const STATUSES: Record<string, string> = {
  draft: "Draft",
  approved: "Approved",
  rejected: "Rejected",
  withdrawn: "Approval withdrawn",
};

export const statusWord = (status: string): string =>
  STATUSES[status] ?? status;
