import type { ExperimentDetail } from "@/features/experiments/lib/experiments";
import { useStudyRaterSchedule } from "@/features/study-ratings/useStudyRatings";
import { Section } from "@/shared/components/ui/Section";

import type { ExperimentAssignments } from "../types";
import { RaterChips } from "./RaterChips";
import { NotInPart2, Part1Schedule, Part2Schedule } from "./StudySchedule";

/**
 * An ended experiment's raters, read only: the study's rater schedule for its lesson, or,
 * for an experiment run in the app, whoever was assigned before it ended. Nothing assigns.
 */
export function ConcludedRaters({
  experiment,
  view,
}: {
  experiment: ExperimentDetail;
  view: ExperimentAssignments;
}) {
  const { data: schedule, isLoading } = useStudyRaterSchedule(experiment.experiment_id);
  if (isLoading) return <p className="text-sm text-(--muted)">Loading…</p>;

  const base = `/research/experiments/${experiment.experiment_id}`;
  const sets = schedule?.sets ?? [];
  const part1 = sets.filter((set) => set.part === 1);
  const part2 = sets.filter((set) => set.part === 2);

  return (
    <>
      <Section title="Class revision notes" aside={part1.length > 0 ? "2 raters per note" : null}>
        {part1.length > 0 ? (
          <Part1Schedule sets={part1} base={base} />
        ) : (
          <RaterChips raters={view.h1?.raters ?? []} />
        )}
      </Section>

      <Section title="Learner revision notes" aside={part2.length > 0 ? "2 raters per learner" : null}>
        {part2.length > 0 ? (
          <Part2Schedule sets={part2} slots={view.h2} base={base} />
        ) : sets.length > 0 ? (
          <NotInPart2 compared={schedule?.compared_lessons ?? []} />
        ) : view.h2.length > 0 ? (
          <ul className="space-y-2">
            {view.h2.map((slot) => (
              <li key={slot.focal_case_id} className="flex flex-wrap items-center gap-3 text-sm">
                <span className="font-medium text-(--ink)">
                  {slot.student_full_name ?? slot.student_id}
                </span>
                <RaterChips raters={slot.raters} />
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-(--muted)">None.</p>
        )}
      </Section>
    </>
  );
}
