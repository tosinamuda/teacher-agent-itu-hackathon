import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  listChats,
  sendMessage,
  startChat,
  stopChat,
  type ChatHighlight,
} from "./chatApi";

/** The chats on a piece of content, read again now and then while the panel is open. */
export function useContentChats(contentId: string, open: boolean) {
  return useQuery({
    queryKey: ["contentChats", contentId],
    queryFn: () => listChats(contentId),
    enabled: open,
    refetchInterval: open ? 10_000 : false,
  });
}

export function useStartChat(contentId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (title?: string) => startChat(contentId, title),
    onSuccess: () =>
      void queryClient.invalidateQueries({
        queryKey: ["contentChats", contentId],
      }),
  });
}

export function useSendMessage(contentId: string) {
  return useMutation({
    mutationFn: ({
      chatId,
      text,
      highlight,
    }: {
      chatId: string;
      text: string;
      highlight?: ChatHighlight | null;
    }) => sendMessage(contentId, chatId, text, highlight),
  });
}

export function useStopChat(contentId: string) {
  return useMutation({
    mutationFn: (chatId: string) => stopChat(contentId, chatId),
  });
}
