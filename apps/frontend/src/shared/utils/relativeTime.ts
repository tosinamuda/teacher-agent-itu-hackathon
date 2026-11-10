const OFFSET = /(?:Z|[+-]\d{2}:?\d{2})$/i;

/** Milliseconds since the epoch; the database keeps every moment in UTC, so a time sent without an offset is UTC. */
export function parseApiMoment(iso: string): number {
  return Date.parse(iso.includes("T") && !OFFSET.test(iso) ? `${iso}Z` : iso);
}

/** "3 min ago", "2 hr ago", "4 days ago"; a date after a month. */
export function formatRelativeTime(
  iso: string | null | undefined,
  now: number = Date.now(),
): string | undefined {
  if (!iso) return undefined;
  const ts = parseApiMoment(iso);
  if (Number.isNaN(ts)) return undefined;
  const deltaSec = Math.floor((now - ts) / 1000);
  if (deltaSec < 60) return "just now";
  if (deltaSec < 3600) return `${Math.floor(deltaSec / 60)} min ago`;
  if (deltaSec < 86400) return `${Math.floor(deltaSec / 3600)} hr ago`;
  const days = Math.floor(deltaSec / 86400);
  if (days < 30) return `${days} day${days === 1 ? "" : "s"} ago`;
  return new Date(ts).toLocaleDateString();
}
