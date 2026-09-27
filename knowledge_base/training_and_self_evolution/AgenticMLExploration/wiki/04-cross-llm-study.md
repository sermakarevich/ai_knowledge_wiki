> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Cross-LLM Study and Agent-Surfaced Techniques
**In one sentence:** With the agent loop, skills, and prompts held fixed while only the LLM (large language model) was swapped, L2 work split into two capability clusters led by Sonnet >=3.5, Gemini 2.5, and GPT-5, L3 results differed by model family and prompt stress with Sonnet 4.0 best under stress, and the strongest portfolio wins came from technique transfer.
## Key points
- The study held the agent loop, skills, and prompts fixed and swapped only the LLM (large language model) to separate harness effects from model effects.
- On L2 task completeness, Gemini 2.5 scored 100, Sonnet 4.0 scored 96.7, Sonnet 3.5 and 3.7 scored 93.3 each, GPT-5 scored 66.7, and GPT-4 scored 13.3.
- Weak models could not operate the workflow loop at all, often hallucinating workflow IDs or failing to wait for asynchronous jobs.
- Under the basic prompt on L3 architecture exploration, Gemini 2.5 and GPT-5 were the most aggressive explorers at 116.04 x1e-4 rMSE (relative mean squared error, a prediction-error metric where improvement means lower error) gain, while the Sonnet family stayed conservative.
- Under stressful competitive prompts the pattern flipped: Sonnet 4.0 gave the best overall result at 255.87 x1e-4 (about 2.6e-2) rMSE improvement, while GPT-5 retreated to 68.05 x1e-4 and gave back most of its basic-prompt gains.
- Table 2 lists five technique families with attempted counts bucketed as many (>=8 models), several (3-7 models), or few (<=2 models) and passed-gating counts bucketed as majority or mixed: SSL (self-supervised pretraining, a method that pre-trains on unlabeled data) many/majority, generic optimizer/loss tweaks many/mixed, embedding-based features several/majority, token-mixing architectures several/mixed, and architecture scaling few/mixed.
- The strongest portfolio results came from technique transfer to structurally similar models, while the agent struggled on models whose baseline had recently changed because its hypotheses were calibrated to the older version.
---
## Study design
The question is how much of A-MLE's behavior comes from the orchestration harness versus the underlying LLM (large language model). The team kept the agent loop, shared skill library, and prompts exactly the same and changed only the LLM. They then compared models from the Claude Sonnet, Gemini, and GPT families on L2 task completeness and L3 exploration outcomes.
## L2 task completeness by model
L2 measures whether the agent can complete assigned workflow tasks end to end. Scores split into two clear groups. The capable group scored in the high range: Gemini 2.5 at 100, Sonnet 4.0 at 96.7, and Sonnet 3.5 and 3.7 at 93.3 each, with GPT-5 also in the capable set at 66.7. The weak group could not run the loop at all, with GPT-4 at only 13.3. Common failure modes were hallucinating workflow IDs (inventing job names that do not exist) and failing to wait for asynchronous jobs (background jobs that finish later).
## L3 exploration outcomes: basic vs stressful prompts
L3 measures architecture exploration quality as rMSE (relative mean squared error, a prediction-error metric where larger improvement means a better model) improvement in units of x1e-4. Under the basic prompt, Gemini 2.5 and GPT-5 explored most aggressively, both around 116.04 x1e-4, while Sonnet models were conservative. Under stressful competitive prompts, Sonnet 4.0 jumped to 255.87 x1e-4, the largest improvement of any setup, while GPT-5 fell back to 68.05 x1e-4.
![Cross-LLM comparison: (a) L2 task completeness by model; (b) L3 rMSE improvement under basic vs stressful prompts](images/fig3-cross-llm.png)
## The three observations
First, at L2 the models form two clusters by capability, with Sonnet >=3.5, Gemini 2.5, and GPT-5 as the capable models and the rest unable to operate the loop. Second, at L3 the link between model and outcome is nuanced: Gemini 2.5 and GPT-5 push hardest under the basic prompt, while the Sonnet family plays conservatively. Third, prompt stress flips behavior by family: Sonnet 4.0 improves sharply under stress to about 2.6e-2 rMSE gain, while GPT-5 turns conservative and loses most of its basic-prompt gains.
## Technique families Table 2
Across the model portfolio during the evaluation window, A-MLE surfaced and validated techniques in five families. Attempted counts show on how many distinct models each family was tried. Passed-gating counts show only candidates that cleared the human-review statistical-significance bar without rework.
| Technique family | Attempted | Passed gating |
| --- | --- | --- |
| Self-supervised pretraining (SSL) | many | majority |
| Generic optimizer / loss tweaks | many | mixed |
| Embedding-based features | several | majority |
| Token-mixing architectures | several | mixed |
| Architecture scaling | few | mixed |
Bucket definitions: many means >=8 models, several means 3-7 models, few means <=2 models. Passed gating counts only candidates that cleared the human review bar without rework. SSL (self-supervised pretraining) means pre-training a model on unlabeled data before fine-tuning on the ranking task.
## Technique transfer as the strongest pattern
The agent's strongest results came from technique transfer. This means noticing that a technique already validated on one model, such as a model architecture change or an embedding-based feature variant (a new input feature built from learned embeddings), was likely to work on a structurally similar model that had not tried it yet. This reuse drove the biggest wins across the portfolio, including gains on long-tail models that had received little senior attention.
## Stale-baseline weakness
The agent struggled on models that had recently gone through non-trivial baseline changes. Its hypotheses were calibrated to the older version of the model, so ideas tuned for the prior baseline did not fit the new one. This shows the agent needs fresh baseline context after a model is changed.
**Covers:** Paper Sections 6.7-6.8.
