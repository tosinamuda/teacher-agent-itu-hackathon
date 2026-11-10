import { useMyQueue } from "@/features/evaluation/hooks/useMyQueue";

import { LandingCard, RoleLanding } from "../components/RoleLanding";

// Rater-facing task wording only — no hypothesis ids, condition codes (C0–C3 /
// P0–P1), or base/personalised roles: those would unblind the study design.
const H1_CARD = {
  href: "/research/rater/h1",
  label: "Revision-note reviews",
  body: "Rate each candidate revision note against its lesson plan.",
};
const H2_CARD = {
  href: "/research/rater/h2",
  label: "Learner comparisons",
  body: "Rate the candidate revision notes prepared for each focal learner.",
};
const AUDIT_CARD = {
  href: "/research/rater/audit",
  label: "Source-grounding audit",
  body: "Score the per-excerpt source-fidelity claims.",
};

/** Rater home — queues appear only when there are assignments.
 *
 *  Calls ``/evaluation/my-queue``; reads the actor-bound rater profile and
 *  groups assignments by hypothesis. A queue card only renders if its array
 *  is non-empty, with the assignment count on it; a rater with nothing
 *  assigned sees the empty state instead of static cards that go nowhere.
 */
export function RaterHome({ greeting }: { greeting: string }) {
  const { data: queue, isLoading } = useMyQueue(true);

  if (isLoading) {
    return (
      <main className="py-10 text-sm text-(--muted)">Loading your assignments…</main>
    );
  }

  const cards: LandingCard[] = [];
  if (queue && queue.h1.length > 0) {
    cards.push({
      ...H1_CARD,
      body: `${queue.h1.length} lesson${queue.h1.length === 1 ? "" : "s"} assigned · ${H1_CARD.body}`,
    });
  }
  if (queue && queue.h2.length > 0) {
    cards.push({
      ...H2_CARD,
      body: `${queue.h2.length} focal learner${queue.h2.length === 1 ? "" : "s"} assigned · ${H2_CARD.body}`,
    });
  }
  if (queue && queue.audit.length > 0) {
    const auditCount = queue.audit.length;
    const adjudicatorCount = queue.audit.filter((line) => line.is_adjudicator).length;
    const detail =
      adjudicatorCount > 0
        ? `${auditCount} item${auditCount === 1 ? "" : "s"} (${adjudicatorCount} as adjudicator) · ${AUDIT_CARD.body}`
        : `${auditCount} item${auditCount === 1 ? "" : "s"} assigned · ${AUDIT_CARD.body}`;
    cards.push({ ...AUDIT_CARD, body: detail });
  }

  if (cards.length === 0) {
    return (
      <main className="flex w-full flex-col gap-8 py-8">
        <header className="space-y-2">
          <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[color:var(--accent)]">
            Rater
          </div>
          <h1 className="text-3xl font-semibold tracking-tight text-(--ink)">
            Welcome, {greeting}
          </h1>
          <p className="max-w-2xl text-sm leading-relaxed text-(--muted)">
            You have no assignments yet. A researcher will allocate lessons, focal
            learners, or source-audit items to you; once that&apos;s done, the relevant
            queues will appear here.
          </p>
        </header>
      </main>
    );
  }

  return (
    <RoleLanding
      eyebrow="Rater"
      title={`Welcome, ${greeting}`}
      lede="Your assigned review work."
      cards={cards}
    />
  );
}
