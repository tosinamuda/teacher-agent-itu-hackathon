// @vitest-environment jsdom
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { DownloadFileButton } from "./DownloadFileButton";

const { downloadContentFile, saveBlob } = vi.hoisted(() => ({
  downloadContentFile: vi.fn(),
  saveBlob: vi.fn(),
}));
vi.mock("../api/content", () => ({ downloadContentFile }));
vi.mock("@/shared/lib/saveBlob", () => ({ saveBlob }));

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

const shown = () =>
  render(
    <QueryClientProvider client={new QueryClient()}>
      <DownloadFileButton contentId="AT-1" />
    </QueryClientProvider>,
  );

it("saves the file under the name the server gave it", async () => {
  const blob = new Blob(["file"]);
  downloadContentFile.mockResolvedValue({ blob, filename: "AT-1.pptx" });
  shown();

  fireEvent.click(screen.getByRole("button", { name: "Download file" }));

  await waitFor(() => expect(saveBlob).toHaveBeenCalledWith(blob, "AT-1.pptx"));
  expect(downloadContentFile).toHaveBeenCalledWith("AT-1");
});

it("tells the teacher when the file could not be prepared", async () => {
  downloadContentFile.mockRejectedValue(new Error("down"));
  shown();

  fireEvent.click(screen.getByRole("button", { name: "Download file" }));

  expect(await screen.findByRole("alert")).toHaveProperty(
    "textContent",
    "The file could not be prepared. Try again.",
  );
  expect(saveBlob).not.toHaveBeenCalled();
});
