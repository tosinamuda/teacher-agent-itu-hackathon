import { Link } from "@/shared/router";
import { usePathname, useRouter } from "@/shared/router";
import type { ReactNode } from "react";

import { TeacherShell } from "@/features/teaching-workspace/components/TeacherShell";
import { hasPanel } from "@/features/teaching-workspace/lib/pagesWithPanel";
import { ResearchManagerGate } from "@/shared/components/layouts/ResearchManagerGate";
import { ResearchRoleGuard } from "@/shared/components/layouts/ResearchRoleGuard";
import { UserMenu } from "@/shared/components/layouts/UserMenu";
import { useAuthMe, useRefreshAuthMe } from "@/shared/hooks/useAuthMe";
import { clearAuthCode } from "@/shared/lib/auth";

type ResearchShellProps = {
  children: ReactNode;
};

// Three containment-based destinations. Each owns a set of route prefixes so the right
// tab stays lit when you drill in (an experiment lives under Studies; learners under
// Setup). Story / H1 / H2 / New-baseline are no longer top-level — they live inside a
// study, an experiment, or Setup.
const navItems: { href: string; label: string; owns: string[] }[] = [
  // The home IS the studies portfolio; study detail lives under it.
  { href: "/research", label: "Studies", owns: ["/research/investigations"] },
  {
    href: "/research/experiments",
    label: "Experiments",
    owns: [
      "/research/experiments",
      "/research/h1",
      "/research/h2",
      "/research/story",
    ],
  },
  {
    href: "/research/setup",
    label: "Setup",
    owns: ["/research/setup", "/research/learners"],
  },
  { href: "/research/plugins", label: "Plugins", owns: ["/research/plugins"] },
  { href: "/research/ops", label: "Ops", owns: ["/research/ops"] },
];

/** Wraps researcher routes with a shared local navigation shell.
 *
 *  Any authenticated role passes the gate, then `ResearchRoleGuard` checks the
 *  pathname's area against the caller's role; the researcher tab rail is shown
 *  only for research managers (every other role lands on the role-aware home
 *  and navigates from there).
 */
export function ResearchShell({ children }: ResearchShellProps) {
  const pathname = usePathname();
  const router = useRouter();
  const { data: actor } = useAuthMe();
  const refreshAuthMe = useRefreshAuthMe();
  const isManager = Boolean(actor?.is_research_manager);
  const isAuthenticated = Boolean(actor && actor.role !== "anonymous");

  // Light the destination whose prefixes best match the path. "Studies" ("/research")
  // matches the home exactly OR any of its owned sub-routes (the study detail), so it
  // doesn't win on every sub-route via a bare prefix.
  const matchLength = (item: (typeof navItems)[number]): number => {
    const prefixes = item.owns.length > 0 ? item.owns : [item.href];
    const hit = prefixes.filter(
      (p) => pathname === p || pathname.startsWith(`${p}/`),
    );
    const ownMatch =
      hit.length > 0 ? Math.max(...hit.map((p) => p.length)) : -1;
    if (item.href === "/research") {
      return pathname === "/research" ? item.href.length : ownMatch;
    }
    return ownMatch;
  };
  const activeHref = navItems.reduce(
    (best, item) =>
      matchLength(item) > matchLength(best.item)
        ? { href: item.href, item }
        : best,
    {
      href: "",
      item: { href: "", label: "", owns: [] } as (typeof navItems)[number],
    },
  ).href;

  // Sign-out must LEAVE the current page: staying put parks the sign-in panel
  // on whatever (possibly role-privileged) URL the last user was reading, and
  // the next sign-in resumes there — a teacher signing in after a researcher
  // landed straight on an experiment detail (2026-06-11). Going to the
  // role-aware home gives every role a correct landing.
  const signOut = () => {
    clearAuthCode();
    refreshAuthMe();
    router.push("/research");
  };

  // The H1/H2 rater packet workspace is a deliberately immersive, full-screen
  // tool — its own sidebar, slide-in drawer and h-screen layout live in
  // RaterPacketShell. Render it edge-to-edge (still gated) rather than boxing it
  // into the centred max-w-[1200px] research column, which on a wide monitor
  // leaves the rating workspace cramped between large empty gutters.
  const isImmersivePacket = /^\/research\/rater\/(?:h1|h2)\/.+/.test(pathname);
  if (isImmersivePacket) {
    return (
      <div className="min-h-screen bg-(--bg)">
        <ResearchManagerGate>
          <ResearchRoleGuard>{children}</ResearchRoleGuard>
        </ResearchManagerGate>
      </div>
    );
  }

  // The teacher workspace has its own frame: sidebar, page and right panel.
  if (/^\/research\/teacher(?:\/|$)/.test(pathname)) {
    return (
      <TeacherShell
        signedIn={isAuthenticated}
        fillsFrame={hasPanel(pathname)}
        userMenu={
          isAuthenticated && actor ? (
            <UserMenu
              actor={actor}
              onSignOut={signOut}
              variant="row"
              settingsHref="/research/teacher/settings"
            />
          ) : null
        }
      >
        <ResearchManagerGate>
          <ResearchRoleGuard>{children}</ResearchRoleGuard>
        </ResearchManagerGate>
      </TeacherShell>
    );
  }

  return (
    <div className="min-h-screen bg-(--bg)">
      <div className="mx-auto flex w-full max-w-[1200px] flex-col gap-4 px-4 py-4 sm:px-6">
        <header className="flex flex-wrap items-center justify-between gap-3 border-b border-(--line) pb-3">
          <Link
            href="/research"
            className="font-(family-name:--font-display) text-base font-semibold tracking-[-0.01em] text-(--ink) no-underline hover:opacity-80"
          >
            Plan-to-Tutor
          </Link>
          {isAuthenticated && actor ? (
            <nav className="flex flex-wrap items-center gap-5 text-sm">
              {isManager
                ? navItems.map((item) => {
                    const active = item.href === activeHref;
                    return (
                      <Link
                        key={item.href}
                        href={item.href}
                        className={`border-b-2 pb-1 transition-colors ${
                          active
                            ? "border-(--accent) font-medium text-(--ink)"
                            : "border-transparent text-(--ink-2) hover:text-(--ink)"
                        }`}
                      >
                        {item.label}
                      </Link>
                    );
                  })
                : null}
              <UserMenu actor={actor} onSignOut={signOut} />
            </nav>
          ) : null}
        </header>
        <ResearchManagerGate>
          <ResearchRoleGuard>{children}</ResearchRoleGuard>
        </ResearchManagerGate>
      </div>
    </div>
  );
}
