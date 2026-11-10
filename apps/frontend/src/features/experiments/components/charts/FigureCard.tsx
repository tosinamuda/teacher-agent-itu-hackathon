import { ReactNode, useRef } from "react";

import { downloadPng, downloadSvg } from "./figureExport";

type FigureCardProps = {
  title: string;
  caption?: string;
  filename: string;
  children: ReactNode;
};

/** A titled chart card with SVG/PNG figure export for the thesis report. */
export function FigureCard({ title, caption, filename, children }: FigureCardProps) {
  const ref = useRef<HTMLDivElement>(null);
  return (
    <section className="border border-(--line) bg-(--surface) p-4">
      <header className="mb-3 flex items-start justify-between gap-3">
        <div className="min-w-0">
          <h3 className="text-sm font-medium text-(--ink)">{title}</h3>
          {caption ? <p className="mt-0.5 text-xs leading-5 text-(--muted)">{caption}</p> : null}
        </div>
        <div className="flex shrink-0 gap-3 text-xs">
          <button
            className="text-(--muted) hover:text-(--ink)"
            onClick={() => downloadSvg(ref.current, `${filename}.svg`)}
            type="button"
          >
            SVG
          </button>
          <button
            className="text-(--muted) hover:text-(--ink)"
            onClick={() => downloadPng(ref.current, `${filename}.png`)}
            type="button"
          >
            PNG
          </button>
        </div>
      </header>
      <div ref={ref}>{children}</div>
    </section>
  );
}
