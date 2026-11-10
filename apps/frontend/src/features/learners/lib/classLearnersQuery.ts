import { queryOptions } from "@tanstack/react-query";

import { apiFetch } from "@/shared/api/client";

import type { ClassLearnersResponse } from "../types";

/** The learners of a class, each with their latest class test and where their notes stand. */
export const classLearnersQuery = (workspaceId: string) =>
  queryOptions({
    queryKey: ["learners", "class", workspaceId],
    queryFn: () => apiFetch<ClassLearnersResponse>(`/teaching/workspaces/${workspaceId}/learners`),
    enabled: Boolean(workspaceId),
  });
