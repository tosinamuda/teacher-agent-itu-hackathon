import { Link } from "@/shared/router";

import { LINK, ROW_HEAD, TABLE, TD, TH } from "@/shared/components/ui/table";
import type { RatedSet, RaterSchedule } from "@/features/study-ratings/types";

import { candidateOrder, part1Grid, part2ByLearner, raterLoads } from "../lib/studySchedule";
import type { H2AssignmentSlot } from "../types";

const SHORT: Record<RatedSet["state"], string | null> = {
  complete: null,
  partial: "partly answered",
  untouched: "unanswered",
};

function Returned({ set }: { set: RatedSet }) {
  const short = SHORT[set.state];
  return short ? <span className="text-(--warning-ink)"> · {short}</span> : null;
}

/** Part 1: every note by condition and draw, the two raters who scored it, and each rater's load. */
export function Part1Schedule({ sets, base }: { sets: RatedSet[]; base: string }) {
  const grid = part1Grid(sets);
  const loads = raterLoads(sets);
  return (
    <div className="space-y-6">
      <div className="overflow-x-auto">
        <table className={TABLE}>
          <thead>
            <tr>
              <th className={TH}>Condition</th>
              {grid.draws.map((draw) => (
                <th key={draw} className={TH}>
                  Draw {draw}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {grid.conditions.map((condition) => (
              <tr key={condition}>
                <th scope="row" className={ROW_HEAD}>
                  {condition}
                </th>
                {grid.draws.map((draw) => (
                  <td key={draw} className={`${TD} whitespace-nowrap`}>
                    {grid.ratedBy(condition, draw).map((set) => (
                      <p key={set.packet} title={set.date_completed ?? undefined}>
                        {set.rater_name}
                        <Returned set={set} />
                      </p>
                    ))}
                    <Link href={`${base}/${condition.toLowerCase()}?draw=${draw}`} className={LINK}>
                      Read
                    </Link>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="overflow-x-auto">
        <table className={TABLE}>
          <thead>
            <tr>
              <th className={TH}>Rater</th>
              <th className={TH}>Notes</th>
              <th className={TH}>Completed</th>
            </tr>
          </thead>
          <tbody>
            {loads.map((load) => (
              <tr key={load.rater}>
                <td className={ROW_HEAD}>{load.rater}</td>
                <td className={`${TD} whitespace-nowrap`}>
                  {load.notes}
                  {load.short > 0 ? (
                    <span className="text-(--warning-ink)"> · {load.short} partly answered</span>
                  ) : null}
                </td>
                <td className={`${TD} text-(--ink-2)`}>
                  {load.dates.length > 0 ? load.dates.join(" · ") : "—"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function ComparedBy({ set }: { set: RatedSet }) {
  const order = candidateOrder(set);
  return (
    <p title={set.date_completed ?? undefined}>
      {set.rater_name}
      {order ? <span className="text-(--muted)"> · {order}</span> : null}
      <Returned set={set} />
    </p>
  );
}

/** Part 2: each learner, and the two raters who compared their P0 and P1. */
export function Part2Schedule({
  sets,
  slots,
  base,
}: {
  sets: RatedSet[];
  slots: H2AssignmentSlot[];
  base: string;
}) {
  const learners = part2ByLearner(sets);
  return (
    <div className="overflow-x-auto">
      <table className={TABLE}>
        <thead>
          <tr>
            <th className={TH}>Learner</th>
            <th className={TH}>Case</th>
            <th className={TH}>Compared by</th>
            <th className={TH} />
          </tr>
        </thead>
        <tbody>
          {[...slots]
            .sort((a, b) => a.student_id.localeCompare(b.student_id))
            .map((slot) => (
              <tr key={slot.focal_case_id}>
                <td className={ROW_HEAD}>{slot.student_full_name ?? slot.student_id}</td>
                <td className={`${TD} capitalize`}>{slot.focal_case_type}</td>
                <td className={`${TD} whitespace-nowrap`}>
                  {(learners.get(slot.student_id) ?? []).map((set) => (
                    <ComparedBy key={set.packet} set={set} />
                  ))}
                </td>
                <td className={`${TD} text-right`}>
                  <Link href={`${base}/h2/learners/${slot.student_id}`} className={LINK}>
                    Compare
                  </Link>
                </td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
}

/** A lesson the study's Part 2 left out, and the lessons it did compare. */
export function NotInPart2({ compared }: { compared: RaterSchedule["compared_lessons"] }) {
  return (
    <p className="text-sm text-(--ink-2)">
      Not in the study&apos;s Part 2
      {compared.length > 0 ? (
        <>
          , which compared{" "}
          {compared.map((lesson, index) => (
            <span key={lesson.experiment_id}>
              {index > 0 ? (index === compared.length - 1 ? " and " : ", ") : null}
              <Link
                href={`/research/experiments/${lesson.experiment_id}/raters`}
                className={`${LINK} font-mono`}
              >
                {lesson.experiment_code}
              </Link>
            </span>
          ))}
        </>
      ) : null}
      .
    </p>
  );
}
