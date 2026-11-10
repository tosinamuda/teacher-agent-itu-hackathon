import { useMutation } from "@tanstack/react-query";

import { Button } from "@/shared/components/ui/Button";
import { saveBlob } from "@/shared/lib/saveBlob";

import { downloadContentFile } from "../api/content";

/** Saves the file the content's plugin makes of it, such as a slide deck as PowerPoint. */
export function DownloadFileButton({ contentId }: { contentId: string }) {
  const download = useMutation({
    mutationFn: () => downloadContentFile(contentId),
    onSuccess: ({ blob, filename }) => saveBlob(blob, filename),
  });

  return (
    <>
      <Button
        size="sm"
        variant="outline"
        disabled={download.isPending}
        onClick={() => download.mutate()}
      >
        {download.isPending ? "Preparing file…" : "Download file"}
      </Button>
      {download.isError ? (
        <span role="alert" className="text-xs text-(--danger-ink)">
          The file could not be prepared. Try again.
        </span>
      ) : null}
    </>
  );
}
