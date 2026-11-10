import { useEffect, useState } from "react";
import { useRouter } from "@/shared/router";

import { fetchAuthMe } from "@/shared/api/auth";
import { useAuthMe, useRefreshAuthMe } from "@/shared/hooks/useAuthMe";
import { clearAuthCode, setAuthCode } from "@/shared/lib/auth";

/**
 * The general landing page (``/``) — the front door for every role.
 *
 * One sign-in: researcher, teacher, rater, student and admin codes all enter
 * here. The backend resolves the role; ``/research`` then renders the
 * role-appropriate workspace. If the caller is already authenticated, we jump
 * straight there — there's nothing to do on this page.
 *
 * Visual cues are borrowed from ``docs/design-system.html`` —
 * eyebrow → display headline → lede on the left, sign-in card on the right, a
 * single editorial serif line for the research-grade voice, sharp 0px corners
 * and hairline framing throughout (no shadows, no gradients).
 */
export default function HomePage() {
  const router = useRouter();
  const refreshAuthMe = useRefreshAuthMe();
  const { data: me } = useAuthMe();
  const [code, setCode] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  // If already signed in, this page has nothing to offer — go to the workspace.
  useEffect(() => {
    if (me && me.role !== "anonymous") {
      router.replace("/research");
    }
  }, [me, router]);

  const signIn = async () => {
    const trimmed = code.trim();
    if (!trimmed || busy) return;
    setBusy(true);
    setError(null);
    setAuthCode(trimmed);
    refreshAuthMe();
    try {
      const result = await fetchAuthMe();
      if (result.role && result.role !== "anonymous") {
        router.push("/research");
        return;
      }
      clearAuthCode();
      refreshAuthMe();
      setError("That access code isn't recognised.");
    } catch {
      clearAuthCode();
      refreshAuthMe();
      setError("We can't reach the service. Try again in a moment.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <main className="min-h-screen bg-(--bg)">
      <div className="mx-auto flex min-h-screen w-full max-w-[1120px] flex-col px-5 sm:px-7">
        {/* Brand bar — thin, no actions; the page IS the front door.
            Deliberately omits the thesis framing — visiting raters and students
            should not learn the study's hypothesis from the sign-in page. */}
        <header className="flex h-[60px] items-center border-b border-(--line)">
          <p className="text-base font-semibold tracking-[-0.01em] text-(--ink)">
            Plan-to-Tutor
          </p>
        </header>

        <section className="grid flex-1 grid-cols-1 items-start gap-8 py-[clamp(28px,8vw,96px)] md:grid-cols-[1fr_360px] md:gap-16">
          {/* Head — design-system "page-head": eyebrow → d1 → lede + a serif accent.
              Says enough about WHAT the platform does for a participant to orient
              themselves, but deliberately stops short of naming the study
              hypothesis — raters and students shouldn't learn that here. */}
          <div className="space-y-5">
            <p className="text-[11px] font-medium uppercase tracking-[0.13em] text-(--accent)">
              Research workspace
            </p>
            <h1 className="text-[clamp(34px,5vw,50px)] font-semibold leading-[1.04] tracking-[-0.025em] text-(--ink)">
              A study of student
              <br />
              review-note quality.
            </h1>
            <p className="max-w-[60ch] text-[17px] leading-relaxed text-(--ink-2)">
              Teachers&apos; lesson plans drive personalised revision notes for each
              student. This workspace is where we author the plans, generate the
              notes, route them to expert teachers for rating, and learn what makes
              a revision note useful.
            </p>
            <dl className="hidden max-w-[60ch] gap-x-6 gap-y-3 border-t border-(--line) pt-5 text-sm leading-relaxed text-(--ink-2) sm:grid sm:grid-cols-2">
              <div>
                <dt className="text-[11px] font-semibold uppercase tracking-[0.14em] text-(--muted)">
                  Teachers
                </dt>
                <dd>Author lesson plans, approve the revision notes for your class.</dd>
              </div>
              <div>
                <dt className="text-[11px] font-semibold uppercase tracking-[0.14em] text-(--muted)">
                  Raters
                </dt>
                <dd>Rate generated revision notes against rubric criteria.</dd>
              </div>
              <div>
                <dt className="text-[11px] font-semibold uppercase tracking-[0.14em] text-(--muted)">
                  Students
                </dt>
                <dd>Take exit assessments and read your approved revision notes.</dd>
              </div>
              <div>
                <dt className="text-[11px] font-semibold uppercase tracking-[0.14em] text-(--muted)">
                  Researchers · Admins
                </dt>
                <dd>Set up studies, schools, and participants.</dd>
              </div>
            </dl>
          </div>

          {/* Sign-in card — sharp corners, single hairline, one action. */}
          <aside className="border border-(--line) bg-(--surface) p-6">
            <label className="block space-y-2">
              <span className="text-[11px] font-semibold uppercase tracking-[0.16em] text-(--muted)">
                Access code
              </span>
              <input
                autoFocus
                aria-label="Access code"
                className="h-10 w-full border border-(--line-2) bg-(--surface) px-3 font-mono text-sm text-(--ink) outline-none transition focus:border-(--accent)"
                placeholder="e.g. uncle-tosin"
                value={code}
                onChange={(event) => setCode(event.target.value)}
                onKeyDown={(event) => {
                  if (event.key === "Enter") void signIn();
                }}
              />
            </label>
            {error ? (
              <p role="alert" className="mt-3 text-sm text-(--danger-ink)">
                {error}
              </p>
            ) : null}
            <button
              type="button"
              onClick={() => void signIn()}
              disabled={busy}
              className="mt-4 inline-flex h-10 w-full items-center justify-center bg-(--accent) text-sm font-semibold text-white transition hover:bg-(--accent-bright) disabled:opacity-60"
            >
              {busy ? "Signing in…" : "Enter workspace"}
            </button>
            <p className="mt-4 text-[12px] leading-relaxed text-(--muted)">
              Your role is who you are, not a choice. Whichever code you enter — researcher,
              teacher, rater, student, admin — takes you to the right view.
            </p>
          </aside>
        </section>

        <footer className="border-t border-(--line) py-5 text-[12px] text-(--muted)">
          <span className="font-mono">/research</span>
          <span aria-hidden className="mx-2 text-(--line-2)">
            ·
          </span>
          Restricted to study participants
        </footer>
      </div>
    </main>
  );
}
