import { useQuery } from "@tanstack/react-query";

import { getExperiment, getReviewPackManifest } from "../lib/api";
import {
  ComparePackManifest,
  ExperimentComparison,
} from "../lib/experiments";

const H1_ORDER = ["C0", "C1", "C2", "C3"];
const BAND_ORDER = ["remediate", "reinforce", "extend", "mixed_or_misconception"];

/**
 * Assembles the condition comparison for a lesson: the H1 base-pack ablation
 * (C0–C4) and the H2 personalisation per learner band (shared base vs P1), each
 * resolved to its rendered study-pack manifest. Reads the latest H1 + H2 executions
 * and fetches every referenced pack so the view renders real content, not logs.
 */
export function useExperimentComparison(experimentId: string | null) {
  return useQuery({
    queryKey: ["experimentComparison", experimentId ?? "empty"],
    enabled: Boolean(experimentId),
    queryFn: async (): Promise<ExperimentComparison> => {
      const detail = await getExperiment(experimentId ?? "");
      const executions = detail.executions ?? [];
      const h1 = executions.find((execution) => execution.hypothesis === "H1");
      const h2 = executions.find((execution) => execution.hypothesis === "H2");

      const artefactIds = new Set<string>();
      for (const run of [...(h1?.condition_runs ?? []), ...(h2?.condition_runs ?? [])]) {
        if (run.artefact_id) artefactIds.add(run.artefact_id);
      }
      const manifests = new Map<string, ComparePackManifest>();
      await Promise.all(
        [...artefactIds].map(async (id) => {
          try {
            manifests.set(id, await getReviewPackManifest(id));
          } catch {
            /* a missing pack just renders as unavailable */
          }
        })
      );
      const manifestOf = (id: string | null | undefined) =>
        (id && manifests.get(id)) || null;

      const h1Packs = (h1?.condition_runs ?? [])
        .filter((run) => H1_ORDER.includes(run.condition_code))
        .sort((a, b) => H1_ORDER.indexOf(a.condition_code) - H1_ORDER.indexOf(b.condition_code))
        .map((run) => ({
          condition_code: run.condition_code,
          artefact_id: run.artefact_id ?? null,
          manifest: manifestOf(run.artefact_id),
        }));

      const bandByLearner = new Map<string, string>();
      for (const focalCase of h2?.focal_cases ?? []) {
        bandByLearner.set(focalCase.learner_id, focalCase.focal_type);
      }
      const byLearner = new Map<string, { p0?: string | null; p1?: string | null }>();
      for (const run of h2?.condition_runs ?? []) {
        if (!run.learner_id) continue;
        const entry = byLearner.get(run.learner_id) ?? {};
        if (run.condition_code === "P0") entry.p0 = run.artefact_id;
        if (run.condition_code === "P1") entry.p1 = run.artefact_id;
        byLearner.set(run.learner_id, entry);
      }
      const h2Bands = [...byLearner.entries()]
        .map(([learnerId, entry]) => ({
          band: bandByLearner.get(learnerId) ?? "unknown",
          learner_id: learnerId,
          base: manifestOf(entry.p0),
          personalised: manifestOf(entry.p1),
        }))
        .sort((a, b) => BAND_ORDER.indexOf(a.band) - BAND_ORDER.indexOf(b.band));

      return { experiment_id: experimentId ?? "", h1: h1Packs, h2_bands: h2Bands };
    },
  });
}
