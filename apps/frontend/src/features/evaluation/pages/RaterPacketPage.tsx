import { useEffect, useState } from "react";
import { Modal } from "@/shared/components/ui/Modal";

import { H1PacketIntro } from "../components/H1PacketIntro";
import { H1PacketWorkspace } from "../components/H1PacketWorkspace";
import { H2PacketIntro } from "../components/H2PacketIntro";
import { H2RubricForm } from "../components/H2RubricForm";
import { H1DrawerContent, H2DrawerContent } from "../components/RaterPacketDrawerContent";
import { RaterPacketShell } from "../components/RaterPacketShell";
import { ReviewPackPreview } from "../components/ReviewPackPreview";
import {
  useDownloadH1Worksheet,
  useDownloadH2Worksheet,
  useEvaluationPacket,
  useEvaluationQueue,
  useSaveEvaluationRating,
} from "../hooks/useEvaluation";
import { useRaterSession } from "../hooks/useRaterSession";
import { EvaluationHypothesis } from "../types";

type RaterPacketPageProps = {
  hypothesis: EvaluationHypothesis;
  packetId: string;
};

/** Renders one blinded H1 or H2 packet inside the dedicated packet app shell. */
export function RaterPacketPage({ hypothesis, packetId }: RaterPacketPageProps) {
  const { session, isHydrated } = useRaterSession();
  const packetQuery = useEvaluationPacket(hypothesis, packetId, session?.rater_id);
  const queueQuery = useEvaluationQueue(hypothesis, session?.rater_id);
  const saveMutation = useSaveEvaluationRating(hypothesis, packetId, session?.rater_id);
  const worksheetDownload = useDownloadH1Worksheet(
    hypothesis === "H1" ? packetId : undefined,
    hypothesis === "H1" ? session?.rater_id : undefined
  );
  const h2WorksheetDownload = useDownloadH2Worksheet(
    hypothesis === "H2" ? packetId : undefined,
    hypothesis === "H2" ? session?.rater_id : undefined
  );
  const [isIntroVisible, setIsIntroVisible] = useState(true);
  // The candidate_id whose full pack is open in the preview modal (H2 only).
  const [openCandidatePackId, setOpenCandidatePackId] = useState<string | null>(null);

  const detail = packetQuery.data;
  const queue = queueQuery.data ?? [];
  const currentQueuePacket = queue.find((packet) => packet.evaluation_packet_id === packetId);
  const nextPacket = queue.find(
    (packet) => packet.evaluation_packet_id !== packetId && !packet.rating
  );
  const packetIndex = queue.findIndex((packet) => packet.evaluation_packet_id === packetId);
  const packetPosition = packetIndex >= 0 ? packetIndex + 1 : null;
  const queueCompletedCount = queue.filter((packet) => Boolean(packet.rating)).length;
  const backHref = `/research/rater/${hypothesis.toLowerCase()}`;

  useEffect(() => {
    setIsIntroVisible(true);
  }, [hypothesis, packetId]);

  if (!isHydrated) {
    return (
      <main className="mx-auto flex min-h-screen w-full max-w-3xl items-center justify-center px-6 py-10">
        <p className="text-sm text-[color:var(--muted)]">Restoring rater workspace…</p>
      </main>
    );
  }

  if (!session) {
    return (
      <main className="mx-auto flex min-h-screen w-full max-w-3xl items-center justify-center px-6 py-10">
        <p className="text-sm text-[color:var(--muted)]">
          You need a rater access code to review this note.
        </p>
      </main>
    );
  }

  if (packetQuery.isError) {
    return (
      <main className="mx-auto flex min-h-screen w-full max-w-3xl flex-col items-center justify-center gap-3 px-6 py-10">
        <p className="text-sm text-(--ink)">This revision note is not in your queue.</p>
        <a href={backHref} className="text-sm font-semibold text-(--accent-deep) hover:underline">
          Back to your queue
        </a>
      </main>
    );
  }

  if (!detail) {
    return (
      <main className="mx-auto flex min-h-screen w-full max-w-3xl items-center justify-center px-6 py-10">
        <p className="text-sm text-[color:var(--muted)]">Loading revision note…</p>
      </main>
    );
  }

  const nextPacketHref = nextPacket
    ? `/research/rater/${hypothesis.toLowerCase()}/${nextPacket.evaluation_packet_id}`
    : undefined;
  const completedCount =
    Boolean(detail.existing_rating) && !currentQueuePacket?.rating
      ? queueCompletedCount + 1
      : queueCompletedCount;
  const remainingCount = Math.max(queue.length - completedCount, 0);

  const drawerContent =
    detail.hypothesis === "H1" ? (
      <H1DrawerContent detail={detail} />
    ) : (
      <H2DrawerContent
        detail={detail}
        onOpenCandidatePack={(candidateId) => setOpenCandidatePackId(candidateId)}
      />
    );

  return (
    <>
      <RaterPacketShell
        backHref={backHref}
        drawerContent={drawerContent}
        hypothesis={hypothesis}
        packetCode={detail.packet_code}
        packetPosition={packetPosition}
        queueLength={queue.length}
      >
        {isIntroVisible ? (
          detail.hypothesis === "H1" ? (
            <H1PacketIntro
              completedCount={completedCount}
              detail={detail}
              isDownloadingWorksheet={worksheetDownload.isPending}
              onDownloadWorksheet={() => worksheetDownload.mutateAsync().then(() => undefined)}
              onContinue={() => setIsIntroVisible(false)}
              packetPosition={packetPosition}
              queueLength={queue.length}
              remainingCount={remainingCount}
              sessionName={session.display_name}
            />
          ) : (
            <H2PacketIntro
              completedCount={completedCount}
              detail={detail}
              isDownloadingWorksheet={h2WorksheetDownload.isPending}
              onDownloadWorksheet={() =>
                h2WorksheetDownload.mutateAsync().then(() => undefined)
              }
              onContinue={() => setIsIntroVisible(false)}
              packetPosition={packetPosition}
              queueLength={queue.length}
              remainingCount={remainingCount}
              sessionName={session.display_name}
            />
          )
        ) : detail.hypothesis === "H1" ? (
          <H1PacketWorkspace
            detail={detail}
            isDownloadingWorksheet={worksheetDownload.isPending}
            isSaving={saveMutation.isPending}
            nextPacketHref={nextPacketHref}
            onDownloadWorksheet={() => worksheetDownload.mutateAsync().then(() => undefined)}
            onOpenPacketBrief={() => setIsIntroVisible(true)}
            onSubmit={(payload) => saveMutation.mutateAsync(payload).then(() => undefined)}
          />
        ) : (
          <H2RubricForm
            detail={detail}
            isSaving={saveMutation.isPending}
            nextPacketHref={nextPacketHref}
            onOpenPacketBrief={() => setIsIntroVisible(true)}
            onSubmit={(payload) => saveMutation.mutateAsync(payload).then(() => undefined)}
          />
        )}
      </RaterPacketShell>

      {detail.hypothesis === "H2"
        ? detail.candidates.map((candidate) => (
            <Modal
              key={candidate.candidate_id}
              isOpen={openCandidatePackId === candidate.candidate_id}
              maxWidthClassName="max-w-5xl"
              onClose={() => setOpenCandidatePackId(null)}
              title={`Full ${candidate.label} pack`}
            >
              <ReviewPackPreview
                anchorPrefix={`${candidate.candidate_id}-${detail.evaluation_packet_id}`}
                label={`${candidate.label} pack`}
                pack={candidate.pack}
                showStepNavigator
                tone="candidate"
              />
            </Modal>
          ))
        : null}
    </>
  );
}
