> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Method: Retrieve, Curate, Execute, Update
**In one sentence:** JITMEM runs a four-step loop — retrieve top-k raw trajectories, curate a task-adaptive payload, execute with a frozen executor, and update the bank on LLM-judged success — and trains only the curator with GRPO using immediate per-task reward.
## Key points
- The loop is Retrieve (ξ̂t = R(xt, Mt)), Curate (pt = πϕ(xt, ξ̂t)), Execute ((ξt, rt) = πL(xt, pt)), Update (Mt+1 = UPDATE(Mt, ξt, rt)); the payload pt is ephemeral and never stored, only ξt is considered for insertion.
- The memory bank stores complete unabstracted raw trajectories ξ = (x, o1, a1, …, on, an) with no summarization at storage time, so the same trace can be distilled differently per task.
- Admission is gated by the executor model as LLM-as-judge: UPDATE appends ξt only if the judge deems it successfully solved, keeping retrieved demonstrations as positive exemplars.
- Retrieval is untrained BM25 over task descriptions only (not trajectory content), fixed across train and test, with retrieved trajectories concatenated in ranked order for the curator.
- The curator outputs a compact natural-language briefing pt identifying relevant past experiences, extracted strategies, and specific guidance; because pt depends on xt, the same retrieved trajectory yields a different distillation per task.
- The executor πL is a frozen pretrained LLM that acts from the compact payload prepended to its prompt rather than consuming raw trajectories, and the same model serves as the LLM-as-judge; one trained curator can serve multiple executors without retraining.
- Curator training uses GRPO without a value network: per training task a group of G candidates is generated, the frozen executor attempts each, rewards rt ∈ [0,1] (binary success on ALFWorld and τ²-bench, continuous score on WebShop) give advantages Âi = rtⁱ − meanⱼ rtʲ (no std normalization), with loss LGRPO = −(1/G)·Σᵢ Âi·log πϕ(ptⁱ|xt, ξ̂t); credit assignment is immediate (zero temporal gap), unlike write-time storage decisions graded many tasks later.
- Training uses a fixed bank built by running the base executor without curator on the training set once and keeping successes via ground-truth labels (not the LLM judge); evaluation starts each test sequence from an empty bank (cold-start) with batched streaming updates, ground-truth verifier for scoring but LLM judge for bank admission, averaged over multiple random orderings.
---
## The four-step loop
- Quoted loop definition: "1. Retrieve: ξ̂t = R(xt, Mt), fetch the top-k raw trajectories from the memory bank. 2. Curate: pt = πϕ(xt, ξ̂t), synthesize a task-adaptive payload. 3. Execute: (ξt, rt) = πL(xt, pt), run the frozen executor with pt in context. 4. Update: Mt+1 = UPDATE(Mt, ξt, rt), append ξt to the bank if the quality gate accepts it."
- "The curated payload pt is ephemeral and is not stored. Instead, only the resulting trajectory ξt is considered for insertion into the memory bank."
## Memory bank
- Stores "complete, unabstracted trajectories" ξ = (x, o1, a1, …, on, an): task description plus full interleaved observation–action sequence.
- "No summarization, reflection, or skill abstraction is applied at storage time. Preserving raw traces is essential: it allows the curator to extract different information from the same trajectory for different tasks, an affordance lost when trajectories are distilled to fixed summaries at storage."
- Gating: "Since task success labels are unavailable at deployment, we use the executor model as LLM-as-judge … to gate which trajectories enter the bank: UPDATE appends ξt only if the judge deems the task successfully solved."
- Ablation pointer: "Section 4.2 ablates this choice against storing all trajectories and labeling each as success or failure when presented to the curator."
## Retrieval
- "The retriever R selects the top-k trajectories from M most relevant to the current task xt."
- "We use BM25 over task descriptions only (not trajectory content), keeping retrieval lightweight and decoupled from trajectory length."
- "We choose BM25 for consistency with baselines, and the framework places no constraint on the retriever. The retrieved trajectories are concatenated in ranked order and passed to the curator."
- "The retriever is not trained and operates identically at training and test time. The choice of k is reported in Appendix A."
## Memory curator
- Input: "a structured prompt containing the current task description xt followed by the k retrieved raw trajectories ξ̂t, delimited by lightweight separators."
- Output: "a compact natural-language memory payload pt = πϕ(xt, ξ̂t): a concise briefing that identifies the most relevant past experiences, extracts strategies that worked on similar tasks, and provides specific guidance for the current task (prompt in Appendix A)."
- Task-adaptivity: "Since pt depends on xt, the same retrieved trajectory yields a different distillation for each task that retrieves it — the task-adaptive property central to our approach."
## Agent executor
- "The executor πL is a frozen pretrained LLM that is never updated during curator training. Freezing the executor keeps the system modular: one trained curator can serve multiple executors without retraining, and the memory component can be evaluated in isolation."
- "The payload is prepended to the executor's prompt, providing task-relevant guidance extracted from past experience (prompt in Appendix A); the executor therefore acts from the compact curated payload rather than directly consuming the raw retrieved trajectories."
- "The same executor model also serves as the LLM-as-judge for the memory update policy."
## Curator training (GRPO)
- "To train the curator, we use GRPO: for each sampled training task xt, the retriever fetches trajectories ξ̂t from the memory bank and the curator generates a group of G candidate payloads {ptⁱ}."
- "The frozen executor attempts xt with each payload and returns the ground-truth task reward rtⁱ ∈ [0,1], the benchmark's native evaluation metric (binary success on ALFWorld and τ²-bench, continuous score on WebShop)."
- Advantages: "Âi = rtⁱ − meanⱼ rtʲ (we omit the standard-deviation normalization following Liu et al. (2025))" with loss "LGRPO = −(1/G)·Σᵢ Âi·log πϕ(ptⁱ | xt, ξ̂t), without a value network. The executor πL remains frozen throughout."
- Immediate credit: "rt is a direct function of the payload pt produced for that same task t, with no intervening steps: the temporal gap between the curator's action and its reward is zero. This makes credit assignment immediate and eliminates the need for task-grouping or delayed-return machinery. In write-time memory, by contrast, a storage decision at step s is graded only when a future task t > s retrieves the artifact, possibly many tasks later."
## Training bank vs deployment bank
- Deployment: "the memory bank grows online as tasks are solved."
- Training stabilization: "construct a fixed training bank by running the base executor (without the curator) on the training set once and retaining successful trajectories using ground-truth success labels rather than the LLM judge. This bank is held fixed throughout training, ensuring stable and reproducible learning."
- Distribution shift: "the training bank contains base-executor trajectories, while at test time the bank grows with curator-augmented ones. Section 4.2 studies a staged bank refresh to quantify and close this gap."
## Evaluation procedure and experiment setup (in chunk)
- "By default, the memory bank is initialized empty at the start of each test sequence; the training bank does not carry over. The bank grows organically as tasks are solved, so early tasks benefit less from memory than later ones, resulting in a natural cold-start effect."
- "For evaluation efficiency, we use a batched streaming protocol: tasks within a batch share the same memory bank state, and the bank is updated after each batch."
- "Task success is measured by the benchmark's ground-truth verifier, while the memory update policy uses the LLM judge to avoid leaking ground-truth labels into the bank."
- "Since both task ordering and batch composition affect performance, we report results averaged over multiple runs with different random orderings."
- Benchmarks named in chunk: ALFWorld (140 test tasks), WebShop (500 test instances), τ²-bench (airline, retail, telecom); metrics success rate plus averaged score on WebShop.
- Baselines named: no-memory frozen executor plus write-time ReasoningBank, MemP, SkillOS; "-base" (no curator training) and "-gpt/-gemini" (GPT-5.4 or Gemini-2.5-Pro zero-shot curator) variants.
- Executors: Qwen3-8B, Gemini-2.5-Pro, GPT-5.4; curator initialized from Qwen3-8B with thinking mode disabled, GRPO for 100 steps (learning rate 1×10⁻⁶, batch size 32, group size 8) using Qwen3-8B as training executor; retriever fixed across methods.

**Covers:** JITMEM method loop (Retrieve / Curate / Execute / Update), memory bank, BM25 retrieval, curator, frozen executor, GRPO training, training-bank construction, and evaluation/batched-streaming setup; chunk tail extends into Section 4 experiment setup and start of 4.1.
