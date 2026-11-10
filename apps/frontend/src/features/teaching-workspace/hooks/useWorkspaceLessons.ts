import { useMemo } from "react";

import { useQuery } from "@tanstack/react-query";

import { listWorkspaceLessons } from "../api/lessons";

/**
 * Lists the current workspace's lessons split into a "to create" to-do (no approved
 * plan yet) and the rest, each carrying its under-research-study flag.
 */
export function useWorkspaceLessons(workspaceId: string | null) {
  const query = useQuery({
    queryKey: ["workspaceLessons", workspaceId ?? "empty"],
    queryFn: () => listWorkspaceLessons(workspaceId ?? ""),
    enabled: Boolean(workspaceId),
  });

  const lessons = useMemo(() => query.data ?? [], [query.data]);
  const todo = useMemo(
    () => lessons.filter((lesson) => lesson.approved_version_count === 0),
    [lessons],
  );

  return {
    lessons,
    todo,
    isLoading: query.isLoading,
    isError: query.isError,
  };
}
