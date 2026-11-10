import { ReactNode } from "react";

import { EvaluationObjective, EvaluationReferenceSheet } from "../types";

/**
 * Renders a compact label/value row for lesson or learner reference details.
 */
export function ContextRow({ label, value }: { label: string; value?: string | null }) {
  return (
    <div className="rounded-none border border-[color:var(--line)] bg-white px-4 py-3">
      <dt className="text-[11px] font-semibold uppercase tracking-[0.16em] text-[color:var(--muted)]">
        {label}
      </dt>
      <dd className="mt-1 text-sm text-[color:var(--ink)]">{value ?? "Not provided"}</dd>
    </div>
  );
}

/** Renders ordered lesson objectives in a compact stacked list. */
export function ObjectivesPanel({ objectives }: { objectives: EvaluationObjective[] }) {
  return (
    <ol className="space-y-2">
      {objectives.map((objective, index) => (
        <li
          key={objective.lesson_objective_id}
          className="rounded-none border border-[color:var(--line)] bg-white px-4 py-3 text-sm text-[color:var(--muted)]"
        >
          <span className="mr-2 font-semibold text-[color:var(--ink)]">{index + 1}.</span>
          {objective.objective_text ?? objective.lesson_objective_id}
        </li>
      ))}
    </ol>
  );
}

/** Wraps drawer sections in a shared visual treatment. */
export function DrawerSection({
  title,
  children,
}: {
  title: string;
  children: ReactNode;
}) {
  return (
    <section className="space-y-3 rounded-none border border-[color:var(--line)] bg-[color:var(--panel)] px-4 py-4">
      <p className="text-sm font-semibold text-[color:var(--ink)]">{title}</p>
      <div className="space-y-3">{children}</div>
    </section>
  );
}

/** Renders the full lesson reference sheet inside the packet drawer. */
export function ReferenceSheetContent({
  referenceSheet,
}: {
  referenceSheet: EvaluationReferenceSheet;
}) {
  return (
    <div className="space-y-4 text-sm text-[color:var(--muted)]">
      <dl className="grid gap-3 sm:grid-cols-2">
        <ContextRow label="Subject" value={referenceSheet.subject} />
        <ContextRow label="Class" value={referenceSheet.grade} />
        <ContextRow label="Term" value={referenceSheet.term} />
        <ContextRow label="Topic" value={referenceSheet.topic} />
        <ContextRow label="Subtopic" value={referenceSheet.subtopic} />
        <ContextRow label="Theme" value={referenceSheet.theme} />
      </dl>

      <ListBlock label="Curriculum objectives" items={referenceSheet.curriculum_objectives} />
      <ListBlock label="Previous knowledge" items={referenceSheet.entry_behaviour ?? []} />
      <ListBlock label="Lesson sequence" items={referenceSheet.lesson_sequence} />
      <ListBlock label="Instructional materials" items={referenceSheet.instructional_materials} />
      <ListBlock label="Evaluation" items={referenceSheet.evaluation ?? []} />
    </div>
  );
}

function ListBlock({ label, items }: { label: string; items: string[] }) {
  return (
    <div className="space-y-2">
      <p className="text-sm font-semibold text-[color:var(--ink)]">{label}</p>
      {items.length ? (
        <ul className="space-y-2">
          {items.map((item) => (
            <li
              key={item}
              className="rounded-none border border-[color:var(--line)] bg-white px-4 py-3 text-sm text-[color:var(--muted)]"
            >
              {item}
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-sm text-[color:var(--muted)]">No {label.toLowerCase()} recorded.</p>
      )}
    </div>
  );
}
