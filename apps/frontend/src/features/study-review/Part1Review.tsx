import { Section } from "@/shared/components/ui/Section";
import { useLessonNote } from "@/features/content/hooks/useLessonNote";
import { JourneyPack } from "@/features/experiments/components/JourneyPack";
import { usePlanVersion } from "@/features/lesson-plan/hooks/usePlanVersion";
import {
  InstrumentDetails,
  ObjectiveScores,
  RaterSets,
  raterNames,
} from "@/features/study-ratings/RatingParts";
import { useStudyInstrument, useStudyRatings } from "@/features/study-ratings/useStudyRatings";

import { ObjectiveTaught } from "./ObjectiveTaught";
import { lessonObjectives, sectionsFor } from "./objectives";
import { Subhead } from "./Subhead";
import { usePackManifest } from "./usePackManifest";

/**
 * A Part 1 revision note as its raters met it: objective by objective, what the teacher taught
 * beside the part of the note that addresses it, then every rater's scores for that objective.
 * There was no overall score for the whole note.
 */
export function Part1Review({ planVersionId, noteId }: { planVersionId: string; noteId: string }) {
  const plan = usePlanVersion(planVersionId);
  const note = useLessonNote(planVersionId);
  const manifest = usePackManifest(noteId);
  const ratings = useStudyRatings(noteId);
  const instrument = useStudyInstrument();

  if (
    plan.isLoading ||
    note.isLoading ||
    manifest.isLoading ||
    ratings.isLoading ||
    instrument.isLoading
  ) {
    return <p className="text-sm text-(--muted)">Loading…</p>;
  }
  if (!plan.data || !manifest.data || !ratings.data || !instrument.data) {
    return (
      <p className="text-sm text-(--danger-ink)">Couldn&apos;t load this note and its ratings.</p>
    );
  }
  const objectives = lessonObjectives(plan.data.session_plan);
  const criteria = instrument.data.part_1;
  const names = raterNames(ratings.data.documents);
  return (
    <div className="space-y-10">
      <Section title="Rated by">
        <RaterSets documents={ratings.data.documents} />
        <InstrumentDetails criteria={criteria} instrument={instrument.data} comparative={false} />
      </Section>
      {objectives.map((objective, index) => (
        <Section key={objective.id} title={`${index + 1}. ${objective.text}`}>
          <div className="grid gap-6 lg:grid-cols-2">
            <div className="min-w-0 space-y-2">
              <Subhead>Taught in the lesson</Subhead>
              <ObjectiveTaught objective={objective} note={note.manifest} />
            </div>
            <div className="min-w-0 space-y-2">
              <Subhead>Revision note</Subhead>
              <JourneyPack
                manifest={{ ...manifest.data, steps: sectionsFor(manifest.data, objective.id) }}
              />
            </div>
          </div>
          <div className="space-y-2 pt-2">
            <Subhead>Scores</Subhead>
            <ObjectiveScores
              scores={ratings.data.scores.filter((s) => s.lesson_objective_id === objective.id)}
              criteria={criteria}
              names={names}
            />
          </div>
        </Section>
      ))}
      <details className="text-sm">
        <summary className="cursor-pointer text-(--muted) hover:text-(--ink)">
          The whole revision note, straight through
        </summary>
        <div className="mt-3">
          <JourneyPack manifest={manifest.data} />
        </div>
      </details>
    </div>
  );
}
