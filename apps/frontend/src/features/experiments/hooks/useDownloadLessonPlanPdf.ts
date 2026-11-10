import { useMutation } from "@tanstack/react-query";

import { saveBlob } from "@/shared/lib/saveBlob";

import { downloadLessonPlanPdf, downloadPackPdf } from "../lib/api";

/**
 * Downloads the lesson plan as a WeasyPrint PDF and saves it locally.
 * Same render pipeline as the H1/H2/audit pack exports.
 */
export const useDownloadLessonPlanPdf = (planVersionId: string | null | undefined) =>
  useMutation({
    mutationFn: async () => downloadLessonPlanPdf(planVersionId ?? ""),
    onSuccess: ({ blob, filename }) => saveBlob(blob, filename),
  });

/** Downloads one review pack (C0–C4 / P0–P1) as a PDF and saves it locally. */
export const useDownloadPackPdf = () =>
  useMutation({
    mutationFn: (artefactId: string) => downloadPackPdf(artefactId),
    onSuccess: ({ blob, filename }) => saveBlob(blob, filename),
  });
