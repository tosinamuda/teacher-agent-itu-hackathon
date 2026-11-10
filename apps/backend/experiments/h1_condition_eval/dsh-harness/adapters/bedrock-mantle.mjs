/**
 * A DeepSeek Harness LLM adapter for Bedrock mantle's OpenAI-compatible endpoint.
 *
 * Loaded by absolute path from cordis.yml, against the STOCK pip-installed
 * runtime. Nothing is compiled and no runtime is rebuilt: the packaged
 * executable mounts a plugin named by path, and `ctx.llm.registerAdapter`
 * accepts an adapter built from this directory's own copy of
 * `@deepseek-ai/dsh-llm` — the registry duck-types rather than checking class
 * identity. Both were verified against the shipped binary before this was
 * written; see README.md.
 *
 * WHY THIS EXISTS. `dsh-llm-deepseek` cannot talk to mantle. Its SSE parser
 * requires the literal `data: [DONE]` and raises STREAM_CLOSED without it,
 * which is a deliberate truncation check: absent a terminal sentinel, a
 * connection dropped mid-response is indistinguishable from a complete one.
 * Mantle never sends it — verified on the wire, it emits a final chunk
 * carrying `finish_reason` and closes:
 *
 *     data: {"choices":[{"delta":{},"finish_reason":"stop",...}],...}
 *     <EOF>
 *
 * So `finish_reason` is the end-of-stream marker here. The truncation check is
 * KEPT in the weaker form the transport allows: EOF having seen no
 * `finish_reason` is still an error. A generation truncated silently scores as
 * a bad one rather than a failed one, which is the failure mode this study can
 * least afford.
 *
 * Scope is deliberately narrower than the DeepSeek adapter: text, reasoning and
 * tool calls, no images, no thinking-mode toggles, no dynamic catalogue. The
 * generator sends text and reads text.
 */

import { EventSourceParserStream } from 'eventsource-parser/stream'
import { LlmAdapter, LlmError } from '@deepseek-ai/dsh-llm'

/** The provider route this plugin owns. */
const PROVIDER = 'bedrock-mantle'

/** Synthesised locally; mantle never sends it. `finish_reason` stands in. */
const DONE = Symbol('done')

/** Flatten a harness content-block list to plain text. */
function flattenText(blocks) {
  return (blocks ?? [])
    .filter((block) => block.type === 'text')
    .map((block) => block.text)
    .join('')
}

/**
 * Harness messages to OpenAI chat-completions messages.
 *
 * Tool results ride inside user messages in the harness vocabulary and must
 * leave as their own `role: 'tool'` messages, which is the one non-obvious
 * mapping — see `llm-deepseek/src/serialize.ts`, which does the same.
 */
function serializeMessages(messages) {
  const wire = []
  for (const message of messages) {
    if (message.role === 'system') {
      wire.push({ role: 'system', content: flattenText(message.content) })
      continue
    }
    if (message.role === 'assistant') {
      const toolCalls = (message.content ?? [])
        .filter((block) => block.type === 'tool-call')
        .map((block) => ({
          id: block.id,
          type: 'function',
          function: { name: block.name, arguments: block.arguments },
        }))
      const text = flattenText(message.content)
      // An assistant turn with neither content nor tool_calls is rejected 400
      // by OpenAI-shaped APIs, so an empty one is sent as empty string.
      wire.push({
        role: 'assistant',
        content: text,
        ...(toolCalls.length > 0 ? { tool_calls: toolCalls } : {}),
      })
      continue
    }
    const results = (message.content ?? []).filter((block) => block.type === 'tool-result')
    const text = flattenText(message.content)
    if (text.length > 0 || results.length === 0) {
      wire.push({ role: 'user', content: text })
    }
    for (const result of results) {
      wire.push({
        role: 'tool',
        tool_call_id: result.toolCallId,
        content: flattenText(result.content),
      })
    }
  }
  return wire
}

/** Harness tool schemas to the OpenAI `tools` field. */
function serializeTools(tools) {
  if (!tools || tools.length === 0) return undefined
  return tools.map((tool) => ({
    type: 'function',
    function: { name: tool.name, description: tool.description, parameters: tool.parameters },
  }))
}

/** Provider usage to the harness's DISJOINT token accounting. */
function translateUsage(usage) {
  if (!usage) return undefined
  const cacheRead = usage.prompt_tokens_details?.cached_tokens ?? 0
  return {
    // `prompt_tokens` folds cache hits in; the harness wants them separate.
    inputTokens: Math.max(0, (usage.prompt_tokens ?? 0) - cacheRead),
    outputTokens: usage.completion_tokens ?? 0,
    ...(cacheRead > 0 ? { cacheReadTokens: cacheRead } : {}),
    ...(usage.completion_tokens_details?.reasoning_tokens
      ? { reasoningTokens: usage.completion_tokens_details.reasoning_tokens }
      : {}),
  }
}

/**
 * A tool name with gpt-oss harmony control tokens removed.
 *
 * Observed on mantle in multi-turn agent loops, never in a single-turn call:
 * `check_sections<|channel|>commentary` and `str_replace_editor<|channel|>commentary`
 * arrive as the function NAME. The token is gpt-oss's channel marker surviving
 * whatever unwraps the harmony format upstream — it arrives concatenated, not as
 * a separate delta, so it is not this adapter mis-joining fragments. DeepSeek's
 * own endpoint never produces it.
 *
 * Passing it through means the harness looks up a tool that does not exist and
 * the turn is wasted; the model then flails, which is what a 539-second run and
 * an empty pack looked like from the outside. Trimming at the first token yields
 * the name the model meant.
 */
function toolName(raw) {
  const cut = String(raw ?? '').indexOf('<|')
  return cut === -1 ? String(raw ?? '') : String(raw).slice(0, cut)
}

/** Provider finish_reason to the harness's FinishReason. */
function translateFinish(reason) {
  if (reason === 'tool_calls') return { kind: 'tool-calls' }
  if (reason === 'length') return { kind: 'max-tokens' }
  return { kind: 'stop' }
}

/**
 * Decode the SSE byte stream into payloads, terminated by `finish_reason`.
 * Yields {@link DONE} last so the caller owns final flushing.
 */
async function* parseSse(stream) {
  const events = stream.pipeThrough(new TextDecoderStream()).pipeThrough(new EventSourceParserStream())
  let finished = false
  for await (const { data } of events) {
    if (data === '[DONE]') { yield DONE; return }
    let chunk
    try {
      chunk = JSON.parse(data)
    } catch {
      throw new LlmError(`malformed SSE payload: ${data.slice(0, 120)}`, 'MALFORMED_RESPONSE')
    }
    if ((chunk.choices ?? []).some((choice) => choice.finish_reason != null)) finished = true
    yield chunk
  }
  if (!finished) throw new LlmError('SSE stream ended without finish_reason', 'STREAM_CLOSED')
  yield DONE
}

/**
 * Payloads to StreamChunks.
 *
 * `block-end`, `usage` and `finish` are all deferred to the terminal marker:
 * the protocol requires usage BEFORE finish and nothing after it, and a
 * provider may send trailing usage-only chunks.
 */
async function* translate(payloads) {
  let nextIndex = 0
  let textBlock
  let reasoningBlock
  const toolBlocks = new Map()
  const order = []
  let pendingFinish
  let pendingUsage

  const open = (kind) => {
    const block = { index: nextIndex++, kind, text: '', callId: '', name: '' }
    order.push(block)
    return block
  }
  const close = (block) => {
    if (block.kind === 'text') return { type: 'text', text: block.text }
    if (block.kind === 'reasoning') return { type: 'reasoning', text: block.text }
    return { type: 'tool-call', id: block.callId, name: block.name, arguments: block.text }
  }

  for await (const payload of payloads) {
    if (payload === DONE) {
      for (const block of order) yield { type: 'block-end', index: block.index, block: close(block) }
      if (pendingUsage) yield { type: 'usage', usage: pendingUsage }
      const reason = pendingFinish ?? { kind: 'stop' }
      // A completed response with no content at all is a degenerate provider
      // result, not a successful empty message.
      yield {
        type: 'finish',
        reason: reason.kind === 'stop' && order.length === 0
          ? { kind: 'error', failure: { message: 'model returned a completed response with no content', code: 'EMPTY_RESPONSE' } }
          : reason,
      }
      return
    }

    if (payload.usage) pendingUsage = translateUsage(payload.usage)

    for (const choice of payload.choices ?? []) {
      const delta = choice.delta ?? {}

      const reasoning = delta.reasoning_content ?? delta.reasoning
      if (typeof reasoning === 'string' && reasoning.length > 0) {
        if (!reasoningBlock) {
          reasoningBlock = open('reasoning')
          yield { type: 'block-start', index: reasoningBlock.index, blockType: 'reasoning' }
        }
        reasoningBlock.text += reasoning
        yield { type: 'reasoning-delta', index: reasoningBlock.index, text: reasoning }
      }

      if (typeof delta.content === 'string' && delta.content.length > 0) {
        if (!textBlock) {
          textBlock = open('text')
          yield { type: 'block-start', index: textBlock.index, blockType: 'text' }
        }
        textBlock.text += delta.content
        yield { type: 'text-delta', index: textBlock.index, text: delta.content }
      }

      for (const call of delta.tool_calls ?? []) {
        // Index by the provider's tool-call slot, not by arrival: fragments of
        // one call arrive across many chunks and must reuse one block index.
        const slot = call.index ?? 0
        let block = toolBlocks.get(slot)
        if (!block) {
          block = open('tool-call')
          toolBlocks.set(slot, block)
          yield { type: 'block-start', index: block.index, blockType: 'tool-call' }
        }
        if (call.id) block.callId = call.id
        if (call.function?.name) block.name = toolName(call.function.name)
        const argumentsDelta = call.function?.arguments ?? ''
        block.text += argumentsDelta
        yield {
          type: 'tool-call-delta',
          index: block.index,
          id: block.callId,
          ...(call.function?.name ? { name: toolName(call.function.name) } : {}),
          // RAW JSON string fragments, end to end. Never parsed here.
          argumentsDelta,
        }
      }

      if (choice.finish_reason != null) pendingFinish = translateFinish(choice.finish_reason)
    }
  }
}

class BedrockMantleAdapter extends LlmAdapter {
  constructor(resolve) {
    super()
    this.resolve = resolve
  }

  providerInfo(provider) {
    return { id: provider, name: 'Bedrock mantle' }
  }

  async *stream(options) {
    const { baseURL, apiKey } = this.resolve()
    if (options.stop && options.stop.length > 0) {
      // Sanctioned path for a field this adapter will not silently drop.
      throw new LlmError('bedrock-mantle: stop sequences are not supported', 'UNSUPPORTED')
    }

    const messages = serializeMessages(options.messages)
    if (options.system) messages.unshift({ role: 'system', content: options.system })

    let response
    try {
      response = await fetch(`${baseURL.replace(/\/$/, '')}/chat/completions`, {
        method: 'POST',
        headers: { 'content-type': 'application/json', authorization: `Bearer ${apiKey}` },
        body: JSON.stringify({
          model: options.model,
          messages,
          stream: true,
          ...(options.maxTokens ? { max_tokens: options.maxTokens } : {}),
          ...(options.temperature != null ? { temperature: options.temperature } : {}),
          ...(serializeTools(options.tools) ? { tools: serializeTools(options.tools) } : {}),
        }),
        signal: options.signal,
      })
    } catch (cause) {
      throw new LlmError(`bedrock-mantle: request failed: ${cause?.message ?? cause}`, 'NETWORK_ERROR')
    }

    if (!response.ok || !response.body) {
      const body = await response.text().catch(() => '')
      throw new LlmError(
        `bedrock-mantle: HTTP ${response.status}: ${body.slice(0, 300)}`,
        response.status === 401 || response.status === 403 ? 'INVALID_CREDENTIAL' : 'PROVIDER_ERROR',
      )
    }

    yield* translate(parseSse(response.body))
  }
}

export const name = 'llm-bedrock-mantle'
export const inject = ['llm']

export function apply(ctx, config = {}) {
  const resolve = () => {
    const baseURL = config.baseURL ?? process.env.BEDROCK_MANTLE_BASE_URL
    const apiKey = config.apiKey ?? process.env[config.apiKeyEnv ?? 'BEDROCK_MANTLE_API_KEY']
    if (!baseURL) throw new LlmError('bedrock-mantle: no baseURL configured', 'INVALID_CONFIG')
    if (!apiKey) throw new LlmError('bedrock-mantle: no API key configured', 'INVALID_CREDENTIAL')
    return { baseURL, apiKey }
  }
  ctx.llm.registerAdapter([PROVIDER], new BedrockMantleAdapter(resolve))
}
