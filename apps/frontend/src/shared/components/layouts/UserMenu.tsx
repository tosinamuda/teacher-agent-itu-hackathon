import { useEffect, useRef, useState } from "react";

import type { AuthMe } from "@/shared/api/auth";
import { Link } from "@/shared/router";

type UserMenuProps = {
  actor: AuthMe;
  onSignOut: () => void;
  /** `avatar` is the initials alone, opening downward. `row` is a sidebar row of avatar and name, opening upward. */
  variant?: "avatar" | "row";
  /** Where the settings gear beside a row goes; no gear without it. */
  settingsHref?: string;
};

/** First letter of each word in the source name, max two, uppercased. */
function initialsFrom(actor: AuthMe): string {
  const source = actor.full_name ?? actor.email ?? actor.auth_id;
  const letters = source
    .split(/[\s@._-]+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((segment) => segment[0]?.toUpperCase() ?? "")
    .join("");
  return letters || "?";
}

/**
 * Account menu: a circular avatar with the actor's initials, opened to reveal
 * full name, email, role badge and Sign out. Closes on outside click or
 * Escape. The same shape any productised app uses for the identity strip —
 * preserves header space for navigation rather than spelling identity inline.
 */
export function UserMenu({
  actor,
  onSignOut,
  variant = "avatar",
  settingsHref,
}: UserMenuProps) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const onMouseDown = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setOpen(false);
      }
    };
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") setOpen(false);
    };
    document.addEventListener("mousedown", onMouseDown);
    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("mousedown", onMouseDown);
      document.removeEventListener("keydown", onKeyDown);
    };
  }, [open]);

  const initials = initialsFrom(actor);
  const displayName = actor.full_name ?? actor.email ?? actor.auth_id;
  const subline = actor.full_name ? actor.email : null;

  const asRow = variant === "row";
  return (
    <div
      ref={ref}
      className={asRow ? "relative flex w-full items-center" : "relative"}
    >
      <button
        type="button"
        aria-haspopup="menu"
        aria-expanded={open}
        aria-label={`Account menu — ${displayName}`}
        onClick={() => setOpen((value) => !value)}
        className={
          asRow
            ? "flex min-w-0 flex-1 items-center gap-3 px-4 py-3 text-left text-sm font-semibold text-(--ink) hover:bg-(--line)"
            : `flex h-9 w-9 items-center justify-center border bg-(--surface) text-xs font-semibold uppercase tracking-[0.06em] transition ${
                open
                  ? "border-(--accent) text-(--accent)"
                  : "border-(--line-2) text-(--ink-2) hover:border-(--accent) hover:text-(--ink)"
              }`
        }
      >
        {asRow ? (
          <>
            <span className="flex size-8 shrink-0 items-center justify-center bg-(--ink) text-[11px] font-semibold uppercase text-white">
              {initials}
            </span>
            <span className="flex-1 truncate">{displayName}</span>
            {settingsHref ? null : (
              <span aria-hidden="true" className="text-(--ink-2)">
                ···
              </span>
            )}
          </>
        ) : (
          initials
        )}
      </button>
      {asRow && settingsHref ? (
        <Link
          href={settingsHref}
          aria-label="Settings"
          className="flex shrink-0 items-center px-4 py-3 text-(--ink-2) hover:bg-(--line) hover:text-(--ink)"
        >
          <svg
            viewBox="0 0 24 24"
            width="20"
            height="20"
            aria-hidden="true"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.6"
          >
            <circle cx="12" cy="12" r="3" />
            <path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z" />
          </svg>
        </Link>
      ) : null}
      {open ? (
        <div
          role="menu"
          className={`absolute z-30 w-72 border border-(--line) bg-(--surface) ${
            asRow
              ? "bottom-[calc(100%+4px)] left-2"
              : "right-0 top-[calc(100%+8px)]"
          }`}
        >
          <div className="space-y-1.5 border-b border-(--line) p-4">
            <p
              className="text-sm font-semibold text-(--ink)"
              title={displayName}
            >
              {displayName}
            </p>
            {subline ? (
              <p
                className="truncate text-xs text-(--muted)"
                title={subline ?? undefined}
              >
                {subline}
              </p>
            ) : null}
            <span className="inline-flex border border-(--line-2) bg-(--surface) px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.08em] text-(--ink)">
              {actor.role}
            </span>
          </div>
          <button
            type="button"
            role="menuitem"
            onClick={() => {
              onSignOut();
              setOpen(false);
            }}
            className="block w-full p-3 text-left text-sm text-(--ink-2) transition hover:bg-(--sunken) hover:text-(--ink)"
          >
            Sign out
          </button>
        </div>
      ) : null}
    </div>
  );
}
