import { useState } from "react";

import { Button } from "@/shared/components/ui/Button";
import type { NeedsItem } from "@/shared/components/workspace/RightPanel";
import { ReasonAction } from "@/shared/components/workspace/ReasonAction";

import { useApproveContent, useRejectContent, useReviseContent } from "../hooks/useContent";
import { ContentItem } from "../types";

/** Reject a pending version, or withdraw an approved one, with the reason the teacher gives. */
export function Rejection({ item }: { item: ContentItem }) {
  const reject = useRejectContent(item.id);
  const withdrawing = item.review_status === "approved";
  return (
    <ReasonAction
      verb={withdrawing ? "Withdraw approval" : "Reject"}
      isPending={reject.isPending}
      error={
        reject.isError ? "It changed since you opened it. Review the current version, then try again." : null
      }
      note={
        withdrawing && item.type === "revision-note" && item.level === "class"
          ? "The learners' notes made from this one are withdrawn with it."
          : undefined
      }
      onSubmit={(reason) => reject.mutate({ expectedVersion: item.version, reason })}
    />
  );
}

/** Say what to change in a few words; the version is revised and comes back for review. */
function ReviseWithFeedback({ item }: { item: ContentItem }) {
  const revise = useReviseContent(item.id);
  const [feedback, setFeedback] = useState("");
  return (
    <details className="text-sm">
      <summary className="cursor-pointer font-semibold text-(--ink)">Revise with feedback</summary>
      <div className="mt-2 space-y-2">
        <textarea
          id="content-feedback"
          rows={2}
          value={feedback}
          onChange={(event) => setFeedback(event.target.value)}
          placeholder="Say what to change; everything else is kept as it is."
          className="w-full border border-(--line) p-2 text-sm outline-none focus:border-(--accent)"
        />
        {revise.isError ? (
          <p className="text-xs text-(--danger-ink)">The revision failed. Please try again.</p>
        ) : null}
        <Button
          size="sm"
          variant="secondary"
          isLoading={revise.isPending}
          disabled={!feedback.trim()}
          onClick={() => revise.mutate(feedback.trim(), { onSuccess: () => setFeedback("") })}
        >
          Send revision
        </Button>
      </div>
    </details>
  );
}

/** Reject, ask the agent for changes, or approve: the way to decide on a version waiting for review. */
function DecisionActions({ item, openAgent }: { item: ContentItem; openAgent: () => void }) {
  const approve = useApproveContent(item.id);
  return (
    <>
      {approve.isError ? (
        <p className="w-full text-xs text-(--danger-ink)">
          It changed since you opened it. Review the current version, then approve again.
        </p>
      ) : null}
      <Rejection item={item} />
      <Button size="sm" variant="secondary" onClick={openAgent}>
        Ask for changes
      </Button>
      <Button size="sm" isLoading={approve.isPending} onClick={() => approve.mutate(item.version)}>
        {item.type === "class-test" ? "Approve and send" : "Approve"}
      </Button>
    </>
  );
}

/** What waits on the teacher for this version, if anything: to decide on it, or to revise a rejected one. */
export function decisionOf(item: ContentItem, label: string, grounding: string | null): NeedsItem | null {
  if (item.read_only) return null;
  if (item.review_status === "rejected") {
    return {
      id: "rejected",
      title: `The ${label} was rejected`,
      detail: item.review_reason ? item.review_reason.replace(/[.\s]+$/, "") : "Ask the agent to revise it, then review it again.",
      body: <ReviseWithFeedback item={item} />,
      actions: ({ openAgent }) => (
        <Button size="sm" variant="secondary" onClick={openAgent}>
          Ask for changes
        </Button>
      ),
    };
  }
  if (item.review_status === "approved") return null;
  return {
    id: "decision",
    title: item.type === "class-test" ? "Approve and send to students?" : `Approve the ${label}?`,
    detail: grounding ?? (item.type === "class-test" ? "Once sent, it can no longer be revised." : undefined),
    body: item.type === "class-test" ? undefined : <ReviseWithFeedback item={item} />,
    actions: ({ openAgent }) => <DecisionActions item={item} openAgent={openAgent} />,
  };
}
