import { Link } from "@/shared/router";

import { Section } from "@/shared/components/ui/Section";
import { LINK, ROW_HEAD, TABLE, TD, TH } from "@/shared/components/ui/table";

import { ExperimentConditionRun, ExperimentFocalCase } from "../lib/experiments";
import { objectiveStates } from "../lib/learnerState";

const succeeded = (run: ExperimentConditionRun | undefined) =>
  Boolean(run && run.artefact_id && /succeed|complete|done/i.test(run.status));

/** A learner's bands by objective, when they say more than the case does. */
function objectiveBands(focalCase: ExperimentFocalCase): string | null {
  const bands = objectiveStates(focalCase.learner_state_snapshot).map((state) => state.band ?? "—");
  return bands.some((band) => band !== focalCase.focal_type) ? bands.join(" · ") : null;
}

/**
 * H2, one row per focal learner: their case, and a way to read their two revision notes side
 * by side. A note not yet made shows where it stands; notes that were made go without saying.
 */
export function H2LearnerTable({
  focalCases,
  runs,
  experimentBaseHref,
}: {
  focalCases: ExperimentFocalCase[];
  runs: ExperimentConditionRun[];
  experimentBaseHref: string;
}) {
  if (focalCases.length === 0) {
    return <p className="text-sm text-(--muted)">No focal learners were chosen for this run.</p>;
  }
  const runFor = (learnerId: string, code: string) =>
    runs.find((run) => run.learner_id === learnerId && run.condition_code === code);
  /** Each note not yet made, with where it stands, e.g. "P1 running". */
  const unmade = (learnerId: string) =>
    ["P0", "P1"].flatMap((code) => {
      const run = runFor(learnerId, code);
      return succeeded(run) ? [] : [`${code} ${run?.status ?? "not started"}`];
    });

  return (
    <Section title="Focal learners" aside={`${focalCases.length} learners`}>
      <div className="overflow-x-auto">
        <table className={TABLE}>
          <thead>
            <tr>
              <th className={TH}>Learner</th>
              <th className={TH}>Case</th>
              <th className={TH} />
            </tr>
          </thead>
          <tbody>
            {[...focalCases]
              .sort((a, b) => a.learner_id.localeCompare(b.learner_id))
              .map((focalCase) => {
                const missing = unmade(focalCase.learner_id);
                const bands = objectiveBands(focalCase);
                return (
                  <tr key={focalCase.focal_case_id}>
                    <td className={ROW_HEAD}>
                      {focalCase.learner_name ?? focalCase.learner_id}
                      {focalCase.learner_name ? (
                        <span className="ml-2 font-mono text-xs font-normal text-(--muted)">
                          {focalCase.learner_id}
                        </span>
                      ) : null}
                    </td>
                    <td className={`${TD} capitalize`}>
                      {focalCase.focal_type}
                      {bands ? (
                        <span className="ml-2 text-xs normal-case text-(--muted)">{bands}</span>
                      ) : null}
                    </td>
                    <td className={`${TD} text-right`}>
                      {missing.length === 0 ? (
                        <Link
                          href={`${experimentBaseHref}/h2/learners/${encodeURIComponent(focalCase.learner_id)}`}
                          className={LINK}
                        >
                          Compare P0 and P1 →
                        </Link>
                      ) : (
                        <span className="text-(--ink-2)">{missing.join(" · ")}</span>
                      )}
                    </td>
                  </tr>
                );
              })}
          </tbody>
        </table>
      </div>
    </Section>
  );
}
