import { RightPanel } from "@/shared/components/workspace/RightPanel";
import { WorkspacePage } from "@/shared/components/workspace/WorkspacePage";

import { PendingPackList } from "../components/PendingPackList";
import { usePendingPacks } from "../hooks/usePendingPacks";

/**
 * The teacher's queue of personalised notes awaiting approval. A note lands here when its learner
 * answers the class test; the teacher opens one to read it, revise it and approve it.
 */
export default function PackReviewQueuePage() {
  const { packs, isLoading, isError } = usePendingPacks();
  const approved = usePendingPacks(undefined, "approved");

  const panel = (
    <RightPanel
      needs={[]}
      agent={
        <p className="text-xs text-(--faint)">
          Each note has its own chat with the agent. Open a note to talk to it.
        </p>
      }
    />
  );

  return (
    <WorkspacePage panel={panel}>
      <div className="flex flex-col gap-5">
        <header className="flex flex-col gap-1">
          <h1 className="text-2xl font-semibold text-(--ink)">Personalised notes</h1>
          <p className="text-xs text-(--ink-2)">
            {isLoading ? "" : `${packs.length} to review. Each learner has one note per lesson. A learner sees their note once you approve it.`}
          </p>
        </header>

        {isError ? (
          <p className="text-sm text-(--danger)">We couldn&apos;t load the notes. Please refresh in a moment.</p>
        ) : null}

        <PendingPackList packs={packs} isLoading={isLoading} />

        <section aria-label="Approved notes" className="flex flex-col gap-3">
          <h2 className="text-sm font-semibold text-(--ink)">Approved</h2>
          <PendingPackList packs={approved.packs} isLoading={approved.isLoading} kind="approved" />
        </section>
      </div>
    </WorkspacePage>
  );
}
