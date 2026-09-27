# PracRepair: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices
Source: https://arxiv.org/abs/2606.17612v1
PDF: https://arxiv.org/abs/2606.17612v1 (full PDF not vendored; build-time copy at /Users/sergii/.fleet/workflows/summarise/wfr-x7r0cc23/source.pdf exceeds 2 MB limit)
Kind: pdf
Fetched: 2026-09-23T19:56:19.493980+00:00
Tool: pdftotext
Research-Target: /Users/sergii/.ai/knowledge/research_topics/coding_agents/research/ai_coding_best_practices
Topic: coding_agents

                                         IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 14, NO. 8, AUGUST 2021                                                                      1




                                                    P RAC R EPAIR: LLM-Empowered Automated
                                                      Program Repair Inspired by Human-Like
                                                                Debugging Practices
                                                              Yu Cheng, Zhongxin Liu, Zhenchang Xing, Chao Ni, Qing Huang, Xiaoxue Ren



                                            Abstract—As software systems grow in scale and complexity,                by inspecting the buggy method and failing tests, navigating
                                         debugging and repair remain costly and time-consuming. Large                 to relevant implementations, and tracing execution through
                                         language models (LLMs) have advanced automated program




arXiv:2606.17612v1 [cs.SE] 16 Jun 2026
                                                                                                                      interactive operations such as step into and step over. Through
                                         repair (APR), but existing LLM-based APR approaches still
                                         largely rely on static or retrieved context, error messages, and             this process, they recover implicit execution knowledge, in-
                                         coarse-grained validation outcomes. As a result, they underuti-              cluding call relationships, and observe fine-grained runtime
                                         lize dynamic information for failure understanding and repair,               behaviors such as executed paths, variable states, branch
                                         including failure-execution dynamics and patch-validation dy-                outcomes, and intermediate values [6], [9]–[12]. Based on
                                         namics. Effectively leveraging such information, however, is chal-           such evidence, developers then diagnose failures in a question-
                                         lenging: failure-execution traces are large and noisy, raw static-
                                         dynamic context is not self-explanatory, and patch-validation                driven manner [7], [8], [13], asking targeted questions such
                                         dynamics are often reduced to coarse feedback. To address                    as what happened here? or why is x null at this point?, and
                                         these challenges, we propose P RAC R EPAIR, a fully automated                progressively narrowing down the root cause while identifying
                                         LLM-based APR framework inspired by human-like debugging                     what additional evidence is needed to better understand the
                                         practices. P RAC R EPAIR constructs an on-demand static-dynamic              buggy behavior [12]. After completing the failure diagnosis,
                                         context from buggy programs and failure executions, performs
                                         question-driven failure diagnosis to formulate explicit repair               developers often return to the debugging environment to re-
                                         hypotheses, and iteratively refines candidate patches using valida-          execute the patched program and compare its behavior with the
                                         tion diagnostics and trace-level behavioral changes. Experimental            original failing execution. If the patch does not fully resolve
                                         results on Defects4J V1.2 and V2.0 show that P RAC R EPAIR                   the bug, they further analyze the remaining failure and refine
                                         consistently outperforms state-of-the-art baselines. Specifically,           the repair accordingly. As a result, failure understanding and
                                         under GPT-3.5, P RAC R EPAIR correctly fixes 139/136 bugs on
                                         Defects4J V1.2/V2.0, while under GPT-4o it further improves                  patch construction co-evolve through continuous feedback and
                                         to 162/171. Moreover, P RAC R EPAIR generalizes effectively to               refinement [10]–[12].
                                         RWB (Real-World Bugs), achieving the best performance across                    Although such a debugging workflow is effective in practice,
                                         multiple foundation models.                                                  it is also expensive and time-consuming. Software developers
                                           Index Terms—Automated program repair, large language                       spend roughly 35% to 50% of their time, and 50% to 75%
                                         model.                                                                       of project budgets, on testing, verification, and debugging,
                                                                                                                      costing over 100 billion dollars each year [14]–[16]. This
                                                                                                                      high cost has motivated extensive research on automated
                                                                  I. I NTRODUCTION
                                                                                                                      program repair (APR), which aims to automatically generate
                                            As modern software systems continue to grow in scale                      patches for buggy programs [17]–[28]. Early APR approaches
                                         and complexity, defects have become increasingly common                      mainly relied on manually designed fix patterns or bug-
                                         in real-world development [1], [2]. Fixing these defects is                  fixing datasets [18]–[23], but their effectiveness was often
                                         often challenging in practice, because in real-world software                constrained by limited pattern coverage, strong data depen-
                                         systems, the causes and effects of a defect often extend                     dence, and weak generalization ability [18], [29]. Recently,
                                         beyond a single function and require reasoning over non-                     large language models (LLMs) have demonstrated stronger
                                         local contextual information, such as call relationships, data               code understanding and generation capabilities for APR [24],
                                         dependencies, and execution logic [3].                                       [30], [31]. Building on this progress, recent LLM-based APR
                                            Developers typically debug in IDE-like environments [4],                  approaches, such as ChatRepair [25], ThinkRepair [27], Re-
                                         [5], where they leverage richer information and follow a                     pairAgent [26], and ReInFix [28], further incorporate richer
                                         structured workflow to understand failures, formulate repair                 repair context and iterative interaction, achieving stronger
                                         hypotheses, and iteratively refine fixes [6]–[11]. More specifi-             repair performance on benchmarks such as Defects4J [3].
                                         cally, developers first gather both static and dynamic evidence                 However, a key limitation is that prior approaches un-
                                                                                                                      derutilize dynamic information for failure understanding
                                           Y. Cheng, Z. Liu, C. Ni, and X. Ren are with Zhejiang University, China.
                                         E-mail: {yucheng1127, liu zx, chaoni, xxren}@zju.edu.cn.                     and repair, while overestimating LLMs’ ability to precisely
                                           Z. Xing is with CSIRO’s Data61, Australia. E-mail: zhen-                   infer complex program behavior from static context alone.
                                         chang.xing@data61.csiro.au.                                                  Although recent methods such as ChatRepair [25], ThinkRe-
                                           Q. Huang is with Jiangxi Normal University, China. E-mail:
                                         qh@jxnu.edu.cn.                                                              pair [27], RepairAgent [26], and ReInFix [28] incorporate test
                                           X. Ren is the corresponding author.                                        feedback, richer repair context, or iterative interaction, their
IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 14, NO. 8, AUGUST 2021                                                             2



repair processes are still largely driven by static or retrieved    by P RAC R EPAIR with GPT-3.5 and 93 unique correct fixes
context, error messages, and coarse-grained validation out-         under GPT-4o when compared with ReInFix. Across repair
comes. In particular, they do not systematically exploit two        scenarios, P RAC R EPAIR performs strongly from single-line to
types of dynamic information that are critical in practical         multi-function bugs, with particularly notable advantages on
debugging: failure-execution dynamics, which reveal how the         more challenging cases. Ablation studies further verify the
original failure is triggered through executed paths, runtime       effectiveness of all three stages, showing that these gains come
states, and branch outcomes, and patch-validation dynamics,         from enriching repair with failure-aware information, question-
which reveal how a candidate patch changes program behavior         driven diagnosis, and feedback-guided refinement inspired by
during validation. Without these dynamic signals, LLMs may          human-like debugging practices. Beyond Defects4J, P RAC R E -
miss root causes or generate incomplete and overfitted fixes,       PAIR also generalizes well to RWB V1.0/V2.0 [27], achieving
especially for bugs whose root causes depend on runtime states      the best performance across multiple foundation models.
and value evolution.                                                   Overall, this work makes the following main contributions:
   Effectively leveraging such dynamic information introduces          • We identify and formulate a critical gap between practi-
three challenges. C1: Failure-execution dynamics are large               cal debugging workflows and existing LLM-based APR
and noisy. Directly exposing complete traces to the LLM may              techniques. Specifically, we show that current approaches
overwhelm the repair context rather than help identify failure-          have not fully exploited three debugging practices that are
relevant behavior. C2: Raw static-dynamic context is not                 widely used by developers: static-dynamic evidence gath-
self-explanatory. Even when execution traces are available,              ering, question-driven failure diagnosis, and feedback-
the LLM still needs to determine which runtime states matter             guided patch refinement.
and how they relate to the faulty logic; otherwise, it may             • We introduce P RAC R EPAIR , a fully automated LLM-
make incorrect behavioral inferences. C3: Patch-validation               based APR framework that operationalizes these debug-
dynamics are often underused. They are frequently reduced                ging practices. P RAC R EPAIR constructs an on-demand
to coarse validation outcomes, such as pass/fail results or error        static-dynamic context from buggy programs and failure
messages, leaving subsequent repair iterations without fine-             executions, performs question-driven failure diagnosis
grained evidence about what behavior has changed and why                 to formulate explicit repair hypotheses, and iteratively
the current patch still fails.                                           refines candidate patches using validation diagnostics and
   To address the above challenges, we design and implement              trace-level behavioral changes.
P RAC R EPAIR, an LLM-empowered APR framework inspired                 • We conduct extensive experiments on Defects4J and
by human-like debugging practices. Specifically, P RAC R EPAIR           RWB. Results show that P RAC R EPAIR consistently out-
consists of three stages. (1) Static-dynamic context con-                performs SOTA APR baselines, remains effective across
struction addresses C1 by combining static program context               different repair scenarios from single-line to multi-
with selectively organized execution traces collected from               function bugs, and generalizes well across multiple foun-
triggering test runs. Instead of directly exposing complete              dation models. Ablation studies further confirm the effec-
traces to the LLM, P RAC R EPAIR indexes and structures dy-              tiveness of all three modules.
namic evidence through a unified interface, allowing the LLM           The code and experimental results are available at [Link]
to access relevant code context, call relationships, executed
paths, and runtime states on demand. (2) Question-driven                                   II. M OTIVATION
failure diagnosis addresses C2 by guiding the LLM to ask               We present a real-world example in Figure 1, based on
and answer targeted diagnostic questions about what happens         a simplified code snippet excerpted from the Java project
during execution, why the failure occurs, and how the faulty        commons-compress, to illustrate why APR should move be-
logic should be corrected. By retrieving the evidence needed        yond direct patch generation and instead follow a debugging-
to answer these questions, P RAC R EPAIR progressively nar-         oriented repair process. This example mirrors how developers
rows down the root cause and formulates an explicit repair          debug in practice: they inspect static code context, observe
hypothesis. (3) Feedback-guided patch refinement addresses          concrete runtime states, ask targeted diagnostic questions,
C3 by extracting validation diagnostics, code diffs, and trace      and refine incomplete fixes based on changed program be-
diffs from failed candidate patches, and feeding these patch-       havior. Accordingly, it motivates the three key designs of
validation dynamics back into diagnosis for iterative refine-       P RAC R EPAIR: static-dynamic context construction, question-
ment. This enables more evidence-grounded repair and helps          driven failure diagnosis, and feedback-guided patch refine-
avoid incomplete or overfitted fixes.                               ment. The bug is located in the writeBits method, which
   Experimental results on real-world benchmarks demonstrate        packs bits into a temporary buffer cache and flushes them
the effectiveness of P RAC R EPAIR’s human-like debugging-          according to shift. The defect is an off-by-one error:
inspired design. On Defects4J V1.2 and V2.0, P RAC R EPAIR          shift is initialized to 7 and decremented after each bit is
consistently outperforms state-of-the-art APR baselines [18]–       written, but the buggy code flushes the buffer when shift
[20], [22], [24]–[28]. Specifically, under GPT-3.5, P RAC R E -     == 0, causing only seven bits to be written and triggering
PAIR correctly fixes 139 bugs on Defects4J V1.2 and 136             java.io.IOException: Unknown property 128.
bugs on Defects4J V2.0; under GPT-4o, it further improves to        C1: Failure-execution dynamics are large and noisy. Ex-
162 and 171 bugs, respectively. It also fixes many previously       isting LLM-based APR methods already use failure-related
unsolved bugs, including 75 unique correct fixes achieved           signals, but these signals are often coarse-grained. For exam-
                                                                    ple, ChatRepair [25] and ThinkRepair [27] use buggy code,
IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 14, NO. 8, AUGUST 2021                                                                                                                                                                            3



                                Bug Information                                     A. Repairing with Static Context                           Question-driven Diagnosis                          C. Feedback-guided Patch Refinement
         Test Suite:                                                                      ## Task: generate a corrected patch...
         public void testSevenEmptyFiles() throws Exception {                             ## Input: Bug_Info, Program_Context                   What are cache and shift when if (shift
                                                                                                                                                                                                   ## Task: generate a corrected patch..
            testCompress252(7, 0);                                                                                                              == 0) is entered?
                                                                                                                                                                                                   ## Input: Bug_Info
         }                                                                                Writing cache directly may produce
                                                                                                                                             When branch is entered,cache = 254                    Root Cause: Off-by-one flush logic
         Failure Info:                                                                    invalid data, so use cache & 0xFF to
                                                                                          keep only the lower 8 bits.                        and shift = 0 after i = 6                             Modification Suggestion: Flush only
         java.io.IOException: Unknown property 128
                                                                                          ......                                                                                                   when shift < 0
         Buggy Code:                                                                                                                            How should the in-loop flush condition
         01 private void writeBits(final DataOutput header,                               if (shift == 0) {                                     be changed?
                final BitSet bits, final int length) throws IOException {                        header.write(cache & 0xFF);                                                                       Apply the modification to the in-loop
         02     int cache = 0;                                                            ......                                                                                                   flush condition.
                                                                                                             Unknown property 128            Change if (shift == 0) to if (shift < 0).             ......
         03     int shift = 7;
         04     for (int i = 0; i < length; i++) {                                                                                                                                                 if(shift < 0) {
                                                                                         Dynamic Execution Trace                                                                                          header.write(cache);
         05          cache |= ((bits.get(i) ? 1 : 0) << shift);                                                                                       Validation Feedback
         06          --shift;                                                   <testSevenEmptyFiles, writeBites>                                                                                  ......
         07          if (shift == 0) {                                          ......                                                                                                             if (length > 0 && shift > 0) {
                                                                                                                                           Failure Info:
         08               header.write(cache);                                  Line6: {'i': 6, ......, 'cache': 254, 'shift': 0}          java.io.IOException: Badly terminated header                           Badly terminated header
         09               shift = 7;                                            Line7: {'type': 'branch', 'executed': True}                Code Diff:
         10               cache = 0;                                                                                                       - if ( shift == 0 ){                                    ## Task: generate a corrected patch..
         11          }                                                          Line6: {'i': 7, ......, 'cache': 128, 'shift': 6} ......
                                                                                                                                           + if ( shift < 0 ){                                     ## Input: Bug_Info,
         12     }                                                               Line13: {'length': 8, 'shift': 6, 'cache': 128}
                                                                                                                                           Trace Diff:                                             Validation_FeedBack
         13     if (length > 0 && shift > 0) {                                  Line13: {'type': 'branch', 'executed': True}                                                                       Root Cause: The final flush condition
                                                                                                                                           - Line7: {'type': 'branch', 'executed': True}
         14          header.write(cache);                                                                                                                                                          is inconsistent with the updated in-
         15     }                                                                             B. Repairing with                            + Line6: {'i': 7, ......, 'cache': 258, 'shift': -1}
                                                                                                                                           + Line7: {'type': 'branch', 'executed': False}          loop flush logic.
         16 }                                                                             Static + Dynamic Context                         - Line13: {'shift': 6, 'cache': 128}                    Modification Suggestion: Flush
                                                                                          ## Task: generate a corrected patch...           + Line13: {'shift': 7, 'cache': 0}                      remaining bits only when shift < 7.
                           Static Program Context                                         ## Input: Bug_Info, Program_Context
                                                                                                                                                                                                   The refined patch correctly flushes
         private void testCompress252(int numberOfFiles,                                  , Execution_Trace                                               Re-diagnosis                             the remaining bits after the loop.
               int numberOfNonEmptyFiles) throws Exception {
           import java.io.DataOutput;                                                     Change `shift > 0` to `shift < 8` to                  Why does the initial patch cause a                 ......
              ......                                                                      ensure any remaining cached bits are                                                                     if (shift < 0) {
           import   java.io.DataOutputStream;
               private void      writeFileEmptyFiles(final DataOutput header)                                                                   header-termination failure?
              verifyCompress252(output,         numberOfFiles,                            flushed after writing.                                                                                          header.write(cache);
           import java.io.File;
                       throws     IOException {
                    numberOfNonEmptyFiles);}                                              ......                                                                                                   ......
                           ......
           import org.apache.commons.compress.archivers.                                                                                      After the initial patch, Line 14
                         writeBits(out, emptyFiles, emptyStreamCounter);                  if (length > 0 && shift < 8 ) {                     writes 0 instead of 128, causing the                 if (length > 0 && shift < 7 )
                         out.flush();                                                            header.write(cache);                         header to terminate incorrectly.                     ......
                         ......}}                                                         ......                                                                                                                                 All Tests Pass
                                                                                                             Unknown property 128



Fig. 1: A motivating example based on Compress-21, illustrating the need for dynamic execution trace, question-driven diagnosis, and feedback-guided
refinement in APR.



failing tests, and validation feedback, but do not expose fine-                                                                     As shown in the Validation Feedback panel, the initial patch
grained execution traces such as executed paths, variable                                                                           changes if (shift == 0) to if (shift < 0), which
states, and branch outcomes. As shown in the A. Repairing                                                                           removes the original failure Unknown property 128 but
with Static Context panel, given only bug information and                                                                           introduces a new failure, Badly terminated header.
static context, the model changes header.write(cache)                                                                               If validation is treated only as a pass/fail signal, the model
to header.write(cache & 0xFF). This patch appears                                                                                   receives limited guidance for the next repair attempt. In-
to address the symptom suggested by Unknown property                                                                                stead, P RAC R EPAIR extracts structured validation feedback,
128, but still fails with the same error. In contrast, the Dy-                                                                      including the validation diagnostic, code diff, and trace diff
namic Execution Trace panel reveals how cache and shift                                                                             between the original and patched executions. The trace diff
evolve across loop iterations and exposes the runtime state                                                                         reveals that after the initial patch, the post-loop write becomes
where the failure is triggered. However, complete execution                                                                         inconsistent with the updated in-loop flush behavior, localizing
traces in real programs may contain many irrelevant calls,                                                                          the remaining issue to the final flush condition. This leads
branches, and state changes, and directly exposing them to the                                                                      to the refined patch if (length > 0 && shift < 7),
LLM may overwhelm the repair context. This motivates static-                                                                        which passes all tests. This motivates feedback-guided patch
dynamic context construction in Stage I of P RAC R EPAIR.                                                                           refinement in Stage III of P RAC R EPAIR.
C2: Raw static-dynamic context is not self-explanatory.
Recent agentic APR methods, such as RepairAgent [26]                                                                                                                                  III. A PPROACH
and ReInFix [28], allow the model to interact with external                                                                            Figure 2 shows the overall workflow of P RAC R EPAIR,
tools, retrieve additional context, or refine patches iteratively.                                                                  which aims to improve automated program repair by drawing
However, richer context alone does not guarantee that the                                                                           inspiration from human-like debugging practices. To achieve
model will identify the failure-relevant behavior. To illustrate                                                                    this goal, P RAC R EPAIR first extracts static program context
this issue, the B. Repairing with Static + Dynamic Context                                                                          from the project and collects dynamic execution trace from
panel shows what may happen when the model is provided                                                                              triggering test runs to build a context basis for repair, while
with additional dynamic evidence without explicit diagnostic                                                                        providing a uniform interface for the LLM to access the
guidance. This suggests that raw context is useful but not self-                                                                    needed information on demand; instead of directly using this
explanatory: the model still needs to determine which runtime                                                                       evidence for patch generation, it then guides the LLM to diag-
states matter and how they explain the faulty logic. In the                                                                         nose faulty program behaviors by incrementally raising and an-
Question-driven Diagnosis panel, targeted questions such as                                                                         swering diagnostic questions, thereby formulating an explicit
What are cache and shift when if (shift == 0)                                                                                       repair hypothesis; finally, it generates and validates candidate
is entered? and How should the in-loop flush condition be                                                                           patches, analyzes the code-level and behavioral differences
changed? guide the model to focus on the premature flush                                                                            introduced by each patch, and feeds these diagnostic signals
and formulate a more precise repair hypothesis. This motivates                                                                      back into failure diagnosis to iteratively refine the repair.
question-driven failure diagnosis in Stage II of P RAC R EPAIR.                                                                     Specifically, P RAC R EPAIR contains three main stages: Static-
C3: Patch-validation dynamics are often underused. Itera-                                                                           dynamic Context Construction (Stage I), Question-driven Fail-
tive APR methods commonly use validation results to refine                                                                          ure Diagnosis (Stage II), and Feedback-guided Patch Re-
patches [25]–[27], but validation feedback is often reduced to                                                                      finement (Stage III). During repair, P RAC R EPAIR maintains
coarse outcomes such as pass/fail results or error messages.                                                                        three intermediate artifacts: the diagnostic QA history, the
IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 14, NO. 8, AUGUST 2021                                                                                                                                 4



         Stage I: Static-dynamic Context Construction                         Stage II: Question-driven Failure Diagnosis                         Stage III: Feedback-guied Patch Refinement
                         CPG Constructing                                                                                                          Feedback Extracting and
                                                                                                                                                       Re-diagnosing
                                     Code Property Graph (CPG)
                                                                                                                             （         ）
                                                                               QA Pairs
                                                                 Diagnostic              Buggy Code Test Suite Failure Info Feedback
                                                                  Answer      (Optional)                                     Optional                                            All Tests   Y
                         Unified Context Access Interface                                                             Inputs to Diagnosis                                         Pass?
        Project                                                                                                                                      Refinement Loop for
                                                                        Diagnosis Loop for MAX Rounds                                                    MAX Rounds
                                                                                                              Stopping                                                              N
                    Bytecode            Tests                                                                                                       Patch
                  Instrumenting        Running                                                               Criteria met                         Generating
                                                                                                                                                                       Patch
                            ByteCode    Execution Trace Table                     Diagnostic                                           Repair              Candidate Validating Validation Plausible
                                                                 Answering                          Asking             Formulating   Hypothesis              Patch
                                                                                  Question                                                                                        Result    Patch
                  Trace Collecting



                                                                   Fig. 2: The Overall Framework of P RAC R EPAIR.



repair hypothesis, and the validation feedback. The diagnosis                                        collects runtime execution evidence from triggering test execu-
loop updates the QA history by asking and answering one                                              tions. Since the goal is to observe actual failing behavior with-
diagnostic question at a time, and terminates when no further                                        out modifying source code semantics, we adopt non-intrusive
question is needed or the diagnosis budget is exhausted. The                                         bytecode instrumentation [34]. Specifically, P RAC R EPAIR in-
refinement loop updates the repair hypothesis using feedback                                         struments Java bytecode using JavaAgent [35] and ASM [36],
from failed candidate patches, and terminates when a plausible                                       and then executes the triggering tests to record runtime states.
patch is found or the refinement budget is exhausted. In our                                         Considering that dynamic execution information can be ex-
implementation, the diagnosis and refinement budgets are set                                         tremely large in real-world programs, P RAC R EPAIR focuses
to 10 and 3, respectively, and both serve as upper bounds rather                                     trace collection on the buggy function under triggering test
than mandatory numbers of rounds.                                                                    executions, so as to capture failure-relevant runtime behavior
                                                                                                     while controlling trace noise and token overhead. We apply
A. Static-dynamic Context Construction                                                               statement-level instrumentation to capture execution evidence
                                                                                                     with sufficient granularity for diagnosis while controlling trace
   As shown in Figure 2, the goal of Static-dynamic Context                                          noise. P RAC R EPAIR records the executed statement sequence
Construction is to build a failure-relevant context basis for                                        within the buggy function, the values of in-scope variables
subsequent diagnosis and repair. To simulate how developers                                          after each executed statement, and the outcomes of conditional
debug in practice, P RAC R EPAIR must support the LLM in                                             branches. For object-type variables, fields are recursively se-
understanding both where failure-relevant logic resides in the                                       rialized up to a depth of 3 to balance contextual richness and
program and how the faulty behavior is actually triggered                                            token efficiency. The collected runtime evidence is organized
during execution. This requires two complementary sources of                                         into an Execution Trace Table, where each table corresponds to
evidence. Static information is needed to expose the structural                                      a specific <triggering test, buggy function> pair and records
and semantic context of the bug, such as surrounding imple-                                          the executed statements, their associated runtime states, and
mentations, control structures, call relationships, and value-                                       branch outcomes.
flow dependencies. Dynamic information is needed to reveal
the concrete failure behavior at runtime, including executed                                            3) Unified context access interface.: The static and dy-
paths, branch outcomes, variable states, and failure-triggering                                      namic context constructed above is not provided to the LLM
execution conditions. To unify these two complementary                                               all at once. Instead, P RAC R EPAIR exposes it through a uniform
sources for diagnosis and repair, P RAC R EPAIR provides a                                           interface that supports on-demand retrieval during diagnosis.
uniform interface to access the required information.                                                This design avoids overwhelming the LLM with the full
   1) Static context construction via CPG construction.: To                                          project context and long execution traces, while allowing
support diagnosis of failure-relevant program structure and                                          context retrieval to be guided by the current diagnostic need,
semantics, P RAC R EPAIR first performs static program analysis                                      similar to how developers inspect code and execution behavior
on the input project and constructs a Code Property Graph                                            during debugging.
(CPG). We use Joern [32] to parse the project source code                                               For static evidence, the interface supports three forms of
and build the CPG [33], which unifies the abstract syntax tree                                       access: (1) dependency and entity localization, which helps
(AST), control-flow graph (CFG), and data-dependence rela-                                           identify relevant program entities and resolve referenced types;
tions into a single representation. Based on this representation,                                    (2) structured definitions and code inspection, which helps
P RAC R EPAIR can access not only syntactic entities such as                                         inspect classes, methods, and implementations to understand
classes, methods, and statements, but also semantic relations                                        surrounding logic and identify candidate modification points;
such as control branches, call edges, and variable definition–                                       and (3) structural and semantic relation inspection, which
use chains. This static evidence is important for understanding                                      helps reason about control constructs, caller relationships,
the structural context of the buggy code, locating related                                           and variable definition–use chains. For dynamic evidence,
program entities, tracing inter-procedural dependencies, and                                         the interface supports three common debugging needs: (1)
reasoning about how values and control decisions propagate                                           execution-path inspection, which helps understand what ac-
to failure-relevant locations.                                                                       tually happens during failing execution; (2) runtime-value
   2) Dynamic context construction via trace collection.: To                                         inspection, which helps track variable evolution and identify
support the diagnosis of faulty behavior, P RAC R EPAIR further                                      abnormal state changes; and (3) statement-level state inspec-
IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 14, NO. 8, AUGUST 2021                                                                                                                                                         5


                                                        TABLE I: Unified interface for accessing static and dynamic context in P RAC R EPAIR
 Access Capability                           Function Calls                                                          Diagnostic Use
 Dependency & entity localization            get_imports_of_path;         find_class;         find_method            Support why- and how-type questions by locating referenced entities and dependencies
 Structured definitions & code inspection    get_definition_of_class; get_definition_of_method; get_code_of_method   Support how-type questions by inspecting surrounding logic and candidate modification points
 Structural & semantic relation inspection   get_structure_of_method;get_callers_of_method;get_def_use_of_variable   Support why-type questions by analyzing control flow, caller relations, and value propagation
 Execution-path inspection                   get_execution_path                                                      Support what-type questions by revealing what actually happens during failing execution
 Runtime-value inspection                    get_runtime_values                                                      Support what- and why-type questions by tracking variable evolution and abnormal states
 Statement-level state inspection            get_state_at_statement                                                  Support what-, why-, and how-type questions by examining concrete states and checking repair hypotheses




tion, which helps examine concrete program states at specific                                           question. For example, a what-type question may target the
locations and check whether a repair hypothesis is consistent                                           value of a variable at a suspicious statement, while a why-
with the observed execution.                                                                            type question may target the control or data dependency that
   Table I summarizes the function calls that implement these                                           explains an abnormal state. This constrained format makes the
context access capabilities. Together, the static and dynamic                                           diagnosis process traceable and prevents the model from ask-
evidence constructed in this stage, along with the uniform                                              ing multiple unrelated questions in one round. The diagnosis
access interface, provide the information basis for the next                                            loop terminates when either the diagnosis budget is reached
stage, Question-driven Failure Diagnosis (Section III-B).                                               or the LLM returns the stopping signal.
                                                                                                           2) Question Answering.: To answer each diagnostic ques-
B. Question-driven Failure Diagnosis                                                                    tion, P RAC R EPAIR lets the LLM retrieve failure-relevant con-
                                                                                                        text through the unified interface in Section III-A. Depending
   As illustrated in Stage II of Figure 2, P RAC R EPAIR does                                           on the question type, the LLM may inspect static evidence,
not directly generate a patch from the context constructed in                                           such as dependencies, implementations, and structural rela-
Section III-A. Instead, it first transforms the collected evidence                                      tions, or dynamic evidence, such as execution paths, runtime
into diagnostic understanding through question-driven failure                                           values, and statement-level states. Inspired by ReAct [37],
diagnosis. This stage takes as input the buggy code, test suite,                                        this process interleaves reasoning and retrieval until enough
failure information, the accumulated diagnostic QA history,                                             evidence is collected to answer the question. The resulting
and optionally the validation feedback returned from Stage III.                                         answer is paired with the question and appended to the QA
At each round, P RAC R EPAIR raises one diagnostic question,                                            history for subsequent diagnosis. When Stage III returns vali-
retrieves the evidence needed to answer it, and appends the                                             dation feedback, the same loop incorporates it to re-diagnose
resulting QA pair to the diagnosis history. Each QA pair                                                the current patch behavior.
records the question, retrieved evidence, diagnostic answer,
                                                                                                           3) Repair Hypothesis Formulating.: When the diagnosis
and repair implication. The loop terminates when the diagnosis
                                                                                                        loop terminates, P RAC R EPAIR formulates an explicit repair
budget is exhausted or the accumulated QA history is suffi-
                                                                                                        hypothesis based on the accumulated QA history and the
cient to formulate a repair hypothesis. Finally, P RAC R EPAIR
                                                                                                        currently available failure-relevant evidence. The hypothesis
summarizes the diagnostic findings into an explicit repair
                                                                                                        is represented in a structured form with four fields: faulty
hypothesis.
                                                                                                        behavior, which describes the observed abnormal execution;
   1) Question Asking.: Prior studies show that questions
                                                                                                        supporting evidence, which records the key QA findings
are central to debugging and program understanding [7],
                                                                                                        and retrieved context; suspected root cause, which explains
[8]. Accordingly, P RAC R EPAIR reduces diagnostic uncertainty
                                                                                                        why the failure occurs; and modification suggestion, which
through three question types, grounded in the context access
                                                                                                        specifies how the faulty logic should be changed. For exam-
capabilities in Table I.
                                                                                                        ple, in Figure 1, the hypothesis identifies premature flushing
   • What-type questions establish factual understanding of                                             at shift == 0 as the faulty behavior, uses the observed
      the failing execution, such as executed statements, branch                                        values of cache and shift as supporting evidence, and
      outcomes, variable evolution, and deviations from ex-                                             suggests changing the in-loop flush condition. This structured
      pected behavior, mainly using dynamic evidence.                                                   hypothesis serves as the output of Stage II and the input to
   • Why-type questions explain the failure by connecting                                               Stage III, bridging diagnosis and patch generation.
      abnormal runtime behavior to underlying program logic,
      such as incorrect control flow, abnormal state transitions,
      or invalid data dependencies, using both static and dy-                                           C. Feedback-guided Patch Refinement
      namic evidence.                                                                                      As illustrated in Stage III of Figure 2, P RAC R EPAIR turns
   • How-type questions determine how to change the faulty                                              the repair hypothesis produced by Question-driven Failure
      logic to restore the intended semantics, mainly using the                                         Diagnosis into an iterative loop. Rather than treating validation
      diagnosed root cause and static code context.                                                     as a simple pass/fail check, this stage explicitly analyzes the
   To avoid unnecessary diagnostic overhead, P RAC R EPAIR                                              behavioral differences before and after patching and uses them
does not ask all questions at once. Instead, it requires the LLM                                        as new evidence for subsequent diagnosis. In this way, Stage
to make a structured diagnostic decision at each step. The                                              III closes the loop between repair and diagnosis: a repair
decision either raises one new diagnostic question or returns                                           hypothesis guides patch generation, patch validation reveals
a stopping signal. When raising a question, the LLM must                                                how the patched execution differs from the original failing
specify the question type, the target program entity or runtime                                         execution, and unsuccessful validation produces feedback that
behavior to inspect, and the evidence needed to answer the                                              is fed back into Stage II to refine the diagnosis and the next
IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 14, NO. 8, AUGUST 2021                                                                6



repair hypothesis. This refinement loop continues until the           removed statement executions, and divergent runtime values.
maximum number of refinement rounds is reached (i.e., 3),             The resulting feedback therefore explains not only whether the
or terminates earlier once a plausible patch is found.                patch fails, but also how the patch changes the failing behavior.
   1) Patch Generating.: Given the current repair hypothe-               This extracted feedback is then fed back into Question-
sis, P RAC R EPAIR prompts the LLM to generate a candidate            driven Failure Diagnosis as optional diagnostic input, as
patch for the buggy function. The patch-generation prompt is          shown in Figure 2. Based on the original bug context, the
constructed from three parts: (1) bug context, including the          accumulated QA history, and the new feedback, the LLM re-
buggy function, triggering tests, and failure information; (2)        diagnoses the current patch failure. For instance, if the trace
repair hypothesis, including the suspected root cause of the          diff shows that a branch outcome changes but the failing value
failure and the corresponding modification suggestions; and           remains abnormal, the next diagnosis round can ask why the
(3) generation instruction, which directs the LLM to produce          changed branch still does not restore the expected state. The
a corrected implementation of the buggy function. In this way,        resulting QA pairs are used to refine the repair hypothesis,
patch generation is guided not only by the observed symptom,          which then guides the next round of patch generation and
but also by the explicit diagnostic understanding accumulated         validation. Through this feedback-guided loop, P RAC R EPAIR
in Stage II. To preserve input clarity and minimize prompt            progressively improves candidate patches until a plausible fix
bias, P RAC R EPAIR adopts a zero-shot prompting strategy, with       is found or the refinement budget is exhausted.
patch generation relying solely on the structured prompt rather
than in-context examples. Due to page limits, all AI prompt                             IV. E XPERIMENT D ESIGN
templates are provided in the artifact [38].                             To evaluate our approach, we design experiments to answer
   2) Patch Validating.: After generating a candidate patch,          the following research questions (RQs):
P RAC R EPAIR applies it to the original program and validates
                                                                       • RQ1 (Repair Effectiveness): How effective is P RAC R E -
the patched program through compilation and test execution.
                                                                         PAIR compared with existing APR tools under the standard
During this process, P RAC R EPAIR also collects execution
                                                                         perfect fault localization setting, and does it remain effec-
traces from the patched program using the same trace col-
                                                                         tive when exact fault locations are unavailable?
lection procedure described in Section III-A, so that patched
                                                                       • RQ2 (Repair Scenarios): How well does P RAC R EPAIR
behaviors can later be compared with the original failing
                                                                         perform across different repair scenarios?
execution. If the patched program compiles successfully and
                                                                       • RQ3 (Ablation Study): What are the individual contribu-
passes all tests within the maximum execution time (i.e., 10
                                                                         tions of each component of P RAC R EPAIR to the overall
minutes), the patch is regarded as a plausible patch.
                                                                         improvement in repair effectiveness?
   3) Feedback Extracting and Re-diagnosing.: If a candidate
                                                                       • RQ4 (Generalizability Study): How effectively does
patch does not pass validation, P RAC R EPAIR does not treat the
                                                                         P RAC R EPAIR generalize to unseen datasets when deployed
result as a simple failure signal. Instead, it first determines how
                                                                         with different underlying foundation models?
the current repair attempt fails, because different validation
outcomes provide different high-level directions for the next
diagnosis round. For example, a compilation failure indicates         A. Datasets
that the patch itself is syntactically or semantically invalid.          Since our approach is implemented and evaluated in the
   To provide such high-level guidance, P RAC R EPAIR first           Java APR setting, we use two Java bug-repair benchmarks,
categorizes invalid validation results into four outcomes: (1)        Defects4J [3] and RWB (Real-World Bugs) [27]. We therefore
compilation failures, where the patched program cannot be             do not include datasets in other programming languages,
compiled; (2) runtime failures, where the patched program             such as SWE-Bench, in this study. For the Defects4J dataset,
compiles successfully but triggers runtime exceptions or time-        following prior studies [25], [27], [28], we split it into V1.2
outs during testing; (3) remaining failures, where the origi-         (391 bugs after removing 4 deprecated ones) and V2.0 (438
nally failing test(s) are still not fully fixed; and (4) regression   new bugs). We also follow [25], [27], [28] to categorize bugs
failures, where the original failure is resolved but previously       into four repair scenarios: multi-function (MF), where a fix
passing tests become failing. After establishing this coarse-         involves multiple functions; single-function (SF), where a fix
grained diagnosis direction, P RAC R EPAIR further extracts           is confined to one function; single-hunk (SH), where a fix
three complementary forms of feedback to understand why               modifies one contiguous code region; and single-line (SL),
the patch fails. First, it collects validation diagnostics, such      where a fix changes only one line. Note that SH ⊆ SF and SL
as compiler errors, runtime exceptions, timeout messages, or          ⊆ SH. Table II shows the statistics. For the generalizability
updated failing tests, to describe the observed failure outcome.      study, we use the recent benchmark RWB (Real-World Bugs)
Second, it computes a code diff between the generated patch           introduced by ThinkRepair [27], which consists of two ver-
and the original buggy function to identify which statements or       sions. RWB V1.0 comprises bug-fixing commits after October
conditions have been changed. Third, it computes a trace diff         2021, while RWB V2.0 includes bug-fixing commits after
between the original and patched executions. To compute the           March 2023, resulting in 44 and 29 single-function bugs,
trace diff, P RAC R EPAIR executes the same triggering tests on       respectively. For fault information, to eliminate potential bias
both versions, collects traces using the same instrumentation         introduced by different fault localization (FL) tools, we follow
procedure, aligns trace records by executed statement and exe-        recent APR studies [25]–[28] and use perfect fault localization
cution order, and extracts changed branch outcomes, added or          as the default setting, where the repair system is provided
IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 14, NO. 8, AUGUST 2021                                                               7


                   TABLE II: Statistics of Studied Datasets.
                                                                       and Question-driven Failure Diagnosis. Specifically, it re-
   Dataset         #Total Bugs #MF Bugs #SF Bugs #SH Bugs #SL Bugs     tains only Feedback-guided Patch Refinement, allowing the
   Defects4J 1.2       391         136       255        154    80      model to iteratively improve patches based on feedback.
   Defects4J 2.0       438         210       228        159    78
                                                                     • w/o SDC: This variant evaluates the contribution of Static-
   #Sum                909         346       563        390    235
                                                                       dynamic Context Construction. It preserves Question-driven
                                                                       Failure Diagnosis and Feedback-guided Patch Refinement,
with the exact buggy statement location(s). In addition, to            but removes the structured repair context built from static
examine whether the effectiveness of P RAC R EPAIR depends             and dynamic evidence.
on this idealized assumption, we further include a relaxed           • w/o DI: This variant evaluates the contribution of dynamic

fault-localization setting in RQ1, where exact buggy statement         execution information in Static-dynamic Context Construc-
locations are not provided.                                            tion. Specifically, it removes dynamic traces and retains
                                                                       only static program context with failure information.
B. Implementation                                                    • P RAC R EPAIR CoT : This variant evaluates the contribution
                                                                       of the proposed diagnosis strategy in Question-driven Fail-
   For the base models, we use gpt-3.5-turbo [39] and
                                                                       ure Diagnosis. It replaces question-driven diagnosis with
gpt-4o [40] in our main experiments to maintain direct
                                                                       Chain-of-Thought prompting, in which the model formu-
comparability with prior APR studies. Following [41], we
                                                                       lates a repair hypothesis from the buggy code, failure infor-
set the sampling temperature to 1.0. To further evaluate
                                                                       mation, and execution traces, similar to ThinkRepair [27].
whether P RAC R EPAIR remains effective with newer foun-
                                                                     • P RAC R EPAIR ReAct : This variant is designed to investigate
dation models, we additionally study its generalizability in
                                                                       the contribution of question-driven diagnosis. Specifically,
RQ4 (Section V-D) using gpt-4 [42], Llama-3 [43], and
                                                                       it allows the LLM to use function calls, but replaces
DeepSeek-v3 [44]. We set the maximum number of repair
                                                                       the proposed diagnosis strategy with direct interleaving of
sessions to 3 per bug, where each session is independent
                                                                       reasoning and tool use, similar to ReInFix [28].
and starts from the original bug context. Within each session,
the diagnosis loop is allowed to run for at most 10 rounds,
although in practice the average number of rounds is no more         D. Metrics
than 5, since the loop terminates once no further diagnostic            Following prior work [25]–[28], we report two widely
questions are raised. The refinement loop is allowed to run for      adopted metrics to evaluate repair effectiveness:
at most 3 rounds, since this setting achieves a better balance        • Number of plausible patches: The number of bugs for
between repair effectiveness (cf. Section V-C). All experiments         which at least one generated patch passes all developer-
were conducted on a workstation running Ubuntu 20.04, with              written test cases [21], [22]. A plausible patch satisfies the
a 16-core Intel Xeon processor, 192GB of RAM, and eight                 test oracle but is not necessarily semantically correct.
NVIDIA A800 GPUs.                                                     • Number of correct patches: The number of bugs for which
                                                                        at least one generated patch is semantically correct. To
C. Baselines                                                            determine correctness, we first check whether a generated
   In our comparative evaluation, we evaluate P RAC R EPAIR             patch matches the developer-provided fix; otherwise, we
against nine state-of-the-art baselines. These baselines include        manually assess its semantic equivalence. A patch is con-
one traditional APR method, TBar [18]; three learning-based             sidered correct if it passes either of these checks [19].
APR methods, SelfAPR [19], KNOD [22], and Tare [20]; and
five recent LLM-based APR methods, including Codex [45],                                    V. E VALUATION
AlphaRepair [24], ChatRepair [25], ThinkRepair [27], Re-             A. RQ1: Repair Effectiveness
pairAgent [26], and ReinFix [28]. Since our evaluation adopts           We evaluate the repair effectiveness of P RAC R EPAIR on
the same benchmark split, fault-localization setting, and repair     Defects4J under both the standard perfect fault localization
metrics as these studies, we follow common practice in the           setting and a relaxed setting where exact buggy statement
APR community [19], [24], [25], [27], [28] and reuse the             locations are unavailable. Under the standard setting, we first
repair results reported in their original papers [18]–[20], [22],    compare P RAC R EPAIR with existing APR tools on repair
[24]–[28] instead of directly running these APR tools.               results, and then further analyze its unique repair capability.
   To conduct the ablation study and investigate the contribu-       Under the relaxed setting, we examine whether P RAC R EPAIR
tion of different components of P RAC R EPAIR, we design the         remains effective without perfect fault localization.
following variants by removing or replacing components of            Effectiveness under Perfect Fault Localization. Following
the framework.                                                       the standard setting used in prior APR studies, we instantiate
 • w/o SDC+QFD+FPR: This variant is designed to evaluate             P RAC R EPAIR with two foundation models, GPT-3.5 [39] and
    the overall contribution of the proposed three-stage frame-      GPT-4o [40], referred to as P RAC R EPAIRGPT-3.5 and P RAC R E -
    work. Specifically, it removes all three stages and directly     PAIR GPT-4o , respectively. As shown in Table III, P RAC R E -
    prompts the underlying LLM to generate a patch from the          PAIR GPT-3.5 generates plausible fixes for 332 bugs and correct
    given bug information.                                           fixes for 275 bugs. With GPT-4o, P RAC R EPAIRGPT-4o further
 • w/o SDC+QFD: This variant is designed to investigate              improves to 413 plausible fixes and 333 correct fixes. Since
    the contribution of Static-dynamic Context Construction          plausible patches pass all test cases but are not necessarily
IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 14, NO. 8, AUGUST 2021                                                                                                                                   8


                     TABLE III: Repair results (correct patches / plausible patches) of APR tools under perfect fault localization on Defects4J.

 APR Tool            P RAC R EPAIRGPT-4o   P RAC R EPAIRGPT-3.5   ReInFixGPT-4o   ReInFixGPT-3.5   ChatRepair   ThinkRepair   RepairAgent      AlphaRepair      KNOD       Tare    SelfRepair    TBar

 Chart                     19/22                  18/20               18/20           16/17           15/–         11/–          11/14             9/–           10/11     11/–        7/–        11/–
 Closure                   40/52                  34/40               40/50           30/37           37/–         31/–          25/25            23/–           23/29     25/–       17/–        16/–
 Lang                      44/49                  36/39               33/47           26/33           21/–         19/–          17/17            13/–           11/13     14/–       10/–        13/–
 Math                      42/70                  38/54               39/68           35/52           32/–         27/–          29/29            21/–           20/25     22/–       18/–        22/–
 Mockito                   10/11                   9/9                10/11            8/9             6/–          6/–           6/6              5/–            5/5       2/–        3/–         3/–
 Time                       7/9                    4/5                 6/11            3/4             3/–          4/–           2/3              3/–            2/2       3/–        3/–         3/–

 #Total (D4J V1.2)        162/213                139/167            146/207          118/152         114/–          98/–         90/94           74/109          71/85     77/–       58/–       68/95
 #Total (D4J V2.0)        171/200                136/165            145/190          123/147          48/–         107/–         74/92            36/–           50/85      –/–       42/–        8/–

 #Sum                     333/413                275/332            291/397          241/299         162/–         205/–        164/186          110/109        121/170    77/–      100/–       76/95
Note: “–” indicates that no result was reported in the original work.


                                                                                                    TABLE IV: Repair results (correct patches / plausible patches) without perfect
                                                                                                    fault localization on Defects4J V1.2.

                                                                                                      APR Tool                P RAC R EPAIRNo-PFL ThinkRepairNo-PFL Codex
                                                                                                      Chart                              12/16                             9/–                  –/–
                                                                                                      Closure                            28/32                            19/–                  –/–
                                                                                                      Lang                               23/31                            15/–                  –/–
                                                                                                      Math                               32/43                            27/–                  –/–
                                                                                                      Mockito                             7/8                              7/–                  –/–
     (a) vs. GPT-3.5-based result                      (b) vs. GPT-4o-based result
                                                                                                      Time                                3/3                              3/–                  –/–
Fig. 3: Venn diagram of correct patches of P RAC R EPAIR vs. LLM-based
                                                                                                      #Total (D4J V1.2)              105/133                              80/–                  63/–
baselines on Defects4J V1.2 and V2.0.
                                                                                                    Note: “–” indicates that no result was reported in the original work.

                                                                                                      TABLE V: Repair results (correct fixes) under different repair scenarios.
semantically correct, these results indicate that P RAC R EPAIR
not only satisfies the test oracle on a large number of bugs, but                                     Benchmark                     Defects4J V1.2                         Defects4J V2.0
also achieves strong repair accuracy. In addition, P RAC R EPAIR                                      Repair Scenario          MF         SF     SH        SL      MF        SF        SH        SL
successfully fixes bugs across all Defects4J projects, including
                                                                                                      ChatRepair                –        76        –       –         –         –         –        48
Chart, Closure, Lang, Math, Mockito, and Time, demonstrat-                                            ThinkRepair               –        98       78       52        –       107        81        47
ing its effectiveness across projects from different domains.                                         RepairAgent               7        83       71       51        6        68        65        48
   Compared with prior work, P RAC R EPAIR consistently out-                                          ReInFixGPT-3.5           14        104      78       53       14       109       85         47
                                                                                                      ReInFixGPT-4o            22        124      93       57       15       130       103        56
performs the strongest baseline, ReInFix, on both Defects4J                                           P RAC R EPAIRGPT-3.5     19        120      90       55       15       121       92         51
V1.2 and V2.0. On Defects4J V1.2, P RAC R EPAIRGPT-4o im-                                             P RAC R EPAIRGPT-4o      27        135      97       57       18       153       108        57
proves over ReInFixGPT-4o by 16 correct fixes, while P RAC R E -                                    Note: “–” indicates that no result was reported in the original work.
PAIR GPT-3.5 exceeds ReInFixGPT-3.5 by 21 fixes. Similar gains
are observed on the more challenging Defects4J V2.0 bench-
mark, where P RAC R EPAIRGPT-4o and P RAC R EPAIRGPT-3.5 out-                                       further evaluate it under GPT-3.5 without providing exact
perform their ReInFix counterparts by 26 and 13 bugs, re-                                           fault locations, referred to as P RAC R EPAIRNo-PFL . We compare
spectively. In addition, under GPT-3.5, P RAC R EPAIR also                                          it with available baselines under the same setting, including
surpasses other recent LLM-based APR approaches, including                                          ThinkRepairNo-PFL [27] and Codex [45], on Defects4J V1.2.
ChatRepair, ThinkRepair, and RepairAgent.                                                           As shown in Table IV, P RAC R EPAIRNo-PFL fixes 105 bugs
Unique Fix Analysis. We further analyze the unique repair                                           correctly and generates 133 plausible patches. Although this
capability of P RAC R EPAIR on Defects4J V1.2 and V2.0.                                             is lower than P RAC R EPAIRGPT-3.5 under perfect fault localiza-
Specifically, we compare the sets of correctly repaired bugs                                        tion (139 correct and 167 plausible patches), it outperforms
produced by P RAC R EPAIR and recent LLM-based APR base-                                            ThinkRepairNo-PFL and Codex by 25 and 42 correct fixes,
lines under the same base model setting. As shown in Figure 3,                                      respectively. These results show that fault locations are helpful,
under GPT-3.5, P RAC R EPAIRGPT-3.5 achieves 75 unique correct                                      but P RAC R EPAIR remains effective when they are unavailable.
fixes, compared with 29 for ThinkRepair, 26 for RepairAgent,
and 12 for ChatRepair. Under GPT-4o, P RAC R EPAIRGPT-4o                                             Answer to RQ1: P RAC R EPAIR achieves the best overall
achieves 93 unique correct fixes, while ReInFix achieves 51.                                         repair effectiveness under perfect fault localization with
We exclude ReInFix from the GPT-3.5-based comparison be-                                             both GPT-3.5 and GPT-4o. Without exact buggy statement
cause its public results are only available under GPT-4o. These                                      locations, its performance decreases but still surpasses the
results show that P RAC R EPAIR maintains stronger unique                                            only comparable baseline, showing that its effectiveness
repair capability than existing LLM-based APR baselines,                                             does not solely rely on perfect fault localization.
suggesting that its repair process complements prior methods.
Effectiveness without Perfect Fault Localization. The above
comparisons assume perfect fault localization, where exact                                          B. RQ2: Repair Scenarios
buggy statement locations are provided. To examine whether                                             While RQ1 evaluates the overall repair effectiveness of
P RAC R EPAIR remains effective without this assumption, we                                         P RAC R EPAIR, analyzing its performance under specific repair
IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 14, NO. 8, AUGUST 2021                                                                          9


                                                                    TABLE VI: Repair results (correct patches / plausible patches) of the ablation
scenarios provides a more fine-grained understanding of its ca-     study on Defects4J V1.2.
pabilities across different levels of repair complexity. Follow-
ing prior work [26]–[28], we further examine P RAC R EPAIR                 Variant                   Result      MF      SF     SH     SL
under four commonly scenarios: single-line (SL), single-hunk               w/o SDC+QFD+FPR            84/98      7       77     55     38
(SH), single-function (SF), and multi-function (MF).                       w/o SDC+QFD               105/113     12      93     74     46
                                                                           w/o SDC                   115/126     16      99     77     48
Repair Scenarios Analysis. As shown in Table V, P RAC R E -                w/o DI                    120/137     17     103     80     49
PAIR achieves strong performance across all studied repair                 P RAC R EPAIRCOT          107/123     9       98     68     52
scenarios on both Defects4J V1.2 and V2.0. In the single-                  P RAC R EPAIRReAct        121/149     15     106     79     53
                                                                           P RAC R EPAIRGPT-3.5      139/167     19     120     90     55
function (SF) setting, it delivers the best overall results among
                                                                    Note: “–” indicates that no result was reported in the original work.
all compared approaches. On Defects4J V1.2, P RAC R E -
PAIR GPT-3.5 and P RAC R EPAIR GPT-4o repair 120 and 135 bugs,
respectively, while on Defects4J V2.0 the corresponding num-
bers further increase to 121 and 153, consistently exceeding
all baselines. In the single-hunk (SH) and single-line (SL)
settings, P RAC R EPAIR continues to match or surpass recent
LLM-based baselines, demonstrating its effectiveness across
simpler and more complex repair scenarios. More importantly,
P RAC R EPAIR shows clear advantages in the multi-function          Fig. 4: The performance of P RAC R EPAIR with different refinement rounds
(MF) setting. Compared with ReInFix, the only other base-
line explicitly supporting MF repair, P RAC R EPAIR achieves
higher repair counts on both dataset versions. For example,         contribute to repair effectiveness, and their combination yields
P RAC R EPAIRGPT-4o repairs 27 and 18 MF bugs on Defects4J          the strongest performance.
V1.2 and V2.0, compared with 22 and 15 for ReInFixGPT-4o .          Impacts of Dynamic Execution Traces. Table VI shows the
Overall, these results indicate that P RAC R EPAIR performs ro-     contribution of dynamic execution traces to P RAC R EPAIR.
bustly across diverse repair scenarios, with particularly strong    The w/o DI variant removes dynamic execution traces from
advantages on challenging multi-function bugs.                      Static-dynamic Context Construction, leaving only static pro-
                                                                    gram context and failure information. Compared with the full
 Answer to RQ2: P RAC R EPAIR consistently outperforms              system, this change reduces the number of correct patches
 prior methods across different repair scenarios, including         from 139 to 120 and the number of plausible patches from
 SL, SH, SF, and MF bugs. Its advantage is especially clear         167 to 137. These results indicate that dynamic execution
 on the more challenging multi-function setting.                    traces provide important failure-relevant evidence that cannot
                                                                    be fully recovered from static context alone. By exposing
                                                                    runtime behaviors, such as executed paths, branch outcomes,
C. RQ3: Ablation Study                                              and variable state changes, they help the model perform more
  To assess the impact of individual components in P RAC R E -      grounded diagnoses and repairs.
PAIR, we conduct an ablation study using the variants defined       Impacts of Reasoning Strategy. Table VI shows that, com-
in Section IV-C. These variants are designed by systematically      pared with plain CoT and ReAct, the proposed question-driven
removing or replacing key parts of the framework. Based on          diagnosis mechanism in Question-driven Failure Diagnosis
this design, we evaluate the contribution of each stage, as well    improves repair effectiveness. The one-shot P RAC R EPAIRCoT
as the effects of dynamic execution traces, diagnosis strategy,     variant, which does not use the designed function calls,
and refinement rounds. Due to computational budget con-             produces 107 correct patches. Allowing on-demand retrieval of
straints, all ablation experiments are conducted on Defects4J       failure-relevant evidence in P RAC R EPAIRReAct increases this
V1.2 with GPT-3.5.                                                  number to 121, which suggests that tool-assisted diagnosis can
Impacts of the Three Stages. Table VI reports the per-              be more effective than reasoning over a fixed input context
formance of several ablated variants, each designed to iso-         alone. The full P RAC R EPAIR further improves the result to
late the contribution of one stage in P RAC R EPAIR. The            139. Since both P RAC R EPAIRReAct and the full P RAC R EPAIR
w/o SDC+QFD+FPR variant performs the worst, achieving               support function-call interaction, this additional gain indicates
84 correct patches and 98 plausible patches. Adding only            that the proposed question-driven diagnosis provides bene-
Feedback-guided Patch Refinement in w/o SDC+QFD in-                 fits beyond tool use alone. By organizing diagnosis around
creases the number of correct patches to 105, showing the           targeted questions, P RAC R EPAIR appears to help the model
benefit of iterative refinement. Further adding Question-driven     systematically inspect failure-relevant evidence and formulate
Failure Diagnosis in w/o SDC raises the number of correct           repair hypotheses.
patches to 115, indicating that diagnosis improves repair           Impacts of Refinement Interaction Number. According to
beyond refinement alone. The full P RAC R EPAIR configuration       Figure 4, repair performance improves as the number of refine-
achieves the best results. Compared with w/o SDC, adding            ment interactions increases. Without refinement, P RAC R EPAIR
Static-dynamic Context Construction increases the number of         produces 89 correct patches, which increases to 107 and 119
correct patches from 115 to 139 and plausible patches from          after one and two refinement rounds, respectively, indicating
126 to 167. Overall, the results show that all three stages         that iterative feedback helps correct early patch errors. Per-
IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 14, NO. 8, AUGUST 2021                                                                          10


TABLE VII: Repair results (correct fixes) of the generalizability study on
RWB.
                                                                                   Answer to RQ4: P RAC R EPAIR generalizes well across both
                                                                                   unseen benchmarks and different foundation models. These
APR Tool              P RAC R EPAIR                ReInFix       ThinkRepair       results show that its repair framework is robust and not tied
LLM            G4 DS-v3 L3 G3.5 DS-C G4 G3.5 DS-C G3.5 DS-C                        to a specific dataset or model.
Cli             4     4      4    4      –     4    4        –    4      –
Codec           4     3      3    3      –     3    3        –    3      –                                 VI. D ISCUSSION
Collections     1     1      1    1      –     1    1        –    1      –
Compress        3     3      3    2      –     2    2        –    1      –        A. Repair Costs
Csv             1     1      1    1      –     1    1        –    1      –           Using LLMs may raise concerns about repair costs. To
Jsoup           7     8      7    7      –     7    6        –    6      –
                                                                                  address this, we follow prior work [25], [26], [28] and report
Lang            3     3      3    3      –     3    3        –    3      –
                                                                                  the average monetary cost per repaired bug based on the
# RWB V1.0 23         23    22   21      –    21    20     –     19       –       RQ1 results on Defects4J. For prior methods, we compare
# RWB V2.0 15         14    13   –      13    –      –    12      –      10
                                                                                  against the costs reported in their original papers. In our set-
Note: “–” indicates that no result was reported in the original work. G4/G3.5 =
GPT-4/GPT-3.5; DS-v3/DS-C = DeepSeek-v3/DeepSeek-Coder; L3=Llama-3.
                                                                                  ting, P RAC R EPAIRGPT-3.5 costs $0.04 per repaired bug, while
                                                                                  P RAC R EPAIRGPT-4o costs $1.13. Compared with prior LLM-
                                                                                  based APR methods, P RAC R EPAIR remains cost-efficient:
formance further improves to 139 correct patches after three                      under GPT-3.5, its cost is lower than ReInFixGPT-3.5 ($0.06),
rounds, but remains unchanged with additional interactions,                       RepairAgent ($0.14), and ChatRepair ($0.42), while under
showing diminishing returns beyond this point. Considering                        GPT-4o it also costs less than ReInFixGPT-4o ($1.45). These
both repair effectiveness and interaction cost, we adopt three                    results show that P RAC R EPAIR improves repair effectiveness
refinement rounds as the default setting.                                         while maintaining competitive repair cost.

 Answer to RQ3: P RAC R EPAIR is well designed, and                               B. Threats to Validity
 all three stages, i.e., Static-dynamic Context Construction,                     Internal Validity. One internal threat comes from the man-
 Question-driven Failure Diagnosis, and Feedback-guided                           ual validation of plausible patches. Since passing all test
 Patch Refinement, can be effectively integrated to improve                       cases does not guarantee semantic correctness, we first check
 the correct repair effectiveness of P RAC R EPAIR.                               whether a plausible patch exactly matches the developer-
                                                                                  provided fix; otherwise, we manually assess its semantic
                                                                                  equivalence, following prior APR work. Another threat comes
D. RQ4: Generalizability Study                                                    from potential data leakage, as some benchmark bugs or
   In the generalizability study, we evaluate P RAC R EPAIR                       reference patches may have appeared in the pre-training data of
on the RWB benchmark under the perfect fault localization                         the evaluated LLMs. To mitigate this concern, we additionally
setting, following ThinkRepair [27], and further instantiate                      evaluate P RAC R EPAIR on the RWB benchmark, whose bug-
P RAC R EPAIR with multiple foundation models, including                          fixing commits were collected after the training cutoff dates
GPT-4, GPT-3.5, DeepSeek-v3, DeepSeek-Coder, and Llama-                           of widely used LLMs. P RAC R EPAIR still achieves strong
3. We also report the published results of ThinkRepair [27]                       results on this benchmark under multiple foundation models,
and ReInFix [28] on the same benchmark for comparison.                            suggesting that its gains are not merely due to memorization.
Notably, RWB V1.0 and RWB V2.0 consist of bug-fixing                              External Validity. To reduce the risk of an unrepresentative
commits collected after the training cutoff dates of GPT-3.5                      evaluation, we assess P RAC R EPAIR on Defects4J and RWB,
and DeepSeek-Coder, respectively [27].                                            two widely used real-world Java bug benchmarks. However,
                                                                                  both datasets are limited to Java and may not fully repre-
Result Analysis. As shown in Table VII, P RAC R EPAIR
                                                                                  sent other programming languages or much larger codebases.
achieves the best or tied-best repair performance across both
                                                                                  Evaluating P RAC R EPAIR on additional languages and broader
RWB datasets and all evaluated model settings. On RWB V1.0
                                                                                  repair settings remains future work.
(44 bugs), P RAC R EPAIR repairs 23 bugs with GPT-4 and
DeepSeek-v3, outperforming ReInFix (21 bugs with GPT-4)
and ThinkRepair (19 bugs with GPT-3.5). Similar trends hold                                           VII. R ELATED W ORK
under other models: P RAC R EPAIR repairs 22 bugs with Llama-                        Existing APR approaches can be broadly categorized from
3 and 21 bugs with GPT-3.5, indicating stable effectiveness                       three perspectives: non-learning-based approaches, learning-
across different model backbones. On the more recent RWB                          based approaches, and LLM-based approaches.
V2.0 benchmark (29 bugs), P RAC R EPAIR again achieves the                        Non-learning-based Approaches. Automated program repair
strongest results, repairing 13 bugs with DeepSeek-Coder,                         has been widely studied for more than a decade [17]. Early ap-
compared with 12 and 10 repaired by ReInFix and ThinkRe-                          proaches formulate repair as a search problem with manually
pair, respectively. Moreover, when instantiated with open-                        designed mutation operators or fix patterns [18], [46]. Other
source models such as GPT-4, DeepSeek-v3, and Llama-3,                            techniques learn transformation templates or repair patterns
P RAC R EPAIR still maintains competitive repair effectiveness.                   from human-written patches [47], [48], or synthesize repairs
These results suggest that the proposed approach generalizes                      using symbolic execution, constraints, and SMT solving [49],
well across both benchmarks and foundation models, rather                         [50]. Additional work integrates repair into static analysis
than depending on a specific dataset or model family.
IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 14, NO. 8, AUGUST 2021                                                                                         11



pipelines or retrieves similar code fragments as repair ingredi-                    [3] René Just, Darioush Jalali, and Michael D. Ernst. Defects4j: a database
ents [51], [52]. Beyond functional bugs, prior studies have also                        of existing faults to enable controlled testing studies for java programs.
                                                                                        In Proceedings of the 2014 International Symposium on Software Testing
addressed syntax errors, performance bugs, vulnerabilities,                             and Analysis, ISSTA 2014, page 437–440, New York, NY, USA, 2014.
type errors, and build failures [53], [54].                                             Association for Computing Machinery.
Learning-based Approaches. With the development of ma-                              [4] JetBrains. Intellij idea: The leading ide for professional java and kotlin
                                                                                        development. https://www.jetbrains.com/idea/. Accessed: 2026-03-21.
chine learning, repair methods increasingly rely on data-driven                     [5] Microsoft. Visual studio code: The open source ai code editor. https:
models. Early learning-based methods use machine learning                               //code.visualstudio.com/. Accessed: 2026-03-21.
to rank or prioritize candidate patches [55]. More recent                           [6] John D. Gould. Some psychological evidence on how people debug
                                                                                        computer programs. International Journal of Man-Machine Studies,
approaches adopt neural machine translation models to directly                          7(2):151–182, 1975.
transform buggy code into fixed code [56], [57], or design                          [7] Amy J. Ko and Brad A. Myers. Designing the whyline: a debugging
neural architectures that predict tree-level or syntax-aware                            interface for asking questions about program behavior. In Proceedings
                                                                                        of the SIGCHI Conference on Human Factors in Computing Systems,
code transformations [58], [59]. Some methods further train                             CHI ’04, page 151–158, New York, NY, USA, 2004. Association for
repair-specific models on curated bug-fix datasets [19], [60].                          Computing Machinery.
Unlike these task-specific learning approaches, recent LLM-                         [8] Jonathan Sillito, Gail C. Murphy, and Kris De Volder. Asking and
                                                                                        answering questions during a programming change task. IEEE Trans.
based APR methods use general-purpose foundation models                                 Softw. Eng., 34(4):434–451, July 2008.
without explicit repair-specific training.                                          [9] Lucas Layman, Madeline Diep, Meiyappan Nagappan, Janice Singer,
LLM-based Approaches. With the emergence of large lan-                                  Robert Deline, and Gina Venolia. Debugging revisited: Toward un-
                                                                                        derstanding the debugging needs of contemporary software developers.
guage models, APR has increasingly shifted toward prompt-                               In 2013 ACM / IEEE International Symposium on Empirical Software
based and agentic repair paradigms. Early LLM-based ap-                                 Engineering and Measurement, pages 383–392, 2013.
proaches mainly rely on prompt engineering to perform one-                         [10] Zack Coker, David Gray Widder, Claire Le Goues, Christopher Bogart,
shot repair, where the model directly generates a candidate                             and Joshua Sunshine. A qualitative study on framework debugging.
                                                                                        In 2019 IEEE International Conference on Software Maintenance and
patch from buggy code and related inputs in a single interac-                           Evolution (ICSME), pages 568–579, 2019.
tion [24], [45], [61]. Later methods introduce iterative repair                    [11] Yiling Lou, Jun Yang, Samuel Benton, Dan Hao, Lin Tan, Zhenpeng
by repeatedly querying the LLM with validation feedback and                             Chen, Lu Zhang, and Lingming Zhang. When automated program repair
                                                                                        meets regression testing—an extensive study on two million patches.
refining patches across multiple rounds [12], [25], [27]. More                          ACM Trans. Softw. Eng. Methodol., 33(7), September 2024.
recent agent-based approaches further extend this paradigm by                      [12] Kyla H. Levin, Nicolas van Kempen, Emery D. Berger, and Stephen N.
allowing the LLM to invoke external tools during repair [26],                           Freund. Chatdbg: Augmenting debugging with large language models.
                                                                                        Proc. ACM Softw. Eng., 2(FSE), June 2025.
[28]. Our work is most closely related to this line of research,                   [13] Abdulaziz Alaboudi and Thomas D. Latoza.                 Hypothesizer: A
but differs in that it is inspired by practical debugging behav-                        hypothesis-based debugger to find and test debugging hypotheses. In
iors and structures repair around static-dynamic information                            Proceedings of the 36th Annual ACM Symposium on User Interface
                                                                                        Software and Technology, UIST ’23, New York, NY, USA, 2023.
integration, question-driven failure diagnosis, and feedback-                           Association for Computing Machinery.
guided patch refinement.                                                           [14] Devon H. O’Dell.          The debugging mind-set.        Commun. ACM,
                                                                                        60(6):40–45, May 2017.
                                                                                   [15] Hadeel Eladawy, Claire Le Goues, and Yuriy Brun. Automated program
                          VIII. C ONCLUSION                                             repair, what is it good for? not absolutely nothing! In Proceedings of
                                                                                        the IEEE/ACM 46th International Conference on Software Engineering,
   In this work, we present P RAC R EPAIR, a fully automated                            ICSE ’24, New York, NY, USA, 2024. Association for Computing
                                                                                        Machinery.
program repair framework inspired by real-world debugging
                                                                                   [16] Herb Krasner. The cost of poor software quality in the us: A 2020
practices. Specifically, P RAC R EPAIR constructs static and dy-                        report. Proc. Consortium Inf. Softw. QualityTM (CISQTM), 2(3), 2021.
namic context, performs question-driven failure diagnosis to                       [17] Claire Le Goues, Michael Pradel, and Abhik Roychoudhury. Automated
formulate explicit repair hypotheses, and iteratively refines                           program repair. Commun. ACM, 62(12):56–65, November 2019.
                                                                                   [18] Kui Liu, Anil Koyuncu, Dongsun Kim, and Tegawendé F. Bissyandé.
candidate patches using validation feedback. Extensive ex-                              Tbar: revisiting template-based automated program repair. In Proceed-
periments, including comparisons with state-of-the-art base-                            ings of the 28th ACM SIGSOFT International Symposium on Software
lines, scenario-based analysis, and ablation studies, show                              Testing and Analysis, ISSTA 2019, page 31–42, New York, NY, USA,
                                                                                        2019. Association for Computing Machinery.
that P RAC R EPAIR consistently outperforms existing methods.                      [19] He Ye, Matias Martinez, Xiapu Luo, Tao Zhang, and Martin Monperrus.
These results suggest that developer-inspired debugging work-                           Selfapr: Self-supervised program repair with test execution diagnostics.
flows can substantially improve APR effectiveness. In future                            In Proceedings of the 37th IEEE/ACM International Conference on
                                                                                        Automated Software Engineering, ASE ’22, New York, NY, USA, 2023.
work, we plan to extend P RAC R EPAIR to more languages for                             Association for Computing Machinery.
stronger generalizability.                                                         [20] Qihao Zhu, Zeyu Sun, Wenjie Zhang, Yingfei Xiong, and Lu Zhang.
                                                                                        Tare: Type-Aware Neural Program Repair . In 2023 IEEE/ACM 45th
                                                                                        International Conference on Software Engineering (ICSE), pages 1443–
                              R EFERENCES                                               1455, Los Alamitos, CA, USA, May 2023. IEEE Computer Society.
                                                                                   [21] Nan Jiang, Thibaud Lutellier, and Lin Tan. Cure: Code-aware neural
 [1] Sicong Cao, Xiaobing Sun, Xiaoxue Wu, David Lo, Lili Bo, Bin Li,                   machine translation for automatic program repair. In 2021 IEEE/ACM
     Xiaolei Liu, Xingwei Lin, and Wei Liu. Snopy: Bridging sample                      43rd International Conference on Software Engineering (ICSE), pages
     denoising with causal graph learning for effective vulnerability detection.        1161–1173, 2021.
     In Proceedings of the 39th IEEE/ACM International Conference on               [22] Nan Jiang, Thibaud Lutellier, Yiling Lou, Lin Tan, Dan Goldwasser,
     Automated Software Engineering, ASE ’24, page 606–618, New York,                   and Xiangyu Zhang. Knod: Domain knowledge distilled tree decoder
     NY, USA, 2024. Association for Computing Machinery.                                for automated program repair. In 2023 IEEE/ACM 45th International
 [2] Zimin Chen, Steve Kommrusch, and Martin Monperrus. Neural transfer                 Conference on Software Engineering (ICSE), pages 1251–1263, 2023.
     learning for repairing security vulnerabilities in c code. IEEE Transac-      [23] He Ye and Martin Monperrus. Iter: Iterative neural repair for multi-
     tions on Software Engineering, 49(1):147–165, 2023.                                location patches. In Proceedings of the IEEE/ACM 46th International
IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 14, NO. 8, AUGUST 2021                                                                                     12



     Conference on Software Engineering, ICSE ’24, New York, NY, USA,          [47] Dongsun Kim, Jaechang Nam, Jaewoo Song, and Sunghun Kim. Au-
     2024. Association for Computing Machinery.                                     tomatic patch generation learned from human-written patches. In Pro-
[24] Chunqiu Steven Xia and Lingming Zhang. Less training, more repairing           ceedings of the 2013 International Conference on Software Engineering,
     please: revisiting automated program repair via zero-shot learning. In         ICSE ’13, page 802–811. IEEE Press, 2013.
     Proceedings of the 30th ACM Joint European Software Engineering           [48] Rohan Bavishi, Hiroaki Yoshida, and Mukul R. Prasad. Phoenix:
     Conference and Symposium on the Foundations of Software Engineering,           automated data-driven synthesis of repairs for static analysis violations.
     ESEC/FSE 2022, page 959–971, New York, NY, USA, 2022. Associa-                 In Proceedings of the 2019 27th ACM Joint Meeting on European
     tion for Computing Machinery.                                                  Software Engineering Conference and Symposium on the Foundations
[25] Chunqiu Steven Xia and Lingming Zhang. Automated program repair                of Software Engineering, ESEC/FSE 2019, page 613–624, New York,
     via conversation: Fixing 162 out of 337 bugs for $0.42 each using chat-        NY, USA, 2019. Association for Computing Machinery.
     gpt. In Proceedings of the 33rd ACM SIGSOFT International Symposium       [49] Hoang Duong Thien Nguyen, Dawei Qi, Abhik Roychoudhury, and
     on Software Testing and Analysis, ISSTA 2024, page 819–831, New                Satish Chandra. Semfix: program repair via semantic analysis. In Pro-
     York, NY, USA, 2024. Association for Computing Machinery.                      ceedings of the 2013 International Conference on Software Engineering,
[26] Islem Bouzenia, Premkumar Devanbu, and Michael Pradel. Repairagent:            ICSE ’13, page 772–781. IEEE Press, 2013.
     An autonomous, llm-based agent for program repair. In Proceedings of      [50] Xusheng Xiao, Sihan Li, Tao Xie, and Nikolai Tillmann. Characteristic
     the IEEE/ACM 47th International Conference on Software Engineering,            studies of loop problems for structural test generation via symbolic exe-
     ICSE ’25, page 2188–2200. IEEE Press, 2025.                                    cution. In Proceedings of the 28th IEEE/ACM International Conference
[27] Xin Yin, Chao Ni, Shaohua Wang, Zhenhao Li, Limin Zeng, and                    on Automated Software Engineering, ASE ’13, page 246–256. IEEE
     Xiaohu Yang. Thinkrepair: Self-directed automated program repair.              Press, 2013.
     In Proceedings of the 33rd ACM SIGSOFT International Symposium            [51] Yu Liu, Sergey Mechtaev, Pavle Subotić, and Abhik Roychoudhury.
     on Software Testing and Analysis, ISSTA 2024, page 1274–1286, New              Program repair guided by datalog-defined static analysis. In Proceedings
     York, NY, USA, 2024. Association for Computing Machinery.                      of the 31st ACM Joint European Software Engineering Conference and
[28] Jiayi Zhang, Kai Huang, Jian Zhang, Yang Liu, and Chunyang Chen.               Symposium on the Foundations of Software Engineering, ESEC/FSE
     Repair ingredients are all you need: Improving large language model-           2023, page 1216–1228, New York, NY, USA, 2023. Association for
     based program repair via repair ingredients search, 2025.                      Computing Machinery.
                                                                               [52] Alexandru Marginean, Johannes Bader, Satish Chandra, Mark Harman,
[29] Kai Huang, Zhengzi Xu, Su Yang, Hongyu Sun, Xuejun Li, Zheng Yan,
                                                                                    Yue Jia, Ke Mao, Alexander Mols, and Andrew Scott. Sapfix: Automated
     and Yuqing Zhang. Evolving paradigms in automated program repair:
                                                                                    end-to-end repair at scale. In 2019 IEEE/ACM 41st International
     Taxonomy, challenges, and opportunities. ACM Comput. Surv., 57(2),
                                                                                    Conference on Software Engineering: Software Engineering in Practice
     October 2024.
                                                                                    (ICSE-SEIP), pages 269–278, 2019.
[30] Sophia D Kolak, Ruben Martins, Claire Le Goues, and Vincent Josua         [53] Rahul Gupta, Aditya Kanade, and Shirish Shevade. Deep reinforcement
     Hellendoorn. Patch generation with language models: Feasibility and            learning for syntactic error repair in student programs. In Proceedings
     scaling behavior. In Deep Learning for Code Workshop, 2022.                    of the Thirty-Third AAAI Conference on Artificial Intelligence and
[31] Julian Aron Prenner, Hlib Babii, and Romain Robbes. Can openai’s               Thirty-First Innovative Applications of Artificial Intelligence Conference
     codex fix bugs?: An evaluation on quixbugs. In 2022 IEEE/ACM                   and Ninth AAAI Symposium on Educational Advances in Artificial
     International Workshop on Automated Program Repair (APR), pages                Intelligence, AAAI’19/IAAI’19/EAAI’19. AAAI Press, 2019.
     69–75, 2022.                                                              [54] Daniel Tarlow, Subhodeep Moitra, Andrew Rice, Zimin Chen, Pierre-
[32] joernio. Joern: The bug hunter’s workbench. https://github.com/joernio/        Antoine Manzagol, Charles Sutton, and Edward Aftandilian. Learning
     joern, 2024. Accessed: 2026-03-06.                                             to fix build errors with graph2diff neural networks. In Proceedings of
[33] Fabian Yamaguchi, Nico Golde, Daniel Arp, and Konrad Rieck. Model-             the IEEE/ACM 42nd International Conference on Software Engineer-
     ing and discovering vulnerabilities with code property graphs. In 2014         ing Workshops, ICSEW’20, page 19–20, New York, NY, USA, 2020.
     IEEE Symposium on Security and Privacy, pages 590–604, 2014.                   Association for Computing Machinery.
[34] Raffi Khatchadourian, Yiming Tang, Mehdi Bagherzadeh, and Syed            [55] Fan Long and Martin Rinard. Automatic patch generation by learning
     Ahmed. Safe automated refactoring for intelligent parallelization of           correct code. In Proceedings of the 43rd Annual ACM SIGPLAN-
     java 8 streams. In 2019 IEEE/ACM 41st International Conference on              SIGACT Symposium on Principles of Programming Languages, POPL
     Software Engineering (ICSE), pages 619–630, 2019.                              ’16, page 298–312, New York, NY, USA, 2016. Association for Com-
[35] Oracle. Package java.lang.instrument. Java Platform, Standard Edition          puting Machinery.
     API Specification. Accessed: 2026-03-06.                                  [56] Rahul Gupta, Soham Pal, Aditya Kanade, and Shirish Shevade. Deepfix:
[36] Romain Lenglet. Asm: a code manipulation tool to implement adaptable           fixing common c language errors by deep learning. In Proceedings of
     systems. Adaptable and extensible. . . , 2002.                                 the Thirty-First AAAI Conference on Artificial Intelligence, AAAI’17,
[37] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik              page 1345–1351. AAAI Press, 2017.
     Narasimhan, and Yuan Cao. ReAct: Synergizing reasoning and acting         [57] Michele Tufano, Jevgenija Pantiuchina, Cody Watson, Gabriele Bavota,
     in language models. In International Conference on Learning Repre-             and Denys Poshyvanyk. On learning meaningful code changes via neural
     sentations (ICLR), 2023.                                                       machine translation. In Proceedings of the 41st International Conference
[38] Anonymous Authors. Artifact: Source code, prompts, datasets, and               on Software Engineering, ICSE ’19, page 25–36. IEEE Press, 2019.
     experimental results for this paper. https://doi.org/10.5281/zenodo.      [58] Qihao Zhu, Zeyu Sun, Yuan-an Xiao, Wenjie Zhang, Kang Yuan, Yingfei
     19336422, 2026. Anonymous research artifact.                                   Xiong, and Lu Zhang. A syntax-guided edit decoder for neural program
[39] OpenAI. gpt-3.5-turbo-0125. https://developers.openai.com/api/docs/            repair. In Proceedings of the 29th ACM Joint Meeting on European
     models#gpt-3-5-turbo, September 2023. Accessed: 2025-09-29.                    Software Engineering Conference and Symposium on the Foundations
                                                                                    of Software Engineering, ESEC/FSE 2021, page 341–353, New York,
[40] OpenAI. Gpt-4o-2024-05-13: Openai’s next-generation language model.
                                                                                    NY, USA, 2021. Association for Computing Machinery.
     https://developers.openai.com/api/docs/models#gpt-4-turbo-and-gpt-4,
                                                                               [59] Yi Li, Shaohua Wang, and Tien N. Nguyen. Dlfix: context-based code
     September 2023. Accessed: 2025-09-29.
                                                                                    transformation learning for automated program repair. In Proceedings of
[41] Fabrizio Gilardi, Meysam Alizadeh, and Maël Kubli. Chatgpt out-               the ACM/IEEE 42nd International Conference on Software Engineering,
     performs crowd workers for text-annotation tasks. Proceedings of the           ICSE ’20, page 602–614, New York, NY, USA, 2020. Association for
     National Academy of Sciences, 120(30):e2305016120, 2023.                       Computing Machinery.
[42] OpenAI. GPT-4. https://developers.openai.com/api/docs/models/gpt-4,       [60] He Ye, Matias Martinez, and Martin Monperrus. Neural program
     2023. OpenAI API documentation.                                                repair with execution-based backpropagation. In Proceedings of the
[43] Ollama. Meta Llama 3: The Most Capable Openly Available LLM to                 44th International Conference on Software Engineering, ICSE ’22, page
     Date. https://ollama.com/library/llama3, 2024.                                 1506–1518, New York, NY, USA, 2022. Association for Computing
[44] DeepSeek AI. DeepSeek Coder: Let the Code Write Itself. https://               Machinery.
     github.com/deepseek-ai/DeepSeek-Coder, 2023. GitHub repository.           [61] Nan Jiang, Kevin Liu, Thibaud Lutellier, and Lin Tan. Impact of code
[45] Chunqiu Steven Xia, Yuxiang Wei, and Lingming Zhang. Automated                 language models on automated program repair. In Proceedings of the
     program repair in the era of large pre-trained language models, 2023.          45th International Conference on Software Engineering, ICSE ’23, page
[46] Claire Le Goues, ThanhVu Nguyen, Stephanie Forrest, and Westley                1430–1442. IEEE Press, 2023.
     Weimer. Genprog: A generic method for automatic software repair.
     IEEE Transactions on Software Engineering, 38(1):54–72, 2012.

