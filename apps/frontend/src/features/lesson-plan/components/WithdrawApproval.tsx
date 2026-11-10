import { useState } from "react";

import {
  useContentTypes,
  useLessonContent,
} from "@/features/content/hooks/useContent";
import { Button } from "@/shared/components/ui/Button";
import { Modal } from "@/shared/components/ui/Modal";

const MIN_REASON = 3;

const REVIEW_WORD = {
  approved: "Approved",
  pending: "Waiting for your review",
  rejected: "Rejected",
} as const;

/** Taking an approval back: what it leaves as it is, the materials made from it, and why. */
export function WithdrawApproval({
  planVersionId,
  isOpen,
  onClose,
  isPending,
  error,
  onWithdraw,
}: {
  planVersionId: string;
  isOpen: boolean;
  onClose: () => void;
  isPending: boolean;
  error: string | null;
  onWithdraw: (reason: string) => void;
}) {
  const [reason, setReason] = useState("");
  const labels = new Map(
    (useContentTypes().data ?? []).map((info) => [info.type, info.label]),
  );
  const made = (useLessonContent(planVersionId).data ?? []).filter(
    (item) => item.level === "class",
  );

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Withdraw approval?">
      <div className="flex flex-col gap-4">
        <p className="text-sm text-(--ink-2)">
          Materials already made from this plan, and what students have seen,
          stay as they are. Nothing new can be made until a plan is approved
          again.
        </p>
        {made.length > 0 ? (
          <ul className="divide-y divide-(--line) border-y border-(--line)">
            {made.map((item) => (
              <li
                key={item.id}
                className="flex items-center justify-between gap-4 py-2.5 text-sm"
              >
                <span className="text-(--ink)">
                  {labels.get(item.type) ?? item.type}
                </span>
                <span className="text-xs text-(--ink-2)">
                  {REVIEW_WORD[item.review_status]}
                </span>
              </li>
            ))}
          </ul>
        ) : null}
        <label
          htmlFor="withdraw-reason"
          className="text-sm font-semibold text-(--ink)"
        >
          Why? Your reason is kept with it.
        </label>
        <textarea
          id="withdraw-reason"
          rows={2}
          value={reason}
          onChange={(event) => setReason(event.target.value)}
          className="w-full border border-(--line) p-2 text-sm outline-none focus:border-(--accent)"
        />
        {error ? <p className="text-xs text-(--danger-ink)">{error}</p> : null}
        <div className="flex gap-2">
          <Button size="sm" variant="secondary" onClick={onClose}>
            Keep approved
          </Button>
          <Button
            size="sm"
            isLoading={isPending}
            disabled={reason.trim().length < MIN_REASON}
            onClick={() => onWithdraw(reason.trim())}
          >
            Withdraw approval
          </Button>
        </div>
      </div>
    </Modal>
  );
}
