import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";

import { Button } from "@/shared/components/ui/Button";

import { importRatings } from "../lib/api";
import { RatingImportResult, RatingImportRow } from "../lib/experiments";

type FormValues = { payload: string };

const PLACEHOLDER = `[
  {"packet_code": "PKT-...", "rater_name": "Rater A", "overall_score": 3.5},
  {"packet_code": "PKT-...", "rater_name": "Rater B", "overall_score": 4}
]`;

/**
 * Research-manager action: paste a JSON array of offline ratings (packet_code +
 * rater_name + overall_score) to bulk-import them — e.g. ratings collected on paper
 * or in a spreadsheet. Imported ratings flow straight into the results dashboards.
 */
export function OfflineRatingImport() {
  const queryClient = useQueryClient();
  const { register, handleSubmit } = useForm<FormValues>({ defaultValues: { payload: "" } });
  const [parseError, setParseError] = useState<string | null>(null);
  const [result, setResult] = useState<RatingImportResult | null>(null);

  const mutation = useMutation({
    mutationFn: (rows: RatingImportRow[]) => importRatings(rows),
    onSuccess: (data) => {
      setResult(data);
      void queryClient.invalidateQueries({ queryKey: ["experimentRatings"] });
      void queryClient.invalidateQueries({ queryKey: ["investigationResults"] });
    },
  });

  const submit = handleSubmit((values) => {
    setParseError(null);
    setResult(null);
    let rows: RatingImportRow[];
    try {
      const parsed = JSON.parse(values.payload);
      rows = Array.isArray(parsed) ? parsed : parsed.ratings;
      if (!Array.isArray(rows)) throw new Error("Expected an array of rating rows.");
    } catch (error) {
      setParseError(error instanceof Error ? error.message : "Invalid JSON.");
      return;
    }
    mutation.mutate(rows);
  });

  return (
    <details className="rounded-2xl border border-(--line) bg-(--surface) p-5">
      <summary className="cursor-pointer text-base font-semibold text-(--ink)">
        Import offline ratings
      </summary>
      <p className="mt-2 text-xs text-(--muted)">
        Paste a JSON array of {`{packet_code, rater_name, overall_score}`} rows.
      </p>
      <textarea
        {...register("payload")}
        rows={6}
        placeholder={PLACEHOLDER}
        className="mt-3 w-full rounded-lg border border-(--line) p-2 font-mono text-xs outline-none focus:border-accent-deep"
      />
      <div className="mt-2 flex items-center justify-between gap-3">
        <div className="text-xs">
          {parseError ? <span className="text-(--danger)">{parseError}</span> : null}
          {result ? (
            <span className="text-(--muted)">
              Imported {result.imported}, updated {result.updated}, skipped {result.skipped}
              {result.errors.length ? ` · ${result.errors.length} error(s)` : ""}
            </span>
          ) : null}
        </div>
        <Button size="sm" onClick={submit} isLoading={mutation.isPending}>
          Import ratings
        </Button>
      </div>
      {result && result.errors.length ? (
        <ul className="mt-2 max-h-32 space-y-0.5 overflow-auto text-xs text-(--danger)">
          {result.errors.map((error) => (
            <li key={error}>{error}</li>
          ))}
        </ul>
      ) : null}
    </details>
  );
}
