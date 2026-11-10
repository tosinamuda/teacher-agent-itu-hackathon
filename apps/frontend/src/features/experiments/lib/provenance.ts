import { apiFetch } from "@/shared/api/client";

/** One published dataset, at the Hub commit the study was imported from. */
export type DatasetRelease = { repo: string; revision: string; provenance_sha256: string };

/** The model and prompt version that wrote some of a hypothesis's notes. */
export type GenerationRecord = {
  hypothesis: string;
  model_name: string | null;
  prompt_version: string | null;
  notes: number;
};

/** Where an experiment's notes came from and what wrote them. */
export type Provenance = {
  /** Set for an experiment imported from the published study. */
  source: { datasets: DatasetRelease[]; importer_sha256: string; imported_at: string } | null;
  generation: GenerationRecord[];
};

export const getExperimentProvenance = (experimentId: string): Promise<Provenance> =>
  apiFetch<Provenance>(`/experiments/${encodeURIComponent(experimentId)}/provenance`);

/** The dataset's files on the Hub, at exactly the commit the study was imported from. */
export const hubTreeUrl = (dataset: DatasetRelease): string =>
  `https://huggingface.co/datasets/${dataset.repo}/tree/${dataset.revision}`;
