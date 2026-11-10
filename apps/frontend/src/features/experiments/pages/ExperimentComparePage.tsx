import { useMemo, useState } from "react";

import { Choices } from "@/shared/components/ui/Choices";
import { Picker } from "@/shared/components/ui/Picker";
import { Section } from "@/shared/components/ui/Section";

import { SectionCompare } from "../components/SectionCompare";
import { useExperimentComparison } from "../hooks/useExperimentComparison";
import { ComparePackManifest } from "../lib/experiments";

const H1_LABEL: Record<string, string> = {
  C0: "C0 · objective only",
  C1: "C1 · lesson steps",
  C2: "C2 · + retrieval",
  C3: "C3 · grounded base",
};
const BAND_LABEL: Record<string, string> = {
  remediate: "Remediate",
  reinforce: "Reinforce",
  extend: "Extend",
  mixed_or_misconception: "Mixed / misconception",
};

/** A small pill-group selector for choosing what to compare. */
/**
 * Side-by-side condition comparison for one lesson, rendered as real study-pack
 * content and aligned section-by-section. Pick any two H1 conditions (C0→C3) to
 * compare grounding, and a band to compare its base (P0) vs personalised (P1) pack.
 */
export default function ExperimentComparePage({ experimentId }: { experimentId: string }) {
  const { data, isLoading, isError } = useExperimentComparison(experimentId);

  const h1Map = useMemo(() => {
    const map: Record<string, ComparePackManifest | null> = {};
    (data?.h1 ?? []).forEach((condition) => {
      map[condition.condition_code] = condition.manifest;
    });
    return map;
  }, [data]);
  const h1Codes = useMemo(() => (data?.h1 ?? []).map((c) => c.condition_code), [data]);

  const [h1Left, setH1Left] = useState("C0");
  const [h1Right, setH1Right] = useState("C3");
  const [bandLearner, setBandLearner] = useState<string | null>(null);

  const activeBand =
    (data?.h2_bands ?? []).find((band) => band.learner_id === bandLearner) ?? data?.h2_bands?.[0];

  const h1Options = h1Codes.map((code) => ({ value: code, label: code }));
  const bandOptions = [...(data?.h2_bands ?? [])]
    .sort((a, b) => a.learner_id.localeCompare(b.learner_id))
    .map((band) => ({
      value: band.learner_id,
      label: `${band.learner_id} · ${BAND_LABEL[band.band] ?? band.band}`,
    }));

  return (
    <div className="space-y-6 py-6">

      {isError ? <p className="mb-4 text-sm text-(--danger)">Couldn&apos;t load the comparison.</p> : null}
      {isLoading ? <p className="text-sm text-(--muted)">Loading packs…</p> : null}

      {data ? (
        <div className="space-y-10">
          <Section title="Class revision notes">
            {h1Codes.length === 0 ? (
              <p className="text-sm text-(--muted)">None for this lesson.</p>
            ) : (
              <>
                <div className="flex flex-wrap items-center gap-3">
                  <Choices options={h1Options} value={h1Left} onChange={setH1Left} />
                  <span className="text-sm text-(--muted)">vs</span>
                  <Choices options={h1Options} value={h1Right} onChange={setH1Right} />
                </div>
                <SectionCompare
                  leftLabel={H1_LABEL[h1Left] ?? h1Left}
                  rightLabel={H1_LABEL[h1Right] ?? h1Right}
                  left={h1Map[h1Left] ?? null}
                  right={h1Map[h1Right] ?? null}
                />
              </>
            )}
          </Section>

          <Section title="Learner revision notes" aside="Each learner's P0 against their P1">
            {bandOptions.length === 0 || !activeBand ? (
              <p className="text-sm text-(--muted)">None for this lesson.</p>
            ) : (
              <>
                <Picker
                  label="Learner"
                  options={bandOptions}
                  value={activeBand.learner_id}
                  onChange={setBandLearner}
                />
                <SectionCompare
                  leftLabel="Base (P0)"
                  rightLabel="Personalised (P1)"
                  rightBadge={BAND_LABEL[activeBand.band] ?? activeBand.band}
                  left={activeBand.base}
                  right={activeBand.personalised}
                />
              </>
            )}
          </Section>
        </div>
      ) : null}
    </div>
  );
}
