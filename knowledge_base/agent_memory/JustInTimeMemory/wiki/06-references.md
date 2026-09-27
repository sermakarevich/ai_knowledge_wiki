> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# References (Liu–Zhou Block) and Appendix A Prompt Start
**In one sentence:** This chunk contains no new results — it is the bibliography tail from Liu et al. (2025) through Zhou et al. (2025) plus the start of Appendix A with the verbatim JITMEM Memory Curator prompts for ALFWorld, WebShop, and τ²-bench and the opening of the ALFWorld Executor prompt.
## Key points
- The chunk lists alphabetically ordered references spanning memory surveys, skill/experience learning, and agent benchmarks (e.g., Luo et al. ACL 2026 Findings pp. 41622–41652; Ma et al. ACL 2026 pp. 34789–34812).
- Cited memory/skill methods include Skill-Os (Ouyang et al. arXiv:2605.06614), ReasoningBank (Ouyang et al. ICLR 2026 pp. 94327–94354), A-MEM (NeurIPS 38 pp. 17577–17604), and Agentic Plan Caching (NeurIPS 38 pp. 103270–103296).
- Cited agent benchmarks and frameworks include ALFWorld (Shridhar et al. ICLR 2021), WebShop (Yao et al. NeurIPS 35 pp. 20744–20757), Voyager (arXiv:2305.16291), and Reflexion (NeurIPS 36 pp. 8634–8652).
- Appendix A gives three JITMEM Memory Curator system prompts that all share the same structure: role as Memory Curator, synthesis of retrieved past experiences into a concise actionable briefing, and a user prompt with `{query}` plus numbered Memory blocks with `{memoryN_query}` and `{memoryN_trajectory}`.
- The ALFWorld curator prompt instructs the model to identify the most relevant past experiences, extract strategies such as where to find objects and useful action orders, and give specific guidance for the current task.
- The WebShop curator prompt instructs the model to extract how search was phrased, how the right product was chosen, how options (color, size) were set, and how the price constraint was met, while warning not to rely on specific product IDs and noting past trajectories may only partially satisfy their instruction.
- The τ²-bench curator prompt defines transcript roles ([USER] customer, [AGENT] messages/tool calls as `fn(arg=value)`, [TOOL] results), requires a short ordered plan (read/lookup tools, user confirmation, policy conditions verified, write/mutating calls), and forbids copying concrete identifiers or suggesting actions conflicting with domain policy.
---
## Reference list tail
**Covers:** pp. 11–13 bibliography entries, Liu et al. through Zhou et al.

| Citation (as in chunk) | Venue / identifier |
|---|---|
| Zichen Liu, Changyu Chen, Wenjun Li, Penghui Qi, Tianyu Pang, Chao Du, Wee Sun Lee, and Min Lin. Understanding r1-zero-like training: A critical perspective. | Second Conference on Language Modeling, 2025 |
| Jinghao Luo et al. From storage to experience: A survey on the evolution of llm agent memory mechanisms. | Findings of ACL: ACL 2026, pp. 41622–41652 |
| Wenquan Ma, Jiayan Nan, and Wenlong Wu. What deserves memory: Adaptive memory distillation for llm agents. | ACL 2026 Vol. 1 Long Papers, pp. 34789–34812 |
| Siru Ouyang et al. Skillos: Learning skill curation for self-evolving agents. | arXiv:2605.06614, 2026a |
| Siru Ouyang et al. Reasoningbank: Scaling agent self-evolving with reasoning memory. | ICLR 2026, vol. 2026, pp. 94327–94354 |
| Joon Sung Park et al. Generative agents: Interactive simulacra of human behavior. | ACM UIST 36th, pp. 1–22, 2023 |
| Stephen Robertson and Hugo Zaragoza. The probabilistic relevance framework: BM25 and beyond, vol. 4. | Now Publishers Inc, 2009 |
| Daniel L. Schacter and Donna Rose Addis. The cognitive neuroscience of constructive memory: remembering the past and imagining the future. | Phil. Trans. R. Soc. B, 362:773–786, 2007 |
| Zhihong Shao et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. | arXiv:2402.03300, 2024 |
| Maohao Shen et al. Decocted experience improves test-time inference in llm agents. | arXiv:2604.04373, 2026 |
| Noah Shinn et al. Reflexion: Language agents with verbal reinforcement learning. | NeurIPS 36:8634–8652, 2023 |
| Mohit Shridhar et al. {ALFW}orld: Aligning text and embodied environments for interactive learning. | ICLR, 2021 |
| Guanzhi Wang et al. Voyager: An open-ended embodied agent with large language models. | arXiv:2305.16291, 2023 |
| Jingxing Wang et al. Skills on the fly: Test-time adaptive skill synthesis for llm agents. | arXiv:2605.16986, 2026 |
| Lei Wang et al. A survey on large language model based autonomous agents. | Front. Comput. Sci. 18(6):186345, 2024a |
| Zora Zhiruo Wang et al. Agent workflow memory. | arXiv:2409.07429, 2024b |
| Rong Wu et al. Memharness: Memory is reconstructed, not replayed. | arXiv:2607.28272, 2026a |
| Yifan Wu et al. Remember when it matters: Proactive memory agent for long-horizon agents. | arXiv:2607.08716, 2026b |
| Wujiang Xu et al. A-mem: Agentic memory for llm agents. | NeurIPS 38:17577–17604, 2026 |
| Sikuan Yan et al. Memory-r1: Enhancing large language model agents to manage and utilize memories via reinforcement learning. | ACL 2026 Vol. 1 Long Papers, pp. 12805–12825 |
| Shunyu Yao et al. Webshop: Towards scalable real-world web interaction with grounded language agents. | NeurIPS 35:20744–20757, 2022 |
| Weiran Yao et al. Retroformer: Retrospective large language agents with policy gradient optimization. | ICLR 2024, vol. 2024, pp. 10091–10111 |
| Yi Yu et al. Agentic memory: Learning unified long-term and short-term memory management. | ACL 2026 Vol. 1 Long Papers, pp. 21457–21483, 2026a |
| Zhaochen Yu et al. Recursive experiential-working memory evolution for long-horizon agent harnesses. | arXiv:2608.24876, 2026b |
| Qianhao Yuan et al. Memsearcher: Training llms to reason, search and manage memory via end-to-end reinforcement learning. | arXiv:2511.02805, 2025 |
| Qizheng Zhang et al. Agentic plan caching: Test-time memory for fast and cost-efficient llm agents. | NeurIPS 38:103270–103296, 2026 |
| Andrew Zhao et al. Expel: Llm agents are experiential learners. | AAAI 38, pp. 19632–19642, 2024 |
| Longtao Zheng et al. Synapse: Trajectory-as-exemplar prompting with memory for computer control. | ICLR 12, 2024 |
| Huichi Zhou et al. Memento: Fine-tuning llm agents without fine-tuning llms. | arXiv:2508.16153, 2025 |

## Appendix A — JITMEM Memory Curator prompts (verbatim structure)
**Covers:** Appendix A, pp. 14–15: ALFWorld / WebShop / τ²-bench curator prompts plus Executor Prompt (ALFWorld) opening

Common user-prompt skeleton (all three tasks):

> `Question: {query}`
> `### Retrieved Memories:`
> `Memory 1: / Question: {memory1_query} / Trajectory: / {memory1_trajectory} / ...`

ALFWorld curator — verbatim directives:
> "You are a Memory Curator. You will be given a task that an AI agent needs to solve in a household (ALFWorld) environment, along with retrieved past experiences from similar successful tasks."
> "Your job: synthesize these raw memories into a concise, actionable briefing that will help the agent solve the current task."
> "Your output should: 1. Identify which past experiences are most relevant 2. Extract strategies that worked on similar tasks (e.g., where to find objects, useful action orders) 3. Give specific guidance for THIS task"
> "Be concise - the agent has limited context."

WebShop curator — verbatim directives:
> "You are a Memory Curator. You will be given a shopping task that an AI agent needs to solve in the WebShop e-commerce environment, along with retrieved past experiences from similar shopping tasks the agent completed with partial or full success."
> "Your output should: 1. Identify which past experiences target similar products and attributes 2. Extract strategies that worked - how the search was phrased, how the right product was chosen, how the requested options (e.g. color, size) were set, and how the price constraint was met before purchasing. A past trajectory may have only partially satisfied its instruction, so keep what generalizes. 3. Give specific, actionable guidance for THIS task"
> "Do not assume a past trajectory's exact product is still available, and do not rely on specific product IDs."
> "Be concise - the agent has limited context."

τ²-bench curator — verbatim directives:
> "You are a Memory Curator. You will be given a customer-service request that an AI agent must handle by talking to the user and calling tools, along with retrieved past experiences from similar requests the agent resolved successfully."
> "Each memory contains: - A past customer request and the transcript that resolved it. In the transcript, [USER] lines are the customer, [AGENT] lines are the agent's messages or its tool calls written as fn(arg=value), and [TOOL] lines are the tool results."
> "Your output should: 1. Identify which past experiences target the most similar request type 2. Extract the resolution strategy that worked, described as a short ordered plan: the read/lookup tools used to gather state, the confirmation the agent obtained from the user, the policy conditions verified, and the write/mutating tool call(s) that completed the task 3. Give specific, actionable guidance for THIS request"
> "Do not copy concrete identifiers or values from past memories (reservation IDs, confirmation numbers, user IDs, flight numbers, prices, dates) - always look up the current case with the tools. Never suggest an action that conflicts with the domain policy."
> "Be concise - the agent has limited context."

Executor Prompt (ALFWorld) — opening only (chunk truncates here):
> "You are an expert agent operating in the ALFRED Embodied Environment. Your task is to: {task_description}"
> "Here are past experiences and trajectories that might be helpful for your decision: {retrieved_context}"
> "## Current Progress" (cut off at chunk end)
