import { apiFetch } from "@/shared/api/client";

/** What clearing a lesson removes, by table, and why it may not be cleared. */
export type StartOver = { counts: Record<string, number>; blocked: string[] };

const path = (workspaceId: string, lessonPeriodId: string): string =>
  `/teaching/workspaces/${workspaceId}/lessons/${lessonPeriodId}/start-over`;

export const previewStartOver = (workspaceId: string, lessonPeriodId: string): Promise<StartOver> =>
  apiFetch<StartOver>(path(workspaceId, lessonPeriodId));

export const startOver = (workspaceId: string, lessonPeriodId: string): Promise<StartOver> =>
  apiFetch<StartOver>(path(workspaceId, lessonPeriodId), { method: "DELETE" });
