import { Link } from "@/shared/router";

import { ExperimentSummary } from "../lib/experiments";
import { buildLessonPrepSteps, LessonPrepStatus, StudentNoteProgress } from "../services/lessonPrep";

const STATUS_STYLE: Record<LessonPrepStatus, { ring: string; label: string; labelClass: string }> = {
  done: { ring: "border-(--success-ink) bg-(--success-tint) text-(--success-ink)", label: "Done", labelClass: "text-(--success-ink)" },
  current: { ring: "border-(--accent) bg-(--accent-soft) text-(--accent-deep)", label: "Now", labelClass: "text-(--accent-deep)" },
  auto: { ring: "border-(--line) bg-(--surface) text-(--muted)", label: "Preparing…", labelClass: "text-(--muted)" },
  upcoming: { ring: "border-(--line) bg-(--surface) text-(--faint)", label: "Later", labelClass: "text-(--faint)" },
};

/**
 * Read-only map of the teacher's lesson-preparation workflow for one lesson:
 * the ordered steps (plan → revision note → assessment → students) and where each
 * one currently stands. The research conditions run in the background and are
 * never shown here. Actions for the active step live in the cards below this.
 *
 * `studentNotes` counts this lesson's students with a note of their own and those awaiting
 * the teacher's approval — it drives the two per-student steps.
 */
export function LessonPrepChecklist({
  experiment,
  studentNotes = { made: 0, awaiting: 0 },
  assessment = { ready: false, sent: false },
}: {
  experiment: ExperimentSummary;
  studentNotes?: StudentNoteProgress;
  assessment?: { ready: boolean; sent: boolean };
}) {
  const steps = buildLessonPrepSteps(experiment, studentNotes, assessment);

  return (
    <ol className="space-y-3">
      {steps.map((step, index) => {
        const style = STATUS_STYLE[step.status];
        return (
          <li key={step.title} className="flex gap-3">
            <span
              className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-full border text-xs font-semibold ${style.ring}`}
            >
              {step.status === "done" ? "✓" : index + 1}
            </span>
            <div className="flex-1 border-b border-(--line)/60 pb-3">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <p className="text-sm font-semibold text-(--ink)">{step.title}</p>
                <span className={`text-[11px] font-semibold uppercase tracking-wide ${style.labelClass}`}>
                  {style.label}
                </span>
              </div>
              <p className="mt-0.5 text-xs text-(--muted)">{step.detail}</p>
              {step.href ? (
                <Link
                  href={step.href}
                  className="mt-1 inline-block text-xs font-semibold text-(--accent-deep) hover:underline"
                >
                  Open this step →
                </Link>
              ) : null}
            </div>
          </li>
        );
      })}
    </ol>
  );
}
