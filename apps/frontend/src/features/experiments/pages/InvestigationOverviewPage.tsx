import { Link } from "@/shared/router";

import { Button } from "@/shared/components/ui/Button";
import { Section } from "@/shared/components/ui/Section";
import { useStudyRatingsTally } from "@/features/study-ratings/useStudyRatings";

import { InvestigationExperimentsTable } from "../components/InvestigationExperimentsTable";
import { useInvestigation } from "../hooks/useInvestigations";

/** A study's lessons, each linked to its experiment, with the study's rating counts beside it. */
export default function InvestigationOverviewPage({
  investigationId,
}: {
  investigationId: string;
}) {
  const investigation = useInvestigation(investigationId).data;
  const planVersionIds = (investigation?.experiments ?? []).flatMap((experiment) =>
    experiment.plan_version_id ? [experiment.plan_version_id] : [],
  );
  const tallies = useStudyRatingsTally(planVersionIds).data ?? [];
  if (!investigation) return null;

  return (
    <Section
      title="Lessons"
      aside={
        investigation.status === "ended" ? null : (
          <Link
            href={`/research/experiments/new?investigationId=${investigation.investigation_id}`}
          >
            <Button size="sm">Add experiment</Button>
          </Link>
        )
      }
    >
      <InvestigationExperimentsTable experiments={investigation.experiments} tallies={tallies} />
    </Section>
  );
}
