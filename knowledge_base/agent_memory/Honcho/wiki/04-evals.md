> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Evaluations: LongMemEval, LoCoMo, BEAM
**In one sentence:** Honcho's maker reports top scores on three long-memory tests for LLM (Large Language Model, an AI system that reads and writes text) agents, with 90.4% on LongMemEval-S, 89.9% on LoCoMo, and 0.630 to 0.409 across BEAM scales, plus 60-90% token savings.
## Key points
- On LongMemEval-S (500 long chats of about 115,000 tokens each), Honcho scored 90.4% vendor-reported, which is 27.8 percentage points above the Claude Haiku 4.5 baseline of 62.6% vendor-reported.
- On LongMemEval-S parts, Honcho scored 90.0% vendor-reported on single-session preference against 23.3% for the baseline, and 85.0% vendor-reported on multi-session reasoning against 46.6% for the baseline.
- On LoCoMo (a long-conversation question-answering test with single-hop, temporal, multi-hop, and open-domain questions), Honcho scored 89.9% vendor-reported overall.
- The custom XR reasoning model (Neuromancer XR, a fine-tune of Qwen3-8B) scored 86.9% vendor-reported overall as the conclusion-writing model, against 80.0% for Claude 4 Sonnet and 69.6% for Qwen3-8B base, with final answers always from Claude 4 Sonnet.
- On BEAM (Beyond a Million Tokens, an ICLR 2026 test with 100 conversations, 2,000 questions, and 10 memory skills), Honcho scored 0.630 at 100K tokens, 0.646 at 500K, 0.618 at 1M, and 0.409 at 10M, all vendor-reported.
- Outside reports give useful context: the mem0 paper reports 66.9% for mem0 and 72.9% for full context on LoCoMo, while a third-party Omi repeat reports 58.4% for Zep, 74% for Letta, 86.6% for Omi, and 92.5% vendor-reported for the closed mem0 platform.
- Scores move by 15 to 25 percentage points when the LLM judge or test setup changes, so vendor baseline choices matter; Honcho's maker publishes an open test kit at github.com/plastic-labs/honcho-benchmarks and claims 60-90% token savings, but independent repeats are still pending.
---
## What each benchmark measures
LongMemEval-S (S stands for small, single-model version) tests memory over very long chats. It uses 500 conversations of about 115,000 tokens each (a token is a small piece of text, roughly part of a word). Question types include single-session preference (remember what one user likes), multi-session reasoning (join facts across several chats), and knowledge updates (handle facts that change over time).
LoCoMo (Long Conversation Memory) tests question answering over long multi-turn talks. Its question types are single-hop (one fact), temporal (time order and dates), multi-hop (join several facts), and open-domain (broad knowledge), with adversarial (tricky or misleading) questions in the full set.
BEAM (Beyond a Million Tokens, presented at ICLR, the International Conference on Learning Representations, in 2026) tests memory as chats grow from thousands to millions of tokens. It uses 100 conversations and 2,000 questions across 4 sizes (128K, 500K, 1M, and 10M tokens) and 10 memory skills. Its simple baseline method is called LIGHT.
## Honcho scores by benchmark
All Honcho scores in this table are vendor-reported.
| Benchmark | Size and setup | Honcho score | Baseline for context |
|---|---|---:|---|
| LongMemEval-S overall | 500 chats, about 115K tokens each | 90.4% vendor-reported | 62.6% for Claude Haiku 4.5 vendor-reported (+27.8 points for Honcho) |
| LongMemEval-S single-session preference | Likes and facts in one session | 90.0% vendor-reported | 23.3% for baseline vendor-reported |
| LongMemEval-S multi-session reasoning | Facts spread over sessions | 85.0% vendor-reported | 46.6% for baseline vendor-reported |
| LoCoMo overall | Long talks, 4 question types | 89.9% vendor-reported | See XR and third-party tables below |
| BEAM-100K | 100K-token scale | 0.630 vendor-reported | LIGHT baseline is much lower; see third-party table |
| BEAM-500K | 500K-token scale | 0.646 vendor-reported | Same test family, larger input |
| BEAM-1M | 1M-token scale | 0.618 vendor-reported | Same test family, larger input |
| BEAM-10M | 10M-token scale | 0.409 vendor-reported | Score drops as input grows to 10M |
## XR ablation: which model writes the conclusions
This test keeps the final answer model fixed as Claude 4 Sonnet and only swaps the model that writes logic conclusions. All scores in this table are vendor-reported.
| Conclusion model | Overall | Single-hop | Temporal | Multi-hop | Open-domain |
|---|---:|---:|---:|---:|---:|
| XR | 86.9% vendor-reported | 81.0% vendor-reported | 89.4% vendor-reported | 84.4% vendor-reported | 88.4% vendor-reported |
| Claude 4 Sonnet | 80.0% vendor-reported | not split out | not split out | not split out | not split out |
| Qwen3-8B base | 69.6% vendor-reported | not split out | not split out | not split out | not split out |
The gap is 6.9 points for XR over Sonnet and 17.3 points for XR over its Qwen3-8B base, which the maker uses to argue that a small custom reasoning model beats a large general model at this step.
## Third-party comparison
These numbers come from outside papers and repeats, not from Honcho's maker, except where marked.
| Source | Test | Score |
|---|---|---:|
| mem0 paper, mem0 system | LoCoMo | 66.9% |
| mem0 paper, full context (all text in prompt) | LoCoMo | 72.9% |
| Omi repeat, Zep | LoCoMo | 58.4% |
| Omi repeat, Letta | LoCoMo | 74.0% |
| Omi repeat, Omi | LoCoMo | 86.6% |
| mem0 platform, vendor-reported, closed test | LoCoMo | 92.5% vendor-reported |
| Omi repeat, LIGHT baseline at 1M | BEAM-1M | about 34% |
| Omi repeat, Omi systems at 100K | BEAM-100K | 55% to 62.5% |
| Public report, Hindsight system at 100K | BEAM-100K | about 73% |
The spread shows why one number alone misleads: the same LoCoMo test gives 58.4% to 92.5% across systems, judges, and setups.
## Caveats: judges, baselines, and protocols
Most of these tests use an LLM as judge, which means another AI model grades the answers. Omi reports that only changing the judge can move scores by 15 to 25 percentage points. Vendors also pick their own baselines and prompts, so a weak baseline makes any gain look larger. The open test kit at github.com/plastic-labs/honcho-benchmarks helps because others can rerun the same steps, but a full independent repeat of Honcho's 90.4%, 89.9%, and BEAM numbers is still pending.
## Token efficiency and open harness
Honcho's maker claims 60-90% token savings vendor-reported, because it sends short logic conclusions instead of 100K raw tokens at query time. Storage and recall calls are free and unlimited on managed cloud; users pay for reasoning work, from 0.001 dollars for a minimal query to 0.50 dollars for a max query. The open harness holds the test scripts and prompts so others can check accuracy, cost, speed, and tokens together.
**Covers:** honcho.dev evals page + Neuromancer XR blog + public benchmark literature (retrieved 2026-09-10)
