import { useState } from "react";

import type {
  LessonStepStructured,
  StepActivity,
} from "@/shared/types/lesson-schema";

import { Pager } from "@/shared/components/renderer/Pager";

import { LessonNoteManifest } from "../types";
import { NoteText } from "./NoteText";

type NoteLayout = "prepared" | "class";

const WHO: Record<StepActivity["who"], string> = {
  teacher: "Teacher",
  student: "Students",
};

/** What happens in the step, in the teacher's words: the plan's activities, in order. */
function StepProse({ step }: { step: LessonStepStructured }) {
  if (!step.activities?.length) return null;
  return (
    <ul className="space-y-1 border-l-2 border-(--line) pl-3 text-sm italic text-(--ink-2)">
      {step.activities.map((activity, index) => (
        <li key={index}>
          <span className="font-semibold not-italic">
            {WHO[activity.who]}:{" "}
          </span>
          <NoteText text={activity.what} />
        </li>
      ))}
    </ul>
  );
}

function LayoutSwitch({
  layout,
  onChange,
}: {
  layout: NoteLayout;
  onChange: (next: NoteLayout) => void;
}) {
  const options: [NoteLayout, string][] = [
    ["prepared", "As prepared"],
    ["class", "As used in class"],
  ];
  return (
    <div
      className="inline-flex rounded-full border border-(--line) p-0.5"
      role="group"
      aria-label="Note layout"
    >
      {options.map(([value, label]) => (
        <button
          key={value}
          type="button"
          aria-pressed={layout === value}
          onClick={() => onChange(value)}
          className={`rounded-full px-3 py-1 text-xs font-semibold ${
            layout === value
              ? "bg-(--accent-deep) text-(--surface)"
              : "text-(--muted)"
          }`}
        >
          {label}
        </button>
      ))}
    </div>
  );
}

/**
 * The lesson note, one section per lesson step, in plan order.
 *
 * Given the plan's steps, it shows the note as the teacher prepares it — what the teacher and
 * the students do in each step, above the content — or as it is used in class, the content
 * alone. The note holds only the content; the teacher's prose is the plan's activities.
 */
export function LessonNoteView({
  manifest,
  steps,
  paged = false,
}: {
  manifest: LessonNoteManifest;
  steps?: LessonStepStructured[];
  /** One step at a time, filling the height it is given, for the teacher's review page. */
  paged?: boolean;
}) {
  const [layout, setLayout] = useState<NoteLayout>("prepared");
  const byId = new Map((steps ?? []).map((step) => [step.step_id, step]));
  const prepared = Boolean(steps) && layout === "prepared";
  if (paged) {
    return (
      <div className="flex min-h-0 flex-1 flex-col gap-3">
        {steps && (
          <div className="shrink-0">
            <LayoutSwitch layout={layout} onChange={setLayout} />
          </div>
        )}
        <Pager count={manifest.sections.length} label="Step">
          {(index) => {
            const section = manifest.sections[index];
            const step = byId.get(section.step_id);
            return (
              <article className="flex min-h-0 flex-1 flex-col rounded-2xl border border-(--line) bg-white p-4">
                <p className="shrink-0 text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent-deep)">
                  Step {index + 1}
                  {step?.title ? ` · ${step.title}` : ""}
                </p>
                <div className="relative mt-3 max-h-[70dvh] space-y-3 overflow-y-auto overscroll-contain pr-2 md:max-h-none md:min-h-0 md:flex-1">
                  {prepared && step && <StepProse step={step} />}
                  <NoteText text={section.body} />
                </div>
              </article>
            );
          }}
        </Pager>
      </div>
    );
  }
  return (
    <div className="space-y-3">
      {steps && <LayoutSwitch layout={layout} onChange={setLayout} />}
      <ol className="space-y-5">
        {manifest.sections.map((section, index) => {
          const step = byId.get(section.step_id);
          return (
            <li
              key={section.step_id}
              className="space-y-3 rounded-2xl border border-(--line) bg-(--surface) p-5"
            >
              <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent-deep)">
                Step {index + 1}
                {step?.title ? ` · ${step.title}` : ""}
              </p>
              {prepared && step && <StepProse step={step} />}
              <NoteText text={section.body} />
            </li>
          );
        })}
      </ol>
    </div>
  );
}
