import katex from "katex";

/**
 * TeX as KaTeX reads it.
 *
 * The textbook was typeset for MathJax, and its records lost escapes on the way into
 * JSON and Python strings; the model copies both into what it writes. Each rewrite here
 * keeps what the author meant and changes only how it is spelled.
 */
export function asKatex(tex: string): string {
  return withRowBreaks(
    withColumnSpecs(withEnclosures(withDoubledEscapesHalved(withEatenEscapes(tex)))),
  ).replace(/\\require\{[^}]*\}/g, "");
}

const known = new Map<string, boolean>();

/** Whether KaTeX has a command of this name: it names the ones it lacks as undefined. */
export function isKatexCommand(name: string): boolean {
  const cached = known.get(name);
  if (cached !== undefined) return cached;
  let found = true;
  try {
    katex.renderToString(`\\${name}`, { throwOnError: true, strict: "ignore" });
  } catch (error) {
    found = !String((error as Error).message).includes("Undefined control sequence");
  }
  known.set(name, found);
  return found;
}

/** The escape letter a control character stands in for, when a decode ate `\b`, `\t`… */
const EATEN: Record<string, string> = {
  "\b": "b",
  "\f": "f",
  "\x07": "a",
  "\x0b": "v",
  "\r": "r",
  "\t": "t",
  "\n": "n",
};

/**
 * Backspace, form feed, bell and vertical tab are never meant in maths, so each goes
 * back to its escape. Tab, return and newline are real whitespace too, so they go back
 * only where the letters after them finish a command KaTeX knows — two letters at
 * least after a newline, as a line of maths may begin with a variable `u`.
 */
const EATEN_COMMAND = new RegExp(`[${Object.keys(EATEN).join("")}]([A-Za-z]+)`, "g");

function withEatenEscapes(tex: string): string {
  return tex
    .replace(EATEN_COMMAND, (whole, letters: string) => {
      const letter = EATEN[whole[0]];
      const always = "bfav".includes(letter);
      const enough = letter !== "n" || letters.length >= 2;
      return always || (enough && isKatexCommand(letter + letters))
        ? `\\${letter}${letters}`
        : whole;
    })
    .replace(/(?<![\\A-Za-z])ewline(?![A-Za-z])/g, "\\newline");
}

/** `\\frac` is a line break and the word "frac" to TeX; a string escaped twice meant `\frac`. */
function withDoubledEscapesHalved(tex: string): string {
  return tex.replace(/(?<!\\)\\\\([A-Za-z]{2,})/g, (whole, name: string) =>
    isKatexCommand(name) ? `\\${name}` : whole,
  );
}

/** The KaTeX spelling of each MathJax `\enclose` notation it has an equivalent for. */
const ENCLOSURES: Record<string, (body: string) => string> = {
  longdiv: (body) => `\\overline{\\smash{)}\\,${body}}`,
  circle: (body) => `\\text{\\textcircled{$${body}$}}`,
  box: (body) => `\\boxed{${body}}`,
  roundedbox: (body) => `\\boxed{${body}}`,
  updiagonalstrike: (body) => `\\cancel{${body}}`,
  downdiagonalstrike: (body) => `\\bcancel{${body}}`,
};

/**
 * MathJax's `\enclose{notation}[attributes]{body}`. A notation KaTeX has no equivalent
 * for keeps its body; a `mathcolor` attribute keeps its colour.
 */
function withEnclosures(tex: string): string {
  let out = "";
  let rest = tex;
  for (;;) {
    const found = /\\enclose\{([^}]*)\}(?:\[([^\]]*)\])?\{/.exec(rest);
    if (!found) return out + rest;
    const end = closingBrace(rest, found.index + found[0].length);
    if (end < 0) return out + rest;
    const body = rest.slice(found.index + found[0].length, end);
    const notation = found[1].split(/[\s,]+/).find((name) => name in ENCLOSURES);
    const drawn = notation ? ENCLOSURES[notation](body) : `{${body}}`;
    const colour = /mathcolor\s*=\s*"?([#\w]+)"?/.exec(found[2] ?? "")?.[1];
    out += rest.slice(0, found.index) + (colour ? `\\textcolor{${colour}}{${drawn}}` : drawn);
    rest = rest.slice(end + 1);
  }
}

/** The index of the `}` closing a group whose body starts at `start`, or -1. */
function closingBrace(tex: string, start: number): number {
  let depth = 1;
  for (let index = start; index < tex.length; index += 1) {
    const char = tex[index];
    if (char === "\\") index += 1;
    else if (char === "{") depth += 1;
    else if (char === "}" && (depth -= 1) === 0) return index;
  }
  return -1;
}

/** MathJax reads `{array}{2}` as two columns; KaTeX wants a letter for each. */
function withColumnSpecs(tex: string): string {
  return tex.replace(/\\begin\{array\}\{(\d+)\}/g, (_whole, count: string) => {
    return `\\begin{array}{${"l".repeat(Number(count))}}`;
  });
}

const ENVIRONMENT =
  /\\begin\{(array|aligned|align\*?|gathered|gather\*?|split|cases|[pbBvV]?matrix)\}((?:\{[lcr|\s]*\})?)([\s\S]*?)\\end\{\1\}/g;

/**
 * Inside an environment MathJax takes `\newline` as the row break `\\`. A row the
 * author ended at `\hline` or at the end without one — or with a lone `\`, a control
 * space — has the `\\` it was meant to have.
 */
function withRowBreaks(tex: string): string {
  return tex.replace(ENVIRONMENT, (_whole, name: string, columns: string, body: string) => {
    const rows = body
      .replace(/\\newline(?![A-Za-z])/g, "\\\\")
      .replace(/(?<!\\)\\(?!\\)\s*(?=\\hline)/g, "\\\\ ")
      .replace(/(?<!\\)\\\s*$/, "\\\\ ")
      .split(/\s*\\hline\s*/);
    const ruled = rows.map((row, index) => {
      const before = (rows[index - 1] ?? "").trim();
      if (index === 0) return row;
      const rule = before === "" || before.endsWith("\\\\") ? " \\hline" : " \\\\ \\hline";
      return row === "" ? rule : `${rule} ${row}`;
    });
    return `\\begin{${name}}${columns}${ruled.join("")}\\end{${name}}`;
  });
}
