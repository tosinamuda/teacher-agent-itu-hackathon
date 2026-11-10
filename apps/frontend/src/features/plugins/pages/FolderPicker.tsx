import { InputHTMLAttributes, useRef } from "react";

import { Button } from "@/shared/components/ui/Button";

import { filesOfFolder } from "../lib/folderFiles";
import type { PluginFiles } from "../types";

/** React's input types do not know the folder-picking attribute. */
const folderAttributes = {
  webkitdirectory: "",
} as InputHTMLAttributes<HTMLInputElement>;

type Props = {
  label: string;
  disabled?: boolean;
  title?: string;
  busy?: boolean;
  variant?: "primary" | "outline";
  /** Called with the picked folder's files; a folder that cannot be read raises `onProblem`. */
  onFiles: (files: PluginFiles) => void;
  onProblem: (problem: string) => void;
};

/** A button that opens the folder picker and hands on the folder's text files. */
export function FolderPicker({
  label,
  disabled,
  title,
  busy,
  variant = "outline",
  onFiles,
  onProblem,
}: Props) {
  const input = useRef<HTMLInputElement>(null);

  const picked = async (list: FileList | null) => {
    if (!list || list.length === 0) return;
    try {
      onFiles(await filesOfFolder(Array.from(list)));
    } catch (error) {
      onProblem(error instanceof Error ? error.message : String(error));
    } finally {
      if (input.current) input.current.value = "";
    }
  };

  return (
    <>
      <input
        ref={input}
        type="file"
        multiple
        hidden
        data-testid="plugin-folder-input"
        {...folderAttributes}
        onChange={(event) => void picked(event.target.files)}
      />
      <Button
        type="button"
        size="sm"
        variant={variant}
        disabled={disabled}
        isLoading={busy}
        title={title}
        onClick={() => input.current?.click()}
      >
        {label}
      </Button>
    </>
  );
}
