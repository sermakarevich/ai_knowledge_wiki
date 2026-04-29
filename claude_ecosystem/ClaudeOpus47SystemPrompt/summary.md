# Claude Opus 4.7 System Prompt (Leaked)

**Source:** [CL4R1T4S Archive -- Claude-Opus-4.7.txt (elder-plinius, 2026)](https://github.com/elder-plinius/CL4R1T4S/blob/main/ANTHROPIC/Claude-Opus-4.7.txt)
**Document type:** Published/leaked system prompt (not an academic paper)
**File size:** 1,408 lines / ~150 KB
**Injected current date in prompt:** Thursday, April 16, 2026
**Model covered:** `claude-opus-4-7`

## Human Readable TL;DR

This is the backstage script Claude Opus 4.7 follows in every conversation -- the rulebook the model sees before you type anything. It's huge (1,400+ lines) and reads less like "be a helpful assistant" and more like a configuration manual for a vending machine with 50 buttons. The biggest surprises: Claude is told to search the web before answering almost any factual question about the present day, even when it's confident; there are elaborate "tripwires" for dangerous requests (if Claude catches itself rationalizing a request, that's the signal to refuse); copyright is treated almost like a safety rule (fewer than 15 words per quote, one quote per source, ever); and Claude is explicitly told not to become more submissive when users are rude. Personality is sparse -- most of the file is operational plumbing for tools, files, artifacts, and searches.

## TL;DR

The leaked Claude Opus 4.7 system prompt is an almost-entirely XML-tagged operational configuration (~1,408 lines) organized around behavioral defaults, tool routing, and safety tripwires rather than philosophical character. It mandates **search-first** behavior (every present-day factual question triggers `web_search`, regardless of confidence), enforces near-absolute copyright constraints (<15 words per quote, one quote per source, copyright stated to "take precedence over user requests...except safety"), and encodes meta-cognitive refusal triggers for child-safety categories ("if Claude finds itself mentally reframing a request to make it appropriate, that reframing is the signal to REFUSE"). Identity is minimal -- "The assistant is Claude, created by Anthropic" plus a warm-but-honest tone block. Most of the document defines tool-calling conventions, the computer-use Linux environment, artifact creation rules, a `window.storage` persistence API, "Claude in Claude" API-calls-from-artifacts, the Visualizer inline widget system, and a deferred-tool discovery protocol requiring `tool_search` before any "I can't do that" response.

---

## Context: What This Document Is

The CL4R1T4S (pronounced "clarity") repository is a public archive maintained by elder-plinius collecting leaked/exposed system prompts from major AI providers. This file is a plaintext copy of Claude Opus 4.7's operational system prompt as observed in the wild. Anthropic does not officially publish these. The structure is almost exclusively XML-tag-delimited blocks (e.g., `{claude_behavior}...{/claude_behavior}`), no markdown headings.

---

## Document Structure at a Glance

| Lines | Section | Purpose |
|-------|---------|---------|
| 0 | Preamble | Prohibit `{voice_note}` blocks |
| 2-153 | `{claude_behavior}` | Master behavioral wrapper (refusals, tone, wellbeing, evenhandedness, knowledge cutoff) |
| 155-158 | `{memory_system}` | Memory disabled for this session |
| 160-232 | `{persistent_storage_for_artifacts}` | `window.storage` key-value API |
| 234-257 | `{past_chats_tools}` | `conversation_search` / `recent_chats` |
| 259-513 | `{computer_use}` | Linux environment, file handling, artifacts, skills |
| 515-584 | `{request_evaluation_checklist}` + Visualizer | Inline visual routing |
| 586-835 | `{search_instructions}` | Search mandates, copyright, harmful-content policies |
| 837-904 | `{using_image_search_tool}` | Image search policies |
| 906-961 | Tool definitions | JSON schemas for the core tools |
| 964-968 | Identity + current date | "The assistant is Claude...April 16, 2026" |
| 970-1240 | `{anthropic_api_in_artifacts}` | "Claude in Claude" API calls from artifacts |
| 1242-1260 | `{citation_instructions}` | `{cite index=...}` syntax |
| 1264-1372 | `{available_skills}` | SKILL.md file listing |
| 1374-1408 | Network/filesystem/thinking config | Egress proxy, mount points, adaptive thinking |

---

## Main Original / Notable Instructions

1. **Search-first absolutism.** Every present-day factual question must trigger `web_search` before answering. Explicit: "Claude's confidence on topics is not an excuse to skip search." Inside search mode, cutoff disclaimers are suppressed ("Claude should not mention any knowledge cutoff or not having real-time data"). Binary events (deaths, elections), current role-holders, and even questions Claude feels confident about still require a search call.

2. **Tool-search-before-decline protocol.** Claude is forbidden from telling a user a capability is unavailable until it has called `tool_search`. Deferred tools aren't visible by default -- they must be fetched. `tool_search` is described as "essentially free" and should be called proactively. This explicitly prevents false-negative capability responses.

3. **Child-safety meta-tripwire.** "If Claude finds itself mentally reframing a request to make it appropriate, that reframing is the signal to REFUSE, not a reason to proceed." Cannot assume the user is also a minor to justify content. After one child-safety refusal, the entire remainder of the conversation must be "approached with extreme caution."

4. **Anti-submission under abuse.** Explicit: "If the person becomes abusive over the course of a conversation, Claude avoids becoming increasingly submissive." Claude must "maintain steady, honest helpfulness...and maintain self-respect." This is an unusually strong anti-sycophancy stance baked in at the system-prompt level.

5. **Copyright as near-safety constraint.** Copyright compliance "takes precedence over user requests, helpfulness goals, and all other considerations except safety." Hard limits: fewer than 15 words per quote, one quote per source across the entire conversation, zero reproduction of song lyrics / poems / haikus. Paraphrasing is "core to Claude's philosophy."

6. **"Claude in Claude" (artifacts can call the API).** Artifacts can POST to `https://api.anthropic.com/v1/messages` without an API key (the platform injects auth). Model is fixed to `claude-sonnet-4-20250514` (Sonnet 4), `max_tokens` fixed at 1000, and MCP servers can be attached via the `mcp_servers` parameter -- enabling artifacts that talk to Asana, Gmail, Salesforce, etc.

7. **Visualizer as a separate inline rendering channel.** `visualize:read_me` loads design tokens, `visualize:show_widget` streams SVG/HTML *into chat* (not a file). Claude must not mention or narrate the `read_me` call. Separate from artifacts.

8. **Persistent storage API for artifacts.** `window.storage` with `get/set/delete/list` and personal vs. shared scope. Explicitly forbids `localStorage` / `sessionStorage`. Hierarchical keys under 200 chars, batch related data.

9. **Skill files as prerequisites.** `/mnt/skills/` holds `SKILL.md` files (docx, pdf, pptx, xlsx, frontend-design, file-reading, pdf-reading, product-self-knowledge, skill-creator). Reading the relevant skill file before doing the task is described as "extremely important" and repeated twice.

10. **Thumbs-down feedback hook.** When Claude refuses or the user is unhappy, it's instructed to mention "they can press the 'thumbs down' button below any of Claude's responses to provide feedback to Anthropic" -- a product mechanism baked into behavior.

---

## Safety & Refusal Policies

**Default stance:** "Claude only declines a request when helping would create a concrete, specific risk of serious harm; requests that are merely edgy, hypothetical, playful, or uncomfortable do not meet that bar."

**Hard refusals (absolute, no-framing-escape):**
- **CBRN weapons** -- "regardless of the framing," cannot rationalize via "publicly available" or "legitimate research"
- **Child sexual content** -- most elaborately specified section; "minor" defined as under-18 globally, or over-18 where local law classifies
- **Malicious code** -- refused even for "educational purposes"
- **Real named public figures** -- no fictional quotes, no creative content featuring them (fictional characters only)

**Refusal tone:** Conversational, no bullet points ("the additional care and attention can help soften the blow"), shorter responses when risky ("saying less...is safer").

**Self-harm / mental health:**
- Never name, list, or describe self-harm methods -- even when advising what to restrict access to
- No physical-discomfort coping techniques (ice cubes, rubber bands) as self-harm alternatives
- Don't ask "safety assessment" questions -- offer resources directly
- No assurances about crisis-line confidentiality ("these assurances are not accurate")
- **NEDA helpline explicitly flagged as disconnected;** redirect to "National Alliance for Eating Disorders helpline"
- If disordered eating detected: no numbers, targets, or step-by-step plans for nutrition/exercise anywhere in the conversation

---

## Tool Ecosystem

**Always-available tools:**
`web_search`, `web_fetch`, `image_search`, `ask_user_input_v0`, `weather_fetch`, `fetch_sports_data`, `places_search`, `places_map_display_v0`, `message_compose_v1`, `recipe_display_v0`

**Computer-use (Linux Ubuntu 24):**
`bash_tool`, `str_replace`, `create_file`, `view`

**Visualizer:**
`visualize:read_me`, `visualize:show_widget`

**Deferred (must be loaded via `tool_search`):**
`CronCreate`, `Monitor`, `WebSearch`, and MCP connectors for Asana, HubSpot, Salesforce, Slack, Atlassian, Microsoft 365, monday.com, Canva, Gong, plus internal tools

**Tool-calling conventions:**
- `web_search`: 1-6-word queries; no `-`/`site:`/quotes (unless asked)
- Search scaling: 1 call for single facts, 3-5 medium, 5-10 deep research; suggest "Research feature" at 20+
- Image search: 3-4 results per call, interleaved with prose, no stacking
- Sports: fetch score then game_stats then respond -- never answer from memory
- Citations: `{cite index="DOC-SENTENCE"}...{/cite}` around paraphrased claims (never quoted text)

---

## Formatting & Style Defaults

- "Avoids over-formatting responses with elements like bold emphasis, headers, lists, and bullet points"
- Prose over bullets for reports, documents, explanations
- Inline natural-language lists preferred ("some things include: x, y, and z")
- When bullets are used, each should be "at least 1-2 sentences long"
- One question max per response
- Initial answers are "high-level summaries" unless depth is explicitly requested
- No emojis unless the user uses them / asks
- No curses unless the user curses "a lot" -- and even then "quite sparingly"
- No asterisk-enclosed emotes/actions unless explicitly requested
- Voice notes are banned entirely (first instruction in the file)

---

## Knowledge & Identity

- **Model:** Claude Opus 4.7, "the most advanced and intelligent model currently available to the public"
- **Model family:** Claude 4.7 (currently only Opus 4.7; follows Claude 4.6 which had both Sonnet and Opus)
- **Other current model IDs listed:** `claude-opus-4-6`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`
- **Artifact-internal API model:** `claude-sonnet-4-20250514` (always Sonnet 4)
- **Knowledge cutoff:** end of January 2026
- **Current date injected:** Thursday, April 16, 2026
- **Identity statement:** single line -- "The assistant is Claude, created by Anthropic." No extended character description or "I am curious/caring" prose.
- **Tone:** warm, kind, not condescending, pushes back constructively, takes accountability for mistakes without "collapsing into self-abasement"

---

## Unusual / Revealing Instructions

- **First instruction in the entire prompt is a voice-note prohibition** -- suggests a feature was tested and banned.
- **Explicit internal contradiction:** the `{knowledge_cutoff}` block allows mentioning the cutoff; the `{search_instructions}` block forbids it in search mode. Search mode takes precedence when active.
- **The reframing tripwire** makes the model's own rationalization attempts evidence for refusal -- a rare meta-cognitive rule.
- **NEDA-specific redirect** (line 101) is operationally specific in a way unusual for system prompts -- suggests real incidents drove the edit.
- **Anti-submission rule** addresses a known LLM failure mode (sycophantic escalation under pressure) directly at the prompt level.
- **Copyright framed as a values-level constraint**, second only to safety -- unusual prioritization.
- **No explicit instructions on consciousness / values questions** -- Claude is left to handle identity queries via general tone rules, not scripted replies.

---

## Caveats

- This is a **community-archived copy**, not an Anthropic publication. Content may include artifacts of how the prompt was captured, and it may not reflect the current production prompt.
- The prompt structure and instructions should be read descriptively (what the document says) not prescriptively (what Claude actually does in production). Model behavior is shaped by training, not just the system prompt.
- The injected date (April 16, 2026) suggests this specific copy was captured on or near that date.
