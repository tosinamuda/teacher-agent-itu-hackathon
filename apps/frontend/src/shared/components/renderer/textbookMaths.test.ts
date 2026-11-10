import { readFileSync } from "node:fs";
import path from "node:path";

import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";

import { RichText } from "./RichText";

/**
 * Every exercise and answer in the textbook, drawn the way a lesson note quotes it.
 *
 * The records carry MathJax's dialect and escapes their conversion lost, and the model
 * copies them word for word; so a rewrite that holds for these holds for what is drawn.
 */
const RECORDS = path.resolve(
  __dirname,
  "../../../../../../dataset/processed/textbook/jsonl/linked/records.jsonl",
);

interface TextbookRecord {
  record_id: string;
  prompt_text?: string | string[];
  answer_text?: string | string[];
}

function texts(): { id: string; text: string }[] {
  return readFileSync(RECORDS, "utf8")
    .trim()
    .split("\n")
    .map((line) => JSON.parse(line) as TextbookRecord)
    .flatMap((record) =>
      [record.prompt_text, record.answer_text]
        .flat()
        .filter(
          (text): text is string =>
            typeof text === "string" && text.trim() !== "",
        )
        .map((text) => ({ id: record.record_id, text })),
    );
}

describe("the textbook's maths", () => {
  const drawn = texts().map(({ id, text }) => ({
    id,
    html: renderToStaticMarkup(createElement(RichText, { text, tables: true })),
  }));

  it("is every record's", () => {
    expect(drawn.length).toBeGreaterThan(1500);
  });

  it("sets in KaTeX, every piece of it", () => {
    const failed = drawn
      .filter(({ html }) => html.includes("katex-error"))
      .map(
        ({ id, html }) =>
          `${id}: ${/title="([^"]*)"/.exec(html.slice(html.indexOf("katex-error")))?.[1]}`,
      );

    expect(failed).toEqual([]);
  });

  it("is never a block of code", () => {
    expect(
      drawn.filter(({ html }) => html.includes("<pre>")).map(({ id }) => id),
    ).toEqual([]);
  });

  it("never shows a dollar sign", () => {
    expect(
      drawn
        .filter(({ html }) => html.replace(/<[^>]+>/g, "").includes("$$"))
        .map(({ id }) => id),
    ).toEqual([]);
  });
});
