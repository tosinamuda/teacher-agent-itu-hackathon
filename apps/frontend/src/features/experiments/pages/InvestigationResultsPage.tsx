import { Section } from "@/shared/components/ui/Section";
import { StudyWideResults } from "@/features/study-ratings/StudyWideResults";
import { useStudyRatingsTally } from "@/features/study-ratings/useStudyRatings";

import { InvestigationResultsRollup } from "../components/InvestigationResultsRollup";
import { useInvestigation, useInvestigationResults } from "../hooks/useInvestigations";

/**
 * A study's results across its lessons: the study's own ratings charted when it has them,
 * and the ratings made in the app rolled up whenever there are any.
 */
export default function InvestigationResultsPage({ investigationId }: { investigationId: string }) {
  const investigation = useInvestigation(investigationId).data;
  const resultsQuery = useInvestigationResults(investigationId);
  const planVersionIds = (investigation?.experiments ?? []).flatMap((experiment) =>
    experiment.plan_version_id ? [experiment.plan_version_id] : [],
  );
  const tallyQuery = useStudyRatingsTally(planVersionIds);
  const hasStudyRatings = (tallyQuery.data ?? []).length > 0;
  const inAppPackets = resultsQuery.data?.packet_count ?? 0;
  if (!investigation || tallyQuery.isLoading) {
    return <p className="text-sm text-(--muted)">Loading…</p>;
  }

  return (
    <>
      {hasStudyRatings ? <StudyWideResults investigationId={investigationId} /> : null}
      {!hasStudyRatings || inAppPackets > 0 ? (
        <Section title="Ratings made in the app">
          <InvestigationResultsRollup
            rollup={resultsQuery.data}
            isLoading={resultsQuery.isLoading}
          />
        </Section>
      ) : null}
    </>
  );
}
