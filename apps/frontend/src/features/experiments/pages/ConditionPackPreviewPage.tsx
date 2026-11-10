import { Link, usePathname, useRouter, useSearchParams } from "@/shared/router";

import { Choices } from "@/shared/components/ui/Choices";
import { Card } from "@/shared/components/ui/Card";
import { Part1Review } from "@/features/study-review/Part1Review";
import { usePackManifest } from "@/features/study-review/usePackManifest";

import { JourneyPack } from "../components/JourneyPack";
import { useDownloadPackPdf } from "../hooks/useDownloadLessonPlanPdf";
import { useExperiment } from "../hooks/useExperiments";

const VALID_CODES = new Set(["c0", "c1", "c2", "c3"]);

/**
 * Researcher-facing READ-ONLY preview of one H1 condition's review pack
 * (C0–C3). Walks the experiment's executions, offers every succeeded run of
 * the condition (a study's draws; `?draw=N`, else the latest), and renders the chosen
 * pack via `JourneyPack` with whatever the study's raters recorded about it. The raw `artefact_id` is shown small in the header for
 * cross-reference with logs / the replay surface.
 */
export function ConditionPackPreviewPage({
  experimentId,
  conditionCode,
}: {
  experimentId: string;
  conditionCode: string;
}) {
  const normalised = conditionCode.toLowerCase();
  const experimentQuery = useExperiment(experimentId);
  const experiment = experimentQuery.data;
  const downloadPdf = useDownloadPackPdf();
  // Every succeeded run of this condition, one per H1 execution (a study's draws), oldest first.
  const draws = (experiment?.executions ?? [])
    .filter((execution) => execution.hypothesis === "H1")
    .sort((a, b) => a.attempt_number - b.attempt_number)
    .flatMap((execution) =>
      (execution.condition_runs ?? [])
        .filter(
          (run) =>
            run.condition_code.toLowerCase() === normalised &&
            /succeed|complete|done/i.test(run.status) &&
            Boolean(run.artefact_id),
        )
        .map((run) => ({
          attempt: execution.attempt_number,
          artefactId: run.artefact_id as string,
        })),
    );
  const router = useRouter();
  const pathname = usePathname();
  const requested = Number(useSearchParams().get("draw"));
  const draw = draws.find((each) => each.attempt === requested) ?? draws[draws.length - 1];
  const artefactId = draw?.artefactId;

  const manifestQuery = usePackManifest(artefactId);

  if (!VALID_CODES.has(normalised)) {
    return (
      <main className="w-full py-4">
        <Card padding="lg" className="space-y-2">
          <h1 className="text-xl font-semibold text-(--ink)">Unknown condition</h1>
          <p className="text-sm text-(--muted)">
            <code>{conditionCode}</code> is not one of the H1 conditions (C0, C1, C2, C3).
          </p>
        </Card>
      </main>
    );
  }

  if (experimentQuery.isLoading) {
    return (
      <main className="w-full py-4">
        <Card padding="lg">
          <p className="text-sm text-(--muted)">Loading experiment…</p>
        </Card>
      </main>
    );
  }

  if (!experiment) {
    return (
      <main className="w-full py-4">
        <Card padding="lg">
          <p className="text-sm text-(--muted)">Experiment not found.</p>
        </Card>
      </main>
    );
  }

  if (!artefactId) {
    return (
      <main className="w-full py-4">
        <Card padding="lg" className="space-y-2">
          <h1 className="text-xl font-semibold text-(--ink)">
            {normalised.toUpperCase()} hasn&apos;t been generated yet
          </h1>
          <p className="text-sm text-(--muted)">
            No succeeded condition run for {normalised.toUpperCase()} in this experiment&apos;s
            executions.
          </p>
          <Link
            className="text-sm font-semibold text-(--accent-deep) hover:underline"
            href={`/research/experiments/${experimentId}/run`}
          >
            Open Test tab to trigger a run →
          </Link>
        </Card>
      </main>
    );
  }

  if (manifestQuery.isLoading) {
    return (
      <main className="w-full py-4">
        <Card padding="lg">
          <p className="text-sm text-(--muted)">Loading {normalised.toUpperCase()} pack…</p>
        </Card>
      </main>
    );
  }

  if (manifestQuery.isError || !manifestQuery.data) {
    return (
      <main className="w-full py-4">
        <Card padding="lg" className="space-y-2">
          <h1 className="text-xl font-semibold text-(--ink)">
            Couldn&apos;t load {normalised.toUpperCase()} pack
          </h1>
          <p className="text-sm text-(--muted)">Artefact: {artefactId}</p>
        </Card>
      </main>
    );
  }

  const code = normalised.toUpperCase();
  return (
    <main className="flex w-full flex-col gap-8 py-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-4">
          <h2 className="text-lg font-semibold text-(--ink)" title={artefactId}>
            {code} · class revision note
          </h2>
          {draws.length > 1 ? (
            <div className="flex items-center gap-2" role="group" aria-label="Draw">
              <span className="text-sm text-(--muted)">Draw</span>
              <Choices
                options={draws.map((each) => ({
                  value: String(each.attempt),
                  label: String(each.attempt),
                }))}
                value={String(draw?.attempt)}
                onChange={(attempt) => router.replace(`${pathname}?draw=${attempt}`)}
              />
            </div>
          ) : null}
        </div>
        <button
          type="button"
          disabled={downloadPdf.isPending}
          onClick={() => downloadPdf.mutate(artefactId)}
          className="text-sm text-(--muted) hover:text-(--ink) disabled:opacity-60"
        >
          {downloadPdf.isPending ? "Exporting…" : "PDF"}
        </button>
      </div>

      {experiment.plan_version_id ? (
        <Part1Review planVersionId={experiment.plan_version_id} noteId={artefactId} />
      ) : (
        <Card padding="lg">
          <JourneyPack manifest={manifestQuery.data} />
        </Card>
      )}
    </main>
  );
}
