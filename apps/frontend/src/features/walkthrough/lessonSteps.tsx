import { useState } from "react";

import { Choices } from "@/shared/components/ui/Choices";
import { SectionCompare } from "@/features/experiments/components/SectionCompare";
import { LearnerStateTable } from "@/features/experiments/components/LearnerStateTable";
import { StoryLessonPlan } from "@/features/experiments/components/StoryLessonPlan";
import { useExperimentStory } from "@/features/experiments/hooks/useExperimentStory";
import { objectiveStates } from "@/features/experiments/lib/learnerState";
import { ConcludedRaters } from "@/features/rater-assignments/components/ConcludedRaters";
import { useExperimentAssignments } from "@/features/rater-assignments/hooks/useRaterAssignments";
import { Part1Review } from "@/features/study-review/Part1Review";
import { Part2Review } from "@/features/study-review/Part2Review";
import { usePackManifest } from "@/features/study-review/usePackManifest";

import { LessonRecord, useLessonObjectives } from "./useLessonRecord";

const Waiting = () => <p className="text-sm text-(--muted)">Loading…</p>;

/** The lesson as the teacher set it up: where it sits in the scheme of work, and the plan. */
export function LessonStep({ experimentId }: { experimentId: string }) {
  const story = useExperimentStory(experimentId).data;
  if (!story) return <Waiting />;
  const curriculum = story.curriculum;
  const place = [
    curriculum?.subject,
    curriculum?.grade,
    curriculum?.term,
    curriculum?.week != null ? `Week ${curriculum.week}` : null,
  ].filter(Boolean);
  return (
    <div className="space-y-6">
      <div className="space-y-1 text-sm">
        <p className="text-(--muted)">{place.join(" · ")}</p>
        <p className="text-(--ink)">
          <span className="text-(--muted)">{curriculum?.topic} › </span>
          <span className="font-medium">{curriculum?.subtopic}</span>
        </p>
      </div>
      <StoryLessonPlan plan={story.lesson_plan} />
    </div>
  );
}

/** An ungrounded or partly grounded note beside the fully grounded C3, for the chosen draw. */
export function GroundingStep({ record, draw }: { record: LessonRecord; draw: number }) {
  const others: string[] = record.conditions.filter((condition) => condition !== "C3");
  const [left, setLeft] = useState<string>(others[0] ?? "C0");
  const leftNote = usePackManifest(record.noteOf(left, draw)).data;
  const c3 = usePackManifest(record.noteOf("C3", draw)).data;
  if (!leftNote || !c3) return <Waiting />;
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3 text-sm">
        <Choices
          options={others.map((condition) => ({ value: condition, label: condition }))}
          value={left}
          onChange={setLeft}
        />
        <span className="text-(--muted)">beside C3</span>
      </div>
      <SectionCompare
        leftLabel={`${left} · draw ${draw}`}
        rightLabel={`C3 · draw ${draw}`}
        left={leftNote}
        right={c3}
        onSurface
      />
    </div>
  );
}

/** The C3 note of the chosen draw as its raters met it, objective by objective. */
export function RatedNoteStep({ record, draw }: { record: LessonRecord; draw: number }) {
  const noteId = record.noteOf("C3", draw);
  const planVersionId = record.experiment?.plan_version_id;
  if (!noteId || !planVersionId) return <Waiting />;
  return <Part1Review planVersionId={planVersionId} noteId={noteId} />;
}

/** The chosen learner's band on each objective, read from their marked class work. */
export function LearnerStep({ record, learnerId }: { record: LessonRecord; learnerId: string }) {
  const objectives = useLessonObjectives(record.experiment?.experiment_id);
  const focalCase = record.learners.find((learner) => learner.learner_id === learnerId);
  if (!objectives) return <Waiting />;
  return (
    <LearnerStateTable
      states={objectiveStates(focalCase?.learner_state_snapshot)}
      objectives={objectives}
    />
  );
}

/** The chosen learner's P0 and P1 as the raters compared them, and their judgements. */
export function ComparedStep({ record, learnerId }: { record: LessonRecord; learnerId: string }) {
  const planVersionId = record.experiment?.plan_version_id;
  const p0 = record.learnerNote(learnerId, "P0");
  const p1 = record.learnerNote(learnerId, "P1");
  const focalCase = record.learners.find((learner) => learner.learner_id === learnerId);
  if (!planVersionId || !p0 || !p1) return <Waiting />;
  return (
    <Part2Review
      planVersionId={planVersionId}
      learnerId={learnerId}
      p0Id={p0}
      p1Id={p1}
      states={objectiveStates(focalCase?.learner_state_snapshot)}
    />
  );
}

/** Who rated the lesson, set by set, and the order each learner's two notes were shown in. */
export function RatersStep({ record }: { record: LessonRecord }) {
  const view = useExperimentAssignments(record.experiment?.experiment_id ?? "").data;
  if (!record.experiment || !view) return <Waiting />;
  return (
    <div className="space-y-10">
      <ConcludedRaters experiment={record.experiment} view={view} />
    </div>
  );
}
