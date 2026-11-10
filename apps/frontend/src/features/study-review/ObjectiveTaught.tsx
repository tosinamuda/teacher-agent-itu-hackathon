import { NoteText } from "@/features/content/components/NoteText";
import type { LessonNoteManifest } from "@/features/content/types";

import { LessonObjective } from "./objectives";

/**
 * What the teacher taught for one objective, as the rating documents set it out: the curriculum
 * target, the step that taught it and what happened in it, the teacher's note for that step,
 * and the evaluation questions the teacher set on it.
 */
export function ObjectiveTaught({
  objective,
  note,
}: {
  objective: LessonObjective;
  note: LessonNoteManifest | undefined;
}) {
  const bodies = new Map((note?.sections ?? []).map((section) => [section.step_id, section.body]));
  return (
    <div className="space-y-3 text-sm">
      {objective.curriculumTarget ? (
        <p className="text-(--ink-2)">
          <span className="text-(--muted)">Curriculum target:</span> {objective.curriculumTarget}
        </p>
      ) : null}
      {objective.steps.map((step) => (
        <div key={step.step_id} className="space-y-2">
          <p className="text-(--ink)">
            <span className="font-medium">{step.title}.</span> {step.content}
          </p>
          {step.activities?.length ? (
            <ul className="list-disc pl-5 text-(--ink-2)">
              {step.activities.map((activity) => (
                <li key={`${activity.who}-${activity.what}`}>
                  The {activity.who} {activity.what}
                </li>
              ))}
            </ul>
          ) : null}
          {bodies.get(step.step_id) ? (
            <div className="space-y-1 border-l-2 border-(--line) pl-3">
              <p className="text-xs text-(--muted)">The teacher&apos;s note</p>
              <NoteText text={bodies.get(step.step_id) as string} />
            </div>
          ) : null}
        </div>
      ))}
      {objective.questions.length ? (
        <div className="space-y-1">
          <p className="text-xs text-(--muted)">The teacher&apos;s evaluation questions</p>
          <ol className="list-decimal pl-5">
            {objective.questions.map((question) => (
              <li key={question.id}>
                <NoteText text={question.question} />
              </li>
            ))}
          </ol>
        </div>
      ) : null}
    </div>
  );
}
