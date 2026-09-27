> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# References and Appendix Opening: Benchmark Construction Details
**In one sentence:** This chunk lists references [38]–[52] and opens Appendix A with the source trajectory pools, mined-fork statistics and validation rules, and the generator prompts used to build the benchmark.
## Key points
- Engineering trajectories come from 2,677 graded rollouts on 517 tasks from 11 repositories, produced by GPT-5.4 and GPT-5.5 agents in 31 runs between April and July 2026 on SWE-bench Pro.
- Research trajectories come from MALT/METR with 1,132 runs on 47 tasks from RE-Bench and HCAST, produced by Claude 3.5 Sonnet, Claude 3.7 Sonnet, Claude Sonnet 4, Claude Opus 4, and DeepSeek V3 agents.
- Detour construction input was 896 trajectories in a first pass plus 437 further trajectories in a second pass; parallel construction input was 600 pairs of opposite-outcome attempts, retained from 905 candidate pairs after exclusions.
- Released parallel engineering cell has 111 of 124 pairs contrasting same-model attempts and 13 contrasting GPT-5.5 vs GPT-5.4; all 48 research parallel pairs contrast same-model attempts.
- Detour forks require four verbatim excerpts in order (abandoned-direction commit, observed failure, recovery commit, recovery success) plus a failure signal such as non-zero exit code or error message, with mechanical discarding on any failed check.
- Parallel pairs are formed within a task between one passing and one failing attempt with at most eight pairs per task, pairing same-model/same-reasoning-setting attempts first.
- The generator is GPT-5.6 Sol at high reasoning effort, returning one JSON object per candidate fork, with separate parallel and detour prompts ending in the rubric requirements.
---
## References [38]–[52]
- [38] Peiyi Wang, Lei Li, Zhihong Shao, Runxin Xu, Damai Dai, Yifei Li, Deli Chen, Yu Wu, and Zhifang Sui. Math-shepherd: Verify and reinforce LLMs step-by-step without human annotations. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics, 2024.
- [39] Yifan Song, Da Yin, Xiang Yue, Jie Huang, Sujian Li, and Bill Yuchen Lin. Trial and error: Exploration-based trajectory optimization of LLM agents. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics, 2024.
- [40] Mukai Li, Qingcheng Zeng, Tianqing Fang, Zhenwen Liang, Linfeng Song, Qi Liu, Haitao Mi, and Dong Yu. Verified critical step optimization for LLM agents. In Findings of the Association for Computational Linguistics: ACL 2026, 2026.
- [41] Hyungjoo Chae, Seonghwan Kim, Junhee Cho, Seungone Kim, Seungjun Moon, Gyeom Hwangbo, Dongha Lim, Minjin Kim, Yeonjun Hwang, Minju Gwak, et al. Web-shepherd: Advancing PRMs for reinforcing web agents. In Advances in Neural Information Processing Systems, 2025.
- [42] Mingchen Zhuge, Changsheng Zhao, Dylan R. Ashley, Wenyi Wang, Dmitrii Khizbullin, Yunyang Xiong, Zechun Liu, Ernie Chang, Raghuraman Krishnamoorthi, Yuandong Tian, Yangyang Shi, Vikas Chandra, and Jürgen Schmidhuber. Agent-as-a-judge: Evaluate agents with agents. In International Conference on Machine Learning, 2025.
- [43] Xing Han Lù, Amirhossein Kazemnejad, Nicholas Meade, Arkil Patel, Dongchan Shin, Alejandra Zambrano, Karolina Stańczak, Peter Shaw, Christopher J. Pal, and Siva Reddy. AgentRewardBench: Evaluating automatic evaluations of web agent trajectories. In Conference on Language Modeling, 2025.
- [44] Shaokun Zhang, Ming Yin, Jieyu Zhang, Jiale Liu, Zhiguang Han, Jingyang Zhang, Beibin Li, Chi Wang, Huazheng Wang, Yiran Chen, and Qingyun Wu. Which agent causes task failures and when? on automated failure attribution of LLM multi-agent systems. In International Conference on Machine Learning, 2025.
- [45] Guibin Zhang, Junhao Wang, Junjie Chen, Wangchunshu Zhou, Kun Wang, and Shuicheng Yan. AgenTracer: Who is inducing failure in the LLM agentic systems? In International Conference on Learning Representations, 2026.
- [46] Geoffrey Hinton, Oriol Vinyals, and Jeff Dean. Distilling the knowledge in a neural network. arXiv preprint arXiv:1503.02531, 2015.
- [47] Amanda Askell, Yuntao Bai, Anna Chen, Dawn Drain, Deep Ganguli, Tom Henighan, Andy Jones, Nicholas Joseph, Ben Mann, Nova DasSarma, et al. A general language assistant as a laboratory for alignment. arXiv preprint arXiv:2112.00861, 2021.
- [48] Charlie Snell, Dan Klein, and Ruiqi Zhong. Learning by distilling context. arXiv preprint arXiv:2209.15189, 2022.
- [49] Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah D. Goodman. STaR: Bootstrapping reasoning with reasoning. In Advances in Neural Information Processing Systems, 2022.
- [50] Sanjiban Choudhury and Paloma Sodhi. Better than your teacher: LLM agents that learn from privileged AI feedback. In International Conference on Learning Representations, 2025.
- [51] Rishabh Agarwal, Nino Vieillard, Yongchao Zhou, Piotr Stanczyk, Sabela Ramos, Matthieu Geist, and Olivier Bachem. On-policy distillation of language models: Learning from self-generated mistakes. In International Conference on Learning Representations, 2024.
- [52] Parth Asawa, Alan Zhu, Abigail O'Neill, Matei Zaharia, Alexandros G. Dimakis, and Joseph E. Gonzalez. How to train your advisor: Steering black-box LLMs with advisor models. In International Conference on Machine Learning, 2026.

## A Benchmark Construction Details
This appendix supplements Section 3 with the source data, the statistics of the mined forks, the prompts of the generator and the judges, and the counts at each stage of the construction.

## A.1 Source trajectories
- Engineering pool: 2,677 graded rollouts on 517 tasks from 11 repositories, from GPT-5.4 and GPT-5.5 agents in 31 runs between April and July 2026 on SWE-bench Pro; test result of each attempt is recorded.
- Research pool: MALT public transcript release of METR, keeping only runs with native score recorded: 1,132 runs on 47 tasks from RE-Bench and the research subset of HCAST, from Claude 3.5 Sonnet, Claude 3.7 Sonnet, Claude Sonnet 4, Claude Opus 4, and DeepSeek V3 agents.
- Detour inputs: 896 trajectories in a first pass and 437 further trajectories in a second pass.
- Parallel inputs: 600 pairs of attempts with opposite outcomes, remaining from 905 candidate pairs after excluding pairs whose scores are not comparable or whose combined transcript exceeds the generator context.

## A.2 Statistics of the mined forks
- Parallel pairing: within a task between one passing and one failing attempt, at most eight pairs per task; attempts by the same model under the same reasoning setting paired first.
- Generator reads both full attempts and locates the decision point in each, so the two candidates describe actual actions at comparable points; question prefix is the supported attempt's part before its decision point.
- Released engineering parallel cell: 111 of 124 pairs same-model contrasts; remaining 13 contrast GPT-5.5 with GPT-5.4. Research cell: all 48 pairs same-model contrasts.
- Detour fork placement: step right before the agent takes the abandoned direction; generator must cite four excerpts in order: (1) step committing to abandoned direction, (2) observed failure after which agent abandons it, (3) step committing to recovery, (4) evidence recovery succeeds.
- Detour validation: each excerpt must appear verbatim in the cited step, four steps must appear in order, and cited failure must contain a failure signal such as non-zero exit code or error message; candidate failing any check is discarded mechanically.
- Prefix rendering: prefix rendered from trajectory steps before the fork; Appendix C describes rendering.

Table 1 Size of the released questions per cell. Steps is the number of trajectory steps before the fork, and words is the number of words in one candidate.

| Cell | Questions | Tasks | Trajectories | Steps (median) | Steps (10th–90th) | Words (median) |
|---|---|---|---|---|---|---|
| Parallel engineering | 124 | 62 | 120 | 35 | 21–57 | 38 |
| Parallel research | 48 | 8 | 32 | 56 | 6–132 | 27 |
| Detour engineering | 266 | 133 | 266 | 47 | 24–71 | 23 |
| Detour research | 64 | 22 | 64 | 30 | 3–81 | 22 |

## A.3 Prompts of the generator and the judges (opening)
- Generator is GPT-5.6 Sol at high reasoning effort; receives one prompt per candidate fork and returns one JSON object; parallel and detour constructions use different prompts.
- Parallel prompt receives the task, the outcome of each attempt, and the two complete attempts. Detour prompt receives the task, the outcome of the run, and the complete trajectory. Both prompts end with the requirements that the main text calls the rubric.
- Parallel generator system message (verbatim): "You build parallel judgment benchmark items from real agent trajectories. Return one JSON object only. Ground every decision point and option in the supplied trajectories. Do not invent grader evidence or use prior benchmark labels. Treat rejection as a correct and preferred result whenever a clean causal fork cannot be demonstrated from exact post-decision evidence."
- Parallel generator user-message goal (verbatim): "Find one genuine decision fork where the branch with the better native outcome made a better task-solving decision than the worse branch. Locate the decision in the raw trajectories and write two neutral, parallel candidate next steps."
- Rejection rule (verbatim): "Reject the candidate if the outcome difference is mostly a typo, crash, luck, missing dependency, or generic execution quality rather than the chosen approach."

**Covers:** References [38]–[52]; Appendix A opening through A.3 parallel-generator goal and Required JSON lead-in
