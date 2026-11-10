import { Link } from "@/shared/router";
import { usePathname } from "@/shared/router";

const STUDENT_NAV = [{ href: "/research/student/pack-runner", title: "Pack Runner" }];

/** App-wide top bar: brand and role nav. One gutter. */
export function AppHeader() {
  const pathname = usePathname();
  // The rater packet view is a focused, chrome-less surface.
  if (/^\/research\/rater\/h[12]\/[^/]+$/.test(pathname)) return null;
  // Inside /research/*, ResearchShell owns the whole top strip (brand + nav
  // + identity + sign-out). Suppressing AppHeader here keeps a single strip.
  if (pathname.startsWith("/research")) return null;
  // The landing pages (``/`` and ``/home``) are self-contained sign-in surfaces
  // with their own brand bar — no global chrome above them.
  if (pathname === "/" || pathname === "/home") return null;
  const isStudentRoute = pathname.startsWith("/research/student");
  const isRaterRoute = pathname.startsWith("/research/rater");
  const role = isStudentRoute ? "student" : "root";
  const navItems = role === "student" ? STUDENT_NAV : [];
  // The Research entry belongs to the landing/hub only. The rater and student
  // persona workspaces stay focused and never cross-link to research — the brand
  // link is always the way back to the hub (where Research lives).
  const showResearchLink = role === "root" && !isRaterRoute;
  const researchActive =
    pathname.startsWith("/research") || pathname.startsWith("/experiments");

  const linkClass = (active: boolean) =>
    `border-b-2 pb-1 transition-colors ${
      active
        ? "border-(--accent) font-medium text-(--ink)"
        : "border-transparent text-(--ink-2) hover:text-(--ink)"
    }`;

  return (
    <header className="sticky top-0 z-20 border-b border-(--line) bg-(--bg)">
      <div className="mx-auto flex max-w-[1200px] flex-wrap items-center justify-between gap-4 px-6 py-3">
        <div className="flex items-center gap-4">
          <Link
            className="font-(family-name:--font-display) text-base font-semibold tracking-[-0.01em] text-(--ink) no-underline"
            href="/"
          >
            Plan-to-Tutor
          </Link>
        </div>
        <nav className="flex flex-wrap items-center gap-6 text-sm" aria-label="Primary">
          {navItems.map((item) => {
            const active = pathname === item.href || pathname.startsWith(`${item.href}/`);
            return (
              <Link key={item.href} href={item.href} className={linkClass(active)}>
                {item.title}
              </Link>
            );
          })}
          {showResearchLink ? (
            <Link href="/research" className={linkClass(researchActive)}>
              Research
            </Link>
          ) : null}
        </nav>
      </div>
    </header>
  );
}
