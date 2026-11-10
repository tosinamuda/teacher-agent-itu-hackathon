import type { TeachingWorkspace } from "../types";

export function formatTeachingWorkspaceLabel(
  workspace: TeachingWorkspace,
): string {
  const parts = [
    workspace.school_name,
    workspace.class_name,
    workspace.subject_name,
    workspace.term,
  ].filter(Boolean);

  return parts.length > 0 ? parts.join(" · ") : workspace.name;
}

/** The class as a teacher names it: no school, which a teacher is already scoped to. */
export function formatClassLabel(workspace: TeachingWorkspace): string {
  const parts = [
    workspace.class_name,
    workspace.subject_name,
    workspace.term,
  ].filter(Boolean);

  return parts.length > 0 ? parts.join(" · ") : workspace.name;
}
