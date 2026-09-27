> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# The Technology Probe: Partners, Activation, Engagement
**In one sentence:** Next.js/Markdown probe where users configure partner role + event triggers + contextual heuristic; LLM decision engine activates max 2 partners; suggestions are acknowledgement + question; engagement is ignore/inspire/execute.

## Key points
- Users create a partner by specifying name/emoji, role, one or more event triggers, and a contextual heuristic, for example the Evidence Partner configured to help strengthen claims by suggesting evidence when the writer pauses and the context calls for examples.
- Three rule-based event triggers detect candidate moments from real-time keystrokes: Long Pause after 5s inactivity by default, Sentence End after sentence completion plus 1s idle by default, and Text Selection after selection plus 5s idle by default, all customizable.
- On each trigger the LLM decision engine receives session goal, current text, cursor position, trigger event, recent behavior including 15s keystroke logs, and the list of enabled partners for that trigger, then selects at most 2 partners whose heuristics match.
- The decision engine uses gemini-2.5-flash-lite and selects partners in under 1 second, with the partner floating tag appearing immediately to reduce perceived latency.
- Each suggestion has two parts -- acknowledgement of what the writer just did or may be trying next, plus a question-style suggestion, for example asking how Rafael Nadal's relentless drills or Roger Federer's recovery routines could illustrate training principles.
- Engagement is graduated: ignore by continuing to write while the floating tag fades after 15s, inspire by clicking the tag to expand a suggestion card with optional follow-up chat, or execute via Help Me Write which inserts or revises text directly with accept/revert control.
- Implementation uses Next.js with server-side rendering and API routes, BlockNote Markdown editor with adapted AI SDK integration for insertion/revision, Gemini APIs and Firebase for logging, JavaScript keystroke listeners, and gemini-2.5-flash for suggestion generation, follow-up, and execution with about 8s generation time.

---
## 4.1 Partner customization
The probe has three main interfaces: an onboarding panel for login and session writing goals, a partner configuration panel for creating and enabling partners, and a lightweight Markdown editor with a side panel for proactive suggestions.

In the configuration panel users define both role and proactivity. Partner Role defines responsibility and capability such as generating ideas, identifying weak evidence, or challenging an argument. Event Triggers define observable candidate moments such as pausing, completing a sentence, or selecting text, with one or more selectable per partner and none selected by default to avoid anchoring. Contextual Heuristic defines precise contextual criteria for intervening after a trigger, such as when a claim lacks evidence or an argument needs a counterpoint, drawing on context-aware computing ideas.

The running example is the Evidence Partner, configured with name and emoji plus a role of strengthening claims, pause triggers, and a heuristic to suggest evidence when the current context calls for examples.

## 4.2 Activation pipeline with triggers + decision engine
Triggers identify broad candidate moments while heuristics determine precise contextual relevance. The three implemented rule-based triggers are grounded in proactive AI, interruption management, and writing keystroke-analysis work.

Long Pause treats inactivity as a natural cognitive break and fires after 5 seconds by default. Sentence End treats sentence completion as a subtask boundary less disruptive for intervention, with a short 1 second idle wait by default to avoid interrupting rapid typing. Text Selection treats selecting text plus remaining idle for 5 seconds by default as the local focus, enabling lightweight proactivity without requiring the writer to formulate a prompt or command.

When a trigger fires, the system sends session goal, current editor text, cursor position, trigger event, 15s of prior keystroke logs, and enabled partners for that trigger to the LLM decision engine. The 15s window follows prior keystroke studies using short windows to infer states such as boredom and engagement. The engine checks user-defined heuristics and activates at most two matching partners. Activated partners appear as small floating tags in the right-side panel aligned with cursor position, showing emoji and name as a peripheral cue.

## 4.3 Suggestion generation
An activated partner generates a suggestion shown after the writer clicks its floating tag. Each suggestion contains acknowledgement plus question-style suggestion.

Acknowledgement briefly states what the writer just did, is doing, or may try next, making visible what the responder understands before offering guidance, following writing-feedback research. Suggestion offers a thought-provoking question tailored to context, chosen because question-style AI suggestions can stimulate ideas while preserving ownership.

The paper's example: after a writer introduces elite players' training habits, the Evidence Partner acknowledges the move from general principles to concrete elite-player examples, then asks how a specific anecdote or training philosophy such as Rafael Nadal's relentless drills or Roger Federer's recovery routines could illustrate the stated principles.

## 4.4 Three engagement forms
Once floating tags appear, writers choose increasing levels of AI involvement while retaining agency.

Ignoring: continue writing without clicking; the tag gradually fades and disappears after 15 seconds, requiring no explicit dismissal and supporting efficient termination of mixed-initiative action.

Inspiring: click the tag to expand a floating card at the same position showing the suggestion for use as inspiration while refining prose; a message icon opens follow-up conversation to clarify, request alternatives, challenge framing, or explore related ideas.

Executing: hover the suggestion card and click Help Me Write to have the partner insert or revise editor text directly; the writer explicitly initiates the action and reviews the change before accepting or reverting. This moves the partner from cognitive scaffolding to temporarily taking over writing work.

Together these options let proactive support function as peripheral cue, inspiration source, or actionable edit, and let researchers observe whether writers ignore, open, discuss, or execute suggestions.

## 4.5 Implementation stack
The probe is implemented with Next.js for server-side rendering and backend API routes to external services, including Google Gemini APIs for LLM functions and Firebase APIs for event logging. The Markdown editor is built with BlockNote, with adapted BlockNote AI SDK integration for partner text insertion and revision. Keystroke logging uses JavaScript event listeners.

The decision engine uses gemini-2.5-flash-lite to minimize latency, taking less than one second after a trigger, with the floating tag shown immediately. Suggestion generation, follow-up discussion, and text insertion or revision use gemini-2.5-flash, with partner suggestion generation taking approximately eight seconds. Prompts are in supplementary materials.

**Covers:** Section 4.1-4.5 (probe design and implementation)
