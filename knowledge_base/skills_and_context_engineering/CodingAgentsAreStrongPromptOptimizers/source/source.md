# Coding Agents are Strong Prompt Optimizers
Source: https://arxiv.org/pdf/2609.26261
Kind: pdf
Fetched: 2026-09-26T01:45:55.291845+00:00
Tool: pdftotext

                                                                         Coding Agents are Strong Prompt Optimizers
                                                                        Agamdeep Singh                  Srishti Gautam        Priyanshu Gupta
                                                                        Nikita Mehrotra                 Tanmay Bakshi          Sumit Gulwani
                                                                                        Microsoft
                                                   {t-agasingh, srgautam, priyansgupta, nmehrotra, t-tbakshi, sumitg}@microsoft.com




                                                                      Abstract                                   mains the same: iterative search driven by repeated rollouts




arXiv:2609.26261v1 [cs.AI] 13 Aug 2026
                                                                                                                 and validation.
                                           Search-based prompt optimizers improve prompts through it-
                                           erative search: they propose edits, execute fresh rollouts, score
                                                                                                                    This search-based recipe carries two structural limitations.
                                           the resulting trajectories, and retain only edits that improve a      First, every prompt revision must be validated through fresh
                                           validation metric. We show that this optimization loop is un-         environment interaction, keeping the environment, user sim-
                                           necessary. Given only a static corpus of agent trajectories,          ulator, and evaluation metric in the optimization loop while
                                           an off-the-shelf coding agent can directly synthesize an opti-        making cost grow with the number of candidate edits. More
                                           mized prompt, requiring neither environment access nor val-           fundamentally, each prompt revision is informed by only a
                                           idation data. We call this approach Coding-Agent Skill Dis-           small sample of trajectories, limiting the optimizer’s ability to
                                           tillation (CASD). The key insight is reflection scope. Rather         identify behavioral patterns that emerge only at corpus scale.
                                           than reasoning over a small batch of trajectories at each op-         For example, no single reflection step can reliably discover
                                           timization step, the coding agent writes and executes anal-           that a tool was invoked 284 times but duplicated 123 times,
                                           ysis code to compute corpus-wide statistics, identifies sys-
                                           tematic failure modes, inspects representative episodes, and
                                                                                                                 or that an entire task category failed in 24 of 24 attempts.
                                           distills the resulting insights into behavioral rules. Across four       We show that the optimization loop can be replaced by
                                           agentic benchmarks (ALFWorld, τ 2 -bench retail and telecom,          a single offline analysis pass over a static corpus of agent
                                           and SpreadsheetBench-Verified), under matched data access,            trajectories. Our approach, Coding-Agent Skill Distillation
                                           a single CASD pass outperforms GEPA, a state-of-the-art re-           (CASD; Figure 1), uses an unmodified, off-the-shelf coding
                                           flective prompt optimizer, on three of four benchmarks and            agent to analyze the corpus and directly synthesize an op-
                                           outperforms validation-gated reflective search (SkillOpt) on          timized prompt. The recipe is deliberately simple: provide
                                           all four, improving the unoptimized baseline by 16.6 per-             the coding agent with the rollout corpus and a short natural-
                                           centage points on average versus 10.9 for GEPA and 5.3
                                                                                                                 language instruction, then use the generated skill file as the
                                           for SkillOpt. Because CASD performs a single offline analy-
                                           sis pass rather than iterative search, producing an optimized         optimized system prompt. No optimization loop, validation
                                           prompt costs approximately $1.60—over 22× cheaper than                gate, environment interaction, or held-out validation set is
                                           validation-gated search. Even when competing methods are              required; prompt optimization becomes a single offline pass
                                           granted additional validation data and unrestricted environ-          costing about $1.60.
                                           ment access, CASD remains ahead on two of four benchmarks.               What replaces iterative search is corpus-scale reflection.
                                           These results suggest that corpus-scale statistical reflection is     Rather than reasoning over a small sample of trajectories, the
                                           a viable alternative to iterative search for prompt optimization.     coding agent writes and executes analysis code to compute
                                                                                                                 corpus-wide statistics—per-category pass rates, tool-call his-
                                                                                                                 tograms, duplicate-call counts, and argument-hallucination
                                                               1    Introduction                                 frequencies—before drilling into the episodes those statis-
                                         Large language model (LLM) agents are highly sensitive to               tics identify as most informative. Offloading the counting to
                                         their system prompts, motivating a growing line of work on              an interpreter is the same move that makes program-aided
                                         automatic prompt optimization. Search-based prompt opti-                prompting exact where free-form reasoning is not (Gao et al.
                                         mizers treat the prompt as a learnable artifact by iteratively          2023; Chen et al. 2023), applied here to the optimizer rather
                                         proposing prompt edits, evaluating them through fresh en-               than to the task solver. The resulting prompts are grounded in
                                         vironment rollouts, and retaining only those that improve a             measured evidence rather than anecdotal observations from
                                         validation objective (Zhou et al. 2023; Yang et al. 2024a;              a handful of trajectories.
                                         Pryzant et al. 2023; Khattab et al. 2024; Opsahl-Ong et al.                Across four agentic benchmarks, a single CASD pass out-
                                         2024). Recent methods such as GEPA (Agrawal et al. 2026)                performs GEPA, a state-of-the-art reflective prompt opti-
                                         strengthen this search process with natural-language reflec-            mizer, on three of four benchmarks and validation-gated re-
                                         tion, using language models to diagnose failures from sam-              flective search (SkillOpt) on all four when every optimizer
                                         pled trajectories before proposing revised prompts. Despite             is restricted to the same static rollout corpus. Even when
                                         these advances, the underlying optimization paradigm re-                the search baselines are granted additional validation data
Figure 1: A coding agent as a prompt optimizer. Left: Search-based optimizers (GEPA, SkillOpt) iteratively refine prompts
using environment rollouts and validation feedback. In contrast, CASD performs a single offline pass over a frozen rollout corpus
to directly produce the optimized skill file, without iterative search or additional environment interaction. Right: Across four
agentic benchmarks under matched data access, CASD achieves the largest average improvement while requiring substantially
lower optimization cost.


and unrestricted environment access that CASD never uses,          tions and demonstrations under a validation score. A parallel
CASD remains competitive, outperforming them on two of             evolutionary line—Promptbreeder (Fernando et al. 2023),
four benchmarks. Our contributions are as follows:                 EvoPrompt (Guo et al. 2024)—mutates and recombines a
                                                                   population, while PromptAgent (Wang et al. 2024b) plans
 • We characterize reflection scope as a fundamental design
                                                                   edits with MCTS. GEPA (Agrawal et al. 2026) is the strongest
   dimension for prompt optimization, showing that expand-
                                                                   reflective variant: it evolves a population of prompts, mutat-
   ing reflection from sampled trajectories to corpus-scale
                                                                   ing them with LM reflection over sampled trajectories and
   analysis can replace iterative validation-gated search.
                                                                   selecting on a Pareto front over a validation set. What unites
 • We present Coding-Agent Skill Distillation (CASD), a            the family is a scoring gate: every candidate must be re-
   prompt optimization framework that replaces iterative           executed and re-scored, so all of them need fresh rollouts per
   search with a single offline corpus-analysis pass using an      candidate. CASD needs none.
   unmodified off-the-shelf coding agent, eliminating vali-
   dation loops and additional environment interaction dur-           Learning from experience without weight updates. Re-
   ing optimization.                                               flexion (Shinn et al. 2023) and Self-Refine (Madaan et al.
                                                                   2023) convert per-episode failures into verbal feedback for
 • We evaluate CASD across four agentic benchmarks,
                                                                   the next attempt of the same task instance. Voyager (Wang
   showing that a single offline optimization pass consis-
                                                                   et al. 2024a) and ExpeL (Zhao et al. 2024) accumulate
   tently matches or outperforms state-of-the-art search-
                                                                   reusable skills or insights across episodes; Agent Workflow
   based prompt optimizers while substantially reducing op-
                                                                   Memory (Wang et al. 2025b) induces reusable workflows
   timization cost.
                                                                   from past trajectories; memory-stream architectures (Park
                                                                   et al. 2023) retrieve and reflect over stored observations. A
                   2    Related Work                               recent wave keeps this loop online at test time—Dynamic
Prompt optimization as search. Discrete prompt search be-          Cheatsheet (Suzgun et al. 2026), ReasoningBank (Ouyang
gins with gradient-guided token search (Shin et al. 2020) and      et al. 2025), and ACE (Zhang et al. 2025) curate an evolving
moves to LM-driven proposal: APE (Zhou et al. 2023) and            context from the agent’s own execution feedback. All of these
OPRO (Yang et al. 2024a) sample candidate instructions and         systems reflect trajectory-by-trajectory, with the LM’s con-
keep the best under a task metric; ProTeGi (Pryzant et al.         text window as the bottleneck and with long-context recall
2023) follows natural-language “textual gradients,” gener-         degrading as the digest grows (Liu et al. 2024). CASD differs
alized by TextGrad (Yuksekgonul et al. 2024) and Trace             in how the corpus is digested: by executable analysis code
(Cheng, Nie, and Swaminathan 2024) into backpropagation-           whose outputs (exact counts over all episodes) then direct tar-
like updates over compound systems; DSPy/MIPRO (Khat-              geted reading, so corpus size enters through the interpreter
tab et al. 2024; Opsahl-Ong et al. 2024) jointly tune instruc-     rather than through the context window.
   Coding agents. Tool-using coding agents (Yang et al.               The distillation process terminates when the agent writes
2024b; Wang et al. 2025a; Anthropic 2025) interleave code          the skill markdown file, which we use directly as the op-
execution, file inspection, and editing to resolve software        timized prompt p⋆ . The next subsection characterizes the
tasks, and are now strong enough on real repository-level          analysis strategy that emerges from this unconstrained in-
benchmarks (Jimenez et al. 2024) to be treated as general-         struction.
purpose analysts rather than code generators. We repurpose
one, unmodified, as an optimizer: the “program” it edits is a      3.3   Inside the distillation process
prompt, and the “test suite” it consults is a corpus of frozen     Given only the high-level instruction described above, the
rollouts.                                                          coding agent exhibits consistent analysis behavior across in-
   Offline improvement and conservatism. Improving a               dependent distillation runs. To characterize this behavior, we
policy from a fixed dataset without further interaction is         manually classify every tool call in the 24 logged distillation
the offline RL setting (Levine et al. 2020), where the central     runs (816 total tool calls) into four semantic categories: ex-
difficulty is over-estimation on out-of-distribution actions;      ploring the corpus layout (filesystem navigation; 94 calls),
BCQ (Fujimoto, Meger, and Precup 2019) and CQL (Kumar              computing corpus statistics (executing aggregation code over
et al. 2020) address it by constraining the improved policy        all episodes; 184), inspecting episodes (reading individual
to the data support, and one-step methods (Brandfonbrener          trajectories, either through code or file inspection; 510), and
et al. 2021) show that a single un-iterated improvement step is    writing the final skill file (28). Figure 2 summarizes every
often preferable to iterated updates when the dataset is small.    run. Three consistent analysis patterns emerge:
CASD is the textual analogue: a single, support-constrained        1. Exploration precedes synthesis. Exploration is front-
improvement step over a frozen corpus, with no off-policy              loaded (median first occurrence at position 0.0 of the run;
evaluation to gate it.                                                 34% of tool calls occur in the first fifth of the run and only
                                                                       5% thereafter), while skill writing is consistently terminal
  3   Method: Coding-Agent Skill Distillation                          (median position 1.0). Individual runs contain 16–51 tool
3.1   Problem Setup                                                    calls (mean 34.0) and produce a 5–8 KB skill file.
Let πθ (p) denote the target agent, where the model parame-        2. Statistics-guided investigation. Rather than reading
ters θ are fixed and only the system prompt p is optimized.            trajectories sequentially, the agent alternates between
Executing the initial prompt p0 over a training set produces           corpus-level statistical analysis and targeted inspection of
a rollout corpus                                                       individual episodes. It analyzes categories with poor pass
                                                                       rates, unusually long trajectories, repeated tool invoca-
                        D = {τi }Ni=1 ,                                tions, or early termination, then reads the corresponding
where each trajectory τi records the complete agent execu-             trajectories to verify hypotheses before deciding what to
tion, including messages, tool calls, tool outputs, rewards,           investigate next. Runs switch between these two modes
and execution metadata. The goal of offline prompt opti-               a median of five times (up to 16), suggesting an iter-
mization is to construct an improved prompt p⋆ from the                ative analysis strategy despite the prompt providing no
fixed rollout corpus alone,                                            prescribed analysis procedure.
                                                                       The executed analysis code consistently computes corpus-
                     p⋆ = CASD(D, p0 ),                                level statistics rather than simple summaries. Every run
without collecting additional trajectories or interacting with         measures rewards/pass rates and episode lengths, 96%
the environment. The remainder of this section describes how           quantify termination and failure modes, 92% analyze tool
CASD implements this offline distillation process.                     usage, 79% break performance down by task category,
                                                                       and one third explicitly search for duplicated tool invoca-
3.2   The Distillation Pass                                            tions (Figure 2b).
To instantiate CASD, we invoke an unmodified off-the-shelf         3. Evidence-grounded rule synthesis. The resulting skills
coding agent with access to the rollout corpus D and the               directly reference the measured behaviors they seek to cor-
initial prompt p0 . The agent receives a single high-level             rect (e.g., “16/50 episodes fabricated an identity-lookup
natural-language instruction to analyze the rollout corpus             argument” or “get_details_by_id was called 284
directly and produce an improved system prompt. Impor-                 times, 123 of them exact duplicates”). This grounding
tantly, we do not prescribe an analysis pipeline, optimization         is reflected in the generated artifacts themselves: the 12
procedure, evaluation metric, or intermediate representation.          CASD skills contain 54 quantitative evidence citations
Instead, the coding agent determines its own analysis process          (fractions, percentages, and measured counts; 4.6 per 1k
for extracting useful behavioral rules from the rollout corpus.        words, Figure 2c), compared with none across the four
                                                                       GEPA prompts and only one across the four SkillOpt
   “There is a results file here containing N agent rollout            prompts.
   trajectories for [task family]. Analyze it directly—no other
   inputs, no precomputed summaries—and distill a skill mark-         Taken together, these observations show that the cod-
   down file capturing the behavioral rules that would make a      ing agent follows a consistent workflow: it first computes
   future agent instance more accurate and more token/step-        corpus-level statistics, then uses those statistics to guide tar-
   efficient on this task family. Use your own judgment fully on   geted inspection of representative episodes, and finally syn-
   methodology. Write the skill file into this directory.”         thesizes evidence-backed behavioral rules into an improved
Figure 2: Inside the distiller. (a) Tool traces across 24 distillation runs show a characteristic workflow: exploration is front-
loaded, skill writing is terminal, and the intermediate steps alternate between corpus-statistics analysis and inspection of flagged
episodes. (b) Corpus statistics most frequently computed by the executed analysis code. (c) The resulting prompts consistently
cite quantitative evidence (fractions, percentages, and measured counts), reflecting the corpus-driven reasoning process.


prompt. The next section analyzes why this offline optimiza-            where ρ proposes a prompt modification from execution
tion regime behaves differently from iterative search-based          feedback ϕt , ⊕ applies the modification, and Π determines
optimizers.                                                          whether the updated prompt is accepted.
                                                                        Search-based methods instantiate this framework using
        4    Prompt Optimization Through                             sampled rollout batches together with validation estimates,
                Corpus-Scale Reflection                                                                               
                                                                                ϕsearch
                                                                                  t       =   {(τ, r)} x∈B t
                                                                                                             , r
                                                                                                               bval (p)  ,
Although recent prompt optimization algorithms differ oper-
ationally, they all optimize the same objective: improving a                                   1     X                        (2)
                                                                                rbval (p) =                 R(πθ (p), x),
prompt from execution experience to maximize the expected                                   |Dval |
                                                                                                   x∈Dval
reward of the target agent. Their primary distinction therefore
lies not in what they optimize, but in how prompt improve-              where Bt denotes the sampled rollout batch, Dval the val-
ments are inferred. Search-based optimizers repeatedly esti-         idation set, and both the execution feedback and validation
mate prompt updates from sampled trajectories and validate           score are Monte Carlo estimates computed from sampled
them through additional rollouts, whereas CASD performs a            trajectories.
single offline inference from corpus-level statistics computed          In contrast, CASD instantiates the same framework using
over a fixed rollout corpus. We first present a unified formu-       a fixed rollout corpus D,
lation of prompt optimization before analyzing the statistical                                                  
trade-offs induced by these different optimization regimes.                         ϕCASD = Φ(D), {τi }i∈I(Φ) ,               (3)
4.1   A Unified View of Prompt Optimization                             where Φ(D) denotes corpus statistics computed over the
Let                                                                  rollout corpus, and I(Φ) denotes the index set of represen-
                                                                     tative trajectories selected for detailed inspection. The next
                J(p) = Ex∼PX [R(πθ (p), x)]
                                                                     subsection analyzes the statistical consequences of these two
denote the expected task reward of the target agent under            feedback representations.
system prompt p. Prompt optimization seeks an improved
prompt that maximizes J(p) using execution experience. A             4.2   Bias–Variance Analysis of Prompt
broad class of prompt optimization methods can be written                  Optimization
in the common form
                                                                     The feedback representations in Equations (2) and (3) induce
                         h               i                           different statistical properties for prompt optimization. For
                pt+1 = Π pt ⊕ ρ(pt , ϕt ) ,           (1)            search-based methods, the validation score rbval (p) is a Monte
Carlo estimate whose variance decreases with the number of         Table 1: Limited-data regime (headline): held-out test ac-
validation episodes,                                               curacy (%), mean over 3 seeds (SD), when all optimizers see
                                                                   only the static rollout pool. ‡ ALFWorld SkillOpt uses its na-
                                      σ2                           tive scaffold (own baseline 58.7%); not directly comparable
                   Var[b
                       rval (p)] =           ,                     to column 2.
                                     |Dval |
where σ 2 denotes the per-episode reward variance. Conse-          Benchmark            Baseline CASD (ours)      SkillOpt      GEPA
quently, prompt updates are inferred from noisy feedback                                                                   ‡
whose reliability improves only through additional rollout         ALFWorld             56.7±1.2     83.3±2.3     68.0±2.0     74.0±2.0
                                                                   τ 2 retail           32.5±2.5     40.0±2.5     38.3±10.1    39.2±7.2
evaluations.
                                                                   τ 2 telecom          19.2±5.2     39.2±8.0     25.8±3.8     17.5±4.3
   By contrast, the corpus statistics Φ(D) are deterministic       SSB-Verified         39.3±3.1     51.3±3.1     38.7±2.3     60.7±3.1
functions of the observed rollout corpus. Once the rollout
corpus has been collected, they eliminate the minibatch sam-       Mean gain vs. base      —          +16.6         +5.3        +10.9
pling variance associated with repeatedly estimating feed-
back from sampled trajectory subsets.
   The resulting optimization procedures therefore occupy             Models. Target agent (and user simulator, where appli-
different points on the bias–variance trade-off. Search-based      cable): GPT-5.4-mini with reasoning disabled (no-think)
optimization relies on Monte Carlo feedback with decreas-          throughout. Optimizer/reflection LM for all methods: Claude
ing variance as additional rollouts are collected. In contrast,    Sonnet 5. Test accuracy is the mean over 3 seeds; parenthe-
CASD reduces estimator variance by aggregating evidence            sized values are sample SD (n−1). At these evaluation-set
over the entire rollout corpus, at the cost of introducing bias    sizes the binomial standard error alone is ≈7 points per seed,
whenever the rollout corpus fails to capture important behav-      so we report seed-level dispersion throughout rather than
iors. The next subsection analyzes the practical implications      single point estimates (Miller 2024).
of this trade-off.                                                    Methods. Baseline: no skill, cost $0. CASD (ours): one
                                                                   distillation pass per skill over the static pool rollouts; we syn-
4.3   Operating Regimes                                            thesize 3 skills per benchmark and report their mean (so our
The preceding analysis suggests that the effectiveness of          SD measures skill-to-skill variance; baselines’ SD measures
prompt optimization depends on the available optimization          seed-to-seed variance of one skill). GEPA (Agrawal et al.
budget. Under limited rollout budgets, reducing estimator          2026): evolutionary reflective prompt optimization. SkillOpt:
variance is often more valuable than eliminating asymptotic        reflective search with a validation-selection gate.
bias. In this regime, CASD can simultaneously improve opti-           Data regimes. In the limited-data regime—our headline
mization effectiveness while operating at substantially lower      comparison—every optimizer sees only the same fixed pool
optimization cost by replacing iterative search with a single      (retail 35, telecom 50, SSB 50 tasks; a 50-game ALFWorld
offline distillation step.                                         pool): GEPA sets its Pareto set equal to train, SkillOpt splits
   As additional rollout data and environment interaction be-      the pool internally. In the head-to-head regime, GEPA and
come available, the variance of search-based optimization          SkillOpt additionally receive a separate held-out validation
decreases while the bias associated with a fixed rollout cor-      set (and, as always, unlimited environment access for candi-
pus remains unchanged. Consequently, the relative advantage        date rollouts) that CASD never uses.
of offline distillation is expected to diminish, and iterative        Optimizer settings and hyperparameters For repro-
search becomes increasingly attractive as its lower asymp-         ducibility: all methods use Claude Sonnet 5 as the reflec-
totic bias begins to dominate.                                     tion/optimizer LM. GEPA runs with a budget of 120 metric
   These observations suggest that offline corpus-scale reflec-    calls, with its Pareto set equal to train in the limited-data
tion and iterative search occupy complementary operating           regime; resuming the telecom run to 240 calls returned a
regimes rather than optimizing different objectives. Offline       byte-identical prompt, so we report the 120-call point. Skil-
distillation is particularly well suited to budget-constrained     lOpt runs 3–5 epochs with minibatch size scaled to the train
optimization, whereas iterative search is expected to benefit      split (8–40), an edit budget of 4 per step (cosine-decayed to
more from abundant interaction budgets.                            2), and its validation gate enabled; its internal split is 25/10
                                                                   on retail and 35/15 elsewhere for limited data regime setting.
               5    Experimental Setup                                                      6      Results
Benchmarks. (i) ALFWorld (Shridhar et al. 2021): em-
bodied household tasks, ReAct-style scaffold (Yao et al.           6.1   Matched data access: one pass beats the loops
2023), win rate on 50 held-out games. (ii/iii) τ 2 -bench retail   Table 1 and Figure 3 give the headline comparison. With
and telecom (Barres et al. 2026), the dual-control successor       every optimizer restricted to the same static pool, CASD is
to τ -bench (Yao et al. 2024): tool-using customer-service         best on ALFWorld (83.3 vs. GEPA’s 74.0), retail (40.0 vs.
agents against an LM user simulator, pass@1 on 40 held-out         39.2), and telecom (39.2 vs. 17.5), and second on SSB (51.3
tasks. (iv) SpreadsheetBench-Verified (SSB), derived from          vs. GEPA’s 60.7). Averaged over benchmarks, CASD lifts
SpreadsheetBench (Ma et al. 2024): spreadsheet manipula-           the baseline by +16.6 points, versus +10.9 for GEPA and
tion, modified accuracy on 50 held-out items.                      +5.3 for SkillOpt. Telecom is the sharpest separation: with
Table 2: Head-to-head regime: GEPA and SkillOpt addi-                6.3    Cost
tionally get a separate held-out validation set and environ-
                                                                     Table 3 summarizes production cost. A CASD pass costs
ment access; CASD is unchanged (it uses neither). ALF-
                                                                     ≈$1.60 per skill —one multi-tool coding-agent session, with
World cells repeat the limited-data runs (no separate head-
                                                                     no rollout bill because the corpus is a byproduct of rollouts
to-head run exists).
                                                                     that were already generated. Totaled over the four bench-
                                                                     marks this is 22× cheaper than SkillOpt ($142.5) and still
  Benchmark      Baseline CASD (ours)      SkillOpt     GEPA         less than GEPA ($8.4); unlike both, it also runs where no sim-
                                                   ‡                 ulator, grader, or validation split exists. Optimized prompts
  ALFWorld       56.7±1.2     83.3±2.3     68.0±2.0    74.0±2.0
  τ 2 retail     32.5±2.5     40.0±2.5     38.3±10.1   46.7±8.0      also shift test-time cost: e.g., on telecom, SkillOpt’s prompt
  τ 2 telecom    19.2±5.2     39.2±8.0     44.2±5.2    15.8±5.2      induces 20.1M prompt tokens over the 3-seed evaluation
  SSB-Verified   39.3±3.1     51.3±3.1     48.0±2.0    56.7±1.2      versus 11.9M for GEPA’s, a reminder that verbose optimized
                                                                     prompts are not free to deploy.

                                                                     6.4    Why does corpus-scope reflection win?
                                                                     Three observations support the reflection-scope explanation.
                                                                     (1) The rules are statistical, not anecdotal. The telecom
                                                                     skill’s top rule targets fabricated identity-lookup arguments
                                                                     observed in 16/50 episodes; no single-minibatch reflection
                                                                     reliably surfaces a 32%-frequency error, and GEPA’s telecom
                                                                     prompts never address it. (2) Efficiency rules need duplicate
                                                                     counts. Detecting that 123 of 284 get_details_by_id
Figure 3: Limited-data regime: held-out test accuracy over 3         calls were exact duplicates requires joining tool calls across
seeds (bars: mean; whiskers: SD). A single CASD pass over            a whole episode set—a one-liner in pandas, but invisible in a
the static pool beats GEPA on 3/4 benchmarks and SkillOpt            context-window reflection. (3) No gate, no gate-overfitting.
on 4/4.                                                              Search methods keep an edit only if a small validation batch
                                                                     approves, which both overfits small pools (Smith and Winkler
                                                                     2006; Dwork et al. 2015) (GEPA-telecom-LD collapsing to
Table 3: Optimizer cost to produce each prompt (USD;                 17.5) and inflates variance (SkillOpt retail SD 10.1). CASD’s
with token-caching on). GEPA/SkillOpt telecom and                    single pass has no acceptance step to overfit; its variance
SSB(SkillOpt) costs are from the head-to-head runs. CASD             across independently produced skills is small (SD ≤ 3.1 on
needs no environment rollouts at all.                                3 of 4 benchmarks).
                                                                        Figure 4 makes the mechanism concrete on a single test
                    ALFWorld Retail Telecom SSB Total                episode. The ticket has two independent root causes, and
      CASD (ours)      1.6       1.6     1.56     1.6 6.4            reward is granted only if the target agent repairs both. The
      GEPA             2.1      1.1      4.5     0.74 8.4            device-side cause is the kind of failure a minibatch reflection
      SkillOpt        15.9      13.9     74.7    38.0 142.5          can see—it is visible in any individual failed trajectory—and
                                                                     all three optimizers encode a rule for it. The account-side
                                                                     cause is not: it appears in the corpus only as an absence, a
                                                                     payment call that no rollout ever makes, which is a statement
no external validation signal, GEPA’s evolutionary loop de-
                                                                     about the whole pool rather than about any one episode it
grades below baseline (17.5 vs. 19.2)—its edits are selected
                                                                     contains. Only CASD writes a rule for it, and only CASD
on the same pool it reflects on, and overfit—while the cod-
                                                                     solves the episode.
ing agent’s statistics-first analysis of the identical data yields
+20.0 points.                                                        6.5    Ablation: does the skill recover thinking?
                                                                     Our target model runs with reasoning disabled, so a natural
6.2    Head-to-head: search buys back some ground,                   reference point is the same model with reasoning turned on
       at a price                                                    (Wei et al. 2022; DeepSeek-AI 2025)—the canonical way
                                                                     to trade output tokens for accuracy at test time (Snell et al.
When GEPA and SkillOpt are granted an extra validation set
                                                                     2025). How much of the accuracy that thinking buys can a
and unrestricted environment rollouts (Table 2), they improve
                                                                     distilled prompt recover, and at what token cost? Table 4 com-
where validation is informative: GEPA reaches 46.7 on retail
                                                                     pares three modes of GPT-5.4-mini on all four benchmarks:
and SkillOpt 44.2 on telecom. CASD, which touches neither
                                                                     no-think, no-think with the CASD skill, and think.1
the environment nor a validation set, still wins ALFWorld
                                                                        Two findings. (1) Distilled rules substitute for much of
outright and remains within noise of the best telecom cell
                                                                     test-time reasoning. On ALFWorld and retail the skill ex-
given its skill-to-skill SD. Notably GEPA still fails on tele-
com (15.8) even with validation—reflective mutation never                1
                                                                           Think accuracies and per-episode token counts come from an
finds the domain’s core failure modes—whereas SkillOpt               earlier study on the same test splits (except SSB think, which used a
only fixes telecom by spending $74.7 of gated search (Ta-            different harness and is indicative). Baseline and CASD accuracies
ble 3).                                                              are from the current runs in Table 1.
Figure 4: Corpus-level absences are invisible to minibatch reflection. A τ 2 -telecom “no service” ticket requires repairing
two independent root causes. Columns show the prompts distilled by the three optimizers from the same 50-rollout pool and
the resulting agent behavior. The device issue is evident in individual trajectories and is captured by all methods. In contrast,
the billing issue appears only as a corpus-level absence—make_payment is never invoked in the rollout pool. Only CASD
identifies this missing behavior from corpus-level statistics and distills the required billing rule, whereas GEPA and SkillOpt
omit it and fail the task.


Table 4: Recovering the reasoning gap without reason-              richment, needed at most once at corpus-construction time.
ing tokens (GPT-5.4-mini). “Rec.” = fraction of the no-            The residual gaps on telecom and SSB suggest a portion
think→think accuracy gap recovered by the skill; tok = mean        of thinking—presumably instance-specific deduction rather
output tokens per episode (think → skill).                         than reusable policy—that no static prompt recovers; closing
                                                                   it is future work.
Benchmark      no-think +CASD      think     Rec.      tok (↓)
ALFWorld        56.7      83.3    71.3±1.2 >100% 3.7k→0.8k                              7    Limitations
τ 2 retail      32.5      40.0    35.0±6.6 >100% 1.6k→0.6k
τ 2 telecom     19.2      39.2    45.0±2.5 78% 2.1k→0.6k           Our SD for CASD measures skill-to-skill variance (3 inde-
SSB-Verified    39.3      51.3    61.3±1.2 55% 3.3k→0.8k           pendently distilled skills, one evaluation each) while base-
                                                                   lines report seed variance of a single prompt; the quantities
                                                                   are close but not identical. All results use one target model
ceeds the think mode outright (83.3 vs. 71.3; 40.0 vs. 35.0);      (GPT-5.4-mini no-think) and one coding agent (Claude Son-
on telecom and SSB it recovers 78% and 55% of the no-              net 5/Claude Code); the recipe’s sensitivity to distiller capa-
think→think gap. It does so while emitting zero reasoning          bility is untested. Finally, CASD inherits the corpus: it cannot
tokens: per-episode output stays at or below the no-think bud-     discover behaviors absent from the logged rollouts and very
get (0.6–0.8k tokens), where thinking costs 2.9–4.5× more.         small or failure-free corpora may leave nothing to distill.
The interpretation is that much of what reasoning re-derives
episode after episode—which diagnostic to run next, when                                8    Conclusion
a lookup argument is unjustified, when not to give up—is
policy-like and can be crystallized once, offline, into explicit   A stock coding agent, pointed at a directory of frozen roll-
rules. (2) The distillation corpus need not contain think-         outs with a one-paragraph instruction, is a strong prompt
ing. In the earlier study round we also distilled skills from      optimizer: it beats state-of-the-art reflective search under
think rollouts of the same pools (a contrastive think-vs-no-       matched data access on 3 of 4 agentic benchmarks, never
think corpus) and deployed them on the no-think policy:            touches the environment, and costs about $1.60 per prompt.
across benchmarks the two corpus compositions land within          The key difference is reflection scope—executing analysis
a few points of each other with no consistent winner (e.g.,        code over the entire rollout corpus instead of relying on
ALFWorld 81.3 think-distilled vs. 78.7 no-think-distilled; re-     minibatch reflection and validation gating. As coding agents
tail 45.8 vs. 40.8; telecom 32.5 vs. 33.3; SSB reversed, 46.0      improve, offline corpus-scale reflection may become the de-
vs. 56.0). Failure-rich no-think rollouts alone carry enough       fault first step of prompt optimization, with search reserved
signal; expensive reasoning traces are optional corpus en-         for the final gains when additional interaction is inexpensive.
                        References                                  2024. DSPy: Compiling Declarative Language Model Calls
Agrawal, L. A.; Tan, S.; Soylu, D.; Ziems, N.; Khare, R.;           into Self-Improving Pipelines. In International Conference
Opsahl-Ong, K.; Singhvi, A.; Shandilya, H.; Ryan, M. J.;            on Learning Representations (ICLR).
Jiang, M.; Potts, C.; Sen, K.; Dimakis, A. G.; Stoica, I.; Klein,   Kumar, A.; Zhou, A.; Tucker, G.; and Levine, S. 2020.
D.; Zaharia, M.; and Khattab, O. 2026. GEPA: Reflective             Conservative Q-Learning for Offline Reinforcement Learn-
Prompt Evolution Can Outperform Reinforcement Learning.             ing. In Advances in Neural Information Processing Systems
In International Conference on Learning Representations             (NeurIPS).
(ICLR).                                                             Levine, S.; Kumar, A.; Tucker, G.; and Fu, J. 2020. Offline
Anthropic. 2025. Claude Code: An Agentic Coding Tool.               Reinforcement Learning: Tutorial, Review, and Perspectives
https://claude.com/product/claude-code.                             on Open Problems. arXiv preprint arXiv:2005.01643.
Barres, V.; Dong, H.; Ray, S.; Si, X.; and Narasimhan, K.           Liu, N. F.; Lin, K.; Hewitt, J.; Paranjape, A.; Bevilacqua, M.;
2026. τ 2 -Bench: Evaluating Conversational Agents in a             Petroni, F.; and Liang, P. 2024. Lost in the Middle: How
Dual-Control Environment. In International Conference on            Language Models Use Long Contexts. Transactions of the
Machine Learning (ICML).                                            Association for Computational Linguistics, 12: 157–173.
Brandfonbrener, D.; Whitney, W. F.; Ranganath, R.; and              Ma, Z.; Zhang, B.; Zhang, J.; Yu, J.; Zhang, X.; Zhang,
Bruna, J. 2021. Offline RL Without Off-Policy Evalua-               X.; Luo, S.; Wang, X.; and Tang, J. 2024. Spreadsheet-
tion. In Advances in Neural Information Processing Systems          Bench: Towards Challenging Real World Spreadsheet Ma-
(NeurIPS).                                                          nipulation. In Advances in Neural Information Processing
Chen, W.; Ma, X.; Wang, X.; and Cohen, W. W. 2023. Pro-             Systems (NeurIPS) Datasets and Benchmarks Track.
gram of Thoughts Prompting: Disentangling Computation               Madaan, A.; Tandon, N.; Gupta, P.; Hallinan, S.; Gao, L.;
from Reasoning for Numerical Reasoning Tasks. Transac-              Wiegreffe, S.; Alon, U.; Dziri, N.; Prabhumoye, S.; Yang,
tions on Machine Learning Research.                                 Y.; Gupta, S.; Majumder, B. P.; Hermann, K.; Welleck, S.;
Cheng, C.-A.; Nie, A.; and Swaminathan, A. 2024. Trace              Yazdanbakhsh, A.; and Clark, P. 2023. Self-Refine: Itera-
is the Next AutoDiff: Generative Optimization with Rich             tive Refinement with Self-Feedback. In Advances in Neural
Feedback, Execution Traces, and LLMs. In Advances in                Information Processing Systems (NeurIPS).
Neural Information Processing Systems (NeurIPS).                    Miller, E. 2024. Adding Error Bars to Evals: A Statistical
DeepSeek-AI. 2025. DeepSeek-R1: Incentivizing Reason-               Approach to Language Model Evaluations. arXiv preprint
ing Capability in LLMs via Reinforcement Learning. arXiv            arXiv:2411.00640.
preprint arXiv:2501.12948.                                          Opsahl-Ong, K.; Ryan, M. J.; Purtell, J.; Broman, D.; Potts,
Dwork, C.; Feldman, V.; Hardt, M.; Pitassi, T.; Reingold,           C.; Zaharia, M.; and Khattab, O. 2024. Optimizing Instruc-
O.; and Roth, A. 2015. The Reusable Holdout: Preserving             tions and Demonstrations for Multi-Stage Language Model
Validity in Adaptive Data Analysis. Science, 349(6248):             Programs. In Empirical Methods in Natural Language Pro-
636–638.                                                            cessing (EMNLP).
Fernando, C.; Banarse, D.; Michalewski, H.; Osindero, S.;           Ouyang, S.; Yan, J.; Hsu, I.-H.; Chen, Y.; Jiang, K.; Wang, Z.;
and Rocktäschel, T. 2023. Promptbreeder: Self-Referential           Han, R.; Le, L. T.; Daruki, S.; Tang, X.; Tirumalashetty, V.;
Self-Improvement via Prompt Evolution. arXiv preprint               Lee, G.; Rofouei, M.; Lin, H.; Han, J.; Lee, C.-Y.; and Pfister,
arXiv:2309.16797.                                                   T. 2025. ReasoningBank: Scaling Agent Self-Evolving with
Fujimoto, S.; Meger, D.; and Precup, D. 2019. Off-Policy            Reasoning Memory. arXiv preprint arXiv:2509.25140.
Deep Reinforcement Learning without Exploration. In In-             Park, J. S.; O’Brien, J. C.; Cai, C. J.; Morris, M. R.; Liang,
ternational Conference on Machine Learning (ICML).                  P.; and Bernstein, M. S. 2023. Generative Agents: Interactive
Gao, L.; Madaan, A.; Zhou, S.; Alon, U.; Liu, P.; Yang,             Simulacra of Human Behavior. In ACM Symposium on User
Y.; Callan, J.; and Neubig, G. 2023. PAL: Program-Aided             Interface Software and Technology (UIST).
Language Models. In International Conference on Machine             Pryzant, R.; Iter, D.; Li, J.; Lee, Y. T.; Zhu, C.; and Zeng,
Learning (ICML).                                                    M. 2023. Automatic Prompt Optimization with “Gradient
Guo, Q.; Wang, R.; Guo, J.; Li, B.; Song, K.; Tan, X.; Liu,         Descent” and Beam Search. In Empirical Methods in Natural
G.; Bian, J.; and Yang, Y. 2024. Connecting Large Lan-              Language Processing (EMNLP).
guage Models with Evolutionary Algorithms Yields Pow-               Shin, T.; Razeghi, Y.; Logan IV, R. L.; Wallace, E.; and Singh,
erful Prompt Optimizers. In International Conference on             S. 2020. AutoPrompt: Eliciting Knowledge from Language
Learning Representations (ICLR).                                    Models with Automatically Generated Prompts. In Empirical
Jimenez, C. E.; Yang, J.; Wettig, A.; Yao, S.; Pei, K.; Press,      Methods in Natural Language Processing (EMNLP).
O.; and Narasimhan, K. 2024. SWE-bench: Can Language                Shinn, N.; Cassano, F.; Gopinath, A.; Narasimhan, K.; and
Models Resolve Real-World GitHub Issues? In International           Yao, S. 2023. Reflexion: Language Agents with Verbal Re-
Conference on Learning Representations (ICLR).                      inforcement Learning. In Advances in Neural Information
Khattab, O.; Singhvi, A.; Maheshwari, P.; Zhang, Z.; San-           Processing Systems (NeurIPS).
thanam, K.; Vardhamanan, S.; Haq, S.; Sharma, A.; Joshi,            Shridhar, M.; Yuan, X.; Côté, M.-A.; Bisk, Y.; Trischler, A.;
T. T.; Moazam, H.; Miller, H.; Zaharia, M.; and Potts, C.           and Hausknecht, M. 2021. ALFWorld: Aligning Text and
Embodied Environments for Interactive Learning. In Inter-        and Olukotun, K. 2025. Agentic Context Engineering: Evolv-
national Conference on Learning Representations (ICLR).          ing Contexts for Self-Improving Language Models. arXiv
Smith, J. E.; and Winkler, R. L. 2006. The Optimizer’s Curse:    preprint arXiv:2510.04618.
Skepticism and Postdecision Surprise in Decision Analysis.       Zhao, A.; Huang, D.; Xu, Q.; Lin, M.; Liu, Y.-J.; and Huang,
Management Science, 52(3): 311–322.                              G. 2024. ExpeL: LLM Agents Are Experiential Learners. In
Snell, C.; Lee, J.; Xu, K.; and Kumar, A. 2025. Scaling LLM      AAAI Conference on Artificial Intelligence.
Test-Time Compute Optimally Can Be More Effective Than           Zhou, Y.; Muresanu, A. I.; Han, Z.; Paster, K.; Pitis, S.; Chan,
Scaling Model Parameters. In International Conference on         H.; and Ba, J. 2023. Large Language Models Are Human-
Learning Representations (ICLR).                                 Level Prompt Engineers. In International Conference on
Suzgun, M.; Yuksekgonul, M.; Bianchi, F.; Jurafsky, D.; and      Learning Representations (ICLR).
Zou, J. 2026. Dynamic Cheatsheet: Test-Time Learning with
Adaptive Memory. In European Chapter of the Association
for Computational Linguistics (EACL).
Wang, G.; Xie, Y.; Jiang, Y.; Mandlekar, A.; Xiao, C.; Zhu,
Y.; Fan, L.; and Anandkumar, A. 2024a. Voyager: An
Open-Ended Embodied Agent with Large Language Mod-
els. Transactions on Machine Learning Research.
Wang, X.; Li, B.; Song, Y.; Xu, F. F.; Tang, X.; Zhuge, M.;
Pan, J.; Song, Y.; Li, B.; Singh, J.; et al. 2025a. OpenHands:
An Open Platform for AI Software Developers as Generalist
Agents. In International Conference on Learning Represen-
tations (ICLR).
Wang, X.; Li, C.; Wang, Z.; Bai, F.; Luo, H.; Zhang, J.;
Jojic, N.; Xing, E. P.; and Hu, Z. 2024b. PromptAgent:
Strategic Planning with Language Models Enables Expert-
Level Prompt Optimization. In International Conference on
Learning Representations (ICLR).
Wang, Z. Z.; Mao, J.; Fried, D.; and Neubig, G. 2025b. Agent
Workflow Memory. In International Conference on Machine
Learning (ICML).
Wei, J.; Wang, X.; Schuurmans, D.; Bosma, M.; Ichter, B.;
Xia, F.; Chi, E. H.; Le, Q. V.; and Zhou, D. 2022. Chain-
of-Thought Prompting Elicits Reasoning in Large Language
Models. In Advances in Neural Information Processing Sys-
tems (NeurIPS).
Yang, C.; Wang, X.; Lu, Y.; Liu, H.; Le, Q. V.; Zhou, D.;
and Chen, X. 2024a. Large Language Models as Optimizers.
In International Conference on Learning Representations
(ICLR).
Yang, J.; Jimenez, C. E.; Wettig, A.; Lieret, K.; Yao, S.;
Narasimhan, K.; and Press, O. 2024b. SWE-agent: Agent-
Computer Interfaces Enable Automated Software Engineer-
ing. In Advances in Neural Information Processing Systems
(NeurIPS).
Yao, S.; Shinn, N.; Razavi, P.; and Narasimhan, K. 2024.
τ -bench: A Benchmark for Tool-Agent-User Interaction in
Real-World Domains. arXiv preprint arXiv:2406.12045.
Yao, S.; Zhao, J.; Yu, D.; Du, N.; Shafran, I.; Narasimhan,
K.; and Cao, Y. 2023. ReAct: Synergizing Reasoning and
Acting in Language Models. In International Conference on
Learning Representations (ICLR).
Yuksekgonul, M.; Bianchi, F.; Boen, J.; Liu, S.; Huang, Z.;
Guestrin, C.; and Zou, J. 2024. TextGrad: Automatic “Dif-
ferentiation” via Text. arXiv preprint arXiv:2406.07496.
Zhang, Q.; Hu, C.; Upasani, S.; Ma, B.; Hong, F.; Kamanuru,
V.; Rainton, J.; Wu, C.; Ji, M.; Li, H.; Thakker, U.; Zou, J.;

