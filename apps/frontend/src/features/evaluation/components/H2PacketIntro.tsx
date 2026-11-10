import { Button } from "@/shared/components/ui/Button";

import { ContextRow, ObjectivesPanel } from "./PacketMetaPanels";
import { LearnerObjectiveStateTable } from "./LearnerObjectiveStateTable";
import { PacketIntroFrame } from "./PacketIntroShared";
import { getCompactLearnerTraits, getLearnerSummary } from "../services/raterPresentation";
import { H2PacketDetail } from "../types";

/** Renders the H2 packet orientation screen before the live comparison opens. */
export function H2PacketIntro({
  completedCount,
  detail,
  isDownloadingWorksheet = false,
  onDownloadWorksheet,
  onContinue,
  packetPosition,
  queueLength,
  remainingCount,
  sessionName,
}: {
  completedCount: number;
  detail: H2PacketDetail;
  isDownloadingWorksheet?: boolean;
  onDownloadWorksheet?: () => void;
  onContinue: () => void;
  packetPosition: number | null;
  queueLength: number;
  remainingCount: number;
  sessionName: string;
}) {
  const learnerTraits = getCompactLearnerTraits(detail.focal_learner.preferences);
  const criteria = detail.rubric.map(
    (criterion) => criterion.display_label ?? criterion.label,
  );

  return (
    <PacketIntroFrame
      continueLabel="Start review"
      criteria={criteria}
      description="Use the learner context and objectives on the right, then read the candidate versions section by section and score each candidate independently."
      headline="Judge how suitable each candidate version is for this learner without losing the lesson goal."
      laneLabel="Revision-note comparison"
      middleColumn={
        <>
          <div className="space-y-2">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[color:var(--muted)]">
              Learner context
            </p>
            <p className="text-2xl font-semibold leading-snug text-[color:var(--ink)]">
              {getLearnerSummary(detail.focal_learner)}
            </p>
          </div>

          <dl className="space-y-4">
            {learnerTraits.map((trait) => (
              <ContextRow key={trait.key} label={trait.key} value={trait.value} />
            ))}
          </dl>
        </>
      }
      objectivesColumn={
        <div className="space-y-2">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[color:var(--muted)]">
            Lesson objectives
          </p>
          <ObjectivesPanel objectives={detail.objectives} />
        </div>
      }
      extraSection={
        <LearnerObjectiveStateTable states={detail.focal_learner.objective_states} />
      }
      onContinue={onContinue}
      progress={{ completedCount, packetPosition, queueLength, remainingCount }}
      secondaryAction={
        onDownloadWorksheet ? (
          <Button
            isLoading={isDownloadingWorksheet}
            onClick={onDownloadWorksheet}
            type="button"
            variant="outline"
          >
            Download worksheet PDF
          </Button>
        ) : null
      }
      sessionName={sessionName}
    />
  );
}
