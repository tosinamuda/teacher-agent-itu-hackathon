import type { Slide } from "../slideDeck";

const WINDOW = 7;

/** The slides to show: a window of them that keeps the slide being read in view. */
export function windowOf(
  count: number,
  current: number,
): { from: number; to: number } {
  const size = Math.min(WINDOW, count);
  const from = Math.max(
    0,
    Math.min(current - Math.floor(size / 2), count - size),
  );
  return { from, to: from + size };
}

/** A strip of the deck's slides, each a small card with its number and title; the shown one is marked. */
export function SlideThumbnails({
  slides,
  current,
  onSelect,
}: {
  slides: Slide[];
  current: number;
  onSelect: (index: number) => void;
}) {
  const { from, to } = windowOf(slides.length, current);
  return (
    <div className="hidden shrink-0 items-center gap-2 md:flex">
      <ol aria-label="Slides" className="flex gap-2">
        {slides.slice(from, to).map((slide, at) => {
          const index = from + at;
          return (
            <li key={index}>
              <button
                type="button"
                aria-label={`Slide ${index + 1}: ${slide.title}`}
                aria-current={index === current ? "true" : undefined}
                onClick={() => onSelect(index)}
                className={`flex h-14 w-24 flex-col justify-between border p-1.5 text-left ${
                  slide.cover
                    ? "bg-(--accent-deep) text-white"
                    : "bg-white text-(--ink)"
                } ${index === current ? "border-2 border-(--ink)" : "border-(--line)"}`}
              >
                <span className="text-[9px] font-semibold opacity-70">
                  {index + 1}
                </span>
                <span className="line-clamp-2 text-[9px] font-semibold leading-tight">
                  {slide.title}
                </span>
              </button>
            </li>
          );
        })}
      </ol>
      <span className="text-xs text-(--ink-2)">of {slides.length}</span>
    </div>
  );
}
