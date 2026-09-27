# Towards Practical and Useful Automated Program Repair for Debugging
Source: https://arxiv.org/abs/2407.08958v1
Kind: pdf
Fetched: 2026-09-23T21:18:13.561503+00:00
Tool: pdftotext
Research-Target: /Users/sergii/.ai/knowledge/research_topics/coding_agents/research/ai_coding_best_practices
Topic: coding_agents

                                                    Towards Practical and Useful Automated Program Repair
                                                                        for Debugging
                                                                                    Qi Xin                                                                       Haojun Wu
                                                                  qxin@whu.edu.cn                                                                       haojunwu@whu.edu.cn
                                                     School of Computer Science, Wuhan University                                            School of Computer Science, Wuhan University
                                                                Hubei Luojia Laboratory                                                                         China
                                                                        China

                                                                             Steven P. Reiss                                                                     Jifeng Xuan∗
                                                                spr@cs.brown.edu                                                                          jxuan@whu.edu.cn
                                                 Department of Computer Science, Brown University                                            School of Computer Science, Wuhan University




arXiv:2407.08958v1 [cs.SE] 12 Jul 2024
                                                                      USA                                                                                       China
                                         ABSTRACT                                                                                        1   MOTIVATION
                                         Current automated program repair (APR) techniques are far from                                  Programs are rarely bug-free. Debugging is an indispensable ac-
                                         being practical and useful enough to be considered for realistic                                tivity in software development. It is however very costly, and can
                                         debugging. They rely on unrealistic assumptions including the re-                               consume up to 50% of the programming time [6]. To reduce the cost
                                         quirement of a comprehensive suite of test cases as the correctness                             of debugging and make it easier, researchers have proposed the con-
                                         criterion and frequent program re-execution for patch validation;                               cept of automated program repair (APR) [9, 11, 28, 52] whose goal is
                                         they are not fast; and their ability of repairing the commonly aris-                            to automatically generate a patch that corrects a buggy program’s
                                         ing complex bugs by fixing multiple locations of the program is                                 misbehavior. For over a decade, more than 60 APR techniques have
                                         very limited. We hope to substantially improve APR’s practicality,                              been developed [29, 36]. They have sought to achieve automated
                                         effectiveness, and usefulness to help people debug. Towards this                                repair via various strategies generally classified as pattern-based
                                         goal, we envision PracAPR, an interactive repair system that works                              (e.g., [17, 24, 40]), constraint-based (e.g., [26, 48]), search-based
                                         in an Integrated Development Environment (IDE) to provide effec-                                (e.g., [12, 43]), and learning-based [52].
                                         tive repair suggestions for debugging. PracAPR does not require a                                  Despite the promising potential, current APR techniques are
                                         test suite or program re-execution. It assumes that the developer                               far from being practical and useful enough to be integrated into
                                         uses an IDE debugger and the program has suspended at a location                                an IDE for debugging. Three key challenges remain. First, current
                                         where a problem is observed. It interacts with the developer to ob-                             approaches are designed based on unrealistic assumptions. They as-
                                         tain a problem specification. Based on the specification, it performs                           sume the existence of a test suite serving as the correctness criterion
                                         test-free, flow-analysis-based fault localization, patch generation                             and require frequent program re-execution for repair validation.
                                         that combines large language model-based local repair and tailored                                 In a realistic debugging scenario, one cannot assume the exis-
                                         strategy-driven global repair, and program re-execution-free patch                              tence of a (high-quality) test suite, especially in the initial develop-
                                         validation based on simulated trace comparison to suggest repairs.                              ment phase of the software. Studies have shown that developers
                                         By having PracAPR, we hope to take a significant step towards                                   do not write test suites containing a sufficient number of test cases
                                         making APR useful and an everyday part of debugging.                                            or even do not write tests at all [4, 19]. As also noted by Koyuncu
                                                                                                                                         et al. [20], bugs are often reported without an available test suite
                                         ACM Reference Format:                                                                           revealing them. Surprisingly, the bug-revealing test cases for over
                                         Qi Xin, Haojun Wu, Steven P. Reiss, and Jifeng Xuan. 2024. Towards Practical                    90% of the bugs in the Defects4J dataset [15] were introduced after
                                         and Useful Automated Program Repair for Debugging. In Proceedings of
                                                                                                                                         the bug was identified.
                                         International Workshop on Software Engineering in 2030 (SE 2030). ACM, New
                                         York, NY, USA, 6 pages. https://doi.org/10.1145/nnnnnnn.nnnnnnn
                                                                                                                                            While some techniques [2, 3, 8, 20, 41] have sought for test-free
                                                                                                                                         repair, they are restricted to handling specific types of bugs (e.g.,
                                                                                                                                         the heap-property faults [41]) and potential issues flagged by static
                                         ∗ Corresponding author                                                                          analyzers and are not designed to repair general semantic bugs that
                                                                                                                                         arise while debugging.
                                                                                                                                            The reliance on frequent program re-execution also makes APR
                                         Permission to make digital or hard copies of all or part of this work for personal or           not practical. In a realistic debugging scenario, recreating the envi-
                                         classroom use is granted without fee provided that copies are not made or distributed           ronment for the immediate failure caused by the bug can be difficult
                                         for profit or commercial advantage and that copies bear this notice and the full citation
                                         on the first page. Copyrights for components of this work owned by others than the              since the failure can be identified in a long run or in an interactive
                                         author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or          session. Moreover, frequent program re-execution makes APR not
                                         republish, to post on servers or to redistribute to lists, requires prior specific permission   fast. Current approaches can take minutes (e.g., [14]) or even hours
                                         and/or a fee. Request permissions from permissions@acm.org.
                                         SE 2030, November 2024, Puerto Galinàs (Brazil)                                                 to repair one bug [25]. Studies showed that developers prefer not
                                         © 2024 Copyright held by the owner/author(s). Publication rights licensed to ACM.               to wait for too long [30] for repair. One can also imagine that APR,
                                         ACM ISBN 978-x-xxxx-xxxx-x/YY/MM
                                         https://doi.org/10.1145/nnnnnnn.nnnnnnn
SE 2030, November 2024, Puerto Galinàs (Brazil)                                                    Qi Xin, Haojun Wu, Steven P. Reiss, and Jifeng Xuan


if integrated into an IDE to provide repair suggestions, is highly       debugger, and the current runtime stack to compute a backward
expected to be quick.                                                    slice containing potential repair locations. Patch generation is done
    Second, while APR has made remarkable progress towards local         with local and global repair, which we will discuss later. Patch val-
repair by generating patches addressing a single location of the         idation does not require program re-execution. Instead, PracAPR
program, the repair ability is still weak. Our statistics based on the   generates via a live programming mechanism simulated traces that
previous evaluation of existing tools shows that traditional non-        reflect the real executions of the original and repaired programs and
learning-based approaches can only repair a small fraction (less         compares the traces to infer patch correctness. Finally, PracAPR
than 23%) of the 150 single-hunk bugs in the Defects4J v1.2 dataset.     presents the repair suggestions to the developer. The developer can
For these bugs, the developer patches change only a single hunk          choose to preview any of the repairs and further accept it to allow
of code. Learning-based approaches, especially those using a large       changes to be applied to the program.
language model (LLM) [10, 13, 16, 39, 45, 47], represent a significant      For local repair, PracAPR uses an LLM-based approach, aiming
improvement. However, a state-of-the-art approach Repilot [42] still     to improve APR’s repair ability in fixing more local bugs (that
failed to repair 86 (or 57.3%) of the single-location bugs. Moreover,    require changes of a single location of the program) and fixing
existing techniques can generate spurious overfitting patches [21,       them more precisely (by generating fewer bad patches). To this
32, 38, 49], which are harmful and can adversely affect debugging [7,    end, PracAPR uses an informative prompt that includes the buggy
30]. In summary, APR’s weak ability of local repair can lower the        location, its context, the failure input and output, dynamic execution
developer’s trust of APR in dealing with even simple bugs and make       information (including for example the coverage and key program
the developer unwilling to use APR for debugging.                        states), promising patterns and fix ingredients, and user guidance
    Finally, current APR cannot do effective global repair to tackle     to help LLM accurately diagnose the problem and propose effective
complex multi-location bugs whose fix requires changes for multi-        patches. PracAPR also allows conversational repair and refinement
ple locations of the program. Zhong and Su [53] found that multi-        and re-fixing of the patches to improve the repair quality.
location bugs are common. At least 40% of real-bug fixes made by            For global repair, PracAPR uses a variety of strategies distilled
developers are used to tackle such bugs. This finding implies that if    from our analysis of multi-location patches that led to a charac-
APR is not designed to support multi-location repair, it can have        terization of 8 types of partial patch relationships. The strategies
very limited usefulness. To enhance the usability of APR, previous       include performing iterative repair to generate patches location by
techniques have attempted to address multi-location bugs using           location to address bugs that require fixing different issues, per-
strategies such as genetic algorithms [22, 51], detection and update     forming simultaneous repair to address related issues, using local
of evolutionary siblings [37], variational execution [44], deep learn-   repair to tackle single-location-alike bugs, and using pattern-based
ing [23], and iterative self-supervised training [50]. A key problem     methods to generate other common patches that involve for exam-
of these approaches is that most of the repaired multi-location bugs     ple adding a definition and use of a variable and inserting if-wrap
are actually multi-fault bugs exposed by multiple failures. A multi-     code (i.e., an if-statement wrapping a code hunk).
fault bug can be decomposed into multiple single-fault bugs and is
rare in realistic debugging, as developers typically deal with one       3     ONGOING AND FUTURE WORK
failure (fault) at a time [18, 31]. To understand how existing ap-
                                                                         We next discuss our ongoing and future work for realizing PracAPR.
proaches deal with single-fault multi-location bugs that commonly
arise while debugging, we did a study and found that (1) about
half (49.5%) of the multi-location bugs in the Defects4J v1.2 dataset    3.1    Interactive Test-Free Repair Framework
are multi-fault, (2) the dataset has 118 single-fault multi-location     We have developed an interactive test-free repair framework ROSE [33],
bugs, and (3) current techniques [23, 37, 44, 46, 50, 51, 55] repaired   which provides initial solutions for fault localization and patch val-
at most 8 of them. This result shows that current APR’s ability of       idation without requiring a test suite and program re-execution.
repairing complex multi-location bugs is poor.                              ROSE works in the Eclipse-based Code Bubbles IDE [5] and
                                                                         allows easy integration of existing APR patch generators. ROSE
                                                                         assumes that the program is suspended at a location where unex-
2    AN ENVISIONED REPAIR SYSTEM FOR 2030                                pected behavior is observed. It interacts with the developer to obtain
We envision a repair system PracAPR that addresses the aforemen-         a problem description. The developer can specify that an exception
tioned challenges and provides quick repair suggestions for realistic    is unexpected, a line should not be executed, or a variable should
debugging. Figure 1 shows an overview of PracAPR. To overcome            not hold a certain value. Based on the specification, ROSE performs
the unrealistic-assumption drawback, PracAPR does not assume the         test-free fault localization using an abstract-interpretation-based
existence of a test suite and does not require program re-execution.     flow analysis to statically compute a partial backward slice contain-
It works in conjunction with an IDE debugger and assumes that            ing potential repair locations. It invokes the patch generators that
the program is stopped at a location where a problem is observed.        have been plugged into the framework to make patches for those
PracAPR interacts with the developer to obtain a description of          locations. For patch validation without using test cases or allowing
the problem and performs test-free fault localization, patch genera-     dynamic program re-execution, ROSE generates simulated traces
tion, and patch validation based on the description (the problem         based on a live-programming system SEEDE [35] for both the orig-
specification) to generate repair suggestions. Without a test suite,     inal and repaired executions and then compares the traces with
PracAPR performs flow-analysis-based fault localization while tak-       respect to the problem to infer patch correctness. Finally, ROSE
ing into account the problem symptom, current values from the            presents a limited number of prioritized patches. The developer can
Towards Practical and Useful Automated Program Repair
for Debugging                                                                                                                      SE 2030, November 2024, Puerto Galinàs (Brazil)




                                     Buggy
                                                                                    2. Test-Free
                                    Program          1. Problem                                                            3. Patch
                                                                                        Fault
                                                    Specification     Problem                             Repair          Generation
                                                                                    Localization
                                                                    Specification                        Locations
                                   Developer




                                                                                     4. Program
                                                                                                                     • LLM-Based Local Repair
                                                      5. Patch                      Re-execution-
                                                                                                                     • Tailored Strategy-Driven
                                                    Presentation                     Free Patch
                                                                                                                       Global Repair
                                                                                     Validation
                                     Patches                         Validated                         Patches
                                   for Preview                        Patches



                                                           Integrated Development Environment (IDE)

                                                 Figure 1: An overview of the PracAPR repair system.


choose a patch for a preview, which highlights the code before and                       1 public     TimeSeries createCopy(int start, int end)
                                                                                         2
after the repair with differences, and ask ROSE to make the repair.                      3     if
                                                                                                           throws CloneNotSupportedException {
                                                                                                      (start < 0) {
More details can be found in [33, 34].                                                   4             throw new IllegalArgumentException("Requires start >= 0.")
                                                                                                     ;
   We evaluated the effectiveness and utility of ROSE with a repair                      5         }
experiment and a user study. Our results showed that ROSE’s test-                        6         if (end < start) {
                                                                                         7             throw new IllegalArgumentException("Requires start <= end.
free fault localization and patch validation are highly effective:                                   ");
the fault localization included the correct repair location for 89%                      8
                                                                                         9
                                                                                                   }
                                                                                                   TimeSeries copy = (TimeSeries) super.clone();
of the bugs tested and the patch validation gave a top-5 rank for                       10          + copy.minY = Double.NaN;
all correct repairs; that a ROSE-based tool can repair as many as                       11          + copy.maxY = Double.NaN;
36/40 QuixBugs and 37/60 Defects4J bugs in only seconds; and that                       12         copy.data = new java.util.ArrayList();
                                                                                        13         if (this.data.size() > 0) {
ROSE helped 44% more participants succeed in a debugging task                           14             for (int index = start; index <= end; index++) {
and helped reduce the debugging time by about 16.5%. Overall, we                        15                 TimeSeriesDataItem item
                                                                                        16                          = (TimeSeriesDataItem) this.data.get(index);
believe that ROSE is a promising repair framework that can make                         17                 TimeSeriesDataItem clone = (TimeSeriesDataItem) item.
debugging easier.                                                                       18
                                                                                                     clone();
                                                                                                           try {
   We plan to build PracAPR on top of ROSE, and we see two                              19                      copy.add(clone);
                                                                                        20
ways for improvement. First, we want to improve ROSE’s user                             21
                                                                                                           }
                                                                                                           catch (SeriesException e) {
interaction for problem specification by exploring not only a better                    22                      e.printStackTrace();
                                                                                        23                 }
presentation of the failure information to facilitate understanding                     24             }
of the program semantics and the failure but also more forms of the                     25         }
                                                                                        26         return copy;
specification (based on for example constraints and even natural                        27 }
language) to effectively guide fault localization and patch validation.
Second, we want to investigate learning-based trace comparison
while considering more information about the execution to enhance                                            Figure 2: Patch for the Chart_3 bug.
patch validation.

                                                                                             are the most common mistakes that ChatGPT makes? and (3) How
3.2     LLM-Based Local Repair                                                               to improve ChatGPT to repair more bugs?
The LLM has demonstrated superior abilities in repairing software                               Our current result shows that existing approaches are weak in
bugs [45, 47]. We believe that an LLM-based approach is promising                            that they use prompts that include only the buggy location, its lim-
in generating high-quality local patches (addressing single locations                        ited context, and shallow information about the failure (including
of the program for repair). Since ChatGPT is widely recognized                               the input and the failing assertion). This is often insufficient for
as a prominent LLM for tackling various software engineering                                 ChatGPT to understand the program semantics and the problem
tasks, we consider a ChatGPT-based approach that serves as a key                             and can result in incorrect patches raising new problems.
component of PracAPR to accurately infer the problem and provide                                Figure 2 shows for example the buggy method for the Defects4J
a low number of promising patches for effective local repair.                                Chart_3 bug and the patch (lines 10 and 11). To repair the bug,
   We are conducting a study to understand the failure of ChatGPT-                           a state-of-the-art ChatGPT-based approach ChatRepair [47] uses
based approaches [45, 47] and motivate possible ways for improve-                            a prompt that includes the code of the buggy method, the name
ment. We seek to answer three research questions: (1) What are the                           of the failing test case testCreateCopy3, the failing assertion
characteristics of the bugs that ChatGPT fails to repair? (2) What                           assertEquals(101.0, s2.getMaxY(), EPSILON), and
SE 2030, November 2024, Puerto Galinàs (Brazil)                                                    Qi Xin, Haojun Wu, Steven P. Reiss, and Jifeng Xuan


the failure message expected:<101.0> but was:<102.0>.                      We aim to design a global repair approach that can effectively
It does not however inform ChatGPT of the test input triggering         address single-fault multi-location bugs. Towards this goal, we went
the failure. Nor does it describe the behavior of the invoked method    about analyzing the developer (ground-truth) patches for a sample
add (line 19) showing how minY and maxY are updated (key in-            of the single-fault multi-location bugs (about one third, or 75 in
formation for bug understanding) and provide the details about          total). We wanted to understand why the repair needs to addresses
the failure execution. Due to insufficient knowledge of the failure,    multiple locations, what are the characteristics of the partial patches
ChatGPT’s problem diagnosis is shallow and inaccurate – it thought      made at different locations, and furthermore what strategies to
that there is a problem with the loop copying the data and did not      consider for patch generation based on the characteristics.
seem to understand that it was the update of the minY and maxY             The analysis has led to a characterization of 8 partial patch
values that causes the error. As a result, ChatGPT proposed a patch     relationships summarized below.
changing the loop condition (line 14), which is incorrect.                   • DU: Partial patches with this relationship add the definition
   To help ChatGPT understand the failure, we plan to use an                    of variables, fields, packages, or methods and later use what
augmented prompt that includes not only what ChatRepair uses in                 has been defined for repair.
its prompt but also the code of the failing test case (including the         • OA: Partial patches with this relationship can be done in
test input), the definition of related methods (including add), and             one repair action or operation by for example adding an
the execution trace showing not only what lines are exercised in the            if-statement wrapping a code hunk.
failure run and their order but also the key program state (variable         • RIF: This relationship indicates that the partial patches are
and field values). Using a prompt like this, ChatGPT successfully               used to address related issues that arise in different locations.
understands that the failure is related to “how the min and max y            • DIF: This relationship indicates that the partial patches ad-
values are updated after copying a subset”. This finally leads to a             dress different issues arising from different program parts
patch that correctly updates the min and max y values.                          that may implement the same functionality.
   An augmented prompt, even with more failure and execution                 • EOH: Partial patches with this relationship can be consid-
information, may not necessarily help ChatGPT figure out what is                ered as a single-hunk patch for reasons such as that there is
wrong. And even if ChatGPT precisely understands the problem, it                only one partial patch that is semantically needed and the
may still fail to generate the correct patch tackling the problem in            others are created only to improve readability.
the right way. For example, ChatGPT may know that there is an                • SU: In this relationship, some partial patches are created to
invalid case where the start index is greater than end but can                  do the setup work by updating a variable, field, or method
be unsure about how to process it – whether the program should                  while the others use what has been updated for repair.
throw an exception, return a special value, or do something else.            • ONPF: In this relationship, some partial patches can fix the
One way to mitigate this problem is to solicit user feedback showing            original problem and resolve the original failure. Unfortu-
for example an exception is expected, a certain line should not be              nately, they also raise new problems triggering new failures,
executed, or a variable should not hold a value.                                which can be tackled by other partial patches.
   In addition to using augmented prompts, we will also explore              • FU: Some partial patches serve as the primary changes
combining ChatGPT with traditional pattern-based and search-                    for correcting the misbehavior of the program. Others are
based methods (finding for example effective patterns and fix in-               needed to undo the negative influence brought by the previ-
gredients) to guide the repair, performing conversational repair                ous changes.
highlighting the (negative) influence of the previous patches to           As the next step, we plan to design specialized repair strategies
allow ChatGPT to reflect on its mistakes for improvement, and           based on the relationships and develop a global repair approach
conducting post-processing operations refining and re-fixing the        that uses these strategies to obtain guided exploration for effective
patches to improve repair quality.                                      multi-location repair. An approach that we envision to have uses
                                                                        the LLM-based method discussed in Section 3.2 to generate single-
                                                                        location patches. It performs iterative repair via repeated single-
3.3     Global Repair Driven by Tailored Strategies                     location-based fault localization and patch generation to generate
Existing global repair techniques have adopted various strategies for   patches of the DIF, ONPF, and FU relationships. Unlike existing
multi-location repair. The evaluation of these techniques is however    approaches [50, 51], our approach considers a variety of program
based on the Defects4J bug dataset [15] and is severely misguided,      syntactic and semantic features and execution information to infer
as the dataset is filled with multi-fault bugs. Multi-fault bugs can    promising patches for further evolution. To generate the RIF patch,
be decomposed into independent single-fault bugs triggering dif-        our approach reuses a simultaneous strategy [37] that identifies
ferent failures. Repairing multi-fault bugs by handling multiple        locations for co-evolution and applies similar changes to those
failures simultaneously is practically uncommon for debugging, as       locations. The approach relies on local repair to address EOH and
the developer typically deals with one failure at a time [18, 31].      uses pattern-based methods to generate DU, SU, and OA patches.
   To understand existing approaches’ abilities of repairing single-       We envision to have a suite of specialized patch generators.
fault multi-location bugs, we proposed an approach to detect such       Once a failure occurs, one would not easily know which gener-
bugs and found that there are 118 single-fault multi-location bugs      ators to use for repair but can run all the generators in parallel
in the Defects4J v1.2 dataset and that current approaches [23, 37,      to get all the patches. This can be further improved via a trained
44, 46, 50, 51, 55] repaired at most 8 bugs, suggesting weak repair     multi-classifier [1, 27] to select the most suitable generators or an
abilities.                                                              ensemble approach (e.g., [54]) for generator prioritization.
Towards Practical and Useful Automated Program Repair
for Debugging                                                                                                                     SE 2030, November 2024, Puerto Galinàs (Brazil)


REFERENCES                                                                                       International Conference on Software Engineering (ICSE). IEEE/ACM, 25–27.
 [1] Aldeida Aleti and Matias Martinez. 2021. E-APR: Mapping the effectiveness of           [24] Kui Liu, Anil Koyuncu, Dongsun Kim, and Tegawendé F Bissyandé. 2019. TBar:
     automated program repair techniques. Empirical Software Engineering 26 (2021),              Revisiting template-based automated program repair. In Proceedings of ACM 28th
     1–30.                                                                                       SIGSOFT International Symposium on Software Testing and Analysis (ISSTA). ACM,
 [2] Johannes Bader, Andrew Scott, Michael Pradel, and Satish Chandra. 2019. Getafix:            31–42.
     Learning to fix bugs automatically. Proceedings of the ACM on Programming              [25] Kui Liu, Shangwen Wang, Anil Koyuncu, Kisub Kim, Tegawendé F Bissyandé,
     Languages 3, OOPSLA (2019), 1–27.                                                           Dongsun Kim, Peng Wu, Jacques Klein, Xiaoguang Mao, and Yves Le Traon. 2020.
 [3] Rohan Bavishi, Hiroaki Yoshida, and Mukul R Prasad. 2019. Phoenix: Automated                On the efficiency of test suite based program repair. In Proceedings of International
     data-driven synthesis of repairs for static analysis violations. In Proceedings of          Conference on Software Engineering. 615–627.
     the 27th ACM Joint Meeting on the Foundations of Software Engineering. 613–624.        [26] Sergey Mechtaev, Jooyong Yi, and Abhik Roychoudhury. 2016. Angelix: Scal-
 [4] Moritz Beller, Georgios Gousios, Annibale Panichella, and Andy Zaidman. 2015.               able multiline program patch synthesis via symbolic analysis. In Proceedings
     When, how, and why developers (do not) test in their IDEs. In Proceedings of the            of IEEE/ACM 38th International Conference on Software Engineering (ICSE).
     10th Joint Meeting on the Foundations of Software Engineering. 179–190.                     IEEE/ACM, 691–701.
 [5] Andrew Bragdon, Steven P Reiss, Robert Zeleznik, Suman Karumuri, William               [27] Xiangxin Meng, Xu Wang, Hongyu Zhang, Hailong Sun, and Xudong Liu. 2022.
     Cheung, Joshua Kaplan, Christopher Coleman, Ferdi Adeputra, and Joseph J LaVi-              Improving fault localization and program repair with deep semantic features
     ola Jr. 2010. Code bubbles: rethinking the user interface paradigm of integrated            and transferred knowledge. In Proceedings of the 44th International Conference on
     development environments. In Proceedings of the 32nd ACM/IEEE International                 Software Engineering (ICSE). IEEE/ACM, 1169–1180.
     Conference on Software Engineering-Volume 1. 455–464.                                  [28] Martin Monperrus. 2018. Automatic software repair: A bibliography. ACM
 [6] Tom Britton, Lisa Jeng, Graham Carver, Paul Cheak, and Tomer Katzenellenbo-                 Computing Surveys (CSUR) 51, 1 (2018), 1–24.
     gen. 2013. Reversible debugging software. Judge Bus. School, Univ. Cambridge,          [29] Martin Monperrus. 2018. The Living review on automated program repair. Tech-
     Cambridge, UK, Tech. Rep 229 (2013).                                                        nical Report hal-01956501. HAL/archives-ouvertes.fr.
 [7] Hadeel Eladawy, Claire Le Goues, and Yuriy Brun. 2024. Automated Program               [30] Yannic Noller, Ridwan Shariffdeen, Xiang Gao, and Abhik Roychoudhury. 2022.
     Repair, What Is It Good For? Not Absolutely Nothing!. In 2024 IEEE/ACM 46th                 Trust enhancement issues in program repair. In Proceedings of the 44th Interna-
     International Conference on Software Engineering (ICSE). IEEE Computer Society,             tional Conference on Software Engineering. 2228–2240.
     868–868.                                                                               [31] Alexandre Perez, Rui Abreu, and Marcelo d’Amorim. 2017. Prevalence of single-
 [8] Xiang Gao, Bo Wang, Gregory J Duck, Ruyi Ji, Yingfei Xiong, and Abhik Roy-                  fault fixes and its impact on fault localization. In 2017 IEEE International Confer-
     choudhury. 2021. Beyond tests: Program vulnerability repair via crash constraint            ence on Software Testing, Verification and Validation (ICST). IEEE, 12–22.
     extraction. ACM Transactions on Software Engineering and Methodology (TOSEM)           [32] Zichao Qi, Fan Long, Sara Achour, and Martin Rinard. 2015. An analysis of patch
     30, 2 (2021), 1–27.                                                                         plausibility and correctness for generate-and-validate patch generation systems.
 [9] Claire Le Goues, Michael Pradel, and Abhik Roychoudhury. 2019. Automated                    In Proceedings of ACM 24th SIGSOFT International Symposium on Software Testing
     program repair. Commun. ACM 62, 12 (2019), 56–65.                                           and Analysis (ISSTA). ACM, 24–36.
[10] Kai Huang, Xiangxin Meng, Jian Zhang, Yang Liu, Wenjie Wang, Shuhao Li, and            [33] Steven P Reiss, Xuan Wei, and Qi Xin. 2023. Quick Repair of Semantic Errors
     Yuqing Zhang. 2023. An empirical study on fine-tuning large language models                 for Debugging. In 2023 IEEE/ACM International Workshop on Automated Program
     of code for automated program repair. In 2023 38th IEEE/ACM International                   Repair (APR). IEEE, 9–10.
     Conference on Automated Software Engineering (ASE). IEEE, 1162–1174.                   [34] Steven P Reiss and Qi Xin. 2022. A Quick Repair Facility for Debugging. arXiv
[11] Kai Huang, Zhengzi Xu, Su Yang, Hongyu Sun, Xuejun Li, Zheng Yan, and Yuqing                preprint arXiv:2202.05577 (2022).
     Zhang. 2023. A survey on automated program repair techniques. arXiv preprint           [35] Steven P Reiss, Qi Xin, and Jeff Huang. 2018. SEEDE: simultaneous execution
     arXiv:2303.18184 (2023).                                                                    and editing in a development environment. In Proceedings of 33rd IEEE/ACM
[12] Jiajun Jiang, Yingfei Xiong, Hongyu Zhang, Qing Gao, and Xiangqun Chen.                     International Conference on Automated Software Engineering. 270–281.
     2018. Shaping program repair space with existing patches and similar code. In          [36] RepairTools 2024. Program Repair Tools. https://program-repair.org/tools.html
     Proceedings of ACM 27th SIGSOFT International Symposium on Software Testing            [37] Seemanta Saha, Ripon k. Saha, and Mukul r. Prasad. 2019. Harnessing evolution
     and Analysis (ISSTA). ACM, 298–309.                                                         for multi-hunk program repair. In Proceedings of IEEE/ACM 41st International
[13] Nan Jiang, Kevin Liu, Thibaud Lutellier, and Lin Tan. 2023. Impact of code                  Conference on Software Engineering (ICSE). IEEE/ACM, 13–24.
     language models on automated program repair. arXiv preprint arXiv:2302.05020           [38] Edward K Smith, Earl T Barr, Claire Le Goues, and Yuriy Brun. 2015. Is the cure
     (2023).                                                                                     worse than the disease? overfitting in automated program repair. In Proceedings
[14] Nan Jiang, Thibaud Lutellier, and Lin Tan. 2021. CURE: Code-aware neural                    of ACM 10th Joint Meeting on Foundations of Software Engineering (FSE). ACM,
     machine translation for automatic program repair. In Proceedings of IEEE/ACM                532–543.
     43rd International Conference on Software Engineering (ICSE). IEEE/ACM, 1161–          [39] Dominik Sobania, Martin Briesch, Carol Hanna, and Justyna Petke. 2023. An
     1173.                                                                                       analysis of the automatic bug fixing performance of chatgpt. arXiv preprint
[15] René Just, Darioush Jalali, and Michael D Ernst. 2014. Defects4J: A database of ex-         arXiv:2301.08653 (2023).
     isting faults to enable controlled testing studies for Java programs. In Proceedings   [40] Shin Hwei Tan, Hiroaki Yoshida, Mukul R Prasad, and Abhik Roychoudhury. 2016.
     of ACM 23rd SIGSOFT International Symposium on Software Testing and Analysis                Anti-patterns in search-based program repair. In Proceedings of the 2016 24th
     (ISSTA). ACM, 437–440.                                                                      ACM SIGSOFT International Symposium on Foundations of Software Engineering.
[16] Sungmin Kang and Shin Yoo. 2022. Language models can prioritize patches for                 727–738.
     practical program patching. In Proceedings of the Third International Workshop         [41] Rijnard van Tonder and Claire Le Goues. 2018. Static automated program repair
     on Automated Program Repair. 8–15.                                                          for heap properties. In Proceedings of the 40th International Conference on Software
[17] Dongsun Kim, Jaechang Nam, Jaewoo Song, and Sunghun Kim. 2013. Automatic                    Engineering. 151–162.
     patch generation learned from human-written patches. In Proceedings of the 35th        [42] Yuxiang Wei, Chunqiu Steven Xia, and Lingming Zhang. 2023. Copiloting the
     International Conference on Software Engineering (ICSE). IEEE, 802–811.                     Copilots: Fusing Large Language Models with Completion Engines for Automated
[18] Amy J Ko and Brad A Myers. 2008. Debugging reinvented: asking and answering                 Program Repair. arXiv preprint arXiv:2309.00608 (2023).
     why and why not questions about program behavior. In Proceedings of the 30th           [43] Ming Wen, Junjie Chen, Rongxin Wu, Dan Hao, and Shing-Chi Cheung. 2018.
     international conference on Software engineering. 301–310.                                  Context-aware patch generation for better automated program repair. In Proceed-
[19] Pavneet Singh Kochhar, Tegawendé F Bissyandé, David Lo, and Lingxiao Jiang.                 ings of IEEE/ACM 40th International Conference on Software Engineering. 1–11.
     2013. An empirical study of adoption of software testing in open source projects.      [44] Chu-Pan Wong, Priscila Santiesteban, Christian Kästner, and Claire Le Goues.
     In Proceedings of 13th International Conference on Quality Software. 103–112.               2021. VarFix: Balancing edit expressiveness and search effectiveness in automated
[20] Anil Koyuncu, Kui Liu, Tegawendé F Bissyandé, Dongsun Kim, Martin Monperrus,                program repair. In Proceedings of ACM 29th Joint European Software Engineering
     Jacques Klein, and Yves Le Traon. 2019. iFixR: Bug report driven program repair.            Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE).
     In Proceedings of the 27th ACM Joint Meeting on the Foundations of Software                 ACM, 354–366.
     Engineering. 314–325.                                                                  [45] Chunqiu Steven Xia, Yuxiang Wei, and Lingming Zhang. 2023. Automated
[21] Xuan-Bach D Le, Ferdian Thung, David Lo, and Claire Le Goues. 2018. Over-                   program repair in the era of large pre-trained language models. In Proceedings of
     fitting in semantics-based automated program repair. In Proceedings of the 40th             the 45th International Conference on Software Engineering (ICSE 2023). Association
     international conference on software engineering. 163–163.                                  for Computing Machinery.
[22] Claire Le Goues, ThanhVu Nguyen, Stephanie Forrest, and Westley Weimer. 2011.          [46] Chunqiu Steven Xia and Lingming Zhang. 2022. Less training, more repairing
     GenProg: A generic method for automatic software repair. IEEE Transactions on               please: revisiting automated program repair via zero-shot learning. In Proceedings
     Software Engineering (TSE) 38, 1 (2011), 54–72.                                             of the 30th ACM Joint European Software Engineering Conference and Symposium
[23] Yi Li, Shaohua Wang, and Tien N Nguyen. 2022. DEAR: A novel deep learning-                  on the Foundations of Software Engineering. 959–971.
     based approach for automated program repair. In Proceedings of IEEE/ACM 44th           [47] Chunqiu Steven Xia and Lingming Zhang. 2023. Keep the Conversation Go-
                                                                                                 ing: Fixing 162 out of 337 bugs for $0.42 each using ChatGPT. arXiv preprint
SE 2030, November 2024, Puerto Galinàs (Brazil)                                                                           Qi Xin, Haojun Wu, Steven P. Reiss, and Jifeng Xuan


     arXiv:2304.00385 (2023).                                                                  arXiv:2301.03270 (2023).
[48] Jifeng Xuan, Matias Martinez, Favio Demarco, Maxime Clement, Sebastian Lame-         [53] Hao Zhong and Zhendong Su. 2015. An empirical study on real bug fixes. In
     las Marcote, Thomas Durieux, Daniel Le Berre, and Martin Monperrus. 2016.                 Proceedings of IEEE/ACM 37th International Conference on Software Engineering
     Nopol: Automatic repair of conditional statement bugs in java programs. IEEE              (ICSE), Vol. 1. IEEE/ACM, 913–923.
     Transactions on Software Engineering 43, 1 (2016), 34–55.                            [54] Wenkang Zhong, Chuanyi Li, Kui Liu, Tongtong Xu, Tegawendé F Bissyandé,
[49] Jun Yang, Yuehan Wang, Yiling Lou, Ming Wen, and Lingming Zhang. 2022.                    Jidong Ge, Bin Luo, and Vincent Ng. 2023. Practical Program Repair via Preference-
     Attention: Not just another dataset for patch-correctness checking. arXiv preprint        based Ensemble Strategy. arXiv preprint arXiv:2309.08211 (to appear in ICSE’24)
     arXiv:2207.06590 (2022).                                                                  (2023).
[50] He Ye and Martin Monperrus. 2023. ITER: Iterative Neural Repair for Multi-           [55] Qihao Zhu, Zeyu Sun, Yuan-an Xiao, Wenjie Zhang, Kang Yuan, Yingfei Xiong,
     Location Patches. arXiv preprint arXiv:2304.12015 (2023).                                 and Lu Zhang. 2021. A syntax-guided edit decoder for neural program repair.
[51] Yuan Yuan and Wolfgang Banzhaf. 2020. Toward better evolutionary program                  In Proceedings of ACM 29th Joint Meeting on European Software Engineering
     repair: An integrated approach. ACM Transactions on Software Engineering and              Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE).
     Methodology (TOSEM) 29, 1 (2020), 1–53.                                                   ACM, 341–353.
[52] Quanjun Zhang, Chunrong Fang, Yuxiang Ma, Weisong Sun, and Zhenyu Chen.
     2023. A Survey of Learning-based Automated Program Repair. arXiv preprint

