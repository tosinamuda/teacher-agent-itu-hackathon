import { NodeViewWrapper, type NodeViewProps } from "@tiptap/react";

import { MathField } from "../MathField";

/**
 * The in-editor view of an inline math node: a MathLive field embedded directly in
 * the line of text. It renders the formatted maths in place and is edited where it
 * sits — click it and use MathLive's symbol toolbar — so there is no popover and no
 * separate preview. A freshly inserted (empty) node is focused for immediate entry;
 * the small × (shown on hover) removes it.
 */
export function InlineMathView({ node, updateAttributes, deleteNode, selected }: NodeViewProps) {
  const latex = (node.attrs.latex as string) ?? "";

  return (
    <NodeViewWrapper
      as="span"
      contentEditable={false}
      className={`group relative inline-flex items-center rounded-sm align-middle ${
        selected ? "ring-1 ring-(--accent)" : ""
      }`}
    >
      <MathField
        inline
        autoFocus={latex.trim() === ""}
        initialLatex={latex}
        onChange={(value) => updateAttributes({ latex: value })}
      />
      <button
        type="button"
        aria-label="Remove equation"
        onMouseDown={(event) => event.preventDefault()}
        onClick={() => deleteNode()}
        className="ml-0.5 hidden text-xs leading-none text-(--muted) hover:text-(--danger) group-hover:inline"
      >
        ×
      </button>
    </NodeViewWrapper>
  );
}
