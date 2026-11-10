import { EditorContent, useEditor, type Editor } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import { Markdown } from "tiptap-markdown";

import { InlineMath } from "./math/InlineMath";

/**
 * A rich-text WYSIWYG editor for prose + mathematics. Formatting and an "Insert
 * equation" control live in a toolbar; maths is an inline MathLive field edited in
 * place with its symbol toolbar (see InlineMathView) — what you edit is the
 * formatted content, not raw LaTeX. Reads/writes Markdown + `$latex$`, the format
 * the generation pipeline and pack renderer use.
 */
export function RichContentEditor({
  value,
  onChange,
  placeholder,
  rows,
}: {
  value: string;
  onChange: (markdown: string) => void;
  placeholder?: string;
  /** Approximate visible lines, mapped to a min-height (kept for call-site parity). */
  rows?: number;
}) {
  const minHeight = rows ? rows * 24 + 16 : 80;
  const editor = useEditor({
    extensions: [
      StarterKit,
      Markdown.configure({ html: false, transformPastedText: true, breaks: true }),
      InlineMath,
    ],
    content: value,
    editorProps: {
      attributes: {
        class:
          "prose prose-sm max-w-none focus:outline-none text-(--ink) px-3 py-2",
        style: `min-height:${minHeight}px`,
        ...(placeholder ? { "data-placeholder": placeholder } : {}),
      },
    },
    onUpdate: ({ editor: ed }) => {
      const storage = ed.storage as { markdown?: { getMarkdown: () => string } };
      onChange(storage.markdown?.getMarkdown() ?? "");
    },
  });

  if (!editor) {
    return <div className="border border-(--line-2) px-3 py-2 text-xs text-(--muted)">Loading editor…</div>;
  }

  return (
    <div className="border border-(--line-2) bg-(--surface) focus-within:border-(--accent)">
      <Toolbar editor={editor} />
      <EditorContent editor={editor} />
    </div>
  );
}

const btn =
  "px-2 py-1 text-xs font-semibold text-(--ink-2) hover:bg-(--surface-2) data-[active=true]:bg-(--accent-soft) data-[active=true]:text-(--accent-deep)";

function Toolbar({ editor }: { editor: Editor }) {
  const cmd = (run: () => void) => (event: React.MouseEvent) => {
    event.preventDefault();
    run();
  };
  return (
    <div className="flex flex-wrap items-center gap-0.5 border-b border-(--line) bg-(--surface-2) px-1 py-1">
      <button
        type="button"
        className={btn}
        data-active={editor.isActive("bold")}
        onMouseDown={cmd(() => editor.chain().focus().toggleBold().run())}
      >
        B
      </button>
      <button
        type="button"
        className={`${btn} italic`}
        data-active={editor.isActive("italic")}
        onMouseDown={cmd(() => editor.chain().focus().toggleItalic().run())}
      >
        I
      </button>
      <button
        type="button"
        className={btn}
        data-active={editor.isActive("bulletList")}
        onMouseDown={cmd(() => editor.chain().focus().toggleBulletList().run())}
      >
        • List
      </button>
      <button
        type="button"
        className={btn}
        data-active={editor.isActive("orderedList")}
        onMouseDown={cmd(() => editor.chain().focus().toggleOrderedList().run())}
      >
        1. List
      </button>
      <span className="mx-1 h-4 w-px bg-(--line)" />
      <button
        type="button"
        className={`${btn} text-(--accent-deep)`}
        onMouseDown={cmd(() =>
          editor.chain().focus().insertContent({ type: "inlineMath", attrs: { latex: "" } }).run()
        )}
      >
        ∑ Insert equation
      </button>
    </div>
  );
}
