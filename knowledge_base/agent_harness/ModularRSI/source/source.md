# ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement
Source: https://arxiv.org/pdf/2609.14857
Kind: pdf
Fetched: 2026-09-21T05:38:31.920661+00:00
Tool: pdftotext

                                         M ODULAR RSI: M ODULAR AND G ENERALIZABLE R E -
                                         CURSIVE H ARNESS S ELF -I MPROVEMENT

                                          Siwei Wu2,3,* , Jincheng Ren4,6,* , Yizhi Li3,† , Haau-Sing Li3 , Chengran Yang3 , Yuxuan
                                          Zhang3 , Weicheng Gu3 , Jian Yang1,‡ , Riza Batista-Navarro2 , Chuanyi Zhang6 ,
                                          Xianglong Liu1 , Ming Zhou5 , Bryan Dai3 , Chenghua Lin2,‡
                                          1
                                           Beihang University, 2 University of Manchester, 3 IQuest Research,
                                          4
                                           M-A-P, 5 Langboat, 6 Hohai University
                                          {siwei.wu-2@postgrad., chenghua.lin@}manchester.ac.uk




arXiv:2609.14857v1 [cs.CL] 14 Sep 2026
                                                                                   A BSTRACT
                                                 Recent work extends Recursive Self-Improvement (RSI) to agent harnesses for
                                                 long-horizon coding and terminal tasks, enabling agents to improve their execu-
                                                 tion mechanisms from experience. However, achieving and demonstrating gen-
                                                 eralizable harness RSI remains challenging. First, existing approaches often
                                                 evolve harnesses directly on evaluation benchmarks or subsets drawn from them,
                                                 making it difficult to distinguish reusable harness improvements from benchmark-
                                                 specific adaptation. Second, updates derived from individual trajectories can en-
                                                 tangle systematic harness deficiencies with instance-specific reasoning and solu-
                                                 tion details, leading to task-specific modifications that transfer poorly to unseen
                                                 tasks. Third, even when recurring behavioral deficiencies are identified, local-
                                                 izing them to the responsible components within a monolithic harness remains
                                                 difficult. Whole-harness optimization can therefore entangle unrelated mecha-
                                                 nisms and produce changes that are difficult to attribute and validate. We pro-
                                                 pose ModularRSI, a benchmark-disjoint, contrastive, and modular framework
                                                 for generalizable harness evolution. ModularRSI contrasts successful and failed
                                                 trajectories for the same task and aggregates evidence across tasks to identify re-
                                                 curring behavioral deficiencies. It further decomposes the evolvable harness into
                                                 five functional modules: Agent Loop, Tool Use, Observation Management, Con-
                                                 text Management, and Task Completion Detection. Each module is evolved inde-
                                                 pendently within a restricted modification scope, after which an integration stage
                                                 combines the evolved modules into a unified harness and resolves potential con-
                                                 flicts among them. To evaluate generalization beyond evolution experience, we
                                                 additionally curate 2,000 executable evolution tasks from external data sources
                                                 that are disjoint from downstream evaluation benchmarks. Experiments on Ter-
                                                 minalBench 2.0 and SWE-Bench Verified show consistent improvements on un-
                                                 seen in-domain and cross-domain tasks, with the evolved harness also transfer-
                                                 ring across different foundation models. All our code and datasets are available at
                                                 https://github.com/IQuestLab/ModularRSI.


                                         1    I NTRODUCTION
                                         CLI agents have achieved remarkable performance on complex software engineering and terminal-
                                         based tasks (Jimenez et al., 2024a; Deng et al., 2025; Merrill et al., 2026b; Hong et al., 2026).
                                         Beyond foundation models, their effectiveness increasingly depends on agent harnesses that gov-
                                         ern execution, tool interaction, context management, and environment feedback. Recent work has
                                         therefore explored recursive self-improvement (RSI) of harnesses, allowing agents to refine these
                                         mechanisms from execution experience.
                                         However, achieving generalizable harness RSI remains challenging because task-level outcomes
                                         provide only coarse supervision for harness evolution. We identify three coupled challenges. First,
                                         there is a data-level challenge in obtaining high-quality evolution experience. Harness RSI re-
                                         quires executable long-horizon terminal tasks with reliable environments and correctness feedback,


                                                                                         1
but constructing such an evolution dataset at sufficient scale and diversity is costly and difficult.
Although recent work has explored automatically generating terminal-related instances, ensuring
their environment completeness, task validity, and evaluator reliability at scale remains challenging,
limiting the availability of high-quality data for Harness RSI (Pi et al., 2026; Wu et al., 2026a). Con-
sequently, existing Harness RSI methods typically rely on data from downstream benchmarks for
evolution (Lee et al., 2026; Lin et al., 2026; Du et al., 2026; Chen et al., 2026a; Pan et al., 2026; Luo
et al., 2026a; Nguyen et al., 2026) , which makes it difficult to determine whether the evolved har-
ness captures generalizable improvements or merely adapts to benchmark-specific patterns. Second,
there is a trajectory-level ambiguity in identifying what should be improved. Individual or one-
sided execution trajectories entangle systematic harness deficiencies with task-specific reasoning
and solution details. Optimizing directly from such evidence may therefore introduce task-specific
behaviors that transfer poorly to unseen tasks. Third, there is a mechanism-level credit-assignment
problem: even when a recurring behavioral deficiency is identified, it remains unclear which har-
ness component should be modified. Although some recent work explores localized diagnosis and
repair (Chen et al., 2026a), many approaches still optimize or rewrite large portions of the har-
ness (Lin et al., 2026; Zhang et al., 2026a; Lee et al., 2026; Pan et al., 2026). This large modification
space can entangle unrelated mechanisms, making targeted and reliable evolution difficult.
To address these challenges, we propose ModularRSI, a contrastive and modular credit-
assignment framework for harness self-evolution. ModularRSI translates coarse task-level out-
comes into localized harness evolution signals by contrasting successful and failed trajectories and
aggregating evidence across tasks to identify recurring behavioral deficiencies. To further localize
these deficiencies, we decompose the evolvable harness into five functional modules: Agent Loop,
Tool Use, Observation Management, Context Management, and Task Completion Detection. Each
module is evolved independently within a restricted modification scope, and the resulting improve-
ments are subsequently integrated into a unified harness. This design reduces both task-specific
adaptation and interference across unrelated harness mechanisms.
To evaluate whether these improvements generalize beyond the evolution experience, we further
establish a benchmark-disjoint evolution protocol with 2,000 independently curated executable
tasks that are fully disjoint from downstream evaluation benchmarks. The evolved harness is frozen
before evaluation, and proposed modifications are retained only after validation for correctness,
executability, and task-specific overfitting.
Our main contributions are summarized as follows:

      1. We propose ModularRSI, a contrastive and modular framework that addresses the credit-
         assignment problem in harness self-evolution. By combining same-task trajectory contrast,
         cross-task evidence aggregation, and module-restricted evolution, ModularRSI converts
         coarse task-level outcomes into localized harness modification signals while reducing task-
         specific and cross-mechanism interference.
      2. We establish a benchmark-disjoint evolution protocol for evaluating generalizable Har-
         ness RSI. We independently curate 2,000 executable evolution tasks from external data
         sources and apply instance-level similarity filtering and fine-grained domain analysis to
         minimize overlap with downstream benchmarks, providing a standardized evolution re-
         source for studying transferable harness improvements.
      3. We extensively evaluate ModularRSI on TerminalBench 2.0 and SWE-Bench Verified.
         The evolved harness consistently improves performance on unseen in-domain and out-of-
         domain tasks and transfers across different foundation models. Our controlled studies fur-
         ther show that independently evolving and merging harness modules substantially outper-
         forms joint or non-modular evolution, while different modules contribute complementary
         improvements to execution reliability and interaction efficiency.


2     R ELATED W ORK
2.1   AGENT H ARNESSES AND S ELF -I MPROVEMENT

Alongside advances in coding models such as LoopCoder and IQuest-Coder-V1 (Yang et al.,
2026b;a), executable environments and verified trajectories provide scalable signals for agent im-


                                                   2
                                                Modular Whole-Harness     Not Use
           Method
                                                Evolution Evolution   Benchmark Data
           AutoHarness (Lou et al., 2026b)         ✗           ✗                 ✗
           Meta-Harness (Lee et al., 2026)         ✗           ✓                 ✗
           AHE (Lin et al., 2026)                  ✗           ✗                 ✗
           Self-Harness (Zhang et al., 2026a)      ✗           ✗                 ✗
           RHO (Pan et al., 2026)                  ✗           ✗                 ✗
           HarnessFix (Chen et al., 2026a)         ✓           ✗                 ✗
           Living-Harness (Du et al., 2026)        ✓           ✗                 ✗
           HarnessForge (Chen et al., 2026b)       ✓           ✓                 ✗
           HarnessBank (Luo et al., 2026a)         ✓           ✓                 ✗
           RSEA (Nguyen et al., 2026)              ✓           ✗                 ✗
           TACO (Ren et al., 2026)                 ✗           ✗                 ✗
           ModularRSI (Ours)                       ✓           ✓                 ✓

Table 1: Comparison of representative self-evolving agent and harness frameworks. Do Not
Use Benchmark Data indicates whether benchmark instances, trajectories, or benchmark-derived
rewards are excluded from harness evolution.


provement (Wu et al., 2026a; Gandhi et al., 2026; Cheng et al., 2026). Prior work uses such experi-
ence to adapt model weights (Wang et al., 2026c; Zweiger et al., 2026; Luo et al., 2026b), accumulate
reusable skills or context artifacts (Zhang et al., 2026c; Yan et al., 2026), and optimize prompts or
external agent mechanisms through trajectory feedback (Agrawal et al., 2026; Zhang et al., 2026d;
Fan et al., 2026). Other approaches use execution traces to diagnose failures and localize editable
components (Lin et al., 2026; Chen et al., 2026a), while recent work directly evolves agent imple-
mentations or synthesizes harness code (Zhang et al., 2026b; Lou et al., 2026a; Lee et al., 2026).
TACO further specializes harness evolution to observation compression for terminal agents (Ren
et al., 2026).


2.2   G ENERALIZATION IN S ELF -I MPROVEMENT

A central challenge in self-improvement is distinguishing transferable improvements from adapta-
tion to the development data. Data selection therefore matters: source-aware rubrics and shortcut
filtering help ensure that learning signals reflect the intended capability (Wang et al., 2026a; Zhang
et al., 2026e). Existing evaluations cover repository repair, terminal interaction, and online work-
flows (Deng et al., 2025; Merrill et al., 2026a; Zhang et al., 2026f), while HarnessDev and broader
studies explicitly examine harness evolution, feedback budgets, and held-out generalization (Wu
et al., 2026b; Wang et al., 2026b). Aspire studies weight and harness evolution under hidden evalu-
ation (Wu et al., 2026c), and S3 Gym separates self-testing, self-judging, and improvement through
history, memory, or parameter updates (Shi et al., 2026).
Despite these advances, existing harness-evolution methods often rely on data drawn from evaluation
benchmarks or treat the harness as a monolithic whole, leaving broadly generalizable, fine-grained
harness improvement underexplored. To address these limitations, we construct a benchmark-
disjoint evolution dataset and propose ModularRSI, which decomposes the harness into functional
modules and performs self-evolution through contrastive trajectory analysis.


3     M ETHOD

Existing harness self-evolution methods face a fundamental credit-assignment problem: task-level
rewards indicate whether an execution succeeds or fails, but provide limited guidance on which
harness mechanisms are responsible and how they should be improved. To address this challenge,
we propose ModularRSI, which decomposes the behavioral components of a harness into indepen-
dently evolvable modules and uses contrastive trajectory analysis to translate task-level outcomes
into localized function-level evolution signals.


                                                    3
                                           Contrastive Trajectory Sampling and Analysis


                                                                                                                      Contrastive Efficiency
                                                            Positive
                                                             Group
                                                                         …             Single
                                        Rolling                      R=1        R=1                            R=1
                                                           Contrastive                          R=1
                                                             Group          …
                                                                      R=1       R=0


                                                                                                                                   Analysis
                                                                            …
                                                                                                                       Analysis
                                   Task-Aware              Negative                                                                            findings
                                                                                                            R=1
                        Function
                                    Function
                                              Trajectory     Group
                                                                      R=1       R=0
                                                                                       Pair       R=0
              Harness    Merge                 Memory
                                   Composer
                                                                                                R=0      R=1


                    Module-wise Harness Modification                                            Validation Gate
                                                                                                 Execution Validation
                                                                                                                      accept
                                                                                      Harness                         roll back
              Observation Tool Use Context   Agent           Task                                       Sandbox
              Management          Management Loop          Completion
                                                                                Program Verification                  Diff Review
                                          Code-Modify Agent                                                                        overfit
                             Retrieve      Record                                                      accept
                                                                                                                                                general
                                     Evolution History                                                roll back function’s diff




Figure 1: Overview of ModularRSI. The framework collects and analyzes contrastive trajectories,
performs module-wise harness modification, and retains modifications through validation gates.

3.1   OVERVIEW OF M ODULAR RSI

As illustrated in Fig. 1, ModularRSI consists of three stages: (i) Contrastive Trajectory Sampling
and Analysis, which identifies recurring harness weaknesses from successful and failed execu-
tions; (ii) Module-wise Harness Evolution, which converts these findings into localized function
updates; and (iii) Validation Gates, which filter proposed modifications through program checks,
generalization-oriented diff review, and execution validation.
Starting from a shared initial harness, we decompose its behavioral mechanisms into five functional
modules. During module-wise evolution, the modules are evolved independently without sharing
intermediate updates, allowing them to be processed in parallel. For each module, ModularRSI
analyzes trajectory evidence in batches and restricts modifications to its functional scope. The agent
under evolution itself serves as the Code-Modify Agent for both trajectory analysis and harness
modification. After all five modules have been evolved independently, we perform Cross-Module
Integration to combine the evolved modules into a unified harness and resolve potential conflicts
among their modifications.
To control the growing function library, we apply Function Merge to remove redundant func-
tions and use a Task-Aware Function Composer to activate only task-relevant functions. After
all module-level evolution is completed, the evolved modules are combined and refined through
cross-module integration. The resulting function library is then frozen for downstream evaluation.

3.2   H ARNESS M ODULARIZATION

A harness contains both infrastructure-level components and behavioral mechanisms. Since compo-
nents such as sandbox initialization, parallel execution, and LLM communication mainly concern
system infrastructure rather than task-solving behavior, ModularRSI restricts evolution to mecha-
nisms that directly mediate agent–environment interaction. Based on our analysis of existing har-
ness implementations and execution trajectories, we organize these mechanisms into five functional
modules:
1. Agent Loop. Controls the iterative reasoning–action–observation process, including execution
flow, interaction control, and recovery behavior.
2. Observation Management. Processes environmental feedback by preserving task-relevant
information while filtering or compressing noisy observations.
3. Tool Use. Manages the selection, invocation, and validation of external tools.
4. Context Management. Maintains and organizes interaction history across execution steps,
including information retention, compression, and retrieval.


                                                                     4
5. Task Completion Detection.          Determines whether the task has been completed or further
interaction is required.
Specifically, the Agent Loop coordinates the outputs of the other modules and constructs prompts for
the LLM to interact with the environment, while the remaining modules process different types of
information required during execution. Details of the interactions among modules and the function
interfaces within each module are provided in Appendix A.
We use Terminus-2 from Harbor (Merrill et al., 2026b) as the initial harness and reorganize its be-
havioral mechanisms into these five modules, which serve as the shared starting point for subsequent
module-wise evolution.

3.3   C ONTRASTIVE T RAJECTORY S AMPLING AND A NALYSIS

For each evolution instance xi , we roll out the agent K times, obtaining trajectories
(tra1i , tra2i , . . . , traK
                            i ). Each trajectory is evaluated by the task-specific evaluator and assigned
a binary reward rik , where rik = 1 indicates success and rik = 0 indicates failure. Based on the
rollout rewards, we divide tasks into three groups:

                                                            k
                                                      P
                                  Positive,             k ri
                                                           P k
                                                              = K,
                              Gi = Contrastive,        0 < k ri < K,                                 (1)
                                                      P k
                                    Negative,            k ri = 0.

We further maintain a Trajectory Memory that stores historical trajectories and their rewards for
each task across evolution epochs. This allows experience from previous epochs to provide addi-
tional contrastive evidence when the current rollouts alone are insufficient.
The Code-Modify Agent analyzes each group according to the available trajectory evidence. For the
Contrastive group, successful and failed trajectories of the same task are paired and compared to
identify function-level factors associated with different outcomes. For the Negative group, where
all current rollouts fail, the agent first queries the Trajectory Memory for a previously successful
trajectory of the same task. If one exists, it is paired with a current failed trajectory for contrastive
analysis. Otherwise, the agent performs single-sided diagnosis over the failed trajectories to identify
evident execution deficiencies, such as repetitive loops, incorrect tool usage, ineffective recovery,
or premature termination. For the Positive group, where all rollouts succeed, the analysis focuses
on opportunities to improve execution quality and efficiency, such as redundant actions, repetitive
exploration, or unnecessary tool calls.
After analyzing all tasks in a batch, the Code-Modify Agent consolidates the diagnoses into struc-
tured findings in JSON format. Each finding specifies the module under analysis, supporting tra-
jectory evidence, the rationale for or against modification, and a proposed change when applicable.
The detailed analysis prompt and output schema are provided in Appendix B and Appendix C.1.

3.4   M ODULE - WISE H ARNESS M ODIFICATION

Based on the findings identified in Sec. 3.3, we again employ the Code-Modify Agent to modify
the corresponding harness functions through two mechanisms designed to improve modification
reliability.
Modification Target Selection. For each batch, we first consolidate semantically similar diag-
noses that target the same function into candidate modifications. Each candidate is then assigned a
vote count based on the number of distinct tasks that provide supporting evidence. We prioritize the
highest-ranked candidates for subsequent evolution, favoring modifications supported across multi-
ple tasks while reducing the influence of instance-specific failures.
Evolution History. To reduce redundant or conflicting modifications and mitigate evolution os-
cillation across iterations, we maintain an Evolution History for each function being updated. The
history records previous code changes and the functionality introduced by each revision. By ex-
posing these historical changes to the Code-Modify Agent, subsequent updates can better preserve
previously evolved functionality while avoiding repeated or contradictory modifications.


                                                   5
The prompts used for harness evolution are provided in Appendix C.2.


3.5   VALIDATION G ATES

Only validated modifications are retained during evolution. After each function update, we apply a
sequence of validation gates to ensure that the modified harness remains executable and compatible
with the surrounding system.
Program Check. We first perform a series of static checks on the modified harness, including
AST validation, import checks, protocol compliance, discovery-contract verification, and static self-
attribute audits. If a modification fails any of these checks, we use the recorded diffs to roll back the
affected function to its previous version.
Diff Review. To mitigate the risk of task-specific modifications, we ask the Code-Modify Agent
to review each modification diff. The agent checks whether the introduced changes encode task-
specific solutions, heuristics, or conditions that are unlikely to generalize beyond the current training
instances. Modifications identified as overly task-specific are rejected and rolled back. The review
prompt is provided in Appendix C.3.
Execution Validation. Finally, we validate the executability of the modified harness through actual
task execution. After each modification, we randomly sample two tasks from the current batch and
execute them using the updated harness. If the modification introduces runtime errors or violates
the expected execution protocol, we use the recorded diffs to roll back the harness to its previous
version.


3.6   C ROSS -M ODULE I NTEGRATION

After the five modules have been evolved independently, their validated variants are combined into
a unified harness. Since independently optimized modules may introduce duplicated mechanisms,
conflicting behaviors, or inconsistent interactions when composed together, direct combination may
not produce a coherent final system.
We therefore perform an additional cross-module integration epoch on the evolution set. The
integrated harness is executed on evolution tasks, and the Code-Modify Agent analyzes the result-
ing trajectories to identify cross-module conflicts. It then refines module interactions by removing
duplicated mechanisms, clarifying module responsibilities, and adjusting coordination logic where
necessary.
After integration, the evolved function library is frozen and no further modifications are allowed
during downstream evaluation. The prompt used for cross-module integration is provided in Ap-
pendix C.4.


3.7   F UNCTION L IBRARY M ANAGEMENT

ModularRSI maintains an expanding library of evolved functions. We introduce two complementary
mechanisms to control its complexity: Function Merge reduces redundancy in the persistent library,
while Task-Aware Function Composition restricts the functions activated for each task.
Function Merge. Within each module, an LLM compares the descriptions and behaviors of its
functions and merges those with highly similar or overlapping functionality, reducing redundancy
while preserving their learned capabilities.
Task-Aware Function Composition. It dynamically constructs the active harness for each task.
Each evolved function is associated with a natural-language description of its current behavior.
Given the task description and the descriptions of all candidate functions, an LLM selects a sub-
set of task-relevant functions, and only these functions are activated during execution.
Those mechanisms are used during both trajectory collection and downstream evaluation. This
allows the underlying function library to expand through evolution while keeping the active harness
compact and task-specific.


                                                   6
                                       ModularRSI evolution pool — task category distribution (2000 instances)
                        (a) Category distribution by domain

    Data processing                        219                           162           381 (19.1%)   (b) Overall composition

      ML & science               104                     168            272 (13.6%)
                                                                                                                               Data processing 381 (19.1%)
         Build & deps             133                    111       244 (12.2%)
                                                                                                                               ML & science 272 (13.6%)
                                                                                                                               Build & deps 244 (12.2%)
     Systems & OS                102                134           236 (11.8%)
                                                                                                                               Systems & OS 236 (11.8%)
                                                                                                                 2000
          Lang & API                     186               41    227 (11.3%)                                                   Lang & API 227 (11.3%)
                                                                                                               instances
                                                                                                                               Web & network 189 (9.4%)
    Web & network                  136              53     189 (9.4%)
                                                                                                                               Algorithms 176 (8.8%)
                                                                                                                               Security & crypto 150 (7.5%)
          Algorithms                     162             176 (8.8%)
                                                                                                                               Database 125 (6.2%)
 Security & crypto          49           101        150 (7.5%)
                                                                           SWE (n=1000)
           Database         57           68      125 (6.2%)
                                                                           Terminal (n=1000)

                        0        50      100      150     200    250     300     350   400
                                                   Number of instances



                                                 Figure 2: The data distribution of our evolution data.



4         E VOLUTION DATASET AND P ROTOCOL


To construct diverse and generalizable evolution instances, we first extract high-level domain in-
formation (i.e., task category labels) from mainstream terminal-related benchmarks, including the
TerminalBench and SWE-Bench families. Using these category labels as search guidance, human
annotators retrieve relevant publicly available resources from external sources, including but not
limited to GitHub repositories 1 , Hugging Face 2 , Kaggle 3 , and Linux kernel documentation 4 . The
retrieved resources are then used as source materials to construct new executable tasks in the Harbor
format. Importantly, downstream benchmarks provide only high-level domain guidance for resource
retrieval; no benchmark instances or task-specific information are used during task construction.
We apply a multi-stage quality-control pipeline to the constructed instances. First, LLM-based fil-
tering evaluates three aspects: Environment Completeness, ensuring that all required data, depen-
dencies, files, and tools are available; Practicality and Non-triviality, excluding artificial or overly
simple tasks with limited reasoning or environment interaction; and Evaluator Validity, requiring
the test suite to assess functional correctness rather than superficial completion signals. We then
perform executable validation by requiring the reference solution.sh to pass all task-specific
tests while ensuring that a no-op submission cannot receive a positive reward. Finally, each in-
stance is manually reviewed for task clarity, environment completeness, and evaluator correctness,
followed by LLM-based semantic similarity screening to remove instances with high overlap with
downstream benchmarks.
As shown in Fig. 2, this pipeline yields 2,000 high-quality, benchmark-disjoint evolution instances.
The data are relatively balanced across task categories, with broadly comparable distributions for
TB-related and SWE-related instances. Overlap between the two groups is limited by their distinct
construction sources: SWE-related tasks are built around GitHub repositories and require repository-
level software engineering, whereas TB-related tasks are constructed for direct interaction with ter-
minal environments.
This standardized evolution set provides a shared foundation for our experiments and future research
on harness self-evolution, enabling evaluation of whether Harness RSI methods learn generalizable
improvements rather than adaptations to downstream evaluation benchmarks.




     1
       https://github.com/
     2
       https://huggingface.co/
     3
       https://www.kaggle.com/
     4
       https://docs.kernel.org/


                                                                                               7
5     E XPERIMENT S ETTING

5.1   B ENCHMARKS

To validate the effectiveness of ModularRSI, we evaluate it against the baseline on two recent and
challenging terminal-related benchmarks: TerminalBench 2.0 (Merrill et al., 2026b) and SWE-
Bench-Verified (Jimenez et al., 2024b). TerminalBench 2.0 contains 89 diverse long-horizon ter-
minal tasks, while SWE-Bench-Verified contains 500 human-validated software engineering tasks
from real-world repositories. Together, they provide complementary evaluation of general termi-
nal interaction and repository-level software engineering. For reproducibility, we use the original
released benchmark versions and conduct all evaluations under the Harbor framework.

5.2   M ETRICS

Considering the stability of the evaluation results and the need to compare both the efficiency and
performance of different harnesses, we evaluate the following four metrics:
Accuracy (Acc): Accuracy measures the average success rate over all rollout trajectories. A trajec-
tory is considered successful if the agent successfully completes the corresponding task according
to the task-specific evaluator.
Pass@3: Pass@3 measures whether the agent can successfully solve a task within three independent
rollout attempts. A task is counted as solved if at least one of the three trajectories succeeds, and the
final score is averaged across all evaluation tasks.
StepNum: Average Step measures the average number of agent-environment interaction steps
required per rollout. It reflects the execution efficiency of the agent, with fewer steps generally
indicating a more efficient problem-solving process.
Pass3 : Pass3 measures the consistency and reliability of the agent across 3 independent rollout
attempts. A task is counted as successfully solved only if all 3 trajectories succeed, and the final
score is averaged across all evaluation tasks.

5.3   I MPLEMENTATION D ETAILS

In our experiments, all evolution processes, including single-module evolution and joint-module
evolution, are conducted for 3 epochs. Due to computational and time constraints, we select 120
instances from each of the TB-related and SWE-related subsets of the 2,000-instance evolution
dataset for harness evolution. The primary models used for evolution are DeepSeek-V4-Flash-
Preview and DeepSeek-V4-Flash-0731. We provision the deployed models with a TPM limit of 2
million tokens and use a batch size of 10 throughout the evolution process.


6     R ESULTS

6.1   G ENERALIZATION B EYOND E VOLUTION E XPERIENCE

The central challenge of Harness RSI is not only improving performance on the tasks used for evo-
lution, but discovering harness modifications that generalize beyond the evolution experience. To
evaluate this capability, we construct two independent evolution sets, i.e., TB-related and SWE-
related. From each set, we sample 120 instances for harness evolution, resulting in 120 TB-related
and 120 SWE-related evolution tasks. We then evaluate the evolved harnesses on both Terminal-
Bench 2.0 and SWE-Bench-Verified under in-domain and out-of-domain settings. The evolution
sets are completely isolated from the evaluation benchmarks, preventing direct exposure to evalua-
tion tasks during evolution.
As shown in Table 2, with DeepSeek-V4-Flash-Preview as the backbone model, ModularRSI con-
sistently improves performance across both evaluation benchmarks under different evolution set-
tings. In the in-domain setting, the evolved harness improves accuracy from 47.57 to 52.43 on
TerminalBench 2.0 and from 73.40 to 76.45 on SWE-Bench-Verified. We further analyze perfor-


                                                   8
Table 2: Cross-benchmark transfer of frozen evolved harnesses. After evolution on TB-related
or SWE-related tasks, each harness is frozen and evaluated on both held-out benchmarks using the
same inference backbone.
                            SWE-Bench-Verified                               TerminalBench 2.0
 Evolution Set    Eval. Setting    Acc ↑ Pass@3 ↑ Pass3 ↑         Eval. Setting   Acc ↑ Pass@3 ↑ Pass3 ↑
 No Evolution           –      73.40       83.20       62.80            –      47.57         58.43   30.34
 TB-Related      Out-of-Domain 75.80       84.67       66.20      In-Domain    52.43         65.17   35.96
 SWE-Related      In-Domain    76.45       85.30       66.80     Out-of-Domain 49.40         60.67   30.34


Table 3: Generalization across different inference models with a frozen evolved harness on Termi-
nalBench 2.0.
                 Inference Model      Method                   Acc ↑   Pass@3 ↑    Pass3 ↑
                                      Baseline                 59.55     70.79      46.07
                 GLM-5.2
                                      ModularRSI               61.80     74.16      49.44
                                      Baseline                 41.57     56.18      24.72
                 MiniMax-2.5
                                      ModularRSI (Ours)        44.94     57.30      30.34
                                      Baseline                 47.57     58.43      30.34
                 DeepSeek-V4-Flash
                                      ModularRSI (Ours)        52.43     65.17      35.96



mance across successive RSI generations and observe a largely monotonic improvement throughout
the evolution process (see Appendix F).
More importantly, these gains transfer beyond the evolution domain. The harness evolved on TB-
related data improves SWE-Bench-Verified accuracy to 75.80, while the harness evolved on SWE-
related data improves TerminalBench 2.0 accuracy to 49.40. These results suggest that ModularRSI
discovers reusable improvements to the underlying agent execution mechanism, rather than merely
specializing to the tasks encountered during evolution.
Notably, the gain is particularly pronounced for Pass3 on TerminalBench 2.0, which increases from
30.34 to 35.96. This improvement suggests that harness evolution not only increases average task-
solving capability but also enhances execution reliability, reducing stochastic failures across re-
peated trials.

6.2   C ROSS -M ODEL G ENERALIZATION

Beyond task-level generalization, we further examine whether the discovered harness improvements
are transferable across different foundation models. Since different models exhibit different be-
haviors in planning, tool interaction, and error recovery, a model-specific optimization may fail to
generalize.
To evaluate this capability, we freeze the harness evolved with DeepSeek-V4-Flash Preview on the
TB-related evolution set and apply it to different foundation models on TerminalBench 2.0.
As shown in Table. 3, the evolved harness consistently improves Acc, Pass@3, and Pass3 across all
evaluated foundation models. For example, the evolved harness improves GLM-5.2 accuracy from
59.55 to 61.80 and MiniMax-2.5 accuracy from 41.57 to 44.94.
These results demonstrate that ModularRSI learns transferable improvements to the agent execution
process rather than exploiting model-specific behaviors.

6.3   E FFECT OF M ODULAR E VOLUTION

As shown in Table 4, independently evolving modules and then integrating them achieves the best
overall performance, improving Acc from 47.57 to 52.43. In contrast, both joint and non-modular
evolution reduce accuracy below the baseline. This suggests that restricting the modification scope
helps reduce interference when optimizing the harness.


                                                   9
       Table 4: Comparison of different harness evolution strategies on TerminalBench 2.0.
                 Method                       Acc ↑ Pass@3 ↑ Pass3 ↑ StepNum ↓
                 Baseline                     47.57    58.43   30.34      34.70
                 Non-modular Evolution        46.44    64.04   24.72      29.03
                 Joint All-Module Evolution   44.19    61.80   24.72      44.34
                 ModularRSI (Ours)            52.43    65.17   35.96      35.57


Table 5: Performance of single-module evolution and cross-module integration on TerminalBench
2.0. Each row under Single-Module Evolution reports the harness obtained by independently evolv-
ing only the corresponding module from the same baseline. ModularRSI (Ours) further integrates
the five independently evolved modules through Cross-Module Integration to construct the final
evolved harness.
                  Method                      Acc ↑ Pass@3 ↑ Pass3 ↑ StepNum ↓
                  Baseline                    47.57    58.43   30.34     34.70
                  Single-Module Evolution
                  Context Management          49.44    61.80   31.40     35.10
                  Tool Use                    50.19    62.92   30.34     41.28
                  Agent Loop                  50.56    64.04   34.83     40.40
                  Observation Management      49.81    65.17   33.70     22.50
                  Task Completion Detection   49.44    65.17   31.40     31.06
                  Cross-Module Integration
                  ModularRSI (Ours)           52.43    65.17   35.96     35.57



We further examine the contribution of each independently evolved module before integration. Since
ModularRSI evolves all five modules independently for three epochs each, evaluating single-module
variants also helps assess whether improvements can be achieved without the larger aggregate trajec-
tory budget of the full framework. As shown in Table 5, all single-module variants improve accuracy
over the baseline, with different modules providing distinct benefits. Agent Loop yields the largest
single-module accuracy gain, whereas Observation Management substantially reduces the average
number of execution steps. Integrating the independently evolved modules further increases Acc to
52.43 and Pass3 to 35.96, suggesting that the modules capture complementary improvements that
can be effectively combined.

6.4   C OMPARING WITH E XISTING RSI M ETHODS

Considering task compatibility, reproducibility,
and method performance, we adapt and repro- Table 6: Comparison with existing harness evo-
duce AHE and Meta-Harness under a unified ex- lution methods on TerminalBench 2.0.
perimental protocol. Specifically, all methods are  Method             Acc ↑ Pass@3 ↑ Pass3 ↑
adapted to the Harbor framework and evolve from
the same Terminus-2 harness using the same 120      Baseline           61.79    73.03     50.56
evolution instances. ModularRSI evolves each        Meta-Harness       62.92    74.16     50.56
                                                    AHE                62.54    73.03     51.69
module independently for three epochs, followed
                                                    ModularRSI (Ours) 67.42     78.65     56.18
by a merging stage. To match the aggregate num-
ber of evolution rounds, accounting for both module-wise evolution and merging in ModularRSI,
we evolve AHE and Meta-Harness for 16 epochs. For all methods, the harness from the final gen-
eration is evaluated on the downstream benchmark. All methods use DeepSeek-V4-Flash-0731 for
both evolution and evaluation, with the same TPM limit of 2M tokens per minute. We additionally
disable web search for all methods to prevent the evolved harnesses from retrieving task solutions
from external sources.
As shown in Tab. 6, although existing RSI methods can achieve strong performance when evolv-
ing directly on benchmark data, their improvements are much more limited under our benchmark-
disjoint protocol. Both AHE and Meta-Harness remain close to the Terminus-2 baseline, with ac-
curacy changes of approximately one percentage point, whereas ModularRSI improves accuracy by


                                                  10
more than five points. This substantially larger gain demonstrates the stronger generalizability of
ModularRSI to unseen tasks.

6.5   T HE E FFECT OF C ONTRASTIVE A NALYSIS

Our ModularRSI leverages contrastive trajectory
analysis and modular evolution to more accu-



                                                       Usable pair ratio (%)
rately localize deficiencies in the harness and                                38                       36.67%
identify generalizable harness improvements. To                                37
                                                                               36                                             34.17%
examine the role of contrastive analysis, we ana-                              35
lyze both the proportion of contrastive trajectory                             34                                        Δ = -7.50 pp
                                                                               33
pairs during evolution and representative case                                      Epoch 1             Epoch 2                Epoch 3
studies.                                                                                          Self-evolution epoch

Specifically, as shown in Fig. 3, we report the
                                                     Figure 3: The contrastive trajectory pairs ratio
proportion of contrastive trajectory pairs among
                                                     variation during evolution.
all trajectory groups in each epoch on Terminal-
Bench 2.0. As evolution progresses, the propor-
tion of available contrastive pairs gradually decreases. This trend suggests that the harness progres-
sively incorporates the reusable behavioral improvements revealed by these contrastive examples,
thereby reducing the occurrence of cases in which successful and failed trajectories coexist for the
same task.
In addition, the case studies in Appendix D further illustrate how our Contrastive Trajectory Analysis
helps identify generalizable harness improvements. In particular, comparing successful and failed
trajectories exposes key behavioral differences, allowing ModularRSI to abstract them into reusable
harness mechanisms rather than task-specific fixes.

6.6   E FFECT OF E VOLUTION DATA Q UALITY

Beyond the evolution strategy, the quality of evo-
                                                             66                                 65.0
lution experience also affects the effectiveness of
                                                           Evolution-set
                                                             64
Harness RSI. Since harness evolution relies on
                                                             62
                                                            score (%)
execution feedback to identify systematic failures                                              61.8
and improve interaction strategies, the informa-             60
                                                             58                 Medium    Hard & Easy
tiveness of evolution tasks is crucial. In partic-
ular, the difficulty distribution of evolution data               0              1               2
plays an important role in determining the quality                              Epoch
of evolution signals. Moderately difficult tasks
are more likely to provide informative contrasts: Figure 4: Accuracy variation during evo-
easy tasks contain insufficient failure cases, while lution under different difficulty distributions.
extremely difficult tasks rarely yield successful DeepSeek-V4-Flash Preview is used as the
trajectories that reveal effective interaction strate- foundation model.
gies. Therefore, we hypothesize that a balanced
difficulty distribution can facilitate the discovery of generalizable harness improvements.
To verify this hypothesis, we construct two evolution settings with different difficulty distributions:
a Medium-centered setting and a Hard & Easy setting. The detailed procedure for constructing these
evolution datasets is described in the Appendix. E.
As shown in Fig. 4, the Medium-centered setting achieves
consistently stronger improvement throughout the evolu-                                 Table 7: Performance of Harnesses
tion process. Moreover, as shown in Tab. 7 the evolved                                  Evolved with Different Evolution-
harness generalizes better to downstream evaluation: the                                Data Distributions on SWE-Bench
harness evolved with the Medium-centered distribution                                   Verified.
achieves 76.45% accuracy on SWE-Bench Verified, outper-                                       Difficulty Distribution      Acc ↑
forming the Hard & Easy setting by 2.20 percentage points
(74.25%). This demonstrates that evolution data with more                                     Medium-centered              76.45
informative trajectory contrasts leads to more effective and                                  Hard & Easy                  74.25
generalizable harness improvements.


                                                  11
7   L IMITATIONS AND C ONCLUSION
We present ModularRSI, a benchmark-disjoint and modular framework for generalizable harness
self-improvement. By contrasting execution trajectories and evolving harness modules indepen-
dently, ModularRSI identifies reusable mechanism-level improvements while reducing task-specific
adaptation. Experiments on TerminalBench 2.0 and SWE-Bench Verified demonstrate consistent
gains across unseen tasks, domains, and foundation models.
Our study has several limitations. First, we do not conduct a dedicated ablation that isolates the con-
tribution of contrastive trajectory analysis, although our trajectory analysis and case studies provide
supporting evidence. In addition, due to computational cost, our main evolution experiments use
only a subset of the 2,000 curated evolution instances. We leave broader comparisons and larger-
scale studies to future work.
Overall, our results demonstrate the potential of benchmark-disjoint, contrastive, and modular evo-
lution for building more generalizable self-improving agent harnesses.

R EFERENCES
Lakshya A Agrawal, Shangyin Tan, Dilara Soylu, Noah Ziems, Rishi Khare, Krista Opsahl-Ong,
  Arnav Singhvi, Herumb Shandilya, Michael J Ryan, Meng Jiang, et al. Gepa: Reflective prompt
  evolution can outperform reinforcement learning. In International Conference on Learning Rep-
  resentations, volume 2026, pp. 8479–8565, 2026.
Mengzhuo Chen, Junjie Wang, Zhe Liu, Yawen Wang, Haiming Zheng, and Qing Wang. From
 failed trajectories to reliable llm agents: Diagnosing and repairing harness flaws. arXiv preprint
 arXiv:2606.06324, 2026a.
Mingju Chen, Can Lv, Guibin Zhang, Heng Chang, and Shiji Zhou. Harnessforge: Joint harness
 and policy evolution for adaptive agent systems, 2026b. URL https://arxiv.org/abs/
 2606.01779.
Zihao Cheng, Hongru Wang, Zeming Liu, Xinyi Wang, Xiangrong Zhu, Yuhang Guo, Wei Lin,
  Jeff Z Pan, and Yunhong Wang. Terminal-world: Scaling terminal-agent environments via agent
  skills. arXiv preprint arXiv:2605.20876, 2026.
Xiang Deng, Jeff Da, Edwin Pan, Yannis Yiming He, Charles Ide, Kanak Garg, Niklas Lauffer,
  Andrew Park, Nitin Pasari, Chetan Rane, et al. Swe-bench pro: Can ai agents solve long-horizon
  software engineering tasks? arXiv preprint arXiv:2509.16941, 2025.
Yuetian Du, Yucheng Wang, He Xu, Jiexu Xu, Shanwen Tan, Bing Zhao, Boyu Yang, Zhijie Xu,
  Ming Kong, Hu Wei, Jie Liu, and Qiang Zhu. Living-harness is an interactive-agent evolver,
  2026. URL https://arxiv.org/abs/2607.26598.
Yingying Fan, Penghui Du, Leyan Zhu, Runze He, Zimeng Wu, Yuxuan Zhang, Liang Chen, Jiahao
  Xie, Jiangtang Wang, Shuai Shao, et al. Medclaw: Heuristic agent harness for long-horizon
  surgical video reasoning. arXiv preprint arXiv:2608.14015, 2026.
Kanishk Gandhi, Shivam Garg, Noah D Goodman, and Dimitris Papailiopoulos. Endless terminals:
  Scaling rl environments for terminal agents. arXiv preprint arXiv:2601.16443, 2026.
Hanhua Hong, Yizhi LI, Jiaoyan Chen, Sophia Ananiadou, Xiaoli Li, Jung-jae Kim, and Chenghua
  Lin. HiRAS: A hierarchical multi-agent framework for paper-to-code generation and execution.
  In Findings of the Association for Computational Linguistics: ACL 2026, pp. 7624–7652, 2026.
Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik
  Narasimhan. Swe-bench: Can language models resolve real-world github issues? In International
  Conference on Learning Representations, volume 2024, pp. 54107–54157, 2024a.
Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik R
  Narasimhan. SWE-bench: Can language models resolve real-world github issues? In The Twelfth
  International Conference on Learning Representations, 2024b. URL https://openreview.
  net/forum?id=VTF8yNQM66.


                                                  12
Yoonho Lee, Roshen Nair, Qizheng Zhang, Kangwook Lee, Omar Khattab, and Chelsea Finn. Meta-
  harness: End-to-end optimization of model harnesses. arXiv preprint arXiv:2603.28052, 2026.

Jiahang Lin, Shichun Liu, Chengjun Pan, Lizhi Lin, Shihan Dou, Zhiheng Xi, Xuanjing Huang,
   Hang Yan, Zhenhua Han, Tao Gui, et al. Agentic harness engineering: Observability-driven
   automatic evolution of coding-agent harnesses. arXiv preprint arXiv:2604.25850, 2026.

Xinghua Lou, Miguel Lázaro-Gredilla, Antoine Dedieu, Carter Wendelken, Wolfgang Lehrach, and
  Kevin P Murphy. Autoharness: improving llm agents by automatically synthesizing a code har-
  ness. arXiv preprint arXiv:2603.03329, 2026a.

Xinghua Lou, Miguel Lázaro-Gredilla, Antoine Dedieu, Carter Wendelken, Wolfgang Lehrach, and
  Kevin P. Murphy. Autoharness: improving llm agents by automatically synthesizing a code har-
  ness, 2026b. URL https://arxiv.org/abs/2603.03329.

Xiaotian Luo, Dizhan Xue, Fengxingyu Wang, Chuanrui Hu, and Yafeng Deng. Harnessbank:
  Semantic gene-bank search with gated verification for agent-harness self-evolution, 2026a. URL
  https://arxiv.org/abs/2607.13683.

Yifu Luo, Zeyu Chen, Haoyu Wang, Xinhao Hu, Yuxuan Zhang, Zhizhou Sha, and Shiwei
  Liu. Learning from the self-future: On-policy self-distillation for dllms. arXiv preprint
  arXiv:2606.18195, 2026b.

Mike Merrill, Alexander Shaw, Nicholas Carlini, Boxuan Li, Harsh Raj, Ivan Bercovich, Lin Shi,
 Jeong Shin, Thomas Walshe, E Kelly Buchanan, et al. Terminal-bench: Benchmarking agents
 on hard, realistic tasks in command line interfaces. In International Conference on Learning
 Representations, volume 2026, pp. 40903–40986, 2026a.

Mike A. Merrill, Alexander G. Shaw, Nicholas Carlini, Boxuan Li, Harsh Raj, Ivan Bercovich, Lin
 Shi, Jeong Yeon Shin, Thomas Walshe, E. Kelly Buchanan, Junhong Shen, Guanghao Ye, Haowei
 Lin, Jason Poulos, Maoyu Wang, Marianna Nezhurina, Jenia Jitsev, Di Lu, Orfeas Menis Mas-
 tromichalakis, Zhiwei Xu, Zizhao Chen, Yue Liu, Robert Zhang, Leon Liangyu Chen, Anurag
 Kashyap, Jan-Lucas Uslu, Jeffrey Li, Jianbo Wu, Minghao Yan, Song Bian, Vedang Sharma,
 Ke Sun, Steven Dillmann, Akshay Anand, Andrew Lanpouthakoun, Bardia Koopah, Changran
 Hu, Etash Guha, Gabriel H. S. Dreiman, Jiacheng Zhu, Karl Krauth, Li Zhong, Niklas Muen-
 nighoff, Robert Amanfu, Shangyin Tan, Shreyas Pimpalgaonkar, Tushar Aggarwal, Xiangning
 Lin, Xin Lan, Xuandong Zhao, Yiqing Liang, Yuanli Wang, Zilong Wang, Changzhi Zhou, David
 Heineman, Hange Liu, Harsh Trivedi, John Yang, Junhong Lin, Manish Shetty, Michael Yang,
 Nabil Omi, Negin Raoof, Shanda Li, Terry Yue Zhuo, Wuwei Lin, Yiwei Dai, Yuxin Wang,
 Wenhao Chai, Shang Zhou, Dariush Wahdany, Ziyu She, Jiaming Hu, Zhikang Dong, Yuxuan
 Zhu, Sasha Cui, Ahson Saiyed, Arinbjörn Kolbeinsson, Jesse Hu, Christopher Michael Rytting,
 Ryan Marten, Yixin Wang, Alex Dimakis, Andy Konwinski, and Ludwig Schmidt. Terminal-
 bench: Benchmarking agents on hard, realistic tasks in command line interfaces, 2026b. URL
 https://arxiv.org/abs/2601.11868.

Michael Nguyen, Quoc Nguyen, and Paul Vuong. Recursive self-evolving agents via held-out se-
 lection, 2026. URL https://arxiv.org/abs/2606.28374.

Wenbo Pan, Shujie Liu, Chin-Yew Lin, Jingying Zeng, Xianfeng Tang, Xiangyang Zhou, Yan Lu,
 and Xiaohua Jia. Evolving agents in the dark: Retrospective harness optimization via self-
 preference, 2026. URL https://arxiv.org/abs/2606.05922.

Renjie Pi, Grace Lam, Mohammad Shoeybi, Pooya Jannaty, Bryan Catanzaro, and Wei Ping. On
  data engineering for scaling llm terminal capabilities, 2026. URL https://arxiv.org/
  abs/2602.21193.

Jincheng Ren, Siwei Wu, Yizhi Li, Kang Zhu, Shu Xu, Boyu Feng, Ruibin Yuan, Wei Zhang,
   Riza Batista-Navarro, Jian Yang, and Chenghua Lin. A self-evolving framework for efficient
   terminal agents via observational context compression, 2026. URL https://arxiv.org/
   abs/2604.19572.


                                              13
Jiajun Shi, Siyuan Tao, Yuhao Wu, Zexuan Wang, Jingyuan Zhang, Jiaheng Liu, Xinping Lei, Xin-
   rong Zhang, Siyuan Fang, Zhewen Tan, et al. S3gym: Can llms turn self-testing and self-judging
   into self-improvement? arXiv preprint arXiv:2608.31100, 2026.
Haowen Wang, Yaxin Du, Jian Yang, Jiajun Wu, Shukai Liu, Yuxuan Zhang, Pingjie Wang, Siheng
  Chen, Tuney Zheng, Ming Zhou, et al. Mira: Mid-training rubric anchoring for source-aware data
  selection. arXiv preprint arXiv:2605.30288, 2026a.
Yike Wang, Huaisheng Zhu, Zhengyu Hu, Yige Yuan, Zhengyu Chen, Shakti Senthil, Hannaneh
  Hajishirzi, Yulia Tsvetkov, Pradeep Dasigi, and Teng Xiao. Rethinking the evaluation of harness
  evolution for agents. In COLM 2026 The 2nd Workshop on Lifelong Agents: Learning, Aligning,
  and Evolving, 2026b.
Yubo Wang, Jiarong Liang, Yuxuan Zhang, Xuye Liu, Cong Wei, Yuyu Zhang, Ping Nie, and Wenhu
  Chen. Function-aware fill-in-the-middle as mid-training for coding agent foundation models.
  arXiv preprint arXiv:2607.12463, 2026c.
Siwei Wu, Yizhi Li, Yuyang Song, Wei Zhang, Yang Wang, Riza Batista-Navarro, Xian Yang,
  Mingjie Tang, Bryan Dai, Jian Yang, and Chenghua Lin. Large-scale terminal agentic trajec-
  tory generation from dockerized environments. In Proceedings of the 43rd International Confer-
  ence on Machine Learning, 2026a. URL https://icml.cc/virtual/2026/poster/
  64240.
Yuhao Wu, Jingyuan Zhang, Jiajun Shi, Xinping Lei, Qingshui Gu, Yuxuan Zhang, Zexuan Wang,
  Chen He, Chen Huang, Maojia Song, et al. Harnessdev: Can llms create and evolve their own
  agent harness? arXiv preprint arXiv:2609.01437, 2026b.
Yuhao Wu, Jingyuan Zhang, Jiajun Shi, Yuxuan Zhang, Xinping Lei, Junting Zhou, Zexuan Wang,
  Yuchen Wu, Huan Zhou, Duo Wang, et al. Aspire: Can models self-evolve from vague goals?
  arXiv preprint arXiv:2608.31111, 2026c.
Zhiling Yan, Dingjie Song, Hanrong Zhang, Wei Liang, Yuxuan Zhang, Yutong Dai, Lifang He,
  Philip S Yu, Ran Xu, Xiang Li, et al. Openskill: Open-world self-evolution for llm agents. arXiv
  preprint arXiv:2606.06741, 2026.
Jian Yang, Wei Zhang, Shawn Guo, Zhengmao Ye, Lin Jing, Shark Liu, Yizhi Li, Jiajun Wu, Cening
   Liu, X. Ma, Yuyang Song, Siwei Wu, Yuwen Li, L. Liao, T. Zheng, Ziling Huang, Zelong Huang,
   Che Liu, Yan Xing, Renyuan Li, Qingsong Cai, Hanxu Yan, Siyue Wang, Shikai Li, Jason Klein
   Liu, An Huang, Yongsheng Kang, Jinxing Zhang, Chuan Hao, Haowen Wang, Weicheng Gu,
   Ran Tao, Mingjie Tang, Peihao Wu, Jianzhou Wang, Xianglong Liu, Weifeng Lv, and Bryan Dai.
   Iquest-coder-v1 technical report, 2026a. URL https://arxiv.org/abs/2603.16733.
Jian Yang, Wei Zhang, Shuyue Guo, Yizhi LI, Linzheng Chai, Zhengmao Ye, Shukai Liu, Yuyang
   Song, Jiajun Wu, Che Liu, Tianyu Zheng, Siwei Wu, Leo L, Xudong Ma, Chuan Hao, Ran Tao,
   Yan Xing, Jianzhou Wang, Mingjie Tang, Aishan Liu, Zhoujun Li, Xianglong Liu, Weifeng
   Lv, and Bryan Dai. LoopCoder: Scaling code intelligence via looped language models. In
   Maria Liakata, Viviane P. Moreira, Jiajun Zhang, and David Jurgens (eds.), Findings of the As-
   sociation for Computational Linguistics: ACL 2026, pp. 16209–16223, San Diego, California,
   United States, July 2026b. Association for Computational Linguistics. ISBN 979-8-89176-395-
   1. doi: 10.18653/v1/2026.findings-acl.796. URL https://aclanthology.org/2026.
   findings-acl.796/.
Hangfan Zhang, Shao Zhang, Kangcong Li, Chen Zhang, Yang Chen, Yiqun Zhang, Lei Bai, and
  Shuyue Hu. Self-harness: Harnesses that improve themselves. arXiv preprint arXiv:2606.09498,
  2026a.
Jenny Zhang, Shengran Hu, Cong Lu, Robert Lange, and Jeff Clune. Darwin gödel machine: open-
  ended evolution of self-improving agents. In International Conference on Learning Representa-
  tions, volume 2026, pp. 104223–104294, 2026b.
Qizheng Zhang, Changran Hu, Shubhangi Upasani, Boyuan Ma, Fenglu Hong, Vamsidhar Kama-
  nuru, Jay Rainton, Chen Wu, Mengmeng Ji, Hanchen Li, et al. Agentic context engineering:
  Evolving contexts for self-improving language models. In International Conference on Learning
  Representations, volume 2026, pp. 86069–86100, 2026c.


                                               14
Yuxuan Zhang, Penghui Du, Bo Li, Cong Wei, Junwen Miao, Huaisong Zhang, Songcheng Cai,
  Yubo Wang, Dongfu Jiang, Yuyu Zhang, et al. Rewardharness: Self-evolving agentic post-
  training. arXiv preprint arXiv:2605.08703, 2026d.
Yuxuan Zhang, EunJeong Hwang, Huaisong Zhang, Penghui Du, Yiming Jia, Dongfu Jiang, Xuan
  He, Shenhui Zhang, Ping Nie, Peter West, et al. Watch before you answer: Learning from visually
  grounded post-training. arXiv preprint arXiv:2604.05117, 2026e.
Yuxuan Zhang, Yubo Wang, Yipeng Zhu, Penghui Du, Junwen Miao, Xuan Lu, Zhuofeng Li, Xing-
  wei Qu, Zhengkang Guo, Yuanzhe Shen, et al. Clawbench: Can ai agents complete everyday
  online tasks? arXiv preprint arXiv:2604.08523, 2026f.
Adam Zweiger, Jyo Pari, Han Guo, Yoon Kim, and Pulkit Agrawal. Self-adapting language models.
  Advances in Neural Information Processing Systems, 38:74084–74115, 2026.




                                               15
A      H ARNESS A RCHITECTURE


                                   Agent Loop                                       execution coordinator




                                         Context Management
                                                                                                             execute
                                                                                  Tool Use                                Environment


                      prompt

        LLM                           Loop control

    model inference                   state / retry / stop
                      response                                                                                               terminal

                                                                                  Observation                             files / processes
                                                   state / decision
                                                                                  Management
                                                                                                            read output


                                         Task Completion
                                         Detection




                                          module call / return             runtime relationships




                                 Figure 5: Architecture of the five-module harness.

Figure 5 shows how the five modules interact during task execution. The outer box is Agent Loop,
and the central Loop control box represents its runtime logic: maintaining execution state, schedul-
ing calls, handling retries, and deciding whether to continue. Each of the other four modules ex-
changes inputs and outputs with this controller. The bidirectional module arrows indicate a call and
its return. The LLM and environment are external resources: the LLM generates responses, while
the environment runs commands and stores files and processes. Before execution, the composer
selects one implementation for each module.
In a normal iteration, Agent Loop first asks Context Management to update the conversation history,
compressing it when needed. It then sends the current prompt to the LLM. Tool Use parses the
response into commands and a completion signal, executes the commands in the environment, and
returns execution results or errors. Observation Management reads the current terminal output and
converts it into agent-readable feedback. This differs from Context Management, which works on
the accumulated conversation. Agent Loop combines the feedback with tool results, updates its
state, and passes that state to Task Completion Detection.
Task Completion Detection returns a stop recommendation and a reason. For example, the detector
requires two consecutive completion declarations. Agent Loop maintains that count and issues the
confirmation prompt after the first declaration; the detector checks whether the count meets its crite-
rion. The loop follows the recommendation, while evolved loop variants can override it. If execution
continues, the loop prepares the next prompt from the feedback. Parsing errors can instead trigger
a retry, and session failures or execution limits can end the run. The figure shows these modules’
relationships; the arrows do not prescribe a fixed module-to-module execution sequence.

A.1      M ODULE I NTERFACE E XCERPTS

Listing 1 shows the main inputs and outputs of all five modules. The signatures follow the implemen-
tation; imports, setup methods, and method bodies are omitted. Each implementation is registered
with a name, description, and configuration parameters. The shared ModuleCtx provides task
configuration, environment access, and recording services.

Listing 1: Selected interfaces of the five harness modules. Ellipses denote omitted implementations.
# 1. Agent Loop
# Input: task, conversation, and the other four modules.
# Output: execution status, final text, and failure tag.
class AgentLoop(Protocol):
    async def run(


                                                                      16
         self, initial_prompt: str, original_instruction: str,
         observation: Observation, context_mgmt: ContextMgmt,
         tools: ToolSet, verification: VerificationLoop,
         chat: Chat, ctx: ModuleCtx,
     ) -> AgentLoopResult: ...

# 2. Observation Management
# Reads the environment through ctx.
# Output: observation text and updated observation state.
class Observation(Protocol):
    async def capture(
        self, prev: ObsState, ctx: ModuleCtx,
    ) -> tuple[ObsResult, ObsState]: ...

# 3. Tool Use
# Model text -> commands, completion signal, parsing errors.
# A tool call -> execution result (success, output, error).
class ToolSet(Protocol):
    def parse_llm_response(
        self, response: str,
    ) -> LLMResponseParseResult: ...

     async def execute(
         self, call: ToolCall, ctx: ModuleCtx,
     ) -> ToolResult: ...

# 4. Context Management
# Input: conversation history and the original task.
# Output: updated Chat and an optional handoff prompt.
class ContextMgmt(Protocol):
    async def maybe_compress(
        self, chat: Chat, original_instruction: str,
        ctx: ModuleCtx,
    ) -> CompressResult: ...

     async def force_summarize(
         self, chat: Chat, original_instruction: str,
         ctx: ModuleCtx,
     ) -> CompressResult: ...

# 5. Task Completion Detection
# Input: loop state, including recent feedback and signals.
# Output: a stop recommendation and its reason.
class VerificationLoop(Protocol):
    async def should_terminate(
        self, state: AgentLoopState, ctx: ModuleCtx,
    ) -> tuple[bool, str]: ...


The completion detector returns a recommendation; Agent Loop maintains the state and controls
whether execution continues. Observation Management returns current environment feedback,
whereas Context Management updates the accumulated conversation history.


B    S TRUCTURED A NALYSIS F INDINGS

The three trajectory groups in Sec. 3.3 describe the available reward evidence. The implementation
refines these groups into routing buckets. The buckets select an analysis path. They do not change
the reward of a trajectory. Table 8 shows the mapping. Tasks with infrastructure-only failures are
excluded from harness diagnosis.
Each analyzed task produces one finding record. The field task identifies the task. The field lens
names the analysis mode, and locked module names the module that may be changed in the
current evolution run. The field is culprit gives the causal decision. The field divergence


                                               17
            Method group Implementation buckets
            Positive        all pass efficient, all pass wasteful
            Contrastive     mixed
            Negative        fixable fail, stuck fail, unreachable fail
            Excluded        infra only

Table 8: Mapping from the method-level trajectory groups to the routing buckets used by the imple-
mentation.


summarizes the relevant trajectory evidence. The field would change outcome gives a counter-
factual judgment: would the proposed module change plausibly change the task result? The fields
fixable now and suggested change state whether and how the system can act on the diag-
nosis. For a negative attribution, other module or note may record an alternative explanation.
The field parse status records whether the structured output was parsed successfully. Some
optional fields are therefore absent from some records.
Listing 2 shows two findings from one evolution batch. The first finding supports a change to the
Agent Loop. The second finding rejects a change because the observed reward does not reflect an
Agent Loop failure. We shorten the text values for readability. We keep the field names, decisions,
and causal conclusions unchanged.

Listing 2: Abridged examples of structured analysis findings. The first record supports an edit. The
second record abstains from an unsupported edit.
{
    "findings": [
      {
         "task": "draft_dp_3493beee_outa",
         "lens": "agent_loop",
         "is_culprit": true,
         "locked_module": "agent_loop",
         "divergence": "The passing roll ran build and package commands. The failing roll ran
       no build or validation command and repeatedly declared completion.",
         "would_change_outcome": "Yes. A completion gate that requires validation evidence
       would force the missing build-and-check stage.",
         "fixable_now": true,
         "suggested_change": "Add an evidence-gated completion variant. Allow termination only
       after a successful build, test, or run has been observed."
      },
      {
         "task": "draft_dp_eae0d1ff_outb",
         "lens": "contrast",
         "is_culprit": false,
         "divergence": "Both rolls produced functionally equivalent solutions. The failing
       artifact compiled and passed differential tests against the reference program.",
         "would_change_outcome": "No. The artifact evidence points to verifier-side noise
       rather than an Agent Loop failure.",
         "fixable_now": false
      }
    ]
}




C     A BRIDGED P ROMPTS U SED IN H ARNESS E VOLUTION

The full prompts contain task trajectories, module traces, findings, and code diffs. These inputs are
inserted at runtime and can be long. The excerpts below preserve the original wording and order.
Text in angle brackets denotes runtime input. Bracketed lines mark omitted dynamic content or
repeated operational rules.

C.1    T RAJECTORY A NALYSIS

The analysis prompt has two modes. The contrastive mode compares successful and failed trajecto-
ries. The efficiency mode examines a successful but wasteful trajectory. Both modes use the same
attribution rule and output format.


                                                 18
Listing 3: Excerpt from the trajectory-analysis prompt. Dynamic evidence and tool instructions are
omitted.
You are a READ-ONLY diagnostician deciding ONE thing: would
changing the ‘<TARGET_MODULE>‘ module actually CHANGE or
IMPROVE this task’s outcome? You get the SAME task solved on
one roll and FAILED on another (same code, different sampling).

This is NOT blame-attribution. Report a culprit ONLY if there
is a concrete ‘<TARGET_MODULE>‘ change that would plausibly
move THIS task from fail toward pass. If no such change would
help, the answer is no culprit, and you do NOT fix.

[... omitted: module scope, yardstick, and starter probes ...]

# The task: <TASK>
## PASSING roll
<PASSING_ROLL>
## FAILING roll
<FAILING_ROLL>

[... omitted: instructions for reading raw trajectories and
module traces ...]

# How to decide (in order)
1. Divergence: where did the pass and fail rolls stop behaving
   the same? What did the passing roll do there that the
   failing roll did not? Cite episodes or steps.
2. The counterfactual: picture a concrete change to
   ‘<TARGET_MODULE>‘. Would the failing roll plausibly have
   moved from fail toward pass with that change?
   - YES, and it fits inside the module: set ‘is_culprit‘ and
     ‘fixable_now‘ to true and describe the change.
   - YES, but it needs an architecture change: set
     ‘is_culprit‘ to true and ‘fixable_now‘ to false.
   - NO: set ‘is_culprit‘ to false. Do not invent a marginal
     tweak just to have a finding.

# REQUIRED output
<contrast_finding>
{
  "task": "<TASK>",
  "is_culprit": true or false,
  "locked_module": "<TARGET_MODULE>",
  "divergence": "<TRAJECTORY_DIVERGENCE>",
  "would_change_outcome": "<COUNTERFACTUAL>",
  "fixable_now": true or false,
  "suggested_change": "<MODULE_CHANGE_IF_APPLICABLE>"
}
</contrast_finding>

[... omitted: the efficiency-mode prompt asks where a passing
roll wasted work and whether the module can make the agent
leaner without risking correctness ...]



C.2   H ARNESS M ODIFICATION

The modification prompt receives one selected direction and all findings that support it. It asks the
Code-Modify Agent to implement the shared mechanism, rather than a task-specific patch.

 Listing 4: Excerpt from the harness-modification prompt. Runtime proposal evidence is omitted.
You are implementing ONE agreed direction on the agent’s


                                                 19
modules.

The direction below was chosen from a backlog of directions,
and the evidence under it is the COMPLETE set of observations
that support it - every one of them, not a sample. Build the
change that addresses the direction across all of that
evidence. Do NOT narrow it to whichever single task reads most
vividly: a change that only rescues one named task is worthless
here and has sunk a lineage before.

# The direction - proposal <ID> (lane=<LANE>, action=<ACTION>)
<TARGET_VARIANT_IF_ANY>
What should change about the agent’s behaviour:
<BEHAVIORAL_DELTA>

Why this is believed to be the cause:
<CAUSAL_HYPOTHESIS>

# The evidence - <N> finding(s), all of them
<SUPPORTING_FINDINGS>

[... omitted: retry or incomplete-evidence notice, when
applicable ...]

# How to work
1. Read the module(s) involved before editing.
2. Make the change general: it has to hold for every finding
   above, not one.
3. <ACTION-SPECIFIC ADD, MODIFY, OR REPLACE RULE>
4. ‘<validate/>‘, then ‘<commit_patch/>‘, then
   ‘<task_complete>true</task_complete>‘.

[... omitted: shared editor tool syntax and path rules ...]



C.3   D IFFS R EVIEW

The review prompt is reward-blind. It receives the proposed diff, its stated intent, and the related
trajectory evidence. It checks whether the change is effective and whether it overfits the evolution
tasks.

Listing 5: Excerpt from the diff-review prompt. Dynamic diffs, trajectories, and repeated rules are
omitted.
<review_gate_mode>true</review_gate_mode>

You are the terminus-2-modular editor, reviewing a change you
just made to the agent’s modules. The change is ALREADY
applied to the staging copy you can read. Your job now is NOT
to edit - it is to decide whether this change should be KEPT
or REJECTED.

# Review inputs
<DIFF>
<INTENT>
<REWARD-BLIND_TRAJECTORY_SUMMARIES>

[... omitted: architecture facts and raw-trajectory access
instructions ...]

# How to review
1. Effective? Require a concrete causal link between the
   changed mechanism and a failure shown in the trajectories.
   For a new variant, also check that the Composer could select


                                                20
   it for similar tasks.
2. Overfit? Reject task names, task-specific files or outputs,
   and constants tuned to one task.

[... omitted: detailed MODIFY/ADD tests and module-trace
interpretation ...]

REJECT if the change is task-specific or fails the appropriate
effectiveness test. Otherwise ACCEPT.

# Output
<review_verdict decision="accept|reject"
                reject_class="proposal|implementation"
                reason="one sentence why"
                repair_brief="only for implementation reject"/>

[... omitted: detailed verdict-field rules ...]




C.4   T HE C ROSS -M ODULE I NTEGRATION

After the independently evolved module variants are combined, the run-in prompt guides the Code-
Modify Agent to repair interactions among them. The following excerpt preserves the original
instructions. It omits only the runtime trajectories and conflict records.


      Listing 6: Excerpt from the cross-module run-in prompt. Dynamic evidence is omitted.

You are performing integration run-in on a library assembled
from independently evolved module lineages. This is not
feature evolution. Make at most one coherent cross-module
repair; do not add a new capability, tool, behavioral
dimension, or benchmark-specific special case.

[... omitted: frozen-bundle audit and support-generation
metadata ...]

# Same-task, same-bundle support evidence
<TRAJECTORY_SUMMARIES>

# Static conflict candidates
<CONFLICT_FINDINGS>

# Task
Read the raw trajectories and the named source locations.
Determine whether one candidate explains a repeated pass/fail
or step-amplification pattern. Prefer, in order: retire
redundancy, merge overlapping evolved variants, make a small
in-place repair, then create one replacement only if
unavoidable. A static finding is a lead, not proof.

Do not touch Kernel, composer, ‘active_bundle.json‘,
‘baseline.py‘, or ‘editor_file_tools.py‘. Validate before
committing.

[... omitted: skill-loading and lineage-metadata rules ...]

Return ‘<runin_meta>‘ with ‘ADDRESSED‘, ‘INTERACTION‘, and
‘NEW_CAPABILITY: no‘.




                                              21
               Statistic                                                  Count   Percentage
               Current rollouts provide a success–failure pair              732       40.67%
               All-fail groups paired with historical success in replay     150        8.33%
               All current rollouts fail, with no earlier success           262       14.56%
               All current rollouts succeed                                 648       36.00%

               Table 9: Trajectory evidence from the five runs and subsequent replay.

                        Successful trajectory (r0)                Failed trajectory (r1)
    Shared input       The same task instruction and Scala pipeline. The instruction requires excluding
                       NULL categories.
    Decision           Follows the written requirement.         Follows the legacy code.
    Response       ex- Episode 7: “I’ll include the filter to Episode 14: “The output includes rows
    cerpt              match the task specification.”           with NULL category (matching Scala be-
                                                                havior which doesn’t filter them out).”
    Code               Episode 6 adds a filter using The generated script has no NULL-
                       isNotNull().                             category filter.
    Output             47 rows; no NULL categories.             52 rows; five NULL categories.
    Reward             1                                        0

Table 10: A success–failure pair from the same task and harness configuration. The response ex-
cerpts show how the two rollouts resolve the same conflict.


D     C ASE S TUDIES ACROSS T RAJECTORY G ROUPS

D.1    T RAJECTORY G ROUP D ISTRIBUTION

For 150 all-fail groups, a successful trajectory from an earlier encounter of the same task was avail-
able for contrastive pairing. Eight groups had no valid scores.
Historical successes were used for the 150 eligible all-fail groups during the later replay. Eight
groups have no score.

D.2    C ONTRASTIVE : K EEP THE TASK R EQUIREMENTS IN V IEW

Task and trajectory pair. The task asks the agent to port a Scala sales pipeline to PySpark. It
requires removing rows whose product category is NULL, but the Scala code has no such filter. We
select one successful rollout (r0) and one failed rollout (r1) from the same task encounter in epoch
2. Both use generation 7 with the same module bundle. Table 10 shows the pair used for diagnosis.

Change. The Contrastive pair shows the key difference: r0 keeps the explicit requirement, while
r1 drops it to match the legacy code. The analysis proposes a persistent task checklist. Together
with two other findings, this leads to planning with guard in generation 9. The loop shows
task requirements in later prompts. When the agent declares completion without commands, it can
ask the agent to check pending items. The variant passes review and sanity checks and is retained.

Later observation. In epoch 3, the same task runs with the updated loop in generation 13. Roll-
out r0 keeps the NULL filter. At episode 17, the loop asks for another check before completion.
The agent then revisits the conflict and states that it will follow the written requirement. It runs a
command to check the output. The output has 47 rows, and all 52 external tests pass. Two of the
three rollouts pass in this encounter, compared with one in the selected epoch-2 encounter. Listing 7
shows this later execution. The Contrastive pair above comes from epoch 2.

Listing 7: A later execution of the same task. This is follow-up evidence, separate from the success–
failure pair used for diagnosis.
Epoch 3, r0, episode 17, after a completion check:


                                                      22
  "The Scala code doesn’t explicitly filter NULL categories,
  but the requirement says to exclude them. I’ll keep my
  implementation as is since it matches the requirements."
  Action: run an output-schema and row-count check.
  Output: 47 rows. External evaluation: 52 passed.



D.3    N EGATIVE : C HECK THE S TATED ACCEPTANCE C ONDITIONS

Problem. The task asks the agent to build FFmpeg 0.10.16. It also requires ldd to show
libavcodec, libavformat, and libx264. All three epoch-1 rollouts fail, forming a Neg-
ative group. In r0, the binaries can convert and inspect a video, but ldd lists only libx264. The
other two libraries are static archives. The agent still declares completion twice without running a
command. The external evaluator reports one failed test and nine passed tests.

Change. No successful trajectory is needed to see this mismatch. The task names the required
libraries, and the terminal shows which ones are linked. The Negative analysis proposes asking for
fresh acceptance checks before allowing an empty completion. This finding and another finding
lead to completion integrity guard in generation 6. The new loop reads the acceptance
checklist from the task. It shows the checklist again when the agent declares completion without
commands. It then asks the agent to run the checks. The variant is promoted, and this check is later
included in planning with guard.

Later observation. The task remains a Negative group in epoch 2. In epoch 3, it uses generation
14, and all three rollouts pass. In r0, the loop repeats the acceptance checklist at episode 34. The
agent responds by writing and running a verification script. The script includes ldd checks. Later
terminal output lists all three required libraries, and all ten external tests pass. Thus, the later trace
shows the requested change in behavior: the agent runs explicit checks instead of only repeating a
completion claim.

Listing 8: FFmpeg: missing linkage in the original case and explicit verification in a later run.
Addresses and unrelated output are omitted.
Epoch 1, r0, linkage check:
  ldd /usr/local/bin/ffmpeg 2>&1 |
    grep -E ’libavcodec|libavformat|libx264’
  Output: libx264.so.164 only.
  Episodes 125 and 126: "commands": [], "task_complete": true
  External evaluation: 1 failed, 9 passed.

Epoch 3, r0, episode 34:
  Loop: repeats the task’s acceptance checklist.
  Agent: writes and runs /tmp/verify_ffmpeg.sh.

Linkage output visible at episode 38:
  libavformat.so.53 => /usr/local/lib/libavformat.so.53 (...)
  libavcodec.so.53 => /usr/local/lib/libavcodec.so.53 (...)
  libx264.so.164 => /lib/x86_64-linux-gnu/libx264.so.164 (...)
  External evaluation: 10 passed.



D.4    P OSITIVE : AVOID S HELL R ETRIES W HEN W RITING F ILES

Problem. This case comes from the Tool Use evolution run. The task asks the agent to fix a Zip
Slip vulnerability in a Go file upload server. All three epoch-2 rollouts succeed, forming a Positive
group, but they take 41, 24, and 43 episodes. In r0, the agent calls write file with multi-line
Go code at episode 3. The tool dispatcher rejects the newlines and sends the call to the shell. The
shell returns write file: command not found. The agent then retries with other ways to
write the file. It eventually passes all 60 tests.


                                                   23
                  Table 11: Difficulty distributions of different evolution datasets.
            Difficulty Distribution   0–20%    20–40%     40–60%      60–80%     80–100%
            Medium-centered           10%        15%        50%         15%         10%
            Hard & Easy               35%        10%        10%         10%         35%


Change. The Positive analysis identifies the extra work caused by this failed helper call. It pro-
poses routing write file and edit block by the command name and passing the remain-
ing text as file content. The editor combines this finding with a parser-recovery finding to create
tools/combined robust.py in generation 9. The variant passes review and sanity checks
and is promoted. All four sanity rollouts select the new Tools variant.

Later observation. In epoch 3, the same task uses combined robust in generation 12. Its
multi-line dispatch code is unchanged from generation 9. At episode 4, r0 again calls write file
with multi-line Go code. This time, the helper writes the file directly and returns wrote 2204
bytes. All 60 tests pass, and r0 takes 26 episodes. Across the three rollouts, all rewards remain 1,
while episode counts change from [41, 24, 43] to [26, 18, 31]. The mean falls from 36 to 25 episodes.
Listing 9 shows the change in tool behavior.

Listing 9: A successful task with avoidable helper retries, followed by a successful run using the
promoted Tools variant. Go source is omitted.
Epoch 2, r0, episode 3:
  write_file /opt/fileserver/extract.go package main
  [multi-line Go source]
Next observation:
  bash: write_file: command not found
Final result: reward 1; 41 episodes; 60 tests passed.

Epoch 3, r0, episode 4:
  write_file /opt/fileserver/extract.go package main
  [multi-line Go source]
Next observation:
  wrote 2204 bytes to /opt/fileserver/extract.go
Final result: reward 1; 26 episodes; 60 tests passed.



What the cases show. The Contrastive case identifies a requirement to preserve. The Negative
case identifies a check to repeat. The Positive case identifies a tool failure that causes extra work.
Each finding contributes to a promoted module update. Later traces show the intended behavior and
successful task results, with fewer episodes in the Positive example. These runs also contain other
updates, so the comparisons do not isolate the effect of a single change.

E    T HE C URATION OF D IFFERENT DIFFICULTY SETTINGS

As shown in Table. 11, we construct two SWE-related evolution sets with different difficulty distri-
butions. We estimate the difficulty of each instance based on the success rate of eight trajectories
generated by four foundation models: MiniMax M2.7, GLM-5.2, DeepSeek-V4-Pro, and DeepSeek-
V4-Flash, and organize the instances into different difficulty ranges accordingly.

F    T HE E VOLUTION C URVE

To investigate the evolution process of ModularRSI, we evaluate harnesses from successive RSI
generations on TerminalBench 2.0, as shown in Fig. 6. We report both task accuracy, computed
from benchmark-provided rewards, and LLM-based trajectory scores. Specifically, we use Opus-
4.8 to assess the task-solving trajectories generated by each harness using the prompt provided in
Listing 10.


                                                  24
80
           Acc
           Judge                                                                       74.0
70



60


                                                                                       52.2
50



40
     0             3        6          9            12       15         18           22
                                             Generation

Figure 6: Accuracy variation during evolution under different generation on TerminalBench 2.0.

                   Listing 10: Prompt used for LLM-based trajectory evaluation.
You are an expert evaluator of LLM agent trajectories.

Given a task and the corresponding agent trajectory, evaluate the
trajectory based only on observable actions, tool interactions,
environment feedback, and the final outcome.

Task:
{TASK_DESCRIPTION}

Trajectory:
{TRAJECTORY}

Evaluate the trajectory along the following five dimensions:

1. Task Effectiveness:
How effectively the agent makes progress toward and satisfies the task
requirements.

2. Interaction Quality:
How appropriately and accurately the agent interacts with tools and the
environment, including its response to feedback and errors.

3. Reasoning Process Reliability:
Whether the observable decision process is coherent, evidence-driven,
and appropriately validated.

4. Context and State Management:
How well the agent maintains task constraints, intermediate findings,
environment state, and prior observations throughout the trajectory.

5. Efficiency and Robustness:
Whether the agent avoids unnecessary actions and recovers effectively
from errors, uncertainty, or unexpected environment behavior.

Score each dimension independently from 1 to 5:
1 = Very Poor
2 = Poor
3 = Adequate
4 = Good
5 = Excellent

Do not infer that all dimensions are good simply because the task


                                               25
succeeds, or poor simply because it fails. Base each score on concrete
evidence from the trajectory.

Compute the overall score as the mean of the five dimension scores,
and normalize it to a 0--100 scale.

Return only:
{
  "task_effectiveness": <1-5>,
  "interaction_quality": <1-5>,
  "reasoning_process_reliability": <1-5>,
  "context_and_state_management": <1-5>,
  "efficiency_and_robustness": <1-5>,
  "overall_score": <1.0-5.0>,
  "normalized_score": <0-100>
}




                                   26

