import { Link } from "@/shared/router";

import { Button } from "@/shared/components/ui/Button";

import { PackManifestPreview } from "../components/PackManifestPreview";
import { usePackReview } from "../hooks/usePackReview";

const BACK_HREF = "/research/teacher/lesson-preview";

/**
 * Read-only teacher preview of one compiled lesson's revision note. Renders the
 * same clean sectioned reader the review queue uses (PackManifestPreview →
 * ReviewNoteSections), without the approve / revision controls — so the teacher
 * sees exactly what a student would, before personalising.
 */
export default function LessonPreviewPage({
  artefactId,
}: {
  artefactId: string;
}) {
  const { pack, isLoading, isError } = usePackReview(artefactId);

  if (isLoading) {
    return (
      <p className="p-8 text-sm text-(--muted)">Loading lesson preview…</p>
    );
  }
  if (isError || !pack) {
    return (
      <main className="mx-auto max-w-[40rem] p-8 text-center">
        <h1 className="text-xl font-semibold text-(--ink)">
          Lesson preview not found
        </h1>
        <Link href={BACK_HREF} className="mt-4 inline-block">
          <Button variant="ghost">Back to lesson preview</Button>
        </Link>
      </main>
    );
  }

  return (
    <main className="mx-auto w-full max-w-[48rem] p-6 md:p-8">
      <header className="mb-6 flex items-center justify-between gap-3">
        <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent-deep)">
          Phase 2 · Lesson preview
        </p>
        <Link href={BACK_HREF}>
          <Button variant="ghost" size="sm">
            Back to lessons
          </Button>
        </Link>
      </header>

      <PackManifestPreview manifest={pack.manifest} />
    </main>
  );
}
