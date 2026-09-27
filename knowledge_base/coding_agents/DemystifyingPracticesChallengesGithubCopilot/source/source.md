# September 13, 2023     1:2   WSPC/INSTRUCTION FILE                     ws-ijseke
Source: https://arxiv.org/abs/2309.05687v1
Kind: pdf
Fetched: 2026-09-23T19:53:48.542919+00:00
Tool: pdftotext
Research-Target: /Users/sergii/.ai/knowledge/research_topics/coding_agents/research/ai_coding_best_practices
Topic: coding_agents

                                         September 13, 2023     1:2   WSPC/INSTRUCTION FILE                     ws-ijseke




                                               International Journal of Software Engineering and Knowledge Engineering
                                               © World Scientific Publishing Company




arXiv:2309.05687v1 [cs.SE] 11 Sep 2023
                                                 Demystifying Practices, Challenges and Expected Features of Using
                                                                          GitHub Copilot


                                                                             Beiqi Zhang, Peng Liang,∗ Xiyu Zhou
                                                          School of Computer Science, Hubei Luojia Laboratory, Wuhan University
                                                                                  Wuhan 430072, China
                                                                        {zhangbeiqi, liangp, xiyuzhou}@whu.edu.cn

                                                                                        Aakash Ahmad
                                                          School of Computing and Communications, Lancaster University Leipzig
                                                                                Leipzig 04109, Germany
                                                                               a.ahmad13@lancaster.ac.uk

                                                                                     Muhammad Waseem
                                                          School of Computer Science, Hubei Luojia Laboratory, Wuhan University
                                                                                  Wuhan 430072, China
                                                                                  m.waseem@whu.edu.cn


                                                                                 Received Day Month Year)
                                                                                 Revised (Day Month Year)
                                                                                 Accepted (Day Month Year)


                                                   With the advances in machine learning, there is a growing interest in AI-enabled tools
                                                   for autocompleting source code. GitHub Copilot, also referred to as the “AI Pair Pro-
                                                   grammer”, has been trained on billions of lines of open source GitHub code, and is one
                                                   of such tools that has been increasingly used since its launch in June 2021. However,
                                                   little effort has been devoted to understanding the practices, challenges, and expected
                                                   features of using Copilot in programming for auto-completed source code from the point
                                                   of view of practitioners. To this end, we conducted an empirical study by collecting and
                                                   analyzing the data from Stack Overflow (SO) and GitHub Discussions. More specifically,
                                                   we searched and manually collected 303 SO posts and 927 GitHub discussions related to
                                                   the usage of Copilot. We identified the programming languages, Integrated Development
                                                   Environments (IDEs), technologies used with Copilot, functions implemented, benefits,
                                                   limitations, and challenges when using Copilot. The results show that when practition-
                                                   ers use Copilot: (1) The major programming languages used with Copilot are JavaScript
                                                   and Python, (2) the main IDE used with Copilot is Visual Studio Code, (3) the most
                                                   common used technology with Copilot is Node.js, (4) the leading function implemented
                                                   by Copilot is data processing, (5) the main purpose of users using Copilot is to help
                                                   generate code, (6) the significant benefit of using Copilot is useful code generation, (7)
                                                   the main limitation encountered by practitioners when using Copilot is difficulty of in-
                                                   tegration, and (8) the most common expected feature is that Copilot can be integrated
                                                   with more IDEs. Our results suggest that using Copilot is like a double-edged sword,

                                               ∗ Corresponding author.



                                                                                               1
September 13, 2023     1:2      WSPC/INSTRUCTION FILE                   ws-ijseke




          2   B. Zhang et al.


               which requires developers to carefully consider various aspects when deciding whether
               or not to use it. Our study provides empirically grounded foundations that could inform
               software developers and practitioners, as well as provide a basis for future investigations
               on the role of Copilot as an AI pair programmer in software development.

               Keywords: GitHub Copilot, Stack Overflow, GitHub Discussions, Repository Mining


          1. Introduction
          Large Language Models (LLMs) and Machine Learning (ML) for autocompleting
          source code are becoming more and more popular in software development. LLMs
          nowadays incorporate powerful capabilities for Natural Language Processing (NLP)
          [1], and ML approaches have been widely applied to source code using a variety
          of new tools to support software development [2], which makes it possible to use
          LLMs to synthesize code in general-purpose languages [1]. Recently, NLP-based
          code generation tools have come into the limelight, with generative pre-trained
          language models trained on large corpus of code in an attempt to provide reasonable
          auto-completion of the source code when programmers write code [3]. Released in
          June 2021, GitHub Copilot has recently emerged as an “AI pair programmer”,
          which is powered by OpenAI Codex and suggests code or entire functions in IDEs
          as a plug-in [4] to help developers achieve code auto-completion in development.
              Although the emergence of AI-assisted programming tools has empowered prac-
          titioners in their software development efforts, there is little evidence and lack of
          empirically-rooted studies (e.g, [3], [5], [6]) on the role of AI-assisted programming
          tools in software development. The existing studies such as [7] and [8] primarily focus
          on the correctness and understanding of the code suggested by Copilot, and little is
          known about the practices, challenges, and expected features of using Copilot dur-
          ing programming and software development activities for the developers and users
          of Copilot. To ameliorate this gap, we conducted this study that collects data
          from Stack Overflow (SO) and GitHub Discussions to get practitioners’ perspec-
          tives on using Copilot during software development. While Bird et al. investigated
          Copilot users’ initial experiences of how they would use Copilot, as well as what
          challenges they encountered by three studies [5], our study explored the practices,
          challenges, and expected features of using Copilot by analyzing the data from de-
          veloper communities. The emergence of Copilot has shifted the paradigm of pair
          programming, and it is challenging for software development teams to adopt this
          approach and tool on a large scale [5]. Our work intends to provide developers and
          users of GitHub Copilot with comprehensive insights on the practices, purposes,
          and expected features of using Copilot.
              The contributions of this work: (1) we identified the programming lan-
          guages, IDEs, and technologies used with Copilot; (2) we provided the functions im-
          plemented by Copilot, the purposes, benefits, limitations/challenges, and expected
          features of using Copilot; and (3) we collected and added more data related to
          Copilot from SO and GitHub Discussions (134 posts and 272 discussions, leading
          to 303 posts and 927 discussions in total) for purposes of enhancing the external
September 13, 2023   1:2   WSPC/INSTRUCTION FILE                  ws-ijseke




                  Demystifying Practices, Challenges and Expected Features of Using GitHub Copilot   3


          validity of our study results.
              This paper is an extension of our previous conference paper [9] published in
          the Proceedings of the 35th International Conference on Software Engineering and
          Knowledge Engineering (SEKE 2023), and the following additions show how we
          extended the previous work: (1) we extended our dataset by including the latest
          data from Stack Overflow and GitHub Discussions formulated before June 18th,
          2023 (303 SO posts and 927 GitHub discussions in total); we explored and reported
          the purposes of using GitHub Copilot in RQ1.4; (3) we investigated and reported the
          expected features of users about GitHub Copilot from practitioners’ perspectives in
          RQ2.3; and (4) we provide more implications based on the study results.
              The structure of the paper: Section 2 surveys the related work, and Section 3
          presents the research design of this study. Section 4 provides the study results, which
          are further discussed in Section 5. The potential threats to validity are clarified in
          Section 6 and Section 7 concludes this work with future directions.


          2. Related Work
          2.1. Analyzing the Code Generated Using Copilot
          Several studies focused on the security issues of Copilot. Sandoval et al. [10] con-
          ducted a user study to investigate the impact of programming with LLMs that
          support Copilot. Their results show that LLMs have a positive impact on the cor-
          rectness of functions, and they did not find any decisive impact on the correctness
          of safety. Several studies focused on the quality of the code generated by Copi-
          lot. Imai [11] compared the effectiveness of programming with Copilot versus hu-
          man programming, and found that the generated code by Copilot is inferior than
          human-written code. Yetistiren et al. [8] assessed the quality of generated code by
          Copilot in terms of validity, correctness, and efficiency. Their empirical analysis
          shows Copilot is a promising tool. Madi et al. [6] focused on readability and visual
          inspection of Copilot generated code. Through a human experiment, their study
          highlights that programmers should beware of the code generated by tools. Wang
          et al. [12] collected practitioners’ expectations on code generation tools through a
          mixed-methods approach. They found that effectiveness and code quality is more
          important than other expectations. Several studies focused on the limitations and
          challenges in Copilot assisted programming.


          2.2. Capabilities and Limitations of Copilot
          Several studies have explored the capabilities and limitations of GitHub Copilot.
          Dakhel et al. [13] explored Copilot’s capabilities through empirical evaluations, and
          their results suggest that Copilot shows limitations as an assistant for develop-
          ers. Nguyen and Nadi [14] conducted an empirical study to evaluate the correctness
          and comprehensibility of the code suggested by Copilot. Their findings revealed that
          Copilot’s suggestions for different programming languages do not differ significantly,
September 13, 2023     1:2      WSPC/INSTRUCTION FILE           ws-ijseke




          4   B. Zhang et al.


          and they identified potential shortcomings of Copilot, like generating complex code.
          Bird et al. [5] conducted three studies to understand how developers use Copilot
          and their findings indicated that developers spent more time assessing suggestions
          by Copilot than doing the task by themselves. Sarkar et al. [15] compared pro-
          gramming with Copilot to previous conceptualizations of programmer assistance to
          examine their similarities and differences, and discussed the issues that might arise
          in applying LLMs to programming.
              Compared to the existing work (e.g., [8], [13]), our work intends to understand
          the practices, challenges, and expected features of using Copilot by exploring various
          aspects of Copilot’s usage.


          3. Research Design
          The goal of this study is to understand the practices, benefits and challenges, and
          expected features of using GitHub Copilot from the point of view of practitioners in
          the context of Copilot related SO posts and GitHub discussions. We conducted and
          reported this exploratory study by following the guidelines for empirical studies in
          software engine ring proposed in [16]. We formulated two Research Questions (RQs)
          with eight sub-RQs that contribute to the goal of this study, as presented in Section
          3.1 with their rationale. The overview of the research process is shown in Figure 1
          and detailed in Section 3.2 and Section 3.3.




                                   Fig. 1: Overview of the research process




          3.1. Phase A - Outlining the Research Questions
          We aimed to explore the characteristics of practices, challenges, and expected fea-
          tures of using GitHub Copilot by answering the RQs in the following:
          RQ1: Programming Languages, IDEs, Technologies, Functions, and Pur-
          poses of Using GitHub Copilot
          RQ1.1: What programming languages are used with GitHub Copilot?
September 13, 2023   1:2   WSPC/INSTRUCTION FILE                  ws-ijseke




                  Demystifying Practices, Challenges and Expected Features of Using GitHub Copilot   5


          Rationale: In software development, the role of programming languages is funda-
          mental - enabling programmers to translate requirements by writing source code
          using a specific programming language such as Java or Python. This RQ aims to
          collect the programming languages that developers tend to use with Copilot.
          RQ1.2: What IDEs are used with GitHub Copilot?
          Rationale: Copilot is a third-party plug-in used in IDEs. This RQ aims to identify
          the IDEs frequently used with Copilot. The answers of this RQ can help developers
          choose which IDE to use when they code with Copilot.
          RQ1.3: What technologies are used with GitHub Copilot?
          Rationale: When writing code, programmers need to employ certain technologies
          to complete the development. This RQ aims to investigate the technologies that
          can be used with Copilot (e.g., frameworks), and the answers of this RQ can help
          developers to choose the technologies when they use Copilot.
          RQ1.4: What functions are implemented by using GitHub Copilot?
          Rationale: Copilot can complete entire functions according to users’ comments. This
          RQ aims to provide a categorization of the functions that can be implemented by
          Copilot, and the answers of this RQ can provide developers guidance when imple-
          menting functions by using Copilot.
          RQ1.5: What are the purposes of using GitHub Copilot?
          Rationale: Users may use Copilot for different purposes. This RQ aims to explore
          what are users using Copilot for, and the answers of this RQ can help us get a
          better understanding of how people are using Copilot.

          RQ2: Benefits, Limitations & Challenges, and Expected Features of Us-
          ing GitHub Copilot
          RQ2.1: What are the benefits of using GitHub Copilot?
          Rationale: Using Copilot to assist programming can bring many benefits (e.g., re-
          ducing the workload of developers). This RQ aims to collect the advantages brought
          to the development by applying Copilot.
          RQ2.2: What are the limitations & challenges of using GitHub Copilot?
          Rationale: Although using Copilot to assist in writing code can help developers
          with their programming activities, there are still restrictions and problems when
          using Copilot. This RQ aims to collect and identify the limitations and challenges
          practitioners may experience when using Copilot. The answers of this RQ can help
          practitioners make an informed decision when deciding whether to code with the
          help of Copilot.
          RQ2.3: What are the expected features of users about GitHub Copilot?
          Rationale: Since its released on June, 2021, GitHub Copilot has become increas-
          ingly popular among programmers and has been developed into a mature automated
          code-completion tool. However, there are still some features Copilot does not pro-
          vide but users want to have. This RQ aims to investigate the expected features that
          users expect about GitHub Copilot. The answers of this RQ can give suggestions
          to the development team of GitHub Copilot, guiding them to make Copilot an AI-
September 13, 2023     1:2      WSPC/INSTRUCTION FILE          ws-ijseke




          6   B. Zhang et al.


          enabled coding tool that can better meet users’ needs.




          3.2. Phase B - Data Collection and Filtering
          This study focuses on understanding the practices, challenges, and expected features
          of using Copilot collected from SO and GitHub Discussions. SO is a popular soft-
          ware development community and has been widely used by developers to ask and
          answer questions as a Q&A platform. GitHub Discussions is a feature of GitHub
          used to support the communication among the members of a project. Different
          from SO, GitHub Discussions can provide various communication intentions, not
          just question-answering (e.g., a discussion can report errors or discuss the potential
          development of a software project) [17], from which the data can be complemen-
          tary to the data from SO. Besides, GitHub Discussions can provide a center of a
          community knowledge base connected with other artifacts in a project [17]. There-
          fore, we decided to use SO and GitHub Discussions as the data sources to answer
          our RQs, and we conducted the searches for both SO and GitHub Discussions on
          June 18th, 2023. We conducted the data filtering manually because the numbers of
          posts from SO and discussions from GitHub Discussions are not large, which could
          be completed in an acceptable effort and time by manual work. Another reason
          for using a manual approach is that conducting data filtering using an automatic
          approach would lead to false positive filtering results and thus make the filtering
          results inaccurate, which will negatively affect the findings we obtain.
              For SO, “copilot” is used as the term to search the posts related to Copilot.
          After searching, we got a total of 714 posts that include the search term “copi-
          lot”. The term “copilot” may appears more than once in a post, so there may be
          duplicates in the URL collection of these retrieved posts. After removing the du-
          plicates, we ended up with 678 posts with unique URLs. We conducted the data
          To manually label posts related to Copilot, we conducted a pilot data labelling by
          two authors with 10 retrieved SO posts. Specifically, the inclusion criterion is that
          the post must provide information referring to Copilot. We calculated the Cohen’s
          Kappa coefficient [18] to measure the consistency of labelled posts, which is 0.773,
          thus indicating a decent agreement between the two coders. After excluding the
          irrelevant posts in the search results, we finally got 303 Copilot related SO posts.
              For GitHub Discussions, GitHub discussions are organized according to cate-
          gories. After exploring the categories on GitHub Discussions, we found the “Copilot”
          category which contains the feedback, questions, and conversations about Copi-
          lot [19] under the “GitHub product categories”. Since all the discussions under the
          “Copilot” category are related to Copilot, we then included all the discussions un-
          der the “Copilot” category as related discussions to extract data. The number of
          discussions related to Copilot is 927.
September 13, 2023   1:2   WSPC/INSTRUCTION FILE                    ws-ijseke




                  Demystifying Practices, Challenges and Expected Features of Using GitHub Copilot      7


          3.3. Phase C - Data Extraction and Analysis
          To answer the RQs in Section 3.1, similar to Data Collection and Filtering in Sec-
          tion 3.2, we manually extracted the data items listed in Table 1. The first and third
          authors conducted a pilot data extraction independently with 10 SO posts and 10
          GitHub discussions randomly selected from the 303 SO posts and 927 GitHub dis-
          cussions. The second author was involved to discuss with the two authors and came
          to an agreement if any disagreements were found during the pilot. After the pilot,
          the criteria for data extraction were determined: (1) for all the data items listed in
          Table 1, they will be extracted and counted only if they are explicitly mentioned
          by developers that they were used with Copilot; (2) if the same developer repeat-
          edly mentioned the same data item in an SO post or a GitHub discussion, we only
          counted it once. In a post or discussion, multiple developers may mention Copilot
          related data items, resulting in situation that the total number of instances of cer-
          tain data item extracted may be greater than the number of posts and discussions.
          The first and third authors further extracted the data items from the filtered posts
          and discussions according to the extraction criteria, marked uncertain parts, and
          discussed with the second author to reach a consensus. Finally, the first author
          rechecked all the extraction results by the two authors from the filtered posts and
          discussions to ensure the correctness of the extracted data.


                      Table 1: Data items extracted and their corresponding RQs
            #     Data Item                  Description                                        RQ
            D1    Programming language       Programming languages used with Copilot            RQ1.1
            D2    IDE                        IDEs used with Copilot                             RQ1.2
            D3    Technology                 Technologies used with Copilot                     RQ1.3
            D4    Function                   Functions implemented by Copilot                   RQ1.4
            D5    Purpose                    Intentions of using Copilot                        RQ1.5
            D6    Benefit                    Benefits brought by using Copilot                  RQ2.1
            D7    Limitation and challenge   Restrictions and difficulties when using Copilot   RQ2.2
            D8    Expected feature           Features that users want Copilot to provide        RQ2.3




                             Table 2: Data items and their analysis methods
            #     Data Item                           Data Analysis Method                       RQ
            D1    Programming language                Descriptive statistics [20]               RQ1.1
            D2    IDE                                 Descriptive statistics                    RQ1.2
            D3    Technology                          Descriptive statistics                    RQ1.3
            D4    Function                            Constant comparison [21]                  RQ1.4
            D5    Purpose                             Constant comparison                       RQ1.5
            D6    Benefit                             Constant comparison                       RQ2.1
            D7    Limitation and challenge            Constant comparison                       RQ2.2
            D8    Expected Feature                    Constant comparison                       RQ2.3
September 13, 2023     1:2      WSPC/INSTRUCTION FILE          ws-ijseke




          8   B. Zhang et al.


          3.3.1. Analyze Data
          For RQ1.1, RQ1.2, and RQ1.3, we used descriptive statistics [20] to analyze and
          present the results. For RQ1.4, RQ1.5, and RQ2, we conducted a qualitative data
          analysis by applying the Constant Comparison method [22]. We constantly com-
          pared each part of the data (e.g., emergent codes) to explore differences and similar-
          ities in the extracted data to form categories [23]. Note that for answering RQ1.4,
          we categorized the functions (D4) based on developers’ discussions, i.e., develop-
          ers’ descriptions of the mentioned functions. Firstly, the first and the third authors
          coded the filtered posts and discussions with the corresponding data items listed
          (see Table 1). Secondly, the first author reviewed the coded data by the third au-
          thor to make sure the extracted data were coded correctly. Finally, the first author
          combined all the codes into higher-level concepts and turned them into categories.
          After that, the second author examined the coding and categorization results, in
          which any divergence was discussed till the three authors reached an agreement.
          The data analysis methods with their corresponding data items and RQs are listed
          in Table 2. The data analysis results are provided in [24].


          4. Results
          In this section, the study results of RQ1.1 to RQ1.4 are visualized in Fig 2, and the
          results of RQ1.5 and RQ2.1 to RQ2.3 are provided in Table 3, 4, 5, and 6.


          4.1. RQ1: Programming Languages, IDEs, Technologies, and
               Functions of Using GitHub Copilot
          RQ1.1: What programming languages are used with GitHub Copilot?
          Figure 2a lists the 19 programming languages used with Copilot, in which JavaScript
          and Python are the most frequently used ones, both accounting for one fifth. Besides,
          developers often write C# and Java code when using Copilot, as one practitioner
          mentioned “the GitHub Copilot extension is enabled in my VS 2022 C# environ-
          ment” (GitHub #14115). HTML+CSS, TypeScript, Golang, C, Rust, PHP, and
          Kotlin were used with Copilot between 3˜12 times each (1.5% to 6.1%). The rest
          programming languages (e.g., Perl, Ruby), and Visual Basic which are not popular,
          were mentioned only once with Copilot.
          RQ1.2: What IDEs are used with GitHub Copilot?
          Figure 2b shows 25 types of IDEs that are used with Copilot. Visual Studio Code is
          the dominant IDE, accounting for 48.0%. When first released, Copilot only worked
          with Visual Studio Code editor, and it is expected that Visual Studio Code is
          the IDE most often used with Copilot. Mainstream code editors, including Visual
          Studio, IntelliJ IDEA, NeoVim, and PyCharm are also occasionally used, account
          for 38.2% in total. The remaining IDEs were rarely mentioned by developers, and
          one possible reason is that there are often integration issues when using Copilot
          within them according to the results of RQ2.2.
September 13, 2023              1:2       WSPC/INSTRUCTION FILE                                                                      ws-ijseke




                         Demystifying Practices, Challenges and Expected Features of Using GitHub Copilot                                                                                                                                                                                  9


                                                                                                                                                                                                                                                                         Eclipse (0.1%)
                                                                                                                                          Jupyter Notebook                                                                                                               RubyMine (0.1%)
                                                                                                                                               (0.8%)   CLion       Android Studio                                                                                       Emacs (0.1%)
                                              PHP (2.6%)                                                                             GoLand Vim              (0.7%)    (0.7%)                                                                                            Code-OSS (0.1%)
                                    Dart                 Kotlin                                                VSCodium (1.1%)                                                                                                                                           NV Access (0.1%)
                                             C                                                                                        (0.9%) (0.8%)
                              Rust (0.6%) (3.1%)        (1.5%)                                                  Visual Studio                                                                                                                                            Sublime Text (0.1%)
                             (3.1%)                                                                                Insider       Rider (1.3%)                                                                                                                            Google Colab (0.1%)

                      Perl (0.5%)                                                JavaScript                         (1.5%)                                                                                                                                               DataSpell (0.1%)
                                                                                  (19.4%)                             WebStorm                                                                                                                                           Xcode (0.1%)
                                                                                                                                                                                                                                                                         CodeSpaces (0.1%)
                                                                          t                                              (1.9%)
                                                                       rip
                     Python                                   n va
                                                                     Sc                                                      PhpStorm                           Visual Studio Code
                                                           tho Ja
                     (19.4%)                           py                                                                      (2.7%)
                                                       #                                                                PyCharm                            Visual Studio     most used
                                                   va
                                                    C
                                             ++
                                                  Ja
                                                                                            C#                            (7.1%)                         Intellij IDEA         (top 5)
                  Nim (0.5%)
                                             C
                                                                                                                                  NeoVim
                                                                                          (13.8%)                                                      NeoVim
                                                                                                                                                                                                                                                                         Visual Studio
                                                                                                                                   (7.7%)         PyCharm
                                                                                                                                                                                                                                                                             Code
                 Lua (0.5%)               （%）                                                                                                             （%）
                                                                                                                                                                                                                                                                            (48.0%)
                                                    7 .8 4 4
                                             8.7 10. 13 19. 19.                                                                   IntelliJ IDEA              7.1 7.7 8.7 14.748.0
                    Golang                         most used                                                                         (8.7%)
                    (3.1%)                           (top 5)
                            R                                                          HTML+CSS
                         (1.0%)                                                          (6.1%)
                           TypeScript                                          Java                                                            Visual Studio
                                         C++                                                                                                      (14.7%)
                              (4.6%)                                         (10.7%)
                                        (8.7%)
                                            Visual Basic Ruby
                                               (0.5%)    (0.6%)
                       (a) RQ1.1: Programming Languages                                                                  (b) RQ1.2: Integreted Development Environments

                           OpenCV (1.4%)
                   GraphQL (1.4%)       Ajax (2.8%)                                                                                                        URL building
                                                                                                                                                                                                                                                             Algorithm
                  gRPC (1.4%)                                                                                                                                 (3.7%)
                                                                                                                                     Text processing                                                                                                           (7.5%)
                 Htmx (1.4%)                                       .Net (12.5%) Doom (1.4%)                                               (3.7%)                                                                                                                  Calculation
                 Jinja (1.4%)
                                                                                 Next.js (1.4%)                                                                                                                                                                     (3.7%)
            LibTorch (1.4%)
                                                                                  Dlib (1.4%)
          MongoDB (1.4%)




                                                                                                                                                                                                        Front-end element control
                                                              Node.js                                                          Test (15.1%)
                 Vue (5.6%)                                                             React (4.2%)



                                                                                                                                                                 Image processing   String processing
                                             most used                                         Vanilla JS (1.4%)                                                                                                                                                           Data processing


                                                                                                                                                                                                                                           Data processing
             Three.js (1.4%)
                                              (top 5)                                            Flutter (2.8%)                                                                                                                                                                (22.6%)
             PyTorch (1.4%)
                                                                                             Spring Framework (1.4%) String processing
             Pandas (1.4%)                                  .Net
                                                                                              Data Build Tool (1.4%)       (9.4%)                                                                                                   Test
                QT (1.4%)                               Vue
                                                   React                                                                                                   （%）
                                             Ajax
                                                                                                                                                                           2         6
                                          （%）                                                                                                                   7.5 9.4 13. 15.1 22.
                                                                                                                           Serialization                        most implemented
                                              2.8 4.2 5.6 12.5 48.6                                                           (3.8%)                                                      (top 5)
                                                                                                                           Printing (1.9%)                                       Filtering
                                                                                                                                                                                  (1.9%)
                                                                                                                            Memory read
                                                                              Node.js                                           (1.9%) Iteration
                                                                              (48.6%)                                                            Image processing Front-end element control
                                                                                                                                         (3.8%)                            (13.2%)
                                                                                                                                                      (7.5%)

                       (c) RQ1.3: Development Technologies                                                                               (d) RQ1.4: Implemented Functions


          Fig. 2: Programming languages, IDEs, technologies, and implemented functions of
          using Copilot (results of RQ1.1 to RQ1.4)


          RQ1.3: What technologies are used with GitHub Copilot?
          Figure 2c presents 23 technologies used with Copilot. We find that these identified
          technologies include frameworks, APIs, and libraries. Node.js, whose proportion is
          more than 45%, is one of the most popular back-end runtime environments for
          JavaScript, which is also the most frequently used language with Copilot (see the
          results of RQ1.1), thus it is reasonable that Node.js is the major technology used
          with Copilot. In addition, .NET which works for Web development, and Vue, React,
          Flutter, and Ajax which are frameworks for front-end development, were mentioned
          less often compared to Node.js. The rest of the identified technologies, many of
          which relate to machine learning (e.g., Pandas, Dlib, and OpenCV ) or front-end
          development (e.g., Htmx, Vanilla JS, and Next.js), are rarely used with Copilot,
          and each of them appears only once.
          RQ1.4: What functions are implemented by using GitHub Copilot?
          Figure 2d shows 14 functions implemented by using Copilot. The main function
          implemented by Copilot is data processing, indicating that developers tend to make
September 13, 2023    1:2   WSPC/INSTRUCTION FILE             ws-ijseke




          10   B. Zhang et al.


          use of Copilot to write functions working with data. Besides, test (15.1%) and
          front-end element control (13.2%) are the functions that account for more than
          10% besides data processing. When implementing functions, developers also use
          Copilot to code string processing, image processing, and algorithm, among which
          image processing and algorithm account for the same, i.e., 7.5%. The rest types
          of functions are seldom implemented by using Copilot, which are mentioned by
          developers twice or once.
          RQ1.5: What are the purposes of users using GitHub Copilot?
          Table 3 shows nine purposes of using Copilot. 43.3% of the developers from SO
          and GitHub Discussions indicated that they used Copilot to help generate code
          they needed. Another 9 developers (15.0%) said that they wanted to try out the
          functionality of Copilot, so they downloaded the tool and used it. To fix bugs is the
          third most popular reason for developers to use Copilot. When developers found
          their code did not work and they could not fix the bugs by themselves, they would
          turn to Copilot for help, as one developer mentioned in the post “I’ve been working
          with copilot and chatgpt for days trying to get the code to work by fixing it” (SO
          #76498229). To improve coding ability and to provide ideas for writing code have the
          same percentage, 6.7%. Some developers used Copilot to help them learn knowledge
          related to coding to improve coding ability, for examples, one developer said that
          “I am trying to learn js” (GitHub #6947) when he applied for free use of Copilot.
          Some developers did not want to directly use the code suggested by Copilot, and
          they only wanted to refer to the suggestions of Copilot to provide them with ideas
          on how to solve their problems. Copilot can be used for educational purposes and
          for research purposes as well. Users also use Copilot to help them generate code
          comments, as one developer mentioned that he used “Copilot in Visual Studio 2022
          to document code” (SO #76070342), but the percentage of this purpose is only
          5.0%. Besides, two developers (3.3%) made use of Copilot to check the code because
          they could not find why the code did not work.


          4.2. RQ2: Benefits, Limitations & Challenges, and Expected
               Features of Using GitHub Copilot
          RQ2.1: What are the benefits of using GitHub Copilot?
          Table 4 highlights 10 benefits of using Copilot. Most developers mentioned that
          they used Copilot for useful code generation, which reduced their workload and
          gave them help when they have no idea about how to write code. Programming
          with Copilot also brings faster development, as one discussion remarked, Copilot
          “saves developers a lot of time” (GitHub #35850). Meanwhile, better code quality
          can be obtained by using Copilot. Compared to the code written by developers
          themselves, the code suggested by Copilot is usually shorter and more correct, as
          one developer said, “often Copilot is smarter than me” (SO #74512186). Copilot
          can use machine learning models to learn code style of developers, so as to offer
          good adaptation to users’ code patterns. Four developers mentioned that Copilot
September 13, 2023       1:2   WSPC/INSTRUCTION FILE                      ws-ijseke




                  Demystifying Practices, Challenges and Expected Features of Using GitHub Copilot          11


                         Table 3: Purposes of using GitHub Copilot (results of RQ1.5)
           Purpose                       Example                                                  Count    %
           To help generate code         GitHub CoPilot was able to fill in the code I needed      26     43.3%
                                         after I wrote the steps in comments (SO #71905508)
           To try out the functional-    I use VIM and IntelliJ on a daily basis, and I re-         9     15.0%
           ity of Copilot                cently installed VS Code to try out the newest ”Copi-
                                         lot Chat” features (SO #76349751)
           To fix bugs                   spent a month trying to get it to work on my own           7     11.7%
                                         and after a week of trying to get chatgpt or copilot
                                         to fix the bugs I’m all out of ideas (SO #76266095)
           To improve coding ability     I’m improving my rusty skills lately and saw (in           4     6.7%
                                         some Copilot suggestions) the question mark oper-
                                         ator used as a prefix of variables (SO #74008676)
           To provide ideas for writ-    With the input from jps (AES is actually OK for            4     6.7%
           ing code                      encrypted tokens, but not signed) and Github Copi-
                                         lot I came up with a working solution using HMAC-
                                         SHA256 (SO #72812667)
           For educational purposes      For the past year I have used and taught my stu-           3     5.0%
                                         dents how they could benefit from co-pilot while cod-
                                         ing (GitHub #19410)
           To generate code com-         Using ChatGPT and Copilot, I’ve commented it to            3     5.0%
           ments                         understand its functionality. (SO #75624961)
           To check the code             I’ve checked myself by stepping through, I’ve checked      2     3.3%
                                         with GitHub Copilot, I’ve checked with ChatGPT,
                                         and they all say this is correct. (SO #76311798)
           For research purposes         I am working on a scientific study testing how Copi-       2     3.3%
                                         lot will effect the academic setting (GitHub #8324)




                         Table 4: Benefits of using GitHub Copilot (results of RQ2.1)
           Benefit                        Example                                                 Count    %
           Useful code generation         I find myself writing a lot of tests, and Copilot        28     45.9%
                                          is excellent at helping with writing repetitive tests
                                          (GitHub #9282)
           Faster development             I really enjoy using it , it reduce programming time     10     16.4%
                                          (GitHub #17382)
           Better code quality            it’s faster and simpler to your solution (SO             7      11.5%
                                          #68418725)
           Good adaptation to users’      GitHub copilot adapt to your coding practices (SO        4      6.6%
           code patterns                  #69740880)
           Better user experience         Since copilot works totally different compared to        4      6.6%
                                          all the other products out there, it is a lot more
                                          fun to use and does not annoy me like some other
                                          AI systems (GitHub #7254)
           Free for students              If you are a student you can sign up for the GitHub      3      4.9%
                                          Student Pack, which gives a lot of benefits, one
                                          being copilot for free (GitHub #31494)
           Powerful code interpreta-      Does Copilot have the code explanation feature or        2      3.3%
           tion and conversion func-      something similar? It does! some active members
           tions                          were given beta access. (GitHub #38089)
           Frequent updates to provide    Keep in mind that there are updates to the plu-          1      1.6%
           more features                  gin very frequently, so there’s still hope (SO
                                          #70428218)
           Strong integration capabil-    GitHub is supporting more editors (GitHub #6858)         1      1.6%
           ity
           Ease of study and use          when using this plugin, can study at a relatively        1      1.6%
                                          low cost (GitHub #8028)



          can give them better user experience than other AI-assisted programming tools, for
          example, one developer stated that “Copilot works totally different compared to all
September 13, 2023       1:2       WSPC/INSTRUCTION FILE                    ws-ijseke




     12   B. Zhang et al.


     the other products out there, it is a lot more fun to use and does not annoy me like
     some other AI systems” (GitHub #7254), without providing the names of the other
     products.
     RQ2.2: What are the limitations & challenges of using GitHub Copilot?
     Table 5 lists 15 limitations and challenges of using Copilot. Most developers pointed
     out the difficulty of integration between Copilot and IDEs or other plug-ins. After
     Copilot was installed in developers’ IDEs, certain plug-ins did not work and Copilot
     may conflict with some shortcut settings of the editors. Moreover, Copilot cannot be
     successfully integrated with some IDEs as Copilot does not support these editors
     yet. Due to the instability of Copilot servers, no support for proxies, and access
     restriction of some regions, developers may have difficulties of accessing Copilot.
     The code suggested by Copilot has constraints as well, and sometimes it just of-
     fers few solutions, which are not enough for users, which brings limitation to code
     generation, as one developer said “multiple solution is too little” (GitHub #37304).
     Practitioners also complained about the poor quality of generated code by Copilot.
     Some practitioners said that “GitHub Copilot suggest solutions that don’t work ”
     (SO #73701039), and some practitioners found that when the code files became
     larger, the quality of the code suggested by Copilot “becomes unacceptable” (GitHub
     #9282). When using Copilot, developers pay much attention to code privacy threat
     as well. They were worried that Copilot may use their code information without
     permission. Contrary to the developers who mentioned that Copilot gave them a
     better user experience than other AI-assisted programming tools, some practitioners
     said they had an unfriendly user experience when coding with Copilot. Compared
     to the results of our previous work [9], the number of difficulty of subscription in-
     creases significantly. This may be caused by the restrictions for free users, as one
     user complained “so looks like people with a free plan are stuck on a rate-limit for
     now with no way out” (GitHub #43893).


            Table 5: Limitations and challenges of using Copilot (results of RQ2.2)

      Limitation & Challenge          Example                                                Count    %
      Difficulty of integration       Copilot only works with VSCode, VSCodium is not         114    28.1%
                                      supported at the moment (GitHub #14837)
      Difficulty of accessing Copi-   I cannot connect to the GitHub account and the          69     17.0%
      lot                             Copilot server in VSCode, also cannot use the
                                      Copilot plugin (SO #74398521)
      Limitation to code genera-      Copilot is limited to around 1000 characters in the     48     11.8%
      tion                            response (GitHub #15122)
      Poor quality of generated       Github Copilot suggest solutions that don’t work        36     8.9%
      code                            (SO #73701039)
      Code privacy threat             Copilot does collect personal data so just take pre-    29     7.1%
                                      caution when working in private repos (GitHub
                                      #7163)
      Unfriendly user experience      I had the same problem today, an amazing tool           25     6.2%
                                      with poor user experience (GitHub #8468)
      Difficulty of subscription      My copilot subscription suddenly stopped. Tried         22     5.4%
                                      log out and in. Never have reply on support ticket
                                      over 10 days (GitHub #36190)
September 13, 2023     1:2     WSPC/INSTRUCTION FILE                     ws-ijseke




                  Demystifying Practices, Challenges and Expected Features of Using GitHub Copilot          13


           High pricing                   it is obvious that no one in South America will pay      14    3.4%
                                          that price, it is too expensive (GitHub #24594)
           Lack of customization          My question is about setting up shortcuts in Visual      13    3.2%
                                          Studio Code VSCode for GitHub Copilot Labs. (SO
                                          #73564811)
           Difficulty of understanding    I really do not understand this enough, and have         12    3.0%
           the generated code             no idea half of what this code does honestly. It was
                                          written by Copilot. (SO #72282605)
           Hard to configure              Keep getting ”Your Copilot experience is not fully       10    2.5%
                                          configured, complete your setup” in Visual Studio
                                          2022 (GitHub #19556)
           No edition for organizations   Currently, Copilot is only available for individual      8     2.0%
                                          user accounts and organizations aren’t able to pur-
                                          chase/manage Copilot for their members just yet
                                          (GitHub #32775)
           Show loading                   I am not sure what is causing this but while edit-       3     0.7%
                                          ing files within Visual Studio, I am periodically
                                          locking up with the following dialog showing (SO
                                          #73682137)
           Challenge of not providing     making sure that the tool does not provide out-          2     0.5%
           outdated suggestions           dated suggestions would still be a challenge (SO
                                          #72554382)
           Need of basic programming      It is useless if you do not understand the program-      1     0.2%
           knowledge                      ming language or the task you want to do (GitHub
                                          #35850)




                  Table 6: Expected features of users about Copilot (results of RQ2.3)
           Expected Feature                                                                      Count    %
           Can be integrated with more IDEs                                                       32     28.8%
           Allow customization of shortcuts for suggestions                                       12     10.8%
           Give suggestions when requested                                                         8     7.2%
           A team version                                                                          7     6.3%
           Support access proxies                                                                  7     6.3%
           Allow customization of the format of generated code                                     5     4.5%
           Accept the needed part of the suggestions                                               4     3.6%
           Compatible with other code generation tools                                             4     3.6%
           Allow setting filters for suggestions                                                   3     2.7%
           Allow self-signed certificates                                                          3     2.7%
           Can be used with more development frameworks                                            2     1.8%
           Ability to turn off data collection                                                     2     1.8%
           Suggestions in IDE UI can be configured                                                 2     1.8%
           Code explanation                                                                        2     1.8%
           Free for certain type of users                                                          2     1.8%
           Provide more suggestions at a time                                                      2     1.8%
           Provide more complete suggestions                                                       2     1.8%
           Ability to draw UML digrams                                                             1     0.9%
           Enable a dialog to accept or deny suggestions                                           1     0.9%
           A version for CLI (Command-Line Interface)                                              1     0.9%
           A on-premises version                                                                   1     0.9%
           Ability to select the training sources for suggestions                                  1     0.9%
           Can be used in remote servers                                                           1     0.9%
           Provide a getting started guide                                                         1     0.9%
           Provide a security rating for generated code                                            1     0.9%
           Remind users when it has no suggestions                                                 1     0.9%
           Show acceptance rate of suggestions                                                     1     0.9%
           View the code-related data shared by Copilot                                            1     0.9%
           Disable notification sounds of suggestions                                              1     0.9%



          RQ2.3: What are the expected features of users about GitHub Copilot?
September 13, 2023    1:2   WSPC/INSTRUCTION FILE              ws-ijseke




          14   B. Zhang et al.


          Table 6 presents 29 features that users expected to use about Copilot. The most of-
          ten mentioned feature by users is that they hope Copilot can be integrated with more
          IDEs (28.8%). According to the results of RQ2.2, the dominant limitation and chal-
          lenge of using Copilot is difficulty of integration as Copilot cannot be used in some
          editors. It is then reasonable that many users want Copilot to support more IDEs.
          10.8% users remarked that they wanted Copilot to allow customization of shortcuts
          for suggestions, as one post wrote “Github CoPilot should give us an option to as-
          sign a custom key instead of a [TAB] or should change to something like [SHIFT +
          TAB] instead of TAB ”(GitHub #7036). Eight users (7.2%) expected Copilot to give
          suggestions when requested. They did not want Copilot to suggest code all the time
          because it was interruptive, and they just wanted to get suggestions from Copilot
          when they requested. For example, one user asked “Is it possible to not have GitHub
          Copilot automatically suggest code, instead only showing its suggestions when us-
          ing the ‘trigger inline suggestion’ shortcut? ” (SO #76147937). Seven developers
          expected Copilot to lanch a team version and support access proxies, respectively.
          Allow customization of the format of generated code was mentioned by 5 develop-
          ers. They wanted this feature to “configure suggestion appearance” (GitHub #7234)
          so that Copilot suggestions could be “more distinguishable with normal code” and
          thus “improve the accessibility” (GitHub #7628). Few developers indicated that
          they only wanted to “accept one line of several ” of Copilot suggested code (SO
          #75183662), and they called for the feature that they can accept the needed part of
          the suggestions. Besides, four developers also mentioned that they hoped Copilot
          could be compatible with other code generation tools like ReSharper.


          5. Implications
          This section presents the key implications of our study, which represent empirically
          grounded findings that could help researchers and developers to understand the
          effective usage of Copilot.
          Integration of Copilot with IDEs: According to the results of RQ1.2 and RQ2.2,
          we found that most developers choose to integrate the Copilot plug-in with main-
          stream IDEs (including Visual Studio Code, Visual Studio, IntelliJ IDEA, NeoVim,
          and PyCharm), and the percentage of mainstream IDEs used with Copilot by practi-
          tioners reaches 86.2%. When developers choose the lesser known IDEs (e.g., Sublime
          Text), they often find it hard to integrate the Copilot plug-in and thus have diffi-
          culty of integration. In addition to the reason that developers may install Copilot in
          their chosen IDEs incorrectly, another reason for the difficulty of integration is that
          Copilot does not support certain IDEs at the moment. When developers choose to
          use Copilot in mainstream IDEs, they can install it smoothly, and even if problems
          arise during the installation or use, they can easily find a solution on SO or GitHub
          Discussions as many other developers may have encountered similar issues. On the
          contrary, when developers choose to use Copilot in unpopular IDEs, they may not
          be able to install it because the IDEs are not officially supported by Copilot, and
September 13, 2023   1:2   WSPC/INSTRUCTION FILE                  ws-ijseke




                 Demystifying Practices, Challenges and Expected Features of Using GitHub Copilot   15


          they cannot find solutions as few developers use Copilot with these IDEs. To reduce
          the difficulty of integration, we recommend practitioners to use mainstream IDEs
          with Copilot. Besides, the most expected feature of users is that they hope Copilot
          can be integrated with more IDEs, which confirms with the results of RQ2.2 (the
          main limitation of using Copilot is difficulty of integration). We suggest GitHub
          can consider integrating Copilot with more IDEs in the future, which can meet the
          needs of diverse developers.
          Support for Front-end and Machine Learning Development: As shown in
          the results of RQ1.1, RQ1.3, and RQ1.4, practitioners often write JavaScript and
          Python code when using Copilot, and they tend to use Copilot with front-end and
          machine learning related technologies (including frameworks, APIs, and libraries)
          to implement front-end (e.g., front-end element control ) and machine learning func-
          tions (e.g., data processing and image processing). JavaScript is the foundation lan-
          guage of many popular front-end frameworks and most of Websites use JavaScript
          on the client side. Python is the first choice when it comes to the development of
          machine learning solutions with the help of rich libraries, e.g., OpenCV. It is conse-
          quently reasonable that developers tend to use Copilot with JavaScript to generate
          code for front-end and Python for developing machine learning applications.
          Different Versions of Copilot: From the results of RQ2.3, we can find that
          different versions of Copilot are needed (i.e., a team version, a version for CLI
          (Command-Line Interface), and a on-premises version). In different development
          environments, developers may have specific requirements when using Copilot. If
          GitHub can release different versions of Copilot, it would increase the usability and
          acceptance of Copilot and thus make it available to a wider variety of users. Besides,
          GitHub has officially launched some versions of Copilot, e.g., Copilot Labs, Copilot
          X, and Copilot Nightly. Copilot Labs [25] is used to experiment with new ideas
          before taking them into real production, Copilot X [26] provides an enhancement
          with new features, and Copilot Nightly contains experimental and less well tested
          changes. Developers can choose the version of Copilot according to their needs.
          Potentials and Perils of Using Copilot in Software Development: Trained
          on billions of lines of code, Copilot can turn natural language prompts into coding
          suggestions across dozens of programming languages and make developers code
          faster and easier [4]. The results of RQ2.1 and RQ2.2 show that many benefits of
          using Copilot contradict its limitations and challenges, e.g., useful code generation
          vs. limitation to code generation. When deciding to use Copilot, developers should
          consider tool integration, user experience, budget, code privacy, and some other
          aspects, and make trade-offs between these factors. In short, using Copilot is like
          a double-edged sword, and practitioners need to consider various aspects carefully
          when deciding whether or not to use it. If Copilot can be used with appropriate
          programming languages and technologies to implement functions required by users
          correctly in developers’ IDEs, it will certainly optimize developers’ coding workflow
          and do what matters most - building software by letting AI do the redundant
          work. Otherwise, it will bring difficulties and restrictions to development, making
September 13, 2023    1:2   WSPC/INSTRUCTION FILE               ws-ijseke




          16   B. Zhang et al.


          developers feel frustrated and constrained. The study results can help practitioners
          being aware of the potential advantages and disadvantages of using Copilot and
          thus make an informed decision whether to use it for programming activities.
          Understanding the Code Generated by Copilot: From the results of RQ2.1,
          RQ2.2, and RQ2.3, we can see that some practitioners think one of the benefits of
          using Copilot is that it has powerful code interpretation feature, but some practition-
          ers complained about the difficulty of understanding the generated code by Copilot
          and called for code explanation feature. It would be interesting to investigate why
          developers have opposing attitude towards understanding the code generated by
          Copilot and how the generated code by Copilot can be better explained to and
          understood by developers. Besides, GitHub Copilot Labs which is dependent on
          Copilot extension has been released for experimental purposes, and Copilot Labs
          has the feature to provide explanations of the code generated by Copilot for devel-
          opers [25]. The latest Copilot X also has the code explanation feature [26], but we
          do not know the reason why developers do not use Copilot Labs or Copilot X to
          interpret Copilot-generated code. We suggest that Copilot can provide the features
          for developers to better understand the generated code directly, such as generating
          code comments with the generated code in IDEs.
          Users’ customization on suggestions by Copilot: According to the results
          of RQ2.2, some developers thought that one of the limitations and challenges of
          Copilot is lack of customization, and it is expected that a number of developers
          called for features of Copilot to allow customization of shortcuts for suggestions,
          allow customization of the format of generated code, and accept the needed part of the
          suggestions (see the results of RQ2.3). The existing features of Copilot cannot satisfy
          users’ needs on code suggestions. Users pointed out that they had difficulty in setting
          up shortcuts for actions on suggestions (e.g., accepting suggestions). Based on the
          feedback from users, they can only accept suggestions via the tab key, however, they
          want “an option to change the keybinding for accepting the suggestions” instead
          (GitHub #6919). Besides, a few users also reflected that it was hard to distinguish
          between the code wrote by themselves and the code suggested by Copilot. They
          wanted to customize the color, font, and format of Copilot suggestions. Another
          expected feature of users about Copilot is that they hope they can accept the needed
          part of the suggestions. Some users want to accept Copilot suggestions line by line or
          accept only the next word of Copilot suggestions each time, while they do not want
          accept the entire suggestions by Copilot. As a result, there is a need for users to
          customize the way of accepting suggestions by Copilot. Some other expected features
          (e.g., allow setting filters for suggestions, suggestions in IDE UI can be configured,
          and ability to select the training sources for suggestions) also relate to customization
          on suggestions by Copilot. On the basis of the above feedback from users, we believe
          that it is necessary for Copilot to allow customization for suggestions, which will
          give developers better user experience when using Copilot as they are able to use
          it in the way they want.
          Towards an Effective Use of Copilot: Further investigation about the practices
September 13, 2023   1:2   WSPC/INSTRUCTION FILE                  ws-ijseke




                 Demystifying Practices, Challenges and Expected Features of Using GitHub Copilot   17


          of Copilot can be conducted by questionnaire and interview. Under what conditions
          the challenges of using Copilot will show up as advantages or disadvantages, and how
          to use Copilot to convert its disadvantages into advantages are also worth further
          exploration. Besides, although we have investigated various aspects of using Copilot
          (e.g., limitations and challenges), we did not looked in depth at what types of users
          (e.g., developers, educators, and students) who use Copilot, when and how they
          use Copilot. By exploring these aspects, researchers can get meaningful information
          which would help guide towards an effective use of Copilot.



          6. Threats to Validity
          The validity threats are discussed according to the guidelines in [16], and internal
          validity is not considered, since we did not investigate the relationships between
          variables and results. The three validity threats presented below highlight potential
          limitations of this research that may invalidate some of the results. Future research
          can focus on minimizing these threats to ensure methodological rigor of the study.
              Construct validity indicates whether the theoretical and conceptual con-
          structs are correctly measured and interpreted. We conducted data labelling, ex-
          traction, and analysis manually, which may lead to personal bias. To reduce this
          threat, the data labelling of SO posts was performed after the pilot labelling to
          reach an agreement between the authors. The data extraction and analysis was also
          conducted by two authors, and the first author rechecked all the results produced by
          the third author. During the whole process, the first author continuously consulted
          with the second author to ensure there are no divergences.
              External validity indicates the the degree of generalization of the study re-
          sults, i.e., the extent to which the results can be generalized to other contexts. We
          chose two popular developer communities (SO and GitHub Discussions) because
          SO has been widely used in software engineering studies and GitHub Discussions is
          a new feature of GitHub for discussing specific topics [17]. These two data sources
          can partially alleviate the threat to external validity. However, we admit that our
          selected data sources may not be representative enough to understand all the prac-
          tices, challenges, and expected features of using Copilot.
              Reliability indicates the replicability of a study yielding the same or similar
          results. We conducted a pilot labelling before the formal labelling of SO posts with
          two authors, and the Cohen’s Kappa coefficient is 0.773, indicating a decent con-
          sistency. We acknowledge that this threat might still exist due to the small number
          of posts used in the pilot. All the steps in our study, including manual labelling,
          extraction, and analysis of data were conducted by three authors. During the pro-
          cess, the three authors discussed the results until there was no any disagreements
          in order to produce consistent results. In addition, the dataset of this study that
          contains all the extracted data and labelling results from the SO posts and GitHub
          discussions has been provided online for validation and replication purposes [24].
September 13, 2023    1:2   WSPC/INSTRUCTION FILE                 ws-ijseke




          18   B. Zhang et al.


          7. Conclusions
          We conducted an empirical study on SO and GitHub discussions to understand
          the practices, challenges, and expected features of using GitHub Copilot from the
          practitioners’ perspective. We used “copilot” as the search term to collect data
          from SO and collected all the discussions under the “Copilot” category in GitHub
          discussions. Finally, we got 303 SO posts and 927 GitHub discussions related to
          Copilot. Our results identified the programming languages, IDEs, technologies used
          with Copilot, functions implemented by Copilot, and the benefits, limitations, and
          challenges of using Copilot, which are first-hand information for developers. The
          main results are that: (1) JavaScript and Python are the most frequently discussed
          programming languages by developers with Copilot. (2) Visual Studio Code is the
          dominant IDE used with Copilot. (3) Node.js is the major technology used with
          Copilot. (4) Data processing is the main function implemented by Copilot. (5) To
          help generate code is the leading purpose of users using Copilot. (6) Useful code
          integration is the most common benefit mentioned by developers when using Copi-
          lot. (7) Difficulty of integration is the most frequently encountered limitations and
          challenges when developers use Copilot. (8) Copilot can be integrated with more
          IDEs is the most expected feature of users.
              In the next step, we plan to explore the practices of using Copilot by conducting
          interviews or an online survey to get practitioners’ perspectives on using Copilot,
          which can supplement our existing data collected from repository mining. Besides,
          we also plan to further explore various aspects of Copilot, especially how to improve
          the understanding of developers on the generated code (see Section 5).

          Acknowledgements
          This work has been supported by the Natural Science Foundation of China (NSFC)
          under Grant No. 62172311 and the Special Fund of Hubei Luojia Laboratory.

          References
           [1] J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai,
               M. Terry, Q. Le et al., “Program synthesis with large language models,” arXiv preprint
               abs/2108.07732, 2021.
           [2] M. Allamanis, E. T. Barr, P. Devanbu, and C. Sutton, “A survey of machine learning
               for big code and naturalness,” arXiv preprint abs/1709.06182, 2018.
           [3] H. Pearce, B. Ahmad, B. Tan, B. Dolan-Gavitt, and R. Karri, “An empirical
               cybersecurity evaluation of github copilot’s code contributions,” arXiv preprint
               abs/2108.09293, 2021.
           [4] GitHub Copilot · Your AI pair programmer, https://github.com/features/copilot.
           [5] C. Bird, D. Ford, T. Zimmermann, N. Forsgren, E. Kalliamvakou, T. Lowdermilk, and
               I. Gazit, “Taking flight with copilot: Early insights and opportunities of ai-powered
               pair-programming tools,” ACM Queue, vol. 20, no. 6, pp. 35–57, 2023.
           [6] N. Al Madi, “How readable is model-generated code? examining readability and visual
               inspection of github copilot,” in Proc. of the 37th Int. Conf. on Automated Software
               Engineering (ASE). ACM, 2023, pp. 1–5.
September 13, 2023    1:2   WSPC/INSTRUCTION FILE                   ws-ijseke




                  Demystifying Practices, Challenges and Expected Features of Using GitHub Copilot   19


           [7] N. Nguyen and S. Nadi, “An empirical evaluation of github copilot’s code sugges-
               tions,” in Proc. of the 19th Int. Conf. on Mining Software Repositories (MSR). IEEE,
               2022, pp. 1–5.
           [8] B. Yetistiren, I. Ozsoy, and E. Tuzun, “Assessing the quality of github copilot’s code
               generation,” in Proc. of the 18th Int. Conf. on Predictive Models and Data Analytics
               in Software Engineering (PROMISE). ACM, 2022, pp. 62–71.
           [9] B. Zhang, P. Liang, X. Zhou, A. Ahmad, and M. Waseem, “Practices and challenges of
               using github copilot: An empirical study,” in Proc. of the 35th Int. Conf. on Software
               Engineering and Knowledge Engineering (SEKE). KSI, 2023, pp. 124–129.
          [10] G. Sandoval, H. Pearce, T. Nys, R. Karri, B. Dolan-Gavitt, and S. Garg, “Security
               implications of large language model code assistants: A user study,” arXiv preprint
               abs/2208.09727, 2022.
          [11] S. Imai, “Is github copilot a substitute for human pair-programming? an empirical
               study,” in Proc. of the 44th Int. Conf. on Software Engineering: Companion Proceed-
               ings (ICSE-Companion). IEEE, 2022, pp. 319–321.
          [12] C. Wang, J. Hu, C. Gao, Y. Jin, T. Xie, H. Huang, Z. Lei, and Y. Deng, “Practitioners’
               expectations on code completion,” arXiv preprint abs/2301.03846, 2023.
          [13] A. M. Dakhel, V. Majdinasab, A. Nikanjam, F. Khomh, M. C. Desmarais, Z. Ming,
               and Jiang, “Github copilot ai pair programmer: Asset or liability?” arXiv preprint
               abs/2206.15331, 2022.
          [14] N. Nguyen and S. Nadi, “An empirical evaluation of github copilot’s code sugges-
               tions,” in Proc. of the 19th IEEE/ACM Int. Conf. on Mining Software Repositories
               (MSR). IEEE, 2022, pp. 1–5.
          [15] A. Sarkar, A. D. Gordon, C. Negreanu, C. Poelitz, S. S. Ragavan, and B. Zorn, “What
               is it like to program with artificial intelligence?” arXiv preprint abs/2208.06213, 2022.
          [16] P. Runeson and M. Höst, “Guidelines for conducting and reporting case study re-
               search in software engineering,” Empirical Software Engineering, vol. 14, no. 2, pp.
               131–164, 2009.
          [17] H. Hata, N. Novielli, S. Baltes, R. G. Kula, and C. Treude, “Github discussions: An
               exploratory study of early adoption,” Empirical Software Engineering, vol. 27, no. 1,
               pp. 1–32, 2022.
          [18] J. Cohen, “A coefficient of agreement for nominal scales,” Educational and Psycho-
               logical Measurement, vol. 20, no. 1, pp. 37–46, 1960.
          [19] GitHub Discussions: Copilot Category, https://github.com/community/community/
               discussions/categories/copilot.
          [20] A. N. Christopher, Interpreting and Using Statistics in Psychological Research.
               SAGE Publications, 2017.
          [21] K.-J. Stol, P. Ralph, and B. Fitzgerald, “Grounded theory in software engineering
               research: A critical review and guidelines,” in Proc. of the 38th Int. Conf. on Software
               Engineering (ICSE). ACM, 2016, pp. 120–131.
          [22] B. G. Glaser, “The constant comparative method of qualitative analysis,” Social
               Problems, vol. 12, no. 4, pp. 436–445, 1965.
          [23] L. R. Hallberg, “The “core category” of grounded theory: Making constant compar-
               isons,” International Journal of Qualitative Studies on Health and Well-being, vol. 1,
               no. 3, pp. 141–148, 2006.
          [24] B. Zhang, P. Liang, X. Zhou, A. Ahmad, and M. Waseem, Dataset of the Paper:
               Demystifying Practices, Challenges and Expected Features of Using GitHub Copilot,
               2023, https://doi.org/10.5281/zenodo.8123302.
          [25] GitHub Next — GitHub Copilot Labs, https://githubnext.com/projects/copilot-labs.
          [26] Introducing GitHub Copilot X, https://github.com/features/preview/copilot-x.

