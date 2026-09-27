> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Main Results on ALFWorld and WebShop
**In one sentence:** RL-trained read-time curation (JITMEM) beats the strongest write-time baselines by large margins on ALFWorld and WebShop across Qwen3-8B, Gemini-2.5-Pro, and GPT-5.4 executors.
## Key points
- With Qwen3-8B as executor, JITMEM reaches 77.4 SR on ALFWorld vs 61.2 for RL-trained SkillOS (+16.2), and 32.8 SR on WebShop vs 16.5 (+16.3), with WebShop Score 61.1 vs 40.6 (+20.5).
- With Gemini-2.5-Pro as executor, JITMEM reaches 86.2 vs 80.2 (+6.0) on ALFWorld and 50.5 vs 41.3 (+9.2) on WebShop.
- With GPT-5.4 as executor, JITMEM reaches 86.7 (+8.8) on ALFWorld and 45.4 (+10.9) WebShop SR, with Score 53.8 (+10.7).
- Training-free JITMEM-base already beats training-free baselines using the same Qwen3-8B curator: 60.5 SR vs 55.7 for ReasoningBank and 53.1 for SkillOS-base on ALFWorld (Qwen3-8B executor).
- A weaker curator can surpass stronger-curator baselines: with GPT-5.4 executor on ALFWorld, JITMEM-base with Qwen3-8B curator (79.3) outperforms ReasoningBank with GPT-5.4 curator (77.9) and SkillOS-gpt (70.0).
- The Qwen3-8B-trained curator transfers to GPT-5.4 without retraining, closing to within 1.4 SR points of one trained directly with GPT-5.4 (86.7 vs 88.1).
- Read-time curation is more token-efficient: with GPT-5.4 executor on ALFWorld, JITMEM-base adds only 1.9K input tokens over no memory (10.9K vs 9.0K) compared to 10.7K for ReasoningBank and 13.4K for SkillOS-base, while cutting steps by 18.5%–21.9%.
---
## Table 1: Results on ALFWorld and WebShop across three frozen executors
Gains in red are relative to the strongest baseline in each block. Means and standard deviations over 3 runs with different task orderings.

Executor Qwen3-8B — ALFWorld SR / WebShop Score / WebShop SR:
- No Memory: 47.9 1.2 / 33.3 0.7 / 9.8 0.5
- ReasoningBank (Qwen3-8B): 55.7 3.1 / 35.4 1.1 / 11.4 0.9
- MemP (Qwen3-8B): 49.7 0.7 / 35.7 0.9 / 12.0 0.5
- SkillOS-base (Qwen3-8B): 53.1 2.5 / 38.6 0.9 / 13.6 0.8
- SkillOS-gemini (Gemini-2.5-Pro): 50.7 3.6 / 38.1 1.0 / 13.2 0.9
- SkillOS (Qwen3-8B): 61.2 4.6 / 40.6 0.7 / 16.5 0.7
- JITMEM-base (Qwen3-8B): 60.5 2.6 / 32.5 3.2 / 11.7 0.5
- JITMEM (Qwen3-8B): 77.4 2.9 (+16.2) / 61.1 0.9 (+20.5) / 32.8 1.7 (+16.3)

Executor Gemini-2.5-Pro:
- No Memory: 66.4 2.0 / 48.6 0.3 / 38.4 0.5
- ReasoningBank (Qwen3-8B): 71.4 2.9 / 47.1 1.0 / 38.0 0.6
- ReasoningBank (Gemini-2.5-Pro): 78.6 2.9 / 50.8 1.5 / 40.2 1.3
- MemP (Qwen3-8B): 74.3 3.4 / 51.9 1.9 / 40.3 1.3
- MemP (Gemini-2.5-Pro): 77.1 2.1 / 51.3 1.2 / 39.8 1.0
- SkillOS-base (Qwen3-8B): 70.7 3.0 / 52.8 1.0 / 39.6 0.8
- SkillOS-gemini (Gemini-2.5-Pro): 79.3 2.6 / 54.7 1.0 / 41.0 1.2
- SkillOS (Qwen3-8B): 80.2 3.1 / 56.0 0.7 / 41.3 0.8
- JITMEM-base (Qwen3-8B): 80.0 1.5 / 54.7 1.4 / 44.4 0.6
- JITMEM (Qwen3-8B): 86.2 1.9 (+6.0) / 61.0 0.8 (+5.0) / 50.5 0.8 (+9.2)
- JITMEM-gemini (Gemini-2.5-Pro): 81.9 2.7 / 72.1 1.0 / 61.0 0.7

Executor GPT-5.4:
- No Memory: 62.6 0.3 / 40.9 0.5 / 32.6 0.6
- ReasoningBank (Qwen3-8B): 69.8 4.0 / 37.4 1.8 / 29.5 1.0
- ReasoningBank (GPT-5.4): 77.9 4.2 / 43.1 1.7 / 33.6 1.5
- MemP (GPT-5.4): 72.6 1.7 / 40.8 1.0 / 34.5 1.7
- SkillOS-base (Qwen3-8B): 66.9 1.8 / 39.7 2.2 / 31.0 2.0
- SkillOS-gpt (GPT-5.4): 70.0 3.3 / 33.3 1.1 / 26.9 1.4
- JITMEM-base (Qwen3-8B): 79.3 3.6 / 49.9 1.0 / 39.3 0.7
- JITMEM (Qwen3-8B): 86.7 0.7 (+8.8) / 53.8 0.3 (+10.7) / 45.4 0.0 (+10.9)
- JITMEM-gpt (GPT-5.4): 83.3 2.1 / 57.0 1.5 / 47.5 1.4

## Learned read-time vs learned write-time curation
When curators are RL-trained with the same Qwen3-8B base model, JITMEM outperforms SkillOS by 77.4 vs 61.2 (+16.2) on ALFWorld and 32.8 vs 16.5 (+16.3) SR on WebShop; with Gemini-2.5-Pro executor the gap is 86.2 vs 80.2 (+6.0) and 50.5 vs 41.3 (+9.2). The chunk notes this comes with a simpler setup: JITMEM uses only the task reward, while SkillOS requires an additional judge model for content-quality rewards and groups related tasks to create temporal dependencies.

## Transfer and efficiency notes in chunk
The JITMEM curator is trained once with Qwen3-8B as executor yet transfers to stronger executors without retraining; Table 3 (executor transfer on ALFWorld SR) reports No training 60.5 2.6 / 79.3 3.6, Trained w/ Qwen3-8B exec. 77.4 2.9 / 86.7 0.7, Trained w/ GPT-5.4 exec. — / 88.1 0.9, Transfer gap — / 1.4. Table 4 (ALFWorld, GPT-5.4 executor) reports input/output tokens (K) and steps: No Memory 9.0 / 1.40 / 17.8; ReasoningBank 19.7 / 1.26 / 16.2; SkillOS-base 22.4 / 1.36 / 16.9; JITMEM-base 10.9 / 1.00 / 13.2; JITMEM 9.8 / 0.87 / 11.6, with RL training reducing input tokens by 10.1%, output tokens by 13.0%, and steps by 12.1% over JITMEM-base.

**Covers:** Table 1: Results on ALFWorld and WebShop across three frozen executors (plus in-chunk Tables 2–4 carryover text)
