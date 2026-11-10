import { Section } from "@/shared/components/ui/Section";
import { useLessonNote } from "@/features/content/hooks/useLessonNote";
import { JourneyPack } from "@/features/experiments/components/JourneyPack";
import type { ComparePackManifest } from "@/features/experiments/lib/experiments";
import type { ObjectiveStateRow } from "@/features/experiments/lib/learnerState";
import { usePlanVersion } from "@/features/lesson-plan/hooks/usePlanVersion";
import { ClassworkAnswers } from "@/features/study-classwork/ClassworkAnswers";
import type { LearnerClasswork } from "@/features/study-classwork/types";
import { useLearnerClasswork } from "@/features/study-classwork/useLearnerClasswork";
import {
  InstrumentDetails,
  ObjectiveJudgements,
  RaterSets,
  raterNames,
} from "@/features/study-ratings/RatingParts";
import { useStudyInstrument, useStudyRatings } from "@/features/study-ratings/useStudyRatings";

import { ObjectiveTaught } from "./ObjectiveTaught";
import { comparedObjectives, lessonObjectives, sectionsFor, LessonObjective } from "./objectives";
import { Subhead } from "./Subhead";
import { usePackManifest } from "./usePackManifest";

const capitalised = (text: string | null | undefined) =>
  text ? `${text[0].toUpperCase()}${text.slice(1)}` : null;

/** The learner's two notes for one objective, side by side as the raters compared them. */
function TwoNotes({
  objective,
  p0,
  p1,
}: {
  objective: LessonObjective;
  p0: ComparePackManifest;
  p1: ComparePackManifest;
}) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <div className="min-w-0 space-y-2">
        <Subhead>P0 · the class note</Subhead>
        <JourneyPack manifest={{ ...p0, steps: sectionsFor(p0, objective.id) }} />
      </div>
      <div className="min-w-0 space-y-2">
        <Subhead>P1 · personalised to this learner</Subhead>
        <JourneyPack manifest={{ ...p1, steps: sectionsFor(p1, objective.id) }} />
      </div>
    </div>
  );
}

/** The learner's class work on one objective, folded to a line until it is wanted. */
function Classwork({
  classwork,
  objectiveId,
}: {
  classwork: LearnerClasswork;
  objectiveId: string;
}) {
  const questions = classwork.questions.filter((q) => q.lesson_objective_id === objectiveId).length;
  return (
    <details className="text-sm">
      <summary className="cursor-pointer text-(--muted) hover:text-(--ink)">
        The learner&apos;s class work · {questions} {questions === 1 ? "question" : "questions"}
      </summary>
      <div className="mt-3">
        <ClassworkAnswers classwork={classwork} objectiveId={objectiveId} />
      </div>
    </details>
  );
}

/**
 * A Part 2 comparison as its raters met it. Only the objectives the learner has marked class work
 * for were compared; each is taken in turn with what the teacher taught, the learner's class
 * work on it, the two notes side by side, and every rater's judgement. The objectives without
 * class work follow, folded, for context.
 */
export function Part2Review({
  planVersionId,
  learnerId,
  p0Id,
  p1Id,
  states,
}: {
  planVersionId: string;
  learnerId: string;
  p0Id: string;
  p1Id: string;
  states: ObjectiveStateRow[];
}) {
  const plan = usePlanVersion(planVersionId);
  const note = useLessonNote(planVersionId);
  const classwork = useLearnerClasswork(planVersionId, learnerId);
  const p0 = usePackManifest(p0Id);
  const p1 = usePackManifest(p1Id);
  const ratings = useStudyRatings(p1Id);
  const instrument = useStudyInstrument();
  const loading = [plan, classwork, p0, p1, ratings, instrument].some((query) => query.isLoading);
  if (loading || note.isLoading) return <p className="text-sm text-(--muted)">Loading…</p>;
  if (!plan.data || !classwork.data || !p0.data || !p1.data || !ratings.data || !instrument.data) {
    return <p className="text-sm text-(--danger-ink)">Couldn&apos;t load this comparison.</p>;
  }
  const objectives = lessonObjectives(plan.data.session_plan);
  const compared = comparedObjectives(objectives, classwork.data);
  const comparedList = objectives.filter((objective) => compared.has(objective.id));
  const others = objectives.filter((objective) => !compared.has(objective.id));
  const band = new Map(states.map((state) => [state.objectiveId, state]));
  const criteria = instrument.data.part_2;
  const names = raterNames(ratings.data.documents);
  return (
    <div className="space-y-10">
      <Section
        title="Rated by"
        aside={`Compared on ${comparedList.length} of ${objectives.length} objectives, those with marked class work`}
      >
        <RaterSets documents={ratings.data.documents} />
        <InstrumentDetails criteria={criteria} instrument={instrument.data} comparative />
      </Section>
      {comparedList.map((objective, index) => {
        const state = band.get(objective.id);
        return (
          <Section
            key={objective.id}
            title={`${index + 1}. ${objective.text}`}
            aside={[capitalised(state?.band), state?.mastery].filter(Boolean).join(" · ") || null}
          >
            <div className="grid gap-6 lg:grid-cols-2">
              <div className="min-w-0 space-y-2">
                <Subhead>Taught in the lesson</Subhead>
                <ObjectiveTaught objective={objective} note={note.manifest} />
              </div>
              <div className="min-w-0 space-y-2">
                <Subhead>Class work</Subhead>
                {state?.misconception ? (
                  <p className="text-sm text-(--ink-2)">{state.misconception}</p>
                ) : null}
                <Classwork classwork={classwork.data} objectiveId={objective.id} />
              </div>
            </div>
            <div className="pt-2">
              <TwoNotes objective={objective} p0={p0.data} p1={p1.data} />
            </div>
            <div className="space-y-2 pt-2">
              <Subhead>Comparison</Subhead>
              <ObjectiveJudgements
                judgements={ratings.data.judgements.filter(
                  (j) => j.lesson_objective_id === objective.id,
                )}
                criteria={criteria}
                names={names}
              />
            </div>
          </Section>
        );
      })}
      {others.length ? (
        <Section title="Not compared" aside="No marked class work">
          <div className="space-y-2">
            {others.map((objective) => (
              <details key={objective.id} className="text-sm">
                <summary className="cursor-pointer text-(--ink) hover:text-(--accent-deep)">
                  {objective.text}
                </summary>
                <div className="mt-3">
                  <TwoNotes objective={objective} p0={p0.data} p1={p1.data} />
                </div>
              </details>
            ))}
          </div>
        </Section>
      ) : null}
    </div>
  );
}
