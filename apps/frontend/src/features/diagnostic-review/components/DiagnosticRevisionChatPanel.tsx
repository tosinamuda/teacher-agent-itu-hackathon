import { useState } from "react";

import { RevisionSummary } from "@/shared/components/renderer/RevisionSummary";
import { Badge } from "@/shared/components/ui/Badge";
import { Button } from "@/shared/components/ui/Button";

import { DiagnosticRevisionTurn } from "../types";

type DiagnosticRevisionChatPanelProps = {
  turns: DiagnosticRevisionTurn[];
  onSubmit: (instruction: string, onSent: () => void) => void;
  isSubmitting: boolean;
  hasError: boolean;
  canSubmit: boolean;
};

/**
 * Chat-style human-in-the-loop revision for the MCQ diagnostic: type an
 * instruction (e.g. "make Q2 harder", "add an item on perimeter") and the model
 * rewrites the items in place, preserving objective coverage + valid answer keys.
 */
export function DiagnosticRevisionChatPanel({
  turns,
  onSubmit,
  isSubmitting,
  hasError,
  canSubmit,
}: DiagnosticRevisionChatPanelProps) {
  const [instruction, setInstruction] = useState("");

  const submit = () => {
    if (!instruction.trim() || !canSubmit) return;
    onSubmit(instruction.trim(), () => setInstruction(""));
  };

  return (
    <section className="space-y-4 rounded-2xl border border-(--line) bg-(--surface) p-5">
      <div className="flex items-center justify-between">
        <h3 className="text-base font-semibold text-(--ink)">Revise with feedback</h3>
        <Badge variant="accent">
          {turns.length} turn{turns.length === 1 ? "" : "s"}
        </Badge>
      </div>

      {turns.length === 0 ? (
        <p className="text-xs italic text-(--faint)">No revisions yet — this is the generated diagnostic.</p>
      ) : (
        <div className="max-h-64 space-y-3 overflow-y-auto pr-1">
          {turns.map((turn) => (
            <div key={turn.revision_turn_id} className="space-y-1">
              <div className="rounded-lg bg-accent-soft/40 p-2 text-sm text-(--ink)">
                {turn.instruction}
              </div>
              <div className="rounded-lg border border-(--line) p-2 text-xs text-(--ink-2)">
                <span className="font-semibold text-(--ink-2)">Revised:</span>{" "}
                <RevisionSummary
                  text={turn.summary || "Updated the diagnostic."}
                  className="inline"
                />
              </div>
            </div>
          ))}
        </div>
      )}

      <textarea
        value={instruction}
        onChange={(event) => setInstruction(event.target.value)}
        rows={2}
        placeholder="e.g. Make question 2 harder and add an item on perimeter"
        className="w-full rounded-lg border border-(--line) p-2 text-sm outline-none focus:border-accent-deep"
      />
      <div className="flex items-center justify-between">
        {hasError ? (
          <p className="text-xs text-(--danger)">Revision failed — please try again.</p>
        ) : (
          <span />
        )}
        <Button
          size="sm"
          onClick={submit}
          isLoading={isSubmitting}
          disabled={!canSubmit || !instruction.trim()}
        >
          Send revision
        </Button>
      </div>
    </section>
  );
}
