import { useProgressLines } from "@/features/content-chat/useProgressLines";
import type { ProgressLine } from "@/features/content-chat/useProgressLines";

import { ContentTypeSlug } from "../types";

/**
 * What the agent making a lesson's content of one type is doing, read now and then while
 * `running`. Empty when nothing is running, but for a run that stopped and is `kept`.
 */
export function useGenerationProgress(
  planVersionId: string | null,
  type: ContentTypeSlug,
  running: boolean,
  keep = false,
): ProgressLine[] {
  return useProgressLines(
    planVersionId ? "/content/generation-progress" : null,
    { plan_version_id: planVersionId ?? "", type },
    running,
    keep,
  );
}
