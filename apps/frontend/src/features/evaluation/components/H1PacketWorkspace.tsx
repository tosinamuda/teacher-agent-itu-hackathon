import { Button } from "@/shared/components/ui/Button";

import { EvaluationReferenceSheet, H1PacketDetail } from "../types";
import { H1RubricForm } from "./H1RubricForm";
import { ReviewPackPreview } from "./ReviewPackPreview";

type H1PacketWorkspaceProps = {
  detail: H1PacketDetail;
  isDownloadingWorksheet?: boolean;
  isSaving: boolean;
  nextPacketHref?: string;
  onDownloadWorksheet?: () => void;
  onOpenPacketBrief: () => void;
  onSubmit: (payload: {
    rubric_scores: Record<string, number>;
    notes?: {
      strengths?: string;
      concerns?: string;
      recommendation?: string;
    } | null;
  }) => Promise<void>;
};

const lessonSummary = (referenceSheet: EvaluationReferenceSheet) =>
  [referenceSheet.grade, referenceSheet.subject, referenceSheet.subtopic]
    .filter(Boolean)
    .join(" · ");

/** Renders the H1 review workspace after the packet brief has been acknowledged. */
export function H1PacketWorkspace({
  detail,
  isDownloadingWorksheet = false,
  isSaving,
  nextPacketHref,
  onDownloadWorksheet,
  onOpenPacketBrief,
  onSubmit,
}: H1PacketWorkspaceProps) {
  return (
    <div className="flex min-h-0 flex-col gap-3 px-4 py-4 min-[1200px]:h-full min-[1200px]:overflow-hidden min-[1200px]:px-6">
      <section className="shrink-0 rounded-none border border-[color:var(--line)] bg-[color:var(--panel)]/90 px-4 py-3">
        <div className="flex flex-col gap-4 min-[1200px]:flex-row min-[1200px]:items-start">
          <div className="space-y-2 min-[1200px]:w-[20rem] min-[1200px]:shrink-0">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[color:var(--muted)]">
              {detail.candidate_label
                ? `${detail.candidate_label}${
                    detail.candidate_count
                      ? ` · ${detail.candidate_count} candidates in this lesson`
                      : ""
                  }`
                : "Revision-note review"}
            </p>
            <p className="text-sm font-semibold text-[color:var(--ink)]">
              {lessonSummary(detail.reference_sheet) || detail.lesson_title || "Lesson reference"}
            </p>
          </div>

          <div className="min-w-0 flex-1 space-y-2">
            <div className="flex items-center justify-between gap-3">
              <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[color:var(--muted)]">
                Objectives in view
              </p>
              <p className="text-xs font-medium text-[color:var(--accent-deep)]">
                {detail.objectives.length} objective{detail.objectives.length === 1 ? "" : "s"}
              </p>
            </div>
            <ol className="flex flex-col gap-2 text-sm text-[color:var(--muted)]">
              {detail.objectives.map((objective, index) => (
                <li
                  key={objective.lesson_objective_id}
                  className="border-l-2 border-[color:var(--accent)]/55 pl-3 leading-6"
                >
                  <span className="mr-2 font-semibold text-[color:var(--ink)]">{index + 1}.</span>
                  {objective.objective_text ?? objective.lesson_objective_id}
                </li>
              ))}
            </ol>
          </div>

          <div className="flex flex-wrap items-center gap-2 min-[1200px]:ml-auto min-[1200px]:mt-1">
            {onDownloadWorksheet ? (
              <Button
                isLoading={isDownloadingWorksheet}
                onClick={onDownloadWorksheet}
                size="sm"
                type="button"
                variant="outline"
              >
                Download worksheet PDF
              </Button>
            ) : null}
            <Button onClick={onOpenPacketBrief} size="sm" type="button" variant="outline">
              View packet brief
            </Button>
          </div>
        </div>
      </section>

      <section className="rounded-none border border-[color:var(--line)] bg-white p-3 min-[1200px]:flex-1 min-[1200px]:min-h-0 min-[1200px]:overflow-hidden">
        <div className="flex flex-col gap-3 min-[1200px]:h-full min-[1200px]:min-h-0 min-[1200px]:flex-row">
          <div className="flex min-h-0 min-w-0 flex-1 flex-col overflow-hidden rounded-none border border-[color:var(--line)] bg-[color:var(--panel)]">
            <div className="border-b border-[color:var(--line)] px-4 py-3">
              <p className="text-sm font-semibold text-[color:var(--ink)]">
                Take-home student revision note
              </p>
              <p className="mt-1 text-sm text-[color:var(--muted)]">
                Read the teacher&apos;s note and keep the lesson brief available
                from the header when needed.
              </p>
            </div>
            <div className="min-h-0 p-4 min-[1200px]:overflow-y-auto">
              <ReviewPackPreview
                anchorPrefix={`candidate-${detail.evaluation_packet_id}`}
                label="Take-home student revision note"
                pack={detail.candidate_pack}
                showStepNavigator
                showLabel={false}
                tone="candidate"
              />
            </div>
          </div>

          <div className="flex min-h-0 shrink-0 flex-col overflow-hidden rounded-none border border-[color:var(--line)] bg-[color:var(--panel)] min-[1200px]:w-[18rem]">
            <div className="border-b border-[color:var(--line)] px-4 py-3">
              <p className="text-sm font-semibold text-[color:var(--ink)]">Rating</p>
              <p className="mt-1 text-xs leading-5 text-[color:var(--muted)]">
                Score against the lesson objectives and scope while the pack stays in view.
              </p>
            </div>
            <H1RubricForm
              detail={detail}
              isSaving={isSaving}
              nextPacketHref={nextPacketHref}
              onSubmit={onSubmit}
            />
          </div>
        </div>
      </section>
    </div>
  );
}
