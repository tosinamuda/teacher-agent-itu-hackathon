import { useState } from "react";
import { useMutation } from "@tanstack/react-query";

import { errorDetail } from "@/shared/api/errors";
import { runJob } from "@/shared/api/jobs";
import { Button, buttonClass } from "@/shared/components/ui/Button";
import { Link } from "@/shared/router";

import {
  ImportedPlan,
  READABLE_DOCUMENTS,
  importPlanFromDocument,
} from "../api/importPlan";

const LABEL =
  "text-[11px] font-semibold uppercase tracking-[0.12em] text-(--faint)";

/**
 * Write the plan from the teacher's own document instead of entering it by hand. The app
 * turns it into a draft plan that passes every check; the teacher then reads it.
 */
export function ImportFromDocument({
  sessionId,
  experimentId,
  onImported,
  cancelHref,
}: {
  sessionId: string;
  experimentId?: string;
  onImported: (plan: ImportedPlan) => void;
  cancelHref?: string;
}) {
  const [text, setText] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const importing = useMutation({
    mutationFn: () =>
      runJob<ImportedPlan>(() =>
        importPlanFromDocument(
          sessionId,
          { text: text.trim() || undefined, file: file ?? undefined },
          experimentId,
        ),
      ),
    onSuccess: onImported,
  });
  const ready = Boolean(text.trim() || file);

  return (
    <section className="flex flex-col gap-4">
      <div className="flex flex-col gap-4 border border-(--line) bg-(--surface) p-4">
        <label className="flex flex-col gap-2">
          <span className={LABEL}>Paste the plan</span>
          <textarea
            className="min-h-36 w-full border border-(--line-2) bg-(--surface) p-3 text-sm text-(--ink) outline-none focus:border-(--accent)"
            placeholder="Paste the teacher's plan here"
            value={text}
            onChange={(event) => setText(event.target.value)}
            disabled={importing.isPending}
          />
        </label>
        <label className="flex flex-col gap-2">
          <span className={LABEL}>Or upload a file</span>
          <input
            type="file"
            accept={READABLE_DOCUMENTS}
            aria-label="The plan's file"
            className="text-sm text-(--ink-2)"
            disabled={importing.isPending}
            onChange={(event) => setFile(event.target.files?.[0] ?? null)}
          />
          <span className="text-xs text-(--faint)">
            {READABLE_DOCUMENTS.replaceAll(",", "  ")}
          </span>
        </label>
      </div>
      <div className="flex flex-wrap items-center gap-3">
        <Button
          isLoading={importing.isPending}
          disabled={!ready}
          onClick={() => importing.mutate()}
        >
          {importing.isPending ? "Writing the plan…" : "Import the plan"}
        </Button>
        {cancelHref ? (
          <Link href={cancelHref} className={buttonClass({ variant: "ghost" })}>
            Cancel
          </Link>
        ) : null}
        {importing.isError ? (
          <span role="alert" className="text-xs text-(--danger-ink)">
            {errorDetail(importing.error, "Could not import the plan.")}
          </span>
        ) : null}
      </div>
    </section>
  );
}
