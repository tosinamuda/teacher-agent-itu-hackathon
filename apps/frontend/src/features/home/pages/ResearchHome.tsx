import { Navigate } from "react-router";

import { ResearchLandingPage } from "@/features/experiments/pages/ResearchLandingPage";
import { useAuthMe } from "@/shared/hooks/useAuthMe";

import { LandingCard, RoleLanding } from "../components/RoleLanding";
import { RaterHome } from "./RaterHome";

/** ``/research`` home: branches by the authenticated role.
 *
 *  Researcher gets the existing studies portfolio; the other roles get a small
 *  set of cards that link into the existing role-specific pages (the URL
 *  collapse into ``/research/*`` is a follow-up — this phase wires the spine).
 */
export function ResearchHome() {
  const { data: actor } = useAuthMe();
  const role = actor?.role ?? "anonymous";
  const greeting = actor?.full_name ?? actor?.email ?? "there";

  if (role === "research_manager") {
    return <ResearchLandingPage />;
  }
  if (role === "admin") {
    return (
      <RoleLanding
        eyebrow="Admin"
        title={`Welcome, ${greeting}`}
        lede="Manage the platform — schools, workspaces, and learners. The research surfaces remain available to researchers and teachers."
        cards={ADMIN_CARDS}
      />
    );
  }
  if (role === "teacher") {
    // A teacher opens into the class they last used.
    return <Navigate to="/research/teacher/lessons" replace />;
  }
  if (role === "rater") {
    return <RaterHome greeting={greeting} />;
  }
  if (role === "student") {
    return (
      <RoleLanding
        eyebrow="Student"
        title={`Welcome, ${greeting}`}
        lede="Your exit-assessment sessions and the per-lesson revision notes your teacher has approved for you."
        cards={STUDENT_CARDS}
      />
    );
  }
  // ``anonymous`` is caught by the gate; this is a defensive fallthrough only.
  return (
    <main className="py-10 text-sm text-(--muted)">
      Your access code didn&apos;t resolve to a known role.
    </main>
  );
}

const ADMIN_CARDS: LandingCard[] = [
  {
    href: "/research/setup/users",
    label: "Users",
    body: "Every researcher, teacher, rater, student and admin login.",
  },
  {
    href: "/research/setup",
    label: "School setup",
    body: "Schools, workspaces, and learners.",
  },
  {
    href: "/research/learners",
    label: "Study roster",
    body: "Learner cohorts and evidence context.",
  },
];

const STUDENT_CARDS: LandingCard[] = [
  {
    href: "/research/student",
    label: "Your assessments",
    body: "Take the exit assessments your teacher has prepared, and read your revision notes.",
  },
];
