import { ReactNode } from "react";
import { Link } from "@/shared/router";

/** One action card on a role-specific research home. */
export type LandingCard = {
  href: string;
  label: string;
  body: string;
};

type RoleLandingProps = {
  /** Eyebrow text — shows the role context, e.g. ``Teacher``. */
  eyebrow: string;
  /** H1, e.g. ``Welcome back, Aunty Blessing``. */
  title: string;
  /** One-line copy below the title. */
  lede: string;
  cards: LandingCard[];
  /** Optional content rendered between the header and the card grid (e.g. a
   *  "needs your attention" preview). */
  topContent?: ReactNode;
};

/** Shared layout for the non-researcher role homes — a header + a card grid. */
export function RoleLanding({ eyebrow, title, lede, cards, topContent }: RoleLandingProps) {
  return (
    <main className="flex w-full flex-col gap-8 py-8">
      <header className="space-y-2">
        <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[color:var(--accent)]">
          {eyebrow}
        </div>
        <h1 className="text-3xl font-semibold tracking-tight text-(--ink)">{title}</h1>
        <p className="max-w-2xl text-sm leading-relaxed text-(--muted)">{lede}</p>
      </header>

      {topContent}

      <ul className="grid gap-3 md:grid-cols-2">
        {cards.map((card) => (
          <li key={card.href}>
            <Link
              href={card.href}
              className="block h-full border border-(--line) bg-(--surface) p-5 transition hover:border-[color:var(--accent)]"
            >
              <p className="text-base font-semibold text-(--ink)">{card.label}</p>
              <p className="mt-1 text-sm text-(--muted)">{card.body}</p>
            </Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
