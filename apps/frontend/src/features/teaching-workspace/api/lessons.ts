import { apiFetch } from "@/shared/api/client";

/** One lesson in the teacher's workspace + whether it needs a plan / is under study. */
export type WorkspaceLesson = {
  lesson_period_id: string;
  week_number: number;
  period_number: number;
  lesson_title: string;
  lesson_subtitle?: string | null;
  approved_version_count: number;
  latest_approved_version_id?: string | null;
  under_research_study: boolean;
};

/** Lists the lessons (subtopics) for a workspace, with plan + research-study state. */
export const listWorkspaceLessons = (
  workspaceId: string,
): Promise<WorkspaceLesson[]> =>
  apiFetch<WorkspaceLesson[]>(`/experiments/workspaces/${workspaceId}/lessons`);
