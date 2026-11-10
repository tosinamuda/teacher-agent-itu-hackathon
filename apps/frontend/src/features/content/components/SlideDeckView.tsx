import { useState } from "react";

import { Pager } from "@/shared/components/renderer/Pager";
import { RichText } from "@/shared/components/renderer/RichText";
import { TikzFigure } from "@/shared/components/renderer/TikzFigure";

import { Slide, slidesOf } from "../slideDeck";
import { EngineManifest } from "../types";
import { SlideThumbnails } from "./SlideThumbnails";

/** The title slide: the lesson's title, its subject line and what the class will learn. */
function CoverSlide({ slide }: { slide: Slide }) {
  return (
    <article className="relative flex max-h-[60dvh] flex-col justify-center gap-6 overflow-y-auto overscroll-contain rounded-2xl bg-(--accent-deep) p-10 text-white md:max-h-none md:min-h-0 md:flex-1">
      <h2 className="text-5xl font-semibold leading-tight [&_p]:inline">
        <RichText text={slide.title} breaks={false} />
      </h2>
      {slide.points.map((point, at) => (
        <p key={at} className="text-2xl text-white/85">
          {point}
        </p>
      ))}
      {slide.objectives.length > 0 ? (
        <ul className="space-y-2 border-t border-white/30 pt-5 text-xl text-white">
          {slide.objectives.map((objective, at) => (
            <li key={at}>{objective}</li>
          ))}
        </ul>
      ) : null}
    </article>
  );
}

/** A slide of the lesson: an accent band, a title, large points and its drawing. */
function ContentSlide({ slide }: { slide: Slide }) {
  return (
    <article className="relative max-h-[60dvh] overflow-y-auto overscroll-contain rounded-2xl border border-(--line) border-l-[14px] border-l-(--accent-deep) bg-white p-10 md:max-h-none md:min-h-0 md:flex-1">
      <h2 className="text-3xl font-semibold text-(--ink) [&_p]:inline">
        <RichText text={slide.title} breaks={false} />
      </h2>
      {slide.points.length > 0 ? (
        <ul className="mt-6 space-y-4">
          {slide.points.map((point, at) => (
            <li key={at} className="flex gap-3 text-2xl text-(--ink)">
              <span aria-hidden className="text-(--accent-deep)">
                •
              </span>
              <div className="prose prose-xl max-w-none">
                <RichText text={point} />
              </div>
            </li>
          ))}
        </ul>
      ) : null}
      {slide.figure ? <TikzFigure source={slide.figure} /> : null}
    </article>
  );
}

/** A deck for the teacher's review: one slide at a time as the class sees it, notes beneath. */
export function SlideDeckView({ manifest }: { manifest: EngineManifest }) {
  const slides = slidesOf(manifest);
  const [shown, setShown] = useState(0);
  if (slides.length === 0) {
    return (
      <p className="text-sm text-(--muted)">This deck has no slides yet.</p>
    );
  }
  return (
    <>
      <Pager
        index={shown}
        onIndexChange={setShown}
        count={slides.length}
        heading={(index) =>
          `Slide ${index + 1} of ${slides.length} · ${slides[index].step}`
        }
      >
        {(index) => {
          const slide = slides[index];
          return (
            <div className="flex min-h-0 flex-1 flex-col gap-3">
              <SlideThumbnails
                slides={slides}
                current={index}
                onSelect={setShown}
              />
              {slide.cover ? (
                <CoverSlide slide={slide} />
              ) : (
                <ContentSlide slide={slide} />
              )}
              {slide.notes ? (
                <section
                  aria-label="Speaker notes"
                  className="max-h-36 shrink-0 overflow-y-auto overscroll-contain rounded-2xl border border-(--line) bg-(--surface) p-4"
                >
                  <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--muted)">
                    Speaker notes
                  </p>
                  <div className="prose prose-sm mt-1 max-w-none text-(--ink-2)">
                    <RichText text={slide.notes} />
                  </div>
                </section>
              ) : null}
            </div>
          );
        }}
      </Pager>
    </>
  );
}
