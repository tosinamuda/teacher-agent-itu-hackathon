import { Section } from "@/shared/components/ui/Section";
import { StudyLessonResults } from "@/features/study-ratings/StudyLessonResults";
import { useStudyRatingsTally } from "@/features/study-ratings/useStudyRatings";

import { ExperimentStatistics } from "../components/ExperimentStatistics";
import { EvaluationCharts } from "../components/charts/EvaluationCharts";
import { OfflineRatingImport } from "../components/OfflineRatingImport";
import { ResearchRatingsProgress } from "../components/ResearchRatingsProgress";
import { ResearchResultsSummary } from "../components/ResearchResultsSummary";
import { SyntheticProxyCard } from "../components/SyntheticProxyCard";
import { useExperiment } from "../hooks/useExperiments";
import { useExperimentRatings, useExperimentStatistics } from "../hooks/useExperimentResults";

/**
 * Results tab: what the run produced, split by provenance. The Expert zone (reported)
 * sits on top — its numbers are expert-only; when no expert raters have scored it yet,
 * an empty state points to the next action. Synthetic dry-run ratings are demoted to a
 * clearly-labelled proxy card below, never mixed into the reported figures.
 */
export default function ExperimentResultsPage({ experimentId }: { experimentId: string }) {
  const experimentQuery = useExperiment(experimentId);
  const ratingsQuery = useExperimentRatings(experimentId);
  const statisticsQuery = useExperimentStatistics(experimentId);
  const experiment = experimentQuery.data;
  const ratings = ratingsQuery.data;
  const hasRun = (experiment?.executions?.length ?? 0) > 0;
  const hasExpert = (ratings?.total_ratings ?? 0) > 0;
  const stats = statisticsQuery.data;
  // An ended experiment's lesson is concluded: nothing is rated or imported any more.
  const concluded = experiment?.lifecycle_status === "ended";
  const planVersionId = experiment?.plan_version_id ?? null;
  const studyTally = useStudyRatingsTally(planVersionId ? [planVersionId] : []).data?.[0];
  const hasCharts = Boolean(
    stats &&
      (stats.h1.n_ratings + stats.h2.n_ratings > 0 || stats.source_audit.n_ratings > 0)
  );

  if (!hasRun) {
    return (
      <p className="mt-4 rounded-2xl border border-dashed border-(--line) bg-(--panel)/40 px-4 py-8 text-center text-sm text-(--muted)">
        Nothing to show yet. Start a run on the <span className="font-semibold">Run</span> tab —
        generation summary, expert ratings, and statistics appear here once it has run.
      </p>
    );
  }

  if (concluded && studyTally) {
    return (
      <div className="space-y-8 py-6">
        <StudyLessonResults experimentId={experimentId} />
      </div>
    );
  }

  return (
    <div className="space-y-8 py-6">
      <Section title="Generation summary">
        <ResearchResultsSummary execution={experiment?.executions?.[0]} />
      </Section>

      <Section title="Expert evaluation · reported">
        {hasExpert ? (
          <div className="space-y-6">
            <ResearchRatingsProgress ratings={ratings} isLoading={ratingsQuery.isLoading} />
            <ExperimentStatistics
              statistics={statisticsQuery.data}
              isLoading={statisticsQuery.isLoading}
            />
          </div>
        ) : (
          <div className="rounded-2xl border border-(--line) bg-(--surface) px-4 py-6 text-center">
            <p className="text-sm font-medium text-(--ink)">Not yet evaluated</p>
            <p className="mt-1 text-sm text-(--muted)">
              {concluded
                ? "No expert ratings were recorded before this experiment ended."
                : "No expert raters have scored this experiment. Invite raters, or import offline ratings below. These are the only numbers reported in the study."}
            </p>
          </div>
        )}
      </Section>

      {hasCharts ? (
        <Section title="Charts">
          <EvaluationCharts statistics={stats} variant="full" />
        </Section>
      ) : null}

      {ratings?.synthetic ? (
        <Section title="Synthetic rehearsal · proxy">
          <SyntheticProxyCard synthetic={ratings.synthetic} />
        </Section>
      ) : null}

      {concluded ? null : (
        <Section title="Add expert ratings (offline import)">
          <OfflineRatingImport />
        </Section>
      )}
    </div>
  );
}
