import { Section } from "@/shared/components/ui/Section";
import { ROW_HEAD, TABLE, TD, TH } from "@/shared/components/ui/table";
import { ProvenanceSection } from "@/features/experiments/components/ProvenanceSection";
import type { InvestigationDetail } from "@/features/experiments/lib/experiments";
import { StudyWideResults } from "@/features/study-ratings/StudyWideResults";
import type { StudyRatingsTally } from "@/features/study-ratings/types";

import type { LessonDesign, StudyDesign } from "./studyData";
import { LessonRecord } from "./useLessonRecord";

const span = (conditions: string[]) =>
  conditions.length > 1 ? `${conditions[0]}–${conditions[conditions.length - 1]}` : conditions[0];

/** What the study was: its scope counted from the record, its two parts, and each lesson's share. */
export function DesignStep({
  investigation,
  design,
}: {
  investigation: InvestigationDetail;
  design: StudyDesign | undefined;
}) {
  if (!design) return <p className="text-sm text-(--muted)">Loading…</p>;
  const title = new Map(
    investigation.experiments.map((each) => [each.experiment_id, each.lesson_title ?? each.experiment_code]),
  );
  const total = (count: (lesson: LessonDesign) => number) =>
    design.lessons.reduce((sum, lesson) => sum + count(lesson), 0);
  const inPart2 = design.lessons.filter((lesson) => lesson.learners > 0).length;
  const scope: [number, string][] = [
    [design.lessons.length, "lessons"],
    [total((lesson) => lesson.objectives), "objectives"],
    [total((lesson) => lesson.class_notes), "class notes"],
    [total((lesson) => lesson.learners), "Part 2 cases"],
    [design.raters, "raters"],
  ];
  const parts: [string, string][] = [
    [
      "Part 1 · H1",
      `Each lesson's class note written under ${span(design.conditions)}, ${design.draws} draws each; every note scored objective by objective.`,
    ],
    [
      "Part 2 · H2",
      `In ${inPart2} lessons, each learner's personalised note (P1) set blind beside the class note (P0); raters chose the better.`,
    ],
  ];
  return (
    <div className="space-y-10">
      <dl className="grid grid-cols-2 gap-6 sm:grid-cols-5">
        {scope.map(([count, label]) => (
          <div key={label}>
            <dt className="text-sm text-(--muted)">{label}</dt>
            <dd className="text-2xl font-semibold tabular-nums text-(--ink)">{count}</dd>
          </div>
        ))}
      </dl>
      <dl className="space-y-3 text-sm">
        {parts.map(([part, what]) => (
          <div key={part} className="grid gap-1 sm:grid-cols-[8rem_1fr]">
            <dt className="font-medium text-(--ink)">{part}</dt>
            <dd className="text-(--ink-2)">{what}</dd>
          </div>
        ))}
      </dl>
      <Section title="Lessons">
        <div className="overflow-x-auto">
          <table className={TABLE}>
            <thead>
              <tr>
                <th className={TH}>Topic</th>
                <th className={TH}>Objectives</th>
                <th className={TH}>Class notes</th>
                <th className={TH}>Part 1 forms</th>
                <th className={TH}>Learners</th>
                <th className={TH}>Part 2 forms</th>
              </tr>
            </thead>
            <tbody>
              {design.lessons.map((lesson) => (
                <tr key={lesson.experiment_id}>
                  <td className={ROW_HEAD}>{title.get(lesson.experiment_id)}</td>
                  <td className={TD}>{lesson.objectives}</td>
                  <td className={TD}>{lesson.class_notes}</td>
                  <td className={TD}>{lesson.part_1_sets}</td>
                  <td className={TD}>{lesson.learners || "—"}</td>
                  <td className={TD}>{lesson.part_2_sets || "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Section>
    </div>
  );
}

/** The study's ratings across all its lessons, each objective a data point. */
export function ResultsStep({ investigationId }: { investigationId: string }) {
  return (
    <div className="space-y-10">
      <StudyWideResults investigationId={investigationId} />
    </div>
  );
}

/** What the study did not cover, read from its record rather than asserted. */
function limitsOf(
  investigation: InvestigationDetail,
  tallies: StudyRatingsTally[],
  record: LessonRecord,
): string[] {
  const lessons = investigation.experiments.length;
  const compared = tallies.filter((tally) => tally.judgements > 0).length;
  const schools = new Set(investigation.experiments.map((experiment) => experiment.school_name));
  const classes = new Set(investigation.experiments.map((experiment) => experiment.class_name));
  const limits = [
    `Part 2 compared learners in ${compared} of ${lessons} lessons, those with marked class work.`,
    `${schools.size === 1 ? "One school" : `${schools.size} schools`}, ${
      classes.size === 1 ? "one class" : `${classes.size} classes`
    }.`,
  ];
  if (record.conditions.length > 0 && !record.conditions.includes("C4")) {
    limits.unshift("C4, the teacher-reviewed class note, was not run.");
  }
  return limits;
}

/** Where the study came from, and what it did not cover. */
export function ProvenanceStep({
  investigation,
  tallies,
  record,
}: {
  investigation: InvestigationDetail;
  tallies: StudyRatingsTally[];
  record: LessonRecord;
}) {
  return (
    <div className="space-y-8">
      {record.experiment ? (
        <ProvenanceSection experimentId={record.experiment.experiment_id} />
      ) : null}
      <section className="space-y-2">
        <h2 className="text-base font-semibold text-(--ink)">Limits</h2>
        <ul className="list-disc space-y-1 pl-5 text-sm text-(--ink-2)">
          {limitsOf(investigation, tallies, record).map((limit) => (
            <li key={limit}>{limit}</li>
          ))}
        </ul>
      </section>
    </div>
  );
}
