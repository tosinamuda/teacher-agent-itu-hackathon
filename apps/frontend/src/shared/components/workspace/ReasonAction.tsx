import { useState, type ReactNode } from "react";

import { Button } from "@/shared/components/ui/Button";

const MIN_REASON = 3;

/**
 * A button that asks why before it acts: the reason goes with the decision and is kept with it.
 * Used to reject a draft or take an approval back.
 */
export function ReasonAction({
  verb,
  note,
  error,
  isPending,
  onSubmit,
}: {
  verb: string;
  /** What the action does and does not change, said before the teacher commits. */
  note?: ReactNode;
  error?: string | null;
  isPending: boolean;
  onSubmit: (reason: string) => void;
}) {
  const [open, setOpen] = useState(false);
  const [reason, setReason] = useState("");

  if (!open) {
    return (
      <Button size="sm" variant="secondary" onClick={() => setOpen(true)}>
        {verb}
      </Button>
    );
  }
  return (
    <div className="w-full space-y-2">
      <label
        htmlFor="decision-reason"
        className="text-sm font-semibold text-(--ink)"
      >
        Why? Your reason is kept with it.
      </label>
      <textarea
        id="decision-reason"
        rows={2}
        value={reason}
        onChange={(event) => setReason(event.target.value)}
        className="w-full border border-(--line) p-2 text-sm outline-none focus:border-(--accent)"
      />
      {note ? <p className="text-xs text-(--ink-2)">{note}</p> : null}
      {error ? <p className="text-xs text-(--danger-ink)">{error}</p> : null}
      <div className="flex gap-2">
        <Button
          size="sm"
          isLoading={isPending}
          disabled={reason.trim().length < MIN_REASON}
          onClick={() => onSubmit(reason.trim())}
        >
          {verb}
        </Button>
        <Button size="sm" variant="secondary" onClick={() => setOpen(false)}>
          Cancel
        </Button>
      </div>
    </div>
  );
}
