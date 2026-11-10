import { makePlanPath, writePlanPath } from "../lib/planPaths";
import { useCallback, useState } from "react";

import {
  COMMENT_EVENT,
  type ViewComment,
} from "@/features/mcp-app/viewMessage";

import { ContentConversation } from "@/features/content-chat/ContentChat";
import { Button, buttonClass } from "@/shared/components/ui/Button";
import { Status, StatusMark } from "@/shared/components/ui/StatusMark";
import { ReasonAction } from "@/shared/components/workspace/ReasonAction";
import {
  OPEN_AGENT_EVENT,
  RightPanel,
  type NeedsItem,
} from "@/shared/components/workspace/RightPanel";
import { WorkspacePage } from "@/shared/components/workspace/WorkspacePage";
import { CreationsInProgress } from "@/features/lesson-home/components/CreationsInProgress";
import { LessonConversations } from "@/features/lesson-home/components/LessonConversations";
import { Link, useRouter } from "@/shared/router";

import { LessonPlanManualEditor } from "../components/LessonPlanManualEditor";
import { PlanDocument } from "../components/PlanDocument";
import { PlanHistory } from "../components/PlanHistory";
import { PlanMenu, type PlanMenuItem } from "../components/PlanMenu";
import { WithdrawApproval } from "../components/WithdrawApproval";
import {
  usePlanGenerator,
  type PlanGenerationResponse,
} from "../hooks/usePlanGenerator";
import { useManualEdit } from "../hooks/useManualEdit";
import { useLastChange } from "../hooks/useLastChange";
import { useTextSelection } from "../hooks/useTextSelection";
import { AgentChangeBanner } from "../components/AgentChangeBanner";
import { SelectionBubble } from "../components/SelectionBubble";
import { closingError } from "../lib/closingError";
import { planChecks } from "../lib/planChecks";
import { planSubtitle } from "../lib/planSummary";

const lessonHomeHref = (sessionId: string) =>
  `/research/teacher/lessons/${sessionId}`;

const dayOf = (iso?: string | null): string =>
  iso ? ` ${iso.slice(0, 10)}` : "";

/** The agent's checks, then the way to decide. Approving also queues the class test. */
function decisionOf(
  plan: PlanGenerationResponse,
  approve: () => void,
  isApproving: boolean,
  reject: {
    run: (reason: string) => void;
    isPending: boolean;
    error: string | null;
  },
): NeedsItem {
  return {
    id: "approve",
    title: "Approve the plan?",
    detail: "Approving also makes the class test.",
    body: (
      <div className="flex flex-col gap-2">
        {planChecks(plan.unmet_requirements).map((check) => (
          <Status key={check.text} kind={check.status}>
            {check.text}
          </Status>
        ))}
        <p className="text-xs text-(--faint)">
          Select text in a step to ask the agent to change it.
        </p>
      </div>
    ),
    actions: ({ openAgent }) => (
      <>
        <ReasonAction
          verb="Reject"
          note="Rejecting discards this draft. It stays in the lesson's history with your reason."
          isPending={reject.isPending}
          error={reject.error}
          onSubmit={reject.run}
        />
        <Button size="sm" variant="secondary" onClick={openAgent}>
          Ask for changes
        </Button>
        <Button size="sm" isLoading={isApproving} onClick={approve}>
          Approve
        </Button>
      </>
    ),
  };
}

/** The way on from a plan that was discarded or taken back. */
function whatNextOf(
  plan: PlanGenerationResponse,
  sessionId: string | undefined,
  go: (href: string) => void,
): NeedsItem {
  const withdrawn = plan.version_status === "withdrawn";
  return {
    id: "what-next",
    title: withdrawn
      ? "Approval withdrawn. What next?"
      : "Plan rejected. What next?",
    detail: `${withdrawn ? "Withdrawn" : "Rejected"}${dayOf(plan.closed_at)}`,
    body: plan.closed_reason ? (
      <p className="bg-(--sunken) px-3 py-2 text-sm text-(--ink)">
        {plan.closed_reason}
      </p>
    ) : null,
    actions: sessionId ? (
      <>
        <Button
          size="sm"
          variant="secondary"
          onClick={() => go(writePlanPath(sessionId))}
        >
          Write it by hand
        </Button>
        <Button size="sm" onClick={() => go(makePlanPath(sessionId))}>
          Write a new version
        </Button>
      </>
    ) : undefined,
  };
}

/** A lesson plan as a document, with the decision and the agent beside it. */
export function PlanPage({ planId }: { planId: string }) {
  const router = useRouter();
  const {
    planData,
    approve,
    close,
    isClosing,
    closeError,
    isApproving,
    isFetching,
    approveError,
    loadFailed,
    reload,
  } = usePlanGenerator(planId);
  const manualEdit = useManualEdit(planId);
  const { selection, rect, clear, hideBubble } = useTextSelection();
  const [editing, setEditing] = useState(false);
  const [withdrawing, setWithdrawing] = useState(false);
  // The step the teacher pointed at, while the agent changes it.
  const [revising, setRevising] = useState(false);
  const [pointedStep, setPointedStep] = useState<string | null>(null);
  const lastChange = useLastChange(planData);
  const agentWorking = useCallback((working: boolean) => {
    setRevising(working);
    if (!working) setPointedStep(null);
  }, []);

  if (!planData) {
    if (loadFailed) {
      return (
        <div className="flex flex-col items-start gap-3 px-8 py-6">
          <p className="text-sm text-(--danger)">
            The plan could not be loaded.
          </p>
          <Button size="sm" variant="secondary" onClick={() => void reload()}>
            Try again
          </Button>
        </div>
      );
    }
    return (
      <p className="px-8 py-6 text-sm text-(--ink-2)">
        {isFetching ? "Loading the plan…" : "This plan was not found."}
      </p>
    );
  }
  const approved = planData.version_status === "approved";
  const closed =
    planData.version_status === "rejected" ||
    planData.version_status === "withdrawn";
  const withdrawn = planData.version_status === "withdrawn";
  const closing = {
    run: (reason: string) => close({ versionId: planData.version_id, reason }),
    isPending: isClosing,
    error: closingError(closeError),
  };
  const sessionId = planData.session_id;
  const { subtopic, topic } = planData.session_plan;
  const regenerate = () => sessionId && router.push(makePlanPath(sessionId));
  const menu: PlanMenuItem[] = [
    ...(approved
      ? [{ label: "Withdraw approval", onSelect: () => setWithdrawing(true) }]
      : []),
    ...(sessionId && !closed
      ? [{ label: "Write a new version", onSelect: regenerate }]
      : []),
  ];

  const panel = (
    <RightPanel
      key={planData.version_status}
      defaultTab={approved ? "agent" : "needs"}
      needs={
        approved
          ? []
          : closed
            ? [whatNextOf(planData, sessionId, router.push)]
            : [
                decisionOf(
                  planData,
                  () => approve(planData.version_id),
                  isApproving,
                  closing,
                ),
              ]
      }
      agent={
        <div className="flex flex-col gap-4">
          {approved ? (
            <CreationsInProgress planVersionId={planData.version_id} />
          ) : null}
          <ContentConversation
            contentId={planData.plan_id}
            open
            highlight={selection}
            onSent={(pointed) => {
              clear();
              setPointedStep(pointed?.step_id ?? null);
            }}
            onClearHighlight={clear}
            onWorkingChange={agentWorking}
          />
          {sessionId ? (
            <LessonConversations lessonPeriodId={sessionId} />
          ) : null}
        </div>
      }
    />
  );

  return (
    <WorkspacePage panel={panel}>
      <div className="flex flex-col gap-6">
        {approved ? (
          <div className="flex items-center gap-3 bg-(--sunken) px-4 py-3 text-sm text-(--ink)">
            <StatusMark kind="complete" />
            <span className="flex-1">
              Approved{dayOf(planData.approved_at)}. The class materials are
              unlocked.
            </span>
            {sessionId ? (
              <Link
                href={lessonHomeHref(sessionId)}
                className={buttonClass({ variant: "secondary", size: "sm" })}
              >
                Make the class materials
              </Link>
            ) : null}
          </div>
        ) : null}

        {!approved &&
        !closed &&
        planData.run_metadata?.source === "document_import" ? (
          <p className="bg-(--sunken) px-4 py-3 text-sm text-(--ink)">
            Imported from your document.
          </p>
        ) : null}

        {closed ? (
          <div className="flex items-center gap-3 bg-(--sunken) px-4 py-3 text-sm text-(--ink)">
            <StatusMark kind={withdrawn ? "withdrawn" : "rejected"} />
            <span className="flex-1">
              {withdrawn ? "Approval withdrawn" : "Rejected"}
              {dayOf(planData.closed_at)}.{" "}
              {withdrawn
                ? "Nothing new can be made from this version."
                : "Nothing can be made from this version."}
              {withdrawn
                ? " Materials already made from it stay as they are."
                : ""}
            </span>
            {sessionId ? (
              <Link
                href={lessonHomeHref(sessionId)}
                className={buttonClass({ variant: "secondary", size: "sm" })}
              >
                Open lesson
              </Link>
            ) : null}
          </div>
        ) : null}

        <header className="flex items-start justify-between gap-4">
          <div className="flex flex-col gap-1">
            <h1 className="text-2xl font-semibold text-(--ink)">
              {subtopic ?? topic ?? "Lesson plan"}
            </h1>
            <p className="text-xs text-(--ink-2)">
              {planSubtitle(planData.session_plan)}
            </p>
          </div>
          <div className="flex shrink-0 items-center gap-2">
            {!approved && !closed && !editing ? (
              <Button
                size="sm"
                variant="secondary"
                onClick={() => setEditing(true)}
              >
                Edit
              </Button>
            ) : null}
            <PlanMenu items={menu} />
          </div>
        </header>

        {lastChange && !editing && !approved && !closed ? (
          <AgentChangeBanner
            number={lastChange.number}
            diff={lastChange.diff}
            isUndoing={manualEdit.isPending}
            error={
              manualEdit.isError ? "Couldn't undo. Nothing was changed." : null
            }
            onUndo={() => manualEdit.mutate(lastChange.previous)}
          />
        ) : null}

        {approveError ? (
          <p className="text-sm text-(--danger)">{approveError.message}</p>
        ) : null}

        {editing ? (
          <LessonPlanManualEditor
            sessionPlan={planData.session_plan}
            isSaving={manualEdit.isPending}
            error={manualEdit.isError ? "Couldn't save your edits." : null}
            onSave={(next) =>
              manualEdit.mutate(next, { onSuccess: () => setEditing(false) })
            }
            onCancel={() => setEditing(false)}
          />
        ) : (
          <PlanDocument
            sessionPlan={planData.session_plan}
            changedStepIds={
              lastChange
                ? new Set(lastChange.diff.steps.map((step) => step.stepId))
                : undefined
            }
            revisingStepId={revising ? pointedStep : null}
          />
        )}

        {selection && rect && !editing ? (
          <SelectionBubble
            rect={rect}
            onAsk={(request) => {
              const comment: ViewComment = {
                contentId: planData.plan_id,
                text: request,
                highlight: selection,
              };
              window.dispatchEvent(new Event(OPEN_AGENT_EVENT));
              window.dispatchEvent(
                new CustomEvent(COMMENT_EVENT, { detail: comment }),
              );
              setPointedStep(selection.step_id ?? null);
              clear();
            }}
            onEdit={
              !approved && !closed
                ? () => {
                    clear();
                    setEditing(true);
                  }
                : undefined
            }
            onDismiss={hideBubble}
          />
        ) : null}

        <PlanHistory plan={planData} />
        {withdrawing && approved ? (
          <WithdrawApproval
            planVersionId={planData.version_id}
            isOpen
            onClose={() => setWithdrawing(false)}
            isPending={closing.isPending}
            error={closing.error}
            onWithdraw={closing.run}
          />
        ) : null}
      </div>
    </WorkspacePage>
  );
}
