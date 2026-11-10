import { useEffect, useRef, useState } from "react";

import { uploadAttachment } from "@/shared/api/attachments";

/**
 * Optional image attachment: pick a photo of the original (a marked answer sheet
 * or a paper lesson plan), upload it, and hold its opaque id. Provenance only —
 * never required. Shows a local preview after selection.
 */
export function AttachmentField({
  value,
  kind,
  label,
  onChange,
}: {
  value: string | null;
  kind: string;
  label: string;
  onChange: (attachmentId: string | null) => void;
}) {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  const onSelect = async (file: File | undefined) => {
    if (!file) return;
    setError(null);
    setUploading(true);
    try {
      const result = await uploadAttachment(file, kind);
      if (previewUrl) URL.revokeObjectURL(previewUrl);
      setPreviewUrl(URL.createObjectURL(file));
      onChange(result.attachment_id);
    } catch (err) {
      setError((err as Error).message || "Upload failed.");
    } finally {
      setUploading(false);
    }
  };

  const clear = () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(null);
    onChange(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  return (
    <div className="space-y-2">
      <span className="text-[11px] font-semibold uppercase tracking-[0.14em] text-(--muted)">
        {label}
      </span>
      {previewUrl ? (
        <div className="flex items-start gap-3">
          <img
            src={previewUrl}
            alt="Attached original"
            className="max-h-32 rounded-sm border border-(--line-2)"
          />
          <button
            type="button"
            onClick={clear}
            className="text-xs text-(--muted) hover:text-(--danger)"
          >
            Remove
          </button>
        </div>
      ) : (
        <input
          ref={inputRef}
          type="file"
          accept="image/png,image/jpeg,image/webp,image/gif"
          disabled={uploading}
          onChange={(event) => void onSelect(event.target.files?.[0])}
          className="block text-sm text-(--ink-2) file:mr-3 file:border file:border-(--line-2) file:bg-(--surface-2) file:px-3 file:py-1 file:text-xs file:font-semibold"
        />
      )}
      {uploading ? <p className="text-xs text-(--muted)">Uploading…</p> : null}
      {value && !uploading ? <p className="text-xs text-(--accent-deep)">Attached ✓</p> : null}
      {error ? <p className="text-xs text-(--danger-ink)">{error}</p> : null}
    </div>
  );
}
