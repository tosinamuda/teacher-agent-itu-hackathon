import type { FieldChange, PlanDiff } from "../lib/planDiff";
import { isUnchanged } from "../lib/planDiff";

const KIND_WORD = {
  added: "Added",
  removed: "Removed",
  changed: "Changed",
} as const;

function Change({ change }: { change: FieldChange }) {
  return (
    <div className="flex flex-col gap-1.5">
      <p className="text-[11px] font-semibold uppercase tracking-[0.12em] text-(--faint)">
        {change.label}
      </p>
      {change.before ? (
        <div className="bg-(--danger-tint) px-3 py-2">
          <p className="text-[11px] uppercase tracking-[0.12em] text-(--ink-2)">
            Before
          </p>
          <p className="whitespace-pre-wrap text-sm text-(--ink) line-through">
            {change.before}
          </p>
        </div>
      ) : null}
      {change.after ? (
        <div className="bg-(--success-tint) px-3 py-2">
          <p className="text-[11px] uppercase tracking-[0.12em] text-(--ink-2)">
            After
          </p>
          <p className="whitespace-pre-wrap text-sm text-(--ink)">
            {change.after}
          </p>
        </div>
      ) : null}
    </div>
  );
}

/** What differs between two versions of a plan: the plan's basis, then each step that changed. */
export function PlanDiffView({ diff }: { diff: PlanDiff }) {
  if (isUnchanged(diff)) {
    return (
      <p className="text-sm text-(--ink-2)">
        Nothing differs between these two versions.
      </p>
    );
  }
  return (
    <div className="flex flex-col gap-4">
      {diff.overall.length > 0 ? (
        <section className="flex flex-col gap-3 border border-(--line) bg-(--surface) p-4">
          <h4 className="text-sm font-semibold text-(--ink)">The plan</h4>
          {diff.overall.map((change) => (
            <Change key={change.label} change={change} />
          ))}
        </section>
      ) : null}
      {diff.steps.map((step) => (
        <section
          key={step.stepId}
          className="flex flex-col gap-3 border border-(--line) bg-(--surface) p-4"
        >
          <h4 className="text-sm font-semibold text-(--ink)">
            {step.title}{" "}
            <span className="font-normal text-(--ink-2)">
              · {KIND_WORD[step.kind]}
            </span>
          </h4>
          {step.changes.map((change) => (
            <Change key={change.label} change={change} />
          ))}
        </section>
      ))}
    </div>
  );
}
