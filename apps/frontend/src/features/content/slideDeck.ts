import { EngineManifest } from "./types";

export type Slide = {
  title: string;
  points: string[];
  figure: string | null;
  notes: string;
  step: string;
  /** The cover is shown as a title slide: its points are the subject line, then the objectives. */
  cover: boolean;
  objectives: string[];
};

type Row = Record<string, unknown>;

const rows = (value: unknown): Row[] =>
  Array.isArray(value)
    ? value.filter(
        (item): item is Row => typeof item === "object" && item !== null,
      )
    : [];

const text = (value: unknown): string =>
  typeof value === "string" ? value.trim() : "";

const coverSlide = (cover: EngineManifest["cover"]): Slide[] =>
  cover?.title
    ? [
        {
          title: cover.title,
          points: cover.subtitle ? [cover.subtitle] : [],
          figure: null,
          notes: "",
          step: "Cover",
          cover: true,
          objectives: cover.objectives,
        },
      ]
    : [];

/** The deck's cover, then every slide in the order it is shown: each step's slides, step after step. */
export function slidesOf(manifest: EngineManifest): Slide[] {
  return [
    ...coverSlide(manifest.cover),
    ...manifest.sections.flatMap((section) =>
      rows(section.part.slides).map((slide) => ({
        title: text(slide.title),
        points: rows(slide.points)
          .map((entry) => text(entry.point))
          .filter(Boolean),
        figure: text(slide.figure) || null,
        notes: text(slide.speaker_notes),
        step: section.label,
        cover: false,
        objectives: [],
      })),
    ),
  ];
}
