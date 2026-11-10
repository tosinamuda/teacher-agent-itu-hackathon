import { useQuery } from "@tanstack/react-query";

import { getReviewPackManifest } from "@/features/experiments/lib/api";

/** A revision note's manifest, as it is shown for reading. */
export function usePackManifest(artefactId: string | null | undefined) {
  return useQuery({
    queryKey: ["pack-manifest", artefactId],
    queryFn: () => getReviewPackManifest(artefactId as string),
    enabled: Boolean(artefactId),
  });
}
