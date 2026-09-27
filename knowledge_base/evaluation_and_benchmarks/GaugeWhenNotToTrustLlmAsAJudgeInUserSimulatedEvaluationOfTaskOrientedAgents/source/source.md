> PDF original (not vendored: source.pdf is 3.4 MB > 2 MB): https://arxiv.org/pdf/2609.12191

# GAUGE: When Not to Trust LLM-as-a-Judge in User-Simulated Evaluation of Task-Oriented Agents
Source: https://arxiv.org/pdf/2609.12191
Kind: pdf
Fetched: 2026-09-15T07:26:08.104958+00:00
Tool: pdftotext

                                                GAUGE: When Not to Trust LLM-as-a-Judge in User-Simulated
                                                          Evaluation of Task-Oriented Agents

                                                                       Umesh Bodhwani, Thanh Tran, Kai Wei
                                                                                   Amazon
                                                                     {bodhwani, tdt, kaiwe}@amazon.com



                                                               Abstract                                                            SimArena/
                                                                                                                                   LostInSim
                                                                                                                                   ECom-
                                                                                                                                   Bench
                                                                                                                                   Judge-
                                             Comparing and selecting task-oriented LLM                                             eval




arXiv:2609.12191v1 [cs.CL] 10 Sep 2026
                                                                                                                                   Chat-
                                                                                                                                   Bench
                                             agents increasingly relies on a low-cost of-                                          GAUGE
                                             fline evaluation gate: persona-driven LLM user-      Ranking validity vs. reward      ∼   ∼    ✗     ∼   ✓
                                             simulators converse with each candidate, an          Release-decision unit            ∼   ✓    ✗     ∼   ✓
                                             LLM-as-a-judge scores the transcripts, and the       Satisfaction ̸= task success     ✗   ✗    ✗     ∼   ✓
                                             higher-scoring agent is promoted. We intro-          Cross-provider scale             ∼   ✗    ∼     ✗   ✓
                                             duce GAUGE, a reusable offline protocol that         Grounded in real human ratings   ✓   ✗    ✓     ✓   ✓
                                             measures whether this gate’s ranking matches         Judge-free cost decomposition    ✗   ✗    ✗     ✗   ✓
                                             a grounded verifiable reward across 25 agents
                                             from six providers on the τ 2 -bench and Simu-       Table 1: Positioning against prior evaluation work. Only
                                             latorArena benchmarks, separating two kinds          GAUGE tests whether the simulator+judge gate ranks
                                             of evaluation validity that release practices con-   agents like a verifiable non-LLM reward and quantifies
                                             flate: ranking validity and construct validity.      the satisfaction–success gap. ✓ fully addresses the cri-
                                             First, a satisfaction–success gap: satisfaction      terion; ∼ partial; ✗ not.
                                             carries essentially no information about task
                                             success, as conversations rated satisfied by our
                                             blind panel are decorrelated from actual suc-        LLM user-simulators, score the transcripts with
                                             cess, with 57.5% of them failing the customer’s      an LLM-judge, and promote the higher-scoring
                                             task, a pattern consistent across five rater pop-
                                                                                                  variant. It runs in continuous integration (CI) at a
                                             ulations, both benchmarks, and every subjec-
                                             tive dimension we rated. Second, while the           few cents per transcript with no labeled production
                                             gate’s ranking is robust across the broad capa-      data, resting on one assumption teams almost never
                                             bility span, it loses resolution among the near-     measure: that this composite simulator-plus-judge
                                             equal strong agents: this decision-disagreement      gate ranks variants the way a grounded evaluation
                                             rate jumps from <1% on wide-reward pairs to          would. We audit this gate as deployed and pair
                                             31% on close pairs. The gate is thus human-          the audit with a drop-in zero-cost mitigation. That
                                             validated yet mis-anchored. As a remedy, we          LLM judges exhibit systematic biases, including
                                             propose a calibrate-then-trust cadence in which
                                                                                                  self-preference and position bias, is known (Pan-
                                             a judge-free completion bit is a zero-cost trip-
                                             wire for truncation regressions.                     ickssery et al., 2024; Wang et al., 2024); what has
                                                                                                  not been quantified is their magnitude at the release-
                                                                                                  decision unit against a verifiable reward: a 57.5%
                                         1   Introduction                                         false-accept rate on the blind human panel, a gap
                                         Developers and researchers building agentic, task-       that persists across five rater populations and alters
                                         oriented LLM agents for customer service, tool-use       the resulting agent-selection decisions.
                                         assistants, and tutoring must decide which vari-            We introduce GAUGE (Grounded Audit of User-
                                         ant is better, under three constraints: there is no      simulator-and-judge Gate Evaluation), a reusable,
                                         clean held-out test set that captures live user ex-      fully offline protocol that separates two kinds of va-
                                         perience, a controlled human study per candidate         lidity that release practice conflates (Table 1). The
                                         config is prohibitively slow, and the config space       gate has ranking validity (it orders agents like the
                                         (model, prompt, policy, tools) changes often. The        verifiable reward) and is certified for construct va-
                                         field’s de facto answer is a low-cost offline gate:      lidity against human satisfaction; yet satisfaction is
                                         drive each candidate against persona-conditioned         not success (the satisfaction–success gap): 57.5%
of conversations our blind human panel rated sat-         (ρ=0.94) yet loses resolution among near-equal
isfied (≥5/7) had failed the customer’s task, a gap       agents, where the gate promotes the lower-reward
that misleads the LLM-judge and the humans. A             agent on 31% of close pairs, and we isolate same-
gate can be human-validated yet mis-anchored.             family judge self-preference (+0.75/7; §4.2, §4.3).
    The satisfaction anchor remains misleading as a
                                                             (4) Calibrate-then-trust recipe. We show that a
release signal despite ranking validity, for three rea-
                                                          judge-free completion bit is a zero-cost tripwire for
sons. First, the ranking holds only where capability
                                                          truncation regressions (ρ=0.87 vs. 0.80 on broken-
dominates: among the near-equal strong agents
                                                          vs-working; §4.5), and report a negative result: out-
real release decisions compare, the gate promotes
                                                          of-sample recalibration does not transfer (§4.6).
the lower-reward agent on 31% of close pairs (the
decision-disagreement rate; §4.2), up from <1%            Key Findings.
where rewards are far apart. Second, teams opti-              • Subjective approval is decorrelated from task success
mize against gates rather than only reading them,               across all dimensions, so an evaluation gate can be
and tuning to a satisfaction anchor raises a met-               human-validated yet mis-anchored to the outcome.
ric known to diverge from the objective once opti-            • High aggregate ranking validity coexists with unreli-
                                                                able resolution of near-equal candidates, precisely the
mized (Strathern, 1997; Skalse et al., 2022). Third,            comparisons release decisions depend on.
an accept/reject threshold anchored on satisfaction
                                                              • Evaluator reliability is determined by evidence access,
admits agents that fail 48–60% of the time (§4.1).              not model capability: outcome-grounded judging suc-
The anchor thus governs exactly the decisions a                 ceeds where transcript-only satisfaction fails.
gate exists to make: promoting near-equal candi-              • The gate is valid only within a bounded operating
dates, serving as an optimization target, and setting           region, requiring re-auditing on configuration change
                                                                rather than on a fixed schedule.
the absolute accept/reject bar. The user-simulator
is a component of the gate we audit: every central        2   Related Work
claim is anchored on the simulator-independent
verifiable reward and human panel.                        User-simulator reliability. Simulated users have
    GAUGE operates as a periodic calibration              long evaluated dialogue agents, from satisfaction-
(a calibrate-then-trust cadence) rather than a            driven simulation (Sun et al., 2021) to LLM-based
per-decision gate: the verifiable audit is run once       simulators (Davidson et al., 2023; Sekulic et al.,
on a representative benchmark to learn the gate’s         2024) and “agents evaluating agents” (Zhuge et al.,
trusted operating region, after which the cheap gate      2025). SimulatorArena (Dou et al., 2025) and Lost-
is used in CI within that region. It applies wherever     in-Simulation (Seshadri et al., 2026) test LLM user-
an offline verifiable reward is obtainable, here the      simulators as human proxies via absolute rating
τ 2 -bench oracle: DB-state and action checks, and        correlation or single-agent reliability. Delta: we
SimulatorArena’s human-graded correctness. Our            audit the composite gate’s agent-ranking validity at
contributions are as follows.                             the release-decision unit against a non-LLM veri-
                                                          fiable reward, and show its optimized satisfaction
   (1) GAUGE, a reusable protocol for validating          signal is decorrelated from task success.
simulator-plus-judge evaluation. We introduce
                                                          Agent and customer-agent benchmarks. Tool-
the first protocol to validate a simulator-plus-judge
                                                          using agents are evaluated by recent benchmarks
evaluation gate against a verifiable, non-LLM re-
                                                          (Zhou et al., 2024; Qin et al., 2024; Liu et al.,
ward at the release-decision unit, applied at scale:
                                                          2024); ECom-Bench (Wang et al., 2025) reports
25 agents, six providers, four judges, two sub-
                                                          persona-simulator pass-rates, while τ -bench (Yao
strates, ≈3,700 transcripts (§3).
                                                          et al., 2025) and its successor τ 2 -bench (Barres
   (2) Satisfaction–success gap. We show that sat-        et al., 2026) provide a verifiable substrate. Delta:
isfaction carries essentially no information about        we test whether such pass-rates rank agents like
task success: 57.5% of satisfied conversations            a grounded reward, and surface the satisfied-but-
failed the task (ρ= −0.147), a gap that holds across      failed inversion.
five rater populations and two substrates (§4.1).
                                                          LLM-as-a-judge calibration to humans. A
   (3) Separating ranking from construct valid-           large literature validates LLM-judges against hu-
ity. We separate ranking from construct validity          man preference and satisfaction (Zheng et al., 2023;
on the six-provider ladder: the ranking is robust         Liu et al., 2023; Gu et al., 2024), documents judge
Figure 1: GAUGE measures whether the LLM-as-a-Judge and user-simulator evaluation gate ranks agents the way
a grounded, verifiable reward would. Left to right: an agent and a persona simulator converse on a substrate,
and four evaluators score each transcript: three subjective satisfaction signals (the LLM-as-a-Judge gate, an LLM
human-proxy, and a blind 3-person human panel) and one objective non-LLM reward. Aggregating over all 25
agents, the gate’s agent ranking matches the reward’s (ρ=0.94), yet satisfaction is decorrelated from success.


biases (position (Wang et al., 2024), self-preference     3   Method
(Panickssery et al., 2024), inconsistency (Stureborg
et al., 2024)) and benchmarks LLM judges and              Figure 1 shows the audit end to end: an agent and
reward models (Tan et al., 2025; Lambert et al.,          a persona simulator converse on a substrate, and
2025). A complementary line calibrates model              four evaluators score each transcript, one of them a
confidence to signal when to trust an LLM output          verifiable, non-LLM reward.
versus defer to a human (Bodhwani et al., 2025a;
                                                          Problem formulation Let A be a set of can-
Jung et al., 2025). Delta: for customer agents this
                                                          didate agents, P persona strata, and D domains.
anchor is misaligned: human satisfaction is decorre-
                                                          For agent a, persona p, domain d, the simula-
lated from task success, so a judge can be “human-
                                                          tor and agent produce a transcript τa,p,d carry-
validated” yet mis-rank agents. Where recent
                                                          ing a per-transcript verifiable correctness label
work finds simulators over-cooperative or ranking-
                                                          r(τ ) ∈ {0, 1} from a non-LLM oracle. Three
divergent (Mind-the-Sim2Real (Zhou et al., 2026),
                                                          subjective signals also score the transcript on a
SimulatorArena (Dou et al., 2025)), we show the
                                                          satisfaction scale: an LLM-judge gate, an LLM
decorrelation misleads humans too.
                                                          human-proxy, and a human panel; write any such
                                                          signal as s(τ ). At the release-decision unit (the
                                                          agent a; we aggregate over p, d, since per-cell
Measurement validity and proxy gaming. Our                scores are too noisy to act on) we define the
framing draws on construct validity (Cronbach and         agent-level gate G(a) = Ep,d [gate(τ )] and ver-
Meehl, 1955) and its ML translation (Jacobs and           ifiable reward R(a) = Ep,d [r(τ )] ∈ [0, 1], and
Wallach, 2021; Bowman and Dahl, 2021): a metric           likewise Sproxy (a), Shum (a). GAUGE measures
can order systems well yet miss the construct it          two quantities. Ranking validity ρ(G, R) over
certifies, and an optimized proxy diverges from the       A measures whether the gate orders agents like
objective (Goodhart’s law (Strathern, 1997), reward       the verifiable reward. The construct gap (equiva-
hacking (Amodei et al., 2016; Skalse et al., 2022)).      lently, the satisfaction–success gap) is the rate at
Delta: we give a measured instance for release            which the task failed (r(τ )=0) among transcripts
gates, adapting controlled-perturbation instrument        a signal rated satisfied (a high s(τ ): ≥5 on a 7-
validation (Ribeiro et al., 2020; Adebayo et al.,         point or ≥8 on a 10-point scale). Crucially, a
2018) into our flag-only degradation set (§4.5, Ap-       gate can be human-validated (ρ(Shum , G) high, the
pendix C). Unlike ChatBench (Chang et al., 2025),         judge tracks human satisfaction) yet mis-anchored
which closes the offline-vs-interactive gap by fine-      (ρ(Shum , R) low), because satisfaction itself does
tuning, GAUGE is fine-tuning-free.                        not track success.
Figure 2: Satisfaction versus verifiable task success across raters. (a) Share of each rater’s satisfied conversations
that nonetheless failed the task, on the τ 2 human panel and the independent SimulatorArena substrate. (b) Empirical
P (success) by satisfaction rating (integer bins, n≥5; human ±1 SE shaded): success does not rise with satisfaction
for any rater.


Substrates and ground truth. Our primary                     (prompts in Appendix L). The gate is policy-aware:
benchmark (substrate) is τ 2 -bench (Barres et al.,          an operations-supervisor rubric that reads the full
2026) retail and airline, whose verifiable reward is         transcript (tool calls and goal included) and scores
a non-LLM oracle, fully deterministic on airline             service quality with policy adherence and task res-
(DB-state and communicate checks) and predomi-               olution first. The proxy is satisfaction-only: a
nantly deterministic on retail (a deterministic DB           process-blind first-person shopper (tool calls and
check gates an LLM-scored natural-language as-               task stripped) rating how the conversation felt,
sertion; Appendix K); for replication we add Sim-            standing in for the human rater gates are usually
ulatorArena (Dou et al., 2025) math tutoring with            validated against. Disjoint in role, evidence, and
human satisfaction ratings and human-graded cor-             vocabulary, the two cannot agree by a shared-rubric
rectness. Per-substrate statistics in Appendix J.            artifact. Four judges apply the gate rubric to the
                                                             full grid (Claude Sonnet-4.5 and Opus-4.8, GPT-
Agents. We evaluate two complementary sets.                  5.4 and GPT-5.5), with Opus-4.8 the primary judge
The cross-provider ladder (§4.2, §4.3) spans 14              (Anthropic, 2026b) and GPT-5.5 its out-of-family
models from six providers (Anthropic, Meta, Mis-             counterpart; results are consistent across all four
tral, Qwen, DeepSeek, OpenAI) at two tempera-                (§4.3). A blind 3-person panel grounds the scores
tures on the full task pools of 114 retail and 50 air-       on a stratified 150-transcript τ 2 sample.
line tasks, yielding 25 scored model-temperature
configurations and about 3,700 transcripts in to-           Metrics. We report agent-level Spearman corre-
tal (Appendix J). This wide capability span makes           lation with model-clustered bootstrap CIs (Efron,
ranking validity, and its near-equal limit, measur-         1979); broken-vs-working AUC; a power analy-
able. The controlled-degradation set (§4.5, Ap-             sis (min-detectable ρ); out-of-sample recalibration
pendix C) is a positive control: 12 Sonnet-4.5 con-         (leave-one-stratum/agent-out); and panel reliability
figurations of a-priori-known good, medium, or de-          as Krippendorff’s α (Krippendorff, 1980) against a
graded quality, crossed with 6 strata and 2 domains         human–human ceiling (Artstein and Poesio, 2008).
to give 144 cells and 720 transcripts, degraded only
through inference-time hyperparameters such as               4     Results
temperature, token or step limits, and error toler-          4.1    Satisfaction does not imply task success
ance, with no prompt or code edits. It supplies the
broken-vs-working axis the all-strong grid cannot,          On a stratified 150-transcript τ 2 sample rated by
so a signal that fails to rank the degraded configs         three blind, independent annotators (a fully-crossed
last exhibits a measurable validity failure (Ribeiro        150×3 design; Krippendorff’s α=0.79, human–
et al., 2020; Adebayo et al., 2018).                        human ceiling ρ=0.85), two independently-built
                                                            LLM judges reproduce human satisfaction (Opus-
Judges and humans. We score each transcript                 4.8 ρ=0.846, GPT-5.5 ρ=0.827). Yet satisfaction
with two deliberately disjoint satisfaction rubrics         carries essentially no information about task suc-
                               P(fail | base
  Signal                       satisf.) rate   RR AUC
  Human satisfaction (panel)     57.5 57.3 1.00       0.44
  Satisfaction proxy (grid)      32.7 40.2 0.81       0.49
  Policy-aware gate (grid)       20.0 40.2 0.50       0.73

Table 2: Satisfaction matches the base failure rate; only
the policy-aware gate improves on it. For each signal:
the failure rate among the conversations it rated satisfied,
the pool’s own base failure rate, their ratio (relative risk,
RR), and transcript-level discrimination (AUC). The
human panel is a stratified sample (base 57.3%); the            Figure 3: Construct-gap positive control: an agent
grid signals use the natural task mix (base 40.2%).             degraded by configuration flags across three known-
                                                                quality tiers, all signals on a common [0, 1] scale. As
                                                                quality drops good→degraded, verifiable reward col-
cess: across all 150 transcripts the correlation is flat        lapses (0.66 → 0.05) while the satisfaction signals stay
and non-positive (ρ= −0.147; dose-response curve                nearly flat and the policy-aware gate is only partly sen-
                                                                sitive (0.54 → 0.21); the right panel quantifies each
flat, Fig. 2b). Crucially, this is not an artifact of
                                                                signal’s overstatement at the degraded tier.
the word “satisfaction”: all five subjective dimen-
sions the panel rated (satisfaction, respect, clarity,
perceived helpfulness, and would-return) are like-
                                                                faction thresholds. It also holds within each do-
wise decorrelated from success (|ρ| ≤ 0.17; Ap-
                                                                main: satisfied-but-failed is 24.1% (retail), 62.1%
pendix B), so the gap reflects subjective approval
                                                                (airline), and 38.7% (math tutoring), and the rank-
in general. Concretely, 57.5% of the conversations
                                                                ing replicates per domain (ρ=0.95 retail, 0.80 air-
the panel rated satisfied (≥5/7) had failed the task.
                                                                line; Appendices F, H). The process-blind proxy
                                                                overstates success more than the policy-aware gate,
Uninformative, not merely weak. Interpreted
                                                                which observes whether the task resolved.
against the base rate, this pattern is the central find-
ing (Table 2). The 57.5% satisfied-but-failed rate
is statistically indistinguishable from the stratified          Not a simulator or reward-term artifact. The
sample’s own 57.3% base failure rate: conditioning              inversion surfaces only where satisfaction is the
on satisfied does not lower failure, so satisfaction            operative signal: where verifiable reward already
is uninformative rather than merely weak, and at                separates agents cleanly, as on the strong-agent six-
the transcript level it does not discriminate success           provider grid, the gate-accept inversion rate falls
(AUC 0.44). By contrast, the policy-aware gate as-              to 20%, the false-accept ceiling a construct-valid
sesses whether the task resolved: it roughly halves             gate should meet (292/1,460, p = 0.51). As quali-
failure risk (20.0% of gate-accepted conversations              tative cross-substrate corroboration, it replicates on
fail against a 40.2% base rate on the natural task              an independent, human-grounded substrate, Sim-
mix) and discriminates success (AUC 0.73; per-                  ulatorArena math tutoring, where 38.7% of con-
score calibration in Appendix C.1). The process-                versations rated ≥8/10 by humans were verifiably
blind proxy, which never sees the tool calls or task,           incorrect (p = 0.013; Fig. 2a, right). Swapping
behaves like satisfaction, not the gate (32.7% vs.              our Sonnet-4.5 user-simulator with an independent
40.2%; AUC 0.49). Separating these two signals,                 simulator: GPT-5.4, with agent, tasks, rubrics, and
one uninformative and one informative, is the core              oracle fixed, leaves the inversion intact (66.7% gate-
contribution of this work. The panel result is ro-              satisfied and 69.8% proxy-satisfied still failing; Ap-
bust to dropping any single annotator (56.4–60.5%               pendix D). On airline, whose reward is fully de-
leave-one-annotator-out; Appendix A).                           terministic, the proxy still false-accepts 62.1% of
                                                                satisfied conversations (325/523). A degradation
Robust across raters and domains. The                           positive control demonstrates this directly (Fig. 3):
satisfied-but-failed rate is robust across sample               as one agent is degraded across known-quality tiers,
scale, raters, and providers: it is concordant across           reward collapses while satisfaction stays flat; the
five rater populations (the human panel plus gate               starkest case is a transcript truncated mid-task, scor-
and proxy scorings from two LLM providers; 47.6–                ing reward 0.0 yet earning the highest human rating
59.5%; Fig. 2a, Table 4) and stable across satis-               of any degraded variant (4.6/7; Appendices C, M).
                                                           the strictly lower-reward agent of a near-equal
                                                           pair. The primary Opus-4.8 gate does so on 31%
                                                           of them versus <1% on wide pairs, and the four
                                                           other signals behave alike (GPT-5.4 30%, GPT-5.5
                                                           39%, human-proxy 30%, pooled gate 38%; Ap-
                                                           pendix F), over thirty times the 0.9% wide-pair
                                                           rate. This separation is robust to resampling: the
                                                           near-equal rate’s base-model cluster-bootstrap 95%
                                                           CI is [11.6, 50.0]%, whose lower bound alone is
                                                           ∼12× the wide-pair rate. This is a resolution
                                                           limit at deployment-relevant separations, not a non-
                                                           significant correlation. GAUGE thus certifies the
                                                           gate as a regression and coarse-quality detector and
                                                           flags where it cannot adjudicate, a safety-relevant
                                                           gap current gate-based evaluation overlooks.

                                                           4.3   Judge robustness and self-preference
                                                           Because the Anthropic judge and the agents share
Figure 4: Per-agent verifiable reward, LLM-proxy sat-      a provider, “validity” could reflect self-recognition
isfaction, and the two frontier-judge gates (Opus-4.8,     (Panickssery et al., 2024), so we re-score the
GPT-5.5) for all 25 agents. The bar is the satisfaction    grid with an out-of-family judge. Opus-4.8 and
surplus (satisfaction−reward). Both gate ticks track re-   GPT-5.5 agree at ρ=0.92, all four judges recover
ward rather than satisfaction, and every agent is rated    the verifiable-reward ordering (ρ=0.84–0.94) and
more satisfying than it succeeds.
                                                           agree with one another (ρ=0.90–0.98), and the or-
                                                           dering is thus not a single-provider artifact, though
4.2   Ranking is robust across providers                   GPT-5.5 grades ≈0.8/7 lower.
                                                              The ordering is also not a capability artifact. Run
The construct gap might suggest the gate is invalid,       as agents on the same τ 2 pool, both frontier judges
yet its ranking is sound. Across the 25-agent, six-        are statistical peers of the strongest agent (Opus-4.8
provider ladder (Fig. 4; per-agent values in Ap-           0.82, GPT-5.5 0.84, vs. pool-best Opus-4.6 (t.7) at
pendix E), the Opus-4.8 gate recovers the verifiable-      0.87; overlapping 95% CIs); they recover the order-
reward ordering at ρ=0.94, far above the minimum           ing without outclassing it, while the weakest judge-
correlation resolvable with N =25 agents (ρ=0.54           as-agent (GPT-5.4, 0.77) is tied-best as a ranker
at p<0.05); the ranking holds across both domains          (ρ=0.94). The near-equal limit holds for every
and all four judges and cleanly separates broken           judge (top-11 ρ=0.25–0.51, all n.s.; Appendix F.1),
from working agents on the controlled-degradation          confirming genuine agent near-equality rather than
set (AUC=1.00; per-judge and per-domain coeffi-            mis-ranking by a weak judge.
cients in Appendix F). The ordering persists un-              The two-provider design also isolates same-
der an independent-provider user-simulator: re-            family self-preference: the Opus-4.8 judge inflates
running the full 25-agent grid with GPT-5.4 (agent         Claude agents over GPT-5.5 more than non-Claude
and oracle fixed) preserves it at ρ=0.93, against          agents, a scale-invariant diff-in-diff of +0.75/7
0.94 under Sonnet-4.5, so the ranking reflects agent       (Sonnet-4.5 shows +0.67/7 against GPT-5.4; Ap-
quality rather than same-family simulator–agent            pendix F.2), so it reflects self-preference and leaves
affinity (Appendix D).                                     the ranking intact. Two reruns confirm the ranking
   This validity is driven by breadth: it lapses           is stable against judge noise (test–retest ICC=0.87,
among the near-equal strong agents that real re-           rank stability ρ=0.92; Appendix F.3).
lease decisions compare. Such pairs are common
(30% of all pairs and 55% of top-half pairs differ         4.4   Personas stress-test agents
in verifiable reward by less than 0.1, our near-equal      The simulator drives each agent against six per-
threshold, near the oracle’s resolution given per-         sona strata spanning cooperativeness, patience, and
agent sampling noise), so we report the decision-          assertiveness (axes informed by the OPeRA per-
disagreement rate: how often the gate promotes             sona schema (Wang et al., 2026); overlays in Ap-
  Signal                $/dec.        ρ        Use / cadence                   fix. Both natural repair routes fail out-of-sample:
  Completion bit            0         0.87     regressions; every CI run       a human-anchored persona-reweighting lifts in-
  Agent cost / length       0      0.17–0.34   –
                                                                               sample validity from ρ=0.71 to 0.80, but the per-
  LLM-judge gate         +0.60        0.80     coarse rank; bit insufficient
  LLM-proxy sat.         +0.60        0.35     tone only, not success          persona bias term does not hold under leave-one-
  Verifiable audit      rollouts        –      calibration; periodic           stratum-out (dropping to ρ=0.68); combining all
                                                                               four judges gives no lift over the single best and is
Table 3: Release signals by marginal $/decision, Spear-
                                                                               worse under leave-one-agent-out. Both gains are
man ρ vs. the verifiable reward (controlled-degradation
set, N =12 variants), and recommended use/cadence.                             in-sample artifacts (Appendix F.3): the dependable
The zero-cost completion bit catches severe regressions                        path is to learn the gate’s trusted operating region
as well as the paid judge (ρ 0.87 vs. 0.80); agent-cost                        and operate within it (§4.5), rather than attempting
and proxy ρ (0.17–0.35) are not significant.                                   to repair it. Cheap substitutes for the audit fare
                                                                               no better on the near-equal regime: across 21 can-
                                                                               didate signals the four-judge average reproduces
pendix I). A single cooperative user masks failures:
                                                                               the best single judge’s 31% error exactly (27/87),
relative to the default τ 2 baseline (12 variants, re-
                                                                               a common-mode failure (the judges correlate 0.67-
tail; Fig. 10a), the persona population cuts mean
                                                                               0.98 and flip the same pairs; Appendix G); only
verifiable reward by 42% (0.47 → 0.27).
                                                                               calibrated abstention, declining pairs whose gate
   The personas also expose the construct gap                                  gap is within its sampling noise, reduces it, halving
(Fig. 10b): satisfaction swings widely by stratum                              error on the pairs it ranks (14.8%).
(proxy 3.5–5.4/7) yet does not track success (the
anxious/low-trust and skeptical strata tie on re-                              5   Discussion and Guidance
ward, 0.38, but differ by 1.2/7), so a satisfaction-
optimized signal tracks who the user is rather than                            A gate can be human-validated yet still mis-rank on
whether the task succeeded. The benchmark stays                                success: ranking and construct validity are separate
stable: every degraded variant floors at reward                                properties, and certifying one against human satis-
0 and all working variants stay above (whole-set                               faction does not guarantee the other. Framed posi-
reward-rank ρ=0.83), so the ranking validity (§4.2)                            tively, satisfaction and task completion are comple-
reflects agent quality, not the simulator.                                     mentary axes (satisfaction validly captures experi-
                                                                               ence), so a release gate should certify both rather
4.5    A free signal catches severe regressions                                than treat one as a proxy for the other. The cost-
A judge-free completion bit (conversation com-                                 reducing remedy is a cadence (Table 3): run a cheap
pleted), parsed at zero cost from existing rollouts, is                        signal on every config change and the expensive
a targeted tripwire. On the controlled-degradation                             verifiable audit on a trigger rather than a fixed cal-
set (broken-vs-working) it scores ρ=0.87 against                               endar (a change of judge or simulator, a shift in the
the verifiable reward versus 0.80 for the full gate                            candidate pool, or a near-equal candidate set), to
(Table 3), because those failures are truncation-                              calibrate the cheap signal rather than replace it.
style. But truncation is the minority failure mode:                               Three guidelines follow. Never gate on satisfac-
of 1,485 grid failures, 96.5% terminate normally                               tion alone, especially when optimizing: once the
(semantic failures) and only 3.5% truncate, so the                             gate is an optimization target (prompt/policy/model
bit’s recall is 1.0 on truncation but 0.035 overall,                           search), tuning to a gate raises a score decorrelated
and on the six-provider grid it collapses to ρ=0.51                            from success, so pair any satisfaction signal with a
versus the gate’s 0.94. Semantic failures need                                 verifiable check. Aggregate to the variant, never
the paid judge, which does carry signal (ρ=0.37,                               a single (variant×persona) cell. When judge and
AUC 0.72). This division of labor is the calibrate-                            candidate share a provider, calibrate thresholds
then-trust recipe: screen routine changes with the                             against an out-of-family judge: the +0.75/7 self-
free bit for truncation regressions, and reserve the                           inflation (§4.3) can flip an accept/reject bar even
$0.60/decision judge for the semantic failures and                             with the ranking intact.
near-equal ranking (§4.2) it alone resolves.
                                                                               Limitations
4.6    Negative results and additional analyses                                Human panel size. The panel comprises 3 anno-
Recalibration does not transfer, which is why                                  tators rating 150 transcripts in a fully-crossed de-
we recommend calibrate-then-trust over a gate                                  sign (Krippendorff’s α=0.79, human–human ceil-
ing ρ=0.85). While sufficient for the headline           Anthropic. 2026a.    Claude Opus 4.6 system
satisfaction–success decorrelation (ρ= −0.147,             card.        https://www.anthropic.com/
                                                           claude-opus-4-6-system-card. Official
replicated on SimulatorArena at 38.7%), a larger
                                                           system card.
panel would tighten per-dimension confidence in-
tervals. The headline is robust to any single rater:     Anthropic. 2026b.    Claude Opus 4.8 system
leave-one-annotator-out keeps it within the 56.4–          card.        https://www.anthropic.com/
                                                           claude-opus-4-8-system-card. Official
60.5% band around 57.5% (Appendix A).                      system card.
Degradation        coverage. The       controlled-       Anthropic. 2026c.    Claude Sonnet 4.6 system
degradation set uses budget-style perturbations            card.        https://www.anthropic.com/
(output-token caps, step caps, error-abort; Ap-            claude-sonnet-4-6-system-card. Offi-
                                                           cial system card.
pendix C), so its broken-vs-working result detects
truncated agents rather than every failure mode.         Ron Artstein and Massimo Poesio. 2008. Survey article:
The full capability ladder provides complementary          Inter-coder agreement for computational linguistics.
                                                           Computational Linguistics, 34(4):555–596.
coverage of naturalistic failures.
                                                         Victor Barres, Honghua Dong, Soham Ray, Xujie Si,
Synthetic substrates. τ 2 -bench user instructions         and Karthik Narasimhan. 2026. τ 2 -bench: Evalu-
are synthetic, and our absolute pass-rates are not         ating conversational agents in a dual-control envi-
leaderboard-comparable because the harness runs            ronment. In Proceedings of the 43rd International
on Bedrock with a tolerant output parser (Ap-              Conference on Machine Learning.
pendix K). The parser is lossless by construction,       Umesh Bodhwani, Yuan Ling, Shujing Dong, Yarong
leaving the verifiable reward’s deterministic DB-         Feng, Hongfei Li, and Ayush Goyal. 2025a. A cali-
state and action checks unchanged, but generaliza-        brated reflection approach for enhancing confidence
                                                          estimation in LLMs. In Proceedings of the 5th Work-
tion to live customer interactions remains untested.      shop on Trustworthy NLP (TrustNLP 2025), pages
                                                          399–411, Albuquerque, New Mexico. Association
Ethics Statement                                          for Computational Linguistics.
Auditing customer-agent release gates supports           Umesh Bodhwani, Yuan Ling, Cibi Chakravarthy
safer deployment: satisfied-but-failed inversions         Senthilkumar, Shujing Dong, Yarong Feng, Hongfei
are silent failures that harm customers without sur-      Li, and Ayush Goyal. 2025b. LentEx: Generaliz-
                                                          able latent entity extraction via synthetic data and
facing in satisfaction-based monitoring. The hu-          instruction-tuned LLMs. In 2025 International Joint
man study rated only de-identified, synthetic-task        Conference on Neural Networks (IJCNN), pages 1–8.
transcripts (no personal data) and was therefore
                                                         Samuel R. Bowman and George Dahl. 2021. What will
IRB-exempt; the three consenting adult annota-             it take to fix benchmarking in natural language under-
tors (representative lay raters, independent of the        standing? In Proceedings of the 2021 Conference of
project team) were compensated above the local             the North American Chapter of the Association for
minimum wage and rated blind to the AI scores,             Computational Linguistics: Human Language Tech-
                                                           nologies, pages 4843–4855, Online. Association for
variant, and outcome.                                      Computational Linguistics.
                                                         Serina Chang, Ashton Anderson, and Jake M. Hof-
References                                                 man. 2025. ChatBench: From static benchmarks
                                                           to human-AI evaluation. In Proceedings of the 63rd
Julius Adebayo, Justin Gilmer, Michael Muelly, Ian         Annual Meeting of the Association for Computational
   Goodfellow, Moritz Hardt, and Been Kim. 2018. San-      Linguistics (Volume 1: Long Papers), pages 26009–
   ity checks for saliency maps. In Proceedings of the     26038. Association for Computational Linguistics.
  32nd International Conference on Neural Informa-
   tion Processing Systems, NIPS’18, page 9525–9536,     Lee Joseph Cronbach and Paul E. Meehl. 1955. Con-
   Red Hook, NY, USA. Curran Associates Inc.               struct validity in psychological tests. Psychological
                                                           bulletin, 52 4:281–302.
Dario Amodei, Chris Olah, Jacob Steinhardt, Paul
  Christiano, John Schulman, and Dan Mané. 2016.         Sam Davidson, Salvatore Romeo, Raphael Shu, James
  Concrete problems in AI safety.       Preprint,          Gung, Arshit Gupta, Saab Mansour, and Yi Zhang.
  arXiv:1606.06565.                                        2023. User simulation with large language mod-
                                                           els for evaluating task-oriented dialogue. Preprint,
Anthropic. 2025.     Claude Haiku 4.5 system               arXiv:2309.13233.
  card.        https://www.anthropic.com/
  claude-haiku-4-5-system-card. Official                 DeepSeek-AI. 2024. DeepSeek-V3 technical report.
  system card.                                             Preprint, arXiv:2412.19437.
DeepSeek-AI. 2025.    DeepSeek-V3.2 model                   Yang Liu, Dan Iter, Yichong Xu, Shuohang Wang,
  card.         https://huggingface.co/                       Ruochen Xu, and Chenguang Zhu. 2023. G-eval:
  deepseek-ai/DeepSeek-V3.2.       Official                   NLG evaluation using gpt-4 with better human align-
  model card.                                                 ment. In Proceedings of the 2023 Conference on
                                                              Empirical Methods in Natural Language Processing,
Yao Dou, Michel Galley, Baolin Peng, Chris Kedzie,            pages 2511–2522, Singapore. Association for Com-
  Weixin Cai, Alan Ritter, Chris Quirk, Wei Xu, and           putational Linguistics.
  Jianfeng Gao. 2025. SimulatorArena: Are user simu-
  lators reliable proxies for multi-turn evaluation of AI   Meta. 2024. Llama 3.3 70B Instruct model card.
  assistants? In Proceedings of the 2025 Conference on       https://huggingface.co/meta-llama/
  Empirical Methods in Natural Language Processing,          Llama-3.3-70B-Instruct. Official model
  pages 35212–35290. Association for Computational           card.
  Linguistics.
                                                            Mistral AI. 2025. Introducing Mistral 3. https:
Bradley Efron. 1979. Bootstrap methods: Another look         //mistral.ai/news/mistral-3/. Official
  at the jackknife. The Annals of Statistics, 7(1):1–26.      release announcement for Mistral Large 3 and the
  DOI:10.1214/aos/1176344552.                                 Ministral 3 family.
Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri,         OpenAI. 2026a.      Introducing GPT-5.4.
  Abhinav Pandey, Abhishek Kadian, Ahmad Al-                  https://openai.com/index/
  Dahle, Aiesha Letman, Akhil Mathur, Alan Schel-             introducing-gpt-5-4/.    Official release
  ten, Alex Vaughan, Amy Yang, Angela Fan, Anirudh            announcement.
  Goyal, Anthony Hartshorn, Aobo Yang, Archi Mi-
  tra, Archie Sravankumar, Artem Korenev, Arthur            OpenAI. 2026b.      Introducing GPT-5.5.
  Hinsvark, and 542 others. 2024. The Llama 3 herd            https://openai.com/index/
  of models. Preprint, arXiv:2407.21783.                      introducing-gpt-5-5/.    Official release
                                                              announcement.
Jiawei Gu, Xuhui Jiang, Zhichao Shi, Hexiang Tan,
   Xuehao Zhai, Chengjin Xu, Wei Li, Yinghan Shen,          Arjun Panickssery, Samuel R. Bowman, and Shi Feng.
   Shengjie Ma, Honghao Liu, Saizhuo Wang, Kun                2024. Llm evaluators recognize and favor their own
   Zhang, Yuanzhuo Wang, Wen Gao, Lionel Ni, and              generations. In Proceedings of the 38th International
   Jian Guo. 2024. A survey on LLM-as-a-Judge.                Conference on Neural Information Processing Sys-
   Preprint, arXiv:2411.15594.                                tems, NIPS ’24, Red Hook, NY, USA. Curran Asso-
Abigail Z. Jacobs and Hanna Wallach. 2021. Measure-           ciates Inc.
  ment and fairness. In Proceedings of the 2021 ACM         Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan
  Conference on Fairness, Accountability, and Trans-          Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang,
  parency (FAccT). DOI:10.1145/3442188.3445901.               Bill Qian, Sihan Zhao, Lauren Hong, Runchu Tian,
  arXiv:1912.05511.                                           Ruobing Xie, Jie Zhou, Mark Gerstein, dahai li,
Jaehun Jung, Faeze Brahman, and Yejin Choi. 2025.             Zhiyuan Liu, and Maosong Sun. 2024. ToolLLM:
  Trust or escalate: LLM judges with provable guaran-         Facilitating large language models to master 16000+
   tees for human agreement. In The Thirteenth Inter-         real-world APIs. In The Twelfth International Con-
   national Conference on Learning Representations.           ference on Learning Representations.

Klaus Krippendorff. 1980. Content Analysis: An Intro-       Marco Tulio Ribeiro, Tongshuang Wu, Carlos Guestrin,
  duction to Its Methodology. Sage.                          and Sameer Singh. 2020. Beyond accuracy: Be-
                                                             havioral testing of NLP models with CheckList. In
Nathan Lambert, Valentina Pyatkin, Jacob Morrison,           Proceedings of the 58th Annual Meeting of the Asso-
  LJ Miranda, Bill Yuchen Lin, Khyathi Chandu,               ciation for Computational Linguistics, pages 4902–
  Nouha Dziri, Sachin Kumar, Tom Zick, Yejin Choi,           4912. Association for Computational Linguistics.
  Noah A. Smith, and Hannaneh Hajishirzi. 2025. Re-
  wardBench: Evaluating reward models for language          Ivan Sekulic, Silvia Terragni, Victor Guimarães, Nghia
  modeling. In Findings of the Association for Compu-          Khau, Bruna Guedes, Modestas Filipavicius, An-
  tational Linguistics: NAACL 2025, pages 1755–1797,           dre Ferreira Manso, and Roland Mathis. 2024. Re-
  Albuquerque, New Mexico. Association for Compu-              liable LLM-based user simulator for task-oriented
  tational Linguistics.                                        dialogue systems. In Proceedings of the 1st Work-
                                                               shop on Simulating Conversational Intelligence in
Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu              Chat (SCI-CHAT 2024), pages 19–35, St. Julians,
  Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen                Malta. Association for Computational Linguistics.
  Men, Kejuan Yang, Shudan Zhang, Xiang Deng, Ao-
  han Zeng, Zhengxiao Du, Chenhui Zhang, Sheng              Preethi Seshadri, Samuel Cahyawijaya, Ayomide Odu-
  Shen, Tianjun Zhang, Yu Su, Huan Sun, and 3 others.         makinde, Sameer Singh, and Seraphina Goldfarb-
  2024. AgentBench: Evaluating LLMs as agents. In             Tarrant. 2026. Lost in simulation: LLM-simulated
  International Conference on Learning Representa-            users are unreliable proxies for human users in agen-
  tions (ICLR).                                               tic evaluations. In Proceedings of the 64th Annual
  Meeting of the Association for Computational Lin-        Ziyi Wang, Yuxuan Lu, Wenbo Li, Amirali Amini,
  guistics (Volume 1: Long Papers), pages 47423–             Bo Sun, Yakov Bart, Weimin Lyu, Jiri Gesi, Tian
  47439. Association for Computational Linguistics.          Wang, Jing Huang, Yu Su, Upol Ehsan, Malihe
                                                             Alikhani, Toby Jia-Jun Li, Lydia Chilton, and Dakuo
Patrick E. Shrout and Joseph L. Fleiss. 1979. In-            Wang. 2026. OPeRA: A dataset of observation, per-
  traclass correlations: Uses in assessing rater re-         sona, rationale, and action for evaluating LLMs on
  liability. Psychological Bulletin, 86(2):420–428.          human online shopping behavior simulation. In Pro-
  DOI:10.1037/0033-2909.86.2.420.                            ceedings of the 64th Annual Meeting of the Associa-
Joar Skalse, Nikolaus H. R. Howe, Dmitrii Krashenin-         tion for Computational Linguistics (Volume 1: Long
  nikov, and David Krueger. 2022. Defining and char-         Papers), pages 43942–43960. Association for Com-
  acterizing reward hacking. In Proceedings of the           putational Linguistics.
  36th International Conference on Neural Informa-         An Yang, Anfeng Li, Baosong Yang, Beichen Zhang,
  tion Processing Systems, NIPS ’22, Red Hook, NY,           Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao,
  USA. Curran Associates Inc.                                Chengen Huang, Chenxu Lv, Chujie Zheng, Day-
Marilyn Strathern. 1997. ‘improving ratings’: audit          iheng Liu, Fan Zhou, Fei Huang, Feng Hu, Hao
 in the british university system. European Review,          Ge, Haoran Wei, Huan Lin, Jialong Tang, and 41
 5:305 – 321.                                                others. 2025. Qwen3 technical report. Preprint,
                                                             arXiv:2505.09388.
Rickard Stureborg, Dimitris Alikaniotis, and Yoshi
  Suhara. 2024.     Large language models are              Shunyu Yao, Noah Shinn, Pedram Razavi, and
  inconsistent and biased evaluators.      Preprint,         Karthik R Narasimhan. 2025. {$\tau$}-bench: A
  arXiv:2405.01724.                                          benchmark for \underline{T}ool-\underline{A}gent-
                                                             \underline{U}ser interaction in real-world domains.
Weiwei Sun, Shuo Zhang, Krisztian Balog, Zhaochun            In The Thirteenth International Conference on Learn-
 Ren, Pengjie Ren, Zhumin Chen, and Maarten de Ri-           ing Representations.
 jke. 2021. Simulating user satisfaction for the evalu-
 ation of task-oriented dialogue systems. In Proceed-      Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan
 ings of the 44th International ACM SIGIR Confer-            Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin,
 ence on Research and Development in Information             Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang,
 Retrieval, SIGIR ’21, page 2499–2506, New York,             Joseph E. Gonzalez, and Ion Stoica. 2023. Judging
 NY, USA. Association for Computing Machinery.               llm-as-a-judge with mt-bench and chatbot arena. In
                                                             Proceedings of the 37th International Conference on
Sijun Tan, Siyuan Zhuang, Kyle Montgomery,                   Neural Information Processing Systems, NIPS ’23,
   William Yuan Tang, Alejandro Cuadron, Chen-               Red Hook, NY, USA. Curran Associates Inc.
   guang Wang, Raluca Popa, and Ion Stoica. 2025.
   Judgebench: A benchmark for evaluating LLM-based        Shuyan Zhou, Frank F. Xu, Hao Zhu, Xuhui Zhou,
   judges. In The Thirteenth International Conference        Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue
   on Learning Representations.                              Ou, Yonatan Bisk, Daniel Fried, Uri Alon, and Gra-
                                                             ham Neubig. 2024. WebArena: A realistic web en-
Haoxin Wang, Xianhan Peng, Huang Cheng, Yizhe                vironment for building autonomous agents. In In-
  Huang, Ming Gong, Chenghan Yang, Yang Liu, and             ternational Conference on Learning Representations
  Jiang Lin. 2025. ECom-bench: Can LLM agent                 (ICLR). ArXiv:2307.13854.
  resolve real-world E-commerce customer support is-
  sues? In Proceedings of the 2025 Conference on           Xuhui Zhou, Weiwei Sun, Qianou Ma, Yiqing Xie,
  Empirical Methods in Natural Language Process-             Jiarui Liu, Weihua Du, Sean Welleck, Yiming
  ing: Industry Track, pages 276–284, Suzhou (China).        Yang, Graham Neubig, Sherry Tongshuang Wu, and
  Association for Computational Linguistics.                 Maarten Sap. 2026. Mind the sim2real gap in user
                                                             simulation for agentic tasks. In Conference on Lan-
Peiyi Wang, Lei Li, Liang Chen, Zefan Cai, Dawei             guage Modeling (COLM). ArXiv:2603.11245.
  Zhu, Binghuai Lin, Yunbo Cao, Lingpeng Kong,
  Qi Liu, Tianyu Liu, and Zhifang Sui. 2024. Large lan-    Mingchen Zhuge, Changsheng Zhao, Dylan R. Ashley,
  guage models are not fair evaluators. In Proceedings       Wenyi Wang, Dmitrii Khizbullin, Yunyang Xiong,
  of the 62nd Annual Meeting of the Association for          Zechun Liu, Ernie Chang, Raghuraman Krishnamoor-
  Computational Linguistics (Volume 1: Long Papers),         thi, Yuandong Tian, Yangyang Shi, Vikas Chandra,
  pages 9440–9450, Bangkok, Thailand. Association            and Jürgen Schmidhuber. 2025. Agent-as-a-judge:
  for Computational Linguistics.                             Evaluate agents with agents. In Proceedings of the
                                                             42nd International Conference on Machine Learn-
Yizhong Wang, Yeganeh Kordi, Swaroop Mishra, Alisa           ing, volume 267 of Proceedings of Machine Learning
  Liu, Noah A. Smith, Daniel Khashabi, and Hannaneh          Research, pages 80569–80611. PMLR.
  Hajishirzi. 2023. Self-Instruct: Aligning language
  models with self-generated instructions. In Proceed-     A    Satisfied-but-Failed Rates by Rater
  ings of the 61st Annual Meeting of the Association for        Population
  Computational Linguistics (Volume 1: Long Papers),
  pages 13484–13508. Association for Computational         Table 4 reports the satisfied-but-failed rate behind
  Linguistics.                                             Figure 2a and the §4.1 claim: for each indepen-
 Rater population         Failed/Sat. Rate %           p                                                   high-
    2                                                          Human dimension         mean     ρsucc   p fail %     α
 τ -bench customer service
 Human panel (3 raters)     23/40      57.5     2×10  −7       Satisfaction            3.88 −0.147 0.07      57.5 0.79
 Opus-4.8 gate              30/63      47.6     8×10−7         Respect / tone          5.26 −0.118 0.15      63.6 0.76
 Opus-4.8 proxy             50/84      59.5    3×10−15         Clarity                 5.02 +0.085 0.30      56.5 0.83
 GPT-5.5 gate               29/57      50.9     2×10−7         Perceived helpfulness   4.10 −0.129 0.12      63.3 0.80
                                                               Would return            4.19 −0.168 0.04      61.7 0.81
 GPT-5.5 proxy             75/126      59.5    3×10−22
 SimulatorArena math tutoring                                 Table 5: Every subjective dimension the human panel
 Human rating (≥8/10)      12/31       38.7        0.013      rated, not satisfaction alone, is decorrelated from verifi-
                                                              able success (n=150). ρsucc is the Spearman correlation
Table 4: Satisfied-but-failed rate per rater popula-          of the 3-annotator consensus with verifiable reward;
tion: of conversations a population rated satisfied           “high-fail %” is the percentage of conversations rated
(human/Anthropic-scale ≥5/7; the GPT scale, which             ≥5/7 on that dimension that failed the task; α is the
grades ≈1 point lower, ≥4/7; SimulatorArena ≥8/10),           inter-annotator Krippendorff’s α (interval). Satisfaction
the percentage the verifiable oracle scored as failed. p is   (the gate’s optimized construct, bold) is the primary case
a one-sided exact binomial test against the lenient 20%       in the main text and the most conservative.
false-accept ceiling a construct-valid gate would meet.
Every population exceeds it; the gap is not a single-rater,
single-provider, or single-substrate artifact.                cess (all |ρ| ≤ 0.17), and each inverts at a compa-
                                                              rable rate (56–64% of highly-rated conversations
                                                              failed). The dimensions are highly collinear (pair-
dent rater population, the share of conversations
                                                              wise Spearman 0.61–0.97): they are not five in-
it rated satisfied that the non-LLM oracle scored
                                                              dependent tests but roughly one latent “this in-
as a task failure, with an exact one-sided binomial
                                                              teraction felt good” factor, measured five ways,
test against a lenient 20% ceiling, the false-accept
                                                              that is orthogonal to task success, which is why
rate a construct-valid gate should not exceed; for
                                                              the lone nominally significant correlation (would-
the satisfaction signals the primary comparator is
                                                              return, p=0.04, and negative) is a weak effect and,
the base failure rate (Table 2), which they sit at.
                                                              as the only nominal hit among five correlated tests,
Every population’s satisfied-but-failed rate is far
                                                              consistent with chance. Satisfaction is, if anything,
above 20%: the human panel and all four LLM
                                                              the conservative choice: its inversion rate (57.5%)
scorings on τ 2 reject the ceiling at p < 10−6 , and
                                                              is among the lowest of the five. None of the other
the independent SimulatorArena human ratings at
                                                              subjective dimensions would close the gap.
p=0.013.
                                                              C    The Controlled-Degradation Set
Leave-one-annotator-out. The panel headline
does not depend on any single rater: removing any             Purpose and design principle. The headline
one of the three annotators keeps the satisfied-but-          cross-provider grid (25 agents) establishes exter-
failed rate within 56.4–60.5% (a 4.1-point spread             nal validity (does the gate rank real, deployable
around the reported 57.5%), and each annotator                models correctly?), but it cannot cleanly charac-
independently shows the same inversion (58.1%,                terize the gate’s behavior on a known-bad agent,
63.5%, 59.5% satisfied-but-failed).                           because frontier models are all competent. The
                                                              controlled-degradation set supplies that missing in-
B       The Construct Gap Is Not Specific to                  ternal validity: a single model (Claude Sonnet-4.5)
        Satisfaction                                          is run under 12 configurations of a-priori-known
                                                              quality, so any rating difference is attributable to
The main text reports satisfaction as the primary
                                                              agent behavior rather than to provider or prompt-
subjective signal because it is the construct the re-
                                                              style confounds. This instantiates the controlled-
lease gate’s rubric and the LLM-proxy optimize,
                                                              perturbation paradigm reviewed in §2 (Ribeiro
and the target the LLM-judge literature validates
                                                              et al., 2020; Adebayo et al., 2018): the known-
against. The blind human panel, however, rated
                                                              degradation “sanity check” that crippling a system
five subjective dimensions per transcript (satisfac-
                                                              must register on a valid metric, applied here to a
tion, respect/tone, clarity, perceived helpfulness,
                                                              release gate.
and would-return). Table 5 shows the construct
gap generalizes beyond satisfaction: every dimen-             Flag-only degradation. Crucially, every con-
sion shows no association with verifiable task suc-           figuration shares the identical agent prompt
and tool set; we perturb only inference-time               Config          Perturb.         Rew. Gate Prx. Hum.
flags: sampling temperature, the output-token              Good tier (temperature only; full budgets)
cap (max_tokens), the conversation step cap                A1 standard     T =0                0.67 4.08 4.62 4.15
                                                           A2 strict       T =0                0.63 4.20 4.63 4.15
(max_steps), and the orchestrator error toler-             A3 temp0.2      T =0.2              0.68 4.50 4.73 3.24
ance (max_errors). No prompt is rewritten
                                                           Medium tier (higher temp; mild caps)
and no code is edited. Each degradation is a mis-          B3 temp0.7      T =0.7            0.68   4.42   4.72   4.67
configuration a real deployment could plausibly            B4 tight-budget T 0.7,tok256      0.62   4.07   4.32   4.53
ship: a too-low output cap truncates tool-call JSON        B5 high-var.    T =1.0            0.65   4.17   4.87   4.25
                                                           B6 temp0.5      T =0.5            0.62   4.22   4.67   4.52
and confirmations mid-emission; a too-low step             B7 tok384       T 0.3,tok384      0.62   4.27   4.78   3.85
cap cuts the trajectory off before the verifiable          Degraded tier (budget/step/error starvation)
action ( τ 2 retail tasks require authenticate → lo-       D6 trunc.        tok96             0.20 2.27    3.68   2.94
cate → act → confirm ); an aggressive error-abort          D7 step-starv. st6                 0.00 2.70    4.87   4.64
                                                           D8 compound T 1.0,tok48,err1 0.00 1.65          3.85   2.69
terminates the episode on the first malformed tool         D9 tok72/st12 tok72,st12           0.02 2.38    4.05   3.12
call. This keeps the intervention transparent and
reproducible while breaking verifiable task com-           Table 6: The 12 controlled-degradation configura-
pletion rather than surface fluency, precisely the         tions (all Claude Sonnet-4.5, flag-only). Columns:
regime in which satisfaction can diverge from suc-         verifiable reward (pass-rate), and mean LLM-judge
cess. Because these are truncation-style failures,         Gate, LLM-Proxy, and Human-panel satisfaction (1–
                                                           7). tok=max_tokens, st/steps=max_steps,
the judge-free completion bit tracks them well here
                                                           err=max_errors. The degraded tier collapses on
(ρ=0.87; §4.5); on the naturalistic six-provider           verifiable reward (≈0) yet every subjective signal still
grid, where 96.5% of failures instead terminate            rates it mid-scale. D7 (highlighted) is the sharpest in-
normally (semantic), the same bit collapses, which         version: reward 0.00 but human satisfaction 4.64, the
is why we scope it as a truncation-specific tripwire       highest of any degraded config, because a step-capped
rather than a general regression detector.                 trajectory is cut off mid-task while reading as helpful
                                                           turn-by-turn.
Positive control: the ground-truth ordering
is known. By construction the four D (de-
graded) configurations must rank below the eight           the degraded set; the local dip does not establish
A/B (good/medium) ones. The non-LLM veri-                  reliable non-monotonicity. We therefore treat the
fiable reward confirms a large, clean separation           gate as a ranking instrument (§4.2) rather than a
(degraded-tier mean reward 0.05 versus 0.65 for            calibrated probability.
good/medium), so the set behaves as a positive con-
trol: a release signal that fails to place the D configs
                                                           D    Second-Provider Simulator Replication
last is exhibiting a measurable validity failure, not      With a controlled swap, we test directly whether
noise. Table 6 gives the full specification and every      the satisfied-but-failed gap is an artifact of one
signal’s per-variant mean.                                 over-cooperative simulator rather than a property
                                                           of the satisfaction signal. Holding everything else
C.1   Gate-score calibration                               fixed (the same 12 degradation variants, 6 persona
Figure 5 plots the empirical task-success rate at          strata, and identical task ids, the same rubrics and
each integer gate score, with Wilson 95% confi-            judge, and the same non-LLM oracle), we re-drive
dence intervals, for both the controlled-degradation       the grid with the user-simulator changed to a dif-
set and the six-provider grid. Both are increasing         ferent provider, OpenAI GPT-5.4. The simulator
overall (Spearman ρ=0.86 and 0.96 over the seven           provider is then the only variable that differs from
score bins), so a higher gate score does on aver-          the matched arm, so any persistence of the gap
age mean a higher chance of success. Calibration           cannot be a single-simulator effect.
is, however, cleaner on the diverse grid: on the              The inversion persists under the swap (Table 7).
controlled set the mid-range scores (4–5) sit below        Under both simulators the satisfied-but-failed rate
score 3 in point estimate, but those bins are small        sits far above the 20% a construct-valid signal
(n=54, 60) and their intervals overlap score 3’s, so       would target: GPT-5.4 66.7% (gate) and 69.8%
the local dip is not individually significant. Read        (proxy) versus Sonnet-4.5 43.6% and 52.9% on
conservatively, the data show only that mid-range          the matched cells, all with p < 10−7 . We read
gate scores carry little additional success signal on      this as a qualitative invariant (satisfaction fails to
                                                                                         Mean        Gate     Proxy
                                                                User-simulator            rew.   failed %   failed %
                                                                Sonnet-4.5 (Anthropic)    0.32      43.6       52.9
                                                                GPT-5.4 (OpenAI)          0.21      66.7       69.8

                                                            Table 7: Controlled second-provider simulator swap
                                                            on the retail degradation grid: identical 12 variants
                                                            × 6 strata × task ids (n=216 each), same Sonnet-4.5
                                                            agent, only the user-simulator provider differs. The
                                                            satisfied-but-failed (false-accept) rate stays far above
                                                            the 20% null under both simulators, so it is not a Sonnet-
                                                            simulator artifact. “Satisfied” is ≥5/7; “failed” is veri-
                                                            fiable reward = 0. The two simulators yield different
                                                            mean agent reward (GPT-5.4 harsher), so compare each
Figure 5: Gate-score calibration with Wilson 95% confi-     rate to the null, not to each other.
dence intervals: empirical P (success) at each gate score
on the controlled-degradation set (N =718 gate-scored,      rank (1=best) under the verifiable reward and un-
Spearman ρ=0.86) and the six-provider grid (n=3,686
                                                            der the two frontier judges Opus-4.8 and GPT-5.5.
gate-scored, ρ=0.96). The grid is near-monotonic; the
controlled set dips in the mid-range (scores 4–5 below      Agents are grouped by provider with providers
score 3), but with small bins and overlapping intervals     ordered by mean reward (low→high capability),
the dip is not significant. Calibration quality depends     matching the figure’s top-to-bottom layout. The
on the agent population.                                    surplus shrinks across the capability tiers (surplus
                                                            vs. reward Spearman ρ= −0.51, p = 8.5e−3,
                                                            n=25): large and positive for Mistral and Qwen
track success under an independent simulator), not
                                                            (+0.20 to +0.40), mixed for Meta (−0.06 to
as a rate comparison: the two simulators steer the
                                                            +0.20), and near zero or negative for the frontier
same agent into different trajectories and so yield
                                                            (DeepSeek, OpenAI, and the strongest Anthropic
different mean verifiable reward (GPT-5.4 0.21 vs.
                                                            configs). The rank columns make the judges’ agree-
Sonnet 0.32, the harsher simulator surfacing more
                                                            ments and disagreements explicit: both frontier
task failures), which mechanically shifts the ab-
                                                            judges place the OpenAI agents in their top three
solute false-accept rate. The defensible claim is
                                                            on satisfaction, a same-style preference the verifi-
therefore that the gap is large and highly significant
                                                            able reward does not share, as it ranks the GPT-5.4
under both simulator families.
                                                            configs at 7–9 and places Anthropic’s Opus-4.6
Full ranking grid under GPT-5.4. The swap                   first on ground-truth task success.
above isolates the construct gap; we also re-ran the
entire 25-agent ranking grid with the GPT-5.4 user-         F     Per-Judge Ranking Validity Across
simulator (114 tasks per agent, 2,850 transcripts),               Providers and Domains
holding agent, tasks, rubrics, judge, and oracle            Section 4.2 summarizes ranking validity; Fig. 6
fixed. The agent ordering is preserved: Spear-              shows the underlying per-judge gate-vs-reward
man ρ=0.93 (Pearson 0.97; base-model cluster-               scatters in full. On the τ 2 grid the gate’s rank-
bootstrap 95% CI [0.71, 0.98]), against 0.94 under          ing is recovered by all four judges, the primary
Sonnet-4.5, and the near-equal degradation repro-           Opus-4.8 (ρ=0.94) and GPT-5.5 (0.84), and the
duces (top-11 ρ=0.51). Same-family simulator–               deployed Sonnet-4.5 (0.92) and GPT-5.4 (0.94);
agent affinity therefore does not account for the           the two frontier judges’ domain splits are Opus-4.8
ranking result (§4.2).                                      retail 0.95, airline 0.80, and GPT-5.5 retail 0.87,
E    Per-Agent Data Behind Figure 4                         airline 0.65.

Table 8 gives the full per-agent values plotted in          F.1    The near-equal regime persists under
Fig. 4 (the cross-provider dumbbell): for each of                  frontier judges
the 25 agents, the verifiable reward (mean ± SE),           We test whether the judge is weaker than the
the LLM-judge gate and LLM-proxy satisfac-                  strongest agents it scores, which would make the
tion (1–7 means), the satisfaction surplus (proxy           near-equal top-11 ceiling (§4.2) an artifact of judge
mapped to [0, 1] minus reward), and each agent’s            capability rather than a real property of the agents.
                                                                                       Rank (1=best) by
        Agent                   Reward (mean ± SE)   Gate    Proxy   Surplus   Reward      Opus-4.8   GPT-5.5
        Meta (r̄ = 0.34)
        Llama-3.1-8B (t.7)          0.32±0.06        2.16    4.13     +0.20       23          25          25
        Llama-3.3-70B (t.7)         0.33±0.06        2.32    2.76     −0.04       22          22          18
        Llama-3.1-8B                0.35±0.06        2.08    3.79     +0.12       19          24          24
        Llama-3.3-70B               0.35±0.06        2.18    2.71     −0.06       20          21          21
        Mistral (r̄ = 0.40)
        Mistral-Small               0.28±0.04        1.93    3.99     +0.22       25          23          23
        Mistral-Small (t.7)         0.30±0.04        2.16    4.01     +0.20       24          20          22
        Ministral-3B (t.7)          0.35±0.04        2.68    4.45     +0.23       21          19          20
        Ministral-3B                0.44±0.04        2.69    4.83     +0.20       17          17          19
        Mistral-Large-3 (t.7)       0.51±0.04        4.24    5.62     +0.26       15          15          14
        Mistral-Large-3             0.54±0.04        4.40    5.63     +0.24       14          14          15
        Qwen (r̄ = 0.49)
        Qwen3-32B (t.7)             0.37±0.04        2.54    5.60     +0.40       18          16          16
        Qwen3-32B                   0.44±0.04        2.66    5.45     +0.30       16          18          17
        Qwen3-235B                  0.57±0.04        4.16    5.68     +0.21       13          13           6
        Qwen3-235B (t.7)            0.59±0.04        4.23    5.80     +0.21       12          12           4
        DeepSeek (r̄ = 0.77)
        DeepSeek-V3.2 (t.7)         0.75±0.03        5.09    5.53     +0.01       8           9           5
        DeepSeek-V3.2               0.78±0.03        5.20    5.62     −0.01       6           5           7
        OpenAI (r̄ = 0.78)
        GPT-5.4 (t.7)               0.74±0.03        5.51    5.57     +0.02       9           3           3
        GPT-5.4                     0.77±0.03        5.62    5.56     −0.01       7           2           2
        GPT-5.5                     0.84±0.03        5.54    5.79     −0.04       3           1           1
        Anthropic (r̄ = 0.78)
        Haiku-4.5 (t.7)             0.66±0.04        4.68    5.77     +0.13       11          10          13
        Haiku-4.5                   0.68±0.04        4.71    5.85     +0.12       10          11          12
        Sonnet-4.6 (t.7)            0.80±0.03        4.78    5.92     +0.02        5           7          11
        Sonnet-4.6                  0.81±0.03        4.96    5.89     +0.00        4           8          10
        Opus-4.6                    0.84±0.03        5.03    5.97     −0.01        2           6           8
        Opus-4.6 (t.7)              0.87±0.03        5.00    5.97     −0.04        1           4           9

Table 8: Per-agent data behind Fig. 4, all 25 agents. Reward is the verifiable pass-rate (mean ± standard error across
the agent’s transcripts); Gate and Proxy are 1–7 satisfaction means; Surplus = (proxy−1)/6− reward, i.e. how
far satisfaction overstates verifiable success on a common [0, 1] scale. The last three columns give each agent’s
rank (1=best) by verifiable reward and by the two frontier judges Opus-4.8 and GPT-5.5. Providers are ordered by
mean reward r̄. Surplus vs. reward: Spearman ρ= −0.51 (p = 8.5e−3). The rank columns expose where judges
depart from ground truth: both frontier judges rank the GPT agents 1–3 on satisfaction, well above their reward
ranks (GPT-5.4 at 7–9), a same-style preference, whereas the verifiable reward ranks Anthropic’s Opus-4.6 first; the
judges still track the overall ordering (full-ladder ρ≥0.84, §4.3).


Figure 7 rules this out. It places, for all four judges,     Decision-disagreement rate (§4.2). Table 9
the gate-vs-reward Spearman ρ on the full 25-agent           gives, per signal, the fraction of agent pairs on
ladder beside the same ρ on the near-equal top-11            which the gate promotes the lower-reward agent,
subset. Two patterns stand out: every judge recov-           split by whether the pair’s verifiable rewards are
ers the full ladder (ρ=0.84–0.94), and on the top-11         near-equal (|∆R| < 0.1, n=87 pairs) or wide
no judge recovers the ordering (ρ=0.25–0.51, all             (|∆R| ≥ 0.1, n=211). Every signal is near-
n.s. at n=11). The two frontier judges (Opus-4.8,            perfect on wide pairs and degrades sharply on
GPT-5.5), which match the strongest agents in the            close ones; the effect is not sensitive to the ex-
pool by verifiable pass-rate (§4.3), do no better            act 0.1 threshold (Opus-4.8: 45%, 31%, 26% at
there than the deployed Sonnet-4.5 judge. If the             |∆R| < 0.05/0.10/0.15).
ceiling were a judge-capability artifact, the most
capable judges would escape it. The near-equal               Is the 31% reference-ranking noise or an ar-
limit therefore reflects agent near-equality bounded         tifact of non-independent pairs? Two checks
by oracle resolution, not judge capability.                  rule this out. A base-model cluster bootstrap (13
                                                             clusters, resampling base models rather than pairs)
Figure 6: Per-judge gate-vs-reward validity across all available judges and domains. τ 2 rows: four judges pooled
(Sonnet-4.5, GPT-5.4, Opus-4.8, GPT-5.5) and the Opus-4.8/GPT-5.5 retail vs airline splits; each point is an agent,
provider-colored, with Spearman ρ annotated.


Signal                             Near-equal %   Wide %
Opus-4.8 gate (primary frontier)       31.0         0.9
GPT-5.4 gate                           29.9        1.4
GPT-5.5 gate                           39.1        7.6
Pooled gate (gate_quality)             37.9        1.4
LLM-proxy satisfaction                 29.9        10.4

Table 9: Decision-disagreement rate by signal: fraction
of pairs where the gate promotes the lower-reward agent,
on near-equal (|∆R| < 0.1, n=87) vs. wide      (|∆R| ≥
0.1, n=211) pairs; the 2 exact-tie pairs of the 25
                                                 2 =300
are excluded. Base-model cluster-bootstrap 95% CI on
the Opus-4.8 near-equal rate: [11.6, 50.0].                Figure 7: Four-judge robustness. All four judges, includ-
                                                           ing the frontier Opus-4.8 and GPT-5.5, which match the
                                                           strongest agents in the pool by verifiable pass-rate, re-
                                                           cover the full 25-agent ladder (ρ=0.84–0.94), but none
                                                           recovers the near-equal top-11 (ρ=0.25–0.51, all n.s.).
                                                           The near-ceiling regime persists even for the most ca-
puts the primary Opus-4.8 near-equal rate at 31.0%,        pable judges, so the limit reflects agent near-equality
                                                           bounded by oracle resolution, not judge capability.
95% CI [11.6, 50.0], its lower bound still ∼13×
the 0.9% wide-pair rate; and dropping the least-
independent same-base-model temperature pairs
                                                           F.2   Same-family self-preference
leaves 32.0% on the 75 cross-base-model pairs
(24/75). The disagreement is also signal-specific          The two-provider design isolates same-family self-
rather than shared ordering noise: of the 60 near-         preference as a difference of differences (§4.3):
equal pairs flipped by at least one of the five sig-       the Anthropic Opus-4.8 judge rates Claude agents
nals, only 4 are flipped by all five and 22 by ex-         above the GPT-5.5 judge, and by a larger mar-
actly one (mean pairwise Jaccard 0.40), so the 31%         gin than it rates non-Claude agents (Fig. 8). The
is a population-level, signal-specific property, not       diff-in-diff is +0.75/7 (the deployed Sonnet-4.5
shared reference-ranking noise.                            judge shows the same effect at +0.67/7 against
                                                            the error is common-mode, so ensembling cannot
                                                            average it away. The one effective lever is cali-
                                                            brated abstention, declining to rank a pair whose
                                                            gate-score gap falls inside its bootstrap sampling
                                                            noise. On the pairs it does rank (31–49% of near-
                                                            equal pairs, depending on the abstention threshold)
                                                            it roughly halves the error to 14.8%, buying selec-
                                                            tivity rather than resolution, which confirms that
                                                            the limit is oracle resolution, not judge choice.

                                                            H    Why Airline Ranking Is Weaker:
Figure 8: Same-family self-preference, shown explicitly.         Gate-Score Range Restriction
The Opus-4.8 judge inflates Claude agents relative to the
GPT-5.5 judge more than it inflates non-Claude agents
                                                            Range restriction, rather than a deficiency of the
(diff-in-diff +0.75/7).                                     gate, explains the lower airline ranking validity
                                                            (§4.2). Fig. 9 shows the gate-score distributions
                                                            per domain: the airline gate spans a ≈2.2× nar-
GPT-5.4); being scale-invariant, it reflects same-          rower band than retail (Sonnet gate range 2.03 vs
family self-preference rather than absolute harsh-          4.56; GPT-5.4 gate 1.19 vs 3.56, a 3.0× compres-
ness. Crucially, the ranking agreement is un-               sion), while the verifiable-reward spread is nearly
changed (ρ=0.92; §4.3), so self-preference is a             identical across domains (range ratio 1.17×). With
measured caveat on the absolute scores while rank-          agents compressed into a narrow gate band there
ing validity holds.                                         is less to rank, which attenuates a rank correlation;
                                                            both judges exhibit the same compression, confirm-
F.3   Judge stability                                       ing it is a property of the airline substrate rather
Two reruns confirm the agent ranking is not an arti-        than of either judge.
fact of judge noise. First, in a test–retest, re-scoring
48 transcripts three times (judge temperature 0.7)          I   Persona Strata
yields a judge self-reliability of ICC=0.87 (Shrout         The user-simulator is conditioned on one of six
and Fleiss, 1979) and a variant-level rank stability        persona strata, each a 2–4 sentence second-person
of ρ=0.92 across re-scorings, a judge-noise mea-            behavioral overlay prepended to the τ 2 -bench task
sure distinct from the human-panel inter-annotator          instructions (the task facts, namely order IDs, cus-
agreement (Krippendorff’s α=0.79). Second, run-             tomer identity, and item specs, are held fixed, so
ning the GPT judge five independent times agrees            only tone, cooperativeness, and pacing change; the
with itself on the agent ranking at mean ρ=0.74             verifiable-reward signal is unaffected). The strata
(min 0.52); per-run validity against the verifiable         are hand-authored archetypes whose axes (coop-
reward is noisier (ρ=0.24–0.59 across runs), which          erativeness, patience, assertiveness) are informed
is why we report that judge as a ranking-agreement          by the OPeRA persona schema (Wang et al., 2026)
check (§4.3) rather than a per-run validity estimate.       (demographics, Big-Five, and Consumer-Styles-
                                                            Inventory shopping styles); we do not sample indi-
G     Cheap Signals for the Near-Equal                      vidual OPeRA records. Table 10 lists them. Per-
      Regime                                                sona conditioning is behaviorally real: on an iden-
                                                            tical retail task, the cooperative user writes “Yes,
We test whether any cheaper signal removes the
                                                            I confirm. Please go ahead . . . I appreciate your
near-equal decision error of §4.2 without the paid
                                                            help” while the impatient user writes “I don’t have
audit. Across 21 candidate signals, spanning single
                                                            time for this . . . just do it already” and the skep-
judges, the process-blind proxy, the completion bit,
                                                            tical negotiator probes “this ‘no modification fee’
and unweighted and confidence-weighted judge en-
                                                            sounds too good to be true, what’s the catch?”
sembles, none outperforms the best single judge on
near-equal pairs. Averaging all four judges gives           Verbatim persona overlays. Each stratum is
exactly 31.0% (27/87), identical to the best sin-           a second-person behavioral overlay prepended
gle judge, because the judges are highly correlated         to the task instructions with the wrapper
(pairwise ρ 0.67–0.98) and flip the same close pairs:       “PERSONA: adopt this style for
Figure 9: Gate-score distributions by domain for both judges (box + per-agent strip), with the reward distribution as
a control. The airline gate signal is ≈2.2–3.0× more compressed than retail (Sonnet and GPT-5.4 alike), whereas
verifiable reward is comparably spread in both domains, so the weaker airline ranking ρ is driven by gate-score
range restriction, not by the gate being less valid there.


    Stratum                   Coop. Patience Assert.
    S1 Cooperative            high   high     low
    S2 Impatient/rude         low    low      high
    S3 Distracted             med    med      low
    S4 Anxious/low-trust      med    med      med
    S5 Terse                  high   med      med
    S8 Skeptical negotiator   low    med      high

Table 10: The six persona strata and their design axes
(cooperativeness, patience, assertiveness), informed by      Figure 10: Effect of persona strata on agent difficulty
the OPeRA schema (Wang et al., 2026). The six are            and ranking (retail), discussed in §4.4. (a) Per-variant
drawn from an eight-archetype pool; S6 and S7 (chatty        verifiable reward under the ungrounded default-τ 2 user
over-sharer, indecisive perfectionist) are defined but not   versus the six persona strata: personas cut mean verifi-
exercised in the reported runs, hence the index gap.         able reward 42% (0.47 → 0.27) while the agent order-
Used in the controlled-degradation set and the 150-          ing holds (reward-rank ρ=0.83). (b) Per-stratum reward,
transcript human panel; see §4.4 for their effect on agent   gate, and LLM-proxy satisfaction (grounded 720-set,
difficulty and ranking.                                      common [0, 1] scale): satisfaction varies sharply by per-
                                                             sona but does not track reward.

the entire conversation; keep all
facts of your request unchanged:                                  time. Blunt to the point of rudeness, interrupts
{overlay}”, followed by the unchanged                             with demands rather than answering proce-
τ 2 -bench task. The full overlays are:                           dural questions, becomes openly irritated at
                                                                  requests for information they think the agent
S1 Cooperative. A courteous, even-tempered cus-                   should already have, pressures the agent to
    tomer in their mid-30s who shops online regu-                 skip steps, and demands escalation when any-
    larly and trusts the representative. Answers di-              thing takes more than a couple of exchanges.
    rectly and completely, stays focused, stays pa-
                                                             S3 Distracted. A multitasking customer only half
    tient through multi-step resolution, confirms
                                                                 paying attention, replying while distracted.
    details without rushing, and expresses mild
                                                                 Gives incomplete or slightly-off answers,
    appreciation when things go well.
                                                                 misses what was just asked, and drifts onto
S2 Impatient/rude. A busy, short-tempered cus-                   tangents before returning; not hostile, just
    tomer who feels they have wasted too much                    scattered (“sorry, what did you ask?”), so the
     agent must keep them on track.                      Cross-provider ladder (τ 2 -bench retail + airline)
                                                         Scorable transcripts (non-null reward)                  3,691
S4 Anxious/low-trust. A risk-averse customer               retail / airline                              2,487 / 1,204
    who distrusts remote support and worries             Agent configurations scored                                25
                                                         Task pool (retail / airline)                        114 / 50
    something will go wrong. Asks the agent
    to justify each action before agreeing, seeks        Controlled-degradation set (Sonnet-4.5, flag-only)
                                                         Transcripts                                              720
    repeated reassurance about charges, and hesi-        Cells (12 configs × 6 strata × 2 domains)                144
    tates before sharing details; polite but cautious    Transcripts per cell                                        5
    (“are you sure?”, “what happens if this doesn’t      Tiers (good / medium / degraded)            3 / 5 / 4 configs
    work?”).                                             Human panel (τ 2 subsample)
                                                         Transcripts / annotators                             150 / 3
S5 Terse. An experienced, no-nonsense customer           Stratification (retail / airline)                    85 / 65
    who values speed. Responds in clipped, mini-           failed / succeeded                                 86 / 64
                                                         Krippendorff’s α (satisfaction)                        0.79
    mal phrases, skips pleasantries, and provides
    only the specific information requested; coop-       SimulatorArena (math tutoring)
                                                         Models / graded conversations                          9 / 50
    erative in substance but cold in style, nudging      High-satisfaction subset (≥8/10)                           31
    the agent to get to the point.
                                                        Table 11: Dataset statistics across the three substrates.
S8 Skeptical negotiator. A price-sensitive, deal-
                                                        The 25 scored agent configurations are the 28 (model,
    driven customer who treats every interaction        temperature) cells minus three excluded for infrastruc-
    as a negotiation and is skeptical of any policy     ture reasons (Llama-3.1-405B at both temperatures,
    that does not favor them. Assertively chal-         throttle-limited; and the GPT-5.5 temperature-0.7 cell,
    lenges fees and refusals, presses for waivers or    as GPT-5.5 fixes its sampling setting). Conversations
    exceptions, and probes for loopholes; persis-       average 31 messages, 8.6 tool calls, and 7.6 user turns.
    tent and adversarial but not abusive, relenting
    only once a limit is firmly justified.
                                                        2024, 2025), and OpenAI GPT-5.4/5.5 (OpenAI,
The persona modifies only tone, cooper-                 2026a,b), each run at two temperatures.
ativeness, pacing, and assertiveness; task
facts (reason_for_call, known_info,
                                                        K     Oracle Patch and Validation
evaluation_criteria) are untouched,                     The verifiable reward is the ground truth the audit
so the verifiable reward is unaffected. The             rests on, so we document our only modification
two defined-but-unexercised strata (S6 chatty           to the τ 2 -bench evaluator, a bug-fix rather than a
over-sharer, S7 indecisive perfectionist) account       degree of freedom, in two disjoint parts.
for the gap between S5 and S8.
                                                        (A)       Backend       swap      (no     scoring
J   Dataset Statistics                                  change). Four         DEFAULT_LLM_*           con-
                                                        stants are repointed from gpt-4.1 to
Table 11 summarizes the three evaluation sub-           bedrock/...claude-sonnet-4-5 (tem-
strates. The cross-provider ladder is the headline      peratures stay at 0), so the agent, simulator, and
grid; the controlled-degradation set is the posi-       LLM sub-evaluator run on Bedrock; no scoring
tive control (§4.5); the human panel and Simu-          logic is touched.
latorArena provide the human-grounded checks
(§4.1). The controlled-degradation set and the          (B)       Tolerant        verdict       parser. A
persona-simulated conversations are generated syn-      loads_tolerant helper replaces a bare
thetically; synthetic generation is a common rem-       json.loads at two sites (tool-output compar-
edy for scarce labeled data in NLP (Wang et al.,        ison and NL-assertion parsing): it tries strict
2023; Bodhwani et al., 2025b). The ladder’s             json.loads first and only on failure strips
14 base models are Anthropic Opus-4.6/Sonnet-           “‘json fences or extracts the outermost JSON
4.6/Haiku-4.5 (Anthropic, 2026a,c, 2025), Meta          object, re-raising if nothing parses. It never
Llama 405B/70B/8B (Grattafiori et al., 2024;            rewrites or flips a parsed verdict and adds no pass
Meta, 2024), Mistral Large-3/Small/Ministral-3B         condition; it only recovers verdicts strict parsing
(Mistral AI, 2025), Qwen3 235B/32B (Yang                would drop because Claude wraps JSON in prose
et al., 2025), DeepSeek-V3.2 (DeepSeek-AI,              (absent in GPT JSON-mode). A 16-case unit
test confirms identical parsing on valid JSON,            the way an ordinary, non-expert customer would,
recovery on fenced/wrapped JSON, and a raise on           based purely on how the conversation FELT to
unparseable input.                                        you, not on any knowledge of company policies,
                                                          internal tools, or what the agent did behind the
Why the reward is robust to the patch.
                                                          scenes.” It rates satisfaction, respect/tone, clarity,
The reward is the product of each task’s
                                                          perceived helpfulness, and would-return on 1–7,
reward_basis components; the DB-state, ac-
                                                          and is shown only the user-visible spoken turns
tion, environment-assertion, and communicate
                                                          (tool calls and the task stripped out), enforcing
checks are deterministic Python, and the NL-
                                                          process-blindness. This disjointness in role,
assertion judge is the only LLM the parser
                                                          evidence, and vocabulary is what prevents the gate
touches. Airline (reward_basis = (DB, COM-
                                                          and proxy from agreeing by shared-rubric artifact.
MUNICATE)) is thus fully deterministic and patch-
independent; for retail ((DB, NL_ASSERTION))              Human panel. The three annotators received
the NL term is multiplicatively gated by the de-          written instructions to rate the feeling of being
terministic DB check and changed the outcome in           served, not the mechanics: “An agent can feel great
only 113 of 2,537 applicable simulations (4.5%).          yet not actually solve your problem, and vice versa;
The harness persists only the parsed verdict, so          rate your experience.” They scored the same five
we rely on this lossless-by-construction argument         dimensions (1–7) plus a one-phrase “biggest prob-
rather than an empirical recovery rate, and make          lem” field, blind to the verifiable reward, variant,
no claim of human–oracle agreement (the panel             and model identity, on the user-visible transcript
rated experience, not task success). Crucially, the       only.
satisfaction–success gap does not depend on this
component: on airline, whose oracle contains no           User simulator. The persona-driven simulator
LLM, the process-blind proxy still false-accepts          extends the base τ 2 -bench guidelines (“generate
62.1% of satisfied conversations (325/523).               one message at a time. . . disclose information pro-
                                                          gressively. . . never hallucinate information not in
L    Prompts and Rubrics                                  the scenario. . . emit ###STOP### when the goal
                                                          is satisfied”) with the persona overlay (Appendix I);
We reproduce the operative prompts verbatim.              task facts are unchanged.
Model identifiers and tool names are kept as
run. All scoring runs offline through a Bedrock-          M    Representative Examples
Converse harness; a tolerant judge-output parser
recovers the score line from formatting variation,        One real, de-identified example per substrate
cutting null judge scores from 36.6% to near zero.        (public-benchmark tasks; no customer data).

Release-gate judge (policy-aware). System                 τ 2 retail (satisfied but failed). Task: a customer
prompt (abridged): “You are a release-gate quality        (Yusuf Rossi, zip 19122) asks how many t-shirt
auditor for an automated retail customer-service          options exist and to change all pending t-shirt or-
agent. . . you evaluate ONLY the assistant, from          ders to purple, size S, v-neck, polyester. The agent
the standpoint of an operations supervisor decid-         authenticates by name+zip, lists the options, and re-
ing whether this agent variant is safe to ship.” It       ports “Both modifications have been completed suc-
scores four dimensions in priority order, (1) pol-        cessfully.” The user ends satisfied (###STOP###).
icy adherence (authenticate before acting; explicit       Gate 7/7, proxy 7/7, human panel 5.5/7, veri-
confirmation before any database write; one tool          fiable reward 0.0: all three satisfaction signals
call per turn; no fabrication), (2) task resolution,      passed, yet a pending order was never modified (12
(3) efficiency, and (4) professionalism, on a 1–7         of 13 tool calls correct), so the task failed despite a
scale, explicitly instructing that “a polite agent that   flawless-feeling interaction.
skipped authentication or wrote to the database
                                                          τ 2 airline (satisfied but failed). Task: a cus-
without confirmation must score low,” and emitting
                                                          tomer (Mohamed Silva) asks for the summed gift-
a final SCORE: <1-7> line.
                                                          card and certificate balances and to rebook a reser-
Human-proxy       (satisfaction-only). System             vation to the cheapest business round-trip without
prompt (abridged): “You are role-playing a real           changing dates. The agent reports balances and
online shopper who just finished a chat. . . answer       confirms the charges; the user replies “That’s ev-
erything I needed. Thank you so much!” Proxy
7/7, reward 0.0: the rebooking did not match the
required end-state, and the cross-provider judge
(GPT-5.4 gate 1/7) flags it.
SimulatorArena math tutoring (satisfied but
wrong). Problem: 11 players each pass to every
other player three times; how many passes? The
tutor walks through “one player makes 10×3 = 30
passes,” then states “the correct total is indeed 165.
Well done!” Human rating 10/10, proxy 7/7, but
verifiably incorrect: the tutor’s own shown work
(30 passes per player, 11 players) implies 330, not
the stated 165; the policy-aware gate (Opus-4.8
1/7) catches the error the human did not.

