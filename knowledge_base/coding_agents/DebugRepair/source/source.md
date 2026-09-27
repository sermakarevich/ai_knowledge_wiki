# DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging
Source: https://arxiv.org/abs/2604.19305v1
Kind: pdf
Fetched: 2026-09-23T21:17:13.474366+00:00
Tool: pdftotext
PDF: https://arxiv.org/abs/2604.19305v1 (source.pdf not copied: 3.8 MB exceeds 2 MB limit)
Research-Target: /Users/sergii/.ai/knowledge/research_topics/coding_agents/research/ai_coding_best_practices
Topic: coding_agents

                                         DebugRepair: Enhancing LLM-Based Automated Program
                                         Repair via Self-Directed Debugging
                                         LINHAO WU∗ , Shandong University, China
                                         YIFEI PEI∗ , Shandong University, China
                                         ZHEN YANG† , Shandong University, China
                                         KAINAN LI, Shandong University, China
                                         ZHONGHANG LU, Fudan University, China




arXiv:2604.19305v1 [cs.SE] 21 Apr 2026
                                         HAO TAN, Shandong University, China
                                         XIRAN LYU, Shandong University, China
                                         JIA LI, Tsinghua University, China
                                         YIZHOU CHEN, Peking University, China
                                         PENGYU XUE, The Hong Kong Polytechnic University, China
                                         KUNWU ZHENG, Shandong University, China
                                         DAN HAO, Peking University, China
                                         Automated Program Repair (APR) has recently benefited from the strong code understanding and generation
                                         capabilities of Large Language Models (LLMs). Among existing LLM-based APR techniques, feedback-based
                                         approaches have shown promising results by iteratively refining candidate patches according to test execution
                                         feedback. However, most of these approaches rely primarily on outcome-level failure symptoms, e.g., stack
                                         traces, which indicate how failures are observed but fail to expose the intermediate runtime states that are often
                                         critical for root-cause analysis. As a result, LLMs must infer bug causes without access to such intermediate
                                         runtime evidence, often leading to incorrect patches.
                                            To address this limitation, we propose DebugRepair, a self-directed debugging framework for LLM-based
                                         APR. The key idea of DebugRepair is to enhance patch refinement with intermediate runtime evidence collected
                                         through simulated debugging, rather than relying solely on outcome-level failure symptoms. Specifically,
                                         DebugRepair consists of three components. First, test semantic purification extracts the minimal failure-
                                         triggering test context, thereby removing noise in both tests and follow-up debugging logs. Second, simulated
                                         instrumentation enables the LLM to insert targeted debugging statements into buggy functions to collect
                                         runtime traces. A rule-based fallback mechanism is invoked when LLM-instrumented code fails to compile
                                         or semantically introduces inconsistencies. Third, debugging-driven conversational repair organizes patch
                                         ∗ Both authors contributed equally to this research.
                                         † Corresponding author.


                                         Authors’ Contact Information: Linhao Wu, wulinhao@mail.sdu.edu.cn, Shandong University, China; Yifei Pei, peiyifei@
                                         mail.sdu.edu.cn, Shandong University, China; Zhen Yang, zhenyang@sdu.edu.cn, Shandong University, China; Kainan Li,
                                         likainan@mail.sdu.edu.cn, Shandong University, China; Zhonghang Lu, 25213050288@m.fudan.edu.cn, Fudan University,
                                         China; Hao Tan, 202400130169@mail.sdu.edu.cn, Shandong University, China; Xiran Lyu, xiranlyu@mail.sdu.edu.cn,
                                         Shandong University, China; Jia Li, lijia@stu.pku.edu.cn, Tsinghua University, Beijing, China; Yizhou Chen, yizhouchen@
                                         stu.pku.edu.cn, Peking University, China; Pengyu Xue, xuepengyu@mail.sdu.edu.cn, The Hong Kong Polytechnic University,
                                         China; Kunwu Zheng, xiaozhengsdu2022@mail.sdu.edu.cn, Shandong University, China; Dan Hao, haodan@pku.edu.cn,
                                         Peking University, China.

                                         Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee
                                         provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the
                                         full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored.
                                         Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires
                                         prior specific permission and/or a fee. Request permissions from permissions@acm.org.
                                         © 2018 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                         ACM 1557-735X/2018/8-ART111
                                         https://doi.org/XXXXXXX.XXXXXXX


                                                                                                   J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
111:2                                                                                                 Wu et al.


generation into a hierarchical, iterative process, in which the LLM progressively refines candidate patches
using both prior repair attempts and newly observed runtime states.
   We evaluate DebugRepair on three widely used benchmarks across two Programming Languages (PLs), e.g.,
Java and Python. Extensive experiments demonstrate the State-Of-The-Art (SOTA) performance of DebugRe-
pair against 15 representative approaches. For example, with GPT-3.5 as the backbone model, DebugRepair
correctly fixes 224 bugs on Defects4J, achieving an average improvement of 26.2% over SOTA LLM-based
approaches. With DeepSeek-V3, DebugRepair correctly fixes 295 Defects4J bugs, exceeding the second-best
baseline by 59 correct fixes. Across five additional backbone LLMs of different families and sizes, DebugRepair
improves repair performance by 51.3% on average over their vanilla settings, demonstrating its model-agnostic
effectiveness. Further ablation studies confirm that all components of DebugRepair contribute effectively to
the overall repair performance.
CCS Concepts: • Software and its engineering → Software testing and debugging.
Additional Key Words and Phrases: Automated Program Repair, Large Language Models
ACM Reference Format:
Linhao Wu, Yifei Pei, Zhen Yang, Kainan Li, Zhonghang Lu, Hao Tan, Xiran Lyu, Jia Li, Yizhou Chen, Pengyu
Xue, Kunwu Zheng, and Dan Hao. 2018. DebugRepair: Enhancing LLM-Based Automated Program Repair
via Self-Directed Debugging. J. ACM 37, 4, Article 111 (August 2018), 27 pages. https://doi.org/XXXXXXX.
XXXXXXX

1   Introduction
Automated Program Repair (APR) aims to automatically generate patches to fix software bugs [8, 23,
49]. Traditional APR techniques can be broadly categorized into three paradigms: template-based
[9, 12, 27, 30], heuristic-based [13, 21, 22, 34], and constraint-based [7, 20, 29, 31] approaches. With
advances in deep learning, learning-based APR approaches have demonstrated superior generality
by learning code repair patterns from large-scale corpora. These approaches can be primarily
divided into two categories: Neural Machine Translation (NMT)-based approaches and Pre-trained
Language Model (PLM)-based approaches. The former [6, 16, 24, 25] formulates program repair
as a translation task, learning to transform buggy code into correct patches using historical bug-
fixes. Afterwards, leveraging larger-scale training corpora and advanced pre-training algorithms,
PLM-based approaches [32, 35–37] demonstrate much more powerful bug-fixing performance.
   More recently, PLMs have expanded to Large Language Models (LLMs) with billions of parameters
and training data, plus post-training with diverse reinforcement learning techniques to align with
human preferences. As such, their utility has been examined in various software engineering
tasks [39, 41–44], including in the APR area [11, 19, 36, 38, 47, 48]. Specifically, LLM-based APR
techniques can be further broadly categorized into three paradigms: (1) retrieval-based approaches
(e.g., RepairAgent [4] and ReinFix [48]), which utilize external tools, e.g., static analysis and search
mechanisms, to extract relevant repair ingredients and historical fixes for guiding patch generation;
(2) feedback-based approaches (e.g., ChatRepair [38], ContrastRepair [19], and TSAPR [11]), which
perform iterative self-correction to refine candidate patches with test feedback; and (3) hybrid
approaches (e.g., ThinkRepair [47]), which synergistically combine the above two kinds of strategies
for patch generation and refinement.
   This article focuses on the second paradigm of LLM-based APR techniques, i.e., feedback-based
approaches, and tries to resolve one of their significant limitations: the exclusive reliance on
outcome-level failure symptoms, e.g., stack traces, for patch refinement. Although these signals
indicate where and how a failure is observed, they often fail to expose the intermediate runtime
states that causally lead to the failure. In practice, instead of merely relying on stack traces,
developers typically observe program behavior by inserting instrumentation, e.g., print statements,
thereby exposing intermediate runtime states and progressively localizing bug causes. As such, it

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging                          111:3


is imperative to augment LLM-based APR tools with such a debugging-oriented cognitive process,
thereby alleviating their reasoning burden when handling complex bugs.
   To address the above limitation, we propose DebugRepair, a self-directed debugging framework
for LLM-based APR, which consists of three key components: (1) Test Semantic Purification.
In practice, real-world unit tests often encapsulate multiple assertions targeting different testing
scenarios of a focal method, not all of which are responsible for triggering the bug. To reduce
useless debugging logs from executing irrelevant test scenarios in follow-up steps, we perform
static program slicing on the failing test to extract the minimal semantic subset directly related to
the failure. This purified test facilitates the follow-up instrumentation and debugging for LLMs.
(2) Simulated Instrumentation. When the LLM fails to repair a bug using only outcome-level
failure symptoms, DebugRepair proactively guides it into a debugging phase. In this phase, the
LLM autonomously identifies breakpoints and inserts instrumentation (e.g., print statements) along
key execution paths according to the purified test. To ensure robust trace collection, we implement
a hybrid strategy that supplements LLM with a deterministic, rule-based fallback. By executing
the instrumented program, DebugRepair captures intermediate runtime states and transforms
them into structured feedback that guides more precise patch refinement. (3) Debugging-Driven
Conversational Repair. Instead of isolated patch generation, we design a hierarchically iterative,
conversation-driven repair framework to effectively utilize the collected runtime-state feedback.
The outer loop is responsible for simulated instrumentation according to the purified test, while
the inner loop assigns the LLM to refine candidate patches based on both prior fixing and newly
acquired debugging information. The whole process continues until a plausible patch (i.e., one that
passes all tests) is found or the predefined budget is exhausted.
   To evaluate the effectiveness of DebugRepair, we conduct extensive experiments on three distinct
benchmarks: Defects4J (V1.2 and V2.0), QuixBugs, and HumanEval-Java. Specifically, although
DebugRepair follows a feedback-based paradigm of the LLM category, we include 15 baselines for
comparison, covering template-based, learning-based, and LLM-based APR approaches. In particular,
6 of them are recently released SOTA LLM-based approaches across retrieval, feedback, and hybrid-
based paradigms. Experimental results demonstrate that DebugRepair outperforms existing SOTA
baselines. For example, with GPT-3.5 as the backbone model, DebugRepair correctly fixes 224 bugs
on the Defects4J dataset, achieving an average improvement of 26.2% over the SOTA LLM-based
baselines. Meanwhile, when evaluated with the DeepSeek-V3 backbone, DebugRepair continues
to demonstrate its superiority by correctly fixing 295 bugs on the Defects4J dataset, achieving 59
more correct fixes than the second-best approach. Additionally, we implement DebugRepair on five
other LLMs from diverse families and sizes, showing that DebugRepair can fix 51.3% more bugs
than their vanilla settings on average, thereby demonstrating the model-agnostic nature of our
proposal. Furthermore, the follow-up ablation study indicates that both the test purification and
the simulated debugging mechanism play critical roles in enhancing LLMs’ ability to understand
and repair complex bugs. In summary, the main contributions of this paper are as follows:
• Novel Technique. We propose DebugRepair, a novel LLM-based APR framework that enhances
  patch generation via self-directed debugging. Unlike existing feedback-based APR approaches
  that rely mainly on outcome-level failure symptoms, DebugRepair introduces a debugging-
  oriented repair paradigm that equips LLMs with intermediate runtime evidence through test
  semantic purification, simulated instrumentation, and debugging-driven conversational repair.
• Extensive Evaluation. We conduct extensive experiments on three widely used APR bench-
  marks, namely Defects4J, QuixBugs, and HumanEval-Java, against 15 representative baselines
  spanning template-based, learning-based, and LLM-based APR techniques. The results show
  that DebugRepair consistently outperforms existing SOTA approaches across different backbone

                                                  J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
111:4                                                                                                                                                                                            Wu et al.

                   Buggy Function
                                                                                     (a) Chart-24 Bug
                  1: public Paint getPaint(double value) {                                                    Outcome-Level Failure Symptoms
                  2: double v = Math.max(value, this.lowerBound);                                              Java.lang.IllegalArgumentException:
                  3: v = Math.min(v, this.upperBound);                                                             Color parameter outside of expected range: Red Green Blue
                  4: int g = (int) ((value - this.lowerBound) / (this.upperBound
                          - this.lowerBound) * 255.0);
                  5: return new Color(g, g, g);
                  6: }                                             Buggy Position:                                                 Insert print statement
                                         Chart-24
                                                              mistaken reference
                                                              of variable “value”

                   (b) Direct repair with failure symptoms                                                (c) Repair with runtime-state evidence
                                                                                     ···                                           …
                                                                                                                                   System.out.println("//DEBUG: value (input): " + value);
                                                                                     //DEBUG: value (input): -0.5
                     The g value is outside the                                      //DEBUG: v (after clamping): 0.0
                                                                                                                                   System.out.println(“//DEBUG: v (after clamping): " + v);
                                                                                                                                   int g = (int) ((value - this.lowerBound) / (this.upperBound
                     range, so I'll add a clamp.                                     //DEBUG: g (after calculation): -127               - this.lowerBound) * 255.0);
                                                                                     ···                 Runtime Output            System.out.println("//DEBUG: g (after calculation): " + g);
                                                                                                                                   return new Color(g, g, g);
                                                                                                                               }
                  1: public Paint getPaint(double value) {
                  2: double v = Math.max(value, this.lowerBound);                                                             1: public Paint getPaint(double value) {
                  3: v = Math.min(v, this.upperBound);                                                                        2: double v = Math.max(value, this.lowerBound);
                  4: int g = (int) ((value - this.lowerBound) / (this.upperBound                                              3: v = Math.min(v, this.upperBound);
                          - this.lowerBound) * 255.0);                                    Ah! I see! The problem
                                                                                           isn't that the g value is          4: int g = (int) ((v - this.lowerBound) / (this.upperBound
                  5: g = Math.max(0, Math.min(255, g));                                                                              - this.lowerBound) * 255.0);
                  6: return new Color(g, g, g);                                           out of bounds—it's that
                                                                                            g is derived from the             5: return new Color(g, g, g);
                  7: }                                                                                                        6: }
                                                    Incorrect Patch                            wrong variable.                                                 Correct Patch



                                                     Fig. 1. Motivation Example of DebugRepair.


  models. We further perform comprehensive ablation studies to validate the effectiveness of each
  component in the framework.
• Open Science. To facilitate reproducibility and future research, we will release the implementa-
  tion of DebugRepair and detailed repair results in the future version.

2   Motivation
In this section, we present a motivating example from Defects4J (Chart-24 bug) to illustrate the
limitations of relying solely on outcome-level failure symptoms and the necessity of incorporating
runtime-state evidence for effective program repair.
   The Limitation of Outcome-Level Failure Symptoms. Figure 1(a) shows a buggy func-
tion getPaint designed to return an object Color according to a variable v clamped between
lowerBound and upperBound, which is derived from the input parameter Value. However, the
parameter g for constructing Color object erroneously uses the raw input value instead of
the restricted variable v, causing the program to crash with an exception, namely java.lang.
IllegalArgumentException. As shown in Figure 1(b), existing LLM-based APR tools are typically
fed buggy code and the above outcome-level failure symptoms to fix programs. However, such
symptoms only confirm the manifestation of the failure (an invalid color parameter) while con-
cealing the intermediate states, leading LLMs to conclude that g is outside the valid range and to
incorrectly hypothesize that it simply needs to enforce a proper bound. Consequently, this leads
to a plausible but incorrect patch, i.e., explicitly clamping g before sending to the constructor of
Color, shown in Line 5. The incorrect patch merely masks the symptom rather than fixing the
mistaken variable reference of Value in Line 4.
   The Necessity of Debugging. In contrast, consider how a human developer would fix this
bug. As shown in Figure 1(c), they would likely insert print statements to observe the runtime
state, thereby visualizing the intermediate execution trace: value is -0.5, v is evaluated as 0.0, while
g is calculated as -127. By inspecting these runtime values, the root cause becomes immediately
transparent for LLMs: while the variable v is correctly clamped to the legal lower bound (0.0), the
subsequent calculation for g still yields an illegal negative value (-127). This conflict apparently
reveals that g is computed from the raw, negative value (-0.5) rather than the properly restricted
v, thereby helping the LLM generate the correct patch. This example demonstrates that runtime
intermediate states act as a critical bridge between the symptom and the root cause. By enabling
the LLM to proactively insert print statements and analyze the resulting debugging output, rather

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging                            111:5


than passively consuming outcome-level failure symptoms, we can empower the model to precisely
resolve the underlying logic errors.

3     Approach
3.1    Framework Overview
To bridge the gap between the LLM’s understanding of static code and its perception of runtime
behavior, we propose DebugRepair. This is an LLM-based APR framework designed to simulate
the cognitive debugging process of human developers. As shown in Figure 2, the workflow of
DebugRepair consists of three core phases:
• Test Semantic Purification. We perform semantic-level dependency analysis on the original
  failing test to strip away irrelevant test logic and noise, constructing a minimized test. This
  helps the LLM better focus on the current failure and reduce the irrelevant debugging logs in the
  follow-up phases.
• Simulated Instrumentation. For complex bugs that are difficult for LLMs to fix directly, we
  proactively instrument the code using a hybrid strategy that combines LLM-based instrumenta-
  tion with a rule-based fallback to inject print statements at critical code locations. By executing
  the instrumented code within the purified test context, we capture the intermediate states of the
  program execution, thereby facilitating the program repair in follow-up phases.
• Debugging-Driven Conversational Repair. This phase proceeds in a hierarchical and iterative
  fashion, where an outer loop manages the simulated instrumentation and an inner loop performs
  the specific fixing based on the runtime traces generated above. As such, forming a debugging-
  driven multi-turn conversation to simulate human debugging practice.

3.2    Test Semantic Purification
Real-world test cases typically encapsulate multiple assertions and related dependencies to achieve
comprehensive testing coverage. However, not every assertion triggers the current bug, yet retaining
irrelevant ones may introduce noise into logs generated by instrumentation. To mitigate this
interference for subsequent debugging, we propose a Test Semantic Purification approach, detailed
in Algorithm 1.
   Formally, given a failing test method𝑇 parsed into a sequential list of statements 𝑆 = ⟨𝑠 1, 𝑠 2, . . . , 𝑠𝑛 ⟩
alongside the Abstract Syntax Tree (AST) of its enclosing test class C in which 𝑇 is defined, our
objective is to extract a minimal statement subset 𝑇𝑚𝑖𝑛 ⊂ 𝑇 along with its required external depen-
dencies D ⊂ C. The algorithm begins by initializing a statement set Slice to compose 𝑇𝑚𝑖𝑛 and
adding a failure-triggering statement 𝑠 𝑓 𝑎𝑖𝑙 as its first element. Subsequently, we extract all variables
and objects within 𝑠 𝑓 𝑎𝑖𝑙 to form an identifier set, thereby initializing 𝑉𝑟𝑒𝑞 (Lines 1-3). Based on 𝑉𝑟𝑒𝑞 ,
we trace backward anchored at 𝑠 𝑓 𝑎𝑖𝑙 to search dependent statements from 𝑆, thereby expanding
Slice (Lines 5-23). Specifically, for each backward tracing, a preceding statement 𝑠𝑖 is inserted into
the Slice if it satisfies either of the following two criteria (Lines 11-13):
• Direct Data Dependency. If variables or objects explicitly defined or assigned in 𝑠𝑖 (denoted as
  𝑉𝑑𝑒 𝑓 ) overlap with 𝑉𝑟𝑒𝑞 (i.e., 𝑉𝑑𝑒 𝑓 ∩ 𝑉𝑟𝑒𝑞 ≠ ∅), 𝑠𝑖 is inserted in Slice.
• Implicit State Modification. In object-oriented languages such as Java, objects are frequently
  modified via method invocations rather than explicit assignment operators (e.g., dataset.
  addValue(...)). To capture these side effects, if 𝑠𝑖 is a non-assertion statement and the ob-
  jects it utilizes (denoted as 𝑉𝑢𝑠𝑒 ) overlap with 𝑉𝑟𝑒𝑞 (i.e., 𝑉𝑢𝑠𝑒 ∩ 𝑉𝑟𝑒𝑞 ≠ ∅), 𝑠𝑖 is added in Slice.
  Whenever a statement 𝑠𝑖 is added to Slice, variables and objects that exist in it (either for
definition or usage, denoted as 𝑉𝑖 ) are merged into 𝑉𝑟𝑒𝑞 to expand the searching scope of data

                                                    J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
111:6                                                                                                                                                                                                                                                                                            Wu et al.

                (a) Test Semantic Purification                                                                 (b) Simulated Instrumentation                                                                                 (c) Debugging-Driven Conversational Repair
                                                                                                                                                < Max Attempt

                                                                                                                                                                                        Fail
                                                                                                              LLM-based

 contains
                                                                                                                                                                                                                                                   Direct Repair
                                                                                                                                                         …
                                                                                                                                                        System.out.


                  Test Class
                                                                                                                                                        print(x);
                                                                                                                     Insert Print                       System.out.


                                                                                                                      Statement
                                                                                                                                                        print(y);
                                                                                                                                                                                                                        Buggy Function
                                                                                   Buggy Function                                                 Instrumented                  Consistency
                                      Dependency                Purified                                                                            Function                      Check                                                                                           New Session
                                       Analysis               Test Context                                                                                                                                                                                 Feedback
                                                                                                                                                  > Max Attempt                                                                                                                  (> Max Repair
                                                                                                                                                                                              Pass                              d                                                   Round)
                 Failing Test                                                                                                                                                                                              Purified
                                                                                                             Rule-based                                                                                                  Test Context
        public void testCreateCopy3() throws CloneNotSupportedException {                                                                                 …                              …                                                           Debugging
                                                                                                                                                                                                                                                       Repair
                                                                                                                                                         System.out.                    System.out.

           TimeSeries s1 = new TimeSeries("S1");                                                                     Insert Print                        print(x);
                                                                                                                                                         System.out.        or
                                                                                                                                                                                        print(x);
                                                                                                                                                                                        System.out.

           s1.add(new Year(2009), 100.0);                                                                             Statement                          print(y);                      print(y);


           s1.add(new Year(2010), 101.0);
           s1.add(new Year(2011), 102.0);                                                                                                          Rule-based                       Verified
                                                                                                                                                                                                                                                                                         Plausible Patches
           assertEquals(100.0, s1.getMinY(), EPSILON);                                                                                            Instrumented                   Instrumented                               Error
           assertEquals(102.0, s1.getMaxY(), EPSILON);                                                                                               Function                       Function                             Information
                                                              Failure-Triggering
                                                                  Statement                                                                                                                                                                                      Feedback
                TimeSeries s2 = s1.createCopy(0, 1);
                assertEquals(100.0, s2.getMinY(), EPSILON);                                                                                                                                           // Debug …             …

                assertEquals(101.0, s2.getMaxY(), EPSILON);                                                                                                                                                                                          Candidate
                                                                                                                                                                                                      // Debug …            System.out.
                                                                                                                                                                                                                            print(x);

                                                                                                                                                                                                                                                                                             Patch Augment
                                                                                                                                                                                                      // Debug …

                                                                                                                                                                                                                                                       Patch
                                                                                                                                                                                                                            System.out.
                                                                                                                                                                                                      // Debug …            print(y);

                TimeSeries s3 = s1.createCopy(1, 2);
                                                                                                                                                                                                      // Debug …

                                                                                           Print
                assertEquals(101.0, s3.getMinY(), EPSILON);                                                                         Purified                             Run and               Runtime Trace            Instrumented                       < Max Repair
                assertEquals(102.0, s3.getMaxY(), EPSILON);                             Statement                                 Test Context                        Collect Output                                      Function                            Round
            }
                                                               Failing Test         TimeSeries copy = (TimeSeries) super.clone();                                                                                             d                                    Fail
                                                                                    System.out.println("// DEBUG after clone: copy.minY=" + copy.minY                                                                       // Debug …

        public void testCreateCopy3() throws CloneNotSupportedException {                   + ", copy.maxY=" + copy.maxY);                                                ···                                               // Debug …
                                                                                                                                                                                                                                                     Validator
                                                                                                                                                                          // DEBUG after clone: copy.minY=100.0,                                                          Pass
                                                                                                                                                                                                                            // Debug …

           TimeSeries s1 = new TimeSeries("S1");                                    copy.data = new java.util.ArrayList();                                                                                                  // Debug …

                                                                                    for (int index = start; index <= end; index++) {                                      copy.maxY=102.0                                   // Debug …
           s1.add(new Year(2009), 100.0);                                                                                                                                 // DEBUG copied item: index=0, value=100.0,
                                                                                        ···
           s1.add(new Year(2010), 101.0);                                               System.out.println("// DEBUG copied item: index=" + index                         copy.maxY=102.0                                                                                        Plausible
           s1.add(new Year(2011), 102.0);                                                     + ", value=" + item.getValue() + ", copy.maxY=" + copy.maxY);               // DEBUG copied item: index=1, value=101.0,   Runtime Trace                                              Patch
           TimeSeries s2 = s1.createCopy(0, 1);                                      ···                                                                                  copy.maxY=102.0
           assertEquals(101.0, s2.getMaxY(), EPSILON);                              System.out.println("// DEBUG before return: copy.size=" + copy.data.size()            // DEBUG before return: copy.size=2,
       }                                                                                    + ", copy.maxY=" + copy.maxY);                                                copy.maxY=102.0
                                                              Purified Test                                                Instrumented Function                                                  Runtime Trace



                                                                                                              Fig. 2. Overview of DebugRepair.

dependencies (Lines 15 and 17). Besides, since statements that are not dependent on 𝑠 𝑓 𝑎𝑖𝑙 may also
use objects in 𝑉𝑟𝑒𝑞 , making the potentially caused side effects, in turn, affect 𝑠 𝑓 𝑎𝑖𝑙 . Thus, we have to
repeat the traversal iteratively to update Slice and 𝑉𝑟𝑒𝑞 until no new objects appear, i.e., fixing the
changed flag to False in the outer loop (Lines 18-19). To illustrate the necessity of this iterative
mechanism, Figure 3 presents a motivating example, where listB is an alias of listA (L2). In this
snippet, the assertion 𝑠 𝑓 𝑎𝑖𝑙 at L4 fails because the operation listB.add(...) at L3 modifies their
shared object, implicitly affecting listA. When applying our slicing algorithm to this snippet, the
first traversal among the statements preceding 𝑠 𝑓 𝑎𝑖𝑙 (L4) will miss the implicit state modification at
L3, because the object alias listB is not introduced into 𝑉𝑟𝑒𝑞 until L2 is processed. However, the
discovery of listB as a new object at L2 triggers the changed flag from False to True and induces
a second traversal. As such, the algorithm rescans the snippet with the expanded 𝑉𝑟𝑒𝑞 , successfully
capturing the previously missed side effect at L3 and ultimately ensuring a complete Slice.
                                                                                                                                  The first round of traversal                                                                               The second round of traversal
                                                                                                             Line                  ����                          �����                      Action                              Line          ����               �����                  Action
                                          Code Snippet
                                                                                                               L1          {listA, listB}                 {L1, L2, L4}                      Add L1                                  L1    {listA, listB} {L1, L2, L3, L4}           Already in Slice
                   L1: List<String> listA = new ArrayList<>();
                   L2: List<String> listB = listA;                                                                                                                                       Add L2
                                                                                                               L2          {listA, listB}                    {L2, L4}              Set changed = True
                                                                                                                                                                                                                                    L2    {listA, listB} {L1, L2, L3, L4}           Already in Slice
                   L3: listB.add("Bug Trigger!");                                                                                                     在此处键入公式。                                                                                             在此处键入公式。
                                                                                                                                                                                             Skip L3                                                                                      Capture L3
                   L4: assertEquals(1, listA.size()); // s_fail                                                L3               {listA}                           {L4}                                                              L3    {listA, listB} {L1, L2, L3, L4}
                                                                                                                                                                                       (listB ∉ ���� )                                                                                (listB ∈ ���� )

                                                                                                               L4               {listA}                           {L4}                      Add L4                                  L4    {listA, listB}     {L1, L2, L4}           Already in Slice

                                                                                                                                           Slice = {L1, L2, L4}                                                                                 Final Slice = {L1, L2, L3, L4}

                                                                 Fig. 3. An example to illustrate the necessity of repeated traversal.
   Subsequently, we reconstruct the minimal test method, 𝑇𝑚𝑖𝑛 , by preserving the original method
signature of 𝑇 and sequentially assembling the statements retained in Slice according to their
original relative order (Line 24). Furthermore, the reconstructed test method 𝑇𝑚𝑖𝑛 may still reference
class-level fields or call helper methods defined in its enclosing test class C. To construct a complete
testing context without unnecessary noise, we further conduct the follow steps: (1) fetching helper
methods defined in C that are directly or indirectly dependent by 𝑇𝑚𝑖𝑛 ; (2) fetching class-level fields
that are directly or indirectly dependent by 𝑇𝑚𝑖𝑛 . To realize step (1), we maintain a list, namely D𝑚 ,
containing signatures of dependent methods. The initial elements are methods invoked by 𝑇𝑚𝑖𝑛
while defined in 𝐶, namely the direct dependence of 𝑇𝑚𝑖𝑛 (Lines 25-26). Afterwards, we further
iteratively fetch methods in D𝑚 and extract their callees to make intersection with methods defined
in 𝐶, thereby finding indirect dependence of 𝑇𝑚𝑖𝑛 . Signatures of found methods are added to D𝑚 , and
this process continues until the intersection becomes empty (Lines 27-31). To accomplish step (2), we
locate each method definition according to D𝑚 and 𝑇𝑚𝑖𝑛 , extracting their dependent variables and

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging                            111:7


 Algorithm 1: Test Semantic Purification
  Input: 𝑇 : the failing test method, 𝑠 𝑓 𝑎𝑖𝑙 : the failure-triggering statement, C: the AST of the test class
  Output: 𝑇𝑚𝑖𝑛 : the purified test method, D: the set of external dependencies
1 𝑆 := ⟨𝑠 1 , 𝑠 2 , . . . , 𝑠𝑛 ⟩ ← ParseToStatements(𝑇 );         // parse method into a statement sequence
2 𝑆𝑙𝑖𝑐𝑒 := {𝑠 𝑓 𝑎𝑖𝑙 };                                       // initialize slice with the failing statement
3 𝑉𝑟𝑒𝑞 := FetchVarAndObj(𝑠 𝑓 𝑎𝑖𝑙 );                                 // fetch required variables and objects
4 𝑐ℎ𝑎𝑛𝑔𝑒𝑑 := True

5 while 𝑐ℎ𝑎𝑛𝑔𝑒𝑑 do
6     𝑐ℎ𝑎𝑛𝑔𝑒𝑑 := False
7      for 𝑖 := IndexOf(𝑠 𝑓 𝑎𝑖𝑙 , 𝑆) − 1 to 1 do
                                                             // traverse preceding statements backwards
 8        if 𝑠𝑖 ∈ 𝑆𝑙𝑖𝑐𝑒 then
 9             continue
10        end
11       𝑉𝑑𝑒 𝑓 := FetchDefinedVarAndObj(𝑠𝑖 );            // fetch variables or objects defined in 𝑠𝑖
12       𝑉𝑢𝑠𝑒 := FetchUsedObj(𝑠𝑖 );                                       // fetch objects used in 𝑠𝑖
13        if (𝑉𝑑𝑒 𝑓 ∩ 𝑉𝑟𝑒𝑞 ≠ ∅) ∨ (¬IsAssert(𝑠𝑖 ) ∧ 𝑉𝑢𝑠𝑒 ∩ 𝑉𝑟𝑒𝑞 ≠ ∅) then
14             𝑆𝑙𝑖𝑐𝑒 := 𝑆𝑙𝑖𝑐𝑒 ∪ {𝑠𝑖 }
15             𝑉𝑖 := FetchVarAndObj(𝑠𝑖 )
16             𝑉𝑛𝑒𝑤 := 𝑉𝑖 \ 𝑉𝑟𝑒𝑞
17             𝑉𝑟𝑒𝑞 := 𝑉𝑟𝑒𝑞 ∪ 𝑉𝑖
18             if ∃𝑣 ∈ 𝑉𝑛𝑒𝑤 such that IsObject(𝑣) then
19                  𝑐ℎ𝑎𝑛𝑔𝑒𝑑 := True;
20             end
21        end
22    end
23 end
24 𝑇𝑚𝑖𝑛 := Reconstruct(𝑇 , Sort(𝑆𝑙𝑖𝑐𝑒));       // Assemble statements in original execution order
25 𝑀 C := FetchMethodSigs(C);                     // Fetch signatures of all methods defined in 𝐶
26 D𝑚 := FetchCalleeSigs(𝑇𝑚𝑖𝑛 ) ∩ 𝑀 C ;                       // Initial direct dependent methods
27 𝑀𝑛𝑒𝑤 := D𝑚 ;
28 while 𝑀𝑛𝑒𝑤 ≠ ∅ do
29      𝑀𝑛𝑒𝑤 := FetchCalleeSigs(𝑀𝑛𝑒𝑤 ) ∩ 𝑀 C ;     // Find newly discovered indirect dependencies
30      D𝑚 := D𝑚 ∪ 𝑀𝑛𝑒𝑤
31 end
32 𝑉𝑎𝑙𝑙 := FetchVarAndObj(𝑇𝑚𝑖𝑛 ) ∪ FetchVarAndObj(D𝑚 );      // Extract all variables and objects
33 D𝑣 := 𝑉𝑎𝑙𝑙 ∩ FetchDeclaredFields(C);                   // Resolve class-level dependent fields
34 D := FetchDefinitions(D𝑚 , D𝑣 , C);                 // Form the complete external dependencies
35 return ⟨𝑇𝑚𝑖𝑛 , D⟩;                                              // return the purified context




objects. Whereafter, we make an intersection with fields declared in 𝐶 to fetch directly or indirectly
dependent fields of 𝑇𝑚𝑖𝑛 , denoting as D𝑣 . Finally, we fetch those required field declarations and
method definitions according to D𝑚 and D𝑣 from 𝐶, forming the complete external dependencies
𝐷. By stripping away irrelevant contextual noise, this purified context ensures that the subsequent
simulated instrumentation and repair are focused exclusively on the failure-triggering scenario,
while reducing the length of irrelevant logs.

                                                    J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
111:8                                                                                                                                                      Wu et al.


3.3     Simulated Instrumentation
Existing LLM-based APR approaches often rely on outcome-level failure symptoms (e.g., stack
traces), lacking perception of the program’s intermediate runtime states. DebugRepair overcomes
this limitation by inserting instrumentation into original buggy code according to the above purified
test. We formalize this process as follows:
   Breakpoint Prediction. We model breakpoint identification as a prediction task T𝑣 that infers
critical variables V𝑐𝑟𝑖𝑡 essential for deducing the root cause. As such, breakpoints where instrumen-
tation can be guided by V𝑐𝑟𝑖𝑡 . To be specific, the condition of T𝑣 is a crash context, including the puri-
fied test𝑇𝑚𝑖𝑛 alongside its required external dependencies D, the buggy function 𝐹𝑏𝑢𝑔𝑔𝑦 , and the fault
location 𝐿𝑏𝑢𝑔 . This process is driven by an LLM 𝑚, such that V𝑐𝑟𝑖𝑡 = T𝑣 (𝑇𝑚𝑖𝑛 , D, 𝐹𝑏𝑢𝑔𝑔𝑦 , 𝐿𝑏𝑢𝑔 , 𝑚).
   Semantics-Preserving Instrumentation. In this step, we primarily leverage the LLM 𝑚 to
perform the instrumentation injection, denoted as T𝑖𝑛𝑠𝑡 . Given the buggy function 𝐹𝑏𝑢𝑔𝑔𝑦 and the
critical variable set V𝑐𝑟𝑖𝑡 , T𝑖𝑛𝑠𝑡 prompts the LLM to generate an instrumented version 𝐹𝑖𝑛𝑠𝑡 by insert-
ing print statements (e.g., System.out.println) around V𝑐𝑟𝑖𝑡 , i.e., 𝐹𝑖𝑛𝑠𝑡 = T𝑖𝑛𝑠𝑡 (𝐹𝑏𝑢𝑔𝑔𝑦 , V𝑐𝑟𝑖𝑡 , 𝑚).
The detailed insertion instructions are shown in Figure 4.
                                                                    Instrumentation Prompt Template
                            You are a professional Java developer skilled in adding effective debugging print statements to code.

                            Follow the following requirements:
                            1. At the beginning of the function body, must add: System.out.println("START_DEBUG");
                            2. Before the function is about to end, must add: System.out.println("END_DEBUG");
                            3. Add print statements at key positions (after variable assignment, before and after conditional judgments, inside and
                            outside loops, before and after function calls, etc.)
                            4. Print statements should clearly display variable values, execution flow, or conditional results.
                            5. Do not modify the logic, parameters, or return values of the original function.
                            6. Keep the code format neat, and print statements should be properly indented with the surrounding code.
                            7. Only return the complete modified function code without adding any explanations or extra content.
                            8. Every debug print statement’s content must start with "// DEBUG:", for example: System.out.println("// DEBUG: x = " + x);

                            Please add appropriate debugging print statements to the given Java function to help repair bugs:

                                                                                  Buggy Function

                            The following information helps you add the debugging print statements:
                            1) Failing test context:
                                                                                    Test Context
                            2) Error information:

                                                                                  Error Information



                                             Fig. 4. Instrumentation Prompt Template.

   However, LLM-generated instrumentation may introduce unintended edits beyond print state-
ments, such as auxiliary comments or even syntactic errors. To ensure that the instrumented code
preserves the original program semantics, we impose a two-stage consistency check. First, we
perform a line-wise equivalence check between normalized 𝐹𝑖𝑛𝑠𝑡 and 𝐹𝑏𝑢𝑔𝑔𝑦 , where the normal-
ization process Norm(·) denotes a function that removes all print statements and comments from
a given code. Hence, we can confirm that there is no additional statement modified or added to
distort the code logic. Formally, we require:Norm(𝐹𝑖𝑛𝑠𝑡 ) ≡ Norm(𝐹𝑏𝑢𝑔𝑔𝑦 ). Second, we perform a
compilation check on 𝐹𝑖𝑛𝑠𝑡 , because even if the above condition holds, the instrumentation may
still break syntactic correctness. Therefore, we compile 𝐹𝑖𝑛𝑠𝑡 and accept it only if the compilation
succeeds without errors.
   Once the LLM-instrumented code fails the above two-stage consistency check over a pre-defined
maximum attempt limit (𝑀𝑖𝑛𝑠𝑡 ), a deterministic rule-based instrumentation strategy (detailed in
Algorithm 2) will be activated as a fallback. Specifically, given a buggy function 𝐹𝑏𝑢𝑔𝑔𝑦 , we first
parse it into an AST (Line 1) and locate the method declaration node to insert a print statement
with “// START_DEBUG”, as the first statement of 𝐹𝑏𝑢𝑔𝑔𝑦 (Lines 2-3). Next, we continue traversing
the whole AST to insert instrumentation for other critical breakpoints and variables (Lines 4-27).
For each statement of variable initialization or assignment, we fetch all variables involved and
insert a logging statement immediately after it to print the name and value of each variable being
updated (Lines 5-8). For each if statement, we extract the condition expression 𝑐 and insert a
logging statement before it to record both the condition and its specific value (Lines 9-13). To avoid

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging                          111:9


 Algorithm 2: Rule-based Instrumentation
   Input: 𝐹𝑏𝑢𝑔𝑔𝑦 : buggy function
   Output: 𝐹𝑖𝑛𝑠𝑡 : instrumented function
 1 𝑇 := ParseToAST(𝐹𝑏𝑢𝑔𝑔𝑦 )
 2 𝑀 := FetchMethodDecl(𝑇 )
 3 InsertPrintAfter(𝑀, "// START_DEBUG")
 4 foreach 𝑛 ∈ TraverseAST(𝑀) do
 5      if IsVarInitStmt(𝑛) or IsVarAssigStmt(𝑛) then
 6            𝑛𝑎𝑚𝑒𝑠 := FetchVarNames(𝑛)
 7            𝑣𝑎𝑙𝑠 := FetchVarVals(𝑛𝑎𝑚𝑒𝑠)
 8            InsertPrintAfterStmt(𝑛, "// DEBUG [VAR] "+𝑛𝑎𝑚𝑒𝑠.𝑗𝑜𝑖𝑛(",")+" = "+𝑣𝑎𝑙𝑠.𝑗𝑜𝑖𝑛(","))
 9      else if IsIfStmt(𝑛) then
10            𝑐 := FetchConditionExpr(𝑛)
11            (𝑠 1, 𝑠 2, 𝑡) := HandleExpr(𝑐, "// DEBUG [COND] " + ToString(𝑐) + " = ")
12            ReplaceConditionExpr(𝑛, 𝑡)
13            InsertStmtBeforeIf(𝑛, [𝑠 1 ; 𝑠 2 ])
14      else if IsWhileOrForStmt(𝑛) then
15            𝑐 := FetchConditionExpr(𝑛)
16            (𝑠 1, 𝑠 2, 𝑡) := HandleExpr(𝑐, "// DEBUG [LOOP] " + ToString(𝑐) + " = ")
17            ReplaceConditionExpr(𝑛, true);               // Replace the loop condition (c) with true.
18            𝑠 3 := GenConBreakStmt(¬𝑡); // Generate an if-stmt, using non-t as the break condition.
19            InsertStmtAtLoopEntry(𝑛, [𝑠 1 ; 𝑠 2 ; 𝑠 3 ])
20      else if IsReturnStmt(𝑛) then
21            𝑐 := FetchReturnExpr(𝑛)
22            (𝑠 1, 𝑠 2, 𝑡) := HandleExpr(𝑐, "// DEBUG [RETURN] ")
23            ReplaceReturnExpr(𝑛, 𝑡)
24            InsertStmtBeforeReturn(𝑛, [𝑠 1 ; 𝑠 2 ])
25      else if IsEmptyReturnStmt(𝑛) then
26            InsertPrintBeforeReturn(𝑛, "// DEBUG [RETURN] void")
27 end
28 𝑅 := FetchExitPos(𝑀)
29 foreach 𝑟 ∈ 𝑅 do
30      InsertPrintBeforeExit(𝑟, "// END_DEBUG")
31 end
32 𝐹𝑖𝑛𝑠𝑡 := ASTToCode(𝑇 )
33 return 𝐹𝑖𝑛𝑠𝑡

34 Function HandleExpr(𝑐, 𝐿𝑂𝐺):
35      𝑡 := CreateTempVar()
36      𝑠 1 := BuildTempAssignStmt(𝑡, 𝑐)
37      𝑠 2 := GenPrintStmt(𝐿𝑂𝐺 + 𝑡)
38      return 𝑠 1, 𝑠 2, 𝑡
39 return




the unexpected changing of certain variables in 𝑐 owing to the repeated execution, we assign the
value of 𝑐 to a temporal variable 𝑡 for logging, simultaneously replacing 𝑐 with 𝑡 as the condition
expression of the if statement as well. For While and For statements, we still have to resolve the
repeated computation issue during the instrumentation, but we cannot simply replace the loop

                                                  J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
111:10                                                                                        Wu et al.


condition with a temporal variable as If statements, because it will be repeatedly computed to
examine the reachability of loop boundary. Therefore, we first replace the loop condition with True,
and then generate an assignment statement 𝑠 1 from the loop predicate 𝑐 to the temporal variable
𝑡. Afterwards, we generate a logging statement 𝑠 2 printing the loop condition expression and its
associated value. In addition, we further generate a conditional break statement 𝑠 3 using non-𝑡
for judgment, thereby controlling the termination inside the loop. All the above newly generated
statements, namely 𝑠 1 , 𝑠 2 , and 𝑠 3 , are inserted at the loop entry (Lines 14-19). For non-empty
return statements, we extract the return expression 𝑐 and assign its value to a temporal variable
𝑡 for rule-based logging. Likewise, 𝑡 is also used to substitute 𝑐 in the original return statement,
thereby avoiding repeated computation (Lines 20-24). For other empty return statements, i.e., return
statements with no expression after them for function exit only, we insert a fixed logging statement
before them to specify this purpose (Lines 25-26). After all the above instrumentation is completed,
we identify every explicit exit location and insert a fixed logging statement with “// END_DEBUG”
before them, thereby specifying the end of each function (Lines 28-31). Finally, we deserialize
the modified AST back into source code to obtain the instrumented function 𝐹𝑖𝑛𝑠𝑡 (Lines 32-33).
Although this instrumentation cannot uncover targeted state updates for different 𝐹𝑏𝑢𝑔𝑔𝑦 , it still
reveals critical breakpoints and variables that developers commonly inspect during debugging.
Thus, they are still useful in theory as a supplementary to LLM-based instrumentation, especially
when LLM-generated code are uncompilable.
   Runtime Trace Capture. Executing the verified 𝐹𝑖𝑛𝑠𝑡 within the context of ⟨𝑇𝑚𝑖𝑛 , D⟩ produces
a runtime trace:
                                         𝜏𝑟𝑢𝑛𝑡𝑖𝑚𝑒 = ⟨𝑙𝑜𝑔1, . . . , 𝑙𝑜𝑔𝑘 ⟩,
where each log records a critical variable 𝑣 ∈ V𝑐𝑟𝑖𝑡 and its value 𝑣𝑎𝑙 during execution before
𝑠 𝑓 𝑎𝑖𝑙 , thereby helping reveal data flow issues that cannot be identified from outcome-level failure
symptoms alone.

3.4      Debugging-Driven Conversational Repair
Leveraging the captured trace 𝜏𝑟𝑢𝑛𝑡𝑖𝑚𝑒 , DebugRepair initiates a conversational repair process.
Instead of simply repeated sampling or relying on the one-shot generation capability of LLMs,
this phase adopts a debugging logic similar to that of human developers. Specifically, it employs a
closed-loop mechanism of generation, verification, and feedback to allow the LLM to progressively
approximate the correct patch over multi-turn conversations. The core advantage of this strategy is
that it enables the model to utilize negative feedback from historical interactions to correct errors
progressively, rather than starting the repair from scratch each time. To avoid getting stuck in
local optima during patch generation, we design a hierarchical iterative mechanism consisting of
debugging sessions and repair rounds.
   Hierarchical Iteration Strategy. Let 𝑁𝑠𝑒𝑠𝑠𝑖𝑜𝑛 denote the maximum number of debugging
sessions, and 𝐾𝑟𝑜𝑢𝑛𝑑 denote the maximum repair rounds within a single session. The process
proceeds as follows:
• Session Initialization via Direct Repair. At the beginning of each session, the LLM first
  attempts a direct repair using a basic prompt that contains the buggy function 𝐹𝑏𝑢𝑔𝑔𝑦 and the
  outcome-level failure symptoms. If this initial attempt yields a plausible patch, the session
  terminates. However, if the generated patch (denoted as 𝑃 0 ) fails the verification, DebugRepair
  captures the corresponding error message 𝐸 0 and transitions into the debugging mode for the
  subsequent rounds.
• Debugging-Augmented Prompting. Once the direct repair fails, we construct a comprehensive
  prompt for the debugging rounds. This augmented context incorporates the buggy function

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging                                                                                                                                          111:11

                                                                                       public final void translate(CharSequence input, Writer out) throws IOException {
                                  Repair Prompt Template                                    if (out == null) {




                                                                                                                                                                                     Buggy Function
                                                                                                throw new IllegalArgumentException("The Writer must not be null");
                 You are a helpful assistant that fixes Java code.                          }
                                                                                            ...
                 The following Java function contains a bug:                                for (int pt = 0; pt < consumed; pt++) {
                                                                                                  pos += Character.charCount(Character.codePointAt(input, pos)); // Buggy Location
                                                                                              }
                                         Buggy Function                                }

                                                                                        // Failing Test #1: testEscapeSurrogatePairs
                 Buggy lines are marked with '// Buggy Line' as hints. The actual


                                                                                                                                                                                     Test Context
                                                                                       @Test
                 fix may involve changes around these lines or adding new
                                                                                       public void testEscapeSurrogatePairs() throws Exception {
                 statements if necessary.
                                                                                           assertEquals("\uD83D\uDE30", StringEscapeUtils.escapeCsv("\uD83D\uDE30"));
                                                                                       }
                 The following information helps you repair the bug:
                                                                                       This test relies on the following external methods: ...
                 1) Failing test context:
                                                                                       This test depends on these external fields/variables: ...
                                           Test Context

                                                                                                                                                                                     Error Info
                                                                                       [Test] testEscapeSurrogatePairs
                                                                                       [Class] org.apache.commons.lang3.StringUtilsTest
                 2) Error information:                                                 [Failure line] assertEquals("\uD83D\uDE30", StringEscapeUtils.escapeCsv("\uD83D\uDE30"));
                                                                                       [Failure message] java.lang.StringIndexOutOfBoundsException: String index out of range: 2
                                         Error Information
                                                                                       public final void translate(CharSequence input, Writer out) throws IOException {




                                                                                                                                                                                     Instrumented Function and Runtime Trace
                                                                                           System.out.println("// START_DEBUG");
                 3) The buggy method, with debug prints and runtime output                 ...
                 comments:                                                                 int pos = 0;
                                                                                           int len = input.length();
                                         Instrumented Function                             System.out.println("// DEBUG: initial pos=" + pos + ", len=" + len);
                                           and Runtime Trace                               while (pos < len) {
                                                                                               System.out.println("// DEBUG: entering while loop, pos=" + pos + ", len=" + len);
                  4) Feedback on the previous attempt:                                         int consumed = translate(input, pos, out);
                                                                                               System.out.println("// DEBUG: after translate(), consumed=" + consumed);
                                                                                           ...
                                                         Previous Incorrect Patch      Debug output from failing tests ：
                             Feedback                                                  // START_DEBUG
                                                            Error information
                                                                                       // DEBUG: initial pos=0, len=2
                                                                                       // DEBUG: entering while loop, pos=0, len=2
                 Based on all the information above, please provide a correct fix      // DEBUG: after translate(), consumed=2
                 for the bug.                                                          ......
                 Your response must enclose the entire function within a ```java ...   // There was 1 failure:
                 ``` block.                                                            // 1) testEscapeSurrogatePairs(org.apache.commons.lang3.StringUtilsTest)
                                                                                       // java.lang.StringIndexOutOfBoundsException: String index out of range: 2



                                                Fig. 5. Illustration of the Prompt Construction.




  𝐹𝑏𝑢𝑔𝑔𝑦 , its instrumented version 𝐹𝑖𝑛𝑠𝑡 , the purified test context ⟨𝑇𝑚𝑖𝑛 , D⟩, the serialized dynamic
  trace 𝜏𝑟𝑢𝑛𝑡𝑖𝑚𝑒 , as well as the initial failed patch 𝑃0 and its corresponding error message 𝐸 0 . The
  specific repair prompt is shown in Figure 5. This comprehensive context enables the LLM to
  perform evidence-based reasoning, deducing logic errors by contrasting observed runtime values
  against expected behaviors rather than relying solely on outcome-level failure symptoms.
• Augmenting with Feedback History. In each subsequent round 𝑘 (where 1 ≤ 𝑘 < 𝐾𝑟𝑜𝑢𝑛𝑑 ), the
  LLM generates a candidate patch 𝑃𝑘 based on the above augmented context and the feedback
  history. If 𝑃𝑘 fails verification, the framework captures the specific failure symptoms, including
  the compilation or runtime errors. We then collect the conversation information ⟨𝑃𝑘 , 𝐸𝑘 ⟩ and
  append it to the feedback history. The LLM utilizes this updated history to generate a refined
  patch 𝑃𝑘+1 in the next round. This iterative correction continues until a plausible patch is found
  or the iteration limit 𝐾𝑟𝑜𝑢𝑛𝑑 is reached.
• Session-Level Re-Debugging. If a plausible patch is not found after 𝐾𝑟𝑜𝑢𝑛𝑑 attempts, it implies
  that the current debugging information might be insufficient or misleading. Consequently, the
  framework terminates the current session, discards the conversation history, and triggers a
  new debugging session to capture a fresh dynamic trace. The whole process terminates when a
  plausible patch is found or the global budget (𝑁𝑠𝑒𝑠𝑠𝑖𝑜𝑛 × 𝐾𝑟𝑜𝑢𝑛𝑑 ) is exhausted.

   Patch Augmentation. While an initial plausible patch can successfully pass the entire test
suite, it may not always represent the semantically correct fix. This discrepancy frequently arises
from test overfitting, as incomplete test suites may fail to cover all intended program behaviors. To
mitigate this risk, following prior APR work [19, 38], we introduce a patch augmentation module.
Instead of restarting the repair process from scratch, DebugRepair leverages the generated plausible
patch as a valuable reference, given that both plausible and correct patches share the characteristic
of satisfying the available test suite. Specifically, we instruct the LLM to generate alternative
variants that are logically similar to the initial plausible patch but implemented differently. All
newly generated variations are subsequently validated against the test suite. Finally, DebugRepair
outputs a set of plausible patches.

                                                                                       J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
111:12                                                                                            Wu et al.


4     Experimental Setup
4.1      Research Questions
We evaluate DebugRepair on the following research questions (RQs):
• RQ1: How does DebugRepair perform in comparison with SOTA APR techniques? This
  question evaluates the overall repair effectiveness of DebugRepair and compares its performance
  against existing SOTA APR baselines across diverse datasets.
• RQ2: How does DebugRepair perform across different repair scenarios? This question
  investigates DebugRepair’s performance in three distinct repair scenarios (i.e., single-function,
  single-hunk, and single-line bugs).
• RQ3: To what extent does DebugRepair improve the repair effectiveness of vanilla LLMs
  for APR? This question investigates the generality of DebugRepair across different backbone
  LLMs of diverse families and sizes.
• RQ4: What are the contributions of different components of DebugRepair in improving
  repair effectiveness? This question investigates the individual contribution of key components
  of DebugRepair on the overall repair effectiveness.
• RQ5: How well does DebugRepair generalize to bugs introduced after the LLM training
  data cutoff? Considering the potential data leakage risk caused by LLMs, this question evalu-
  ates DebugRepair’s generalization ability by assessing its performance on recent bugs that are
  guaranteed to be unseen during LLMs’ pre-training.

4.2      Benchmarks
To evaluate repair effectiveness, we conduct experiments on two widely adopted benchmarks:
Defects4J [18] and QuixBugs [26]. Following prior APR studies [11, 36, 38, 40, 47, 48], we divide
Defects4J into two versions: V1.2 and V2.0. Defects4J-V1.2 contains 391 real-world bugs, while
Defects4J-V2.0 introduces an additional 438 new bugs. QuixBugs is a smaller yet popular benchmark,
comprising 40 function-level bugs with both Java and Python versions. Consistent with existing
work [11, 38, 47, 50], we further categorize all bugs into three repair scenarios: Single-Function
(SF), Single-Hunk (SH), and Single-Line (SL). Note that the single-line category is a subset of the
single-hunk category, and the single-hunk category is a subset of the single-function category. In
QuixBugs-Java, all single-hunk bugs correspond to single-line fixes, while in QuixBugs-Python, all
fixes are single-line. Detailed statistics for each repair scenario are reported in Table 1.
   Additionally, to assess generalizability, we further include the HumanEval-Java [14] benchmark,
which consists of 163 single-hunk bug cases. HumanEval-Java is released after the data collection
period used to train GPT-3.5 [1], thereby reducing the potential risk of data leakage. In this bench-
mark, developers convert Python programs from HumanEval [5] together with their corresponding
test cases into Java implementations and JUnit test cases, and then deliberately inject some bugs
into these correct Java programs.

                                     Table 1. Statistics of Studied Benchmarks.
                            Benchmarks         # Total Bugs   # SF Bugs   # SH Bugs   # SL Bugs
                            Defects4J-V1.2          391          255         154         80
                            Defects4J-V2.0          438          228         159         78
                            QuixBugs-Java           40           40          37          37
                            QuixBugs-Python         40           40          40          40
                            HumanEval-Java          163          163         163         74




J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging                         111:13


4.3    Baselines
To make a comprehensive evaluation on Defects4J and QuixBugs, we compare DebugRepair against
15 SOTA baselines across different categories, including eight learning-based approaches (CURE
[16], Recoder [50], SelfAPR [45], RewardRepair [46], KNOD [15], AlphaRepair [37], FitRepair [35],
and RAP-Gen [32]), and one template-based traditional method (TBar [28]). Furthermore, we include
six LLM-based approaches, which are categorized into three distinct subgroups: feedback-based
approaches (ChatRepair [38], ContrastRepair [19], and TSAPR [11]), retrieval-based approaches
(RepairAgent [4] and ReinFix [48]), and hybrid approaches (ThinkRepair [47]). Additionally, follow-
ing prior work [19, 38, 47], we create an LLM-based baseline named BaseChatGPT, which directly
uses a basic prompt without providing additional feedback, serving as a foundational comparison.
Following the common practice in the APR community [19, 35, 37, 38, 47, 50], we report the results
provided by their original papers.


4.4    Evaluation Metrics
Following previous work [11, 15, 16, 19, 47, 48], we consider two widely used metrics to evaluate
the effectiveness of both DebugRepair and baselines:

• Number of Plausible Fixes (# Plausible): Counts the number of bugs which can pass all the
  test cases after fixing, without further verification.
• Number of Correct Fixes (# Correct): Measures the number of programs that are successfully
  fixed based on a manual review of the generated plausible patches.


4.5    Implementation
For our experiments, we primarily adopt gpt-3.5-turbo (referred to as GPT-3.5) [1] as the backbone
model for DebugRepair, using the API provided by OpenAI. Additionally, we further incorporate
four other LLMs (including DeepSeek-V3, Qwen2.5-7B, Qwen2.5-Coder-7B, and Qwen2.5-32B),
all using APIs provided by SiliconFlow [2]. These models cover a wide range of architectures and
parameter sizes, enabling a comprehensive evaluation across different LLM backbones. Following
prior work [19, 38, 47, 48], a sampling temperature of 1.0 is utilized to obtain a diverse set of
potential patches. For Fault Localization (FL), to avoid potential biases introduced by FL tools,
we align with recent studies [11, 19, 38, 47, 48] and adopt the perfect fault localization setting.
Regarding the repair budget, we configure the number of debugging sessions (𝑁𝑠𝑒𝑠𝑠𝑖𝑜𝑛 ) to 6, with a
maximum of 4 repair rounds (𝐾𝑟𝑜𝑢𝑛𝑑 ) per session. We further allow 8 additional queries in the patch
augmentation stage. As a result, the maximum number of candidate patches explored for each bug
is bounded by 32 (i.e., patch size = 6 × 4 + 8). Additionally, we set the maximum attempt threshold
for the LLM instrumentation step (𝑀𝑖𝑛𝑠𝑡 ) to 10. All experimental evaluations are conducted on a
server running Ubuntu 20.04 with two Intel Xeon Gold 6138 CPUs and 251 GB of RAM. AST-based
parsing and code manipulation for both Java and Python programs are implemented using the
tree-sitter [3].


5     Experimental Results
In this section, we present the experimental results to answer the research questions formulated
in Section 4.1. We systematically evaluate the effectiveness, robustness, and generalizability of
DebugRepair on widely used benchmarks (Defects4J, QuixBugs, and HumanEval-Java).

                                                  J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
111:14                                                                                                             Wu et al.


5.1      RQ1: Comparison with SOTA Approaches
To answer RQ1, we evaluate the overall repair effectiveness of DebugRepair by comparing it against
15 SOTA baselines on the Defects4J and QuixBugs benchmarks. Table 2 presents the comparative
results in terms of the number of plausible and correct patches.
  Table 2. Comparison of DebugRepair and baselines on Defects4J and QuixBugs (# Correct/# Plausible).

                                                                                    Defects4J                 QuixBugs
              Category                 APR Approach        Patch Size
                                                                          V1.2        V2.0        Total     Java     Python
           Template-based                 TBar [28]             -         68/95       8/25       76/120       -          -
                                         CURE [16]            5000         57/-        19/-        76/-      26          -
                                        Recoder [50]          100          71/-       19/46        90/-      31          -
                    NMT-based           SelfAPR [45]           150        65/74       45/47      110/121      -          -
                                         KNOD [15]            1000        71/85       50/85      121/170     25          -
Learning-based
                                      RewardRepair [46]        200         45/-        45/-        90/-      20          -
                                      AlphaRepair [37]        5000       74/109       36/-        110/-      28        27
                     PLM-based         FitRepair [35]         4000        89/-        44/-        133/-       -         -
                                       RAP-Gen [32]             -         72/-        53/-        125/-       -         -
                         Basic          BaseChatGPT            32        75/104      67/100      142/204     33        32
                                       RepairAgent [4]        117         92/96       72/90      164/186      -          -
                   Retrieval-based
                                        ReinFix [48]          45          104/-       109/-       213/-       -          -
  LLM-based
                         Hybrid       ThinkRepair [47]        125         98/-        107/-       205/-      39        40
                                      ChatRepair [38]         500        114/-        48/-       162/-       39        40
                                     ContrastRepair [19]      160        103/-        40/-      143/201      40        40
                   Feedback-based
                                        TSAPR [10]            32        108/146      93/134     201/280      40         -
                                       DebugRepair            32        111/146     113/137     224/283      40        40
   Φ “-” indicates no results reported in the original work. In addition, the highest numbers of plausible and correct fixes

   are highlighted in bold.

   Results on Defects4J. As presented in Table 2, DebugRepair demonstrates superior repair
capabilities, correctly fixing a total of 224 bugs on the Defects4J dataset, where versions 1.2 and 2.0
account for 111 and 113 fixes, respectively. Compared with ReinFix, the second-ranked approach,
DebugRepair successfully fixes 11 additional bugs with a smaller patch size for patch generation. In
the realm of feedback-based APR, DebugRepair exhibits substantial performance gains with fewer
or equal patch sizes. It correctly fixes 62 and 81 more bugs than ChatRepair and ContrastRepair,
representing improvements of 38.3% and 56.6%, respectively. Furthermore, it fixes 23 more bugs
than TSAPR, an 11.44% increase over that tool’s strong baseline of 201 fixes. Furthermore, our
approach substantially outperforms conventional learning-based approaches, achieving 85.1%–
194.7% more correct fixes while requiring only 1/3 to 1/156 of the patch sizes. Regarding bug-fixes
across different projects (as shown in Table 3), DebugRepair exhibits the highest performance on
7 out of 17 projects, excelling the second-ranked approaches (i.e., TSAPR and ThinkRepair) by 4,
demonstrating its robust and dominant performance. For example, it generates 37 correct fixes in the
Math project, 29 in JacksonDataBind, 27 in Lang, and 18 in Compress, significantly outperforming
all other tools in these projects. These results demonstrate the effectiveness of DebugRepair in
APR. Additionally, to make comparisons on the latest LLMs, we manually reproduced six LLM-
based baselines (i.e., ChatRepair, ContrastRepair, ThinkRepair, RepairAgent, TSAPR, and ReinFix)
on Defects4J using DeepSeek-V3 as the backbone model. The experimental results indicate that
DebugRepair continues to exhibit superior performance, successfully fixing 59 more bugs than the
most competitive counterpart, namely ReinFix.
   Results on QuixBugs. We further evaluate DebugRepair on the QuixBugs benchmark. The
results show that DebugRepair is capable of correctly fixing all 40 bugs in both the Java and Python

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging                                                                                                                   111:15


                              Table 3. Number of correct fixes across different projects on Defects4J.

  Approach       Chart    Closure         Lang     Math          Mockito          Time        Cli   Codec   Collect   Compress    Csv     Gson          Core   Databind             Xml   Jsoup   JxPath   Total
   # Bugs         26          174             63       106               38            26      39    18       4          47        16         18         26        112               6      93     22      835
 RepairAgent      11          27              17        29               6             2        8     9       1          10        6           3         5         11                1     18       0      164
 ThinkRepair      11          34              19        27               6             4        9    10       0          16        8           5         7         17                2     28       2      205
 ChatRepair       15          37              21        32               6             3        5     8       0           2        3           3         3          9                1     14       0      162
ContrastRepair    12          32              19        30               8             2        4     5       0          2         3           1         3         7                 1     14       0      143
   TSAPR          12          28              24        32               8             4       12     5       0          15        7           4         4         18                1     26       1      201
 DebugRepair      12          25              27        37               7             4       10     8       0         18         7          6          4         29                2      27      1      224

    Φ Note that ReinFix is excluded from this specific comparison because its GPT-3.5 performance under the single-function

   (SF) repair scenario across specific projects is neither reported nor open-sourced. In addition, the highest numbers of
   correct fixes are highlighted in bold. Besides, Core is short for JacksonCore, Xml is short for JacksonXml, Databind is
   short for JacksonDatabind, and Collect is short for Collections.

datasets. This exceptional performance matches the best results achieved by existing SOTA baselines,
indicating that the framework operates effectively across different programming languages and
datasets.
   Unique Fix Analysis. To better illustrate the distinct repair capabilities of DebugRepair, we
conduct an overlap analysis of the correct fixes using Venn diagrams. Specifically, we present
two groups of comparisons: one against three representative baselines (RepairAgent, ThinkRepair,
and BaseChatGPT), and another against feedback-based baselines (ChatRepair, ContrastRepair,
and TSAPR). For the first group, we compare DebugRepair with RepairAgent, ThinkRepair, and
BaseChatGPT (excluding ReinFix, as its detailed results under the GPT-3.5 backbone are not publicly
available). As shown in Figure 6(a) and 6(b), 33 and 20 bugs on Defects4J-V1.2 and V2.0, respectively,
can be successfully repaired by all these approaches. This overlap indicates that these approaches
are highly effective and exhibit considerable similarity in their repair capabilities, largely because
they are implemented on the same backbone model. Despite that, DebugRepair is still able to
uniquely fix 27 and 22 bugs on Defects4J-V1.2 and V2.0, respectively, which are not fixed by any
of these other approaches, and ranks first in unique fixes. For the second group, we analyze the
overlap results among feedback-based baselines, including ChatRepair, ContrastRepair, and TSAPR.
As shown in Figure 7(a) and 7(b), 56 and 24 bugs on Defects4J-V1.2 and V2.0, respectively, can
be successfully repaired by all these approaches, again indicating a considerable overlap in their
repair capabilities. Meanwhile, DebugRepair fixes the largest number of bugs that remain unfixed
by the others, contributing 17 and 39 unique fixes on V1.2 and V2.0, respectively. These results
highlight the unique advantage of DebugRepair. In fact, since DebugRepair specifically focuses on
patch refinement via dynamic debugging, it can be easily integrated into most existing APR tools,
making it a strong complement to existing work.

                   RepairAgent                               ThinkRepair                                                  RepairAgent                          ThinkRepair
                                     23                              8                                                                    16                           20
        DebugRepair                                7                                        BaseChatGPT        DebugRepair                               5                                BaseChatGPT
                               4                                              3                                                     10                                          7

                                         13                      6                                                                            15                   3

                         27                        33
                                                                                  11                                          22                         20
                                                                                                                                                                                     4


                                    14                                   2                                                               14                                 1
                                              14             2                                                                                     23          4
                                                   4                                                                                                     5



                          (a) Venn on Defects4J-V1.2                                                                             (b) Venn on Defects4J-V2.0
     Fig. 6. Bug Fix Venn Diagram on Defects4J (DebugRepair, RepairAgent, ThinkRepair, BaseChatGPT)



                                                                                                      J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
111:16                                                                                                                                                                     Wu et al.


                       ChatRepair                         ContrastRepair                               ChatRepair                        ContrastRepair
                                        8                           3                                                   1                         1
             DebugRepair                             8                               TSAPR   DebugRepair                            4                              TSAPR
                                2                                           1                                   3                                         1

                                            14                 16                                                           3                 5

                           17                        56
                                                                                10                         39                       24
                                                                                                                                                              21


                                    3                                   4                                           1                                 1
                                                 3         6                                                                    1         7
                                                     10                                                                             35



                       (a) Venn on Defects4J-V1.2                                                      (b) Venn on Defects4J-V2.0
         Fig. 7. Bug Fix Venn Diagram on Defects4J (DebugRepair, ChatRepair, ContrastRepair, TSAPR)


   Case Study. To further illustrate the effectiveness of DebugRepair, we present a case study on the
Lang-6 bug from Defects4J, as shown in Figure 8. DebugRepair successfully generates a correct patch
for this bug, whereas all six LLM-based baselines fail. This bug occurs in a character processing
utility of Apache Commons Lang. In the loop, the variable pos is repeatedly used as the index of
Character.codePointAt(input, pos). As pos is incremented across iterations, it may eventually
exceed the valid index range of input, leading to a StringIndexOutOfBoundsException. Using
TSAPR as a representative baseline, the repair process can explore and optimize multiple promising
patch candidates via Monte Carlo Tree Search (MCTS), guided by execution feedback. However,
the feedback it uses is still limited to outcome-level symptoms, without exposing the intermediate
runtime states needed to understand how pos evolves during loop execution. As a result, even
though TSAPR can search over multiple high-quality candidates, all of its attempts still fail to
identify the root cause and produce only incorrect modifications, such as changing the index from
pos to pos + 1. In contrast, DebugRepair explicitly instruments the buggy function and observes
the runtime values of pos during repeated calls to codePointAt. These debugging traces reveal
how pos increases step by step until it reaches an invalid boundary, enabling the model to directly
localize the faulty increment logic. Based on this dynamic evidence, DebugRepair generates the
correct fix by inserting a boundary check before the codePointAt call and updating pos using
the retrieved code point. Notably, unlike TSAPR, which searches over multiple patch candidates
without success, DebugRepair only needs to iteratively debug a single candidate for a few rounds.
This example highlights the key advantage of DebugRepair: dynamic execution states provide more
informative guidance than static outcome-level feedback for repairing complex logic bugs.

 x Answer to RQ1: DebugRepair outperforms all SOTA baselines. Specifically, it fixes 111 bugs on Defects4J-
 V1.2, 113 bugs on Defects4J-V2.0 and all 40 bugs on QuixBugs, respectively.

5.2      RQ2: Performance Across Repair Scenarios
To evaluate the robustness of DebugRepair, we investigate its performance across different dimen-
sions of bug complexity: Single-Function (SF), Single-Hunk (SH), and Single-Line (SL) scenarios.
Since the results from RQ1 demonstrate that LLM-based approaches achieve SOTA performance and
outperform traditional and earlier learning-based approaches, we focus our comparative analysis
in this section exclusively on these LLM-based baselines. Table 4 presents the comparative results
on the Defects4J and QuixBugs datasets, where GPT-3.5 is integrated as the backbone LLM for each
approach. We also adopt DeepSeek-V3 as a backbone LLM for experiments in this RQ.
    As shown in Table 4, DebugRepair demonstrates superiority in handling complex repair scenarios
(i.e., SF and SH bugs), consistently performing at the SOTA level. In these complex settings under the

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging                                                                                                                            111:17
             Buggy Function                                                                                         TSAPR
             ...
                     while (pos < len) {                                                                            ...
                                                                                                                            for (int pt = 0; pt < consumed; pt++) {
                        int consumed = translate(input, pos, out);
                                                                                                                    -          pos += Character.charCount(Character.codePointAt(input, pos));
                        if (consumed == 0) {
                                                                                                                    +          pos += Character.charCount(Character.codePointAt(input, pos + 1));
                            char[] c = Character.toChars(Character.codePointAt(input, pos));
                                                                                                                            }
                            out.write(c);                                                               LLM Fix         }
                            pos+= c.length;
                                                                                                                    }                                                         Incorrect Patch
                            continue;
                        }
                     for (int pt = 0; pt < consumed; pt++) {
                        pos += Character.charCount(Character.codePointAt(input, pos)); // Buggy Line               Run and collect runtime output
                     }
                 }
             }                                                                                                          Runtime Output
                                                                                                                          ...                                                          Based on this output,
                                                                 Insert Print Statement                                   // DEBUG: entering while loop, pos=0, len=2                    the LLM can infer
                                                                                                                          // DEBUG: after translate(), consumed=2                      that the index range
             Instrumented Function                                                                                                                                                      in this trigger test
                                                                                                                          // DEBUG: processing consumed characters (2)
             ...                                                                                                                                                                           should be 2.
                                                                                                                          // DEBUG: processing pt=0, current pos=0
             while (pos < len) {
              + System.out.println("// DEBUG: entering while loop, pos=" + pos + ", len=" + len);   1                     // DEBUG: updated pos=2
                  int consumed = translate(input, pos, out);                                                              // DEBUG: processing pt=1, current pos=2
              + System.out.println("// DEBUG: after translate(), consumed=" + consumed);              1                                                                              The LLM can observe
                  if (consumed == 0) {                                                                                                                                             that the program crashes
              +       System.out.println("// DEBUG: consumed is 0, writing character directly");     1                                                                             after this output, thereby
                      char[] c = Character.toChars(Character.codePointAt(input, pos));                                                               LLM Fix                         pinpointing the exact
              +       System.out.println("// DEBUG: character array length=" + c.length);             1                                                                              location of the index
                      out.write(c);                                                                                                                                                   out-of-range error.
                      pos += c.length;
              +       System.out.println("// DEBUG: updated pos=" + pos);                             1           DebugRepair
                      continue;                                                                                   ...
                  }                                                                                               for (int pt = 0; pt < consumed; pt++) {
              + System.out.println("// DEBUG: processing consumed characters (" + consumed + ")"); 1                -       pos += Character.charCount(Character.codePointAt(input, pos)); 1
                  for (int pt = 0; pt < consumed; pt++) {                                                          +        if (pos >= len) {                                              1
              +       System.out.println("// DEBUG: processing pt=" + pt + ", current pos=" + pos);   1            +            break;                                                     1
                      pos += Character.charCount(Character.codePointAt(input, pos));                               +        }                                                              1
              +       System.out.println("// DEBUG: updated pos=" + pos);                             1            +        int codepoint = Character.codePointAt(input, pos);             1
                  }                                                                                                +        pos += Character.charCount(codepoint);                         1
                }                                                                                                       }
              + System.out.println("// END_DEBUG");                                                 1                 }
             }                                                                                                    }                                                            Correct Patch




              Fig. 8. An illustration of the self-directed debugging process on the Lang-6 bug.
Table 4. Repair results of different repair scenarios for DebugRepair and baselines on Defects4J and QuixBugs
(# Correct/# Plausible).

                                                                                                           Defects4J                                                                                QuixBugs
   Category                  APR Approach
                                                                           Defects4J-V1.2                                            Defects4J-V2.0                                           Java              Python
                                                                    SF                  SH                SL                 SF                   SH                 SL               SF                SH        SF
     Basic                    BaseChatGPT                       75/104                56/74             36/45             67/100               49/73              31/44             33/36             33/36     32/37
                               RepairAgent                         80/-                68/-              49/-                65/-                62/-              45/-                 -                  -      -
Retrieval-based
                                 ReinFix                          104/-                78/-              53/-               109/-                85/-              47/-                 -                  -      -
    Hybrid                     ThinkRepair                         98/-                78/-              52/-               107/-                81/-              47/-              39/-              36/-      40/-
                               ChatRepair                        76/-                79/-                57/-               -                    -                 48/-             39/-               37/-      40/-
                             ContrastRepair                     75/120              69/102              56/60               -                    -                 40/-             40/-                -        40/-
Feedback-based
                                TSAPR                          108/146              86/104              57/64            93/134               77/102              45/55             40/-                -         -
                              DebugRepair                      111/146              82/102              55/61           113/137               83/100              50/55            40/40              37/37     40/40
  Φ “-” indicates no results reported in the original work. In addition, the highest numbers of plausible and correct fixes

  are highlighted in bold, while the second-ranked ones are highlighted in underlines.


GPT-3.5 backbone, DebugRepair frequently outperforms the top-performing LLM-based approaches,
such as ReinFix and TSAPR. For example, on Defects4J-V1.2, DebugRepair achieves the highest
number of SF fixes (111), directly outperforming TSAPR (108) and ReinFix (104). On Defects4J-V2.0,
DebugRepair further solidifies its lead in the SF scenario by fixing 113 bugs, surpassing ReinFix
(109) and TSAPR (93). In the SH scenarios, DebugRepair maintains highly competitive performance,
fixing 82 and 83 bugs on V1.2 and V2.0, respectively, closely rivaling the top baseline results in
these categories (86 for TSAPR on V1.2, and 85 for ReinFix on V2.0). As a feedback-based approach,
DebugRepair can be utilized by ReinFix for patch refinement owing to their orthogonal working
mechanisms. As for TSAPR, although it follows the same paradigm of utilizing execution feedback
as DebugRepair, ChatRepair, and ContrastRepair, its underlying design philosophy is different.
Specifically, TSAPR concentrates on utilizing feedback to guide an MCTS for patch exploration.
In contrast, approaches such as ChatRepair, ContrastRepair, and DebugRepair focus directly on
the iterative refinement of a given candidate patch. Hence, the latter category is also orthogonal

                                                                                                       J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
111:18                                                                                              Wu et al.


to TSAPR and can be integrated into it for further improvement during the patch refinement.
Under this refinement-oriented philosophy, DebugRepair significantly outperforms ChatRepair and
ContrastRepair, where it correctly fixes 111 SF and 82 SH bugs on Defects4J-V1.2, while ChatRepair
and ContrastRepair only correctly fix 75 SF and 69 SH bugs, as well as 76 SF and 79 SH bugs,
respectively.
   This effectiveness in complex repairs is further corroborated by the results on the QuixBugs
benchmark, where DebugRepair successfully fixes 100% of the SF and SH bugs. Furthermore,
the experiments conducted with the DeepSeek-V3 backbone confirm that this advantage scales
exceptionally well. Powered by DeepSeek-V3, DebugRepair achieves a commanding lead in complex
scenarios, including against the best-performing approaches, namely ReinFix and TSAPR. To be
specific, DebugRepair correctly fixes 139 and 156 SF bugs on Defects4J V1.2 and V2.0, respectively,
substantially outperforming ReinFix (118 and 118) and TSAPR (108 and 116). A similar dominance
is observed in the SH scenarios, where 98 and 113 fixes for DebugRepair versus 83 and 89 for
the second-ranked approach, i.e., ReinFix. Importantly, because DebugRepair specifically targets
the patch refinement through dynamic execution states, its mechanism is highly orthogonal to
existing APR tools, such as ReinFix and TSAPR. This orthogonality indicates a strong potential for
integrating these approaches in the future to further boost repair performance.
   In the simpler Single-Line (SL) repair scenarios, DebugRepair continues to demonstrate highly
competitive and even leading performance. Under the GPT-3.5 backbone, DebugRepair attains
55 and 50 correct fixes for SL bugs on the Defects4J-V1.2 and V2.0 datasets, respectively. On
Defects4J-V1.2, it performs neck-and-neck with other top approaches, falling only marginally
behind ChatRepair and TSAPR (57 fixes). Notably, on Defects4J-V2.0, DebugRepair surpasses all
evaluated baselines. This strong performance is similarly observed when using the DeepSeek-V3
backbone. With this model, DebugRepair achieves 57 SL fixes on Defects4J-V1.2, which closely
follows the best-performing approach, namely ContrastRepair’s 60 fixes, and secures 61 SL fixes on
Defects4J-V2.0 to significantly outperform the second-ranked ReinFix (47). The marginal variance
observed on Defects4J-V1.2 compared to the top baselines is anticipated. SL bugs typically require
straightforward pattern matching based on outcome-level failure symptoms. In these cases, inserting
print statements and collecting execution traces can make the input context longer and slightly
more difficult for the LLM to process. Despite this, DebugRepair still maintains a top-tier repair
rate, and the robust capability is further evidenced on the QuixBugs benchmark, which consists
predominantly of SL bugs. On this dataset, DebugRepair achieves a 100% fix rate across both Java
and Python versions. Overall, these findings demonstrate that while the self-directed debugging
strategy excels in complex, multi-statement scenarios, it remains a highly effective framework for
simpler, line-level fixes.

 x Answer to RQ2: DebugRepair achieves SOTA performance on complex repairs while maintaining
 competitive performance on simpler bugs, demonstrating its effectiveness across different repair scenarios.


5.3      RQ3: Generalizability Across Different LLMs
To evaluate the model-agnostic nature of DebugRepair, we implement DebugRepair across five
distinct LLMs, encompassing general models, code models, and commercial models. Table 5 summa-
rizes the performance improvements achieved by DebugRepair over the vanilla backbone models.
   As illustrated in Table 5, DebugRepair universally enhances the repair effectiveness of all evalu-
ated LLMs, achieving an average performance improvement of 51.3% over the vanilla backbone
models. Specifically, for general models, the integration of DebugRepair yields substantial improve-
ments, increasing the number of correct fixes for Qwen2.5-7B and Qwen2.5-32B by 21 and 71,

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging                                         111:19


Table 5. Comparison results between vanilla LLMs and DebugRepair on Defects4J (# Correct/# Plausible).

                                                          Defects4J-V1.2                    Defects4J-V2.0
    Category     Model                                                                                                Total
                                                     SF         SH          SL       SF           SH          SL
                 Qwen2.5-7B                         40/64      30/46       20/29    46/73        36/57       23/35    86/137
                 Qwen2.5-7B (DebugRepair)           50/65      39/49       27/32    57/75        42/58       22/32   107/140
    General
                 Qwen2.5-32B                        62/90      47/64       33/43    62/88        42/63       23/34   124/178
                 Qwen2.5-32B (DebugRepair)         92/126      66/89       39/50   103/121       78/91       38/48   195/247
                 Qwen2.5-Coder-7B                   58/88      46/67       33/45    53/82        40/62       27/36   111/170
    Code
                 Qwen2.5-Coder-7B (DebugRepair)     62/96      54/80       33/47    79/91        61/69       34/38   141/187
                 DeepSeek-V3                        82/112     59/76       36/46     73/91       56/70       31/40   155/203
                 DeepSeek-V3 (DebugRepair)         139/179    98/122       57/65   156/180      113/129      61/65   295/359
    Commercial
                 GPT-3.5                            75/104     56/74       36/45    67/100       49/73       31/44   142/204
                 GPT-3.5 (DebugRepair)             111/146    82/102       55/61   113/137      83/100       50/55   224/283
  Φ Note that the highest numbers of plausible and correct fixes are highlighted in bold.




respectively. Similarly, for code models, Qwen2.5-Coder-7B achieves an increase of 30 correct fixes.
The improvements are most pronounced in commercial models, where DebugRepair increases
the total correct fixes from 142 to 224 for GPT-3.5, and from 155 to 295 for DeepSeek-V3. These
results demonstrate that DebugRepair effectively enhances the APR performance across different
categories of LLMs.
   A horizontal comparison across the evaluated models reveals clear performance hierarchies
regarding base architectures and parameter sizes. First, commercial models consistently achieve
the highest overall repair performance, followed by code models, and finally general models. These
results are similar to the findings from previous studies [39, 42] on software engineering tasks.
Specifically, at the same parameter scales, code models consistently outperform their general
model counterparts; for example, the DebugRepair-enhanced Qwen2.5-Coder-7B resolves 141
bugs, significantly outperforming the general model Qwen2.5-7B and approaching the efficacy of
the much larger vanilla GPT-3.5. Second, repair effectiveness scales predictably with model size.
Models with larger parameter sizes inherently outperform smaller variants, as evidenced by the
performance comparison between Qwen2.5-32B and Qwen2.5-7B, as well as their DebugRepair-
enhanced versions.
   Further analysis of the absolute performance gains reveals several key insights into how different
models leverage dynamic feedback. Primarily, DebugRepair exhibits a scaling effect, delivering
greater absolute improvements for models with larger parameter sizes. Specifically, the performance
gain observed in Qwen2.5-32B (+71 fixes) is substantially larger than that of Qwen2.5-7B (+21
fixes). Furthermore, DebugRepair demonstrates a stronger synergistic effect with code models
than with general models; DebugRepair-enhanced Qwen2.5-Coder-7B yields a higher increase
(+30 fixes) than the same integration with Qwen2.5-7B (+21 fixes). Finally, among the commercial
models, DebugRepair yields a significant improvement of 140 additional fixes for DeepSeek-V3
compared to a 74-fix increase for GPT-3.5. These findings suggest that models equipped with
stronger foundational reasoning capabilities and domain-specific code training can process and
leverage the runtime evidence provided by DebugRepair more effectively.

 x Answer to RQ3: DebugRepair consistently enhances the repair capability of various LLMs, regardless
 of their size, type, or architecture. On average, it improves the number of correct fixes by 51.3% across the
 evaluated models.


                                                       J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
111:20                                                                                                        Wu et al.


5.4      RQ4: Ablation Study
To understand the contribution of each component in DebugRepair, we conduct an ablation study
by constructing five variants. (1) DebugRepair-w/o-Purification uses the raw failing test without
slicing, proceeding directly to the subsequent debugging process. (2) DebugRepair-w/o-Debugging
disables the simulated debugging stage and relies solely on outcome-level failure symptoms for
repair. (3) DebugRepair-w/o-Augmentation returns the first plausible patch found without generating
other variants. Additionally, to further analyze the instrumentation design within the simulated
debugging stage, we construct two additional variants: (4) DebugRepair-wo-LLM Instrumentation,
which removes LLM-based instrumentation and uses only the rule-based instrumentation strategy;
and (5) DebugRepair-wo-Rule Instrumentation, which removes the rule-based fallback and skips
cases where LLM-generated instrumentation fails. Table 6 reports the results on the Defects4J
dataset using GPT-3.5 as the backbone LLM.

    Table 6. Ablation results of DebugRepair with different components and instrumentation strategies.

              Variant                            # Plausible    Plausible Drop   # Correct     Correct Drop
              w/o-Purification                      215               ↓ 24.0%       164           ↓ 26.8%
              w/o-Debugging                         213               ↓ 24.7%       165           ↓ 26.3%
              w/o-Augmentation                      283                  –          173           ↓ 19.9%
              w/o-LLM-based Instrumentation         233               ↓ 17.7%       189           ↓ 15.6%
              w/o-Rule-based Instrumentation        227               ↓ 19.4%       181           ↓ 19.2%
              DebugRepair                           283                 –           224             –
                 Φ Note that the highest numbers of plausible and correct fixes are highlighted in bold.


   Effectiveness of test purification. Removing test semantic purification leads to a substantial
performance decline, with the number of correct fixes dropping from 224 to 164, corresponding
to a 26.8% decrease. This result confirms that real-world failing tests often contain irrelevant test
scenarios that obscure the failure-triggering logic and bring about redundant runtime outputs. To
quantitatively validate this, we further analyze the runtime output collected from the inserted
print statements during the repair process. We observe that applying test purification reduces the
average token count of the collected runtime output by 18.6% compared to the unpurified setting.
This reduction indicates that test purification effectively minimizes redundant runtime outputs,
ensuring the concentration of LLMs during bug fixing.
   Effectiveness of simulated debugging. Disabling the simulated debugging mechanism also
causes a substantial performance drop, reducing the number of plausible and correct fixes to 213 and
165, respectively, with a 24.7% and 26.3% decrease. This result highlights the importance of dynamic
execution evidence. Without runtime traces, the framework has to rely only on static, outcome-level
error information, which greatly limits the LLM’s ability to reason about intermediate program
states and trace the root cause of complex bugs. The result shows that incorporating runtime trace
information is essential for grounding patch generation in concrete execution behavior.
   Effectiveness of patch augmentation. Removing the patch augmentation stage preserves
the number of plausible patches (283) but reduces the number of correct fixes from 224 to 173,
corresponding to a 19.9% decrease. This gap directly reflects the common overfitting issue in
APR: a patch may satisfy the available test suite while still being semantically incorrect. Patch
augmentation alleviates this issue by generating and validating diverse semantic variants from the
initial plausible patch, thereby increasing the chance of obtaining a truly correct fix.
   Effectiveness of the hybrid instrumentation design. We further study the internal design of
the simulated debugging stage by separately ablating its two instrumentation strategies. When LLM-
based instrumentation is removed, and only the rule-based strategy is retained, the number of correct

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging                               111:21


fixes drops from 224 to 189. When the rule-based fallback is removed and failed LLM instrumentation
cases are skipped, the number further drops to 181. Similar performance drops are also shown in
plausible fixes. The above results suggest that the two strategies are complementary. LLM-based
instrumentation provides flexible, context-aware observation points, while the rule-based strategy
improves robustness by guaranteeing trace collection when LLM-generated instrumentation is
invalid or fails the consistency check.

 x Answer to RQ4: The effectiveness of DebugRepair comes from the joint contribution of its three core
 components and its hybrid instrumentation design. Removing any single module leads to a substantial drop
 in correct fixes (19.9%–26.8%), proving that all components are jointly essential. Further ablation within the
 simulated debugging stage shows that both LLM-based instrumentation and the rule-based fallback are
 necessary.


5.5   RQ5: Generality to Unseen Bugs
In light of prevailing concerns regarding potential data leakage from established benchmarks,
such as Defects4J and QuixBugs, during the pre-training phase of LLMs, we conduct an additional
evaluation to assess the effectiveness of DebugRepair on unseen datasets. It is worth noting
that while benchmark memorization is a common threat to validity, our comparative analysis in
previous RQs remains robust, given that the evaluated baselines utilize the same backbone models.
Nevertheless, to rigorously verify whether the framework’s performance stems from genuine
reasoning rather than mere memorization, we evaluate DebugRepair on HumanEval-Java, a dataset
released after the training data cutoff of the backbone model (i.e., GPT-3.5). As we mentioned in
Section 5.2, although ChatRepair, ContrastRepair, and TSAPR all follow a paradigm of refining
patches with feedback, the first two focus more on the refinement of a given patch, while the
last one concentrates on searching for a high-quality patch. Thus, DebugRepair is orthogonal to
TSAPR but matches the philosophy of the former. As such, we use ChatRepair and ContrastRepair
as baselines for comparison in this RQ, and directly adopt their results from [19].
   As illustrated in Table 7, DebugRepair achieves the best results among the evaluated tools on
the HumanEval-Java dataset, successfully fixing 153 out of 163 total bugs. In comparison, Con-
trastRepair achieved 137 fixes, while ChatRepair managed 130. DebugRepair exhibits a significant
improvement in the correct repair rate, surpassing ContrastRepair and ChatRepair by 11.68% and
17.69%, respectively. Furthermore, it is crucial to highlight that DebugRepair attains these superior
results while utilizing a significantly smaller patch size compared to the baseline approaches. These
results confirm that the effectiveness of DebugRepair stems from its unique debugging design
rather than mere memorization, highlighting its generalization capability to unseen bugs.


                Table 7. Repair results for DebugRepair and baselines on HumanEval-Java.

             Approach                      Patch Size                  # Plausible                # Correct
             ChatRepair                       500                         143                        130
             ContrastRepair                   160                         151                        137
             DebugRepair                       32                         153                        153
                Φ Note that the highest numbers of plausible and correct fixes are highlighted in bold.




 x Answer to RQ5: DebugRepair maintains high effectiveness on unseen bugs, confirming that its perfor-
 mance stems from the debugging-driven reasoning process rather than data memorization.


                                                        J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
111:22                                                                                        Wu et al.


6     Discussion
6.1      Impact of Hyper-parameters
We analyze the impact of DebugRepair’s hyper-parameters from two perspectives. We first study the
interaction between the number of debugging sessions (𝑁𝑠𝑒𝑠𝑠𝑖𝑜𝑛 ) and the number of repair rounds
per session (𝐾𝑟𝑜𝑢𝑛𝑑 ) without patch augmentation, so as to determine a proper repair budget for the
main debugging process. We then fix this budget and investigate the effect of the augmentation
number in the subsequent patch augmentation stage. As shown in Figure 9(a), the number of
correct fixes generally increases with both 𝑁𝑠𝑒𝑠𝑠𝑖𝑜𝑛 and 𝐾𝑟𝑜𝑢𝑛𝑑 , indicating that enlarging either the
cross-session re-debugging budget or the within-session iterative refinement budget can improve
repair effectiveness.
   A closer look at the trend reveals two important observations. First, increasing 𝐾𝑟𝑜𝑢𝑛𝑑 from 1 to 2
brings a particularly clear improvement, which shows that feedback-driven iterative refinement is
highly beneficial. Second, as 𝑁𝑠𝑒𝑠𝑠𝑖𝑜𝑛 increases, performance rises rapidly in the early stage and then
gradually saturates. This pattern suggests that restarting the repair process with newly collected
debugging evidence is highly effective. At the same time, the later-stage gains become marginal,
showing diminishing returns from continuously increasing the repair budget.
   After fixing the main repair budget, we further study the augmentation number. As shown in
Figure 9(b), increasing the number of augmentation queries consistently improves the number of
correct fixes, confirming that patch augmentation is effective in transforming an initial plausible
patch into more semantically correct variants. However, the improvement also becomes less
pronounced when the augmentation budget grows larger, again indicating diminishing returns.
Considering both repair effectiveness and computational overhead, we set 𝑁𝑠𝑒𝑠𝑠𝑖𝑜𝑛 = 6 and 𝐾𝑟𝑜𝑢𝑛𝑑 =
4 for the debugging-driven repair stage, and use 8 additional queries for patch augmentation. This
yields the default configuration of 6×4+8, which provides a favorable trade-off between effectiveness
and cost under a limited budget.


6.2      Cost Analysis
To comprehensively evaluate the practicality of the proposed framework, we analyze the cost
differences between DebugRepair and existing APR tools in terms of patch size, token consumption,
and monetary cost. We select ChatRepair [38], RepairAgent [4], TSAPR [11], and ReinFix [48] as
baselines, as other LLM-based baselines do not report cost-related statistics for direct comparison.
For a fair comparison, all approaches use GPT-3.5 as the backbone model, and the cost metrics are
evaluated on the Defects4J dataset.
   Table 8 presents the detailed cost comparison. With the patch size set to 32, which is tied for the
smallest among all baselines alongside TSAPR, DebugRepair demonstrates a significant advantage
in token efficiency. It consumes an average of only 38,000 tokens per bug, which is merely 18.1%
of the 210,000 tokens reported by ChatRepair, 14.1% of the 270,000 tokens by RepairAgent, and
less than the 40,000 tokens required by TSAPR. This token efficiency over TSAPR primarily stems
from two factors: first, TSAPR incurs additional token overhead by invoking LLMs for intermediate
reasoning (e.g., Chain-of-Thought) and patch evaluation (e.g., LLM-as-Judge), whereas DebugRepair
limits LLM generation to instrumentation and patch generation; second, DebugRepair’s higher
repair success rate effectively reduces the average token consumption per fixed bug.
   In terms of monetary cost, DebugRepair achieves the lowest cost at $0.036 per bug. When com-
pared to the recent SOTA baselines TSAPR and ReinFix (both costing $0.06 per bug), DebugRepair
achieves a substantial cost reduction of 35.0%. Moreover, this cost is only 27.9% of the $0.14 ex-
penditure reported by both ChatRepair (today’s pricing) and RepairAgent. Crucially, DebugRepair


J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging                                                                                111:23


                                              200




                    Number of Correct Fixes
                                              180

                                              160

                                              140
                                                                                                                               Repair Rounds (Kround = 1)
                                              120                                                                              Repair Rounds (Kround = 2)
                                                                                                                               Repair Rounds (Kround = 3)
                                              100                                                                              Repair Rounds (Kround = 4)
                                                                                                                               Repair Rounds (Kround = 5)
                                               80
                                                    1           2           3          4        5          6         7               8             9         10
                                                                                    Number of Debugging Sessions (Nsession )

                                                        (a) Repair performance under different 𝑁𝑠𝑒𝑠𝑠𝑖𝑜𝑛 and 𝐾𝑟𝑜𝑢𝑛𝑑 settings.

                                              240




                    Number of Correct Fixes
                                              220


                                              200


                                              180


                                              160
                                                    0    1     2    3   4       5   6     7    8  9 10 11 12 13          14     15       16   17   18   19   20
                                                                                              Augmentation Numbers

                                                             (b) Repair performance under different augmentation budgets.

             Fig. 9. Impact of hyper-parameter settings on the repair performance of DebugRepair.


achieves this superior cost-efficiency while simultaneously delivering a higher number of cor-
rect fixes, demonstrating the ability of the proposed framework to yield SOTA performance at a
significantly lower budget.

         Table 8. Cost comparison between DebugRepair and existing APR approaches on Defects4J.
Approach                                                                        Patch/Bug                            Token/Bug                                    Money/Bug
ChatRepair (2024) [38]                                                              500                               210,000                                       $0.42
ChatRepair (today’s price)                                                          500                               210,000                                       $0.14
RepairAgent (2024) [4]                                                              117                               270,000                                       $0.14
TSAPR (2025) [10]                                                                   32                                40,000                                        $0.06
ReinFix (2026) [48]                                                                 45                                   -                                          $0.06
DebugRepair (Ours)                                                                  32                                38000                                        $0.036
    Φ “-” indicates no results reported in the original work, while the lowest cost on patch/token/money consumption per

    bug is highlighted in bold.                                                                    1


7    Threats to Validity
Threats to construct validity. The primary concern lies in the subjectivity of evaluating the
correctness of generated patches. While automated testing can easily identify plausible patches that
pass all test cases, verifying the semantic correctness of these patches requires manual inspection,
which introduces potential human bias. To mitigate this threat, we implement a rigorous and
systematic evaluation protocol. Specifically, two researchers with extensive development back-
grounds independently review each plausible patch in a double-blind manner to assess whether it
is semantically consistent with the developer patch. When disagreements arise, a third independent

                                                                                              J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
                                                                                                   1
111:24                                                                                       Wu et al.


researcher serves as an arbitrator to conduct an additional review and moderate the discussion
until consensus is reached. This mechanism ensures the reliability and objectivity of the evaluation
process.
   Threats to internal validity. A primary threat arises from potential data leakage in LLM-based
evaluation. Since the backbone models are pretrained on large-scale public code corpora, they may
have been exposed to repair patterns or corresponding fixes during training. To mitigate this risk,
we additionally evaluate DebugRepair on the HumanEval-Java benchmark, whose release date
postdates the training data cutoff of GPT-3.5. The consistent performance gains observed on this
temporally isolated dataset suggest that the improvements stem from the design of DebugRepair
rather than memorization of pretraining data.
   Threats to external validity. External validity concerns the generalizability of the proposed
approach across different datasets and programming languages (PLs). To mitigate this threat,
we evaluate DebugRepair on three widely used benchmarks, including Defects4J, QuixBugs, and
HumanEval-Java, which differ in bug characteristics and complexity. Notably, we intentionally
exclude issue-resolving benchmarks such as SWE-bench [17] from our evaluation because they
restrict APR tools from accessing explicit test cases as the default experimental setting, thereby
rendering DebugRepair inapplicable to such evaluations. Besides, our evaluation further spans both
Java and Python to reduce potential PL-specific bias. The consistent performance gains observed
across these datasets and languages demonstrate the generalization capability of DebugRepair.

8   Related Work
Automated Program Repair (APR) aims to automatically generate patches that fix software bugs,
thereby reducing developers’ manual debugging effort [8, 23, 49]. Early APR studies can be broadly
categorized into template-based [9, 12, 27, 30], heuristic-based [13, 21, 22, 34], and constraint-
based [7, 20, 29, 31] paradigms. For example, Liu et al. [28] propose TBar, which applies a set of
recurrently-used fix patterns to resolve software bugs. Gao et al. [7] propose ExtractFix, which
synthesizes vulnerability patches guided by crash constraints extracted via symbolic execution.
Although effective in specific settings, these approaches are often limited by limited patch diversity
and limited generality for semantically complex bugs.
   With advances in deep learning, APR shifted from rule-intensive repair to data-driven patch
generation. Existing learning-based approaches mainly include NMT-based approaches [6, 16,
24, 25], which formulate repair as a code-to-code translation task, and PLM-based approaches
[32, 35–37], which leverage large-scale pre-training to improve contextual modeling and repair
capability. For example, Ye et al. [45] propose SelfAPR, a self-supervised training approach that
captures fault-specific knowledge by encoding execution diagnostics. Additionally, Xia et al. [35]
introduce FitRepair, a PLM-based approach that uses fine-tuning and prompting to extract fix
ingredients. Despite their improved generality over traditional APR, these approaches still rely
heavily on historical fixes and often struggle to reason about failure-specific execution semantics.
   More recently, Large Language Models (LLMs) have substantially advanced APR due to their
strong capabilities in code understanding and generation. Existing LLM-based APR techniques can
be broadly categorized into three paradigms: retrieval-based [4, 48], feedback-based [19, 38], and
hybrid approaches [47]. (1) Retrieval-based approaches, such as RepairAgent [4] and ReinFix [48],
enrich repair prompts with external code fragments, semantic ingredients, or historical fixes. (2)
Feedback-based approaches leverage execution feedback to improve repair quality, but differ in
how it is used: ChatRepair [38] and ContrastRepair [19] directly refine candidate patches through
execution feedback, whereas TSAPR [11] incorporates execution feedback into a Monte Carlo Tree
Search (MCTS) process to guide patch exploration. (3) Hybrid approaches combine multiple repair
signals to improve LLM-based patch generation. For example, ThinkRepair [47] adopts a two-phase

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging                                    111:25


framework that first collects chains of thought and verified fixes to build a knowledge pool, and
then selects few-shot examples from this pool to guide repairs, optionally incorporating test-failure
feedback for further refinement.
   Despite the progress of LLM-based APR, a common limitation remains across these paradigms:
Most approaches rely on source code and outcome-level failure symptoms, i.e., stack traces. Al-
though useful for identifying the manifestation of a bug, these signals are often too coarse to
expose the intermediate runtime states that directly reveal its root cause. As a result, LLMs may
generate plausible yet semantically incorrect patches that only mask symptoms. We also found
concurrent work, namely InspectCoder [33], which follows the debugging philosophy as well,
using natural-language task descriptions as explicit specifications. However, such an experimental
setting (i.e., being equipped with task descriptions) differs from mainstream real-world APR studies,
making it unfair to include it as a comparison. In contrast, DebugRepair combines with test semantic
purification, simulated instrumentation, and debugging-driven conversational repair, allowing
LLMs to reason over intermediate runtime states and reduce the noise in failure-triggering test
contexts, thereby providing a more failure-specific foundation for LLM-based APR.

9   Conclusion
In this paper, we propose DebugRepair, a novel LLM-based APR framework that enhances repair
effectiveness via self-directed debugging. Unlike existing feedback-based APR approaches that
mainly rely on outcome-level failure symptoms, DebugRepair equips LLMs with runtime-state
evidence through three components, namely test semantic purification, simulated instrumentation,
and debugging-driven conversational repair. Experimental results on Defects4J, QuixBugs, and
HumanEval-Java show that DebugRepair consistently outperforms existing SOTA baselines across
different backbone LLMs, while ablation studies further confirm the effectiveness of all components
in the framework.

Acknowledgments
This work was partially supported by the National Natural Science Foundation of China (Grant
Nos. 62502283 and U24B20149), the Natural Science Foundation of Shandong Province (Grant No.
ZR2024QF093), the Young Talent of Lifting Engineering for Science and Technology in Shandong,
China (Grant No. SDAST2025QTB031).

References
 [1] [n. d.]. Models | OpenAI API. https://platform.openai.com/docs/models#gpt-3-5-turbo [Online; accessed 2026-01-20].
 [2] [n. d.]. SiliconFlow – AI Infrastructure for LLMs & Multimodal Models. https://www.siliconflow.com/ [Online;
     accessed 2026-01-20].
 [3] [n. d.]. tree-sitter/tree-sitter: An incremental parsing system for programming tools. https://github.com/tree-sitter/tree-
     sitter [Online; accessed 2026-03-13].
 [4] Islem Bouzenia, Premkumar Devanbu, and Michael Pradel. 2024. Repairagent: An autonomous, llm-based agent for
     program repair. arXiv preprint arXiv:2403.17134 (2024).
 [5] Mark Chen. 2021. Evaluating large language models trained on code. arXiv preprint arXiv:2107.03374 (2021).
 [6] Zimin Chen, Steve Kommrusch, Michele Tufano, Louis-Noël Pouchet, Denys Poshyvanyk, and Martin Monperrus. 2019.
     Sequencer: Sequence-to-sequence learning for end-to-end program repair. IEEE Transactions on Software Engineering
     47, 9 (2019), 1943–1959.
 [7] Xiang Gao, Bo Wang, Gregory J Duck, Ruyi Ji, Yingfei Xiong, and Abhik Roychoudhury. 2021. Beyond tests: Program
     vulnerability repair via crash constraint extraction. ACM Transactions on Software Engineering and Methodology
     (TOSEM) 30, 2 (2021), 1–27.
 [8] Luca Gazzola, Daniela Micucci, and Leonardo Mariani. 2018. Automatic software repair: A survey. In Proceedings of the
     40th International Conference on Software Engineering. 1219–1219.
 [9] Ali Ghanbari, Samuel Benton, and Lingming Zhang. 2019. Practical program repair via bytecode mutation. In Proceedings
     of the 28th ACM SIGSOFT International Symposium on Software Testing and Analysis. 19–30.

                                                          J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
111:26                                                                                                            Wu et al.


[10] Haichuan Hu, Congqing He, Hao Zhang, Xiaochen Xie, and Quanjun Zhang. 2025. APRMCTS: Improving LLM-based
     Automated Program Repair with Iterative Tree Search. arXiv preprint arXiv:2507.01827 (2025).
[11] Haichuan Hu, Ye Shang, Weifeng Sun, and Quanjun Zhang. 2025. TSAPR: A Tree Search Framework For Automated
     Program Repair. arXiv preprint arXiv:2507.01827 (2025).
[12] Jinru Hua, Mengshi Zhang, Kaiyuan Wang, and Sarfraz Khurshid. 2018. Sketchfix: a tool for automated program repair
     approach using lazy candidate generation. In Proceedings of the 2018 26th ACM Joint Meeting on European Software
     Engineering Conference and Symposium on the Foundations of Software Engineering. 888–891.
[13] Jiajun Jiang, Yingfei Xiong, Hongyu Zhang, Qing Gao, and Xiangqun Chen. 2018. Shaping program repair space with
     existing patches and similar code. In Proceedings of the 27th ACM SIGSOFT international symposium on software testing
     and analysis. 298–309.
[14] Nan Jiang, Kevin Liu, Thibaud Lutellier, and Lin Tan. 2023. Impact of code language models on automated program
     repair. In 2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE). IEEE, 1430–1442.
[15] Nan Jiang, Thibaud Lutellier, Yiling Lou, Lin Tan, Dan Goldwasser, and Xiangyu Zhang. 2023. Knod: Domain knowledge
     distilled tree decoder for automated program repair. In 2023 IEEE/ACM 45th International Conference on Software
     Engineering (ICSE). IEEE, 1251–1263.
[16] Nan Jiang, Thibaud Lutellier, and Lin Tan. 2021. Cure: Code-aware neural machine translation for automatic program
     repair. In 2021 IEEE/ACM 43rd International Conference on Software Engineering (ICSE). IEEE, 1161–1173.
[17] Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik Narasimhan. 2023.
     Swe-bench: Can language models resolve real-world github issues? arXiv preprint arXiv:2310.06770 (2023).
[18] René Just, Darioush Jalali, and Michael D Ernst. 2014. Defects4J: A database of existing faults to enable controlled
     testing studies for Java programs. In Proceedings of the 2014 international symposium on software testing and analysis.
     437–440.
[19] Jiaolong Kong, Xiaofei Xie, Mingfei Cheng, Shangqing Liu, Xiaoning Du, and Qi Guo. 2025. Contrastrepair: Enhancing
     conversation-based automated program repair via contrastive test case pairs. ACM Transactions on Software Engineering
     and Methodology 34, 8 (2025), 1–31.
[20] Xuan-Bach D Le, Duc-Hiep Chu, David Lo, Claire Le Goues, and Willem Visser. 2017. S3: syntax-and semantic-guided
     repair synthesis via programming by examples. In Proceedings of the 2017 11th Joint Meeting on Foundations of Software
     Engineering. 593–604.
[21] Xuan Bach D Le, David Lo, and Claire Le Goues. 2016. History driven program repair. In 2016 IEEE 23rd international
     conference on software analysis, evolution, and reengineering (SANER), Vol. 1. IEEE, 213–224.
[22] Claire Le Goues, ThanhVu Nguyen, Stephanie Forrest, and Westley Weimer. 2011. Genprog: A generic method for
     automatic software repair. Ieee transactions on software engineering 38, 1 (2011), 54–72.
[23] Claire Le Goues, Michael Pradel, and Abhik Roychoudhury. 2019. Automated program repair. Commun. ACM 62, 12
     (2019), 56–65.
[24] Yi Li, Shaohua Wang, and Tien N Nguyen. 2020. Dlfix: Context-based code transformation learning for automated
     program repair. In Proceedings of the ACM/IEEE 42nd international conference on software engineering. 602–614.
[25] Yi Li, Shaohua Wang, and Tien N Nguyen. 2022. Dear: A novel deep learning-based approach for automated program
     repair. In Proceedings of the 44th international conference on software engineering. 511–523.
[26] Derrick Lin, James Koppel, Angela Chen, and Armando Solar-Lezama. 2017. QuixBugs: A multi-lingual program repair
     benchmark set based on the Quixey Challenge. In Proceedings Companion of the 2017 ACM SIGPLAN international
     conference on systems, programming, languages, and applications: software for humanity. 55–56.
[27] Kui Liu, Anil Koyuncu, Dongsun Kim, and Tegawendé F Bissyandé. 2019. Avatar: Fixing semantic bugs with fix
     patterns of static analysis violations. In 2019 IEEE 26th International Conference on Software Analysis, Evolution and
     Reengineering (SANER). IEEE, 1–12.
[28] Kui Liu, Anil Koyuncu, Dongsun Kim, and Tegawendé F Bissyandé. 2019. TBar: Revisiting template-based automated
     program repair. In Proceedings of the 28th ACM SIGSOFT international symposium on software testing and analysis.
     31–42.
[29] Fan Long and Martin Rinard. 2015. Staged program repair with condition synthesis. In Proceedings of the 2015 10th
     Joint Meeting on Foundations of Software Engineering. 166–178.
[30] Matias Martinez and Martin Monperrus. 2016. Astor: A program repair library for java. In Proceedings of the 25th
     international symposium on software testing and analysis. 441–444.
[31] Sergey Mechtaev, Jooyong Yi, and Abhik Roychoudhury. 2016. Angelix: Scalable multiline program patch synthesis
     via symbolic analysis. In Proceedings of the 38th international conference on software engineering. 691–701.
[32] Weishi Wang, Yue Wang, Shafiq Joty, and Steven CH Hoi. 2023. Rap-gen: Retrieval-augmented patch generation with
     codet5 for automatic program repair. In Proceedings of the 31st ACM Joint European Software Engineering Conference
     and Symposium on the Foundations of Software Engineering. 146–158.



J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.
DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging                               111:27


[33] Yunkun Wang, Yue Zhang, Guochang Li, Chen Zhi, Binhua Li, Fei Huang, Yongbin Li, and Shuiguang Deng. 2026.
     InspectCoder: Dynamic Analysis-Driven Self Repair through Interactive LLM-Debugger Collaboration. Proceedings of
     the ACM on Programming Languages 10, OOPSLA1 (2026), 1041–1069.
[34] Ming Wen, Junjie Chen, Rongxin Wu, Dan Hao, and Shing-Chi Cheung. 2018. Context-aware patch generation for
     better automated program repair. In Proceedings of the 40th international conference on software engineering. 1–11.
[35] Chunqiu Steven Xia, Yifeng Ding, and Lingming Zhang. 2023. The plastic surgery hypothesis in the era of large
     language models. In 2023 38th IEEE/ACM International Conference on Automated Software Engineering (ASE). IEEE,
     522–534.
[36] Chunqiu Steven Xia, Yuxiang Wei, and Lingming Zhang. 2023. Automated program repair in the era of large pre-trained
     language models. In 2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE). IEEE, 1482–1494.
[37] Chunqiu Steven Xia and Lingming Zhang. 2022. Less training, more repairing please: revisiting automated program
     repair via zero-shot learning. In Proceedings of the 30th ACM Joint European Software Engineering Conference and
     Symposium on the Foundations of Software Engineering. 959–971.
[38] Chunqiu Steven Xia and Lingming Zhang. 2024. Automated program repair via conversation: Fixing 162 out of 337
     bugs for $0.42 each using chatgpt. In Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing
     and Analysis. 819–831.
[39] Pengyu Xue, Linhao Wu, Zhen Yang, Chengyi Wang, Xiang Li, Yuxiang Zhang, Jia Li, Ruikai Jin, Yifei Pei, Zhaoyan
     Shen, et al. 2025. ClassEval-T: Evaluating Large Language Models in Class-Level Code Translation. Proceedings of the
     ACM on Software Engineering 2, ISSTA (2025), 1421–1444.
[40] Pengyu Xue, Linhao Wu, Zhen Yang, Zhongxing Yu, Zhi Jin, Ge Li, Yan Xiao, Shuo Liu, Xinyi Li, Hongyi Lin, et al.
     2024. Exploring and Lifting the Robustness of LLM-powered Automated Program Repair with Metamorphic Testing.
     arXiv preprint arXiv:2410.07516 (2024).
[41] Pengyu Xue, Linhao Wu, Zhongxing Yu, Zhi Jin, Zhen Yang, Xinyi Li, Zhenyu Yang, and Yue Tan. 2024. Automated
     commit message generation with large language models: An empirical study and beyond. IEEE Transactions on Software
     Engineering (2024).
[42] Pengyu Xue, Kunwu Zheng, Zhen Yang, Yifei Pei, Linhao Wu, Jiahui Dong, Xiapu Luo, Yan Xiao, Fei Liu, Yuxuan
     Zhang, et al. 2025. TransLibEval: Demystify Large Language Models’ Capability in Third-party Library-targeted Code
     Translation. arXiv preprint arXiv:2509.12087 (2025).
[43] Zhen Yang, Fang Liu, Zhongxing Yu, Jacky Wai Keung, Jia Li, Shuo Liu, Yifan Hong, Xiaoxue Ma, Zhi Jin, and Ge Li.
     2024. Exploring and unleashing the power of large language models in automated code translation. Proceedings of the
     ACM on Software Engineering 1, FSE (2024), 1585–1608.
[44] Yifan Yao, Jinhao Duan, Kaidi Xu, Yuanfang Cai, Zhibo Sun, and Yue Zhang. 2024. A survey on large language model
     (llm) security and privacy: The good, the bad, and the ugly. High-Confidence Computing 4, 2 (2024), 100211.
[45] He Ye, Matias Martinez, Xiapu Luo, Tao Zhang, and Martin Monperrus. 2022. Selfapr: Self-supervised program repair
     with test execution diagnostics. In Proceedings of the 37th IEEE/ACM International Conference on Automated Software
     Engineering. 1–13.
[46] He Ye, Matias Martinez, and Martin Monperrus. 2022. Neural program repair with execution-based backpropagation.
     In Proceedings of the 44th international conference on software engineering. 1506–1518.
[47] Xin Yin, Chao Ni, Shaohua Wang, Zhenhao Li, Limin Zeng, and Xiaohu Yang. 2024. Thinkrepair: Self-directed
     automated program repair. In Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and
     Analysis. 1274–1286.
[48] Jiayi Zhang, Kai Huang, Jian Zhang, Yang Liu, and Chunyang Chen. 2025. Repair Ingredients Are All You Need:
     Improving Large Language Model-Based Program Repair via Repair Ingredients Search. arXiv preprint arXiv:2506.23100
     (2025).
[49] Quanjun Zhang, Chunrong Fang, Yuxiang Ma, Weisong Sun, and Zhenyu Chen. 2023. A survey of learning-based
     automated program repair. ACM Transactions on Software Engineering and Methodology 33, 2 (2023), 1–69.
[50] Qihao Zhu, Zeyu Sun, Yuan-an Xiao, Wenjie Zhang, Kang Yuan, Yingfei Xiong, and Lu Zhang. 2021. A syntax-guided
     edit decoder for neural program repair. In Proceedings of the 29th ACM joint meeting on European software engineering
     conference and symposium on the foundations of software engineering. 341–353.

Received 20 February 2007; revised 12 March 2009; accepted 5 June 2009




                                                        J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

