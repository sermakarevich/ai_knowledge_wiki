> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Discussion

**In one sentence:** Replication is the first step in a curriculum of increasing underspecification towards innovation, and the small trained outer agent (Faraday) demonstrates that research taste acquired in weights compounds with frontier coding models, outperforms larger frontier agents on replication, imagined-replication, and scaled-up tasks, and offers a safer, inspectable alternative to hard-coding capabilities in agent harness code.

## Key points

- Replication is reframed not as uncreative output-matching but as a process whose skills — filling in vaguely-specified details — are precisely what is needed to advance the state of the art and design novel experiments; many human researchers likewise learn to replicate before doing original work.
- On "imagined replications" — Claude Opus 4.8 generates two counterfactual variants of a figure from each of five random papers per train/test split (same claim, different dataset/environment; and different claim, same setting) — Faraday's rollouts are preferred to Codex GPT-5.5's by the rubric judge on **19 of 20 tasks**; in a weak sense Faraday not only replicates better than a frontier model but also innovates better (caveat: the judge was never validated on imagined tasks).
- A small model can be trained to direct an inner coding agent at least **two orders of magnitude larger** — a "Coding Agent as a Tool" (CAT) paradigm; skills like deciding what to investigate, scoping experiments to a budget, and judging a replication compound with frontier coding-model improvements, and one can even substitute a stronger inner tool at evaluation time for an uplift (Figure A.2).
- Embedding capabilities in weights rather than code is argued to be more flexible/generalisable long-term (an approachable alternative to harness construction), and the results demonstrate successful oversight of a more powerful model by a less powerful one, with open-weights reasoning traces inspectable unlike a closed API surface.
- Moving away from well-specified tasks with verifiable rewards may reduce exposure to reward-hacking incentives during post-training, because judging entire rollouts in hindsight is a moving target, whereas a foresight-specified verifiable reward is a fixed manipulation target; Faraday is observed acting with greater scientific rigour and faithfulness than frontier agents.
- Faraday generalises to scaled-up compute: on one figure from each of eight papers estimated to need fewer than **8 hours** and **8 B300 GPUs**, Faraday exceeds Claude on average and in **5 of 8 tasks**.
- Real-world validation: authors of four corpus papers (Rupp et al. 2012; Gómez-Bombarelli et al. 2018; Reed et al. 2022; Lu et al. 2024) were "impressed by parts of the replication", the agent's "inventiveness", and fidelity (e.g., "the agent's implementation more closely follows equation (1) in the paper"), while also flagging poor simplifications ("the problem selected is probably too easy"), bad write-up ("paragraph on pre-training dataset design is particularly bad"), and code slop ("calculations contain unnecessarily convoluted code").
- The conclusion: we have built an "intelligence layer with a modicum of research taste, sufficient to extend the capabilities of frontier agents" — the tip of the iceberg, and moving from replication to innovation further sharpens the underspecification problem and the need for systems with good judgement.

---

## Towards innovation

Replicating a figure from a paper is, on the face of it, not a creative endeavour — the output looks like the original. But examining the *process* rather than the output reframes replication as a stepping stone towards innovation: the ability to fill in vaguely-specified details may be the very same skill needed to design one's own experiments and advance the state of the art (Deutsch 2011; Muthukrishna & Henrich 2016; Heyes 2018; Bhoopchand et al. 2023). Humans likewise start careers by replicating before going original. **Replication is the first step in a curriculum of increasing underspecification towards innovation.**

Inspired by this, the authors assess how Faraday generalises to "imagined replications" (Figure 5, right panel). Claude Opus 4.8 generates two variants of five randomly selected papers from each of the Replica train and test splits: (a) the same claim but a different dataset or environment, and (b) a different claim in the same setting (Appendix F.3). Faraday and Codex GPT-5.5 are evaluated; the task interface is unchanged and scoring uses the rubric judge. **Faraday's rollouts are preferred to Codex's on 19 of the 20 tasks.** In a weak sense, Faraday innovates better than a frontier model, but the authors caution the judge was never validated on imagined tasks — future validation is warranted.

![Figure 5 — technical summary: rubric-judge scores for baseline Codex, prompt-optimised Codex, and Faraday on ML (train) and AI-for-science (test) splits (left), and per-task (right), where Faraday leads on the original and counterfactual/imagined tasks.](images/fig5.png)

The right panel of Figure 5 captures exactly these imagined/counterfactual variants: Faraday is at or above Codex in almost every task, with the advantage widening on several test-split tasks — evidence that its advantage comes from post-training rather than prompting.

## Coding agent as a tool (CAT)

It is perhaps surprising that a small model can be trained to better direct a coding agent at least **two orders of magnitude larger**. Training the outer agent need not be prohibitively expensive in inference tokens for the inner tool: after training with a *weaker* coding agent as a tool, one can substitute a more powerful agent at evaluation time and achieve a performance uplift (Figure A.2). The skills Faraday acquires — deciding what to investigate, scoping experiments to a budget, judging a replication — compound with advances in frontier coding models, so a single post-trained outer agent might track the frontier as better models are released, at least over some time period. The optimal cost–benefit tradeoff between inner and outer agent sizes is left as open work.

The CAT paradigm has implications for capabilities and safety:

- **Capabilities:** an approachable alternative to harness construction; encoding capabilities in weights rather than code is, historically, more flexible and generalisable in the long run.
- **Safety:** results demonstrate successful oversight of a more powerful model by a less powerful one (Amodei et al. 2016; Bowman et al. 2022; Kenton et al. 2024), and the reasoning traces of an open-weights model are inspectable, unlike those behind a closed-weights API surface.
- Nothing requires the outer agent to remain the smaller model — whether scientific judgement must match or exceed the cost of engineering execution in the long run is an empirical question.

## Beyond verifiable rewards

To capture the abilities underlying open-ended research, the authors necessarily move away from well-specified tasks with verifiable rewards. A side effect may be lower exposure to **reward hacking** during post-training (Baker et al. 2025): defining a verifiable reward requires specifying the evaluation procedure in *foresight*, turning it into a fixed target for manipulation; judging entire rollouts in *hindsight* is a moving target. Faraday is observed to act with greater scientific rigour and faithfulness than frontier agents — completing tasks as intended rather than reproducing figures performatively. Whether open-ended training scalably ameliorates reward hacking remains open.

## Generalisation

In training, scope is deliberately limited to short horizons and limited GPUs — first for RL throughput per unit wall-clock time, and second because the ability to experiment quickly with minimal versions of research ideas is a valuable transferable skill. To test generalisation to larger resources, the authors select one figure from each of **eight papers** whose replication was estimated to require fewer than **8 hours** and **8 B300 GPUs**, provide Faraday and Claude Opus 4.8 with appropriate resources, and evaluate (Appendix A.1). **Faraday exceeds Claude on average and in 5 of the 8 tasks**, suggesting generalisation. Stronger claims would require clearer validation of the rubric judge on larger-scale tasks and more of such tasks; scaling is further discussed in the supplementary discussion (Appendix E).

## Community engagement

Paper replication is a public good, strengthening scientific foundations; progress is particularly timely because the paper review system is beginning to strain under AI-assisted research (Gartenberg et al. 2026), and high-quality replication tools may help ground AI-assisted reviewing. The authors invite users at faraday@inherentlaboratories.com.

As an early step in real-world validation, they obtained feedback from the authors of **four papers** in the Replica task space (Rupp et al. 2012; Gómez-Bombarelli et al. 2018; Reed et al. 2022; Lu et al. 2024) on Faraday's replication of one of their figures:

- **Positive:** "part b and c look very good"; "the reflexion implementation looks correct"; praise for the agent's inventiveness ("nice and clever toy task design") and fidelity ("the agent's implementation more closely follows equation (1) in the paper").
- **Negative:** some simplifications made no sense ("the problem selected is probably too easy"), parts of the write-up were poor ("paragraph on pre-training dataset design is particularly bad"), and code slop was off-putting ("calculations contain unnecessarily convoluted code").

## Conclusion

The authors have created an **intelligence layer with a modicum of research taste, sufficient to extend the capabilities of frontier agents**. This is "the tip of the iceberg" for imbuing agents with the ability to enrich scientific research as peer collaborators with humans. Stepping from replication towards innovation sharpens the problem of underspecification and deepens the need for systems with good judgement; cultivating creative human–machine teams ultimately requires AI taste in code, experiments, theories, collaboration, and organisational design.

## Ethics statement

- **Awareness of limitations.** AI paper replication is early-stage: though Faraday successfully replicated claims from many papers, it failed in several cases with confidence the original result was rigorous and honestly reported. None of Faraday's failures on published work is claimed to indicate fundamental problems with the original research, and humans must keep cultivating replication skills and inspecting agent results even as AI judges become reliable.
- **Human studies.** The authors assessed whether their human data collection required external board review and concluded it did not, since the elicited information was only professional judgement, without sensitive personal data and with no participant risk. Participants were a mix of pre-existing professional networks and third-party data-provider experts; purpose was disclosed and compensation was paid irrespective of whether ratings cleared internal filtering.
- **Conflict of interest.** Some corpus papers were written by authors of this paper or people they know personally, and some work comes from institutions whose commercial models they used; the same automated pipeline was applied to all corpus items, with no altered scoring treatment for their own or acquaintances' prior work.
- **Technical safety.** Not all scientific applications benefit society; these capabilities could empower malicious actors or increase misalignment risk. The authors selected **in silico** tasks judged unlikely to cause harm, constrained Faraday in time and compute, gave it no access to physical lab equipment, though it did have internet access.

## Acknowledgements

The authors thank Shi Dong, Alex Goldie, Matt Henderson, Akarsh Kumar, Chris Lu, Clare Lyle, and Jimmy Secretan for comments on an early draft; and Sergio Gomez, José Miguel Hernández-Lobato, Chris Lu, and Matthias Rupp for feedback on the quality of replication of their papers.

**Covers:** Section 5 Discussion (Towards innovation; Coding agent as a tool (CAT); Beyond verifiable rewards; Generalisation; Community engagement) plus the paper's Conclusion, Ethics statement, and Acknowledgements.
