> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# TencentCloud/TencentDB-Agent-Memory — In Plain Language

Think of it as a shared "team brain" for AI coding assistants: instead of every
chat starting from zero, past conversations, documents, and code are saved as
reusable memories any agent on the team can load on day one.

## What is this about?

- AI assistants forget everything when a chat ends. This project fixes that by
  turning leftovers — old chats, docs, repos — into organized memory assets.
- It ships three services that start with one command: a memory store
  (`memory-core`), a team web panel (`memory-hub`, at `localhost:8125`),
  and a proxy (`proxy`) that sits between your agent and its language model.
- There are four kinds of memory: Chat Memory (what people said and decided),
  Skills (how to do a tricky task), Wiki (organized documents), and CodeGraph
  (a map of the codebase: symbols, calls, and what-affects-what).
- A control panel lets humans create teams and agents, review memories, and
  decide who sees what (`private`, `team`, or `restricted` access).
- New agents "cold-start": they import the team's saved experience instead of
  re-reading every doc and re-learning every lesson.

## Why does it matter?

- Without shared memory, every session repeats the same work: re-explaining
  project context, re-reading docs, rediscovering workflows that already worked.
- The project's own formula is: reusable memories mean fewer chat turns, less
  rework, and steadier results — experience compounds instead of evaporating.
- Plain chat logs and basic search (RAG) only answer "what can be found?".
  This system also answers "who may use it, which version is current, and
  which agent should get it" — ownership, versions, and routing included.
- A concrete example: one remembered rule — "don't refactor the old auth
  module, mobile still uses it" — can save a whole broken release.
- For teams running several assistants (researcher, builder, reviewer), shared
  memory keeps everyone working from the same playbook.

## How does it work?

1. **Install once.** Clone the repo, fill in two sets of language-model
   settings (one for memory, one for the proxy), and run `./start-all.sh`
   from `deploy/global-images`. Three containers boot on fixed ports: memory
   `8420`, panel `8125`, knowledge `8424`, proxy `8096`.
2. **Connect agents with zero code changes.** Point an agent's model URL at
   the proxy and it just works — no plugin or hook needed. Supported agents
   include Claude Code, Codex, CodeBuddy, DeepSeek Harness, Hermes, and more.
3. **Work normally; memories distill automatically.** Chats distill upward:
   raw conversation (L0) → small facts (L1 Atom) → reusable situations
   (L2 Scenario) → lasting traits and preferences (L3 Persona).
4. **Skills get reviewed like code.** After hard tasks, the system drafts a
   Skill — when to use it, steps to follow, how to check the result. Skills
   stay private until a human approves sharing them with the team.
5. **Docs and code become searchable maps.** Imported documents turn into Wiki
   pages with links; imported repos turn into a CodeGraph, so an agent can
   check callers and impact ("changing this might affect those") before edits.
6. **Humans stay in charge.** Admins create teams and users (a `team / agent /
   task` setup); owners track their assets; visibility is `private`, `team`,
   or `restricted` (fine-grained user/role/agent rules).
7. **In-chat helpers.** Special `mem:` commands refresh memories (`mem:sync`),
   save the current chat as a Skill (`mem:create-skill`), or show help
   (`mem:help`). The roadmap adds task commands, editable memories, and
   Agent templates.

## Where can this be used?

- **Software teams with coding assistants:** onboard a new agent to an existing
  repo via CodeGraph plus Wiki instead of weeks of re-explaining architecture.
- **Tiny "one-person company" squads:** give each role its own loadout — e.g.
  the Scout gets interview notes plus research Wiki, the Builder gets the
  product Wiki plus CodeGraph, the Reviewer gets incident history plus a
  release checklist Skill.
- **Support and operations:** keep decisions, preferences, and incident
  lessons in Chat Memory so the next shift's agent remembers what broke last
  time and why.
- **Multi-agent setups:** share one memory server across frameworks, so a
  lesson learned by one agent (or human) is available to all of them.
- **Local or cloud deploys:** run single-machine with the default lightweight
  storage, or scale to shared service mode (external database plus Redis)
  for many tenants — with an experimental MongoDB option in between.

## Conclusions & takeaways

- The big idea is simple: treat experience as an asset, not exhaust. Save
  what worked, organize it, and hand the "save file" to the next agent.
- The proxy trick is what makes it practical: one redirect gives many agents
  memory with no per-agent rewiring.
- Human review and permissions are first-class, not an afterthought — private
  by default, shared after approval, with clear owners and roles.
- Limits to know: storage backends don't auto-migrate (switching means
  starting fresh), some comparison and deploy docs are truncated, and the next
  release (v2.0.1) is still adding templates, editable memories, and Cursor
  support.
- Bottom line: stop retraining every agent — give it the save file.

## Jargon decoder

| Term | What it really means |
|---|---|
| Memory asset | A saved, reusable piece of experience (a fact, a Skill, a Wiki page) — not a raw chat log |
| Memory Hub | The shared server plus web panel where memories are stored, reviewed, and assigned |
| Proxy | A middleman between the agent and the language model that quietly adds relevant memories |
| L0 → L3 memory | Layers of distillation: raw chat → small facts → typical situations → lasting traits |
| Skill | A tested how-to recipe: when to use it, steps to run, and how to verify it worked |
| Wiki | Team documents converted into linked, searchable pages |
| CodeGraph | A map of the code: what calls what, so agents foresee side effects before editing |
| Cold start | Giving a new agent the team's saved memories on day one instead of training from scratch |
| RAG | Basic "find matching text chunks" search — useful, but with no ownership or versioning |
| Visibility (`private` / `team` / `restricted`) | Who may see a memory: only its owner, the whole team, or a hand-picked list |
