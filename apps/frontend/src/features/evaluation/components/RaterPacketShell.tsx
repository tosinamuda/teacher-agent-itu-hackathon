import { Link } from "@/shared/router";
import { ReactNode, useEffect, useState } from "react";

type RaterPacketShellProps = {
  hypothesis: "H1" | "H2";
  packetCode: string;
  packetPosition: number | null;
  queueLength: number;
  backHref: string;
  drawerContent: ReactNode;
  children: ReactNode;
};

const laneLabel = {
  H1: "Lesson match",
  H2: "Learner comparison",
} as const;

// Short rater-facing badge for the compact sidebar. The thesis labels
// (`H1` / `H2`) are not surfaced to raters; the badge picks up the lane name.
const laneBadge = {
  H1: "MATCH",
  H2: "COMPARE",
} as const;

/** Wraps packet-detail pages in a compact app shell with a collapsible drawer. */
export function RaterPacketShell({
  hypothesis,
  packetCode,
  packetPosition,
  queueLength,
  backHref,
  drawerContent,
  children,
}: RaterPacketShellProps) {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setIsDrawerOpen(false);
      }
    };

    window.addEventListener("keydown", handleEscape);
    return () => window.removeEventListener("keydown", handleEscape);
  }, []);

  return (
    <div className="min-h-screen bg-(--bg) min-[1200px]:h-screen min-[1200px]:overflow-hidden">
      <div className="min-h-screen min-[1200px]:flex min-[1200px]:h-full min-[1200px]:overflow-hidden">
        <aside className="hidden min-[1200px]:flex min-[1200px]:h-full">
          <div className="flex w-16 shrink-0 flex-col items-center justify-between border-r border-[color:var(--line)] bg-(--surface) py-4 backdrop-blur">
            <div className="flex flex-col items-center gap-3">
              <button
                aria-expanded={isDrawerOpen}
                aria-label={isDrawerOpen ? "Close revision-note details" : "Open revision-note details"}
                className="inline-flex h-11 w-11 items-center justify-center rounded-2xl border border-[color:var(--line)] bg-white text-lg font-semibold text-[color:var(--ink)] transition hover:border-[color:var(--accent)]"
                onClick={() => setIsDrawerOpen((current) => !current)}
                type="button"
              >
                ≡
              </button>
              <Link
                className="inline-flex h-11 w-11 items-center justify-center rounded-2xl border border-[color:var(--line)] bg-white text-lg font-semibold text-[color:var(--ink)] transition hover:border-[color:var(--accent)]"
                href={backHref}
              >
                ←
              </Link>
            </div>

            <div className="space-y-2 text-center">
              <span className="inline-flex rounded-none border border-[color:var(--line)] bg-white px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.18em] text-[color:var(--muted)]">
                {laneBadge[hypothesis]}
              </span>
              {packetPosition !== null ? (
                <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-[color:var(--muted)]">
                  {packetPosition}/{queueLength}
                </p>
              ) : null}
            </div>
          </div>

          <div
            className={`overflow-hidden border-r border-[color:var(--line)] bg-(--surface) backdrop-blur transition-[width,opacity] duration-200 ${
              isDrawerOpen ? "w-[320px] opacity-100" : "w-0 opacity-0"
            }`}
          >
            <div className="flex h-full w-[320px] flex-col overflow-y-auto px-5 py-5">
              <div className="space-y-2 border-b border-[color:var(--line)] pb-4">
                <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[color:var(--muted)]">
                  {laneLabel[hypothesis]}
                </p>
                {packetPosition !== null ? (
                  <p className="text-sm font-semibold text-[color:var(--ink)]">
                    Revision note {packetPosition} of {queueLength}
                  </p>
                ) : null}
                <p className="text-sm text-[color:var(--muted)]">{packetCode}</p>
              </div>

              <div className="flex-1 py-5">{drawerContent}</div>

              <div className="space-y-3 border-t border-[color:var(--line)] pt-4">
                <Link
                  className="inline-flex w-full items-center justify-center rounded-none border border-[color:var(--line)] px-4 py-2 text-sm font-semibold text-[color:var(--ink)] transition hover:border-[color:var(--accent)]"
                  href={backHref}
                >
                  Back to queue
                </Link>
              </div>
            </div>
          </div>
        </aside>

        <div className="flex min-w-0 flex-1 flex-col min-[1200px]:h-screen min-[1200px]:overflow-hidden">
          <div className="flex items-center justify-between border-b border-[color:var(--line)] bg-(--surface) px-4 py-3 backdrop-blur min-[1200px]:hidden">
            <button
              aria-expanded={isDrawerOpen}
              className="inline-flex items-center rounded-none border border-[color:var(--line)] px-4 py-2 text-sm font-semibold text-[color:var(--ink)]"
              onClick={() => setIsDrawerOpen(true)}
              type="button"
            >
              Menu
            </button>
            <span className="text-sm font-semibold text-[color:var(--muted)]">
              {laneLabel[hypothesis]}
            </span>
            <Link
              className="inline-flex items-center rounded-none border border-[color:var(--line)] px-4 py-2 text-sm font-semibold text-[color:var(--ink)]"
              href={backHref}
            >
              Queue
            </Link>
          </div>

          {isDrawerOpen ? (
            <div className="fixed inset-0 z-30 bg-black/30 min-[1200px]:hidden">
              <button
                aria-label="Close revision-note details"
                className="absolute inset-0"
                onClick={() => setIsDrawerOpen(false)}
                type="button"
              />
              <div className="relative h-full w-[320px] overflow-y-auto border-r border-[color:var(--line)] bg-white px-5 py-5">
                <div className="space-y-2 border-b border-[color:var(--line)] pb-4">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[color:var(--muted)]">
                    {laneLabel[hypothesis]}
                  </p>
                  {packetPosition !== null ? (
                    <p className="text-sm font-semibold text-[color:var(--ink)]">
                      Revision note {packetPosition} of {queueLength}
                    </p>
                  ) : null}
                  <p className="text-sm text-[color:var(--muted)]">{packetCode}</p>
                </div>
                <div className="py-5">{drawerContent}</div>
                <div className="space-y-3 border-t border-[color:var(--line)] pt-4">
                  <Link
                    className="inline-flex w-full items-center justify-center rounded-none border border-[color:var(--line)] px-4 py-2 text-sm font-semibold text-[color:var(--ink)] transition hover:border-[color:var(--accent)]"
                    href={backHref}
                    onClick={() => setIsDrawerOpen(false)}
                  >
                    Back to queue
                  </Link>
                </div>
              </div>
            </div>
          ) : null}

          <div className="min-h-0 flex-1">{children}</div>
        </div>
      </div>
    </div>
  );
}
