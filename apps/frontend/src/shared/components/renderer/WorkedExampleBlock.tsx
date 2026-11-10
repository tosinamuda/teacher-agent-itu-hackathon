import { WorkedExampleBlock as WorkedExampleBlockType } from "@/shared/types/lesson-schema";
import { stripSourceCitations } from "@/shared/utils/strip-source-citations";

import { RichText } from "./RichText";

export function WorkedExampleBlock({
  block,
}: {
  block: WorkedExampleBlockType;
}) {
  return (
    <div className="my-6 rounded-lg border-l-4 border-accent-solid bg-surface-sunken p-5">
      <div className="mb-3 font-bold uppercase tracking-wider text-accent-solid text-xs">
        Worked Example
      </div>
      <div className="prose prose-sm mb-4 font-medium text-ink">
        <RichText text={block.problem} prepare={stripSourceCitations} />
      </div>

      <div className="space-y-3">
        {block.steps.map((step, idx) => (
          <div key={idx} className="flex gap-3">
            <div className="shrink-0 flex h-6 w-6 items-center justify-center rounded-none bg-accent-soft text-xs font-bold text-accent-deep">
              {idx + 1}
            </div>
            <div className="prose prose-sm text-muted-ink">
              <RichText text={step.content} prepare={stripSourceCitations} />
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 border-t border-line pt-3">
        <span className="font-bold text-ink">Answer: </span>
        <div className="inline-block font-mono text-accent-deep align-middle prose prose-sm max-w-none">
          <RichText text={block.final_answer} prepare={stripSourceCitations} />
        </div>
      </div>
    </div>
  );
}
