# Is Progressive Disclosure All You Need for Long-Context Agents?

**Paper:** [Is Progressive Disclosure All You Need for Long-Context Agents? (He, Zhao, Wang, Chen, 2026)](https://arxiv.org/abs/2607.17598)

## Human Readable TL;DR

Imagine handing someone an 800-page book and asking them a question about it. One approach: they read the whole book cover to cover (slow, and they may not remember the details well). Another: give them a one-paragraph summary of each chapter first, and let them only open the chapters that sound relevant -- like a table of contents that lets you drill down (this is "progressive disclosure"). A third: build a search engine that automatically fetches the most relevant paragraphs. This paper rigorously tests when the "table of contents" trick actually helps AI agents versus when it's wasted effort. The finding: for a single book, if the agent is already good at skimming and searching on its own, the trick doesn't help at all -- it only rescues agents that are bad navigators. But once you dump a whole library of 20 books on the agent and ask about all of them, even the best agents get lost, and the trick becomes essential -- as long as it's one flat index, not a multi-level nested one (nesting adds overhead without adding value, and can even make things worse).

## TL;DR

The paper runs the first controlled comparison of three ways an agent can read book-length documents -- raw-document navigation, a flat single-level "Agent Skills" disclosure pack, and a hierarchical (recursive) disclosure pack -- against a classical hybrid-RAG retriever baseline, across three agent harnesses (Codex, Pi, Claude-Code) and three model families (gpt-5.4-mini, qwen3.6-27b, claude-haiku-4.5) on the LoongDoc environment built atop ∞Bench. On a single book, flat disclosure matches or beats raw navigation only when the underlying harness is a weak navigator (Pi, Claude-Code); it adds nothing for Codex, whose bare agent already greps effectively. At library scale (K=5,10,20 books), raw navigation collapses (En.QA accuracy falls to 0.257 at K=20) while flat disclosure holds far better (0.462), and a second, deeper hierarchical routing level never helps and sometimes actively hurts accuracy. The authors' conclusion: "progressive disclosure buys context, not intelligence."

---

## Problem & Motivation

Long-document question answering forces a choice between loading the whole document into the context window (straining effective long-context attention -- usable context often falls well short of the advertised window) and bolting on a separate retriever (which decouples retrieval quality from the answering model). Agentic AI offers a third option: give the agent the document path and let it decide what to read and when -- e.g., Claude Code dropped its retrieval index in favor of on-demand search, but that switch was reported from engineering experience, not a controlled comparison. Anthropic's Agent Skills standard formalizes on-demand reading as **progressive disclosure**: keep only a short description always in context, and let the agent load the full body only when the description matches the query.

Practitioners rapidly adopted progressive disclosure for book-length material via a "book-to-skill" recipe, but the evidence was anecdotal -- no controlled study had tested the pattern with an actual agent on a standardized long-document benchmark. The paper isolates two design choices the practitioner literature never separates -- how deep the disclosure recurses, and where the per-chunk index physically lives -- and asks:
1. Does progressive disclosure work for book-length understanding at all?
2. What is the best way to structure the skill pack?

---

## Main Original Ideas

1. **A controlled three-way comparison of agentic reading strategies.** `raw` (no skill pack, unconstrained navigation), `flat` (single `SKILL.md` with a table of contents over chunk files, loaded on activation), and `hierarchical` (every chunk promoted to its own child skill with an always-loaded description, routed by a meta-router) all read the same underlying chunk set -- so only the disclosure "wiring" varies, isolating routing depth and context placement as the sole variables.

2. **LoongDoc: a long-context agent environment.** Built on BenchFlow (implementing the Agent Client Protocol), LoongDoc converts static ∞Bench book-QA items into sandboxed-filesystem tasks: the agent reads/greps/opens files, writes an answer, and a deterministic verifier scores it while logging the full trajectory (tool calls issued, files opened, tokens spent per step). This lets the authors explain results via trajectory inspection, not just report accuracy deltas.

3. **The book-to-skill pipeline as shared substrate.** Both `flat` and `hierarchical` packs are built once per book: split along chapter headings (or ~4000-word fallback chunks) into files under `references/`, then LLM-generate a one-to-two sentence summary + comma-separated key-elements list per chunk, and a one-line book-level description from those chunk summaries (written to avoid naming/guessing the book's real title, preventing shortcut memorization cues from leaking into the routing metadata).

4. **Library-scale corpus staging (the K-book knob).** LoongDoc can bundle K books (K=1,5,10,20) into one task, prefixing every question/answer ID with a book label and giving the agent a `corpus-index.md` summary of each member book -- turning single-document QA into a "find the right book, then answer" problem without changing the underlying interface.

5. **Hybrid-RAG as an external reference baseline.** A classical retrieve-and-rerank pipeline (BM25 sparse + BGE-M3 dense retrieval, fused via Reciprocal Rank Fusion, then BGE cross-encoder reranking) separates "does disclosure help" from "is this just retrieval in disguise" -- hybrid-RAG trails both `raw` and `flat` across all three ∞Bench subsets, so the disclosure gain is not reducible to classical retrieval.

---

## Key Findings

**Single-book QA** (Table 1; three harnesses × models, ∞Bench En.MC / En.QA / Zh.QA):

| Harness / Model | Result |
|---|---|
| Codex / gpt-5.4-mini | `raw`, `flat`, `hierarchical` tie within a standard error on all 3 subsets -- disclosure adds nothing to a strong native navigator (Codex's bare agent already greps for named entities and builds its own locate-then-read retrieval) |
| Pi / gpt-5.4-mini | `flat` beats `raw` (En.MC **0.9126** vs 0.8851; En.QA 0.7259 vs 0.7161); `hierarchical` actively hurts, dropping En.MC to 0.6398 |
| Pi / qwen3.6-27b | `hierarchical` falls below `flat` on all 3 subsets, steepest on Zh.QA (0.7479 → 0.3890) |
| Claude-Code / claude-haiku-4.5 | `flat` matches/exceeds `raw` (En.MC 0.8687 vs 0.7448); `hierarchical` ties `flat` within noise |

- Disclosure helps only where native navigation is weak (Pi, Claude-Code); it is redundant for a harness whose bare agent already reconstructs locate-then-read retrieval (Codex).
- A second, deeper routing level (`hierarchical`) never helps on a single book and sometimes breaks accuracy outright.

**Library-scale QA** (Table 2, K=5/10/20; Codex/gpt-5.4-mini and Claude-Code/claude-haiku-4.5):

- `raw` collapses as K grows: Codex En.QA falls from 0.657 (K=5) to **0.257** (K=20); Zh.QA collapses to near zero (0.043 at K=20).
- `flat` degrades far more gently and **overtakes** `raw` once the corpus is large: En.QA at K=20 is **0.462** (`flat`) vs. 0.257 (`raw`) -- a gap clearing one standard error; En.MC leads too (0.760 vs 0.720).
- The rescue is specific to `flat`; `hierarchical` does not reproduce it -- its always-loaded child-skill descriptions inflate the always-on context budget as the library grows, recreating the context pressure disclosure was meant to relieve (on En.QA, `hierarchical` collapses back near `raw` at K=20 while `flat` holds over 1.7× its accuracy).
- The rescue reproduces on a second, weaker harness/model: Claude-Code/claude-haiku-4.5 shows `flat` leading `raw` at every K on En.QA, with the K=10 gap clearing two standard errors.
- Cost tracks the story: at K=20, `raw` burns ~68.3M tokens/question (~$52 uncached) for the worst accuracy; `flat` reaches nearly double the accuracy at roughly half the tokens/cost (~32.5M tokens, ~$25) -- library scale makes disclosure strictly more efficient, not just more accurate.
- Gains are task- and language-specific: sharpest on English open QA, largely absent or negative on Chinese QA, where the base model's own capability (not the skill pack) sets the ceiling.

---

## Suggestions & Future Directions

1. **Practical packaging guidance:** package book-length material as one skill with a single, in-skill-indexed layer of progressive disclosure -- not as multiple parallel packages of child skills with always-loaded descriptions (avoid the `hierarchical` design).
2. **Pre-training confound on En.MC (acknowledged limitation):** ∞Bench's English multiple-choice books are canonical novels the models likely memorized, so the bare agent may answer from parametric knowledge rather than genuine reading; even at K=20 the `raw` agent answers some En.MC questions correctly in far too few tool calls to have read twenty books. A held-out or synthetic-book corpus would remove this confound.
3. **Narrow scaling axis:** corpus size was sampled only at K∈{1,5,10,20} within one benchmark family, so the paper can only bracket -- not pinpoint -- where disclosure begins to pay off, and cannot claim the effect transfers to non-narrative corpora (code, technical manuals).
4. **Fixed chunking/description recipe:** chunk granularity and the description-writing model were held constant; varying either might shift the balance between `raw`, `flat`, and `hierarchical`.
5. **Sample size:** several comparisons stay within a standard error because sample sizes are bounded by what ∞Bench provides; a larger benchmark would tighten every estimate.

---

## Authors & Institutions

Yifeng He (University of California, Davis), Yinzhe Zhao (Zhejiang University; work done while interning at UC Davis), Jicheng Wang (University of California, Davis), Hao Chen (The University of Hong Kong).
