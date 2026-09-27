> [[index|Wiki]] | [[summary|Summary]]
# Andrew Southall | What Codex Actually Delivered in Truly Analytics — Digest

## 1. [[wiki/01-codex-delivered-truly-analytics|What Codex Actually Delivered in Truly Analytics]]
**In one sentence:** Andrew Southall built Truly Analytics from blank repo to working v1.0 in six weeks with Codex GPT 5.3-codex as an accelerator, and git-history analysis shows Codex committed 42.3% of lines but only 46.5% of its code survived versus 72.1% for human code, proving AI excelled at bounded pattern-driven work while human judgment decided architecture, product context, security and operational risk.
## Key points
- Truly Analytics went from first commit to v1.0 in six weeks and launched across all of Southall's digital properties, built with Codex GPT 5.3-codex as an engineering accelerator rather than an autonomous replacement.
- Across 137 commits, humans made 107 commits (78.1%) and Codex made 30 commits (21.9%); of 21,031 committed lines, AI committed 8,886 lines (42.3%) and humans committed 12,145 lines (57.7%).
- Only 12,892 lines (61.3% of committed lines) survived to v1.0: 8,759 human lines (67.94% of v1.0) and 4,133 robot lines (32.06% of v1.0).
- AI code survival rate was 46.5% (4,133 of 8,886 survived; 4,753 or 53.5% replaced/deleted) versus human survival rate of 72.1% (8,759 of 12,145 survived; 3,386 or 27.9% did not make it).
- Of removed AI code, 3,610 of 4,753 lines (76.0%) were overwritten by the human, while only 546 human lines (4.5% of human committed lines) were overwritten by AI.
- Of 30 Codex PRs, 25 were accepted (83.3%) and 5 rejected (16.7%); Codex worked inside an isolated containerised pipeline with a strict wrapper that controlled branches, pushes and PR creation, with no direct access to git, secrets, database or internal services.
- Codex contributed heavily to mechanical implementation work (routing, database access, admin UI, caching, email integration, Kubernetes scaffolding) while human-authored code dominated product-specific and production-sensitive areas (client-side analytics, enrichment logic, event handling, infrastructure decisions, final integration).

## 2. [[wiki/02-code-location-owner-breakdown|Surviving LoC Stacked by Code Location & Owner]]
**In one sentence:** Surviving AI code concentrates in `src` Go scaffolding, JSX/JavaScript frontend boilerplate and generated docs, while the human owns the client analytics code, infrastructure/auxiliary directories, most commits, and all significant deletions.
## Key points
- In `src`, surviving Go is close to 50/50, slightly human-led: AI 2,211 lines vs human 2,671 lines of 4,882 total (45.3% AI / 54.7% human).
- HTML is human-led (870 human vs 519 AI surviving lines of 1,389 total, 37.4% AI), described as Codex providing the testing framework and the human tuning it over time.
- JSX (607 AI vs 474 human, 56.2% AI) and JavaScript (683 AI vs 310 human, 67.3% AI) are both AI-led; the simple `app.jsx` is AI-dominant and one of the largest files.
- The `client` analytics code delivered to browsers is almost entirely human-owned: 1,654 human vs 353 AI surviving lines of 2,007 total (82.4% human), effectively refactored by the human post-release.
- Auxiliary directories are human except docs: ansible is human-managed (custom modules read, implemented and tested directly by the human), project root is human boilerplate (Dockerfile, docker-compose.yml, .gitignore), `k8s` is simple human-managed manifests, while `docs` is entirely AI-generated.
- The largest files are all AI-dominated — Go server/routing code (`server.go` / file-17.go), `app.jsx` (file-01.jsx, biggest file), and the database store (file-09.go, ~700 LoC) — versus a human preference for ~300-line files rarely exceeding 500 lines.
- Churn and commits are human-led: human made 107 of 137 commits (78.1%) vs AI 30 (21.9%); the human deletes with abandon (outlier: 0 added / 900+ deleted) while AI dumps code in (outlier: 800 added / 150 deleted), and the biggest human commit added 1,414 lines while deleting over 1,000.

## 3. [[wiki/03-non-quantifiable-metrics-reflection|The Non-Quantifiable Metrics]]
**In one sentence:** Codex was kept inside a secure PR-levelled pipeline with a 16.7% PR rejection rate, contributed lasting value mostly as a "copy paste machine" for rote server/database/JSX work while failing at novel backend logic and performant client analytics code, and remains worth reusing only with human ownership and an isolated pipeline.
## Key points
- All 30 Codex commits were levelled through PRs into the codebase, with 5 rejected — a 16.7% rejection rate.
- One rejected PR was a trivial Tailwind CSS version change handled manually instead; one was a wrong-instruction debugging PR with 400 additions and only 5 deletions, deleted as code-stuffing.
- One rejected PR was a code-merging problem from Codex working off an old branch, later absorbed via a different branch and instruction — "but a speedbump".
- The final two rejected PRs were "prime examples of agentic over-engineering": an overcomplicated client analytics timing stack and over-complicated trial-restriction evaluation with unwanted test code, both binned for comprehension, maintainability and design reasons (the trial one redone by the human in ~10 minutes).
- Lasting agent contributions were mostly mechanical — server route handling, database access, in-memory cache management, and JSX including basically all admin-panel code — because those are rote, conventional patterns memorisable from abundant examples.
- Novel backend work around data enrichment, event handling, and per-datum management still had to come from the human; root files (Dockerfile, Docker Compose, Ansible, Kubernetes manifests) were battle-tested human copies with nothing for AI to do.
- Client analytics code in `client/` needed to be performant, clear, modular, minimal and dependency-free, but Codex output failed "horribly" — partly blamed on low-quality JS training material and weak JS-side tooling (Go builds were checked, JS was "winging it") — while Codex one-shotting the client upgrade page CSS/classes untouched was "glorious".
- Verdict: yes to AI again in this manner with the isolated pipeline as a required part of the process, strongest as research/typing-automation and throwaway/supporting/isolated code, not yet viable for novel independent work; at $20/month "absolutely worth more than that".

## 4. [[wiki/04-why-openai-codex-errata|Why OpenAI and Codex?]]
**In one sentence:** The author sticks with OpenAI/ChatGPT and Codex because his prompt libraries are tuned for them and they run the way he wants, rejecting Gemini, Anthropic, and Copilot on workflow and operational grounds while deferring open-source/local models to later, and values Codex mainly as scaffolding that breaks writer's block even though he threw away about half the code it gave him.
## Key points
- OpenAI was the author's first LLM, initially little-used because ungrounded generated text without RAG could not reference or source its information, but later useful, with ChatGPT replacing Google as a search tool.
- Code from more than roughly 6–12 months ago is described as "not worth much," implying model quality only recently became practically useful for his work.
- Gemini is rejected on working-relationship grounds after Verizon-era use under a Google contract ("every chat ... broke down into arguments"), rated decent only for image generation.
- Anthropic is rejected on operational grounds (API availability, confusing credits, arbitrary limits and waits, possible model downgrades) plus distrust of its leadership, marketing, and security claims, keeping only a free account for AEO queries.
- Copilot is dismissed with "Which one?", and open-source models are deferred as a future API-key swap, blocked by missing image generation and weaker RAG/search.
- The stated end state is staying on ChatGPT/Codex now, with a possible later move of tedious private work such as GTM automation to a local model that "won't leave the premises."
- Personal gain is framed as momentum and labour saved: about half the bot code was discarded, yet it still replaced code he would otherwise have written himself and broke through writer's block by giving him "a framework I could hammer into shape."

## The argument in five moves
1. A solo engineer ships Truly Analytics v1.0 in six weeks with Codex as an accelerator inside an isolated wrapper pipeline, then measures the git history instead of guessing at productivity.
2. The headline counts show Codex wrote a large share of committed lines (42.3%) but far less of it survived (46.5% survival vs 72.1% human; only 32.06% of v1.0 is robot code), with most dead AI code overwritten by the human.
3. Location analysis refines that split: AI persists in bounded Go scaffolding, JSX/JS boilerplate and docs, while the human owns client analytics code, infrastructure, and all decisive deletion and integration work.
4. Qualitative review explains why: Codex works as a rote "copy paste machine" for conventional patterns but over-engineers or fails at novel enrichment, event handling, and performant dependency-free client code, requiring PR levelling and an isolated pipeline.
5. The verdict is therefore conditional reuse — keep OpenAI/Codex with tuned prompts and strict process for momentum, scaffolding and typing automation — not autonomous replacement for novel, production-sensitive engineering.
