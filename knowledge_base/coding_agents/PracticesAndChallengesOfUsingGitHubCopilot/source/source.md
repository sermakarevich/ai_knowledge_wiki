# Practices and Challenges of Using GitHub Copilot:
Source: https://arxiv.org/abs/2303.08733v3
Kind: pdf
Fetched: 2026-09-23T21:15:47.535103+00:00
Tool: pdftotext
Research-Target: /Users/sergii/.ai/knowledge/research_topics/coding_agents/research/ai_coding_best_practices
Topic: coding_agents

                                          Practices and Challenges of Using GitHub Copilot:
                                                         An Empirical Study
                                                           Beiqi Zhang†‡ , Peng Liang†‡∗ , Xiyu Zhou†‡ , Aakash Ahmad§ , Muhammad Waseem†‡
                                                                             † School of Computer Science, Wuhan University, Wuhan, China
                                                                                           ‡ Hubei Luojia Laboratory, Wuhan, China
                                                           § School of Computing and Communications, Lancaster University Leipzig, Leipzig, Germany

                                                                  {zhangbeiqi, liangp, xiyuzhou, m.waseem}whu.edu.cn, a.ahmad13@lancaster.ac.uk


                                            Abstract—With the advances in machine learning, there is a               [3]. Released on June 2021, GitHub Copilot has recently




arXiv:2303.08733v3 [cs.SE] 27 Apr 2023
                                         growing interest in AI-enabled tools for autocompleting source              emerged as an “AI pair programmer”, which is powered
                                         code. GitHub Copilot, also referred to as the “AI Pair Program-             by OpenAI Codex and suggests code or entire functions in
                                         mer”, has been trained on billions of lines of open source GitHub
                                         code, and is one of such tools that has been increasingly used since        IDEs as a plug-in [4] to help developers achieve code auto-
                                         its launch in June 2021. However, little effort has been devoted            completion in programming activities.
                                         to understanding the practices and challenges of using Copilot                 Although the emergence of AI-assisted programming tools
                                         in programming with auto-completed source code. To this end,                has empowered practitioners in their software development
                                         we conducted an empirical study by collecting and analyzing the
                                                                                                                     efforts, there is little evidence and lack of empirically-rooted
                                         data from Stack Overflow (SO) and GitHub Discussions. More
                                         specifically, we searched and manually collected 169 SO posts               studies (e.g, [3], [5], [6]) on the role of AI-assisted program-
                                         and 655 GitHub discussions related to the usage of Copilot.                 ming tools in software development. The existing studies pri-
                                         We identified the programming languages, IDEs, technologies                 marily focus on the correctness and understanding of the code
                                         used with Copilot, functions implemented, benefits, limitations,            suggested by Copilot, and little is known about the practices
                                         and challenges when using Copilot. The results show that when
                                                                                                                     and challenges of using Copilot with programming activities.
                                         practitioners use Copilot: (1) The major programming languages
                                         used with Copilot are JavaScript and Python, (2) the main IDE               To close the gap, we conducted this study that collects data
                                         used with Copilot is Visual Studio Code, (3) the most common                from Stack Overflow (SO) and GitHub Discussions to get
                                         used technology with Copilot is Node.js, (4) the leading function           practitioners’ perspectives on using Copilot during software
                                         implemented by Copilot is data processing, (5) the significant              engineering and development.
                                         benefit of using Copilot is useful code generation, and (6) the
                                         main limitation encountered by practitioners when using Copilot                The contributions of this work: (1) we identified the
                                         is difficulty of integration. Our results suggest that using Copilot is     programming languages, IDEs, and technologies used with
                                         like a double-edged sword, which requires developers to carefully           Copilot; (2) we provided the functions implemented by Copi-
                                         consider various aspects when deciding whether or not to use                lot, the benefits, limitations, and challenges of using Copilot;
                                         it. Our study provides empirically grounded foundations and                 and (3) we present the directions to be further explored.
                                         basis for future research on the role of Copilot as an AI pair
                                         programmer in software development.
                                            Keywords—GitHub Copilot, Stack Overflow, GitHub Discus-                                       II. R ELATED W ORK
                                         sions, Empirical Study
                                                                                                                        Several studies focused on the security issues of Copilot.
                                                                  I. I NTRODUCTION                                   Sandoval et al. [7] conducted a user study to investigate
                                                                                                                     the impact of programming with LLMs that support Copilot.
                                           Large Language Models (LLMs) and Machine Learning                         Their results show that LLMs have a positive impact on the
                                         (ML) for autocompleting source code are becoming more and                   correctness of functions, and they did not find any decisive
                                         more popular in software development. LLMs nowadays incor-                  impact on the correctness of safety. Several studies focused
                                         porate powerful capabilities for Natural Language Processing                on the quality of the code generated by Copilot. Imai [8]
                                         (NLP) [1], and ML approaches have been widely applied to                    compared the effectiveness of programming with Copilot
                                         source code text in a variety of new tools to support software              versus human programming, and found that the generated code
                                         development [2], which makes it possible to use LLMs to                     by Copilot is inferior than human-written code. Yetistiren et al.
                                         synthesize code in general-purpose languages [1]. Recently,                 [9] assessed the quality of generated code by Copilot in terms
                                         NLP-based code generation tools have come into the limelight,               of validity, correctness, and efficiency. Their empirical analysis
                                         with generative pre-trained language models trained on large                shows Copilot is a promising tool. Madi et al. [6] focused
                                         amounts of code in an attempt to provide reasonable auto-                   on readability and visual inspection of Copilot generated
                                         completion of the source code when programmers write code                   code. Through a human experiment, their study highlights
                                                                                                                     that programmers should beware of the code generated by
                                           This work is funded by the NSFC with Grant No. 62172311 and the Special
                                         Fund of Hubei Luojia Laboratory.                                            tools. Wang et al. [10] collected practitioners’ expectations
                                           DOI reference number: 10.18293/SEKE2023-077                               on code generation tools through a mixed-methods approach.
They found that effectiveness and code quality is more impor-                                                              TABLE I: Research Questions and their Rationales
tant than other expectations. Several studies focused on the                                                          Research Question           Rationale
                                                                                                                      RQ1: What program-          Copilot can help practitioners write less code. This
limitations and challenges in Copilot assisted programming.                                                           ming languages are used     RQ aims to collect the programming languages that
Dakhel et al. [11] explored the capabilities of Copilot through                                                       with GitHub Copilot?        developers tend to use with Copilot.
empirical evaluations, and their results suggest that Copilot                                                         RQ2: What IDEs are          Copilot is a third-party plug-in used in IDEs. This RQ
                                                                                                                      used with GitHub Copi-      aims to identify the IDEs frequently used with Copilot.
shows limitations as an assistant for developers. Nguyen and                                                          lot?                        The answers of this RQ can help developers choose
Nadi [12] conducted an empirical study to evaluate the correct-                                                                                   which IDE to use when they code with Copilot.
                                                                                                                      RQ3: What technologies      When writing code, programmers need to employ cer-
ness and comprehensibility of the code suggested by Copilot.                                                          are used with GitHub        tain technologies to complete the development. This RQ
Their findings revealed that Copilot’s suggestions for different                                                      Copilot?                    aims to investigate the technologies that can be used
                                                                                                                                                  with Copilot (e.g., frameworks), and the answers of
programming languages do not differ significantly, and they                                                                                       this RQ can help developers to choose the technologies
identified potential shortcomings of Copilot, like generating                                                                                     when they use Copilot.
                                                                                                                      RQ4: What functions are     Copilot can complete entire functions according to
complex code. Bird et al. [5] conducted three studies to                                                              implemented by using        users’ comments. This RQ aims to provide a cate-
understand how developers use Copilot and their findings                                                              GitHub Copilot?             gorization of the functions that can be implemented
                                                                                                                                                  by Copilot, and the answers of this RQ can provide
indicated that developers spent more time assessing Copilot’s                                                                                     developers guidance when implementing functions by
suggestions than doing the task by themselves. Sarkar et                                                                                          using Copilot.
                                                                                                                      RQ5: What are the ben-      Using Copilot to assist programming can bring many
al. [13] compared programming with Copilot to previous                                                                efits of using GitHub       benefits (e.g., reducing the workload of developers).
conceptualizations of programmer assistance to examine their                                                          Copilot?                    This RQ aims to collect the advantages brought to the
                                                                                                                                                  development by applying Copilot.
similarities and differences, and discussed the issues that might                                                     RQ6: What are the limi-     Although using Copilot to assist in writing code can
arise in applying LLMs to programming.                                                                                tations and challenges of   help developers with their programming activities, there
                                                                                                                      using GitHub Copilot?       are still restrictions and problems when using Copilot.
   Compared to the existing work (e.g., [9], [11]), our work                                                                                      This RQ aims to collect and identify the limitations
intends to understand the practices and challenges of Copilot                                                                                     and challenges practitioners may experience when using
                                                                                                                                                  Copilot. The answers of this RQ can help practitioners
by exploring the programming languages, IDEs, technologies                                                                                        make an informed decision when deciding whether to
used with Copilot, functions implemented by Copilot, and the                                                                                      code with the help of Copilot.
benefits, limitations, and challenges of using Copilot.
                                III. R ESEARCH D ESIGN
A. Research Questions                                                                                                community knowledge base connected with other artifacts in
  The Research Questions (RQs) and their rationale are pre-                                                          a project [14]. Therefore, we decided to use SO and GitHub
sented in Table I. The overview of the research process is                                                           Discussions as the data sources to answer our RQs, and we
shown in Figure 1 and detailed below.                                                                                conducted the searches for both SO and GitHub Discussions
                                                                                                                     on November 23rd, 2022.
          RQ1                            RQ3                                               [D1~D6: Data Items]
                                                                                          Data Extraction Template
                                                                                                                        For SO, “copilot” is used as the term to search the posts
              Programming   Development
    RQ4        Languages    Technologies           RQ6            "copilot"                                          related to Copilot. After searching, we got a total of 557 posts
                Specify Research
                                           Limitations                                                               that include the search term “copilot”. The term “copilot”
Implemented                                                 Data Collection                Data Extraction
 Functions         Questions
                                           Benefits
                                                             and Filtering                  and Analysis             may appears more than once in a post, so there may be
               Integrated Development
                                                                                       [RQ1~RQ3]      [RQ4~RQ6]      duplicates in the URL collection of these retrieved posts. After
          RQ2       Environments
                                        RQ5
                                                                        Stack Overflow
                                                                                                                     removing the duplicates, we ended up with 521 posts with
                                                         GitHub                          Descriptive Constant
                                                   [655 discussions]     [169 posts]      Statistics Comparison      unique URLs. To manually label posts related to Copilot,
                   Phase A                                    Phase B                           Phase C              we conducted a pilot data labelling by two authors with 10
                                                                                                                     retrieved SO posts. Specifically, the inclusion criterion is that
                  Fig. 1: Overview of the research process                                                           the post must provide information referring to Copilot. We
                                                                                                                     calculated the Cohen’s Kappa coefficient [15] to measure the
B. Data Collection and Filtering                                                                                     consistency of labelled posts, which is 0.773, thus indicating
                                                                                                                     a decent agreement between the two coders. After excluding
   This study focuses on understanding the practices and
                                                                                                                     the irrelevant posts in the search results, we finally got 169
challenges of using Copilot collected from SO and GitHub
                                                                                                                     Copilot related SO posts.
Discussions. SO is a popular software development commu-
nity and has been widely used by developers to ask and                                                                  For GitHub Discussions, GitHub discussions are organized
answer questions as a Q&A platform. GitHub Discussions                                                               according to categories. After exploring the categories on
is a feature of GitHub used to support the communication                                                             GitHub Discussions, we found the “Copilot” category which
among the members of a project. Different from SO, GitHub                                                            contains the feedback, questions, and conversations about
Discussions can provide various communication intentions, not                                                        Copilot [16] under the “GitHub product categories”. Since
just question-answering (e.g., a discussion can report errors or                                                     all the discussions under the “Copilot” category are related
discuss the potential development of a software project) [14],                                                       to Copilot, we then included all the discussions under the
from which the data can be complementary to the data from                                                            “Copilot” category as related discussions to extract data. The
SO. Besides, GitHub Discussions can provide a center of a                                                            number of discussions related to Copilot is 655.
C. Data Extraction and Analysis                                                    authors reached an agreement. The data analysis methods with
   1) Extract Data: To answer the RQs in Section III-A, we                         their corresponding data items and RQs are listed in Table II.
extracted the data items listed in Table II. The first and third                   The data analysis results are provided in [20].
authors conducted a pilot data extraction independently with
10 SO posts and 10 GitHub discussions randomly selected                                                     IV. R ESULTS
from the 169 SO posts and 655 GitHub discussions. The
                                                                                      This section presents the results of the study, in which the
second author was involved to discuss with the two authors
                                                                                   results of RQ1 to RQ4 are visualized in Fig 2, and the results
and came to an agreement if any disagreements were found
                                                                                   of RQ5 and RQ6 are provided in Table III and IV.
during the pilot. After the pilot, the criteria for data extraction
                                                                                   RQ1: Programming languages used with GitHub Copilot
were determined: (1) for all the data items listed in Table II,
                                                                                   Figure 2a lists the 18 programming languages used with
they will be extracted and counted only if they are explicitly
                                                                                   Copilot, in which JavaScript and Python are the most fre-
mentioned by developers that they were used with Copilot;
                                                                                   quently used ones, both accounting for one fifth. Besides,
(2) if the same developer repeatedly mentioned the same data
                                                                                   developers often write C# and Java code when using Copilot,
item in an SO post or a GitHub discussion, we only counted
                                                                                   as one practitioner mentioned “the GitHub Copilot extension
it once. In a post or discussion, multiple developers may
                                                                                   is enabled in my VS 2022 C# environment” (GitHub #14115).
mention Copilot related data items, resulting in situation that
                                                                                   TypeScript, Rust, PHP, C, Golang, and Kotlin were used with
the total number of instances of certain data item extracted
                                                                                   Copilot between 3˜8 times each (1.7% to 8.4%). The rest
may be greater than the number of posts and discussions. The
                                                                                   programming languages (e.g., Perl and Ruby), which are not
first and third authors further extracted the data items from
                                                                                   popular, were mentioned only once with Copilot.
the filtered posts and discussions according to the extraction
criteria, marked uncertain parts, and discussed with the second                    RQ2: IDEs used with GitHub Copilot
author to reach a consensus. Finally, the first author rechecked                   Figure 2b shows 22 types of IDEs that are used with Copilot.
all the extraction results by the two authors from the filtered                    Visual Studio Code is the dominant IDE, accounting for 46.0%.
posts and discussions to ensure the correctness of the extracted                   When first released, Copilot only worked with Visual Studio
data.                                                                              Code editor, and it is expected that Visual Studio Code is the
                                                                                   IDE most often used with Copilot. Mainstream code editors,
TABLE II: Data items extracted with their corresponding RQs                        including Visual Studio, IntelliJ IDEA, NeoVim, and PyCharm
and analysis methods                                                               are also occasionally used, account for 39.9% in total. The
 #    Data Item        Description                         Analysis          RQ    remaining IDEs were rarely mentioned by developers, and one
                                                           Method                  possible reason is that there are often integration issues when
 D1   Programming      Programming language used           Descriptive       RQ1
      language         with Copilot                        statistics [17]         using Copilot within them according to the results of RQ6.
 D2   IDE              IDEs used with Copilot              Descriptive       RQ2   RQ3: Technologies used with GitHub Copilot
                                                           statistics
 D3   Technology       Technologies used with Copilot      Descriptive       RQ3   Figure 2c presents 22 technologies used with Copilot. We find
                                                           statistics              that these identified technologies include frameworks, APIs,
 D4   Function         Functions implemented by            Constant          RQ4
                       Copilot                             comparison              and libraries. Node.js, whose proportion is more than 40%, is
 D5   Benefit          Benefits brought by using Copi-     Constant          RQ5   one of the most popular back-end runtime environments for
                       lot                                 comparison
 D6   Limitation and   The restrictions and difficulties   Constant          RQ6
                                                                                   JavaScript, which is also the most frequently used language
      Challenge        when using Copilot                  comparison              with Copilot (see the results of RQ1), thus it is reasonable that
                                                                                   Node.js is the major technology used with Copilot. In addition,
   2) Analyze Data: For RQ1, RQ2, and RQ3, we used                                 .NET which works for Web development, and Vue, React,
descriptive statistics [17] to analyze and present the results.                    and Ajax which are frameworks for front-end development,
For RQ4, RQ5, and RQ6, we conducted a qualitative data                             were mentioned less often compared to Node.js. The rest of
analysis by applying the Constant Comparison method [18].                          the identified technologies, many of which relate to machine
We constantly compared each part of the data (e.g., emergent                       learning (e.g., Pandas, Dlib, and OpenCV) or front-end devel-
codes) to explore differences and similarities in the extracted                    opment (e.g., Htmx, Vanilla JS, and Next.js), are rarely used
data to form categories [19]. Note that for answering RQ4,                         with Copilot, and each of them appears only once.
we categorized the functions (D4) based on developers’ discus-                     RQ4: Functions implemented by using GitHub Copilot
sions, i.e., developers’ descriptions of the mentioned functions.                  Figure 2d shows 14 functions implemented by using Copilot.
Firstly, the first and the third authors coded the filtered posts                  The main function implemented by Copilot is data processing,
and discussions with the corresponding data items listed (see                      indicating that developers tend to make use of Copilot to
Table II). Secondly, the first author reviewed the coded data                      write functions working with data. Besides, Front-end element
by the third author to make sure the extracted data were coded                     control, string processing, and Test account for the same,
correctly. Finally, the first author combined all the codes into                   i.e., 11.1%. When implementing functions, developers also
higher-level concepts and turned them into categories. After                       use Copilot to code image processing, algorithm, iteration,
that, the second author examined the coding and categorization                     calculation, filtering, printing, memory read, serialization, and
results, in which any divergence was discussed till the three                      URL building, which range from 2.2% to 8.9%.
                                                                                                                                  Android Studio
                                                                                                                                     (0.9%) CLion Jupyter Notebook
                                                           Rust TypeScript                                                   GoLand Vim       (0.9%)   (0.9%)   Eclipse (0.2%)
                                                     Ruby (3.4%) (4.5%)                                                       (1.3%) (1.1%)                     RubyMine (0.2%)
                                                    (0.6%)            C                                   VSCodium (1.3%)                                                                                                                               Emacs (0.2%)
                                                  R
                                               (0.6%)              (2.8%)                                                                                                                                                                               Code-OSS (0.2%)
                                                                                                                      Rider (1.5%)                                                                                                                      NV Access (0.2%)
                                                                                            C#                   WebStorm
                                     Python                                                                                                                                                                                                             Sublime Text (0.2%)
                                                                                          (12.8%)                 (2.0%)
                                     (20.1%)                                     rip
                                                                                    t                                                                                                                                                                   Google Colab (0.2%)
                                                                         n   aS
                                                                                c                                   PhpStorm                                                                                                                            DataSpell (0.2%)
                                                                      tho Jav                                                                                               Visual Studio Code
                                                                   Py                                                 (2.6%)
                                                                                               C++                                                                                                                                                       Visual Studio
                                                                   #
                                                                                                                   PyCharm
                                                              va   C
                             PHP (2.8%)                 ++
                                                             Ja
                                                                                              (8.4%)                                                    Visual Studio
                                                                                                                                                                                                                               most used                     Code
                                                        C
                                                                                                                    (8.5%)                         Intellij IDEA
                             Perl (0.6%)                                                          Dart                                           NeoVim
                                                                                                                                                                                                                                (top 5)                     (46.0%)
                              Nim (0.6%)                                                         (0.6%)                     NeoVim          PyCharm
                                                     （%）
                              Lua (0.6%)                       2 .8 1 7                        Golang                        (8.8%)          （%）
                                                        8.4 11. 12 20. 20.
                                 Kotlin                      most used                          (2.2%)                                            8.5 8.8 9.9 12.746.0
                                 (1.7%)                        (top 5)
                                                                                          HTML+CSS                          IntelliJ IDEA
                                                                                            (6.1%)                             (9.9%)
                                          JavaScript                              Java                                                                                                                                                           Visual Studio
                                           (20.7%)                              (11.2%)                                                                                                                                                             (12.7%)

                                     (a) RQ1: Programming Languages                                             (b) RQ2: Integreted Development Environments

                                                     Vanilla JS                                                                             URL building Algorithm
                                             Three.js (1.7%)                                                               Text processing      (2.2%)                 (6.7%)
                                                                Vue    (6.7%)                                                    (4.4%)                                    Calculation
                                     Spring (1.7%)
                                                                             .Net (15.0%)                                                                                     (4.4%)
                              Framework (1.7%)
                                  React (5.0%)                                                                            Test (11.1%)




                                                                                                                                                                        Front-end element control
                             PyTorch (1.7%)                          Node.js
                                                                                      Ajax (3.3%)                                                                             Data processing
                               Pandas                                                                                                                                              (26.7%)
                                                                                         Data build tool (1.7%) String processing


                                                                                                                                                     Image processing                                      String processing
                                (1.7%)


                                                                                                                                                                                                                               Data processing
                                                      most used                           Dlib (1.7%)                 (11.1%)
                                 OpenCV                 (top 5)                           Doom (1.7%)
                                  (1.7%)                          .Net
                                                                                           Flutter (1.7%)        Serialization
                                                                Vue
                                                                                          GraphQL    (1.7%)                                                                                         Test
                                                      Ajax
                                                           React                                                     (2.2%)                 （%）
                                                                                          gRPC (1.7%)                                                                7
                                                  （%）                                     Htmx (1.7%)                 Printing                 8.9 11.1 11.111.1 26.
                                                                                                                                              most implemented
                                                       3.3 5.0 6.7 15.0 41.7            Jinja (1.7%)                   (2.2%)
                                      Node.js                                                                                                        (top 5)
                                                                                      LibTorch (1.7%)            Memory read                                                  Filtering
                                      (41.7%)                                       MongoDB (1.7%)                    (2.2%)                                                   (2.2%)
                                                                                  Next.js (1.7%)
                                                                                                                  Iteration (4.4%)
                                                                                                                                     Image processing           Front-end element control
                                                                                                                                          (8.9%)                             (11.1%)

                                    (c) RQ3: Development Technologies                                                        (d) RQ4: Implemented Functions


 Fig. 2: Programming languages, IDEs, technologies, and implemented functions of using Copilot (results of RQ1 to RQ4)

                                                        TABLE III: Benefits of using Copilot (results of RQ5)
 Benefit                               Example                                                                                                                                                                                                                                Count    %
 Useful code generation                I find myself writing a lot of tests, and Copilot is excellent at helping with writing repetitive tests (GitHub #9282)                                                                                                                  24     49.0%
 Faster development                    I really enjoy using it , it reduce programming time (GitHub #17382)                                                                                                                                                                     8     16.3%
 Better code quality                   it’s faster and simpler to your solution (SO #68418725)                                                                                                                                                                                  5     10.2%
 Good adaptation to users’ code        GitHub copilot adapt to your coding practices (SO #69740880)                                                                                                                                                                             3     6.1%
 patterns
 Better user experience                Since copilot works totally different compared to all the other products out there, it is a lot more fun to use and does                                                                                                                3      6.1%
                                       not annoy me like some other AI systems (GitHub #7254)
 Powerful code interpretation and      Does Copilot have the code explanation feature or something similar? It does! some active members were given beta                                                                                                                       2      4.1%
 conversion functions                  access. (GitHub #38089)
 Frequent updates to provide           Keep in mind that there are updates to the plugin very frequently, so there’s still hope (SO #70428218)                                                                                                                                 1      2.0%
 more features
 Free for students                     If you are a student you can sign up for the GitHub Student Pack, which gives a lot of benefits, one being copilot for                                                                                                                  1      2.0%
                                       free (GitHub #31494)
 Strong integration capability         GitHub is supporting more editors (GitHub #6858)                                                                                                                                                                                        1      2.0%
 Ease of study and use                 when using this plugin, can study at a relatively low cost (GitHub #8028)                                                                                                                                                               1      2.0%



RQ5: Benefits of using GitHub Copilot                                                                             than other AI-assisted programming tools, for example, one
Table III highlights 10 benefits of using Copilot. Most de-                                                       developer stated that “Copilot works totally different compared
velopers mentioned that they used Copilot for useful code                                                         to all the other products out there, it is a lot more fun to use
generation, which reduced their workload and gave them help                                                       and does not annoy me like some other AI systems” (GitHub
when they have no idea about how to write code. Programming                                                       #7254), without providing the names of the other products.
with Copilot also brings faster development, as one discussion                                                    RQ6: Limitations and challenges of using GitHub Copilot
remarked, Copilot “saves developers a lot of time” (GitHub                                                        Table IV lists 15 limitations and challenges of using Copilot.
#35850). Meanwhile, better code quality can be obtained by                                                        Most developers pointed out the difficulty of integration be-
using Copilot. Compared to the code written by developers                                                         tween Copilot and IDEs or other plug-ins. After Copilot was
themselves, the code suggested by Copilot is usually shorter                                                      installed in developers’ IDEs, certain plug-ins did not work
and more correct, as one developer said, “often Copilot is                                                        and Copilot may conflict with some shortcut settings of the
smarter than me” (SO #74512186). Copilot can use machine                                                          editors. Moreover, Copilot cannot be successfully integrated
learning models to learn code style of developers, so as to offer                                                 with some IDEs as Copilot does not support these editors
good adaptation to users’ code patterns. Three developers                                                         yet. Due to the instability of Copilot servers, developers may
mentioned that Copilot can give them better user experience                                                       have difficulties of accessing Copilot. The code suggested by
                                  TABLE IV: Limitations and challenges of using Copilot (results of RQ6)
 Limitation & Challenge          Example                                                                                                                      Count    %
 Difficulty of integration       Copilot only works with VSCode, VSCodium is not supported at the moment (GitHub #14837)                                       75     28.0%
 Difficulty of accessing Copi-   I cannot connect to the GitHub account and the Copilot server in VSCode, also cannot use the Copilot plugin (SO               47     17.5%
 lot                             #74398521)
 Limitation to code generation   Copilot is limited to around 1000 characters in the response (GitHub #15122)                                                  39     14.6%
 Poor quality of generated       Github Copilot suggest solutions that don’t work (SO #73701039)                                                               31     11.6%
 code
 Code privacy threat             Copilot does collect personal data so just take precaution when working in private repos (GitHub #7163)                       20     7.5%
 Unfriendly user experience      I had the same problem today, an amazing tool with poor user experience (GitHub #8468)                                        14     5.2%
 High pricing                    it is obvious that no one in South America will pay that price, it is too expensive (GitHub #24594)                           11     4.1%
 Difficulty of understanding     I really do not understand this enough, and have no idea half of what this code does honestly. It was written by Copilot.      9     3.4%
 the generated code              (SO #72282605)
 No edition for organizations    Currently, Copilot is only available for individual user accounts and organizations aren’t able to purchase/manage Copilot    7      2.7%
                                 for their members just yet (GitHub #32775)
 Lack of customization           My question is about setting up shortcuts in Visual Studio Code VSCode for GitHub Copilot Labs. (SO #73564811)                5      1.9%
 Difficulty of subscription      My copilot subscription suddenly stopped. Tried log out and in. Never have reply on support ticket over 10 days (GitHub       3      1.1%
                                 #36190)
 Challenge of not providing      making sure that the tool does not provide outdated suggestions would still be a challenge (SO #72554382)                     2      0.7%
 outdated suggestions
 Show loading                    I am not sure what is causing this but while editing files within Visual Studio, I am periodically locking up with the        2      0.7%
                                 following dialog showing (SO #73682137)
 Hard to configure               Keep getting ”Your Copilot experience is not fully configured, complete your setup” in Visual Studio 2022 (GitHub #19556)     2      0.7%
 Need of basic programming       It is useless if you do not understand the programming language or the task you want to do (GitHub #35850)                    1      0.4%
 knowledge



Copilot has restrictions as well, and sometimes it just offers                           Besides, Copilot may consider improving the integration of
few solutions, which are not enough for users, which brings                              Copilot by supporting more IDEs in the future.
limitation to code generation, as one developer said “multiple                              Support for Front-end and Machine Learning Develop-
solution is too little” (GitHub #37304). Practitioners also com-                         ment: As we can see from the results of RQ1, RQ3, and RQ4,
plained about the poor quality of generated code by Copilot.                             practitioners often write JavaScript and Python code when
Some practitioners said that “GitHub Copilot suggest solutions                           using Copilot, and they tend to use Copilot with front-end and
that don’t work” (SO #73701039), and some practitioners                                  machine learning related technologies (including frameworks,
found that when the code files became larger, the quality of the                         APIs, and libraries) to implement front-end (e.g., front-end
code suggested by Copilot “becomes unacceptable” (GitHub                                 element control) and machine learning functions (e.g., data
#9282). When using Copilot, developers pay much attention                                processing and image processing). JavaScript is the foundation
to code privacy threat as well. They were worried that Copilot                           language of many popular front-end frameworks and most of
may use their code information without permission. Contrary                              Websites use JavaScript on the client side. Python is the first
to the developers who mentioned that Copilot gave them a                                 choice when it comes to the development of machine learning
better user experience than other AI-assisted programming                                solutions with the help of rich libraries, e.g., OpenCV. It is
tools, some practitioners said they had an unfriendly user                               consequently reasonable that developers tend to use Copilot
experience when coding with Copilot.                                                     with JavaScript to facilitate and generate code for front-end
                                                                                         and Python for machine learning development.
                              V. I MPLICATIONS
                                                                                            Potentials and Perils of Using Copilot in Software
   Integration of Copilot with IDEs: According to the results                            Development: Trained on billions of lines of code, Copilot
of RQ2 and RQ6, we found that most developers choose to                                  can turn natural language prompts into coding suggestions
integrate the Copilot plug-in in mainstream IDEs (including                              across dozens of programming languages and make developers
Visual Studio Code, Visual Studio, IntelliJ IDEA, NeoVim,                                code faster and easier [4]. The results of RQ5 and RQ6 show
and PyCharm), and the percentage of mainstream IDEs used                                 that many benefits of using Copilot contradict its limitations
with Copilot by practitioners reaches 85.9%. When developers                             and challenges, e.g., useful code generation vs. limitation to
choose the lesser known IDEs (e.g., Sublime Text), they often                            code generation. When deciding to use Copilot, developers
find it hard to integrate the Copilot plug-in and thus have                              should consider tool integration, user experience, budget, code
difficulty of integration. In addition to the reason that devel-                         privacy, and some other aspects, and make trade-offs between
opers may install Copilot in their chosen IDEs incorrectly,                              these factors. In short, using Copilot is like a double-edged
another reason for the difficulty of integration is that Copilot                         sword, and practitioners need to consider various aspects
does not support certain IDEs at the moment. When developers                             carefully when deciding whether or not to use it. If Copilot can
choose to use Copilot in mainstream IDEs, they can install it                            be used with appropriate programming languages and tech-
smoothly, and even if problems arise during the installation                             nologies to implement functions required by users correctly in
or use, they can easily find a solution on SO or GitHub                                  developers’ IDEs, it will certainly optimize developers’ coding
Discussions as many other developers may have encountered                                workflow and do what matters most - building software by
similar issues. To reduce the difficulty of integration, we                              letting AI do the redundant work. Otherwise, it will bring
recommend practitioners to use mainstream IDEs with Copilot.                             difficulties and restrictions to development, making developers
feel frustrated and constrained. The study results can help        GitHub Discussions. Finally, we got 169 SO posts and 655
practitioners being aware of the potential advantages and          GitHub discussions related to Copilot. Our results identified
disadvantages of using Copilot and thus make an informed           the programming languages, IDEs, technologies used with
decision whether to use it for programming activities.             Copilot, functions implemented by Copilot, and the benefits,
   Towards an Effective Use of Copilot: Further investigation      limitations, and challenges of using Copilot, which are first-
about the practices of Copilot can be conducted by question-       hand information for developers.
naire and interview. Under what conditions the challenges of          In the next step, we plan to further explore when to use
using Copilot will show up as advantages or disadvantages,         Copilot, for what specific purposes, and by whom, which helps
and how to use Copilot to convert its disadvantages into ad-       to guide towards an effective use of Copilot.
vantages are also worth further exploration. Besides, although
                                                                                                 R EFERENCES
we have investigated various aspects of using Copilot (e.g.,
limitations and challenges), we have not looked in depth at         [1] J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan,
                                                                        E. Jiang, C. Cai, M. Terry, Q. Le et al., “Program synthesis with large
what types of users (e.g., developers, educators, and students)         language models,” arXiv preprint abs/2108.07732, 2021.
who use Copilot, when and how they use Copilot, and for what        [2] M. Allamanis, E. T. Barr, P. Devanbu, and C. Sutton, “A survey
specific purposes. By exploring these aspects, researchers can          of machine learning for big code and naturalness,” arXiv preprint
                                                                        abs/1709.06182, 2018.
get meaningful information which would help guide towards           [3] H. Pearce, B. Ahmad, B. Tan, B. Dolan-Gavitt, and R. Karri, “An em-
an effective use of Copilot.                                            pirical cybersecurity evaluation of github copilot’s code contributions,”
                                                                        arXiv preprint abs/2108.09293, 2021.
                 VI. T HREATS TO VALIDITY                           [4] GitHub Copilot · Your AI pair programmer, https://github.com/features/
                                                                        copilot.
   Construct validity: We conducted data labelling, extrac-         [5] C. Bird, D. Ford, T. Zimmermann, N. Forsgren, E. Kalliamvakou,
tion, and analysis manually, which may lead to personal bias.           T. Lowdermilk, and I. Gazit, “Taking flight with copilot: Early insights
                                                                        and opportunities of ai-powered pair-programming tools,” ACM Queue,
To reduce this threat, the data labelling of SO posts was               vol. 20, no. 6, pp. 35—-57, 2023.
performed after the pilot labelling to reach an agreement           [6] N. Al Madi, “How readable is model-generated code? examining read-
between the authors. The data extraction and analysis was also          ability and visual inspection of github copilot,” in Proc. of the 37th
                                                                        International Conference on Automated Software Engineering (ASE).
conducted by two authors, and the first author rechecked all the        ACM, 2023, pp. 1–5.
results produced by the third author. During the whole process,     [7] G. Sandoval, H. Pearce, T. Nys, R. Karri, B. Dolan-Gavitt, and S. Garg,
the first author continuously consulted with the second author          “Security implications of large language model code assistants: A user
                                                                        study,” arXiv preprint abs/2208.09727, 2022.
to ensure there are no divergences.                                 [8] S. Imai, “Is github copilot a substitute for human pair-programming?
   External validity: We chose two popular developer com-               an empirical study,” in Proc. of the 44th International Conference
munities (SO and GitHub Discussions) because SO has been                on Software Engineering: Companion Proceedings (ICSE-Companion).
                                                                        IEEE, 2022, pp. 319–321.
widely used in software engineering studies and GitHub Dis-         [9] B. Yetistiren, I. Ozsoy, and E. Tuzun, “Assessing the quality of github
cussions is a new feature of GitHub for discussing specific             copilot’s code generation,” in Proc. of the 18th International Conference
topics [14]. These two data sources can partially alleviate the         on Predictive Models and Data Analytics in Software Engineering
                                                                        (PROMISE). ACM, 2022, pp. 62–71.
threat to external validity. However, we admit that our selected   [10] C. Wang, J. Hu, C. Gao, Y. Jin, T. Xie, H. Huang, Z. Lei, and
data sources may not be representative enough to understand             Y. Deng, “Practitioners’ expectations on code completion,” arXiv
all the practices and challenges of using Copilot.                      preprint abs/2301.03846, 2023.
                                                                   [11] A. M. Dakhel, V. Majdinasab, A. Nikanjam, F. Khomh, M. C. Desmarais,
   Reliability: We conducted a pilot labelling before the for-          Z. Ming, and Jiang, “Github copilot ai pair programmer: Asset or
mal labelling of SO posts with two authors, and the Cohen’s             liability?” arXiv preprint abs/2206.15331, 2022.
Kappa coefficient is 0.773, indicating a decent consistency.       [12] N. Nguyen and S. Nadi, “An empirical evaluation of github copilot’s
                                                                        code suggestions,” in Proc. of the 19th IEEE/ACM International Con-
We acknowledge that this threat might still exist due to the            ference on Mining Software Repositories (MSR). IEEE, 2022, pp. 1–5.
small number of posts used in the pilot. All the steps in our      [13] A. Sarkar, A. D. Gordon, C. Negreanu, C. Poelitz, S. S. Ragavan, and
study, including manual labelling, extraction, and analysis of          B. Zorn, “What is it like to program with artificial intelligence?” arXiv
                                                                        preprint abs/2208.06213, 2022.
data were conducted by three authors. During the process,          [14] H. Hata, N. Novielli, S. Baltes, R. G. Kula, and C. Treude, “Github
the three authors discussed the results until there was no              discussions: An exploratory study of early adoption,” Empirical Software
any disagreements in order to produce consistent results.               Engineering, vol. 27, no. 1, pp. 1–32, 2022.
                                                                   [15] J. Cohen, “A coefficient of agreement for nominal scales,” Educational
In addition, the dataset of this study that contains all the            and Psychological Measurement, vol. 20, no. 1, pp. 37–46, 1960.
extracted data and labelling results from the SO posts and         [16] GitHub Discussions: Copilot Category, https://github.com/community/
GitHub discussions has been provided online for validation              community/discussions/categories/copilot.
                                                                   [17] A. N. Christopher, Interpreting and Using Statistics in Psychological
and replication purposes [20].                                          Research. SAGE Publications, 2017.
                                                                   [18] B. G. Glaser, “The constant comparative method of qualitative analysis,”
                     VII. C ONCLUSIONS                                  Social Problems, vol. 12, no. 4, pp. 436–445, 1965.
                                                                   [19] L. R. Hallberg, “The “core category” of grounded theory: Making
  We conducted an empirical study on SO and GitHub Dis-                 constant comparisons,” International Journal of Qualitative Studies on
cussions to understand the practices and challenges of using            Health and Well-being, vol. 1, no. 3, pp. 141–148, 2006.
GitHub Copilot from the practitioners’ perspective. We used        [20] B. Zhang, P. Liang, X. Zhou, A. Ahmad, and M. Waseem, Dataset
                                                                        of the Paper: Practices and Challenges of Using GitHub Copilot: An
“copilot” as the search term to collect data from SO and                Empirical Study, 2023, https://doi.org/10.5281/zenodo.7604508.
collected all the discussions under the “Copilot” category in

