import { useQuery } from "@tanstack/react-query";

import { useContent } from "@/features/content/hooks/useContent";
import { getPackArtefact } from "@/features/pack-review/api/packReview";
import {
  latestVersionOf,
  type PlanGenerationResponse,
} from "@/features/lesson-plan/hooks/usePlanGenerator";
import { apiFetch } from "@/shared/api/client";
import { usePathname } from "@/shared/router";

import { lessonRouteOf } from "../lib/lessonRoute";

/**
 * The lesson the teacher is in, found from the page's address, or null outside a lesson. While the
 * page's lesson is still being found, `resolving` holds, so the sidebar does not show the class first.
 */
export function useLessonScope(): {
  lessonPeriodId: string | null;
  resolving: boolean;
} {
  const route = lessonRouteOf(usePathname());
  const planId = route?.kind === "plan" ? route.planId : "";
  const content = useContent(route?.kind === "content" ? route.contentId : "");
  const pack = useQuery({
    queryKey: ["packArtefact", route?.kind === "pack" ? route.artefactId : ""],
    queryFn: () =>
      getPackArtefact(route?.kind === "pack" ? route.artefactId : ""),
    enabled: route?.kind === "pack",
    retry: false,
  });
  const versionId =
    route?.kind === "diagnostic"
      ? route.planVersionId
      : route?.kind === "pack"
        ? (pack.data?.plan_version_id ?? "")
        : (content.data?.plan_version_id ?? "");

  const plan = useQuery({
    queryKey: ["plan", planId],
    queryFn: () => latestVersionOf(planId),
    enabled: Boolean(planId),
    retry: false,
  });
  const version = useQuery({
    queryKey: ["planVersion", versionId],
    queryFn: () =>
      apiFetch<PlanGenerationResponse>(
        `/artefacts/lesson-plans/${encodeURIComponent(versionId)}`,
      ),
    enabled: Boolean(versionId),
    retry: false,
  });

  if (route?.kind === "lesson")
    return { lessonPeriodId: route.lessonPeriodId, resolving: false };
  const found =
    (route?.kind === "plan"
      ? plan.data?.session_id
      : version.data?.session_id) ?? null;
  return {
    lessonPeriodId: found,
    resolving:
      found === null &&
      (content.isLoading ||
        pack.isLoading ||
        plan.isLoading ||
        version.isLoading),
  };
}
