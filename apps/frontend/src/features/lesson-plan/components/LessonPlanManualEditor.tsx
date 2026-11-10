import { useState } from "react";

import { Badge } from "@/shared/components/ui/Badge";
import { Button } from "@/shared/components/ui/Button";

import type { EditableSessionPlan } from "../api/manualEdit";
import { changeCount, editedStepIds } from "../lib/planEdits";

const boxClass =
  "border border-(--line-2) bg-(--surface) px-3 py-2 text-sm text-(--ink) outline-none focus:border-(--accent)";
const fieldClass = `w-full ${boxClass}`;
const sectionClass = "space-y-3 border-t border-(--line) pt-5";
const labelClass =
  "text-[11px] font-semibold uppercase tracking-[0.14em] text-(--muted)";

type Activity = {
  who: "teacher" | "student";
  what: string;
  [key: string]: unknown;
};

type Step = {
  step_id: string;
  title: string;
  content: string;
  estimated_minutes?: number | null;
  activities?: Activity[];
  [key: string]: unknown;
};

type Objective = {
  lesson_objective_id: string;
  objective_text: string;
  [key: string]: unknown;
};

/**
 * Manual editor for the *text* of a lesson plan: objectives, entry behaviour, instructional
 * materials, references, and for each step its title, minutes, what the teacher and the students
 * do, and its content. Deliberately does NOT expose the structured blocks (worked examples,
 * practice, KC types): they carry strict cross-field validators, so steering them is left to the
 * agent. Curriculum objectives stay read-only (curriculum-bound).
 *
 * Holds a local draft; Save hands the full edited plan back to the parent, which persists it as
 * a new version.
 */
export function LessonPlanManualEditor({
  sessionPlan,
  onSave,
  onCancel,
  isSaving,
  error,
}: {
  sessionPlan: EditableSessionPlan;
  onSave: (next: EditableSessionPlan) => void;
  onCancel: () => void;
  isSaving: boolean;
  error?: string | null;
}) {
  const [draft, setDraft] = useState<EditableSessionPlan>(() =>
    structuredClone(sessionPlan),
  );

  const objectives = (draft.lesson_plan_objectives ?? []) as Objective[];
  const steps = (draft.steps ?? []) as unknown as Step[];
  const changes = changeCount(sessionPlan, draft);
  const edited = new Set(editedStepIds(sessionPlan, draft));

  const patch = (next: Partial<EditableSessionPlan>) =>
    setDraft((current) => ({ ...current, ...next }));

  const setObjectiveText = (index: number, text: string) => {
    const updated = objectives.map((objective, i) =>
      i === index ? { ...objective, objective_text: text } : objective,
    );
    patch({ lesson_plan_objectives: updated } as Partial<EditableSessionPlan>);
  };

  const setStep = (index: number, change: Partial<Step>) => {
    const updated = steps.map((step, i) =>
      i === index ? { ...step, ...change } : step,
    );
    patch({ steps: updated } as unknown as Partial<EditableSessionPlan>);
  };

  const setActivity = (
    stepIndex: number,
    activityIndex: number,
    what: string,
  ) => {
    const step = steps[stepIndex];
    setStep(stepIndex, {
      activities: (step.activities ?? []).map((activity, i) =>
        i === activityIndex ? { ...activity, what } : activity,
      ),
    });
  };

  return (
    <div className="space-y-6">
      <p className="bg-(--info-tint) px-4 py-3 text-sm text-(--info-ink)">
        Editing. Saving makes a new version.
      </p>

      <section className="space-y-3">
        <p className={labelClass}>Objectives</p>
        {objectives.length === 0 ? (
          <p className="text-xs italic text-(--muted)">No objectives.</p>
        ) : (
          objectives.map((objective, index) => (
            <textarea
              key={objective.lesson_objective_id}
              rows={2}
              aria-label={`Objective ${index + 1}`}
              className={fieldClass}
              value={objective.objective_text}
              onChange={(event) => setObjectiveText(index, event.target.value)}
            />
          ))
        )}
      </section>

      <section className={sectionClass}>
        <p className={labelClass}>Steps</p>
        <div className="space-y-4">
          {steps.map((step, index) => (
            <StepEditor
              key={step.step_id}
              step={step}
              number={index + 1}
              edited={edited.has(step.step_id)}
              onChange={(change) => setStep(index, change)}
              onActivity={(activityIndex, what) =>
                setActivity(index, activityIndex, what)
              }
            />
          ))}
        </div>
      </section>

      <StringListEditor
        label="Entry behaviour"
        items={draft.entry_behaviour ?? []}
        onChange={(items) => patch({ entry_behaviour: items })}
      />
      <StringListEditor
        label="Instructional materials"
        items={draft.instructional_materials ?? []}
        onChange={(items) => patch({ instructional_materials: items })}
      />
      <StringListEditor
        label="References"
        items={draft.references ?? []}
        onChange={(items) => patch({ references: items })}
      />

      {error ? <p className="text-sm text-(--danger-ink)">{error}</p> : null}

      <div className="sticky bottom-0 flex items-center gap-3 border border-(--line-2) bg-(--surface) px-4 py-3">
        <p className="flex-1 text-sm text-(--ink)">
          {changes === 0
            ? "No changes"
            : `${changes} ${changes === 1 ? "change" : "changes"}`}
        </p>
        <button
          type="button"
          onClick={onCancel}
          className="text-sm text-(--ink-2) underline-offset-2 hover:text-(--ink) hover:underline"
        >
          Cancel
        </button>
        <Button
          isLoading={isSaving}
          disabled={changes === 0}
          onClick={() => onSave(draft)}
        >
          Save edits
        </Button>
      </div>
    </div>
  );
}

/** One step as fields: its title and minutes, what the teacher and the students do, its content. */
function StepEditor({
  step,
  number,
  edited,
  onChange,
  onActivity,
}: {
  step: Step;
  number: number;
  edited: boolean;
  onChange: (change: Partial<Step>) => void;
  onActivity: (activityIndex: number, what: string) => void;
}) {
  const activities = step.activities ?? [];
  const column = (who: Activity["who"], title: string) => {
    const mine = activities
      .map((activity, index) => ({ activity, index }))
      .filter(({ activity }) => activity.who === who);
    if (mine.length === 0) return null;
    return (
      <div className="flex flex-col gap-2">
        <p className={labelClass}>{title}</p>
        {mine.map(({ activity, index }) => (
          <textarea
            key={index}
            rows={2}
            aria-label={`${title}, ${index + 1}`}
            className={fieldClass}
            value={activity.what}
            onChange={(event) => onActivity(index, event.target.value)}
          />
        ))}
      </div>
    );
  };
  return (
    <div className="space-y-3 border border-(--line-2) p-3">
      <div className="flex items-center gap-2">
        <span className="text-xs text-(--faint)">{number}</span>
        <input
          className={`min-w-0 flex-1 ${boxClass}`}
          aria-label={`Step ${number} title`}
          value={step.title}
          onChange={(event) => onChange({ title: event.target.value })}
          placeholder="Step title"
        />
        <input
          type="number"
          min={1}
          className={`w-20 shrink-0 ${boxClass}`}
          aria-label={`Step ${number} minutes`}
          value={step.estimated_minutes ?? ""}
          onChange={(event) =>
            onChange({
              estimated_minutes: event.target.value
                ? Number(event.target.value)
                : null,
            })
          }
        />
        {edited ? <Badge variant="outline">Edited</Badge> : null}
      </div>
      {activities.length > 0 ? (
        <div className="grid gap-3 sm:grid-cols-2">
          {column("teacher", "Teacher does")}
          {column("student", "Students do")}
        </div>
      ) : null}
      <details>
        <summary className="cursor-pointer text-xs text-(--ink-2)">
          Lesson content for this step
        </summary>
        <textarea
          rows={3}
          aria-label={`Step ${number} content`}
          className={`${fieldClass} mt-2`}
          value={step.content ?? ""}
          onChange={(event) => onChange({ content: event.target.value })}
        />
      </details>
    </div>
  );
}

/** Edit a list of free-text strings: per-row edit + remove, plus an add field. */
function StringListEditor({
  label,
  items,
  onChange,
}: {
  label: string;
  items: string[];
  onChange: (items: string[]) => void;
}) {
  const [draftNew, setDraftNew] = useState("");
  return (
    <section className={sectionClass}>
      <p className={labelClass}>{label}</p>
      {items.map((item, index) => (
        <div key={index} className="flex items-center gap-2">
          <input
            className={fieldClass}
            value={item}
            onChange={(event) =>
              onChange(
                items.map((value, i) =>
                  i === index ? event.target.value : value,
                ),
              )
            }
          />
          <button
            type="button"
            onClick={() => onChange(items.filter((_, i) => i !== index))}
            className="shrink-0 text-xs text-(--muted) hover:text-(--danger)"
          >
            remove
          </button>
        </div>
      ))}
      <div className="flex items-center gap-2">
        <input
          className={fieldClass}
          value={draftNew}
          placeholder={`Add ${label.toLowerCase()}…`}
          onChange={(event) => setDraftNew(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && draftNew.trim()) {
              onChange([...items, draftNew.trim()]);
              setDraftNew("");
            }
          }}
        />
        <button
          type="button"
          onClick={() => {
            if (!draftNew.trim()) return;
            onChange([...items, draftNew.trim()]);
            setDraftNew("");
          }}
          className="shrink-0 text-xs font-semibold text-(--accent-deep) hover:underline"
        >
          add
        </button>
      </div>
    </section>
  );
}
