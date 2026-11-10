import { ContentBlockRenderer } from "@/shared/components/renderer/ContentBlockRenderer";
import { Badge } from "@/shared/components/ui/Badge";

import { ComparePackManifest } from "../lib/experiments";

/** Renders a study pack as real learner-facing sections + blocks (journey step). */
export function JourneyPack({ manifest }: { manifest: ComparePackManifest | null }) {
  if (!manifest) {
    return <p className="text-sm italic text-(--muted)">No pack generated for this step.</p>;
  }
  return (
    <div className="space-y-6">
      {manifest.steps.map((step) => (
        <article key={step.step_id}>
          <div className="flex items-center justify-between gap-2">
            <h4 className="font-semibold text-(--ink)">{step.title ?? "Section"}</h4>
            {step.personalisation_band ? (
              <Badge variant="accent">{step.personalisation_band}</Badge>
            ) : null}
          </div>
          <div className="mt-2 space-y-2">
            {step.blocks.map((block, index) => (
              <ContentBlockRenderer key={block.id ?? `${step.step_id}-${index}`} block={block} />
            ))}
          </div>
        </article>
      ))}
    </div>
  );
}
