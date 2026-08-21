---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: GraphPlanner

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. What are the three concrete challenges of agentic routing that motivate GraphPlanner, and which one does the paper call "deferred rewards"?

> [!tip]- Answer
> (1) diverse and complex relations among queries, responses, and LLM candidates; (2) deferred rewards — early routing decisions can cascade into redundant calls or degraded downstream reasoning, a hard credit-assignment problem; (3) under-exploited historical memories from past multi-agent workflows. "Deferred rewards" is challenge (2). See [[wiki/01-problem-and-preliminaries|Problem, Motivation & Preliminaries]].

### Q2. In GraphPlanner's action space, what does an action `a_t = (α_t, m_t)` consist of, and why does this make the action space size `|A| = 3K`?

> [!tip]- Answer
> `α_t` is the chosen agent role (planner, executor, or summarizer) and `m_t` is the chosen LLM backbone out of K candidates. Since there are 3 roles and K backbones, and any role can in principle pair with any backbone, the total number of possible actions is 3×K. See [[wiki/02-graphplanner-method|GraphPlanner Method]].

### Q3. Why does GARNet compute the historical graph embedding `H(his)` before the workflow graph embedding `H(loc)`, rather than encoding both independently?

> [!tip]- Answer
> The nested dual-graph encoding injects `H(his)` into the workflow encoder — `H(loc) = GARNet_θloc(G_workflow; H(his))` — so that current-step decisions are contextualized by accumulated historical experience rather than being computed in isolation; this lets the shared role-hub nodes carry historical signal into the local decision without adding extra nodes or an explicit temporal graph structure. See [[wiki/02-graphplanner-method|GraphPlanner Method]].

### Q4. What is the difference between Phase 1 and Phase 2 evaluation, and why does the paper design the experiment this way?

> [!tip]- Answer
> Phase 1 optimizes routing decisions *within* a user-predefined fixed workflow (choosing the LLM backbone for each already-specified agent slot, controlled by Depth/Width hyperparameters); Phase 2 requires the router to jointly generate the workflow topology (which agent roles exist and in what structure) *and* pick backbones. This isolates whether GraphPlanner's gains come purely from better model selection (Phase 1) or also from better workflow structure generation (Phase 2) — Phase 2's larger accuracy gain (+9.3% vs. +3.8%) shows workflow generation itself is a major source of improvement. See [[wiki/03-experiments-and-results|Experiments, Results & Conclusion]].

### Q5. On the history ablation (w/o History, Homo-Graph, Hetero-Graph vs. full GARNet), which variant drops accuracy the most, and what does this tell you about what GARNet is actually contributing?

> [!tip]- Answer
> Removing history entirely (w/o History) causes the largest accuracy drop across all five domains. This shows that GARNet's main value is not just distinguishing heterogeneous roles (which Hetero-Graph alone partially captures) but specifically integrating historical interaction memory — modeling not just who interacts, but how interactions evolve over time. See [[wiki/03-experiments-and-results|Experiments, Results & Conclusion]].

### Q6. GraphPlanner uses far more LLM training calls (4.25 avg.) than competitors like Router-R1 (~1.18) yet trains with dramatically less GPU compute (1.04 GiB vs. 186.26 GiB). How does the paper reconcile these two facts?

> [!tip]- Answer
> The extra LLM calls reflect more extensive multi-step planning per query during training (generating richer workflow trajectories), but GraphPlanner's actual trainable policy network (GARNet) is lightweight — a graph neural network with small hidden dimensions (32) rather than a full LLM fine-tune — so the GPU memory footprint of *training the policy* stays tiny even though more environment interactions are collected. See [[wiki/03-experiments-and-results|Experiments, Results & Conclusion]] and [[wiki/04-related-work-and-implementation|Related Work & Implementation Details]].

### Q7. What are the PPO hyperparameters used for GraphPlanner's policy training (discount factor, clipping threshold, epochs per update), and on what hardware was it trained?

> [!tip]- Answer
> γ = 0.99, ϵ = 0.2 (clipping threshold), k = 4 epochs per update; hidden dimension 32, candidate embedding dim 1536, state embedding dim 768, Adam learning rate 3×10⁻⁴ (doubled for the value function), gradient clip norm 0.5, BF16 training, gradient checkpointing, on a single NVIDIA A6000 GPU. See [[wiki/04-related-work-and-implementation|Related Work & Implementation Details]].

### Q8. GraphPlanner generalizes zero-shot to two new agent roles (Thinker and Verifier) it was never trained with. How does its "New-role-zero-shot" performance compare to the original 3-role baseline, and what does adding a small amount of history data (New-role-few-shot) do?

> [!tip]- Answer
> New-role-zero-shot (same 3-role training, but the policy may choose among all 5 roles at test time) already beats the original 3-role GraphPlanner on all five domains (e.g. 68.5% vs. 67.0% on Math). New-role-few-shot augments the history graph with just 50 historical interactions (1% of training queries) paired with all five roles, lifting performance further (e.g. 69.6% on Math) — still below full retraining (New-role-train, 70.5%) but demonstrating the graph memory itself, not just retraining, drives generalization. See [[wiki/05-additional-ablations-and-generalization|Additional Ablations & Generalization]].

### Q9. Why does GraphPlanner beat LLM-based history-processing baselines (History-summary, History-retrieval) by such large margins on World Knowledge specifically (up to 171% relative improvement), while the gap is much smaller on Commonsense Reasoning (~4%)?

> [!tip]- Answer
> The wiki page attributes GraphPlanner's overall advantage to LLM-based summarization/retrieval struggling with highly heterogeneous, unstructured histories with mixed-quality reasoning traces that are hard to exploit when injected as raw text into a prompt, whereas GARNet's graph structure captures cross-interaction relations more principled-ly. The World Knowledge domain shows the largest relative gap, suggesting fact-heavy historical traces are the case where structured graph retrieval most outperforms lossy LLM summarization; Commonsense Reasoning's smaller gap suggests that domain's historical signal is either less critical or already well-captured by simpler summarization. See [[wiki/05-additional-ablations-and-generalization|Additional Ablations & Generalization]].

### Q10. In the three worked examples in Appendix K, how does the workflow topology differ between the math task, the code task, and the natural-QA task, and what does this reveal about GraphPlanner's decomposition behavior?

> [!tip]- Answer
> The math task uses a flat one-level fan-out (Planner creates parallel sub-queries, Executors answer them, Summarizer merges, final Executor answers); the code task uses two-level *nested* planning (a second Planner pass decomposes one sub-query further, with two Summarizer merge passes); the natural-QA task ("Who painted the Mona Lisa?") skips decomposition entirely — a single Executor step. This shows GraphPlanner adapts workflow depth and topology to task complexity rather than applying a fixed template. See [[wiki/06-prompt-templates-and-examples|Prompt Templates & Worked Examples]].

### Q11. What is the single strongest limitation in the evidence supporting GraphPlanner's claims of real-world robustness, based on the critical analysis?

> [!tip]- Answer
> All evaluation happens within a closed, fixed pool of 12 known LLM backbones and clean, non-adversarial historical interaction graphs; the paper never tests behavior with an open-ended/growing model pool, noisy or adversarially poisoned history, or role sets that must expand dynamically at inference time — so claims of "generalization" are generalization within a controlled benchmark design, not proof of production robustness. See [[critical_thinking|Critical Analysis]].

### Q12. If you wanted to apply GraphPlanner's core idea (shared role-hub nodes bridging a per-task memory graph and a cross-task historical memory graph) to a completely different domain — say, routing customer support tickets across a mix of internal agents and external vendors — what would you need to define as the equivalents of "role," "LLM backbone," and "workflow memory graph"?

> [!tip]- Answer
> "Role" would map to ticket-handling stages (triage, resolution, escalation, closure-summary); "LLM backbone" would map to the pool of available handlers (specific support agents, automated bots, or vendor teams); "workflow memory graph" would track the current ticket's handling history (who touched it, cost/time, resolution quality), while a "historical memory graph" would aggregate past tickets' handling patterns, all connecting through shared (handler, stage) hub nodes so that current routing decisions can draw on how that handler performed at that stage historically. See [[wiki/02-graphplanner-method|GraphPlanner Method]] and [[explainer|Plain-Language Explainer]].
