import { useQuery } from "@tanstack/react-query";
import { useState } from "react";

import { API_BASE_URL } from "@/shared/api/client";
import { figureId } from "@/shared/utils/figures";

/**
 * A teacher's TikZ drawing, drawn once on the server and fetched as a small SVG only when it
 * scrolls into view. Where it cannot be drawn, its caption stands in; its source never shows.
 */
export function TikzFigure({
  source,
  caption,
}: {
  source: string;
  caption?: string | null;
}) {
  const id = useQuery({
    queryKey: ["figure-id", source],
    queryFn: () => figureId(source),
    staleTime: Infinity,
  });
  const [failed, setFailed] = useState(false);
  if (failed || id.isError) {
    return (
      <p className="my-3 text-center text-sm italic text-(--muted)">
        {caption
          ? `Figure: ${caption}`
          : "A figure the teacher drew is not available here."}
      </p>
    );
  }
  return (
    <figure className="my-3 flex justify-center">
      {id.data ? (
        <img
          src={`${API_BASE_URL}/figures/${id.data}.svg`}
          alt={caption ?? "A figure the teacher drew"}
          loading="lazy"
          decoding="async"
          className="h-auto max-w-full"
          onError={() => setFailed(true)}
        />
      ) : (
        <div className="h-24 w-full max-w-sm animate-pulse rounded bg-(--sunken)" />
      )}
    </figure>
  );
}
