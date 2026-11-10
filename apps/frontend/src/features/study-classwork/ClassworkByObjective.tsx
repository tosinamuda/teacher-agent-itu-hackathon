import { ClassworkAnswers } from "./ClassworkAnswers";
import { LearnerClasswork } from "./types";

/** A learner's class work, objective by objective, with the teacher's total. */
export function ClassworkByObjective({
  classwork,
  objectives,
}: {
  classwork: LearnerClasswork;
  objectives: { id: string; text: string }[];
}) {
  const asked = new Set(classwork.questions.map((question) => question.lesson_objective_id));
  const covered = objectives.filter((objective) => asked.has(objective.id));
  return (
    <div className="space-y-6">
      {classwork.script ? (
        <p className="text-sm text-(--ink-2)">
          Teacher&apos;s total: {classwork.script.teacher_total}
        </p>
      ) : (
        <p className="text-sm text-(--muted)">This learner&apos;s script was not captured.</p>
      )}
      {covered.map((objective) => (
        <section key={objective.id} className="space-y-3">
          <h3 className="font-medium text-(--ink)">{objective.text}</h3>
          <ClassworkAnswers classwork={classwork} objectiveId={objective.id} />
        </section>
      ))}
    </div>
  );
}
