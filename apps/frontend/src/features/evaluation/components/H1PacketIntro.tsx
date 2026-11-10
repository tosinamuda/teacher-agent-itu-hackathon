import { Button } from "@/shared/components/ui/Button";

import { ContextRow, ObjectivesPanel } from "./PacketMetaPanels";
import { PacketIntroFrame } from "./PacketIntroShared";
import { H1PacketDetail } from "../types";

/** Renders the H1 packet orientation screen before the live review opens. */
export function H1PacketIntro({
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
  detail: H1PacketDetail;
  isDownloadingWorksheet?: boolean;
  onDownloadWorksheet?: () => void;
  onContinue: () => void;
  packetPosition: number | null;
  queueLength: number;
  remainingCount: number;
  sessionName: string;
}) {
  const lessonMeta = [
    detail.reference_sheet.term,
    detail.reference_sheet.week ? `Week ${detail.reference_sheet.week}` : null,
    detail.reference_sheet.theme ? `Theme: ${detail.reference_sheet.theme}` : null,
  ]
    .filter(Boolean)
    .join(" · ");

  return (
    <PacketIntroFrame
      continueLabel="Start review"
      criteria={detail.rubric.map((criterion) => criterion.display_label ?? criterion.label)}
      description="Use the lesson context and objectives on the right, then review one take-home student revision note and score how well it stays aligned."
      headline={`This is a take-home student revision note prepared by a teacher for a ${detail.reference_sheet.grade} ${detail.reference_sheet.subject} lesson on ${detail.reference_sheet.subtopic}.`}
      laneLabel={detail.candidate_label ?? "Student revision note"}
      middleColumn={
        <>
          <div className="space-y-2">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[color:var(--muted)]">
              Current lesson
            </p>
            <p className="text-2xl font-semibold leading-snug text-[color:var(--ink)]">
              {detail.lesson_title ?? "Lesson focus unavailable"}
            </p>
            {lessonMeta ? <p className="text-base text-[color:var(--muted)]">{lessonMeta}</p> : null}
          </div>

          <dl className="space-y-4">
            <ContextRow label="Class" value={detail.reference_sheet.grade} />
            <ContextRow label="Subject" value={detail.reference_sheet.subject} />
            <ContextRow label="Topic" value={detail.reference_sheet.topic} />
            <ContextRow label="Subtopic" value={detail.reference_sheet.subtopic} />
          </dl>
        </>
      }
      objectivesColumn={
        <>
          <div className="flex items-center justify-between gap-3">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[color:var(--muted)]">
              Lesson objectives
            </p>
            <p className="text-sm font-medium text-[color:var(--accent-deep)]">
              {detail.objectives.length} objective{detail.objectives.length === 1 ? "" : "s"} in scope
            </p>
          </div>
          <ObjectivesPanel objectives={detail.objectives} />
        </>
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
