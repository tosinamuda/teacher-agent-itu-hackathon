import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { approvePack, getPackArtefact } from "../api/packReview";
import { PackArtefact, PackManifest } from "../types";

/**
 * Drives one pack's review: loads the pack artefact, exposes an approve action,
 * and lets a revision turn replace the rendered manifest in the cache so the
 * preview re-renders in place. The pack key is shared with the revision chat hook.
 */
export function usePackReview(artefactId: string | undefined) {
  const queryClient = useQueryClient();
  const packKey = ["packArtefact", artefactId];

  const packQuery = useQuery({
    queryKey: packKey,
    queryFn: () => getPackArtefact(artefactId as string),
    enabled: Boolean(artefactId),
  });

  const approveMutation = useMutation({
    // Echo the version we loaded so the server rejects a stale approve (the pack was
    // revised under us) with 409 instead of blessing a manifest we never saw.
    mutationFn: () =>
      approvePack(artefactId as string, packQuery.data?.version),
    onSuccess: (artefact) => {
      queryClient.setQueryData<PackArtefact>(packKey, artefact);
      void queryClient.invalidateQueries({ queryKey: ["pendingPacks"] });
      void queryClient.invalidateQueries({ queryKey: ["pendingStudentNotes"] });
    },
    onError: (error: unknown) => {
      // On a stale-approve conflict, refetch so the teacher sees the current (revised)
      // pack and its new version before they re-review.
      if (
        error instanceof Error &&
        error.message.includes("artefact_changed")
      ) {
        void queryClient.invalidateQueries({ queryKey: packKey });
      }
    },
  });

  const approveConflict =
    approveMutation.error instanceof Error &&
    approveMutation.error.message.includes("artefact_changed");

  const applyRevisedManifest = (manifest: PackManifest) => {
    // Optimistic in-place swap for instant feedback, then refetch so the rendered note
    // matches what the server actually persisted — a revision rewrites the pack and
    // resets it to pending, and the optimistic copy alone left the body stale until reload.
    queryClient.setQueryData<PackArtefact>(packKey, (old) =>
      old ? { ...old, manifest, review_status: "pending" } : old,
    );
    void queryClient.invalidateQueries({ queryKey: packKey });
  };

  return {
    pack: packQuery.data,
    isLoading: packQuery.isLoading,
    isError: packQuery.isError,
    approve: approveMutation.mutate,
    isApproving: approveMutation.isPending,
    isApproved: packQuery.data?.review_status === "approved",
    approveError: approveMutation.isError,
    // The approve was rejected because the pack changed under the teacher; the cache
    // has been refreshed to the current version — they should re-review and re-approve.
    approveConflict,
    applyRevisedManifest,
  };
}
