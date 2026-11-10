import { useState } from "react";

import { Button } from "@/shared/components/ui/Button";

import { usePlanVersion } from "../hooks/usePlanVersion";
import type { PlanGenerationResponse } from "../hooks/usePlanGenerator";
import { useSessionPlans } from "../hooks/useSessionPlans";
import { diffPlans } from "../lib/planDiff";
import {
  sourceLabel,
  statusWord,
  versionsOfPlan,
  type NumberedVersion,
} from "../lib/planVersions";
import { PlanDiffView } from "./PlanDiffView";
import type { SessionPlanData } from "./SessionPlanView";

/** What one version changed, against the version before it. */
function WhatChanged({
  version,
  before,
}: {
  version: NumberedVersion;
  before: NumberedVersion;
}) {
  const after = usePlanVersion(version.version_id);
  const was = usePlanVersion(before.version_id);
  if (!after.data || !was.data) {
    return <p className="text-sm text-(--ink-2)">Loading both versions…</p>;
  }
  return (
    <div className="flex flex-col gap-3">
      <p className="text-sm text-(--ink-2)">
        Version {before.number} to version {version.number}
      </p>
      <PlanDiffView
        diff={diffPlans(
          was.data.session_plan as SessionPlanData,
          after.data.session_plan as SessionPlanData,
        )}
      />
    </div>
  );
}

/** Every version of the plan, and for each one what it changed. */
export function PlanHistory({ plan }: { plan: PlanGenerationResponse }) {
  const [shown, setShown] = useState<number | null>(null);
  const summaries = useSessionPlans(plan.session_id);
  const versions = versionsOfPlan(summaries.data ?? [], plan.plan_id);
  if (versions.length < 2) return null;

  const open = versions.find((version) => version.number === shown);
  const before = open ? versions[open.number - 2] : undefined;

  return (
    <details className="text-sm">
      <summary className="cursor-pointer text-base font-semibold text-(--ink)">
        History{" "}
        <span className="text-sm font-normal text-(--ink-2)">
          · {versions.length} versions
        </span>
      </summary>
      <ul className="mt-3 border border-(--line) bg-(--surface)">
        {[...versions].reverse().map((version) => (
          <li
            key={version.version_id}
            className="flex items-center gap-4 border-t border-(--line) px-4 py-3 first:border-t-0"
          >
            <span className="flex min-w-0 flex-1 flex-col">
              <span className="text-sm font-semibold text-(--ink)">
                Version {version.number}
                {version.version_id === plan.version_id ? " · current" : ""}
              </span>
              <span className="text-xs text-(--ink-2)">
                {[
                  sourceLabel(version.source_type),
                  statusWord(version.status),
                  version.created_at.slice(0, 10),
                ]
                  .filter(Boolean)
                  .join(" · ")}
              </span>
            </span>
            {version.number > 1 ? (
              <Button
                size="sm"
                variant="secondary"
                onClick={() =>
                  setShown(shown === version.number ? null : version.number)
                }
              >
                {shown === version.number ? "Hide changes" : "What changed"}
              </Button>
            ) : null}
          </li>
        ))}
      </ul>
      {open && before ? (
        <div className="mt-4">
          <WhatChanged version={open} before={before} />
        </div>
      ) : null}
    </details>
  );
}
