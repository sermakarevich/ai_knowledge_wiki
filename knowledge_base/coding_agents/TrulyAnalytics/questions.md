---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Andrew Southall | What Codex Actually Delivered in Truly Analytics

### Q1. How fast was Truly Analytics v1.0 built, and what were the headline commit and line counts for human versus Codex?
> [!tip]- Answer
> Truly Analytics went from first commit to v1.0 in six weeks, launched across all of Southall's digital properties, using Codex GPT 5.3-codex as an accelerator. Across 137 commits, humans made 107 (78.1%) and Codex made 30 (21.9%), while of 21,031 committed lines AI wrote 8,886 (42.3%) and the human wrote 12,145 (57.7%). See [[wiki/01-codex-delivered-truly-analytics|What Codex Actually Delivered in Truly Analytics]].

### Q2. How much committed code survived to v1.0, and in which direction did overwrites flow?
> [!tip]- Answer
> Only 12,892 lines (61.3%) survived: 8,759 human lines (67.94% of v1.0) and 4,133 robot lines (32.06% of v1.0). AI survival was 46.5% versus 72.1% for human code, with 3,610 of the 4,753 removed AI lines (76.0%) overwritten by the human while only 546 human lines (4.5%) were overwritten by AI. See [[wiki/01-codex-delivered-truly-analytics|What Codex Actually Delivered in Truly Analytics]].

### Q3. How was Codex isolated from the repository, secrets, and services during the build?
> [!tip]- Answer
> Codex ran inside an isolated containerised pipeline behind a strict wrapper that controlled branches, pushes, and PR creation. It had no direct access to git, secrets, the database, or internal services, with only outbound internet for research, and the wrapper pulled code and prompts from a prompt library before opening a PR. Of 30 Codex PRs, 25 were accepted (83.3%) and 5 rejected (16.7%). See [[wiki/01-codex-delivered-truly-analytics|What Codex Actually Delivered in Truly Analytics]].

### Q4. Where did surviving AI code concentrate by location and file type, and where did the human dominate?
> [!tip]- Answer
> Surviving AI code concentrated in src Go scaffolding (2,211 AI vs 2,671 human lines), AI-led JSX (607 vs 474) and JavaScript (683 vs 310), plus entirely AI-generated docs. The human owned the browser-delivered client analytics code (1,654 vs 353 lines, 82.4% human), infrastructure roots such as Dockerfile, compose, ansible, and k8s manifests, and all significant deletions. See [[wiki/02-code-location-owner-breakdown|Surviving LoC Stacked by Code Location & Owner]].

### Q5. Which five Codex PRs were rejected, and what lasting work did Codex contribute as a "copy paste machine"?
> [!tip]- Answer
> All 30 Codex commits were levelled through PRs with 5 rejected: a trivial Tailwind version change, a wrong-instruction debugging dump of 400 additions, a stale-branch merge problem, and two over-engineered PRs for client timing and trial restrictions. Lasting contributions were rote and pattern-driven — server routing, database access, in-memory caching, and nearly all admin-panel JSX — while novel enrichment, event handling, and per-datum logic stayed human. See [[wiki/03-non-quantifiable-metrics-reflection|The Non-Quantifiable Metrics]].

### Q6. Why does Southall stay on OpenAI/Codex, and on what grounds does he reject Gemini, Anthropic, and Copilot?
> [!tip]- Answer
> He stays because OpenAI was his first LLM, ChatGPT replaced Google as search, his prompt libraries are tuned for these models, and Codex runs the way he wants with momentum that breaks writer's block. Gemini is rejected after argument-prone Verizon-era use, Anthropic for API outages, confusing credits, arbitrary limits, and distrust of leadership and security claims, and Copilot with "Which one?", while local open models are deferred for missing image generation and weaker RAG. See [[wiki/04-why-openai-codex-errata|Why OpenAI and Codex?]].

### Q7. Should a solo engineer reuse Codex in this isolated PR-levelled manner for a production v1.0, given the survival gap and failure modes?
> [!tip]- Answer
> Yes, conditionally: reuse Codex for bounded scaffolding, typing automation, and throwaway or isolated code inside the strict wrapper pipeline, since at $20/month the momentum gain outweighs a ~50% discard rate. Keep human ownership of novel, production-sensitive work such as enrichment, client analytics, and infrastructure, because Codex over-engineers and fails at performant dependency-free code without strict review. See [[wiki/03-non-quantifiable-metrics-reflection|The Non-Quantifiable Metrics]].
