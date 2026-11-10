import { Controller, useForm, useWatch } from "react-hook-form";

import { Button } from "@/shared/components/ui/Button";

import { CompactScoreField } from "./CompactScoreField";
import { SourceAuditItemDetail, SourceAuditRatingSaveRequest } from "../types";

const SCORE_OPTIONS = [
  { value: 0, label: "0 Fail" },
  { value: 1, label: "1 Partial" },
  { value: 2, label: "2 Pass" },
];

type FormValues = {
  source_relevance?: number;
  support_sufficiency?: number;
  faithfulness?: number;
  scope_correctness?: number;
  recommendation: string;
};

const isScore = (value: unknown): value is number =>
  value === 0 || value === 1 || value === 2;

type AuditRatingFormProps = {
  detail: SourceAuditItemDetail;
  isSaving: boolean;
  onSubmit: (payload: SourceAuditRatingSaveRequest) => Promise<void>;
};

/** Renders the four 0/1/2 source-grounding criteria + an optional recommendation for one audit item. */
export function AuditRatingForm({ detail, isSaving, onSubmit }: AuditRatingFormProps) {
  const existing = detail.existing_rating;
  const form = useForm<FormValues>({
    mode: "onChange",
    defaultValues: {
      source_relevance: existing?.source_relevance,
      support_sufficiency: existing?.support_sufficiency,
      faithfulness: existing?.faithfulness,
      scope_correctness: existing?.scope_correctness,
      recommendation: "",
    },
  });
  const values = useWatch({ control: form.control });
  const complete =
    isScore(values.source_relevance) &&
    isScore(values.support_sufficiency) &&
    isScore(values.faithfulness) &&
    isScore(values.scope_correctness);

  return (
    <form
      className="space-y-3"
      onSubmit={form.handleSubmit(async (entered) => {
        if (!complete) {
          return;
        }
        const recommendation = entered.recommendation.trim();
        await onSubmit({
          source_relevance: Number(entered.source_relevance),
          support_sufficiency: Number(entered.support_sufficiency),
          faithfulness: Number(entered.faithfulness),
          scope_correctness: Number(entered.scope_correctness),
          notes: recommendation ? { recommendation } : null,
        });
      })}
    >
      {detail.criteria.map((criterion) => (
        <Controller
          key={criterion.criterion_id}
          control={form.control}
          name={criterion.criterion_id as keyof FormValues}
          render={({ field }) => (
            <CompactScoreField
              description={criterion.description}
              label={criterion.label}
              onChange={(nextValue) => field.onChange(Number(nextValue))}
              options={SCORE_OPTIONS}
              value={typeof field.value === "number" ? field.value : undefined}
            />
          )}
        />
      ))}

      <textarea
        className="min-h-20 w-full rounded-none border border-[color:var(--line)] bg-white px-3 py-2 text-sm text-[color:var(--ink)] outline-none transition focus:border-[color:var(--accent)]"
        placeholder="Optional recommendation (e.g. how to improve the excerpt)"
        {...form.register("recommendation")}
      />

      <div className="flex items-center justify-between gap-3">
        <p className="text-xs text-[color:var(--muted)]">
          {complete ? "Ready to save." : "Score all four criteria to save."}
        </p>
        <Button disabled={!complete} isLoading={isSaving} size="sm" type="submit">
          {existing ? "Update audit" : "Save audit"}
        </Button>
      </div>
    </form>
  );
}
