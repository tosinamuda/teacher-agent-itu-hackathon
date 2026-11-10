/**
 * Fractions in prose, marked as maths so KaTeX stacks them.
 *
 * The class-test generator writes a fraction however the model likes: `8/5`, `⁸⁄₅`,
 * `8⁄5` or `⅗`. A font draws each of the last three as a small slanted glyph, and all
 * four read worse than the stacked fraction the lesson notes set, in a test about
 * numerators and denominators. Maths already delimited is left as written.
 */
export function withFractionsAsMath(text: string): string {
  return text
    .split(DELIMITED_MATH)
    .map((part, index) => (index % 2 === 1 ? part : fractionsMarked(part)))
    .join("");
}

const DELIMITED_MATH = /(\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]|\$\$[\s\S]*?\$\$|\$[^$\n]+?\$)/;

const SUPERSCRIPT_DIGITS = "⁰¹²³⁴⁵⁶⁷⁸⁹";
const SUBSCRIPT_DIGITS = "₀₁₂₃₄₅₆₇₈₉";
const VULGAR_FRACTIONS: Record<string, [number, number]> = {
  "½": [1, 2],
  "⅓": [1, 3],
  "⅔": [2, 3],
  "¼": [1, 4],
  "¾": [3, 4],
  "⅕": [1, 5],
  "⅖": [2, 5],
  "⅗": [3, 5],
  "⅘": [4, 5],
  "⅙": [1, 6],
  "⅚": [5, 6],
  "⅐": [1, 7],
  "⅛": [1, 8],
  "⅜": [3, 8],
  "⅝": [5, 8],
  "⅞": [7, 8],
  "⅑": [1, 9],
  "⅒": [1, 10],
};

const SCRIPT_FRACTION = new RegExp(`([${SUPERSCRIPT_DIGITS}]+)[⁄/]([${SUBSCRIPT_DIGITS}]+)`, "g");
const SLASHED_FRACTION = /(?<![\w./\\])(\d+)[⁄/](\d+)(?![\w/]|\.\d)/g;
const VULGAR_FRACTION = new RegExp(`[${Object.keys(VULGAR_FRACTIONS).join("")}]`, "g");

function fractionsMarked(prose: string): string {
  return prose
    .replace(SCRIPT_FRACTION, (_whole, top: string, bottom: string) =>
      fraction(digitsOf(top, SUPERSCRIPT_DIGITS), digitsOf(bottom, SUBSCRIPT_DIGITS)),
    )
    .replace(SLASHED_FRACTION, (_whole, top: string, bottom: string) => fraction(top, bottom))
    .replace(VULGAR_FRACTION, (glyph) => {
      const [top, bottom] = VULGAR_FRACTIONS[glyph];
      return fraction(String(top), String(bottom));
    });
}

function digitsOf(script: string, alphabet: string): string {
  return [...script].map((glyph) => String(alphabet.indexOf(glyph))).join("");
}

function fraction(top: string, bottom: string): string {
  return `\\(\\frac{${top}}{${bottom}}\\)`;
}
