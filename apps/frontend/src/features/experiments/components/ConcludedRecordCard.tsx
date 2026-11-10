import type { ReactNode } from "react";

import { Link } from "@/shared/router";
import { LINK } from "@/shared/components/ui/table";
import { useStudyRatingsTally } from "@/features/study-ratings/useStudyRatings";

import { ExperimentDetail } from "../lib/experiments";

const succeeded = (status: string) => /succeed|complete|done/i.test(status);

type Count = { value: number; unit: string };

function Figure({ value, unit }: Count) {
  return (
    <div>
      <p className="text-2xl font-semibold text-(--ink)">{value}</p>
      <p className="text-sm text-(--muted)">{unit}</p>
    </div>
  );
}

/** One part of the record: its notes beside the ratings they received. */
function Part({
  title,
  notes,
  ratings,
  detail,
  children,
}: {
  title: string;
  notes: Count;
  ratings: Count | null;
  detail: string;
  children?: ReactNode;
}) {
  return (
    <div className="space-y-3 border-t border-(--line) pt-4">
      <p className="text-sm font-medium text-(--ink)">{title}</p>
      <div className="flex gap-10">
        <Figure {...notes} />
        {ratings ? <Figure {...ratings} /> : null}
      </div>
      <p className="text-sm text-(--ink-2)">{detail}</p>
      {children ? <div className="flex flex-wrap gap-x-4 text-sm">{children}</div> : null}
    </div>
  );
}

/**
 * What a concluded experiment holds, read only: its lesson, then each part of the study
 * with its notes beside the ratings they received, each linked to where it is read.
 */
export function ConcludedRecordCard({
  experiment,
  base,
}: {
  experiment: ExperimentDetail;
  base: string;
}) {
  const executions = experiment.executions ?? [];
  const runs = (hypothesis: string) =>
    executions
      .filter((execution) => execution.hypothesis === hypothesis)
      .flatMap((execution) => execution.condition_runs ?? [])
      .filter((run) => succeeded(run.status));
  const classNotes = runs("H1");
  const learnerNotes = runs("H2");
  const draws = executions.filter((execution) => execution.hypothesis === "H1").length;
  const conditions = [...new Set(classNotes.map((run) => run.condition_code))].sort();
  const learners = new Set(learnerNotes.flatMap((run) => (run.learner_id ? [run.learner_id] : [])))
    .size;
  const tally = useStudyRatingsTally(experiment.plan_version_id ? [experiment.plan_version_id] : [])
    .data?.[0];

  return (
    <div className="space-y-6 py-2">
      <Link href={`${base}/lesson-plan`} className={`${LINK} text-sm`}>
        Read the lesson plan and note →
      </Link>
      <div className="grid gap-8 sm:grid-cols-2">
        <Part
          title="Class revision notes"
          notes={{ value: classNotes.length, unit: "notes" }}
          ratings={tally ? { value: tally.scores, unit: "scores" } : null}
          detail={`${conditions.join(", ")}${draws > 1 ? ` × ${draws} draws` : ""}`}
        >
          <Link href={`${base}/h1`} className={LINK}>
            Notes →
          </Link>
          {tally ? (
            <Link href={`${base}/results`} className={LINK}>
              Results →
            </Link>
          ) : null}
        </Part>
        <Part
          title="Learner revision notes"
          notes={{ value: learnerNotes.length, unit: "notes" }}
          ratings={tally && learners > 0 ? { value: tally.judgements, unit: "comparisons" } : null}
          detail={learners > 0 ? `P0 and P1 for ${learners} learners` : "Not in the study's Part 2"}
        >
          {learners > 0 ? (
            <>
              <Link href={`${base}/h2`} className={LINK}>
                Compare →
              </Link>
              {tally ? (
                <Link href={`${base}/results`} className={LINK}>
                  Results →
                </Link>
              ) : null}
            </>
          ) : null}
        </Part>
      </div>
    </div>
  );
}
