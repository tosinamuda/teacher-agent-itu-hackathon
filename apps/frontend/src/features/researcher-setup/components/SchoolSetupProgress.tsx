import { Link } from "@/shared/router";

type StepState = "done" | "current" | "todo";

type Step = {
  n: number;
  label: string;
  href: string;
  state: StepState;
};

type SchoolSetupProgressProps = {
  schoolId: string;
  /** Drives the done/current cues — a class workspace is the gate for learners + experiments. */
  workspaceCount: number;
};

/** A numbered progress rail above the school-setup tabs. Makes the dependency order
 *  explicit: details → class & teacher → learners → experiment. You can't add learners
 *  before a class workspace exists, or run an experiment before a class is set up. */
export function SchoolSetupProgress({ schoolId, workspaceCount }: SchoolSetupProgressProps) {
  const hasWorkspace = workspaceCount > 0;
  const steps: Step[] = [
    { n: 1, label: "School details", href: `/research/setup/${schoolId}/details`, state: "done" },
    {
      n: 2,
      label: "Add a class & teacher",
      href: `/research/setup/${schoolId}/classes`,
      state: hasWorkspace ? "done" : "current",
    },
    {
      n: 3,
      label: "Add learners",
      href: `/research/setup/${schoolId}/learners`,
      state: hasWorkspace ? "current" : "todo",
    },
    {
      n: 4,
      label: "Create experiment",
      href: `/research/experiments/new?schoolId=${schoolId}`,
      state: "todo",
    },
  ];

  return (
    <nav
      aria-label="School setup progress"
      className="flex flex-wrap items-center gap-x-3 gap-y-3 rounded-2xl border border-(--line) bg-(--surface) px-4 py-3"
    >
      {steps.map((step, index) => (
        <div key={step.n} className="flex items-center gap-3">
          <Link href={step.href} className="flex items-center gap-2">
            <span className={markerClass(step.state)}>
              {step.state === "done" ? "✓" : step.n}
            </span>
            <span className={labelClass(step.state)}>{step.label}</span>
          </Link>
          {index < steps.length - 1 && (
            <span className="text-(--muted)" aria-hidden>
              →
            </span>
          )}
        </div>
      ))}
    </nav>
  );
}

const MARKER_BASE = "flex h-6 w-6 items-center justify-center rounded-full text-xs font-semibold ";

function markerClass(state: StepState): string {
  if (state === "done") return MARKER_BASE + "bg-[color:var(--accent)] text-white";
  if (state === "current")
    return MARKER_BASE + "border-2 border-[color:var(--accent)] text-[color:var(--accent-deep)]";
  return MARKER_BASE + "border border-(--line) text-(--muted)";
}

function labelClass(state: StepState): string {
  if (state === "current") return "text-sm font-semibold text-(--ink)";
  if (state === "done") return "text-sm text-(--ink)";
  return "text-sm text-(--muted)";
}
