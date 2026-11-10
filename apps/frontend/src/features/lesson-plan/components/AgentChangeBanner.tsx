import { useState } from "react";

import { Button } from "@/shared/components/ui/Button";

import type { PlanDiff } from "../lib/planDiff";
import { PlanDiffView } from "./PlanDiffView";

/** What the agent just changed in the plan, with a way to see it beside the old words and to go back. */
export function AgentChangeBanner({
  number,
  diff,
  onUndo,
  isUndoing,
  error,
}: {
  number: number;
  diff: PlanDiff;
  onUndo: () => void;
  isUndoing: boolean;
  error?: string | null;
}) {
  const [comparing, setComparing] = useState(false);
  const steps = diff.steps.length;
  return (
    <section
      aria-label="What the agent changed"
      className="flex flex-col gap-3"
    >
      <div className="flex items-center gap-3 bg-(--info-tint) px-4 py-3 text-sm text-(--info-ink)">
        <span className="flex-1">
          Version {number} ·{" "}
          {steps === 0
            ? "changed"
            : `${steps} ${steps === 1 ? "step" : "steps"} changed`}
        </span>
        <Button
          size="sm"
          variant="outline"
          onClick={() => setComparing(!comparing)}
        >
          {comparing ? "Hide" : "Compare"}
        </Button>
        <Button
          size="sm"
          variant="outline"
          isLoading={isUndoing}
          onClick={onUndo}
        >
          Undo
        </Button>
      </div>
      {error ? (
        <p role="alert" className="text-sm text-(--danger-ink)">
          {error}
        </p>
      ) : null}
      {comparing ? <PlanDiffView diff={diff} /> : null}
    </section>
  );
}
