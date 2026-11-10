"use strict";

// ── The conversation with the agent that wrote the content ─────────────────
// Select text and comment on it, or write to the agent below the content; the agent keeps its
// place between comments and carries on. It is offered only where the host passes tool calls on
// to the server (the host says so as `serverTools`), so a host without that shows the content only.
// A host that has a chat of its own says so as `message`: the page then offers only the comment
// on selected text, and sends it to that chat as a message (`ui/message`), which the host shows
// as the teacher's own.
const talk = (() => {
  const COMMENT = "comment_on_content";
  const STATE = "conversation_state";
  const CONTENT = "show_content";
  const POLL_MS = 2000;
  const MAX_COMMENT = 4000;
  const MAX_SELECTED = 1000;

  const panel = document.getElementById("conversation");
  let enabled = false;
  let hostChat = false;
  let listening = false;
  let version = null;
  let watching = false;
  let thread = null;
  let status = null;
  let input = null;
  let send = null;
  let pin = null;
  let box = null;

  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  async function call(name, args) {
    const result = await request("tools/call", { name, arguments: args || {} });
    if (result.isError) throw new Error(((result.content || [])[0] || {}).text || "The request was refused.");
    if (result.structuredContent) return result.structuredContent;
    const text = (result.content || []).find((block) => block.type === "text");
    return text ? JSON.parse(text.text) : {};
  }

  function turnView(turn) {
    const row = element("div", "turn");
    const quote = turn.highlight && turn.highlight.selected_text;
    if (quote) row.append(element("div", "quote", quote));
    row.append(element("div", "you", turn.comment));
    if (turn.summary) { const said = markdown(turn.summary); said.classList.add("agent"); row.append(said); }
    return row;
  }

  function show(state) {
    thread.replaceChildren(...(state.turns || []).map(turnView));
    const busy = state.working || state.waiting > 0;
    status.className = state.error ? "status error" : "status";
    status.textContent = state.error
      ? `The agent could not finish: ${state.error}`
      : busy ? "The agent is working on it…" : "";
  }

  // A new version is drawn as soon as it is there, without waiting for the host.
  async function refresh(state) {
    const changed = version !== null && state.version !== version;
    version = state.version;
    if (!changed) return;
    const item = contentOf(await request("tools/call", { name: CONTENT, arguments: {} }));
    if (item) render(item);
  }

  async function watch() {
    if (watching) return;
    watching = true;
    try {
      for (;;) {
        const state = await call(STATE);
        show(state);
        await refresh(state);
        if (!state.working && !state.waiting) break;
        await sleep(POLL_MS);
      }
    } catch (error) {
      status.className = "status error";
      status.textContent = error.message;
    } finally {
      watching = false;
    }
  }

  async function say(text, pointed) {
    send.disabled = true;
    try {
      await call(COMMENT, { comment: text, ...(pointed || {}) });
      status.className = "status";
      status.textContent = "The agent is working on it…";
      watch();
    } catch (error) {
      status.className = "status error";
      status.textContent = error.message;
    } finally {
      send.disabled = false;
    }
  }

  // The comment goes to the host's chat as a message, which the host shows and answers there.
  function notice(text, failed) {
    const toast = element("div", failed ? "toast error" : "toast", text);
    document.body.append(toast);
    setTimeout(() => toast.remove(), 2500);
  }

  async function tell(text, pointedAt) {
    try {
      const result = await request("ui/message", {
        role: "user",
        // Where the teacher pointed rides on the text block: a host reads a block's own _meta.
        content: [{ type: "text", text, _meta: { highlight: pointedAt || null } }],
      });
      if (result && result.isError) throw new Error("The chat could not take the comment.");
      notice("Sent to the chat.");
    } catch (error) {
      notice(error.message, true);
    }
  }

  // ── Where the teacher pointed ────────────────────────────────────────────
  function pointed() {
    const selection = window.getSelection();
    if (!selection || selection.isCollapsed || !selection.rangeCount) return null;
    const text = selection.toString().trim();
    const node = selection.anchorNode;
    const start = node && (node.nodeType === Node.TEXT_NODE ? node.parentElement : node);
    if (!text || !start || !document.getElementById("root").contains(start)) return null;
    const field = start.closest("[data-path]");
    const unit = start.closest("[data-unit]");
    return {
      rect: selection.getRangeAt(0).getBoundingClientRect(),
      selected_text: text.slice(0, MAX_SELECTED),
      ...(unit ? { unit_id: unit.dataset.unit } : {}),
      ...(field ? { path: field.dataset.path } : {}),
    };
  }

  function clear() {
    if (pin) pin.remove();
    if (box) box.remove();
    pin = box = null;
  }

  function place(node, rect) {
    node.style.left = `${Math.max(8, rect.left + window.scrollX)}px`;
    node.style.top = `${rect.bottom + window.scrollY + 6}px`;
  }

  function comment(where) {
    clear();
    const { rect, ...pointedAt } = where;
    box = element("div", "comment-box");
    const text = element("textarea");
    text.maxLength = MAX_COMMENT;
    text.placeholder = "What should change here?";
    const post = element("button", "talk", "Send comment");
    const cancel = element("button", "talk quiet", "Cancel");
    post.onclick = () => {
      if (!text.value.trim()) return;
      (hostChat ? tell : say)(text.value.trim(), pointedAt);
      clear();
    };
    cancel.onclick = clear;
    const row = element("div", "row");
    row.append(cancel, post);
    box.append(element("div", "quote", where.selected_text), text, row);
    document.body.append(box);
    place(box, rect);
    // A frame takes keystrokes only once it has focus, and the button that opened this did not give it.
    window.focus();
    text.focus();
  }

  function offer() {
    if (box && box.contains(document.activeElement)) return;
    clear();
    const where = enabled ? pointed() : null;
    if (!where) return;
    pin = element("button", "talk pin", "Comment");
    pin.onmousedown = (event) => event.preventDefault();
    pin.onclick = () => comment(where);
    document.body.append(pin);
    place(pin, where.rect);
  }

  function listen() {
    document.addEventListener("mouseup", () => setTimeout(offer, 0));
    document.addEventListener("keyup", (event) => { if (event.key === "Escape") clear(); });
  }

  function build() {
    input = element("textarea");
    input.maxLength = MAX_COMMENT;
    input.placeholder = "Ask the agent to change something, or select text above to comment on it.";
    send = element("button", "talk", "Send");
    send.onclick = () => {
      const text = input.value.trim();
      if (!text) return;
      input.value = "";
      say(text, null);
    };
    thread = element("div", "turns");
    status = element("div", "status");
    panel.replaceChildren(element("h2", "", "Conversation"), thread, status, input, send);
    panel.hidden = false;
    listen();
  }

  return {
    enable(capabilities) {
      hostChat = Boolean(capabilities && capabilities.message);
      enabled = hostChat || Boolean(capabilities && capabilities.serverTools);
      if (!enabled || listening) return;
      listening = true;
      if (hostChat) listen();
      else build();
    },
    rendered(item) {
      if (!enabled) return;
      if (hostChat) { clear(); return; }
      if (version === null) version = item.version;
      clear();
      call(STATE).then((state) => { show(state); version = state.version; if (state.working || state.waiting) watch(); }).catch(() => {});
    },
  };
})();
