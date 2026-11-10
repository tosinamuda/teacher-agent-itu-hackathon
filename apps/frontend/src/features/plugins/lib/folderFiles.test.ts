import { describe, expect, it } from "vitest";

import { filesOfFolder, MAX_FILES, pathInFolder } from "./folderFiles";

const file = (path: string, text = "x") => ({
  webkitRelativePath: path,
  name: path.split("/").at(-1) as string,
  size: text.length,
  text: async () => text,
});

describe("pathInFolder", () => {
  it("leaves off the folder's own name", () => {
    expect(pathInFolder(file("plugin/skills/a/SKILL.md"))).toBe(
      "skills/a/SKILL.md",
    );
  });

  it("keeps a lone file's name", () => {
    expect(pathInFolder({ webkitRelativePath: "", name: "plugin.json" })).toBe(
      "plugin.json",
    );
  });
});

describe("filesOfFolder", () => {
  it("reads each file's text by its path inside the folder", async () => {
    const files = await filesOfFolder([
      file("p/plugin.json", "{}"),
      file("p/skills/a/SKILL.md", "hi"),
    ]);

    expect(files).toEqual({ "plugin.json": "{}", "skills/a/SKILL.md": "hi" });
  });

  it("leaves out hidden files and node_modules", async () => {
    const files = await filesOfFolder([
      file("p/plugin.json"),
      file("p/.DS_Store"),
      file("p/.git/config"),
      file("p/node_modules/x/index.js"),
    ]);

    expect(Object.keys(files)).toEqual(["plugin.json"]);
  });

  it("refuses an empty folder and a folder with too many files", async () => {
    await expect(filesOfFolder([])).rejects.toThrow("no files");
    const many = Array.from({ length: MAX_FILES + 1 }, (_, i) =>
      file(`p/f${i}.md`),
    );
    await expect(filesOfFolder(many)).rejects.toThrow("more than");
  });
});
