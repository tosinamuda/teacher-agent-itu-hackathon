import { Link } from "@/shared/router";

import { Section } from "@/shared/components/ui/Section";
import { LINK, ROW_HEAD, TABLE, TD, TH } from "@/shared/components/ui/table";

import { ExperimentConditionRun, ExperimentExecution } from "../lib/experiments";

const succeeded = (run: ExperimentConditionRun | undefined) =>
  Boolean(run?.artefact_id && /succeed|complete|done/i.test(run.status));

/** An imported study's class notes: one row per condition, one column per draw. */
export function StudyDraws({
  draws,
  experimentBaseHref,
  onExportPack,
  exportingArtefactId,
}: {
  draws: ExperimentExecution[];
  experimentBaseHref: string;
  onExportPack: (artefactId: string) => void;
  exportingArtefactId: string | null;
}) {
  const conditions = [
    ...new Set(draws.flatMap((draw) => (draw.condition_runs ?? []).map((run) => run.condition_code))),
  ].sort();
  const runOf = (draw: ExperimentExecution, condition: string) =>
    (draw.condition_runs ?? []).find((run) => run.condition_code === condition);

  return (
    <Section title="Class revision notes" aside={`${conditions.length} conditions × ${draws.length} draws`}>
      <div className="overflow-x-auto">
        <table className={TABLE}>
          <thead>
            <tr>
              <th className={TH}>Condition</th>
              {draws.map((draw) => (
                <th key={draw.execution_id} className={TH}>
                  Draw {draw.attempt_number}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {conditions.map((condition) => (
              <tr key={condition}>
                <th scope="row" className={ROW_HEAD}>
                  {condition}
                </th>
                {draws.map((draw) => {
                  const run = runOf(draw, condition);
                  return (
                    <td key={draw.execution_id} className={TD}>
                      {run && succeeded(run) ? (
                        <span className="flex gap-4">
                          <Link
                            href={`${experimentBaseHref}/${condition.toLowerCase()}?draw=${draw.attempt_number}`}
                            className={LINK}
                          >
                            Read
                          </Link>
                          <button
                            type="button"
                            onClick={() => onExportPack(run.artefact_id as string)}
                            disabled={exportingArtefactId === run.artefact_id}
                            className="text-(--muted) hover:text-(--ink) disabled:opacity-60"
                          >
                            {exportingArtefactId === run.artefact_id ? "Exporting…" : "PDF"}
                          </button>
                        </span>
                      ) : (
                        <span className="text-(--muted)">{run?.status ?? "—"}</span>
                      )}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Section>
  );
}
