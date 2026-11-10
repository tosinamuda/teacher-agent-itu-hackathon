import { Section } from "@/shared/components/ui/Section";
import { ROW_HEAD, TABLE, TD, TH } from "@/shared/components/ui/table";

import { FigureCard } from "@/features/experiments/components/charts/FigureCard";

import { overallMeans } from "./lessonResults";
import { FavourableChart, SpreadChart } from "./ProportionCharts";
import { FavourableShares, Part2Choices } from "./ProportionTables";
import { Part1Chart, Part2Chart } from "./StudyResultsCharts";
import { InstrumentCriterion, LessonResults } from "./types";
import { useStudyInstrument, useStudyLessonResults } from "./useStudyRatings";

function Mean({ mean, n }: { mean: number; n: number }) {
  return (
    <span className="font-medium text-(--ink)" title={`${n} scores`}>
      {mean.toFixed(2)}
    </span>
  );
}

function Part1Means({
  results,
  criteria,
}: {
  results: LessonResults;
  criteria: InstrumentCriterion[];
}) {
  const conditions = [...new Set(results.part_1.map((mean) => mean.condition))].sort();
  const overall = overallMeans(results.part_1);
  const cell = (criterionId: string, condition: string) =>
    results.part_1.find(
      (mean) => mean.criterion_id === criterionId && mean.condition === condition,
    );
  return (
    <div className="overflow-x-auto">
      <table className={TABLE}>
        <thead>
          <tr>
            <th className={`${TH} w-2/5`}>Criterion</th>
            {conditions.map((condition) => (
              <th key={condition} className={TH}>
                {condition}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {criteria.map((criterion) => (
            <tr key={criterion.id}>
              <th scope="row" className={ROW_HEAD}>
                {criterion.name}
              </th>
              {conditions.map((condition) => {
                const found = cell(criterion.id, condition);
                return (
                  <td key={condition} className={TD}>
                    {found ? <Mean mean={found.mean} n={found.n} /> : "—"}
                  </td>
                );
              })}
            </tr>
          ))}
          <tr>
            <th scope="row" className={`${ROW_HEAD} font-semibold`}>
              All criteria
            </th>
            {conditions.map((condition) => {
              const found = overall.get(condition);
              return (
                <td key={condition} className={TD}>
                  {found ? <Mean mean={found.mean} n={found.n} /> : "—"}
                </td>
              );
            })}
          </tr>
        </tbody>
      </table>
    </div>
  );
}

/**
 * One lesson's study ratings, described: Part 1's mean score, share scored 4 or 5 and spread
 * per criterion for each condition, and Part 2's comparisons counted by outcome. Every rater, draw and objective
 * is pooled, and nothing here is a test.
 */
export function StudyLessonResults({ experimentId }: { experimentId: string }) {
  const results = useStudyLessonResults(experimentId).data;
  const instrument = useStudyInstrument().data;
  if (!results || !instrument) return <p className="text-sm text-(--muted)">Loading…</p>;
  return (
    <>
      <Section
        title="Class revision notes"
        aside="Every rater, draw and objective pooled"
      >
        <FigureCard title="Mean score by criterion and condition" filename="study-part1-means">
          <Part1Chart results={results} criteria={instrument.part_1} />
        </FigureCard>
        <Part1Means results={results} criteria={instrument.part_1} />
        <div className="grid gap-4 xl:grid-cols-2">
          <FigureCard title="Share scored 4 or 5" filename="study-part1-favourable">
            <FavourableChart results={results} criteria={instrument.part_1} />
          </FigureCard>
          <FigureCard title="How the scores spread" filename="study-part1-spread">
            <SpreadChart results={results} />
          </FigureCard>
        </div>
        <FavourableShares results={results} criteria={instrument.part_1} />
      </Section>
      <Section
        title="Learner revision notes"
        aside="Which of each learner's notes raters preferred"
      >
        {results.part_2.length > 0 ? (
          <>
            <FigureCard title="Which note raters preferred" filename="study-part2-preferences">
              <Part2Chart results={results} criteria={instrument.part_2} />
            </FigureCard>
            <Part2Choices results={results} criteria={instrument.part_2} />
          </>
        ) : (
          <p className="text-sm text-(--ink-2)">Not in the study&apos;s Part 2.</p>
        )}
      </Section>
    </>
  );
}
