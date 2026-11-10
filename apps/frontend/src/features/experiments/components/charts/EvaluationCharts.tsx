import { ExperimentStatistics } from "../../lib/experiments";
import { FigureCard } from "./FigureCard";
import { H1CompositeChart } from "./H1CompositeChart";
import { H1DimensionChart } from "./H1DimensionChart";
import { H2PairedChart } from "./H2PairedChart";
import { PairwiseEffectChart } from "./PairwiseEffectChart";
import { SourceGroundingChart } from "./SourceGroundingChart";

const SYNTHETIC_CAPTION =
  "Illustrative — synthetic dry-run ratings until expert ratings are collected.";

type EvaluationChartsProps = {
  statistics: ExperimentStatistics | undefined;
  /** "headline" = the three story charts; "full" = the complete dashboard suite. */
  variant?: "full" | "headline";
};

/** The protocol's planned charts (§6.4) driven by the experiment statistics payload. */
export function EvaluationCharts({ statistics, variant = "full" }: EvaluationChartsProps) {
  if (!statistics) {
    return null;
  }
  const caption = statistics.synthetic ? SYNTHETIC_CAPTION : undefined;

  const headline = (
    <>
      <FigureCard
        title="H1 composite quality by condition"
        caption={caption}
        filename="h1-composite"
      >
        <H1CompositeChart conditions={statistics.h1.conditions} />
      </FigureCard>
      <FigureCard title="H2 personalisation lift (P0 → P1)" caption={caption} filename="h2-paired">
        {/* Within-rating paired scores are canonical; legacy separate-packet pairs are the
            fallback for archived experiments rated before the paired-packet redesign. */}
        <H2PairedChart
          pairs={
            statistics.h2.paired_p0_p1.by_focal.length > 0
              ? statistics.h2.paired_p0_p1.by_focal
              : statistics.h2.pairs
          }
        />
      </FigureCard>
      <FigureCard title="Source-grounding audit" caption={caption} filename="source-grounding">
        <SourceGroundingChart audit={statistics.source_audit} />
      </FigureCard>
    </>
  );

  if (variant === "headline") {
    return <div className="grid gap-4 lg:grid-cols-3">{headline}</div>;
  }

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      {headline}
      <FigureCard
        title="H1 dimension scores by condition"
        caption={caption}
        filename="h1-dimensions"
      >
        <H1DimensionChart dimensions={statistics.h1.dimensions} />
      </FigureCard>
      <FigureCard
        title="Adjacent-condition effects"
        caption={caption}
        filename="pairwise-effects"
      >
        <PairwiseEffectChart contrasts={statistics.h1.contrasts} />
      </FigureCard>
    </div>
  );
}
