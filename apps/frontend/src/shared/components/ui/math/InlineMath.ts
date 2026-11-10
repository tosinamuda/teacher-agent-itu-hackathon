import { mergeAttributes, Node } from "@tiptap/core";
import { ReactNodeViewRenderer } from "@tiptap/react";

import { InlineMathView } from "./InlineMathView";

/**
 * An inline atomic math node. Stores LaTeX in `latex`, renders/edits in place as an
 * embedded MathLive field (see InlineMathView), and serialises to `$latex$` so the
 * content stays in the Markdown + LaTeX format the generation pipeline and pack
 * renderer expect.
 */
export const InlineMath = Node.create({
  name: "inlineMath",
  group: "inline",
  inline: true,
  atom: true,
  selectable: true,

  addAttributes() {
    return {
      latex: {
        default: "",
        parseHTML: (element) => element.getAttribute("data-latex") ?? "",
        renderHTML: (attributes) => ({ "data-latex": attributes.latex }),
      },
    };
  },

  parseHTML() {
    return [{ tag: "span[data-inline-math]" }];
  },

  renderHTML({ HTMLAttributes }) {
    return ["span", mergeAttributes(HTMLAttributes, { "data-inline-math": "" })];
  },

  addNodeView() {
    // The embedded MathLive field owns its own editing; ProseMirror must not also
    // process events that originate inside it.
    return ReactNodeViewRenderer(InlineMathView, { stopEvent: () => true });
  },

  addStorage() {
    return {
      markdown: {
        serialize(state: { write: (text: string) => void }, node: { attrs: { latex: string } }) {
          state.write(`$${node.attrs.latex}$`);
        },
        parse: {
          // Inline `$...$` round-trips saved content back into editable math nodes:
          // a tokeniser rule recognises the span, and a renderer emits the HTML the
          // node's parseHTML (`span[data-inline-math]`) reattaches to — tiptap-markdown
          // parses by rendering Markdown to HTML, so without the renderer the maths is
          // dropped on load.
          setup(markdownit: {
            inline: { ruler: { before: (a: string, b: string, fn: unknown) => void } };
            renderer: { rules: Record<string, (tokens: { content: string }[], idx: number) => string> };
          }) {
            const rule = (
              state: {
                src: string;
                pos: number;
                posMax: number;
                push: (type: string, tag: string, nesting: number) => { content: string; markup: string; attrs: [string, string][] };
              },
              silent: boolean
            ) => {
              if (state.src[state.pos] !== "$") return false;
              const start = state.pos + 1;
              let end = start;
              while (end < state.posMax && state.src[end] !== "$") end += 1;
              if (end >= state.posMax || end === start) return false;
              if (!silent) {
                const latex = state.src.slice(start, end);
                const token = state.push("inlineMath", "span", 0);
                token.content = latex;
                token.attrs = [["latex", latex]];
                token.markup = "$";
              }
              state.pos = end + 1;
              return true;
            };
            markdownit.inline.ruler.before("escape", "inlineMath", rule);
            markdownit.renderer.rules.inlineMath = (tokens, idx) => {
              const latex = tokens[idx].content
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/"/g, "&quot;");
              return `<span data-inline-math data-latex="${latex}"></span>`;
            };
          },
        },
      },
    };
  },
});
