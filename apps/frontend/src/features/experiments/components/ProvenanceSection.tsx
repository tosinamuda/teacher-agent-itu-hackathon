import type { ReactNode } from "react";

import { Section } from "@/shared/components/ui/Section";
import { LINK } from "@/shared/components/ui/table";

import { useExperimentProvenance } from "../hooks/useExperimentProvenance";
import { GenerationRecord, hubTreeUrl } from "../lib/provenance";

const short = (sha: string) => sha.slice(0, 7);

function Row({ term, children }: { term: string; children: ReactNode }) {
  return (
    <>
      <dt className="text-(--muted)">{term}</dt>
      <dd className="text-(--ink)">{children}</dd>
    </>
  );
}

/** Each hypothesis's prompt versions, with how many notes each wrote. */
function promptVersions(records: GenerationRecord[]): string[] {
  const byHypothesis = new Map<string, string[]>();
  for (const record of records) {
    const version = `${record.prompt_version ?? "unrecorded"} (${record.notes})`;
    byHypothesis.set(record.hypothesis, [...(byHypothesis.get(record.hypothesis) ?? []), version]);
  }
  return [...byHypothesis.entries()].map(
    ([hypothesis, versions]) => `${hypothesis} ${versions.join(", ")}`,
  );
}

/**
 * Where the experiment's notes came from and what wrote them: for an imported study, the
 * published release at its exact Hub commits and the importer that read it; for every
 * experiment, the model and prompt version behind its notes.
 */
export function ProvenanceSection({ experimentId }: { experimentId: string }) {
  const provenance = useExperimentProvenance(experimentId).data;
  if (!provenance) return null;
  const { source, generation } = provenance;
  const models = [...new Set(generation.map((record) => record.model_name ?? "unrecorded"))];

  return (
    <Section title="Provenance">
      {generation.length === 0 && !source ? (
        <p className="text-sm text-(--muted)">Nothing generated yet.</p>
      ) : (
        <dl className="grid grid-cols-[9rem_1fr] gap-x-6 gap-y-2 text-sm">
          {source ? (
            <>
              <Row term="Released as">
                <ul className="space-y-0.5">
                  {source.datasets.map((dataset) => (
                    <li key={dataset.repo}>
                      <a
                        href={hubTreeUrl(dataset)}
                        target="_blank"
                        rel="noreferrer"
                        className={LINK}
                        title={`PROVENANCE.json sha256 ${dataset.provenance_sha256}`}
                      >
                        {dataset.repo}
                      </a>
                      <span className="ml-2 font-mono text-xs text-(--muted)">
                        @ {short(dataset.revision)}
                      </span>
                    </li>
                  ))}
                </ul>
              </Row>
              <Row term="Imported">
                {new Date(source.imported_at).toLocaleDateString(undefined, {
                  dateStyle: "medium",
                })}
                <span
                  className="ml-2 font-mono text-xs text-(--muted)"
                  title={`importer sha256 ${source.importer_sha256}`}
                >
                  importer {short(source.importer_sha256)}
                </span>
              </Row>
            </>
          ) : null}
          {generation.length > 0 ? (
            <>
              <Row term="Model">{models.join(", ")}</Row>
              <Row term="Prompt version">
                <ul className="space-y-0.5">
                  {promptVersions(generation).map((line) => (
                    <li key={line}>{line}</li>
                  ))}
                </ul>
              </Row>
            </>
          ) : null}
        </dl>
      )}
    </Section>
  );
}
