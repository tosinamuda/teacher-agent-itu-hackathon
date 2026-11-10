import type { Options } from "react-markdown";
import rehypeKatex from "rehype-katex";

import { asKatex } from "@/shared/utils/katexDialect";

interface HastNode {
  type: string;
  tagName?: string;
  value?: string;
  properties?: { className?: unknown };
  children?: HastNode[];
}

/**
 * Indentation is layout here, never code: the textbook's working comes indented from
 * its HTML, and four spaces made it a monospaced block. Fenced code still reads as code.
 */
export function remarkNoIndentedCode(this: { data(): object }) {
  const data = this.data() as { micromarkExtensions?: object[] };
  data.micromarkExtensions = [
    ...(data.micromarkExtensions ?? []),
    { disable: { null: ["codeIndented"] } },
  ];
}

/** Each piece of maths, rewritten for KaTeX before KaTeX reads it. */
function rehypeKatexDialect() {
  return (tree: HastNode) => rewriteMath(tree);
}

function rewriteMath(node: HastNode): void {
  const classes = node.properties?.className;
  if (
    node.tagName === "code" &&
    Array.isArray(classes) &&
    classes.includes("language-math")
  ) {
    node.children = [{ type: "text", value: asKatex(textOf(node)) }];
    return;
  }
  node.children?.forEach(rewriteMath);
}

function textOf(node: HastNode): string {
  return node.value ?? (node.children ?? []).map(textOf).join("");
}

/**
 * Maths that still cannot be set shows its source in the text's own colour: red read
 * as the reader's mistake. KaTeX keeps its `katex-error` class and message for review.
 */
export const mathRehypePlugins: NonNullable<Options["rehypePlugins"]> = [
  rehypeKatexDialect,
  [rehypeKatex, { strict: "ignore", errorColor: "inherit" }],
];
