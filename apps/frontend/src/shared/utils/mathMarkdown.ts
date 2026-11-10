/**
 * Markdown whose maths `remark-math` reads as the author meant it.
 *
 * Everything here is about where maths starts and ends, which markdown decides before
 * KaTeX sees a character; what is inside is `asKatex`'s concern.
 */
export function tidyMathMarkdown(markdown: string): string {
  return displayBareEnvironments(
    withDisplaysIndentedAsOpened(
      withoutEmptyDisplays(
        withDisplayFencesAlone(withDollarDelimiters(withoutCurrencyEscapes(markdown))),
      ),
    ),
  );
}

/**
 * A backslash before the naira sign or before a digit is a currency escape that left its
 * mark: neither is LaTeX, and both would be drawn as a stray `\`. The `\\` of a line break
 * is kept.
 */
function withoutCurrencyEscapes(markdown: string): string {
  return markdown.replace(/(?<!\\)\\(?=[₦\d])/g, "");
}

/** `remark-math` reads `$…$` and `$$…$$`; the model writes the LaTeX `\(…\)` and `\[…\]`. */
function withDollarDelimiters(markdown: string): string {
  return markdown
    .replace(/(?<!\\)\\\[([\s\S]*?)(?<!\\)\\\]/g, (_whole, inner: string) => `$$${inner}$$`)
    .replace(/(?<!\\)\\\(([\s\S]*?)(?<!\\)\\\)/g, (_whole, inner: string) => `$${inner}$`);
}

/**
 * A `$$` sharing its line with anything else goes on a line of its own: text after an
 * opening `$$` is read as the fence's label and dropped, and one line holding all of
 * `$$…$$` is read as inline maths, where `align` cannot be set.
 */
function withDisplayFencesAlone(markdown: string): string {
  return markdown
    .split("\n")
    .map((line) => {
      const indent = /^\s*/.exec(line)?.[0] ?? "";
      const fences = line.split("$$").length - 1;
      const oneLiner = /^\s*\$\$([^$]+)\$\$\s*$/.exec(line);
      if (oneLiner) return [`${indent}$$`, `${indent}${oneLiner[1].trim()}`, `${indent}$$`].join("\n");
      if (fences !== 1 || line.trim() === "$$") return line;
      const [before, after] = line.split("$$");
      return [before, "$$", after]
        .filter((part) => part.trim() !== "")
        .map((part) => `${indent}${part.trim()}`)
        .join("\n");
    })
    .join("\n");
}

/**
 * `\require` loads a MathJax extension and typesets nothing, so it goes; a `$$…$$` pair
 * left with nothing between them goes too. Pairs are counted from the start, as
 * markdown counts them, so a close is never mistaken for an open.
 */
function withoutEmptyDisplays(markdown: string): string {
  const parts = markdown.replace(/\\require\{[^}]*\}/g, "").split("$$");
  let out = parts[0];
  for (let index = 1; index < parts.length; index += 2) {
    const inside = parts[index];
    const after = parts[index + 1];
    if (after === undefined) return `${out}$$${inside}`;
    out += inside.trim() === "" ? after : `$$${inside}$$${after}`;
  }
  return out;
}

/**
 * A display's lines take its opening fence's indentation. The textbook's working is
 * indented from its HTML while its maths is not, so a display opened inside a list item
 * closed outside it, and markdown read the rest of the text as maths.
 */
function withDisplaysIndentedAsOpened(markdown: string): string {
  let opened: string | null = null;
  return markdown
    .split("\n")
    .map((line) => {
      const fence = line.trim() === "$$";
      if (opened === null) {
        if (fence) opened = /^\s*/.exec(line)?.[0] ?? "";
        return line;
      }
      const indent = opened;
      if (fence) opened = null;
      return line.trim() === "" ? line : `${indent}${line.trimStart()}`;
    })
    .join("\n");
}

const MATH = /(\$\$[\s\S]*?\$\$|\$(?:\\\$|(?!\*\*|\n\n)[^$])+?\$)/;
const BARE_ENVIRONMENT =
  /(?<!\\)\\begin\{(array|aligned|align\*?|gathered|gather\*?|split|cases|[pbBvV]?matrix)\}[\s\S]*?\\end\{\1\}/g;

/** An environment standing in prose with no delimiter around it is display maths. */
function displayBareEnvironments(markdown: string): string {
  return markdown
    .split(MATH)
    .map((part, index) =>
      index % 2 === 1 ? part : part.replace(BARE_ENVIRONMENT, (environment) => `\n$$\n${environment}\n$$\n`),
    )
    .join("");
}
