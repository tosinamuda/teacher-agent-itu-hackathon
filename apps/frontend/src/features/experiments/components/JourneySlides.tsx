import { ReactNode, useEffect, useRef, useState } from "react";

import { Picker } from "@/shared/components/ui/Picker";

/** One slide in the journey deck. */
export type JourneySlide = {
  title: string;
  subtitle?: string;
  /** The part of the journey the step belongs to, headed once above its first step. */
  chapter?: string;
  body: ReactNode;
  /** Optional per-step drill-down (e.g. "how this was generated") shown below the body. */
};

function StepList({
  slides,
  current,
  onGo,
}: {
  slides: JourneySlide[];
  current: number;
  onGo: (index: number) => void;
}) {
  return (
    <ol className="hidden text-sm lg:block">
      {slides.map((item, i) => (
        <li key={item.title}>
          {item.chapter && item.chapter !== slides[i - 1]?.chapter ? (
            <p className={`pb-1 text-xs font-medium text-(--muted) ${i > 0 ? "pt-4" : ""}`}>
              {item.chapter}
            </p>
          ) : null}
          <button
            type="button"
            aria-current={i === current ? "step" : undefined}
            onClick={() => onGo(i)}
            className={`w-full border-l-2 py-1.5 pl-3 text-left ${
              i === current
                ? "border-(--accent) font-medium text-(--ink)"
                : "border-transparent text-(--muted) hover:text-(--ink)"
            }`}
          >
            <span className="mr-2 tabular-nums text-(--faint)">{i + 1}</span>
            {item.title}
          </button>
        </li>
      ))}
    </ol>
  );
}

/**
 * A journey walked one step at a time: the steps listed down the side with any controls
 * above them, and the current step in a single panel with its neighbours named at its foot.
 * The ← → keys move between steps.
 */
export function JourneySlides({
  slides,
  controls,
  index: shown,
  onIndexChange,
}: {
  slides: JourneySlide[];
  controls?: ReactNode;
  /** The step to show, when a parent keeps it (in the URL, say); else the deck keeps its own. */
  index?: number;
  onIndexChange?: (index: number) => void;
}) {
  const [own, setOwn] = useState(0);
  const current = Math.min(shown ?? own, Math.max(slides.length - 1, 0));
  const slide = slides[current];
  const go = (to: number) => {
    const next = Math.min(Math.max(to, 0), slides.length - 1);
    setOwn(next);
    onIndexChange?.(next);
  };

  // Presses land faster than renders, so each moves from the step the last press reached.
  const reached = useRef(current);
  useEffect(() => {
    reached.current = current;
  }, [current]);
  useEffect(() => {
    const move = (by: number) => {
      const next = Math.min(Math.max(reached.current + by, 0), slides.length - 1);
      reached.current = next;
      setOwn(next);
      onIndexChange?.(next);
    };
    const onKey = (event: KeyboardEvent) => {
      if ((event.target as HTMLElement | null)?.closest("input, select, textarea")) return;
      if (event.key === "ArrowRight") move(1);
      if (event.key === "ArrowLeft") move(-1);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [slides.length, onIndexChange]);

  if (!slide) return <p className="text-sm text-(--muted)">Nothing to walk through yet.</p>;

  return (
    <div className="grid gap-8 lg:grid-cols-[15rem_minmax(0,1fr)]">
      <aside className="flex flex-wrap items-end gap-4 lg:sticky lg:top-4 lg:block lg:space-y-6 lg:self-start">
        {controls}
        <div className="lg:hidden">
          <Picker
            stacked
            label="Step"
            options={slides.map((item, i) => ({
              value: String(i),
              label: `${i + 1}. ${item.title}`,
            }))}
            value={String(current)}
            onChange={(value) => go(Number(value))}
          />
        </div>
        <StepList slides={slides} current={current} onGo={go} />
      </aside>

      <section className="min-w-0 self-start border border-(--line) bg-(--surface)">
        <header className="border-b border-(--line) px-6 py-4">
          <p className="text-xs text-(--muted)">
            {slide.chapter ? `${slide.chapter} · ` : ""}Step {current + 1} of {slides.length}
          </p>
          <h2 className="text-lg font-semibold text-(--ink)">{slide.title}</h2>
          {slide.subtitle ? <p className="text-sm text-(--muted)">{slide.subtitle}</p> : null}
        </header>
        <div className="space-y-4 px-6 py-5">
          {slide.body}
        </div>
        <footer className="flex items-center justify-between gap-3 border-t border-(--line) px-6 py-3 text-sm">
          <button
            type="button"
            onClick={() => go(current - 1)}
            disabled={current === 0}
            className="text-(--muted) hover:text-(--ink) disabled:invisible"
          >
            ‹ {current > 0 ? slides[current - 1].title : ""}
          </button>
          <button
            type="button"
            onClick={() => go(current + 1)}
            disabled={current === slides.length - 1}
            className="font-medium text-(--ink) hover:text-(--accent-deep) disabled:invisible"
          >
            {current < slides.length - 1 ? slides[current + 1].title : ""} ›
          </button>
        </footer>
      </section>
    </div>
  );
}
