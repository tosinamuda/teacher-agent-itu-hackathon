import { ROW_HEAD, TABLE, TD, TH } from "@/shared/components/ui/table";

import { outcomeCounts, overallMeans } from "./lessonResults";
import { Share, bothFavourable, favourable, shareOf } from "./proportions";
import { ConditionMean, InstrumentCriterion, LessonResults } from "./types";

function Percent({ share }: { share: Share }) {
  return (
    <span className="whitespace-nowrap">
      <span className="font-medium text-(--ink)">{share.percent.toFixed(1)}%</span>
      <span className="ml-1.5 text-xs text-(--muted)">
        {share.count}/{share.of}
      </span>
    </span>
  );
}

function ShareRows({
  name,
  conditions,
  of,
}: {
  name: string;
  conditions: string[];
  of: (condition: string) => ConditionMean | undefined;
}) {
  const paired = conditions.some((condition) => (of(condition)?.double_rated ?? 0) > 0);
  const cells = (read: (mean: ConditionMean) => Share) =>
    conditions.map((condition) => {
      const mean = of(condition);
      return (
        <td key={condition} className={TD}>
          {mean ? <Percent share={read(mean)} /> : "—"}
        </td>
      );
    });
  return (
    <>
      <tr>
        <th scope="row" className={ROW_HEAD}>
          {name}
        </th>
        {cells(favourable)}
      </tr>
      {paired ? (
        <tr>
          <th scope="row" className={`${TD} pl-4 text-left font-normal text-(--muted)`}>
            both raters
          </th>
          {cells(bothFavourable)}
        </tr>
      ) : null}
    </>
  );
}

/** Part 1: each criterion's scores at 4 or 5 by condition, and cells both raters scored so. */
export function FavourableShares({
  results,
  criteria,
}: {
  results: LessonResults;
  criteria: InstrumentCriterion[];
}) {
  const conditions = [...new Set(results.part_1.map((mean) => mean.condition))].sort();
  const overall = overallMeans(results.part_1);
  const of = (criterionId: string) => (condition: string) =>
    results.part_1.find((m) => m.criterion_id === criterionId && m.condition === condition);
  return (
    <div className="overflow-x-auto">
      <table className={TABLE}>
        <thead>
          <tr>
            <th className={`${TH} w-2/5`}>Scored 4 or 5</th>
            {conditions.map((condition) => (
              <th key={condition} className={TH}>
                {condition}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {criteria.map((criterion) => (
            <ShareRows
              key={criterion.id}
              name={criterion.name}
              conditions={conditions}
              of={of(criterion.id)}
            />
          ))}
          <ShareRows
            name="All criteria"
            conditions={conditions}
            of={(condition) => overall.get(condition)}
          />
        </tbody>
      </table>
    </div>
  );
}

/** A side's comparisons as a share of the criterion's, with how many were clear. */
function Side({ clearly, slightly, of }: { clearly: number; slightly: number; of: number }) {
  return (
    <>
      <Percent share={shareOf(clearly + slightly, of)} />
      {clearly + slightly > 0 ? (
        <span className="ml-1.5 text-xs text-(--muted)">{clearly} clearly</span>
      ) : null}
    </>
  );
}

/** Part 2: each criterion's comparisons split by the note preferred, as shares. */
export function Part2Choices({
  results,
  criteria,
}: {
  results: LessonResults;
  criteria: InstrumentCriterion[];
}) {
  return (
    <div className="overflow-x-auto">
      <table className={TABLE}>
        <thead>
          <tr>
            <th className={`${TH} w-2/5`}>Criterion</th>
            <th className={TH}>P1 better</th>
            <th className={TH}>Same</th>
            <th className={TH}>P0 better</th>
          </tr>
        </thead>
        <tbody>
          {criteria.map((criterion) => {
            const counts = outcomeCounts(results.part_2, criterion.id);
            const [p1Clearly, p1Slightly, same, p0Slightly, p0Clearly] = counts;
            const total = counts.reduce((sum, count) => sum + count, 0);
            return (
              <tr key={criterion.id}>
                <th scope="row" className={ROW_HEAD}>
                  {criterion.name}
                </th>
                <td className={`${TD} whitespace-nowrap`}>
                  <Side clearly={p1Clearly} slightly={p1Slightly} of={total} />
                </td>
                <td className={TD}>
                  <Percent share={shareOf(same, total)} />
                </td>
                <td className={`${TD} whitespace-nowrap`}>
                  <Side clearly={p0Clearly} slightly={p0Slightly} of={total} />
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
