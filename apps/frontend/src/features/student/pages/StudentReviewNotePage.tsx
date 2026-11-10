import { useState } from "react";
import { useSearchParams, useRouter } from "@/shared/router";
import { Link } from "@/shared/router";

import { Button } from "@/shared/components/ui/Button";
import { saveBlob } from "@/shared/lib/saveBlob";
import { ReviewNoteReader } from "@/shared/components/renderer/ReviewNoteReader";

import { ReviewNoteInsight } from "@/features/student/components/ReviewNoteInsight";
import { useReviewNote } from "@/features/student/hooks/useReviewNote";
import { ReviewNoteManifest, fetchReviewNotePdf } from "@/features/student/api/reviewNote";
import { normaliseBand } from "@/features/student/services/reviewNoteBand";

/** Header line for a revision note: subject · class · week · sections. */
function noteMeta(manifest: ReviewNoteManifest): string {
  return [
    manifest.subject,
    manifest.grade,
    manifest.week ? `Week ${manifest.week}` : null,
    `${manifest.steps.length} section${manifest.steps.length === 1 ? "" : "s"}`,
  ]
    .filter(Boolean)
    .join(" · ");
}

/**
 * A student's personalised revision note. Shows the lesson context, then the note
 * paged one section at a time — each section carrying its own "based on your
 * assessment" insight (the band it was pitched at). "Export to PDF" downloads
 * the server-rendered PDF (the same WeasyPrint template as the C0–C4 packs).
 */
export function StudentReviewNotePage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const artefactId = searchParams.get("artefact_id");
  const { data: manifest, isLoading, isError } = useReviewNote(artefactId);
  const [downloading, setDownloading] = useState(false);
  const [downloadError, setDownloadError] = useState(false);

  if (!artefactId) {
    return <p className="mx-auto max-w-3xl px-6 py-8 text-sm text-(--muted)">No revision note selected.</p>;
  }
  if (isLoading) {
    return <p className="mx-auto max-w-3xl px-6 py-8 text-sm text-(--muted)">Loading your revision note…</p>;
  }
  if (isError || !manifest) {
    return (
      <p className="mx-auto max-w-3xl px-6 py-8 text-sm text-(--muted)">
        We couldn&rsquo;t load your revision note right now. Please refresh in a moment.
      </p>
    );
  }

  const lessonHref = `/research/student/lesson/${manifest.plan_version_id}`;

  const exportPdf = async () => {
    setDownloading(true);
    setDownloadError(false);
    try {
      const { blob, filename } = await fetchReviewNotePdf(artefactId);
      saveBlob(blob, filename);
    } catch {
      setDownloadError(true);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <main className="mx-auto flex w-full max-w-3xl flex-col gap-5 px-4 py-6 sm:px-6 sm:py-8">
      <div className="flex items-center justify-between gap-3">
        <Link href={lessonHref} className="text-sm text-(--accent-deep) hover:underline">
          ← Back to lesson
        </Link>
        <Button variant="outline" size="sm" onClick={exportPdf} isLoading={downloading}>
          {downloading ? "Preparing PDF…" : "Export to PDF"}
        </Button>
      </div>

      <header className="space-y-1">
        <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent-deep)">
          Revision note
        </p>
        <h1 className="text-2xl font-semibold text-(--ink)">
          {manifest.subtopic || manifest.topic || "Revision note"}
        </h1>
        <p className="text-sm text-(--muted)">{noteMeta(manifest)}</p>
      </header>

      {downloadError ? (
        <p className="text-sm text-(--danger-ink)">
          We couldn&rsquo;t generate the PDF just now. Please try again.
        </p>
      ) : null}

      <ReviewNoteReader
        sections={manifest.steps}
        onDone={() => router.push(lessonHref)}
        renderBandInsight={(band) => {
          const normalised = normaliseBand(band);
          return normalised ? <ReviewNoteInsight band={normalised} /> : null;
        }}
      />
    </main>
  );
}
