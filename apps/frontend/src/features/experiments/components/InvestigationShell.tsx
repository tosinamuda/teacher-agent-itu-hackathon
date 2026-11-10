import type { ReactNode } from "react";

import { Link, usePathname } from "@/shared/router";
import { TabBar } from "@/shared/components/ui/TabBar";

import { useEndInvestigation, useInvestigation } from "../hooks/useInvestigations";
import { EndStudyControl } from "./EndStudyControl";

const TABS = [
  { slug: "", label: "Overview" },
  { slug: "/results", label: "Results" },
];
/** An ended study can be walked through for an audience, on examples switched as it goes. */
const ENDED_TABS = [...TABS, { slug: "/walkthrough", label: "Walkthrough" }];

/**
 * One study's frame: the breadcrumb, its title, the end-study action while it runs, and its
 * tabs. Each tab is its own page beneath.
 */
export function InvestigationShell({
  investigationId,
  children,
}: {
  investigationId: string;
  children: ReactNode;
}) {
  const pathname = usePathname();
  const investigationQuery = useInvestigation(investigationId);
  const endStudy = useEndInvestigation(investigationId);
  const investigation = investigationQuery.data;
  const base = `/research/investigations/${investigationId}`;

  if (investigationQuery.isLoading) {
    return <p className="py-8 text-sm text-(--muted)">Loading…</p>;
  }
  if (investigationQuery.isError || !investigation) {
    return (
      <p className="py-8 text-sm text-(--muted)">
        Study not found.{" "}
        <Link href="/research" className="text-(--accent-deep) hover:underline">
          Studies
        </Link>
      </p>
    );
  }
  const isEnded = investigation.status === "ended";

  return (
    <main className="mx-auto w-full max-w-6xl space-y-6 px-6 py-8">
      <header className="space-y-1">
        <nav className="text-sm text-(--muted)">
          <Link href="/research" className="hover:text-(--ink)">
            Studies
          </Link>{" "}
          ›
        </nav>
        <div className="flex flex-wrap items-baseline justify-between gap-4">
          <h1 className="text-2xl font-semibold text-(--ink)">{investigation.title}</h1>
          {isEnded ? null : (
            <EndStudyControl
              isEnded={false}
              endedBy={investigation.ended_by}
              onEnd={() => endStudy.mutate()}
              isEnding={endStudy.isPending}
            />
          )}
        </div>
        {!isEnded && investigation.description ? (
          <p className="max-w-2xl text-sm text-(--ink-2)">{investigation.description}</p>
        ) : null}
      </header>
      <TabBar
        label="Study"
        tabs={(isEnded ? ENDED_TABS : TABS).map((tab) => ({
          href: base + tab.slug,
          label: tab.label,
          active: tab.slug === "" ? pathname === base : pathname.startsWith(base + tab.slug),
        }))}
      />
      <div className="min-w-0 space-y-8">{children}</div>
    </main>
  );
}
