import { useState } from "react";

import { LiveWork } from "@/features/content-chat/LiveWork";
import { failureLine } from "@/features/content/failure";
import { useGenerateContent } from "@/features/content/hooks/useContent";
import { useGenerationProgress } from "@/features/content/hooks/useGenerationProgress";

import {
  useCreationsInProgress,
  type Creation,
} from "../hooks/useCreationsInProgress";

/** The agent's work on one material, read only while the row is open. */
function Work({
  creation,
  planVersionId,
}: {
  creation: Creation;
  planVersionId: string;
}) {
  const { info, stopped } = creation;
  const generate = useGenerateContent(planVersionId, info.type);
  const progress = useGenerationProgress(
    planVersionId,
    info.type,
    creation.running,
    stopped,
  );
  const label = info.label.toLowerCase();
  return (
    <LiveWork
      events={progress}
      stopped={stopped}
      title={
        stopped
          ? `The agent could not finish the ${label}`
          : `The agent is writing the ${label}`
      }
      footer={
        stopped
          ? failureLine(generate.failure ?? "refused")
          : "It takes a few minutes. You can leave this page; the lesson page shows it when it is made."
      }
    />
  );
}

/**
 * What the agent is writing for this lesson, a row for each, one open at a time. A row that is
 * not open says only what it is and how it stands, so several at once stay short.
 */
export function CreationsInProgress({
  planVersionId,
}: {
  planVersionId: string | null;
}) {
  const creations = useCreationsInProgress(planVersionId);
  const [chosen, setChosen] = useState<string | null | undefined>(undefined);
  if (!planVersionId || creations.length === 0) return null;
  const open = chosen === undefined ? creations[0].info.type : chosen;

  return (
    <section aria-label="In progress" className="flex flex-col gap-2">
      <h3 className="text-[11px] font-semibold uppercase tracking-[0.12em] text-(--faint)">
        In progress
      </h3>
      <ul className="flex flex-col border border-(--line)">
        {creations.map((creation) => {
          const isOpen = open === creation.info.type;
          return (
            <li
              key={creation.info.type}
              className="border-t border-(--line) first:border-t-0"
            >
              <button
                type="button"
                aria-expanded={isOpen}
                onClick={() => setChosen(isOpen ? null : creation.info.type)}
                className="flex w-full items-center gap-3 px-3 py-2.5 text-left text-sm hover:bg-(--sunken)"
              >
                <span
                  aria-hidden="true"
                  className={`size-2 shrink-0 rounded-full ${creation.stopped ? "bg-(--danger)" : "animate-pulse bg-(--accent)"}`}
                />
                <span className="flex-1 font-semibold text-(--ink)">
                  {creation.info.label}
                </span>
                <span className="text-xs text-(--ink-2)">
                  {creation.stopped ? "Stopped" : "Writing"}
                </span>
              </button>
              {isOpen ? (
                <div className="px-3 pb-3">
                  <Work creation={creation} planVersionId={planVersionId} />
                </div>
              ) : null}
            </li>
          );
        })}
      </ul>
    </section>
  );
}
