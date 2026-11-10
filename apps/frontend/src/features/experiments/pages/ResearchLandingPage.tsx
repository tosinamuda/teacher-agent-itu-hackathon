import { Link } from "@/shared/router";

import { LINK, ROW_HEAD, TABLE, TD, TH } from "@/shared/components/ui/table";

import { useInvestigations } from "../hooks/useInvestigations";

/** Research pages that aren't a study. */
const ELSEWHERE = [
  { href: "/research/experiments", label: "All experiments" },
  { href: "/research/setup", label: "School setup" },
  { href: "/research/learners", label: "Study roster" },
];

/** Research home: every study, the ones still running first. A study is what you open. */
export function ResearchLandingPage() {
  const investigationsQuery = useInvestigations();
  const studies = [...(investigationsQuery.data ?? [])].sort(
    (a, b) => Number(a.status === "ended") - Number(b.status === "ended")
  );

  return (
    <main className="flex w-full flex-col gap-8 py-8">
      <header className="flex flex-wrap items-baseline justify-between gap-4">
        <h1 className="text-2xl font-semibold text-(--ink)">Studies</h1>
        <Link
          href="/research/investigations/new"
          className="border border-(--ink) px-3 py-1.5 text-sm font-medium text-(--ink) hover:bg-(--sunken)"
        >
          New study
        </Link>
      </header>

      {investigationsQuery.isLoading ? (
        <p className="text-sm text-(--muted)">Loading…</p>
      ) : investigationsQuery.isError ? (
        <p className="text-sm text-(--danger)">Couldn&apos;t load studies.</p>
      ) : studies.length === 0 ? (
        <p className="text-sm text-(--muted)">No studies yet.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className={TABLE}>
            <thead>
              <tr>
                <th className={TH}>Study</th>
                <th className={TH}>Experiments</th>
                <th className={TH}>Status</th>
              </tr>
            </thead>
            <tbody>
              {studies.map((study) => (
                <tr key={study.investigation_id}>
                  <td className={ROW_HEAD}>
                    <Link href={`/research/investigations/${study.investigation_id}`} className={LINK}>
                      {study.title}
                    </Link>
                    <p className="font-mono text-xs font-normal text-(--muted)">
                      {study.investigation_code}
                    </p>
                  </td>
                  <td className={TD}>{study.experiment_count}</td>
                  <td className={`${TD} capitalize text-(--ink-2)`}>{study.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <p className="text-sm text-(--muted)">
        Also:{" "}
        {ELSEWHERE.map((page, index) => (
          <span key={page.href}>
            {index > 0 ? " · " : null}
            <Link href={page.href} className={LINK}>
              {page.label}
            </Link>
          </span>
        ))}
      </p>
    </main>
  );
}
