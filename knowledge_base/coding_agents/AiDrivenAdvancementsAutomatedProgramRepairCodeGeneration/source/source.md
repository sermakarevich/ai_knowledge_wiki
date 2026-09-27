# A Comprehensive Survey of AI-Driven Advancements and Techniques in Automated Program Repair and Code Generation
Source: https://arxiv.org/abs/2411.07586v1
Kind: pdf
Fetched: 2026-09-23T19:54:39.835687+00:00
Tool: pdftotext
Research-Target: /Users/sergii/.ai/knowledge/research_topics/coding_agents/research/ai_coding_best_practices
Topic: coding_agents

                                         A Comprehensive Survey of AI-Driven Advancements and
                                         Techniques in Automated Program Repair and Code
                                         Generation
                                         AVINASH ANAND, Indraprastha Institute of Information Technology, India




arXiv:2411.07586v1 [cs.AI] 12 Nov 2024
                                         NISHCHAY YADAV, Indraprastha Institute of Information Technology, India
                                         AKSHIT GUPTA, Indraprastha Institute of Information Technology, India
                                         SHAURYA BAJAJ, Indraprastha Institute of Information Technology, India
                                         Bug fixing and code generation have been core research topics in software development for many years.
                                         The recent explosive growth in Large Language Models has completely transformed these spaces, putting in
                                         reach incredibly powerful tools for both. In this survey, 27 recent papers have been reviewed and split into
                                         two groups: one dedicated to Automated Program Repair (APR) and LLM integration and the other to code
                                         generation using LLMs. The first group consists of new methods for bug detection and repair, which include
                                         locating semantic errors, security vulnerabilities, and runtime failure bugs. The place of LLMs in reducing
                                         manual debugging efforts is emphasized in this work by APR toward context-aware fixes, with innovations
                                         that boost accuracy and efficiency in automatic debugging. The second group dwells on code generation,
                                         providing an overview of both general-purpose LLMs fine-tuned for programming and task-specific models.
                                         It also presents methods to improve code generation, such as identifier-aware training, fine-tuning at the
                                         instruction level, and incorporating semantic code structures. This survey work contrasts the methodologies
                                         in APR and code generation to identify trends such as using LLMs, feedback loops to enable iterative code
                                         improvement and open-source models. It also discusses the challenges of achieving functional correctness and
                                         security and outlines future directions for research in LLM-based software development.

                                         CCS Concepts: • Computing methodologies → Artificial intelligence; • Software and its engineering
                                         → Software creation and management.
                                         Additional Key Words and Phrases: Code Generation, Automated Program Repair
                                         ACM Reference Format:
                                         Avinash Anand, Nishchay Yadav, Akshit Gupta, and Shaurya Bajaj. 2024. A Comprehensive Survey of AI-Driven
                                         Advancements and Techniques in Automated Program Repair and Code Generation. 1, 1 (November 2024),
                                         19 pages. https://doi.org/XXXXXXX.XXXXXXX

                                         1    Introduction
                                         Large Language Models (LLMs) have steadily gained popularity in the field of automated software
                                         engineering, including primarily bug fixing [18] [23] [19] [25] [12] and code generation [15] [21]
                                         [6]. Over the past decade, APR and code generation have greatly risen in use [8] [10] and hence,
                                         have also warranted a great amount of research into the subject. A lot of tools that employ APR and
                                         Authors’ Contact Information: Avinash Anand, Indraprastha Institute of Information Technology, New Delhi, Delhi, India;
                                         Nishchay Yadav, Indraprastha Institute of Information Technology, New Delhi, Delhi, India; Akshit Gupta, Indraprastha In-
                                         stitute of Information Technology, New Delhi, Delhi, India; Shaurya Bajaj, Indraprastha Institute of Information Technology,
                                         New Delhi, Delhi, India.

                                         Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee
                                         provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the
                                         full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored.
                                         Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires
                                         prior specific permission and/or a fee. Request permissions from permissions@acm.org.
                                         © 2024 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                         ACM XXXX-XXXX/2024/11-ART
                                         https://doi.org/XXXXXXX.XXXXXXX


                                                                                                            , Vol. 1, No. 1, Article . Publication date: November 2024.
2                                                             Avinash Anand, Nishchay Yadav, Akshit Gupta, Shaurya Bajaj


natural language processing for code generation have been developed [15] [21] [6], which use an
array of different techniques, including implementing Abstract Syntax Trees (ASTs), using varying
heuristics for ranking plausible patches, patterns, and context-matching, among others. Using LLMs
in code-related tasks has significantly improved the quality and speed of automating programming
and discovering bugs in code. These tasks include summarizing code, generating code based on
natural language requests, fixing bugs in pre-existing code, and understanding relatively large and
complex repositories. However, in this paper, we’ll only be covering the research and studies done
in the field of code generation and bug fixing, and to make understanding the work done in these
fields easier, we’ve divided the tools and papers that we’ve covered into these two categories. LLMs
have widely gained usage in these tools due to the natural advantage of having been trained on
extremely large datasets and billions of parameters. Hence, it is easier to employ large LLMs to
do particular tasks pertaining to programming. This leads to impressive performance and sizable
advantages when compared to training models from scratch [18] [19] [25]. Simultaneously, the
task of employing LLMs in APR and code generation is also extremely complex and encompasses
various areas with their own extensive research, such as benchmarking, repair scenarios (syntactic
errors, semantic errors, etc.), repair techniques (recompilation, binary rewriting, etc.) testing of
repairs (patch generation, input testing, coevolution) among others. Hence, understanding the
work already done in this field can prove to be quite complex and time consuming. This survey
paper aims to summarize the research and work already accomplished in this growing field to assist
others in gaining a better understanding of how these tools work, their performance in practical
scenarios, the areas they work on, and their limitations. We’ve collected 27 papers and summarized
various factors about them, including the LLMs they use, the programming languages they work
on, and, by extension, the difficulties faced in building language-agnostic APR tools, the approach
they take to repair bugs and generate code, and the challenges that are still being worked on in the
field. In conclusion, this paper aims to:

    (1) Collect research done on APR and code generation using LLMs and summarize the goals
        achieved.
    (2) Elucidate the repair scenarios these tools can be used for and the programming languages
        they work on.
    (3) How LLMs are integrated into the workflow of repairing and generating code and the
        challenges faced in doing so.
    (4) The limitations of using LLMs in code-related tasks and cases which are still being worked
        on.


2    Survey Methodology
This section covers the measures taken in order to carry out the survey, the ways which we have
implemented in to search, collect and filter out the models, research papers and journals which
closely align with our purpose for this literature survey.


2.1 Research Questions
Through this survey we aim to answer the following research questions, our criteria and metrics
for inclusion of a particular paper focuses mostly on whether it has helped us to answer any of
these questions more comprehensively. Any resource that added no value on any of these topics
were discarded from the study. All of these questions revolve around the existing and the emerging
technologies around APR and Code generation

, Vol. 1, No. 1, Article . Publication date: November 2024.
A Comprehensive Survey of AI-Driven Advancements and Techniques in Automated Program Repair and Code Generation3




                                  Fig. 1. Papers Included in Every Domain


  (1) How have AI techniques, especially large language models (LLMs), improved software
      debugging and bug fixing? What are some recent trends and common challenges in using AI
      for these tasks?
  (2) How do modern debugging tools and benchmarks help evaluate the effectiveness of bug-fixing
      methods? What are the common gaps or limitations in these tools?
  (3) What are the key differences between popular code generation models? How do these models
      perform on tasks like code completion and code summarization?
  (4) How do different AI models and tools compare in handling various code-related tasks? What
      are the main strengths and weaknesses of these models?

2.2   Methods Employed
A number of methods were used in order to select and bifurcate the resources so that the survey
can be done more effectively, these are the following :
  (1) Systematic Literature Review
      A review of the available literature on the subject of interest and related work. This also
      involves having a clear inclusion and exclusion criteria. It is done using searching relevant
      papers revolving around the main topic among various databases. Then applying inclusion
      criteria and exclusion criteria mentioned above and finally conducting a detailed analysis
      and categorizing the selected papers/models under umbrella categories of Code Generation
      and Automated Program Repair as shown in Fig. 1.
  (2) Taxonomy Development
      This method is employed by creating a classification of the AI techniques, tools and methods
      used for debugging, bug fixing and code generation. This comparative analysis is done
      upon the objectives, techniques and outcomes, further figuring out overlaps and distinctions
      between categories.
  (3) Comparative Analysis
      A comparison was made between the selected papers using various evaluation criteria such
      as performance, accuracy etc. Tabular and graphical description for a better visualization of
      the comparison was done between the model and tools.

                                                           , Vol. 1, No. 1, Article . Publication date: November 2024.
4                                                             Avinash Anand, Nishchay Yadav, Akshit Gupta, Shaurya Bajaj


    (4) Trend Analysis and Gap Identification
        A dedicated survey objective was to identify open challenges, and research gaps in AI-driven
        techniques and methods for APR and code generation. In a category specific approach it was
        attempted to figure out the common themes, recurring challenges, and under-explored areas
        across all categories. An attempt to see the future trends and potential in the similar field
        was made as well.
    (5) Survey of Benchmarks and Evaluation Metrics
        A part of the survey involves a study on the benchmarks and evaluation metrics employed for
        evaluating the models and tools. Identifying similarities and differences in the benchmarks
        and listing out the description for each of them ultimately analyzing the strengths and
        weaknesses of different benchmarks and suggesting improvements or new metrics.

3     Research Questions
3.1    How have AI techniques, especially large language models (LLMs), improved
       software debugging and bug fixing? What are some recent trends and common
       challenges in using AI for these tasks?
Automated Program Repair (APR) can be used to achieve a number of goals, one being how it
can be applied to fix security bugs through numerous approaches. Security bugs often arise from
vulnerabilities like buffer overflows, input validation issues, race conditions, or improper access
control. APR can be used to address these issues in different ways, depending on the type of bug,
the repair technique, and the tools used. Below are several ideas on how APR can be applied for
fixing security bugs:
3.1.1 Security Bugs.
   (1) Template Based Patching: There are many Automatic Program Repair (APRs) tools that
       use already existing templates to fix security vulnerabilities [18] [19]. For instance, they can
       fix SQL injection and other types of bugs. Thus, the process is made faster when at least some
       bugs are already fixed.
   (2) Dynamic Analysis for Security Bugs: Methods like fuzzing and symbolic execution are
       the reasons for security flaws that might have been unnoticed at the time of the execution of
       the program [12]. Afterward, the tools can generate dummy patches which will be tested by
       executing on various inputs. The results of the testing will then enable the patches and input
       to co-evolve, thus, the fix for the problem will be improved [17] [25] [12].
   (3) Search-Based APR for Security: Search-based methods are widely utilized in different
       APR and debugging systems to create and confirm patches based on mutations of the initial
       code [25]. These tools likewise act in the same way as the previous ones, where they output
       a list of likely patches and then use different methods to search for the optimal patch that
       meets the given conditions [17] [25].
   (4) Specification-Guided APR for Security Protocols: The APR tools we looked at mostly
       used fuzzing to verify the security of different internet protocols. This process was done by
       obtaining precise grammar and specifications for the protocols [25]. Then the patches are
       checked by applying them on different kinds of inputs and they are tested on the protocols
       [17] [19] [25].
   (5) Input Sanitization and Validation Patches: The problem of security vulnerabilities in
       software may be due to the fact that there is no proper input validation or sanitization. Such
       a situation can lead to problems such as injection attacks or data corruption. Automated
       Program Repair (APR) tools can detect these flaws by checking how inputs are treated
       and processed in the code. One approach is to detect the lack of sufficient input validation

, Vol. 1, No. 1, Article . Publication date: November 2024.
A Comprehensive Survey of AI-Driven Advancements and Techniques in Automated Program Repair and Code Generation5


      after which, the tool can automatically add the required functions for sanitizing, filtering, or
      escaping harmful characters, for example. Through this method, APR enhances the security of
      the software, preventing the use of harmful inputs to breach the system or cause the software
      to behave unexpectedly. Besides, this automated method reduces the manual intervention,
      thus, ensuring more consistency and reliability of input validation throughout the codebase
      [25].
  (6) Repairing Memory Safety Bugs: Bugs concerning memory safety, such as use-after-free,
      buffer overflows, and null pointer dereferences, are very common in low-level programming
      languages, particularly C and C++. These security threats can bring about situations of high
      risk, crash, and non-deterministic behavior in the software. Automated Program Repair (APR)
      methods can both detect unsafe memory accesses [19] and apply corrective measures, such as
      conducting bounds checking, utilizing safer memory allocation techniques [12], or replacing
      raw pointers with smart pointers. The positives of automatically identifying and treating
      these issues are, APR helping to improve the robustness and security of programs, and thus,
      the exploitation or failures probability decreasing.




                         Fig. 2. Programming languages in the papers we surveyed


3.1.2 Semantic Bugs.
   (1) Pattern-Based Patching for Semantic Bugs: The repair of semantic bugs, which consist of
       logical errors or deviations from the expected functioning of the program, can be addressed
       through pattern-based Automated Program Repair (APR) systems [26] [19] [12].
   (2) Fuzzing Techniques for Semantic Bugs: The fact that fuzzing is a very useful tool to
       discover memory and semantic bugs is a development in psychometrics. Techniques like

                                                           , Vol. 1, No. 1, Article . Publication date: November 2024.
6                                                             Avinash Anand, Nishchay Yadav, Akshit Gupta, Shaurya Bajaj


        Greybox Fuzzing [23] which is a testing technique where the fuzzer has partial knowledge of
        the program’s internal structure, combining both black-box and white-box testing elements,
        are found among such techniques. Its goal is to generate test inputs that are as efficient as
        possible in revealing the bugs using the feedback from the program’s execution. This fuzzing
        method enables the detection of bugs that are very difficult to uncover by the traditional
        testing methods [25] [12].
    (3) Search-Based APR for Semantic Bugs: Using evolutionary algorithms, it is possible to
        search different repair options with search-based APR techniques [19] [25]. In this case, the
        candidates produced are also the ones that are covered by the test suites or specifications to
        be able to find the fixes that remove semantic inconsistencies. The process includes mutating
        a part of the program, running the variants, and picking the most efficient one. Search-based
        APR has been very successful in correcting semantic errors for which a specific bug pattern
        is not easy to detect.
    (4) Specification-Guided Repair: Semantic bugs frequently happen due to incorrect or incom-
        plete specifications [7] [19]. APR systems that use specification-guided repair rely on formal
        models of the expected behavior to identify the deviations [25]. This method is practiced
        today because of the fact that the patches produced not only solve the bugs but also conform
        to the formal specifications of the system [12].

3.1.3    Syntactic Bugs.
    (1) Pattern-Based Patching for Syntactic Bugs: Syntactic bugs, which are the bugs that pertain
        to programming language syntax rules as well as having other issues related to incorrect
        code structures, can be dealt with through pattern-based Automated Program Repair (APR)
        systems in a very efficient manner. These systems consider the syntactic violations and
        then use the predefined correction patterns to get to the desired outcome. FixMiner is a tool
        that uses mining previous bug-fixing commits of common syntax errors to generate repair
        patterns, based on those corrections, offering an effective solution for recurring syntactic
        issues [5].
    (2) Grammar-Based Fuzzing for Syntax Validation: Tools that use grammar-based fuzzing
        are concerned with syntactic bugs and they therefore produce program inputs which adhere
        to the grammar rules of the language in question. These tools modify the inputs according to
        the Abstract Syntax Trees (ASTs) to keep them syntactically valid, which in turn helps to get
        bugs that have to do with incomplete or wrongly structured code. Grammar-aware mutation
        strategies have proven effective in discovering syntactic anomalies that can disrupt program
        execution [7].
    (3) Search-Based Techniques for Syntactic Repairs: Search-based techniques can be applied
        to fix syntactic bugs in a similar manner as their use for semantic ones. The methods in this
        case look through many code modifications and then test them so as to get a valid syntactic fix.
        These tools explore a space of potential syntactic mutations and create candidate patches that
        are consistent with the programming language’s syntactic rules and the program’s original
        intent.

3.2     What recent trends have emerged for using AI in APR tools?
Recent Trends:
      • Pre-trained Models: The recruiting of the use of pre-trained models (Codex, CodeT5) that
        have been fine-tuned on large programming datasets is gaining traction.

, Vol. 1, No. 1, Article . Publication date: November 2024.
A Comprehensive Survey of AI-Driven Advancements and Techniques in Automated Program Repair and Code Generation7


      • Transfer Learning for Code: LLMs are becoming more adaptable to transfer learning, which
        is a technique where models pre-trained on general code can be fine-tuned for specific
        bug-fixing tasks.
      • Self-Supervised Learning: This allows LLMs to train on unlabeled datasets, taking advantage
        of the fact that there are a lot of code reposito ries without needing someone to annotate
        them.
      • Explainable AI (XAI): There are initiatives to make the AI-powered bug fixing process more
        interpretable and transparent so that developers can understand the reasoning behind the
        AI’s solution.
      • Interactive Debugging Systems: Tools are becoming more interactive, integrating active
        learning where AI requests human help to resolve unclear cases.
      • Multi-modal Models: New models are not only incorporating code but also comments, docu-
        mentation, and logs, which enhances the AI’s ability to understand the context of bugs.
   There have been a large number of advancements in the realm of automated program repair
which have streamlined the process of integrating artificial intelligence and large language models
into code-related tasks. These include:
  (1) Pre-trained models: The use of pre-trained models such as GPT-4 which have been fine-
      tuned on large programming and bug datasets [12] has shown a steady upward trend over
      the past few years.
  (2) Neural Networks for Fault Localization: Through artificial intelligence, a program can
      carry out a deep analysis of some properties of the code like temporal properties [19] and
      thus be able to identify the bugs in the program. A number of APR tools also make use of
      Abstract Syntax Trees (ASTs) [18] [17] [25] to be able to reason about the control flow of the
      program and fixing it.
  (3) Automated Test Generation: Using AI to automatically create and run test cases [17]
      [25] in order to check the correctness of the potential solutions, so that the repairs are not
      breaking the existing functionality and also meet the desired specifications.
  (4) Test Coverage Improvement: Incorporating AI to dissect code modifications and guarantee
      that new or revised tests encompass all pertinent elements of the codebase, thus boosting the
      accuracy of the automated repairs [17] [25] . This also brings down the chances of overfitting
      which can be a cause of unexpected results for a program [25].

3.3    What challenges are being faced in APR right now?
In spite of having at least hundreds of studies on the subject and AI tools developed to the highest
level, APR is still having some problems and challenges that are yet to be solved. These include:
  (1) Accuracy and Reliability: APR tools still face the problem of sometimes incorrectly identi-
      fying perfectly fine code as faulty and vice-versa [23]. Hence, the corrections made by APR
      tools often need to be verified by humans before being implemented.
  (2) Context Sensitivity: APR tools still have difficulties with the comprehension of large
      codebases that have a lot of dependencies. This is one of the main reasons for the use of
      incorrect practices and repairs which are correct from the technical point of view but not for
      the whole codebase [18].
  (3) Resource Overhead: APR tools also have high demands regarding memory and computing
      power to work adequately [11]. Hence, the resource overhead may sometimes be the reason
      for the user’s workflow disruption and thus the productivity decrease.
  Common Challenges:

                                                           , Vol. 1, No. 1, Article . Publication date: November 2024.
8                                                             Avinash Anand, Nishchay Yadav, Akshit Gupta, Shaurya Bajaj




                             Fig. 3. The workflow of automated program repair tools




    • Generalization: LLMs frequently fail to generalize to new, previously unseen, bugs or highly
      domain-specific code, especially in systems with unconventional architectures or libraries.
    • Scalability: Debugging large, complex systems is still one of the most difficult tasks for LLMs
      as they have to deal with a huge amount of potential interactions and dependencies in the
      code.
    • Limited Understanding of Context: AI models have gone through many improvements but
      they may still make mistakes in understanding the full business logic or domain-specific
      intricacies behind the bugs which may result in incomplete or incorrect fixes.
    • Security Concerns: AI-generated fixes may inadvertently introduce security vulnerabilities
      or fail to address existing ones.
    • Bias in Training Data: LLMs may inherit biases from the data they were trained on, leading
      to over-reliance on common patterns and overlooking edge cases.
    • Overfitting to Benchmarks: Models that are trained mostly on benchmarks might specialize
      in certain datasets and hence not perform well in real-life scenarios.
    • Ethical Concerns: Copyright issues arise when LLMs are trained on proprietary code, and
      there are concerns about reproducing code without proper credit.


4   How do modern debugging tools and benchmarks help evaluate the effectiveness of
    bug-fixing methods? What are the common gaps or limitations in these tools?
Benchmarking is an important part of exploring new possibilities for APR tools and identifying the
repair scenarios that can be used. Several of the papers we surveyed performed a rigorous exercise
in benchmarking and comparison with existing state-of-the-art debugging tools. Benchmarking
against this baseline can help researchers and developers explore new ways to improve their
solutions and hopefully expand the set of scenarios we can trust APR to successfully fix.

, Vol. 1, No. 1, Article . Publication date: November 2024.
A Comprehensive Survey of AI-Driven Advancements and Techniques in Automated Program Repair and Code Generation9


                           Table 1. Targeted programming languages in the surveyed papers

                               Paper Title                               Programming Languages Targeted                      Benchmark(s)

 Report on Timing Side-Channel Mitigation via Automated Program Repair   C                                         QFuzz benchmark suite

 Report on Greybox Fuzzing for Concurrency Testing                       C, C++                                    SCTBench, ConVul

 Coevolution of Patches and Tests in Automated Program Repair            Java                                      Defects4J

 ProveNFix: Temporal-Guided Program Repair                               OCaml                                     Custom Benchmark

 Program Repair by Fuzzing over Patch and Input Space                    C                                         VulnLoc

 LLM-guided Protocol Fuzzing                                             C                                         ProFuzzBench

 DEAR                                                                    Java                                      Defects4J

 Transfer                                                                Java                                      Defects4J

 SPT Code                                                                Java, Python, JavaScript, PHP, Go, Ruby   BLEU, METEOR, ROUGE-L

 Debug like a Human: A Large Language Model Debugger                     Python, Java, C, C++                      HumanEval, MBPP, TransCoder

 Evaluating Debugging Capability of Large Language Models                Python, C++, JavaScript, Java             DebugBench, HumanEval, MBPP




4.1     Modern Debugging tools
In software engineering, modern tools of debugging assist the validation of bug-fixing approaches
mainly by automating the defect detection, location, and repairs on the code. Some of them, including
FuzzRepair [25] and AFLNet [12], integrate code fuzzing techniques, coupled with application of
program repair methods, to stage from one part of the code to another, generating diverse yet
reachable inputs leading them to bugs located in the hard-to-reach areas. Such approaches based
on fuzzing are frequently employed to assess how resilient bug-fixing methods are, because all of
them directly run patched code under diverse conditions to check how thoroughly the fix holds in
a variety of scenarios-and provide information that is valuable in supporting the robustness of the
repairs.
   With regard to machine learning, deep learning techniques for automatically generating patches
have been developed based on existing bug-fixing patterns such as CoCoNuT, SequenceR, and
Tufano19 [9], among others. These tools make well-supported research in assessing how well a bug-
fixing method generalizes across different codebases. For instance, CodeBERT, GraphCodeBERT,
and CugLM [14] evaluate bug fixes by embedding richer semantic code representations relative to
each other to allow for better targeting of potential faults and testing the effectiveness of repairs
through natural language processing and code-understanding models. TreeBERT and T5 [14]
further expand on this development by learning and understanding the structural relationships
within code as well as ensuring that bug fixes are not only syntactically correct but also logically
consistent with the rest of the system.
   ARJA-e, REWARDREPAIR, and EVOREPAIR [17] are tools for evolutionary and template-based
repair that use genetic algorithms and reward-based learning to automatically generate and validate
patches. These tools are quite important for evaluating bug-fixing methods as they can measure the
efficiency and scalability of repair techniques, especially in complex codebases. Similarly, TBAR
and Darjeeling [25] generate fixes based on predefined templates, which can then be utilized to
analyze the effectiveness of rule-based or human-guided patch generation. Prophet, on the other
hand, uses probabilistic models to predict the correctness of the patches. Thus, it proposes a method
to evaluate the success probability of a bug fix before applying it in a production environment [25].
   Tools like Fix2Fit and CPR [25] (Conditional Program Repair) make sure that not only the
rightness of fixes is checked but also their "fit" in the whole program context, which in turn
decreases side effects that might add up to new bugs, are the other example of the explained

                                                                             , Vol. 1, No. 1, Article . Publication date: November 2024.
10                                                            Avinash Anand, Nishchay Yadav, Akshit Gupta, Shaurya Bajaj


practice. SAVER and DLFix [9], with their emphasis on semantic analysis and deep learning models,
make sure that bug fixes not only fix the immediate problem but also secure the integrity of the
program as a whole. The use of these tools by the developers is often to ensure that the bug
fixing methods are put under tough tests for robustness, efficiency, and scalability, thus, improving
software reliability and stability.
   In conclusion, these tools give a range of methods like fuzzing, template-based repair, machine
learning, and semantic analysis, which together can provide a thorough assessment of bug-fixing
techniques as well as checking for its accuracy, robustness, and applicability.



4.2    Modern Benchmark tools
Using modern-day benchmarks is invaluable for measuring the efficiency of bug-fixing techniques
that require standardized and controlled settings in which researchers will be able to run the testing
and verification procedures as thoroughly as possible. These benchmarks include different functions
like checking code generation abilities or measuring debugging efficiency among the vulnerability
detection and debugging. In a precise manner, bug-fixing performance tests should be conducted
within the standards of software quality, which are the different dimensions of software quality.
Code generation benchmarks like HumanEval [27] [20] and MBPP [27] [20] are fundamental for
this purpose. HumanEval challenges models with a set of programming problems to determine
how well they can generate correct code and fix issues. At the same time, MBPP offers an array
of programming solutions to the problems, which are then used to check the efficiency of the
bug-fixing methods in generating and correcting code. These benchmarks help to the decision of
technical meaning to what degree bug-fixing techniques can work together with code generation
processes and fix real-world problems. For example, Fuzzing benchmarks such as ProFuzzBench [12]
and SCTBench [23] test the bug-fixing methods in terms of their efficiency in vulnerability detection
and addressing of vulnerabilities. ProFuzzBench’s network protocol implementations and fuzzing
tools lend a hand in debugging experiments and help researchers find out if bug-fixing methods are
resistant to the vulnerabilities of network protocols. SCTBench uses its collection of multithreaded
benchmarks to detect concurrency problems, thus verifying how well bug-fixing techniques can
deal with synchronization and multithreading problems. Debugging benchmarks like DebugBench
[20] and VulnLoc [25] are testing different debugging methods and the algorithms that can be used.
DebugBench assesses large language model debugging task performances, revealing important
information about the use of these models when trying to identify and correct errors. In contrast,
the process of VulnLoc has the focus on automatic vulnerability localization which implies finding
out the root cause of bugs with the smallest possible error margin. Moreover, Defects4J [17] [9]
[13] supplies defect data composed of real Java bugs through a database that is full of Java bugs.
This benchmark supports the testing of bug-fixing methods against real defects, therefore, bringing
the necessary practical perspective on the effectiveness of the solutions. TransCoder [27] is also
somehow important because of its code translation between programming languages, so that
researchers can do the correctness and bug test during the code translation with the bug-fixing
techniques. To sum up, modern benchmarks are vital elements in the evaluation of bug-fixing
techniques since through them a researcher can conduct different kinds of tests covering various
software quality aspects. These diverse and well-controlled testing environments enable the testing
of bug-fixing methods in the most comprehensive manner possible, which is the result of the
benchmarking process. Therefore, these methods can ultimately help to improve the software
systems’ functionality and fault tolerance.


, Vol. 1, No. 1, Article . Publication date: November 2024.
A Comprehensive Survey of AI-Driven Advancements and Techniques in Automated Program Repair and Code Generation
                                                                                                             11


4.3   Common Gaps and Limitations in Modern Debugging Tools and Benchmarks
Automated program repair (APR) as well as code generation are some of the powerful tools provided
by modern debugging tools and benchmarks. Nevertheless, some unreliability and limitations still
exist, preventing them from being more widely used and effective. Such limitations consist of
questionnaire issues, necessary datasets or benchmarks, as well as difficulty dealing with complex
bugs and program repair scenarios.
  (1) Generalization and Dataset Overfitting: A key obstacle lies in the generalization of the
      outcomes for large and diverse populations of programs. A lot of APR systems and tools
      have been benchmarked based on a limited number of benchmarks, which might not fully
      reflect the complexity of real-world coding problems. To illustrate, tools like QFuzz utilize
      the fuzzing approach to discover side-channel vulnerabilities, however, challenges arise
      because of the randomness and incompleteness of fuzzing, so that the bug detection is not
      comprehensive [19]. Along with that, it is possible that the results may not be applicable
      to other datasets that were not evaluated, as it was in the case of tools that were tested on
      datasets such as Defects4J [25]. These instruments are likely to cause overfitting when tested
      on these specific benchmarks. Thus, their outcomes in other contexts may be different [3].
  (2) Bias in Tool Selection and Limited Benchmarks: Selection bias is one of the main prob-
      lems faced by contemporary debugging frameworks. In such cases the tools and benchmarks
      are usually the most convenient or popular ones rather than diverse sets that can cover many
      real-world bugs. Consequently, this can produce incorrect results and produce imperfect
      evaluations. A case in point is the fact that some frameworks examine only widely used bench-
      marks such as Defects4J and focus on specific languages like Java, thus neglecting the possible
      other issues [17]. Besides, the concern is that the dataset only consists of language-specific
      datasets like CodeSearchNet which would limit the results across the different programming
      languages [7].
  (3) Non-Determinism and Overfitting in Repair Tools: Numerous current repair systems, for
      example, EVO REPAIR, have non-deterministic features that can generate multiple different
      results in separate runs, which makes it difficult to replicate the results consistently. This
      results in problems such as overfitting, where tools generate "plausible" patches that pass
      tests but are still possibly wrong [17]. Overfitting is particularly problematic in the case of
      test case evaluation, as even test adequacy does not guarantee correctness [17].
  (4) Limited Handling of Security and Non-Test Bugs: APR capabilities are still developing
      in fixing test case failures, but the tools do not have the same ability in dealing with security
      vulnerabilities and non-test bugs. Many tools are concentrating on bugs that lead to test
      failures only, while they are ignoring the problems containing memory safety bugs or side-
      channel attacks, which are significant as well [9]. Additionally, APR tools are finding it
      hard to deal with the fixing of memory safety bugs like buffer overflows, and programming
      languages such as C and C++ are especially hard to use in this case [12]. This problem limits
      the scope of their applicability in the systems where robust security measures are required.
  (5) Challenges with Input Validation and Memory Bugs: The input validation and memory
      safety bugs are problems that have to be solved. They are a major obstacle for APR tools.
      Although APR systems can handle input sanitization issues, they often do not produce patches
      that cover complex validation and sanitization functions thoroughly [25]. Additionally, the
      fixing of memory bugs such as use-after-free or null pointer dereference, is still a problem
      because of the complicated memory management that exists in languages like C and C++
      [12]. Even when the fixes are generated, they may not be able to address some deeper existing
      problems, such as ensuring correct memory allocation techniques.

                                                           , Vol. 1, No. 1, Article . Publication date: November 2024.
12                                                            Avinash Anand, Nishchay Yadav, Akshit Gupta, Shaurya Bajaj


     (6) Limitations in Evaluation Metrics and Test Suites: Many benchmarks often rely on
         evaluation metrics that are based on limited test suites, which may not always accurately
         reflect the complexity and as well as the diverse nature of real-world bugs. For instance,
         the usage of test cases from platforms like LeetCode can cause accessibility problems and
         biases since testers need specific accounts and the rate limits on such external platforms
         can restrict their ability to test effectively [17]. Besides, the simulated bugs adopted in some
         investigations may not be the exact reflection of the actual bugs faced in the production
         systems. Thus, the evaluation may not be accurate and realistic [17].
     (7) Difficulties with ML-Based Approaches: Machine learning (ML)-based strategies for APR
         have different problems particularly when it comes to dealing with rare or out-of-vocabulary
         tokens and generating large patches. For example, fixes that need multiple new statements
         or that have rare function names can be difficult to generate using the current ML-based
         methods, which makes them ineffective in more complex cases [9]. Moreover, the wrong
         predictions of ML models can make the correction of the wrong statements such that it
         becomes a compound issue of the patch generation error [9].

5     How do different AI models and tools compare in handling various code-related
      tasks? What are the main strengths and weaknesses of these models?
In recent years, various AI models and tools have emerged to assist in code-related tasks, each
demonstrating unique strengths and limitations. The comparison of these models highlights their
effectiveness across tasks such as code completion, bug fixing, code summarization, and code
translation or refactoring. By analyzing models like Codex [15], CodeT5 [21], GraphCodeBERT
[6], WizardCoder [24], Magicoder [22], Mixtral [3], Smaug [16], Zephyr [4], DeepSeek-Coder [7],
OpenCodeInterpreter [26], Phind [1], StarCoder2 [2], SPT Code [14], and GPT-4, we can better
understand how these tools excel in specific areas and where they fall short.

The speed and fluency in completing codes are the main traits of Codex (OpenAI) [15] which
has worldwide recognition, especially when it is used in GitHub Copilot. A system that gives
effective suggestions in real-time, which thereby increases the productivity of developers, consider-
ably. The drawback, however, is that Codex normally lacks accuracy in highly complex tasks or
domain-dependent code, where its performance degrades. CodeT5 [21], developed by Salesforce, is
also a reliable code reading tool, as long as it is used for smaller, focused tasks. Still, the real time
performance of CodeT5 is not as fast and flexible as that of Codex, so it is often not suitable for
situations which require dynamic coding. On the other hand, GraphCodeBERT [6] from Microsoft
has the ability to process more complicated code structures and it hence performs better in tasks
where there is a need to understand the dependencies. However, this additional complexity comes at
the cost of slower processing and the need for more resources and thus it is not suitable nor practical
to use it for rapid code completion tasks. Two of the more recent models, Phind.com/CodeLlama
(34B) [1] and DeepSeek-Coder (34B and 33B) [7], are models which standout. Phind’s fine-tuning on
Meta’s Code Llama enables it to outperform GPT-4 in HumanEval benchmark tests, thus confirming
the model’s high accuracy in generating code from prompts. DeepSeek-Coder’s "Fill-In-Middle"
(FIM) training greatly enhances its ability to complete unfinished code snippets, especially across
multiple languages such as Python and Java. Conversely, StarCoder2 (15B) [2] displays better
performance in tasks such as HumanEval+ due to a higher mastery of code in 16 different lan-
guages as compared to CodeLlama-34B. Nonetheless, StarCoder2 has troubles when it comes to
C++ code and it is not that successful in fill-in-the-middle tasks where DeepSeek-Coder has good
performance. Meanwhile, models like Smaug (72B) [16] and Zephyr (7B) [4] also play an important
role in code completion. Smaug is a model that has the best performance on the HuggingFace

, Vol. 1, No. 1, Article . Publication date: November 2024.
A Comprehensive Survey of AI-Driven Advancements and Techniques in Automated Program Repair and Code Generation
                                                                                                             13


Open LLM Leaderboard with 80.48% accuracy, leaving other models behind in terms of parameters.
Zephyr, which has an AlpacaEval score of 90.6%, is a model that is one of the best in bug detection
and scalability but still lags behind GPT-4 or Claude 3.5 in complex logic handling.

Another area that the models perform differently is bug fixing. Codex’s [15] fluency makes it
suitable for fixing common bugs quickly, but its ability is less effective when it comes to rare or
highly contextual bugs, often missing subtle logic errors. CodeT5 [21], on the other hand, is very
exact in rectifying bugs in localized codebases due to its task-specific training, but it has trouble
in real-time debugging, where Codex’s flexibility is an advantage. GraphCodeBERT [6] stands
out in bug detection and fixing when structural dependencies are involved making it a suitable
option for detecting bugs in difficult codebases. Nonetheless, similar to CodeT5, it is short in the
real-time flexibility required for the fast debugging. Phind [1] and DeepSeek-Coder [7] are also
the two major ones in bug fixing. Phind’s augmented dataset enables it to give excellent results in
the identification and solving of bugs, and even though it stumbles when it comes to specialized
or domain-specific issues, it is still very strong. DeepSeek-Coder, above all, on benchmarks like
Defects4J and HumanEval, shines in the detection of smaller logic errors. Regardless of that, its
performance varies across different programming languages, particularly in languages such as Bash,
where its poor performance compared to other models like GPT-4 is higher than others. Magicoder
(6.7B) [22] and WizardCoder (34B) [24], two strong models generally, exhibit some weaknesses in
debugging tasks. Magic Coder is the leader in a certain benchmark over GPT-3.5 and WizardCoder,
but it is not as good as CodeLlama-Python (34B) when it comes to large scale bug fixing tasks.
WizardCoder is not able to catch up with GPT-4 in debugging, bug localization, and code genera-
tion, even with well-engineered prompts, so this is its biggest problem. This confirms the fact that
the larger, more complicated models like GPT-4, which still lead in the handling of complex bugs
due to their thorough understanding of the larger context, have the advantage over the simpler ones.

Regarding code summarization, CodeT5 [21] is very efficient because it produces long and coherent
summaries that demonstrate a solid understanding of the code’s structure. Thus, it is suitable
for structured and localized codebases. GraphCodeBERT [6] is really good at summarizing code
with difficult dependencies which is based on graph technology that it uses to give context-aware
explanations but it can be slow on large datasets. Codex is good at summary tasks, howler delivering
crisp summaries for typical development environments but sometimes lacking the required level of
abstraction in case of large or complex codebases. GPT-4, because of its superior natural language
skills, is very good at writing summaries of long and complicated pieces of code, usually providing
more information than other models such as Codex or CodeT5. Though this has the advantage of
being resource efficient, it is overall slower in performance for summarizing small or less complex
codebases. Models such as SPT Code [14] are superior to other models such as GraphCodeBERT and
CodeBERT in terms of tasks like code summarization, even though there are still concerns about
data bias and generalizability. StarCoder2 [2] is impressive in the areas of code summarization
and machine-proof security, yet has its drawbacks in generating insecure code at high parameter
sizes, such as 15B. This is a constraint when contrasted to smaller and more secure models like
StableCode-3B, though StarCoder2 still has the overall better performance.

From the point of view of Codex[15] and GPT-4, both of them are the best in code translation and
refactoring. Codex is especially good for basic translations of codes between different programming
languages, whereas GPT-4 provides more accurate translations between different platforms, but
speed is the downside. CodeT5 [21] is also strong in this area, effectively converting the code
between different languages, yet preserving its functionality. However, it may be short of grasping

                                                           , Vol. 1, No. 1, Article . Publication date: November 2024.
14                                                            Avinash Anand, Nishchay Yadav, Akshit Gupta, Shaurya Bajaj


some delicate contextual indications which a model such as GPT-4 delivers. GraphCodeBERT’s
deep grasp of the structure of the code gives it a great leverage for tasks requiring the dependency
and data flow knowledge, nonetheless, its slower processing speed and high resource decision make
it less fit for the real-time refactoring tasks [6]. Phind.com/CodeLlama [1] and DeepSeek-Coder [7]
are also the best in code translation, particularly with multi-language support. Phind comes from
its Code Llama source, it is capable of nicely handling multiple programming languages, however,
it may not perform very well with languages that have extremely complex or sophisticated features.
DeepSeek-Coder’s repository-level deduplication guarantees that only concise and relevant outputs
are produced, which in turn increases its performance in code translation and refactoring, but its
limitations still remain for niche programming languages.

As for multilingual support, Mixtral [3] and Phind [1] are both the best among others for their
capability of dealing with multilingual datasets in an efficient way. Notably, Mixtral beats Claude-2.1
and Llama 2 70B on instruction fine-tuning and multilingual tasks. Phind obtains high scores due
to its extensive fine-tuning on programming problems for strong performance across languages.
Nevertheless, Smaug-72B [16] has been mainly tested on English-language datasets, which is
its weakness and it cannot perform well in multilingual environments, despite its leaderboard
success. GPT-4 and GraphCodeBERT [6] are great in general tasks but when it comes to handling
multiple languages, they become more resource-intensive. In conclusion, every model has its own
strengths and weaknesses in regard to the particular coding task in question. Codex is the best at
code completion and fast debugging, while GPT-4 is the king of complex tasks with unmatched
precision and depth, but it has speed and resource efficiency issues. CodeT5 and GraphCodeBERT
are the task-specific models, those are performing best in the structured environments but being
real-time adaptable is not their strength. New models like Phind, DeepSeek-Coder, and StarCoder2
are breaking the barriers of what AI can do in terms of accuracy and language support, however,
they still have difficulties in areas like resource intensity and security. By knowing the subtle
differences in these models, developers, and researchers will be able to choose the most suitable
tools for their particular coding needs.




     Fig. 4. A diagram illustrating how different code generation models do on varying code-related tasks




, Vol. 1, No. 1, Article . Publication date: November 2024.
A Comprehensive Survey of AI-Driven Advancements and Techniques in Automated Program Repair and Code Generation
                                                                                                             15




          Fig. 5. Some more models that were surveyed and their performance relative to others


6   How do AI models trained on general language datasets, specialized code datasets, or
    self-supervised learning approaches differ in their ability to handle code-related
    tasks?
The AI models’ aptness to effectively tackle code-related tasks has a relationship with the way
they’ve been trained. Different models have different approaches to the training techniques that
raise the level of their performance in such areas as code generation, debugging, and seman-
tic understanding. While many language models are pre-trained on datasets that are commonly
used, which enables them to have a more general linguistic knowledge, other models are con-
centrated on specialized datasets to build their coding capabilities. Besides, it is a fact that some
models have self-supervised or bootstrapped methods to improve their outputs, and the rest have
their own distinct methodologies. This diversity comes with varying strengths and weaknesses
across the models that in turn make a difference of the models in their applications in the real-world.

Models like Codex [15], CodeT5 [21], GraphCodeBERT [6], and Phind [1] have the common-
ality of being pre-trained on general language datasets. In this regard, Codex that powers GitHub
Copilot and is integrated into the OpenAI API is one of the most notable names for coping with
code-related tasks. It was originally fine-tuned from a collection of GPT models containing 12
billion parameters and trained on natural language data. Then, the code issue was dealt with using
publicly available code from GitHub. This in-depth training enables Codex to win by a large margin
over GPT-3 and GPT-J on HumanEval benchmarks because of many of their features such as Gide.
One of its significant features is its iterative problem-solving capability, where repeated sampling
significantly increases the likelihood of correctly solving complex tasks. The latter can be the case,
however, with inconsistency in its treatment of variables when it comes to intricate code scenarios
which then make its use unreliable in a code with many dependencies and complicated control
flows. On the other hand, CodeT5 [21] uses an approach of a unified encoder-decoder architecture,
making it possible to approach the task using both programming and natural languages, and thus
it can enhance its understanding of code semantics. It makes use of developer-assigned identifiers,
thus, the model improves its understanding of the code meaning which enables it to do such things
as defect detection and code translation more efficiently. This bimodal learning approach makes
CodeT5 to be the top performer on various tasks from the CodeXGLUE benchmark. Though it
has outstanding features, it is centered on identifier recovery meaning that it would be better if it
learned the structural relationships that are natural in code. GraphCodeBERT [6] takes a further

                                                           , Vol. 1, No. 1, Article . Publication date: November 2024.
16                                                            Avinash Anand, Nishchay Yadav, Akshit Gupta, Shaurya Bajaj


step and it enters the world of data flow graphs so code semantics are represented not just by telling
the sequence of tokens as was done by previous models. This model is pre-trained on the Code-
SearchNet dataset and thus, it is capable of performing tasks like code search and clone detection
due to its knowledge of the value transmission between variables. The structure-aware pre-training
tasks have their own contribution, but they may be left behind in case of the more complex logic
that needs the broader control flow structures. Similarly, Phind [1] fine-tunes the CodeLlama-34B
model that is trained on a proprietary dataset of about 80,000 structured programming problems
using advanced training techniques such as DeepSpeed ZeRO 3 and Flash Attention 2. The model
has attained a 73.8% pass rate on the HumanEval benchmark, thanks to a rigorous decontamination
process that guarantees the integrity and validation of the dataset.

In contrast to the ones listed above, OpenCodeInterpreter [26], StarCoder2 [2], SPT Code [14], and
Magicoder [22] are models mainly pre-trained to specialized code datasets which make them more
skilled at coding tasks. OpenCodeInterpreter picks up coding queries from specialized datasets, fil-
tering them for complexity, and turning single-turn query-response pairs into multi-turn dialogues
to create varied and contextual training examples. OpenCodeInterpreter’s cultivation of mimicry of
people was done realistically via dialogues, including but not limited to generating responses and
repeating outputs until they improved their debugging skills through iterative processes. Simulated
human feedback is only part of this model, which additionally benefits from purposely-produced
erroneous code to make more effective debugging learning and teaching, which is particularly
relevant for solving issues on platforms such as LeetCode. StarCoder2 [2] exploits a language model
fine-tuned on programming data from a large scale, which allows it to convert normal text into
code snippets with great success. The interactive feedback mechanism of describing the model
takes the user responses and revisions into account in order to improve the output, making it
more relevant and accurate. SPT Code [14] concentrates on encoding source code sequences to
learn nice representations that are utilized in code completion and translation tasks, respectively.
The two-step process is basically done by first pre-training on massive code datasets and then the
specific tasks fine-tuning is carried out to further enhance the learning and generation capabilities.
Furthermore, the last model Magicoder [22] utilizes OS code snippets through its OSS-INSTRUCT
method for the creation of realistic code instructions and outperforms many state-of-the-art ones
even with a smaller parameter size. Nevertheless, it is likely to inherit biases from its seed snippets
which can lead to the production of low-quality outputs.


   Furthermore, models like DeepSeek-Coder[7], WizardCoder [24], Mixtral [3], and Smaug [16]
are equipped with self-supervised or bootstrapped methods that are augmented with innovative
methodologies. DeepSeek-Coder is a specially configured fine-tuned model that is used for pro-
gramming tasks, it is pre-trained on a large corpus of open-source code to increase its performance
on a variety of coding tasks. Its methodology involves instruction fine-tuning with billions of
tokens to respond effectively to specific coding tasks and generate meaningful outputs. The model
is robust in predicting and completing code snippets with the help of Fill-In-the-Middle training
approach which is a method that allows the model to learn from its outputs. With a large context
window of 128K tokens, it easily tackles long coding projects. WizardCoder [24] has introduced
the Evol-Instruct method, which is the automatic generation of complex instructions. This way,
the human effort is minimized and the performance on difficult tasks is increased. Despite the fact
that it offers improvements over models like Alpaca and Vicuna, it may be lacking in some areas
when compared to ChatGPT. Mixtral [3] uses a Sparse Mixture of Experts architecture and tuning
of parameters to optimize performance by activating only some of its 47 billion parameters for

, Vol. 1, No. 1, Article . Publication date: November 2024.
A Comprehensive Survey of AI-Driven Advancements and Techniques in Automated Program Repair and Code Generation
                                                                                                             17




                             Fig. 6. Learning techniques for different AI models


inference. Thus, it acquires a unique advantage in both mathematics and code generation problems
while conserving resources. Nevertheless, the intricate nature of its structure may lead to troubles
concerning balancing the loads on several GPUs. Smaug improves the model’s performance with
the help of Direct Preference Optimization (DPO) which is a technique that refines the responses
by using pairs of outputs that are preferred and dispreferred. Its DPO-Positive approach improves
alignment and performance, though it may still struggle with preference datasets featuring low
edit distances.

Finally, models like Zephyr [4] propose a novel strategy of direct distillation transferring knowledge
from a teacher model to a student model to improve alignment with human intentions. This method-
ology is put forward zero-shot learning which enables the pupil model to generalize properly and
thus do well on tasks that are not taught to it explicitly. By collecting human feedback, Zephyr
modifies its behavior to be more interpretable which lets it be used for various language tasks.
All in all, these different methods show the ever-changing progress in AI models in programming
tasks, and this is because different training techniques give different results and performance to
the models.

7   Conclusion
In this paper, we’ve covered recent literature on the utilization of LLMs and AI in the field of
automated program repair and code generation. This paper serves to summarize and curate the
most up-to-date research on the subject and assist researchers in getting familiar with the state-of-
the-art developments in the realm of completing code-related tasks using artificial intelligence, the
use cases where this can be effective and the challenges which are currently being worked on in
this field. Furthermore, we’ve also provided comparisons among all the tools that we included in
this survey to assist in selecting the best open-source models to work on for making improvements
in other use cases which currently don’t have reliable fixes made by AI tools.

                                                           , Vol. 1, No. 1, Article . Publication date: November 2024.
18                                                            Avinash Anand, Nishchay Yadav, Akshit Gupta, Shaurya Bajaj


References
 [1] 2023. Phind-CodeLlama. Phind Technical Report (2023). https://www.phind.com/blog/code-llama-beats-gpt4
 [2] Anton Lozhko et al. 2024. StarCoder 2 and The Stack v2: The Next Generation. arXiv preprint (2024). https:
     //arxiv.org/abs/2402.19173
 [3] Albert Q. Jiang et al. 2024. Mixtral of Experts. arXiv preprint (2024). https://arxiv.org/abs/2401.04088
 [4] Lewis Tunstall et al. 2024. ZEPHYR: DIRECT DISTILLATION OF LM ALIGNMENT. arXiv preprint (2024). https:
     //arxiv.org/pdf/2310.16944
 [5] Lucy Gao. 2024. TabbyML. Online. https://github.com/TabbyML/tabby
 [6] Daya Guo, Shuo Ren, Shuai Lu, Long Zhou, Junjie Huang, Daxin Jiang, Shuming Shi, Huanbo Luan, and Ming Zhou.
     2021. GraphCodeBERT: Pre-training Code Representations with Data Flow. In International Conference on Learning
     Representations (ICLR). https://arxiv.org/abs/2009.08366
 [7] Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao Zhang, Guanting Chen, Xiao Bi, Y. Wu, Y.K. Li, Fuli
     Luo, Yingfei Xiong, and Wenfeng Liang. 2024. Deepseek-coder. arXiv preprint (2024). https://arxiv.org/abs/2401.14196
 [8] Cheryl Lee, Chunqiu Steven Xia, Jen tse Huang, Zhouruixin Zhu, Lingming Zhang, and Michael R. Lyu. 2024. A Unified
     Debugging Approach via LLM-Based Multi-Agent Synergy. arXiv preprint (2024). https://arxiv.org/pdf/2404.17153
 [9] Yi Li, Shaohua Wang, and Tien N. Nguyen. 2024. DEAR: A Novel Deep Learning-based Approach for Automated
     Program Repair. arXiv preprint (2024). https://dl.acm.org/doi/pdf/10.1145/3510003.3510177
[10] Michael R. Lyu, Baishakhi Ray, Abhik Roychoudhury, Shin Hwei Tan, and Patanamon Thongtanunam. 2024. Automatic
     Programming: Large Language Models and Beyond. arXiv preprint (2024). https://arxiv.org/pdf/2405.02213
[11] Yingwei Ma, Qingping Yang, Rongyu Cao, Binhua Li, Fei Huang, and Yongbin Li. 2024. How to Understand Whole
     Software Repository? arXiv preprint (2024). https://arxiv.org/pdf/2406.01422
[12] Ruijie Meng, Martin Mirchev, Marcel Bohme, and Abhik Roychoudhury. 2024. Large Language Model guided Protocol
     Fuzzing. arXiv preprint (2024). https://abhikrc.com/pdf/NDSS24.pdf
[13] Xiangxin Meng, Xu Wang, Hongyu Zhang, Hailong Sun, and Xudong Liu. 2024. Improving fault localization and
     program repair with deep semantic features and transferred knowledge. arXiv preprint (2024). https://dl.acm.org/doi/
     abs/10.1145/3510003.3510147
[14] Changan Niu, Chuanyi Li, Vincent Ng, Jidong Ge, Liguo Huang, and Bin Luo. 2024. SPT-Code: Sequence-to-Sequence
     Pre-Training for Learning Source Code Representations. arXiv preprint (2024). https://arxiv.org/abs/2201.01549
[15] OpenAI. 2021. Evaluating Large Language Models Trained on Code. OpenAI Technical Report (2021). https://openai.
     com/research/evaluating-large-language-models
[16] Arka Pal, Deep Karkhanis, Samuel Dooley, Manley Roberts, Siddartha Naidu, and Colin White. 2024. Smaug: Fixing
     Failure Modes of Preference Optimisation with DPO-Positive. arXiv preprint (2024). https://arxiv.org/pdf/2402.13228
[17] Haifeng Ruan, Hoang Lam Nguyen, Ridwan Shariffdeen, Yannic Noller, and Abhik Roychoudhury. 2024. Evolutionary
     Testing for Program Repair. In International Symposium on Software Testing and Analysis (ISSTA). https://abhikrc.com/
     pdf/ICST24.pdf
[18] Haifeng Ruan, Yannic Noller, Saeid Tizpaz-Niari, Sudipta Chattopadhyay, and Abhik Roychoudhury. 2024. Timing
     Side-Channel Mitigation via Automated Program Repair. 2024 International Conference on Software Engineering (ICSE)
     (2024). https://dl.acm.org/doi/pdf/10.1145/3678169
[19] Yahui Song, Xiang Gao, Wenhua Li, Wei-Ngan Chin, and Abhik Roychoudhury. 2024. ProveNFix: Temporal Property-
     Guided Program Repair. In International Conference on Software Engineering (ICSE). https://dl.acm.org/doi/pdf/10.
     1145/3643737
[20] Runchu Tian, Yining Ye, Yujia Qin, Xin Cong, Yankai Lin, Yinxu Pan, Yesai Wu, Haotian Hui, Weichuan Liu, Zhiyuan
     Liu, and Maosong Sun. 2024. Evaluating Debugging Capability of Large Language Models. arXiv preprint (2024).
     https://arxiv.org/pdf/2401.04621
[21] Yue Wang, Weishi Wang, Shafiq Joty, and Steven C.H. Hoi. 2021. CodeT5: Identifier-aware Unified Pre-trained Encoder-
     Decoder Models for Code Understanding and Generation. In Proceedings of the 2021 Conference on Empirical Methods
     in Natural Language Processing (EMNLP). https://arxiv.org/abs/2109.00859
[22] Yuxiang Wei, Zhe Wang, Jiawei Liu, Yifeng Ding, and Lingming Zhang. 2024. Magicoder: Empowering Code Generation
     with OSS-Instruct. arXiv preprint (2024). https://arxiv.org/abs/2312.02120
[23] Dylan Wolff, Zheng Shi, Gregory J. Duck, Umang Mathur, and Abhik Roychoudhury. 2024. Greybox Fuzzing for
     Concurrency Testing. In Proceedings of the 2024 ACM Conference on Computer and Communications Security (CCS).
     https://dl.acm.org/doi/pdf/10.1145/3620665.3640389
[24] Can Xu1, Qingfeng Sun, Kai Zheng, Xiubo Geng, Pu Zhao, Jiazhan Feng, Chongyang Tao, Qingwei Lin, and Daxin
     Jiang. 2024. WizardLM: Empowering Large Language Models to Follow Complex Instructions. arXiv preprint (2024).
     https://arxiv.org/abs/2304.12244
[25] Yuntong Zhang, Ridwan Shariffdeen, Gregory J. Duck, Jiaqi Tan, and Abhik Roychoudhury. 2024. Program Repair
     by Fuzzing over Patch and Input Space. In International Symposium on Software Testing and Analysis (ISSTA). https:


, Vol. 1, No. 1, Article . Publication date: November 2024.
A Comprehensive Survey of AI-Driven Advancements and Techniques in Automated Program Repair and Code Generation
                                                                                                             19


     //arxiv.org/pdf/2308.00666
[26] Tianyu Zheng, Ge Zhang, Tianhao Shen, Xueling Liu, Bill Yuchen Lin, Jie Fu, Wenhu Chen, and Xiang Yue. 2024.
     OpenCodeInterpreter: Integrating Code Generation with Execution and Refinement. arXiv preprint (2024). https:
     //arxiv.org/abs/2402.14658
[27] Li Zhong, Zilong Wang, and Jingbo Shang. 2024. Debug like a Human. In Proceedings of the 2024 ACM Conference on
     Computer and Communications Security (CCS). https://arxiv.org/pdf/2402.16906




                                                             , Vol. 1, No. 1, Article . Publication date: November 2024.

