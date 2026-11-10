import { useState, type ReactNode } from "react";

import { useRouter } from "@/shared/router";

import { ContentConversation } from "@/features/content-chat/ContentChat";
import { useLearnerName } from "@/features/learners/hooks/useLearnerName";
import { LessonPlanComparePanel } from "@/features/pack-review/components/LessonPlanComparePanel";
import { MissingPackPanel } from "@/features/pack-review/components/MissingPackPanel";
import { useReviewLessonPlan } from "@/features/pack-review/hooks/useReviewLessonPlan";
import { Button } from "@/shared/components/ui/Button";
import { Status } from "@/shared/components/ui/StatusMark";
import { RightPanel } from "@/shared/components/workspace/RightPanel";
import { WorkspacePage } from "@/shared/components/workspace/WorkspacePage";

import { Rejection, decisionOf } from "../components/ContentDecision";
import { ContentHistory } from "../components/ContentHistory";
import { ContentView } from "../components/ContentView";
import { DownloadFileButton } from "../components/DownloadFileButton";
import { ReviewEvidence } from "../components/ReviewEvidence";
import { useContent, useContentTypes } from "../hooks/useContent";
import { groundingLine } from "../status";
import { ContentItem, Origin } from "../types";

const ORIGINS: Record<Origin, string> = {
  teacher: "Written by the teacher",
  study_record: "From the study's record",
  generated: "Drafted by the app",
};

/** The lesson plan the note is built from, beside the note, so the teacher can judge its fidelity. */
function PlanBeside({ planVersionId }: { planVersionId: string }) {
  const plan = useReviewLessonPlan(planVersionId, true);
  return (
    <div className="relative max-h-[70dvh] overflow-y-auto overscroll-contain border border-(--line) bg-white p-4 md:max-h-none md:min-h-0">
      {plan.isLoading ? (
        <p className="text-sm text-(--ink-2)">Loading lesson plan…</p>
      ) : plan.data ? (
        <LessonPlanComparePanel plan={plan.data} />
      ) : (
        <p className="text-sm text-(--danger-ink)">
          Couldn&apos;t load the lesson plan.
        </p>
      )}
    </div>
  );
}

/** The chat with the agent, unless the material can no longer change. */
function AgentNote({
  item,
  children,
}: {
  item: ContentItem;
  children: ReactNode;
}) {
  if (item.read_only) {
    return (
      <p className="text-xs text-(--faint)">
        This belongs to a concluded study. It can be read, and it will not
        change.
      </p>
    );
  }
  if (item.type === "class-test" && item.review_status === "approved") {
    return (
      <p className="text-xs text-(--faint)">
        Sent to students; it can no longer be revised.
      </p>
    );
  }
  return <>{children}</>;
}

/** Any content, read in one place, with the decision and the agent beside it. */
export function ContentReviewPage({ contentId }: { contentId: string }) {
  const router = useRouter();
  const [section, setSection] = useState(0);
  const [comparing, setComparing] = useState(false);
  const query = useContent(contentId);
  const item = query.data;
  const types = useContentTypes();
  const learnerName = useLearnerName(item?.student_id ?? null);

  if (query.isLoading) {
    return <p className="px-8 py-6 text-sm text-(--ink-2)">Loading…</p>;
  }
  if (query.isError || !item) {
    return (
      <p className="px-8 py-6 text-sm text-(--ink-2)">
        This material was not found.
      </p>
    );
  }

  const label =
    types.data?.find((type) => type.type === item.type)?.label ?? item.type;
  const spec = item.provenance.specification;
  const grounding = groundingLine(item.provenance);
  const approved = item.review_status === "approved";
  const decision = decisionOf(item, label.toLowerCase(), grounding);
  const canWithdraw = approved && !item.read_only && item.type !== "class-test";
  const panel = (
    <RightPanel
      key={item.review_status}
      defaultTab={decision ? "needs" : "agent"}
      needs={decision ? [decision] : []}
      agent={
        <AgentNote item={item}>
          <ContentConversation
            contentId={item.id}
            open
            highlight={null}
            onSent={() => undefined}
          />
        </AgentNote>
      }
    />
  );

  return (
    <WorkspacePage panel={panel}>
      <div className="flex flex-col gap-5">
        <header className="flex flex-wrap items-start justify-between gap-x-4 gap-y-2">
          <div className="min-w-0 space-y-1">
            <button
              type="button"
              onClick={router.back}
              className="text-sm text-(--accent-deep) hover:underline"
            >
              ← Back
            </button>
            <h1 className="text-2xl font-semibold text-(--ink)">
              {label}
              {item.level === "learner" ? ` · for ${learnerName ?? "one learner"}` : ""}
            </h1>
            {item.version > 1 ? (
              <p className="text-xs text-(--ink-2)">Version {item.version}</p>
            ) : null}
          </div>
          <div className="flex items-center gap-2">
            {item.type === "revision-note" ? (
              <Button
                size="sm"
                variant="secondary"
                onClick={() => setComparing((value) => !value)}
              >
                {comparing ? "Hide lesson plan" : "Compare with lesson plan"}
              </Button>
            ) : null}
            {item.has_file ? <DownloadFileButton contentId={item.id} /> : null}
          </div>
        </header>

        <div className="flex min-h-0 flex-col md:h-[70dvh]">
          {comparing ? (
            <div className="grid min-h-0 flex-1 gap-3 lg:grid-cols-2">
              <PlanBeside planVersionId={item.plan_version_id} />
              <div className="flex min-h-0 min-w-0 flex-col">
                <ContentView
                  item={item}
                  section={section}
                  onSectionChange={setSection}
                />
              </div>
            </div>
          ) : (
            <ContentView
              item={item}
              section={section}
              onSectionChange={setSection}
            />
          )}
        </div>

        {approved ? <Status kind="complete">Approved</Status> : null}
        <details className="text-xs text-(--ink-2)">
          <summary className="cursor-pointer font-semibold hover:text-(--ink)">
            How it was made
          </summary>
          <p className="mt-2">
            {item.provenance.origin
              ? `${ORIGINS[item.provenance.origin]} · `
              : ""}
            Version {item.version}
            {spec ? ` · spec revision ${spec.revision}` : ""}
            {item.provenance.pipeline
              ? ` · pipeline ${item.provenance.pipeline}`
              : ""}
            {item.provenance.generator &&
            item.provenance.generator.ref !== "builtin"
              ? ` · generator ${item.provenance.generator.ref}`
              : ""}
            {grounding ? ` · ${grounding}` : ""}
          </p>
        </details>
        {item.type === "revision-note" && item.level === "class" && approved ? (
          <MissingPackPanel planVersionId={item.plan_version_id} />
        ) : null}
        {item.review ? <ReviewEvidence item={item} section={section} /> : null}
        {canWithdraw ? <Rejection item={item} /> : null}
        <ContentHistory contentId={item.id} />
      </div>
    </WorkspacePage>
  );
}
