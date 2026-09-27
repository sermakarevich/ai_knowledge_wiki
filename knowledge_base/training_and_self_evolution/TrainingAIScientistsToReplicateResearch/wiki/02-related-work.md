> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Related Work: Rewards, Replication, and Training AI Scientists

**In one sentence:** The related work survey positions the paper along three axes — (1) two ways to produce scalar rewards for AI Scientist agents (verifiable benchmark rewards vs. LLM-judged rollouts), (2) the replication-benchmark spectrum trading off ease of evaluation against construct validity, and (3) prior training approaches (test-time scaling, hand-designed multi-agent systems) that this work supersedes with large-scale post-training over a 242-task space using GRPO with an LLM rubric judge.

## Key points

- Scientific research is underspecified: context-dependent, admits many solution kinds, and quality judgement is subjective — so the longstanding "automate science" literature (Schmidhuber 1987; Bengio et al. 1992; Kirsch et al. 2020, 2022; Real et al. 2020) that moves pieces of the research loop (update rule, objective, or full learning algorithm) inside a learner assumes a well-defined reward signal that is hard to define for broad research.
- Two natural reward strategies exist: (a) a verifiable reward derived from existing benchmarks (effective when hill-climbing yields novel insight, as in FunSearch, Romera-Paredes et al. 2024, and AlphaEvolve, Novikov et al. 2025), and (b) qualitative LLM judgement of agent behaviour; this paper adopts (b).
- The benchmark-reward approach has a critical limitation: discoveries are adaptations, not exaptations (Gould & Vrba, 1982) — innovations don't generalise — plus a ceiling on attainable insight, and heavy human labour to build benchmarks limits scalability (Goldie et al., 2026 mitigate via auto-generated combinatorial task spaces with meta-train/test splits, but similar problems re-emerge at the meta level).
- Unlike prior LLM-judge systems that mirror peer review (Lu et al. 2024; Weng et al. 2025; Schmidgall et al. 2025) — a highly underspecified setting with minimal ground truth and considerable noise — this paper's rubric judge evaluates paper replication, a more modest, controlled, grounded setting where agreement with humans is easier to establish.
- Existing replication benchmarks differ in how much of the original work is handed to the agent, trading off ease of evaluation with construct validity (Cronbach & Meehl, 1955; Bean et al., 2026): from scoring a finished reproduction (Hu et al., 2025) and running authors' code to answer questions (Alizadeh et al., 2026; Siegel et al., 2026), to masked reference implementations graded by unit tests (Hua et al., 2025; Kon et al., 2025), code similarity (Xiang et al., 2025), or a judge (Yan et al., 2025); this paper sits at the latter end — paper in, judge-graded out — closest to Zhao et al. (2026) and Seo et al. (2026).
- The paper's task space (242 tasks) is larger and more scalable than prior work while keeping per-task rubrics, and many tasks run under strong resource/time constraints, testing understanding rather than blind copying and necessitating inventiveness bridging towards innovative research.
- Recent AI Scientist systems rely on hard-coded test-time scaling (in-context learning, evolutionary search, tree search, test-time training), which is limited by designer biases (Sutton, 2019); self-modification (Schmidhuber, 1993; Kirsch & Schmidhuber, 2022) relaxes this but more recent LLM works keep fixed weights.
- The paper's approach — Faraday as a single agent inside a container with a coding agent as a tool (CAT), post-trained at scale across 242 tasks with GRPO extended to long-horizon, non-verifiable tasks — draws on large-scale multi-turn RL without language models (Team et al. 2021, 2023): training on a vast, smooth, diverse task distribution yields an agent that generalises out of distribution without a test-time reward.

---

## Rewards for AI Scientists

Scientific research is an underspecified problem: it is context-dependent, admits many different kinds of solutions, and judgement of its quality is subjective. Automating research is a longstanding goal, often pursued by moving pieces of the research loop inside a learning algorithm:

- the **update rule** (Schmidhuber, 1987; Bengio et al., 1992),
- the **objective** (Kirsch et al., 2020; Oh et al., 2020), or
- the **learning algorithm in its entirety** (Real et al., 2020; Kirsch et al., 2022).

These works generally assume a well-defined reward signal against which the meta-learned component can be scored. Such a signal is hard, if not impossible, to define for the broad goal of scientific research. Nevertheless, to train AI Scientist agents, it is convenient to compress their behaviour into a scalar-valued reward. There are at least two natural ways to produce such a reward: **(a)** derive a verifiable reward function from existing benchmarks, or **(b)** judge agent behaviour qualitatively using an LLM.

### (a) Verifiable benchmark rewards

This method is particularly effective when hill-climbing an existing benchmark entails a novel and valuable insight, as was the case for the problems under investigation by **FunSearch** (Romera-Paredes et al., 2024) and **AlphaEvolve** (Novikov et al., 2025). The success of such algorithms has spurred much work creating hill-climbable benchmarks for discovery, including:

- in toy settings (Majumder et al., 2024),
- from Kaggle competitions (Chan et al., 2025; Qiang et al., 2025), and
- based on *in silico* scientific research (Huang et al., 2024; Chen et al., 2025; Nathani et al., 2025; Wijk et al., 2025; Zhao et al., 2025; Rank et al., 2026; Lupidi et al., 2026).

However, this approach suffers a **critical limitation**: the innovations that agents uncover do not tend to be generalisable — they are **adaptations but not exaptations** (Gould & Vrba, 1982). There is a ceiling on what can be achieved within this paradigm; indeed, almost no prerequisite to any truly great invention was conceived with that invention in mind (Secretan et al., 2008; Stanley & Lehman, 2015). Moreover, considerable human labour was required to construct the aforementioned benchmarks, limiting their scalability for large-scale model training. **Goldie et al. (2026)** try to resolve both problems by automatically generating a combinatorially huge space from a modest set of hand-designed components, and by explicitly testing generalisation with a meta-train/test split — however, in time, similar problems will emerge at the meta level.

### (b) LLM judgement of agent rollouts

The paper therefore adopts the latter strategy: post-hoc judgement of agent rollouts by an LLM. A few prior works employ this approach with the aim of automating research paper generation end-to-end (Lu et al., 2024; Weng et al., 2025; Schmidgall et al., 2025). In these works, the judges mirror **peer review**, a highly underspecified setting with minimal ground truth and considerable noise. In contrast, the paper's **rubric judge** evaluates a more modest, controlled and grounded setting, in which agreement with humans can more easily be established: **paper replication**.

## Replication tasks for AI Scientists

Existing replication benchmarks differ in how much of the original work the agent is handed, trading off **ease of evaluation** with **construct validity** — how faithfully they measure replication (Cronbach & Meehl, 1955; Bean et al., 2026):

| Benchmark | What the agent is given | Grading |
|---|---|---|
| Hu et al. (2025) | A finished reproduction | Score only |
| Alizadeh et al. (2026); Siegel et al. (2026) | The authors' code | Run it, answer paper questions |
| Hua et al. (2025); Kon et al. (2025) | Reference implementation with parts masked out | Unit tests |
| Xiang et al. (2025) | Reference implementation with parts masked out | Code similarity |
| Yan et al. (2025) | Reference implementation with parts masked out | A judge |
| Kim et al. (2025) | — | Sweeps this spectrum directly |

This paper **sits at the latter end**, where the agent is given the **paper** and graded by a **judge**, similar to Starace et al. (2025); Gaddipati et al. (2026); Qiu et al. (2026); Huang et al. (2026). The closest prior work is **Zhao et al. (2026)** and **Seo et al. (2026)**, who also work from the paper against a human-calibrated judge. The paper extends this line of work by introducing a **larger and more scalable task space**, while maintaining the benefits of a **per-task rubric** (Cook et al., 2024; Goel et al., 2025; Gunjal et al., 2025; Viswanathan et al., 2026; Shen et al., 2026; Hong et al., 2026). Additionally, many of its tasks require the agent to replicate findings under **strong resource and time constraints**, testing understanding of the method as opposed to blind copying, and necessitating an inventiveness that bridges towards innovative research.

In concurrent work, **Liu et al. (2026)** introduce a complementary task space, extracting a paper's claims and judging each against the evidence from agent-generated experiments across **65 papers** spanning computer science, social science, medicine, and astrophysics.

## Training AI Scientists

Given a static reward function for discovery, many recent AI Scientist systems have pursued **test-time scaling**, typically relying on one or more of:

- **in-context learning** (Yang et al., 2024),
- **evolutionary search** (Lehman et al., 2023; Lange et al., 2025; Hambardzumyan et al., 2026),
- **tree search** (Jiang et al., 2025; Toledo et al., 2025; Inoue et al., 2025), or
- **test-time training** (Surina et al., 2025; Weng et al., 2025; Yang et al., 2026).

The test-time improvement algorithm in these works is **hard-coded** (even if only on the meta level), and thus limited by the biases of the designer (Sutton, 2019). **Self-modification** relaxes this constraint (Schmidhuber, 1993; Kirsch & Schmidhuber, 2022), although more recent LLM-based works retain the strictures of fixed language model weights (Zelikman et al., 2023; Zhang et al., 2026a; Wang et al., 2025; Zhang et al., 2026b).

Other works decompose the scientific method as a **hand-designed system of agents** with different roles and affordances (Tang et al., 2025; Gottweis et al., 2025; Ghafarollahi & Buehler, 2025; Ghareeb et al., 2026), benefiting from specialisation and division of labour. However, these modular architectures are somewhat **brittle and reductive**, and each agent has a restrictive interface, constraining the exploration space in a potentially unhelpful way. This paper proposes a more flexible setup, in which **Faraday is an agent within a containerd container, equipped with a coding agent as a tool (CAT)**. The CAT paradigm extends that of Su et al. (2025); Nielsen et al. (2026) — in which a smaller model is post-trained to use larger models as tools — to the setting where a tool is a **frontier coding agent in its standard CLI harness**.

Unlike previous works, this paper **post-trains Faraday at scale across a space of 242 tasks**, drawing on the ability of neural networks to generalise, yielding an AI Scientist that can effectively conduct rigorous science **out of distribution and without a test-time reward**. This approach draws inspiration from **large-scale multi-turn RL without language models** (Team et al., 2021, 2023), which teaches that training on a vast, smooth, and diverse task distribution produces an agent that can generalise and adapt. In particular, the paper succeeds at extending **GRPO** (Shao et al., 2024) post-training to **long-horizon, non-verifiable tasks**, a regime known to suffer from instability (Xu et al., 2025b; Wang et al., 2026; Kim et al., 2026). Previous works have used rubric-based judges to generate rewards for multi-turn RL in long-form question-answering (Li et al., 2026; Shao et al., 2025) but not for such long-horizon tasks, and not in such a complex environment. **Xie et al. (2026)** introduce turn-level credit assignment weights from an LLM judge that are similar in spirit but different in formulation, and report **negative results**.

**Covers:** Section 2 "Related work" of arXiv 2608.13331v1 (pages 3–4), sub-sections "Rewards for AI Scientists", "Replication tasks for AI Scientists", and "Training AI Scientists".
