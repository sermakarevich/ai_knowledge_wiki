---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: Just-in-Time Memory: Learning to Curate Task-Adaptive Memory for LLM Agents

### Q1. What are the two fundamental costs of write-time memory curation?
> [!tip]- Answer
> Write-time curation decides what to remember before the future query is known, so information loss is premature and irreversible — discarded details can never be recovered by a later task. It also forces a single fixed artifact to serve many different future queries, even though the same trajectory may be useful in different ways depending on the task. See [[wiki/01-introduction-and-problem|Introduction and Problem: Write-Time vs Just-in-Time Memory Curation]].

### Q2. How does JITMEM restructure the agent memory pipeline at inference and training time?
> [!tip]- Answer
> At inference, the retriever fetches raw trajectories from a passive episodic bank, the curator distills them conditioned on the current task into a task-adaptive payload injected into the executor's context, and successful trajectories (per an executor-as-judge) are stored back. At training time, the curator generates multiple candidate payloads per task, the frozen executor attempts the task with each, and the immediate task reward updates the curator via GRPO. See [[wiki/01-introduction-and-problem|Introduction and Problem: Write-Time vs Just-in-Time Memory Curation]].

### Q3. Why does read-time curation simplify credit assignment relative to learned write-time curators such as SkillOS?
> [!tip]- Answer
> Because the curated payload is consumed on the same task it was produced for, the curator's reward is immediate — the temporal gap between action and reward is zero, collapsing credit assignment to a single interaction. A write-time storage decision, by contrast, is graded only when a future task retrieves the artifact, possibly many tasks later, forcing scaffolds like grouping related tasks to manufacture a delayed signal. See [[wiki/02-background-and-related-work|Background and Related Work: Read-Time vs Write-Time Memory Curation]].

### Q4. How does JITMEM differ from the closest read-time concurrent work, MemHarness?
> [!tip]- Answer
> MemHarness also curates at read time but trains a single GRPO policy that both adapts retrieved experience and executes the task, entangling curation and execution so the trained policy does not transfer across executors. JITMEM instead decouples the curator from a frozen executor and operates over a persistent streaming bank, so one trained curator can serve multiple executors without retraining. See [[wiki/02-background-and-related-work|Background and Related Work: Read-Time vs Write-Time Memory Curation]].

### Q5. What are the four steps of the JITMEM loop, and what is stored versus discarded?
> [!tip]- Answer
> The loop is Retrieve (fetch top-k raw trajectories), Curate (synthesize a task-adaptive payload), Execute (run the frozen executor with the payload in context), and Update (append the trajectory if the quality gate accepts it). The curated payload is ephemeral and never stored; only the resulting raw trajectory is considered for insertion into the bank. See [[wiki/03-method-retrieve-curate-execute|Method: Retrieve, Curate, Execute, Update]].

### Q6. How is curator training with GRPO formulated, and what reward does each candidate receive?
> [!tip]- Answer
> Per training task, the curator generates a group of G candidate payloads, the frozen executor attempts the task with each, and each candidate receives the benchmark's native reward (binary success on ALFWorld and τ²-bench, continuous score on WebShop). Advantages are computed as reward minus the group mean with no std normalization, and the loss is the group-averaged advantage-weighted log-likelihood with no value network. See [[wiki/03-method-retrieve-curate-execute|Method: Retrieve, Curate, Execute, Update]].

### Q7. How do the training bank, deployment bank, and evaluation protocol differ?
> [!tip]- Answer
> Training uses a fixed bank built once by running the base executor without the curator and keeping successes via ground-truth labels, ensuring stable learning. Evaluation starts each test sequence from an empty bank (cold-start) with batched streaming updates, scoring success with the ground-truth verifier while admitting trajectories via the LLM judge, averaged over multiple random orderings. See [[wiki/03-method-retrieve-curate-execute|Method: Retrieve, Curate, Execute, Update]].

### Q8. What are JITMEM's headline gains over the strongest baselines on ALFWorld and WebShop?
> [!tip]- Answer
> With Qwen3-8B as executor, JITMEM reaches 77.4 SR on ALFWorld versus 61.2 for RL-trained SkillOS (+16.2), and 32.8 SR on WebShop versus 16.5 (+16.3), with WebShop Score 61.1 versus 40.6 (+20.5). Gaps persist with stronger executors: +6.0 ALFWorld / +9.2 WebShop SR with Gemini-2.5-Pro, and +8.8 / +10.9 with GPT-5.4. See [[wiki/04-main-results-alfworld-webshop|Main Results on ALFWorld and WebShop]].

### Q9. What do the transfer and token-efficiency results show?
> [!tip]- Answer
> The curator trained once with Qwen3-8B transfers to GPT-5.4 without retraining, closing to within 1.4 SR points of one trained directly with GPT-5.4 (86.7 vs 88.1), and even training-free JITMEM-base with a Qwen3-8B curator beats stronger-curator write-time baselines. Read-time curation is also cheaper: with a GPT-5.4 executor on ALFWorld it adds only 1.9K input tokens over no memory versus 10.7K–13.4K for write-time methods, while cutting steps by roughly a fifth. See [[wiki/04-main-results-alfworld-webshop|Main Results on ALFWorld and WebShop]].

### Q10. What do the write-time distillation and empty-retrieval ablations prove?
> [!tip]- Answer
> Replacing raw-trajectory storage with ReasoningBank-style write-time distillation drops JITMEM-base by 1.7–2.9 points on ALFWorld and 6.8–8.2 on WebShop, confirming information lost at storage cannot be recovered at read time. Forcing the retriever to return an empty set degrades RL-trained JITMEM to or below the untrained baseline (up to −14.8 ALFWorld, −15.2 WebShop SR), confirming RL gains come from distilling retrieved experience rather than parametric hints. See [[wiki/05-ablations-and-analysis|Ablations and Analysis: Write-Time Distillation, Bank Dynamics, and Task-Adaptivity]].

### Q11. What do the bank-dynamics controls and qualitative cases show about task-adaptivity?
> [!tip]- Answer
> Staged bank refresh (rebuilding the training bank with curator-augmented trajectories) helps only modestly (+2.8 SR at best) and test-bank warm-starting changes SR by at most 1.3, so the static-bank / cold-start setup suffices. Qualitatively, the same retrieved trace is curated into different payloads per task (heat/cool guidance versus placement guidance), and the RL-trained curator recovers environment-specific workflows the untrained curator misses. See [[wiki/05-ablations-and-analysis|Ablations and Analysis: Write-Time Distillation, Bank Dynamics, and Task-Adaptivity]].

### Q12. How do the three JITMEM Memory Curator prompts differ across benchmarks?
> [!tip]- Answer
> All three share the same skeleton — Memory Curator role, synthesis of retrieved past experiences into a concise briefing, and a user prompt with `{query}` plus numbered Memory blocks. The ALFWorld prompt targets object locations and action orders, the WebShop prompt targets search phrasing, product choice, option-setting, and price constraints while warning against reusing product IDs, and the τ²-bench prompt defines transcript roles and demands an ordered plan ending in policy-compliant mutating calls without copying identifiers. See [[wiki/06-references|References (Liu–Zhou Block) and Appendix A Prompt Start]].

### Q13. What executor, judge, and distillation prompts does Appendix A specify, and where do they come from?
> [!tip]- Answer
> The WebShop executor prompts require step-by-step reasoning aided by past experiences with the choice in `<action>` tags plus search guidance (short core query, retry broader on zero results); the τ²-bench executor mandates valid JSON with either a message or a tool call per turn; and the τ²-bench judge credits only tool-confirmed outcomes via a strict success/reasoning JSON schema. The ReasoningBank-style distillation prompts cap extraction at 3 generalizable memory items in a fixed Title/Description/Content schema and are used only for the ablation. See [[wiki/07-appendix-prompts-a|Appendix A: Prompts — Executor, Judge, and Distillation Prompts]].

### Q14. What are the key GRPO and executor hyperparameters, and how sensitive is JITMEM to retrieval count?
> [!tip]- Answer
> The Qwen3-8B (non-thinking) curator trains up to 100 GRPO steps at learning rate 1×10⁻⁶ (constant with 5 warmup steps), group size 8, batch 32, low-variance KL loss at 1×10⁻³ with KL-in-reward disabled, and temperature 1.0 rollouts. Retrieval count is insensitive: on WebShop, k=3 versus k=5 changes success rate by under 2 points across all executors, so k=3 is used for efficiency. See [[wiki/08-appendix-training-setup|Appendix: Training Setup (Hyperparameters and Optimization)]].

### Q15. What do the example payloads and training curves demonstrate?
> [!tip]- Answer
> One payload per benchmark shows the curator assembling task-specific guidance from partially relevant episodes — a clean-and-place procedure on ALFWorld, search-phrasing plus attribute-selection strategy on WebShop, and an ordered MMS diagnostic separating general strategy from current-request guidance with explicit user-approval policy on τ²-bench. GRPO curves on ALFWorld and WebShop show validation success climbing while executor turns fall over 100 steps under a single task reward with no auxiliary shaping. See [[wiki/09-appendix-example-payloads|Appendix: Example Payloads]].

### Q16. (Evaluation) Should a team running LLM agents on evolving task streams replace a write-time skill library with JITMEM-style read-time curation?
> [!tip]- Answer
> Yes, if tasks are diverse and future queries are unpredictable: read-time curation preserves raw trajectories, adapts the same experience per task, trains on immediate reward, and empirically beats strong write-time baselines with fewer tokens and cross-executor transfer. Hold back if per-task latency budget forbids the extra curator LLM call, the bank will grow so large that BM25 retrieval bottlenecks, or hand-designed payload formats cannot cover the domain. See [[wiki/05-ablations-and-analysis|Ablations and Analysis: Write-Time Distillation, Bank Dynamics, and Task-Adaptivity]].
