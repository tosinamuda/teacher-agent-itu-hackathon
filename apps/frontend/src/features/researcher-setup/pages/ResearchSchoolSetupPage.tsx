import { Link } from "@/shared/router";
import { useSearchParams } from "@/shared/router";

import { SchoolDirectoryTable } from "../components/SchoolDirectoryTable";
import { useResearchSchools } from "../hooks/useSchoolSetup";

/** Researcher school directory — a table of schools, with the create form moved to its
 *  own `/research/setup/school/new` page. A just-created school (`?created=`) is
 *  highlighted at the top. */
export function ResearchSchoolSetupPage() {
  const searchParams = useSearchParams();
  const createdId = searchParams.get("created");
  const schoolsQuery = useResearchSchools();
  const schools = schoolsQuery.data ?? [];

  return (
    <main className="flex w-full flex-col gap-6 py-8">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div className="max-w-3xl space-y-3">
          <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[color:var(--accent)]">
            School setup
          </div>
          <h1 className="text-4xl font-semibold tracking-tight text-[color:var(--ink)]">
            Manage research schools before running experiments.
          </h1>
          <p className="text-base leading-relaxed text-[color:var(--muted)]">
            Create a school, then open it to set up its classes, teachers, and learners.
          </p>
        </div>
        <Link
          href="/research/setup/school/new"
          className="inline-flex shrink-0 rounded-none bg-[color:var(--accent)] px-4 py-2 text-sm font-semibold text-white hover:bg-[color:var(--accent-deep)]"
        >
          New school
        </Link>
      </header>

      <section className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-(--ink)">Current schools</h2>
          <span className="text-sm text-(--muted)">{schools.length} schools</span>
        </div>
        {schoolsQuery.isLoading ? (
          <p className="text-sm text-(--muted)">Loading schools…</p>
        ) : schools.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-(--line) bg-(--surface) p-8 text-center">
            <h3 className="text-lg font-semibold text-(--ink)">No schools yet.</h3>
            <p className="mt-2 text-sm text-(--muted)">
              <Link
                href="/research/setup/school/new"
                className="font-semibold text-(--accent-deep) hover:underline"
              >
                Create the first school →
              </Link>
            </p>
          </div>
        ) : (
          <SchoolDirectoryTable schools={schools} highlightId={createdId} />
        )}
      </section>
    </main>
  );
}
