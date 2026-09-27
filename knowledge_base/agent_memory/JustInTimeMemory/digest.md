> [[index|Wiki]] | [[summary|Summary]]
# Just-in-Time Memory: Learning to Curate Task-Adaptive Memory for LLM Agents — Digest

## 1. [[wiki/01-introduction-and-problem|Introduction and Problem: Write-Time vs Just-in-Time Memory Curation]]
**In one sentence:** The paper argues memory should not be distilled into fixed artifacts at write time — when the future query is unknown — but kept as raw trajectories and curated just-in-time at read time into a task-adaptive payload trained on immediate task success.
## Key points
- Agentic memory systems reuse past experience, but most curate at write time: a completed trajectory is distilled into a fixed artifact (reflection, workflow, skill, reasoning strategy) later retrieved by similarity.
- Write-time curation forces deciding what is worth remembering before the future query is known, irreversibly discarding information and producing a query-independent summary that must serve many downstream tasks.
- Learning a write-time curator is hard because a storage decision's value may only appear when a relevant query arrives many tasks later — a long-horizon credit-assignment problem.
- Just-in-Time Memory (JITMEM) instead retains raw trajectories and defers curation to read time, when the current task is known: a curator synthesizes a compact, task-adaptive payload from retrieved traces plus the new task.
- Because the payload is consumed on the same task, the curator trains directly from immediate task success, avoiding delayed utility signals and artificial grouping of related tasks.
- Across ALFWorld, WebShop, and τ2-bench, JITMEM beats no-memory agents and heuristic/learned write-time methods by 16.2, 16.3, and 3.9 absolute success-rate points over the strongest baseline, respectively.
- Even an untrained curator is already competitive with or surpasses these baselines, showing read-time task-adaptive curation itself is a major source of gain; training compounds it.

## 2. [[wiki/02-background-and-related-work|Background and Related Work: Read-Time vs Write-Time Memory Curation]]
**In one sentence:** JITMEM defers curation to read time so a task-conditioned curator can synthesize a compact payload from raw trajectories for the current task, simplifying credit assignment and outperforming write-time curators.
## Key points
- Write-time curation suffers because a trajectory admits many possible lessons but the downstream task is unknown at write time, so curation happens before the task is known.
- JITMEM keeps a passive episodic bank of raw trajectories with nothing discarded at write time; at read time a retriever selects relevant traces and curator πϕ synthesizes a compact task-conditioned payload.
- The same stored trajectory can yield different payloads for different downstream queries, paralleling the reconstructive episodic-memory view of Schacter & Addis (2007).
- Read-time curation collapses credit assignment to a single interaction because the payload is consumed immediately by the current task, avoiding the task-grouping scaffolds needed by learned write-time curators such as Ouyang et al. (2026a).
- JITMEM reports +16.2 (ALFWorld), +16.3 (WebShop), and +3.9 (τ2-bench) absolute success-rate points over all baselines, with compact payloads cutting input tokens 50.3%–56.3% and executor steps 28.4%–31.4% relative to write-time methods.
- Even untrained, read-time curation beats same-model write-time curation (WebShop JITMEM-gemini 61.0 SR vs SkillOS 41.0 SR, both with Gemini-2.5-Pro curator and executor); RL training compounds the gain and the trained curator transfers to stronger executors without retraining.
- Ablations attribute independent gains to task-conditioned curation, quality-filtered storage, and retention of raw trajectories.

## 3. [[wiki/03-method-retrieve-curate-execute|Method: Retrieve, Curate, Execute, Update]]
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

## 4. [[wiki/04-main-results-alfworld-webshop|Main Results on ALFWorld and WebShop]]
**In one sentence:** RL-trained read-time curation (JITMEM) beats the strongest write-time baselines by large margins on ALFWorld and WebShop across Qwen3-8B, Gemini-2.5-Pro, and GPT-5.4 executors.
## Key points
- With Qwen3-8B as executor, JITMEM reaches 77.4 SR on ALFWorld vs 61.2 for RL-trained SkillOS (+16.2), and 32.8 SR on WebShop vs 16.5 (+16.3), with WebShop Score 61.1 vs 40.6 (+20.5).
- With Gemini-2.5-Pro as executor, JITMEM reaches 86.2 vs 80.2 (+6.0) on ALFWorld and 50.5 vs 41.3 (+9.2) on WebShop.
- With GPT-5.4 as executor, JITMEM reaches 86.7 (+8.8) on ALFWorld and 45.4 (+10.9) WebShop SR, with Score 53.8 (+10.7).
- Training-free JITMEM-base already beats training-free baselines using the same Qwen3-8B curator: 60.5 SR vs 55.7 for ReasoningBank and 53.1 for SkillOS-base on ALFWorld (Qwen3-8B executor).
- A weaker curator can surpass stronger-curator baselines: with GPT-5.4 executor on ALFWorld, JITMEM-base with Qwen3-8B curator (79.3) outperforms ReasoningBank with GPT-5.4 curator (77.9) and SkillOS-gpt (70.0).
- The Qwen3-8B-trained curator transfers to GPT-5.4 without retraining, closing to within 1.4 SR points of one trained directly with GPT-5.4 (86.7 vs 88.1).
- Read-time curation is more token-efficient: with GPT-5.4 executor on ALFWorld, JITMEM-base adds only 1.9K input tokens over no memory (10.9K vs 9.0K) compared to 10.7K for ReasoningBank and 13.4K for SkillOS-base, while cutting steps by 18.5%–21.9%.

## 5. [[wiki/05-ablations-and-analysis|Ablations and Analysis: Write-Time Distillation, Bank Dynamics, and Task-Adaptivity]]
**In one sentence:** Replacing raw-trajectory storage with write-time (ReasoningBank-style) distillation hurts JITMEM-base by 1.7–2.9 points on ALFWorld and 6.8–8.2 on WebShop, while controls confirm the RL curator genuinely distills retrieved experience, staged bank refresh helps only modestly, test-bank warm-starting is negligible, and qualitative cases show the same trace curated differently per task with RL-added procedural semantics.
## Key points
- Applying ReasoningBank-style distillation to each trajectory before storage (saving only distilled items instead of raw traces) drops JITMEM-base by 1.7–2.9 on ALFWorld and 6.8–8.2 on WebShop across executors.
- Forcing the retriever to return an empty set degrades JITMEM to or below untrained JITMEM-base, with success rate (SR) dropping by up to 14.8 on ALFWorld and 15.2 on WebShop, confirming RL gains come from distilling retrieved experience rather than parametric hints.
- Staged bank refresh (after 100 GRPO steps, discard the training bank, rebuild it by re-running the executor with the trained curator, hold fixed, train 50 more steps) improves SR by 2.8 for Qwen3-8B and 0.9 for GPT-5.4, with no change for Gemini-2.5-Pro — modest relative to cost.
- Pre-populating the empty test bank with 100 training trajectories ("test bank warm-starting") changes SR by at most 1.3, within standard deviation, across all three executors.
- The same retrieved past experience is curated into different payloads per task (Figure 3): state-change/heat-cool guidance for "put a hot potato in fridge" versus placement/verify-target guidance for "put a newspaper in sofa."
- On identical inputs (Figure 4, "Examine the bowl with the desklamp"), the RL-trained curator recovers the environment-specific workflow (move to the desklamp, then examine the bowl with it) while the untrained curator gives only a generic action sequence.
- The paper concludes JITMEM's read-time curation turns curator learning into an immediate single-step objective and reports the untrained curator is already competitive with strong write-time baselines, with RL further improving effectiveness, efficiency, and cross-executor transfer; limitations are the BM25 retriever, one extra LLM call per task, and fixed hand-designed payload formats.

## 6. [[wiki/06-references|References (Liu–Zhou Block) and Appendix A Prompt Start]]
**In one sentence:** This chunk contains no new results — it is the bibliography tail from Liu et al. (2025) through Zhou et al. (2025) plus the start of Appendix A with the verbatim JITMEM Memory Curator prompts for ALFWorld, WebShop, and τ²-bench and the opening of the ALFWorld Executor prompt.
## Key points
- The chunk lists alphabetically ordered references spanning memory surveys, skill/experience learning, and agent benchmarks (e.g., Luo et al. ACL 2026 Findings pp. 41622–41652; Ma et al. ACL 2026 pp. 34789–34812).
- Cited memory/skill methods include Skill-Os (Ouyang et al. arXiv:2605.06614), ReasoningBank (Ouyang et al. ICLR 2026 pp. 94327–94354), A-MEM (NeurIPS 38 pp. 17577–17604), and Agentic Plan Caching (NeurIPS 38 pp. 103270–103296).
- Cited agent benchmarks and frameworks include ALFWorld (Shridhar et al. ICLR 2021), WebShop (Yao et al. NeurIPS 35 pp. 20744–20757), Voyager (arXiv:2305.16291), and Reflexion (NeurIPS 36 pp. 8634–8652).
- Appendix A gives three JITMEM Memory Curator system prompts that all share the same structure: role as Memory Curator, synthesis of retrieved past experiences into a concise actionable briefing, and a user prompt with `{query}` plus numbered Memory blocks with `{memoryN_query}` and `{memoryN_trajectory}`.
- The ALFWorld curator prompt instructs the model to identify the most relevant past experiences, extract strategies such as where to find objects and useful action orders, and give specific guidance for the current task.
- The WebShop curator prompt instructs the model to extract how search was phrased, how the right product was chosen, how options (color, size) were set, and how the price constraint was met, while warning not to rely on specific product IDs and noting past trajectories may only partially satisfy their instruction.
- The τ²-bench curator prompt defines transcript roles ([USER] customer, [AGENT] messages/tool calls as `fn(arg=value)`, [TOOL] results), requires a short ordered plan (read/lookup tools, user confirmation, policy conditions verified, write/mutating calls), and forbids copying concrete identifiers or suggesting actions conflicting with domain policy.

## 7. [[wiki/07-appendix-prompts-a|Appendix A: Prompts — Executor, Judge, and Distillation Prompts]]
**In one sentence:** Appendix A provides the verbatim executor prompts for WebShop and τ2-bench, the LLM-as-judge prompt for τ2-bench, and the ReasoningBank-style distillation prompts for the ablation study, with ALFWorld/WebShop executor and judge prompts following SkillOS.
## Key points
- The first WebShop executor prompt injects step count, recent observation/action history, current observation, and admissible actions, then requires step-by-step reasoning aided by past experiences before emitting the choice inside `<action> </action>` tags.
- The second WebShop executor variant ("Current Progress") uses `{available_actions}` in place of `{admissible_actions}` and adds explicit search guidance: search with a short core product query, never pack color/size/price into the query, and retry zero-result searches with a shorter broader query.
- The WebShop search guidance defines the terminal goal mechanism as inspecting/selecting a matching product and eventually clicking `[buy now]`.
- The τ2-bench executor prompt frames the agent as a customer-service agent that per turn either sends a user message or makes a tool call (never both), must output valid JSON only, and must explicitly discuss whether to use past experiences at each step.
- The τ2-bench LLM-as-judge prompt credits success only when tool results confirm the requested booking/cancellation/update/refund/fix succeeded, ignores the agent's own claims, requires evidenced process steps, and outputs exactly `{ "success": <true|false>, "reasoning": "<one or two sentences citing the specific tool results that prove success or failure>" }`.
- The ReasoningBank-style distillation prompts for ALFWorld and WebShop each cap extraction at 3 non-overlapping, generalizable memory items and enforce the output schema `# Memory Item i / ## Title / ## Description / ## Content`.
- Provenance is stated explicitly: ALFWorld and WebShop executor and judge prompts follow SkillOS (Ouyang et al., 2026a), the τ2-bench executor prompt comes from the official benchmark with a separately designed judge prompt, and the distillation prompts are only for the ablation study in Section 4.2.

## 8. [[wiki/08-appendix-training-setup|Appendix: Training Setup (Hyperparameters and Optimization)]]
**In one sentence:** The curator is trained with GRPO for up to 100 steps on Qwen3-8B (non-thinking) using a constant-with-warmup learning rate of 1×10⁻⁶, group size 8, and low-variance KL loss (coef 1×10⁻³), with a Qwen3-8B executor served via vLLM retrieving k=3 memories per task.
## Key points
- Base curator policy is Qwen3-8B (non-thinking), trained with GRPO advantage estimator without std normalization.
- Optimization uses learning rate 1×10⁻⁶ with a constant schedule plus 5 warmup steps (0.05 ratio of 100 steps), max 100 RL steps, train batch 32 prompts and policy mini-batch 32.
- KL in reward is disabled; KL loss is enabled with low-variance KL at coefficient 1×10⁻³, clip range (0.2, 0.2), and token-mean loss aggregation.
- Curator rollout uses 8 samples per prompt (group size), max prompt length 32768, and max response length 8192 (ALFWorld) / 4096 (WebShop) at sampling temperature 1.0.
- Executor is Qwen3-8B (non-thinking) served via vLLM at temperature 1.0 / top-p 0.95 / top-k 20, max 4096 new tokens, max 30 env steps per game, 3 retrieved memories per task.
- Retrieval count is insensitive: on WebShop, k=3 vs k=5 changes success rate by <2 points (Qwen3-8B 32.8 vs 32.8, Gemini-2.5-Pro 50.5 vs 48.6, GPT-5.4 45.4 vs 45.3), so k=3 is used for efficiency.
- Consolidated ablations show removing retrieved trajectories from RL-trained JITMEM causes the largest drop (up to −14.8 SR ALFWorld, −15.2 SR WebShop), and removing raw trajectories costs up to −8.2 SR on WebShop.

## 9. [[wiki/09-appendix-example-payloads|Appendix: Example Payloads]]
**In one sentence:** The curator synthesizes task-specific guidance from retrieved trajectories, shown in one example payload per benchmark plus GRPO training curves where validation success rises and executor turns fall over 100 steps.
## Key points
- One curated payload is shown per benchmark, each pairing a task with the payload the curator synthesized from retrieved trajectories.
- On ALFWorld (Clean: "Put a clean plate in countertop"), the payload assembles a clean-and-place procedure from three partially relevant episodes (cooled plate, cleaned tomato, cleaned soapbar).
- The ALFWorld payload gives a 3-step strategy (locate plate on countertops, clean in sinkbasin, place on countertop) and 4-step specific guidance (go to countertop 1 or 2, take plate, clean at sinkbasin, return and place).
- On WebShop ("high speed flashes with usb port, usb256-pink, 512gb, under $40"), the payload converts searches for different products (men's t-shirts, gym shorts) into a search-phrasing and attribute-selection strategy for the current product.
- The WebShop payload prescribes precise search phrasing including product type, features, color, size, and price; exact color/size clicks ("usb256-pink", "512gb"); and price verification before purchase.
- On τ2-bench Telecom (unable to send MMS), the payload distills several MMS failure cases (Memories 1 and 3 same issue with travel/roaming and data-cap blockage; Memory 2 domestic app-permission/network-mode fix) into an ordered diagnostic procedure separating general resolution strategy from current-request guidance.
- The τ2-bench payload orders diagnosis as identify line, gather device/network state first, apply non-account fixes in order, check account-side blockers only after, and requires explicit user approval with confirmed amount/charge before the mutating `refuel_data` tool; it also warns not to assume line ID, roaming status, or data usage from memory.
- Figures 5 and 6 show GRPO training progress on ALFWorld and WebShop (Qwen3-8B executor) over 100 steps: validation success rate climbs steadily while executor turns per task fall, with stable training under a single task reward and no auxiliary content-quality reward, task grouping, or return shaping.

## The argument in five moves
1. Write-time curation decides what to remember before the future task is known, incurring irreversible information loss and forcing one fixed artifact to serve many queries.
2. JITMEM defers curation to read time: keep raw trajectories losslessly, retrieve top-k with BM25, and synthesize a task-conditioned payload consumed immediately by a frozen executor.
3. Because reward is immediate (zero temporal gap), the curator trains with plain GRPO on same-task success, needing no judge reward, task grouping, or return shaping.
4. Empirically, even the untrained read-time curator matches or beats strong write-time baselines, and RL training adds large gains (+16.2 ALFWorld, +16.3 WebShop, +3.9 τ2-bench) with fewer tokens/steps and cross-executor transfer.
5. Ablations confirm each piece matters — raw retention, task conditioning, quality filtering, retrieved-experience distillation — while bank-refresh and warm-start controls show the simple static-bank / cold-start setup suffices.
6. Therefore effective agent memory depends not only on what is stored but on when and for which task it is curated.
