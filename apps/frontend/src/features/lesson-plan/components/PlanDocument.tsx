import { useRef, useState } from "react";

import { SourceReferences } from "@/shared/components/references/SourceReferences";

import { useTypesetMath } from "../hooks/useTypesetMath";
import { PlanStepRow } from "./PlanStepRow";
import { timelineOf } from "../lib/planSummary";
import type { SessionPlanData } from "./SessionPlanView";

const OVERLINE =
  "text-[11px] font-semibold uppercase tracking-[0.12em] text-(--faint)";

function BasisRow({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div className="grid gap-1 sm:grid-cols-[180px_1fr] sm:gap-4">
      <dt className="text-xs text-(--ink-2)">{label}</dt>
      <dd className="text-sm text-(--ink)">{children}</dd>
    </div>
  );
}

/** What the lesson sets out to do, what it draws on, and its steps. */
export function PlanDocument({
  sessionPlan,
  changedStepIds,
  revisingStepId,
}: {
  sessionPlan: SessionPlanData;
  /** Steps the agent changed in the latest version. */
  changedStepIds?: ReadonlySet<string>;
  /** The step the agent is changing now. */
  revisingStepId?: string | null;
}) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [open, setOpen] = useState<ReadonlySet<string>>(
    () => new Set(sessionPlan.steps.slice(0, 1).map((step) => step.step_id)),
  );
  useTypesetMath(containerRef, sessionPlan);

  const objectives = (
    sessionPlan.lesson_plan_objectives?.length
      ? sessionPlan.lesson_plan_objectives
      : (sessionPlan.curriculum_objectives ?? [])
  ).map((objective) => objective.objective_text);
  const entry = sessionPlan.entry_behaviour ?? [];
  const materials = sessionPlan.instructional_materials ?? [];
  const references = sessionPlan.references ?? [];
  const shares = timelineOf(sessionPlan.steps);
  const allOpen = sessionPlan.steps.every((step) => open.has(step.step_id));
  const setStep = (stepId: string, isOpen: boolean) =>
    setOpen((current) => {
      const next = new Set(current);
      if (isOpen) next.add(stepId);
      else next.delete(stepId);
      return next;
    });
  const setAll = (isOpen: boolean) =>
    setOpen(
      isOpen
        ? new Set(sessionPlan.steps.map((step) => step.step_id))
        : new Set(),
    );

  return (
    <div
      ref={containerRef}
      id="lesson-plan-content"
      className="flex flex-col gap-6"
    >
      {objectives.length > 0 ? (
        <section aria-label="Objectives" className="flex flex-col gap-2">
          <h2 className={OVERLINE}>Objectives</h2>
          <ul className="flex flex-col gap-1">
            {objectives.map((text, at) => (
              <li key={at} className="flex gap-2 text-sm text-(--ink)">
                <span aria-hidden="true" className="text-(--ink-2)">
                  ▪
                </span>
                {text}
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      {entry.length || materials.length || references.length ? (
        <details
          aria-label="Basis for the plan"
          className="group border border-(--line) bg-(--surface)"
        >
          <summary className="flex cursor-pointer list-none items-center gap-3 px-4 py-3 [&::-webkit-details-marker]:hidden">
            <span className={OVERLINE}>Basis for the plan</span>
            <span className="min-w-0 flex-1 truncate text-xs text-(--ink-2)">
              {[
                entry.length ? "What students know" : null,
                materials.length ? "Materials" : null,
                references.length ? "Sources" : null,
              ]
                .filter(Boolean)
                .join(" · ")}
            </span>
            <svg
              viewBox="0 0 16 16"
              width="14"
              height="14"
              aria-hidden="true"
              className="shrink-0 text-(--ink-2) transition-transform group-open:rotate-90"
            >
              <path
                d="M6 3.5L10.5 8 6 12.5"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
              />
            </svg>
          </summary>
          <dl className="flex flex-col gap-2 border-t border-(--line) px-4 py-3">
            {entry.length ? (
              <BasisRow label="Students already know">
                {entry.join(", ")}
              </BasisRow>
            ) : null}
            {materials.length ? (
              <BasisRow label="Materials">{materials.join(", ")}</BasisRow>
            ) : null}
            {references.length ? (
              <BasisRow label="Sources">
                <SourceReferences references={references} />
              </BasisRow>
            ) : null}
          </dl>
        </details>
      ) : null}

      <section aria-label="Steps" className="flex flex-col gap-2">
        <header className="flex items-baseline justify-between gap-4">
          <h2 className={OVERLINE}>Steps</h2>
          <button
            type="button"
            onClick={() => setAll(!allOpen)}
            className="text-xs text-(--ink-2) underline hover:text-(--ink)"
          >
            {allOpen ? "Collapse all" : "Expand all"}
          </button>
        </header>
        <div className="border border-(--line) bg-(--surface)">
          {sessionPlan.steps.map((step, at) => (
            <PlanStepRow
              key={step.step_id}
              step={step}
              number={at + 1}
              share={shares[at]?.share ?? 0}
              open={open.has(step.step_id)}
              onToggle={(isOpen) => setStep(step.step_id, isOpen)}
              mark={
                step.step_id === revisingStepId
                  ? "revising"
                  : changedStepIds?.has(step.step_id)
                    ? "changed"
                    : undefined
              }
            />
          ))}
        </div>
      </section>
    </div>
  );
}
