import { Section } from "@/shared/components/ui/Section";
import { ROW_HEAD, TABLE, TD, TH } from "@/shared/components/ui/table";
import { FigureCard } from "@/features/experiments/components/charts/FigureCard";

import { objectiveSeries } from "./chartData";
import { FavourableChart, SpreadChart } from "./ProportionCharts";
import { FavourableShares, Part2Choices } from "./ProportionTables";
import { ObjectiveLinesChart, Part1Chart, Part2Chart } from "./StudyResultsCharts";
import { useStudyInstrument, useStudyWideResults } from "./useStudyRatings";

/** Each objective's means by condition, the numbers behind the objective chart. */
function ObjectiveTable({ series }: { series: ReturnType<typeof objectiveSeries> }) {
  const conditions = [...new Set(series.flatMap((each) => Object.keys(each.means)))].sort();
  return (
    <details className="text-sm">
      <summary className="cursor-pointer text-(--muted) hover:text-(--ink)">
        Each objective&apos;s means · {series.length} objectives
      </summary>
      <div className="mt-3 overflow-x-auto">
        <table className={TABLE}>
          <thead>
            <tr>
              <th className={`${TH} w-1/2`}>Objective</th>
              {conditions.map((condition) => (
                <th key={condition} className={TH}>
                  {condition}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {series.map((each) => (
              <tr key={each.key}>
                <td className={ROW_HEAD}>
                  {each.text}
                  <p className="font-mono text-xs font-normal text-(--muted)">{each.lesson}</p>
                </td>
                {conditions.map((condition) => (
                  <td key={condition} className={TD}>
                    {each.means[condition]?.toFixed(2) ?? "—"}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </details>
  );
}

/**
 * A study's ratings across all its lessons, described: Part 1 pooled by criterion and
 * condition, each lesson objective as a data point across the conditions, and Part 2's
 * comparisons pooled. Nothing here is a test.
 */
export function StudyWideResults({ investigationId }: { investigationId: string }) {
  const results = useStudyWideResults(investigationId, true).data;
  const instrument = useStudyInstrument().data;
  if (!results || !instrument) return <p className="text-sm text-(--muted)">Loading…</p>;
  const series = objectiveSeries(results.objectives);
  return (
    <>
      <Section
        title="Class revision notes"
        aside="Every lesson, rater and draw pooled; descriptive only"
      >
        <div className="grid gap-4 xl:grid-cols-2">
          <FigureCard title="Mean score by criterion and condition" filename="study-part1-pooled">
            <Part1Chart results={results} criteria={instrument.part_1} />
          </FigureCard>
          <FigureCard
            title="Each objective across the conditions"
            filename="study-part1-objectives"
          >
            <ObjectiveLinesChart series={series} />
          </FigureCard>
        </div>
        <div className="grid gap-4 xl:grid-cols-2">
          <FigureCard title="Share scored 4 or 5" filename="study-part1-favourable">
            <FavourableChart results={results} criteria={instrument.part_1} />
          </FigureCard>
          <FigureCard title="How the scores spread" filename="study-part1-spread">
            <SpreadChart results={results} />
          </FigureCard>
        </div>
        <FavourableShares results={results} criteria={instrument.part_1} />
        <ObjectiveTable series={series} />
      </Section>
      {results.part_2.length > 0 ? (
        <Section title="Learner revision notes" aside="Every compared learner pooled">
          <FigureCard title="Which note raters preferred" filename="study-part2-pooled">
            <Part2Chart results={results} criteria={instrument.part_2} />
          </FigureCard>
          <Part2Choices results={results} criteria={instrument.part_2} />
        </Section>
      ) : null}
    </>
  );
}
