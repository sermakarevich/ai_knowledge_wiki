# Date of publication xxxx 00, 0000, date of current version xxxx 00, 0000
Source: https://arxiv.org/abs/2502.13199v2
Kind: pdf
Fetched: 2026-09-23T19:52:34.468444+00:00
Tool: pdftotext
Research-Target: /Users/sergii/.ai/knowledge/research_topics/coding_agents/research/ai_coding_best_practices
Topic: coding_agents

The Role of GitHub Copilot on Software
Development: A Perspective on Productivity,
Security, Best Practices and Future Directions
Suresh Babu Nettur1*, Shanthi Karpurapu1*, Unnati Nettur2, Likhit Sagar Gajja3, Sravanthy
Myneni1, AND Akhil Dusi4
1
    Independent Researcher, Virginia Beach, VA 23456, USA
2
  Department of Computer Science, Virginia Tech, Blacksburg, VA 24061 USA
3
  Department of Computer Science, BML Munjal University, Haryana 122413 INDIA
4
  Department of Information Systems, Indiana Tech, Indiana USA

Corresponding authors: Shanthi Karpurapu (shanthi.karpurapu@gmail.com), Suresh Babu Nettur (nettursuresh@gmail.com)

*
    Shanthi Karpurapu and Suresh Babu Nettur are co-first authors




ABSTRACT GitHub Copilot is transforming software development by automating tasks and boosting
productivity through AI driven code generation. In this paper, we conduct a literature survey to synthesize
insights on Copilot's impact on productivity and security. We review academic journal databases, industry
reports, and official documentation to highlight key findings and challenges. While Copilot accelerates
coding and prototyping, concerns over security vulnerabilities and intellectual property risks persist. Drawing
from the literature, we provide a perspective on best practices and future directions for responsible AI
adoption in software engineering, offering actionable insights for developers and organizations to integrate
Copilot effectively while maintaining high standards of quality and security.

INDEX TERMS Artificial Intelligence (AI), AI Assistant, GitHub Copilot, OpenAI, security, cyber security,
secure code, vulnerability detection, productivity, GPT-3, GPT-4, Cursor AI, Amazon Code Whisperer,
Google Codey, Large Language Models (LLMs), code generation tools, code quality, defect resolution, code
refactoring, code completion, programming, Java, Python, software development, Agile development,
software testing, unit testing, debugging, developer tools, Continuous Integration and Delivery (CI/CD),
software quality assurance, Ethical AI, software engineering, risk mitigation, secure software development,
data privacy.


I. INTRODUCTION                                                                 years, GitHub Copilot has become a leading AI powered code
The evolution of code generation tools has significantly                        generation tool, integrating seamlessly into developer
transformed the software development landscape, enabling                        environments and redefining the concept of collaborative
developers to automate repetitive tasks, accelerate coding                      coding with AI.
processes, and improve overall productivity. As these tools                     GitHub Copilot, initially launched in 2021 and developed in
have advanced, artificial intelligence integration has enabled                  collaboration with OpenAI, is an AI powered tool designed to
more sophisticated solutions, with tools such as GitHub                         assist developers with code generation. It is powered by
Copilot emerging as significant players in the field. Early                     OpenAI's Codex model, a version of GPT-3 specifically
iterations of code generation tools focused on simplifying                      designed for code generation. Codex leverages deep learning
template-based code creation, assisting with boilerplate code,                  techniques and is trained on a massive data set that includes
and offering solutions for specific programming languages or                    public GitHub repositories and other open source code. This
frameworks. Recently, AI assisted code generation tools                         dataset features 159 gigabytes of Python code from 54 million
leverage models such as Large Language Models (LLMs) to                         repositories, enabling Codex to generate accurate and context
predict, auto complete, and write complex code snippets based                   aware code across various programming languages. GitHub
on contextual input from the developer. These tools aim to                      Copilot Chat now operates on OpenAI's GPT-4o and offers
reduce development time, minimize errors, and assist                            early access to OpenAI o1, a model known for excelling in
developers by making code suggestions in real time. In recent

                                                                                                                                            1
complex reasoning tasks and demonstrating improved                          Pull           AI generated summaries of pull request
performance in benchmark evaluations [1].                                   Request        changes, emphasizing affected files and
                                                                            Summaries      critical areas for review (Copilot Enterprise
GitHub Copilot seamlessly integrates with popular Integrated                               only).
Development Environments (IDEs) like Visual Studio Code,                    Text           AI powered text completion to quickly and
Visual Studio, Neovim, and JetBrains. It offers real time code              Completion     accurately       generate    pull    request
suggestions with auto completion and can generate entire                    (Beta)         descriptions (Copilot Enterprise only).
functions based on natural language descriptions or existing                Knowledge      Create and maintain documentation sets to
code snippets. What distinguishes GitHub Copilot from                       Bases          serve as contextual references for
traditional code completion tools is its capability to understand                          conversations with GitHub Copilot. When
broader coding contexts and predict the next logical steps of                              using Copilot Chat on GitHub.com or in
the development process. This feature is especially beneficial                             Visual Studio Code, you can select a
for developers who work across multiple programming                                        specific knowledge base to improve the
languages and technologies, as Copilot supports various                                    relevance and accuracy of Copilot’s
languages, including but not limited to Python, Java Script,                               responses to your queries.
TypeScript, Ruby, Angular, and Go. As developers use
Copilot, it continually refines its suggestions based on user                         TABLE 1: GITHUB COPILOT KEY FEATURES.
input and project context, providing code snippets tailored to
specific coding styles. This interactive learning method                  Since its launch, GitHub Copilot has experienced rapid
transforms Copilot into an AI partner in software                         adoption within the developer community. Recent statistics
development. The key features of GitHub Copilot [2] are listed            show that GitHub Copilot has been integrated into millions of
in Table 1.                                                               developer environments worldwide, with approximately 14.5
                                                                          million downloads in Visual Studio, 20 million in Visual
    Feature       Description                                             Studio Code, and 10 million in JetBrains. Over 400
                                                                          organizations have adopted GitHub Copilot, according to
    Code          GitHub Copilot provides auto complete style
                                                                          GitHub's 2023 report, and this number is expected to grow
    Completion    suggestions in supported IDEs (e.g., Visual
                                                                          significantly following the launch of GitHub Copilot for
                  Studio Code, Visual Studio, JetBrains, Azure
                                                                          Business [3].
                  Data Studio, Vim/Neovim). Users can select
                  standard commands like /fix (fix the problem in
                                                                          The central goal of our research is to advance the application
                  code), /explain (offer detailed explanations of
                                                                          of deep learning and LLMs across software engineering [4][5]
                  code), /doc (generate documentation for code),
                                                                          and medical diagnostics [6][7]. In this paper, we conducted an
                  and /tests (create tests for the code) for a selected
                                                                          extensive literature survey to synthesize key insights on
                  portion of text. Alternatively, users can enter a
                                                                          GitHub productivity and security implications. Our approach
                  query to receive tailored suggestions, enabling
                                                                          involved selectively reviewing academic databases, along
                  real time code improvements based on AI
                                                                          with examining industry white papers, technical reports,
                  driven insights.
                                                                          official documentation from sources like GitHub and OpenAI.
    Copilot       GitHub Copilot provides a chat interface for
                                                                          Rather than aiming for an exhaustive systematic review, we
    Chat          coding related questions. Users can select
                                                                          focused on identifying studies most critical from our
                  standard commands such as /fix, /explain, /doc,
                                                                          perspective, analyzing their findings, and distilling key
                  or /tests for a selected portion of text.
                                                                          insights. This process enabled us to recognize pressing
                  Alternatively, users can enter custom queries to
                                                                          challenges, evaluate existing solutions, and formulate a
                  receive Copilot’s context aware suggestions and
                                                                          perspective on best practices and future directions to
                  solutions in real time. Users can check log
                                                                          effectively address these issues.
                  errors, create feature flags, and deploy apps to
                  the cloud (Public Beta). Additional features
                  include "pull request difference analysis," a web
                                                                          II. Productivity Impacts of GitHub Copilot
                  search powered by Bing (Public Beta), and the
                                                                          GitHub Copilot is well recognized in the software developer
                  ability to inquire about failed Actions jobs
                                                                          community and is known for its ability to enhance productivity
                  (Public Beta). Users can also obtain answers
                                                                          by automating various coding tasks. It accelerates rapid
                  regarding issues, pull requests, discussions,
                                                                          prototyping and experimentation, enabling developers to
                  files, commits, and more [2].
                                                                          quickly generate code snippets and test new ideas by providing
    Copilot in    A chat like interface in the terminal that              context aware suggestions. GitHub Copilot offers a range of
    the CLI       provides command suggestions or                         use cases that enhance productivity in the software
                  explanations.                                           development process, as summarized in Table 2.


2
.                                                                 productivity improvements associated with Copilot. These
    Use case        Description                                   studies consider a range of factors such as number of
    Routine Task    Experienced developers benefit from
                                                                  developers, experience levels of developers, types of coding
    Automation      Copilot by automating repetitive tasks,
                    allowing more time for complex work.          tasks performed, programming languages used, complexity
                    Senior developers often manage multiple       of the tasks, and various demographic details. This breadth
                    projects and find that tools like Copilot     of analysis allows us to gain a nuanced understanding of
                    save time on routine tasks such as writing    Copilot’s impact on productivity across different segments
                    unit tests or database queries.               of the developer community.
    Learning and    Junior developers benefit from Copilot as     A recent study conducted by Solohubov et al. on GitHub
    Skill           an interactive tutor, helping them quickly    Copilot evaluates its impact on developer productivity,
    Development     learn unfamiliar programming languages,       particularly in the context of creating CRUD operations
                    frameworks, or libraries. By suggesting       using the Dart programming language and the Flutter
                    optimized code and providing immediate        framework [8]. The research evaluates tasks of varying
                    feedback, Copilot enhances their coding       complexity, ranging from simple to challenging, and
                    skills and boosts their confidence. The       measures the approximate reduction in the developer's effort.
                    'Explain this' feature of Copilot helps       These findings suggest that GitHub Copilot significantly
                    junior developers break down and              enhances productivity, reducing the effort needed by
                    understand complex logic or algorithms        approximately 70% for simple tasks and around 20% for
                    easily.                                       more complex ones [8]. A study conducted by Moradi
    Code            Copilot greatly assists developers in         Dakhel et al. investigates the impact of GitHub Copilot on
    Refactoring     cleaning up legacy codebases by               developer productivity, specifically in creating an HTTP
                    identifying        redundancies        and    server in JavaScript [9]. This research involved 95
                                                                  professional programmers recruited through Upwork,
                    recommending reusable code blocks.
                                                                  capturing a diverse sample of experienced developers. These
                    This enhances code readability and
                                                                  findings indicate that software developers utilizing AI
                    maintainability, ultimately accelerating
                                                                  assistance, such as GitHub Copilot, completed their tasks
                    future development efforts.                   approximately 55.8% faster than those without AI support.
    Code Review     Developers can benefit from GitHub            This significant improvement highlights the potential of
                    Copilot during code reviews by receiving      Copilot to streamline development processes and enhance
                    recommendations that help maintain high       efficiency in real world programming scenarios.
                    standards of quality and consistency.         Nguyen and Nadi [10] conducted an empirical study on
                    Copilot's pull request (PR) feature           GitHub Copilot’s effectiveness in generating code
                    streamlines this process by automatically     suggestions using LeetCode programming questions. They
                    generating summaries of changes and           evaluated its performance across multiple programming
                    highlighting key areas that need attention.   languages, including Python, Java, JavaScript, and C,
                    This allows teams to stay productive          highlighting its capability to produce clear and low
                    while ensuring that quality is not            complexity solutions. However, they also identified
                    sacrificed, resulting in a more efficient     limitations, such as the generation of suboptimal code and
                    and detailed review process.                  reliance on undefined helper methods. Mastropaolo et al.
    Test-Driven     Developers benefit from Copilot by            [11] investigated the robustness of deep learning-based code
    Development     supporting TDD practices in the               recommendation systems, including GitHub Copilot, using a
    (TDD)           generation of test cases. This enables        dataset of 892 Java methods. Their findings revealed that
                    them to implement TDD seamlessly and          semantically equivalent descriptions resulted in different
                    efficiently in the early stages of            code generation outcomes approximately 46% of the time.
                                                                  Similarly, Yetistiren et al. [12] assessed the code quality of
                    development, ensuring higher code
                                                                  GitHub Copilot, Amazon CodeWhisperer, and ChatGPT in
                    quality from the outset.
                                                                  the context of Python programming. Their evaluation found
      TABLE 2: GITHUB COPILOT COMMON USE CASES IN SOFTWARE        that ChatGPT outperformed the other tools in generating
                         DEVELOPMENT                              correct code solutions. They also emphasized the importance
                                                                  of input quality, demonstrating that well defined problem
                                                                  descriptions play a key role in successful code generation.
A. UNDERSTANDING PRIOR RESEARCH IN CONTEXT
                                                                  Mehmood et al. [13] examined GitHub Copilot’s ability to
To understand the productivity implications of GitHub             generate test cases, comparing them to manually written
Copilot, we have reviewed relevant research papers. Our           ones. Their analysis highlighted that AI generated test cases
analysis reveals that several studies indicate significant        demonstrated comparable quality and effectiveness.


3
However, their study was limited to Python and a small set        developers. The study found consistent acceptance rates
of files.                                                         (33% for suggestions, 20% for lines of code) and high
Sobania et al. [14] compared GitHub Copilot with Genetic          developer satisfaction (72%). Copilot proved useful for tasks
Programming (GP) for program synthesis in Python. Their           like boilerplate code generation but struggled with domain
findings suggest that GP is better suited for tasks requiring     specific logic [21].
numerous input/output examples, whereas Copilot performs          In addition, an internal study conducted by GitHub focused
well for problems defined through textual descriptions.           on evaluating the impact of GitHub Copilot on developer
Research on productivity and code quality has yielded mixed       efficiency and satisfaction. In an experiment with 95
results regarding Copilot’s impact on developer efficiency.       participants, developers using Copilot completed tasks 55%
While it can significantly boost productivity by generating       faster than those without it, demonstrating its effectiveness
large portions of code, the quality of its outputs often falls    in boosting productivity. Furthermore, a survey of over 2,000
short, requiring extensive debugging. This underscores the        developers revealed that 88% felt more productive in their
need to balance productivity with code quality [15].              work, 77% agreed they spent less time searching for
Researchers have observed a strong correlation between            information, and 87% experienced less mental effort on
Copilot’s acceptance rate and perceived productivity but          repetitive tasks, reducing cognitive load. Additionally, 74%
caution that this metric alone does not fully reflect the         reported being able to focus on more satisfying work, as
complexity of developer experiences [16]. While Copilot can       Copilot alleviated the burden of repetitive coding tasks. This
improve overall programming efficiency, it does not always        analysis highlights how Copilot enhances speed and
shorten task completion time, as AI generated code often          improves overall job satisfaction among developers [22].
requires additional debugging [17].                               Further, a study conducted by GitHub in partnership with
Mozannar et al. [18] analyzed data from interactions with         Accenture explored how developers integrate the tool into
GitHub Copilot, proposing a utility theoretic framework to        their daily workflows [23]. This collaboration aimed to
optimize decisions on displaying or withholding suggestions.      assess the impact of Copilot on developer productivity and
Based on data from 535 programmers, their study                   code quality. The findings indicated that an increase in pull
demonstrated that a substantial portion of suggestions likely     requests is a strong indicator of the value delivered;
to be rejected by developers could be avoided. They also          Accenture developers experienced an 8.69% increase in pull
highlighted the significance of considering a programmer’s        requests. Since each pull request must undergo code review,
latent, unobserved state when determining when to present         the pull request merge rate serves as an excellent measure of
suggestions. Additionally, their findings revealed that using     code quality from the perspective of maintainers and
suggestion acceptance as a reward signal for guiding display      coworkers. Accenture observed a 15% increase in the pull
decisions can lead to lower quality suggestions. Baralla et al.   request merge rate, indicating that as the volume of pull
[19] examined GitHub Copilot's potential to enhance               requests grew, so did the number that successfully passed
developer productivity, particularly in the context of smart      code review. Moreover, there was an 84% increase in
contract development on the blockchain. Their study               successful builds, suggesting that not only were more pull
highlighted Copilot's capacity to generate functional code,       requests moving through the system, but they were also of
improve efficiency, and assist in routine development tasks       higher quality, as evaluated by both human reviewers and
such as code generation, debugging, and testing [19]. The         test automation. Developers accepted approximately 30% of
research found that Copilot excelled in generating code for       suggestions from GitHub Copilot, and 90% reported
simpler smart contracts and standard token implementations,       committing code recommended by Copilot. Additionally,
contributing to accelerated development processes.                91% of developers stated that their teams merged pull
However, its performance weakened with more complex               requests containing code suggested by Copilot. This study
contracts, particularly in handling intricate blockchain          demonstrated a strong adoption and growing influence
specific logic and advanced security considerations. This         within the developer community.
underscores the tool's effectiveness in expediting basic tasks
while still requiring significant human oversight for more
                                                                  B. REFLECTIONS ON LITERATURE
complicated scenarios, especially regarding security and
efficiency.                                                       Task Complexity Matters: Studies suggest that the
Chatterjee et al. [20] reported significant productivity          productivity benefits of Copilot are more noticeable in
improvements following the adoption of GitHub Copilot at          simpler tasks, whereas complex or domain specific
ANZ Bank. During a six-week experiment, the group using           challenges often require additional developer intervention to
Copilot completed tasks 42.36% faster than the control            maintain code quality.
group. Productivity improvements varied by skill level:           Quality vs. Speed Trade off: While accelerated code
beginners showed a 52.27% improvement, intermediates              generation is frequently cited as a key advantage, research
41.6%, and advanced users 40.48%. These results suggest           indicates that AI generated code often requires extra
that Copilot notably enhanced efficiency in software              debugging and validation. This highlights an ongoing need
engineering tasks. Bakal et al. [21] evaluated GitHub             to refine AI tools to better balance speed and code quality.
Copilot’s impact on productivity at ZoomInfo with over 400


4
Context Dependent Effectiveness: The tool’s impact varies           detecting vulnerabilities in smart contracts. While Copilot
based on the developer’s experience and the specific coding         excels in generating basic security features for standard token
context. Some studies suggest that beginners may experience         implementations, it struggles with more complex blockchain
greater relative productivity gains, though they might also         specific security issues. Its vulnerability detection and
rely more on suggestions that do not always align with best         automatic program repair (APR) capabilities are unreliable,
practices.                                                          often requiring multiple prompts to address all identified
Beyond Acceptance Rates: Metrics such as suggestion                 issues. This highlights the critical need for human oversight,
acceptance rates and pull request merge rates provide useful        as Copilot generated code may introduce inconsistencies or
insights, but the literature suggests they may not fully capture    security flaws. Consequently, while Copilot can aid in
the balance between productivity gains and the subsequent           speeding up the development process, developers are
efforts required to ensure code quality.
                                                                    encouraged to integrate additional security measures and
Overall, GitHub Copilot represents a significant
                                                                    review the code thoroughly before deploying it in production
advancement in AI assisted software development, offering
                                                                    environments [19].
the potential to enhance efficiency across a broad range of
coding tasks. Its ability to generate code rapidly and facilitate   Siddque et al. [25] introduced SecurityEval, a comprehensive
learning makes it an invaluable tool in modern software             dataset designed to evaluate the security of machine learning
engineering. However, while its benefits are evident, striking      based code generation models. Comprising 130 diverse
a balance between accelerated code generation and                   samples mapped to 75 different vulnerability types from the
maintaining high quality, reliable software remains a key           Common Weakness Enumeration, SecurityEval allows for an
challenge.                                                          in-depth assessment of models like InCoder and GitHub
                                                                    Copilot. The results reveal that both models can generate
III. Security Concerns with GitHub Copilot                          vulnerable code in certain scenarios. With its thoroughness,
While GitHub Copilot provides numerous advantages in terms          SecurityEval offers a valuable benchmark for evaluating the
of productivity and code generation, it also raises important       security capabilities of other code generation models in future
security concerns that need to be addressed. One major issue        research [25]. Siddique et al. [26] investigated the presence of
is the potential introduction of vulnerabilities, as Copilot may    code smells and security vulnerabilities in the datasets used to
suggest code that includes known weaknesses if such patterns        train code generation models and examined whether these
are prevalent in the training data. This can lead to the            issues are reflected in the generated output. The study
generation of insecure code, such as hardcoded credentials,         employed Pylint and Bandit to evaluate three different training
improper input validation, or insufficient error handling. For      sets and assess the output produced by an open source
instance, it might suggest embedding sensitive information          transformer-based model and GitHub Copilot. The results
like API keys or passwords directly into the code or producing      showed that code smells and security vulnerabilities in the
code that lacks proper input sanitization, potentially resulting    training data were propagated into the generated code. These
in SQL injection or cross site scripting (XSS) vulnerabilities.     findings highlighted the need for further improvements in
Furthermore, this may expose sensitive information, leading         code generation techniques and emphasized the importance of
to potential legal or intellectual property (IP) issues.            carefully curating and scrutinizing the training data to mitigate
                                                                    such issues in the output.
A. UNDERSTANDING PRIOR RESEARCH IN CONTEXT
                                                                    Majdinasab et al. [27] replicated the study by Pearce et al. [24].
To thoroughly assess the security implications of GitHub            to assess security vulnerabilities in newer versions of GitHub
Copilot, we have conducted a review of relevant research            Copilot. While AI powered code generation tools like Copilot
papers, focusing on identified vulnerabilities and the risks        and Amazon CodeWhisperer enhance developer productivity,
associated with AI assisted development. In this section, we        concerns persist regarding the security of their generated code.
will explore potential vulnerabilities, present research            The study analyzed Python code suggestions using CodeQL
evidence on security risks, and highlight broader concerns          and found that the percentage of vulnerable code has
from the developer community and industry experts regarding         decreased from 36.54% to 27.25%. Despite these
the safe use of AI in software development.                         improvements, the findings confirm that Copilot continues to
The study by Pearce et al. focused on evaluating GitHub             generate insecure code, highlighting the need for ongoing
Copilot's code generation across 89 scenarios, covering 25          enhancements in AI assisted coding security.
different Common Weakness Enumerations (CWEs),                      Given that this research was published in 2022, one needs to
particularly high-risk ones from MITRE's "Top 25 Most               assess whether there have been any improvements in
Dangerous Software Weaknesses" list [24]. This research             addressing these issues in the latest version of GitHub Copilot
found that 44% of the code generated by Copilot contained           to draw informed conclusions. In another empirical study
security issues, highlighting significant concerns regarding the    conducted by Fu et al., code snippets generated by GitHub
tool's output [24]. Baralla et al. [19] also examined GitHub        Copilot from GitHub projects were analyzed [28]. The study
Copilot from a security standpoint, emphasizing its limitations     revealed 452 generated snippets with a high likelihood of
in consistently applying advanced security patterns and             security vulnerabilities. Specifically, 32.8% of the Python and

5
24.5% of the JavaScript snippets exhibited security issues.         Despite its capabilities, developers need to remain vigilant in
These vulnerabilities spanned 38 distinct Common Weakness           reviewing and rigorously testing all generated code to ensure
Enumeration (CWE) categories, including critical ones like          that Copilot’s contributions align with the desired quality and
CWE-330: Use of Insufficiently Random Values, CWE-78:               security standards.
OS Command Injection, and CWE-94: Improper Control of
Code Generation. Notably, eight of these CWEs are listed in         IV. Best Practices
the 2023 CWE Top-25, underscoring the severity of the issues
[28].                                                               GitHub Copilot has introduced a transformative approach to
                                                                    code generation, but from our perspective, its integration into
                                                                    development workflows demands a thoughtful balance of its
B. REFLECTIONS ON LITERATURE                                        strengths and limitations. While the tool offers significant
Ensuring Training Data Quality: From our literature study,          potential, we believe its effective use requires careful
we find that vulnerabilities in generated code may stem from        consideration of both its capabilities and its risks. Drawing
issues within the training datasets. This suggests that more        from our analysis of Copilot's features, studies, and real-world
effective curation and filtering of training data could help        impacts, we bring to the forefront practices that can foster
improve security outcomes in AI assisted coding.                    secure and efficient usage. Developers can consider these
The Role of Human Oversight: Based on the literature, while         practices based on their specific work environments and
Copilot significantly accelerates code generation, human            project contexts to maximize Copilot’s benefits while
oversight remains essential. Ensuring a careful review of           mitigating any potential risks.
outputs is vital for developers, especially in security sensitive   Vigilant Code Review: Developers are encouraged to
contexts like smart contract development, to help mitigate          maintain a rigorous approach to code review when
potential risks.                                                    incorporating AI generated code. This involves carefully
Ongoing Security Enhancements: Research indicates that              examining all Copilot generated code for accuracy, security,
newer versions of Copilot appear to have reduced certain            and alignment with project requirements, particularly in
vulnerabilities. However, we believe that the persistent            sensitive areas like authentication, data handling, and
presence of security risks points to the need for continuous        encryption. AI generated code can inadvertently introduce
research and improvements to further strengthen AI assisted         inefficiencies or vulnerabilities, so incorporating thorough
coding security.                                                    peer review practices is essential. Engaging multiple
Effectiveness Based on Context: From our literature study, it       perspectives in validating code suggestions helps identify
appears that Copilot’s performance varies depending on task         potential issues early, ensuring that the code maintains high
complexity and domain specific requirements. While it seems         standards of quality and security throughout the development
highly effective in generating boilerplate and routine code, we     process. To further enhance this review process, the latest
find that it may face challenges in scenarios that demand           version of Copilot introduces advanced code review
deeper security awareness and more nuanced decision making.         capabilities [30], integrated with GitHub to help users iterate,
                                                                    validate, and integrate review comments efficiently. This
However, recognizing the security risks associated with AI          feature, however, is currently unavailable in the free version.
generated code, GitHub introduced significant enhancements          Use Security Tools: It’s worth considering the integration of
in 2023 to address these concerns. A key improvement was            automated security testing tools (if not already implemented),
launching an AI based vulnerability prevention system               such as Static Application Security Testing (SAST) and
designed to block insecure coding patterns in real time,            Dynamic Application Security Testing (DAST), into the
making GitHub Copilot's suggestions more secure. This               development workflow when utilizing GitHub Copilot. These
model targets explicitly common vulnerable coding patterns,         tools can help identify and address vulnerabilities in the
such as hardcoded credentials, SQL injections, and path             generated code, ensuring that potential security issues are
injections, thereby mitigating risks at the code generation         detected early in the development process. Incorporating these
stage itself. These developments represent GitHub's ongoing         tools can enhance the security of projects, adding an extra
efforts to enhance the security of Copilot's output while           layer of protection against threats.
maintaining its productivity benefits [29].                         Educate and Train: Comprehensive developer training can
On the other hand, we believe it is important to highlight the      play a key role in helping enterprise or corporate organizations
potential risks of developers becoming overly reliant on            maximize the potential of GitHub Copilot. By fostering an
Copilot's suggestions. There is a risk that developers might        understanding of best practices for writing secure code,
unintentionally accept sub optimal or insecure code without         developers can become more proficient at recognizing and
sufficient scrutiny, which could negatively impact overall          addressing common vulnerabilities. Additionally, regularly
code quality and security standards. While Copilot can              broadcasting important Copilot enhancements can help keep
expedite the coding process, it remains an AI model that may        the team informed about new features and improvements,
occasionally produce insecure or ineffective code patterns.


6
ensuring they are well equipped to fully utilize the tool’s       training data available for that particular language. Expanding
capabilities.                                                     the breadth and depth of programming language support in
Maintain Transparency and Feedback: Establishing a                GitHub Copilot can enhance its versatility and value for a
feedback loop with GitHub is crucial for enhancing Copilot.       broader range of developers. Incorporating additional
By reporting issues and providing feedback on improvements,       languages, frameworks, and emerging ones allows developers
developers contribute to the ongoing refinement of the tool.      across various fields and specialties to benefit from AI driven
Additionally, maintaining clear documentation on how              code generation. By offering support for a broader range of
Copilot is integrated into projects, including configurations,    languages and frameworks, Copilot can meet the varied needs
guidelines, and usage practices, ensures that team members        of the software development community and enhance overall
can reference best practices and understand the tool's            productivity.
application within their specific context. This transparency      Expand IDE’s support: Expanding GitHub Copilot’s
helps foster a culture of continuous improvement and              support across a broader range of Integrated Development
accountability, leading to high quality, secure code.             Environments (IDEs) could significantly elevate the overall
Legal and Ethical Considerations: When using GitHub               development experience. Currently, Copilot is available in
Copilot, developers need to be mindful of the legal and ethical   popular IDEs such as Visual Studio Code, Eclipse, JetBrains,
implications of the generated code. Vigilance regarding IP and    Azure Data Studio, Vim/NeoVim, Visual Studio, and Xcode
copyright issues is crucial to avoid potential infringement,      [34]. Enhancing Copilot’s integration with even more IDEs
including compliance with relevant licenses. The "Finding         can streamline workflows and allow developers to leverage AI
Matching Code" feature, when enabled, helps by providing          driven code suggestions more seamlessly within their
references to the matching code along with the associated         preferred development environments. By facilitating smoother
number and type of licenses [31]. Ethical usage also requires     interactions between Copilot and other software development
adherence to data privacy and security protocols. Special         tools, teams can foster better collaboration, increase
attention is necessary when using Copilot in contexts             productivity, and ultimately improve both the efficiency of
involving sensitive or confidential information, as this may      project completion and the quality of the code.
lead to unintended data exposure and compromise security          AI Assisted Software Design: Expanding GitHub Copilot's
standards. Establishing and following clear guidelines and        capabilities to include AI assisted software design represents
usage policies for sensitive projects can be highly beneficial.   a significant opportunity for enhancing the development
By following these practices, developers can effectively          process. By offering suggestions for software design and
leverage Copilot while maintaining legal and ethical integrity.   architecture in addition to code generation, Copilot could
                                                                  provide valuable assistance in the early stages of development.
V. Future Work                                                    This expansion may involve generating design patterns,
                                                                  architectural diagrams, and high-level system components,
The growth of GitHub Copilot is evident, as approximately         allowing developers to create more robust and well-structured
30-40% of organizations surveyed by Gartner actively              applications from the outset. Such features could improve
encourage and promote the adoption of AI coding tools.            collaboration among team members and streamline the
Additionally, 29-49% of respondents across various markets        transition from design to implementation, ultimately
reported that their organizations allow using these tools but     contributing to higher quality software outcomes.
provide limited encouragement. This highlights a significant      Legal and Ethical Considerations: Future developments of
opportunity for organizations to actively embrace the AI wave.    GitHub Copilot could benefit from addressing intellectual
As noted in the GitHub Blog, the ongoing integration of AI        property concerns by implementing mechanisms that prevent
tools into software development teams reflects a growing          the generation of code that infringes on copyrighted or
trend that organizations can consider tapping into for            proprietary material. This involves enhancing the model’s
enhanced productivity and innovation [32]. As GitHub              ability to avoid generating code that resembles existing
Copilot and similar AI driven code generation tools continue      proprietary code, thereby improving compliance with legal
to evolve, several areas present further development and          standards and fostering greater trust among developers. Legal
research opportunities. In this section, we present our views     experts have raised important questions regarding the ethical
on potential avenues for future work, including technological     use of AI generated code, necessitating ongoing dialogue and
improvements and broader implications for the software            regulation within the industry. Additionally, investigating the
development industry.                                             ethical and social implications of widespread AI code
                                                                  generation could provide valuable insights into its long-term
Programming Coverage: GitHub Copilot currently supports           effects on the software development industry and the broader
a variety of programming languages, including C, C++, C#,         tech ecosystem.
Go, Java, JavaScript, Kotlin, PHP, Python, Ruby, Rust, Scala,     Transparency and Accountability: Future development
and TypeScript [33]. However, the extent of support for each      could focus on enhancing clarity regarding how GitHub
language can vary, depending on the volume and diversity of       Copilot generates code. Developers can gain a better

7
understanding of the tool by providing detailed explanations       emerging and niche languages, and incorporate evaluation
of its suggestions, including the reasoning and sources used to    metrics focusing on coding standards, security vulnerabilities,
generate responses. This approach helps build user confidence      and maintainability. Developers can gain a deeper
and encourages responsible use among development teams.            understanding of Copilot's capabilities from these large-scale
Academic and Industry Research: Academic and industry              code quality evaluations. This knowledge will equip them with
research plays a crucial role in understanding the impact of AI    valuable insights into the tool's performance and effectiveness,
driven code generation tools, such as GitHub Copilot, Cursor       enabling more informed decisions in their coding practices.
AI, Amazon Code Whisperer, and Google Codey, on various
aspects of software development. Existing studies on               VI. CONCLUSION
developer productivity, code quality, and team dynamics have
already provided valuable insights into how these tools            GitHub Copilot is a powerful tool that enhances productivity
influence real world practices. However, further in-depth          by automating routine coding tasks and enabling rapid
studies can expand on these findings, offering a deeper            prototyping. However, its integration into development
understanding of the long-term implications of these tools.        workflows raises important considerations, particularly
Comprehensive studies and case analyses will help clarify the      around security, intellectual property, and code quality.
evolving relationship between developers and AI tools,             Based on a literature study, we present insights into the
                                                                   benefits and challenges of using Copilot, and to address
providing a clearer understanding of their long-term impact.
                                                                   these, we offer our perspective on best practices for
User Customization: Empowering users to customize the tool
                                                                   integrating Copilot into development workflows, focusing
to their preferences leads to more relevant and accurate
                                                                   on responsible AI adoption and addressing security,
suggestions. The current experimental prerelease version of        intellectual property, and code quality concerns.
copilot chat offers to switch between a few LLMs (GPT 4o,          Additionally, we highlight future research directions and
Claude 3.5 Sonnet, Gemini 2.0 Flash, o1, o3-mini) and the          propose iterative improvements to enhance Copilot’s
option to add workspaces file, which allows user                   capabilities while mitigating the associated risks and
customization [35]. Along with these options for fine tuning       ensuring continuous adaptation to emerging challenges. As
AI behavior, creating user profiles to define tone and subject     AI tools like Copilot continue to evolve, their role in
matter preferences can be a great addition from a user             software development is likely to expand, prompting the
personalization standpoint. The current “custom instruction        need for ongoing reflection and adaptation. The continuous
feature” in GitHub Copilot allows users to set parameters such     evolution of these tools underscores the importance of
as tool usage, language, and style [36]. As this paper is being    sustained research and iterative improvements to address
written, this feature is in preview and has the potential for      current limitations. Looking ahead, it is crucial to critically
further changes and improvements. Additionally,                    assess how Copilot integrates into development workflows,
implementing a feature to save session preferences can ensure      refining best practices that not only enhance productivity but
that future suggestions align with the user’s style, ultimately    also mitigate risks and uphold core principles of software
enhancing overall accuracy.                                        quality.
Standardization of Evaluation Metrics: Establishing
standardized evaluation metrics and benchmarking practices         REFERENCES
across AI based code generation tools can serve as a means for
                                                                       1.    https://github.com/openai/simple-evals
comparing their performance and effectiveness. This                    2.    https://github.com/features/copilot
standardization can facilitate a clearer understanding of each         3.    https://github.blog/news-insights/product-news/github-copilot-
tool’s strengths and weaknesses, enabling developers and                     for-business-is-now-available/
                                                                       4.    Karpurapu, Shanthi, Sravanthy Myneni, Unnati Nettur, Likhit
organizations to make informed choices based on consistent                   Sagar Gajja, Dave Burke, Tom Stiehm, and Jeffery Payne.
criteria. One example we can quote is various LLM                            "Comprehensive Evaluation and Insights into the Use of Large
benchmarks [37] on evaluation, which provide metrics for                     Language Models in the Automation of Behavior-Driven
                                                                             Development Acceptance Test Formulation." IEEE Access
assessing capabilities across different tasks.                               (2024)
Code Generation Tools Evaluation Improvements: Recent                  5.    Nettur, Suresh Babu, Shanthi Karpurapu, Unnati Nettur, and
research has extensively evaluated GitHub Copilot and similar                Likhit Sagar Gajja. "Cypress Copilot: Development of an AI
AI driven code generation tools [38-41]. Researchers have                    Assistant for Boosting Productivity and Transforming Web
                                                                             Application Testing." IEEE Access (2024).
highlighted the significance of various metrics in assessing the       6.    Nettur, Suresh B., Shanthi Karpurapu, Unnati Nettur, Likhit S.
performance and effectiveness of these tools, focusing on                    Gajja, Sravanthy Myneni, Akhil Dusi, and Lalithya Posham.
metrics such as code acceptance rate, correctness ratio,                     "UltraLightSqueezeNet: A Deep Learning Architecture for
                                                                             Malaria Classification with up to 54x Fewer Trainable
reproducibility, similarity, validity, accuracy, and security                Parameters for Resource Constrained Devices." ArXiv, (2025).
vulnerabilities. Additionally, conducting large scale code                   Accessed January 28, 2025. https://arxiv.org/abs/2501.14172.
quality evaluations in real time environments, rather than the         7.    Nettur, Suresh B., Shanthi Karpurapu, Unnati Nettur, Likhit S.
                                                                             Gajja, Sravanthy Myneni, Akhil Dusi, and Lalithya Posham.
typically controlled settings, is important. These evaluations               "Lightweight Weighted Average Ensemble Model for
can consider a breadth of programming languages, including

8
          Pneumonia Detection in Chest X-Ray Images." ArXiv, (2025).            25.    Siddiq, M.L., Santos, J.C.S.: SecurityEval dataset: mining
          Accessed January 28, 2025. https://arxiv.org/abs/2501.16249.                 vulnerability examples to evaluate machine learning-based
    8.    Illia Solohubov, Artur Moroz, Mariia Yu Tiahunova, Halyna H.                 code generation techniques. Assoc. Comput. Mach. (2022).
          Kyrychek and Stepan Skrupsky, “Accelerating software                         https://doi.org/10.1145/3549035.3561184
          development with AI: exploring the impact of ChatGPT and              26.    Siddiq, M.L., Majumder, S.H., Mim, M.R., Jajodia, S., Santos,
          GitHub Copilot” (2023) Pages 76-82, https://ceur-ws.org/Vol-                 J.C.: An empirical study of code smells in transformer-based
          3679/paper17.pdf                                                             code generation techniques. In: International Working
    9.    Arghavan Moradi Dakhel, Vahid Majdinasab, Amin Nikanjam,                     Conference on Source Code Analysis and Manipulation,
          Foutse Khomh, Michel C. Desmarais, Zhen Ming (Jack) Jiang,                   SCAM, pp. 71–82. Dagstuhl Publishing,Limassol (2022)
          “GitHub Copilot AI pair programmer: Asset or Liability?”              27.    Majdinasab, Vahid, Michael Joshua Bishop, Shawn Rasheed,
          (2023)      Volume     203,     111734,    ISSN     0164-1212,               Arghavan Moradidakhel, Amjed Tahir, and Foutse Khomh.
          https://doi.org/10.1016/j.jss.2023.111734                                    "Assessing the Security of GitHub Copilot's Generated Code-A
    10.   N. Nguyen and S. Nadi, "An empirical evaluation of GitHub                    Targeted Replication Study." In 2024 IEEE International
          Copilot's code suggestions", Proc. IEEE/ACM 19th Int. Conf.                  Conference on Software Analysis, Evolution and
          Mining Softw. Repositories (MSR), pp. 1-5, May 2022.                         Reengineering (SANER), pp. 435-444. IEEE, 2024.
    11.   A. Mastropaolo, L. Pascarella, E. Guglielmi, M. Ciniselli, S.         28.    Y. Fu, P. Liang, A. Tahir, Z. Li, M. Shahin, J. Yu and J. Chen.
          Scalabrino, R. Oliveto, et al., "On the robustness of code                   “Security Weaknesses of Copilot Generated Code in GitHub”
          generation techniques: An empirical study on GitHub                          (2023) https://arxiv.org/abs/2310.02059
          copilot", Proc. IEEE/ACM 45th Int. Conf. Softw. Eng. (ICSE),          29.    https://github.blog/ai-and-ml/github-copilot/github-copilot-
          pp. 2149-2160, May 2023.                                                     now-has-a-better-ai-model-and-new-capabilities/
    12.   B. Yetiştiren, I. Özsoy, M. Ayerdem and E. Tüzün, "Evaluating         30.    https://docs.github.com/en/copilot/using-github-copilot/using-
          the code quality of AI-assisted code generation tools: An                    github-copilot-for-pull-requests/using-copilot-to-help-you-
          empirical study on GitHub copilot Amazon CodeWhisperer and                   work-on-a-pull-request
          ChatGPT", arXiv:2304.10778, 2023.                                     31.    https://docs.github.com/en/copilot/using-github-
    13.   S. Mehmood, U. I. Janjua and A. Ahmed, "From manual to                       copilot/finding-public-code-that-matches-github-copilot-
          automatic: The evolution of test case generation methods and                 suggestions
          the role of GitHub copilot", Proc. Int. Conf. Frontiers Inf.          32.    https://github.blog/news-insights/research/survey-ai-wave-
          Technol. (FIT), vol. 34, pp. 13-18, Dec. 2023.                               grows/
    14.   D. Sobania, M. Briesch and F. Rothlauf, "Choose your                  33.    https://docs.github.com/en/enterprise-cloud@latest/get-
          programming copilot: A comparison of the program synthesis                   started/learning-about-github/github-language-support
          performance        of    GitHub      copilot    and    genetic        34.    https://docs.github.com/en/copilot/using-github-
          programming", Proc. Genetic Evol. Comput. Conf., pp. 1019-                   copilot/getting-code-suggestions-in-your-ide-with-github-
          1027, Jul. 2022.                                                             copilot
    15.   S. Imai, "Is GitHub copilot a substitute for human pair-              35.    https://docs.github.com/en/copilot/using-github-copilot/ai-
          programming? An empirical study", Proc. IEEE/ACM 44th Int.                   models/changing-the-ai-model-for-copilot-chat
          Conf. Softw. Eng. Companion, pp. 319-321, May 2022.                   36.    https://docs.github.com/en/copilot/customizing-
    16.   A. Ziegler, E. Kalliamvakou, X. A. Li, A. Rice, D. Rifkin, S.                copilot/adding-custom-instructions-for-github-copilot
          Simister, et al., "Productivity assessment of neural code             37.    https://github.com/leobeeson/llm_benchmarks
          completion", Proc. 6th ACM SIGPLAN Int. Symp. Mach.                   38.    I. Siroš, D. Singelée, and B. Preneel, “GitHub Copilot: the
          Program., pp. 21-29, Jun. 2022.                                              perfect                Code               compLeeter?,” (2024)
    17.   P. Vaithilingam, T. Zhang and E. L. Glassman, "Expectation vs.               https://arxiv.org/abs/2406.11326
          experience: Evaluating the usability of code generation tools         39.    B. Yetistiren, I. Ozsoy, and E. Tuzun, “Assessing the quality of
          powered by large language models", Proc. CHI Conf. Human                     GitHub copilot’s code generation,” (2022) Proceedings of the
          Factors Comput. Syst. Extended Abstr., pp. 1-7, Apr. 2022.                   18th International Conference on Predictive Models and Data
    18.   H. Mozannar, G. Bansal, A. Fourney and E. Horvitz, "When to                  Analytics            in          Software          Engineering,
          show a suggestion? Integrating human feedback in ai-assisted                 https://doi.org/10.1145/3558489.3559072
          programming", Proc. AAAI Conf. Artif. Intell., vol. 38, no. 9,        40.    B. Yetiştiren, I. Özsoy, M. Ayerdem, and E. Tüzün, “Evaluating
          pp. 10137-10144, 2024.                                                       the Code Quality of AI-Assisted Code Generation Tools: An
    19.    Baralla, Gavina, Giacomo Ibba, and Roberto Tonelli.                         Empirical Study on GitHub Copilot, Amazon CodeWhisperer,
          "Assessing GitHub Copilot in Solidity Development:                           and                                          ChatGPT” (2023),
          Capabilities, Testing, and Bug Fixing." IEEE Access (2024).                  https://doi.org/10.48550/arxiv.2304.10778
    20.   Chatterjee, Sayan, Ching L. Liu, Gareth Rowland, and Tim              41.    A. Ziegler et al., “Measuring GitHub Copilot’s Impact on
          Hogarth. "The Impact of AI Tool on Engineering at ANZ Bank                   Productivity” Communications of The ACM, vol. 67, no. 3, pp.
          An Empirical Study on GitHub Copilot within Corporate                        54–63, Feb. 2024, https://doi.org/10.1145/3633453
          Environment." ArXiv, (2024). Accessed February             12,
          2025. https://arxiv.org/abs/2402.05636.
                                                                           SURESH BABU NETTUR has received his Master of Science (M.S)
    21.   Bakal, Gal, Ali Dasdan, Yaniv Katz, Michael Kaufman, and
                                                                           degree from the Birla Institute of Technology and Science (BITS), Pilani,
          Guy Levin. "Experience with GitHub Copilot for Developer
                                                                           Rajasthan, India, and his Bachelor of Technology degree in Computer
          Productivity at Zoominfo." ArXiv, (2025). Accessed February
                                                                           Science and Engineering from Nagarjuna University, Guntur, India. With
          12, 2025. https://arxiv.org/abs/2501.13282.
                                                                           over two decades of expertise, he has established himself as a thought
    22.   https://github.blog/news-insights/research/research-
                                                                           leader in artificial intelligence, deep learning, and machine learning
          quantifying-github-copilots-impact-on-developer-productivity-
                                                                           solutions. His work spans the development of scalable and intelligent
          and-happiness/
                                                                           systems across industries such as healthcare, finance, telecom, and
    23.   https://github.blog/news-insights/research/research-
                                                                           manufacturing. Suresh has been at the forefront of integrating AI-driven
          quantifying-github-copilots-impact-in-the-enterprise-with-
                                                                           innovations into real-world applications, leveraging cutting-edge
          accenture/
                                                                           technologies such as OpenAI models, GitHub Copilot, and custom deep
    24.   Hammond Pearce, Baleegh Ahmad, Benjamin Tan, Brendan
                                                                           learning architectures to deliver transformative solutions. His contributions
          Dolan-Gavitt, and Ramesh Karri. 2025. Asleep at the
                                                                           include designing and implementing advanced machine learning models,
          Keyboard? Assessing the Security of GitHub Copilot’s Code
                                                                           optimizing deep learning architectures for resource-constrained
          Contributions. Commun. ACM 68, 2 (February 2025), 96–105.
                                                                           environments, and integrating AI solutions into software development and
          https://doi.org/10.1145/3610721
                                                                           testing pipelines. With significant experience in cross-functional team


9
leadership and managing onsite-offshore collaboration models, he has
successfully delivered AI-powered applications across cloud platforms like
AWS.

Suresh is passionate about applying AI to solve complex problems in
healthcare and finance, including predictive analytics, automation, and
intelligent decision-making systems. He is proficient in Agile
methodologies, Test-Driven Development (TDD), and service-oriented
architectures (SOA), ensuring seamless integration of AI and machine
learning into software systems. As an advocate for innovative AI
applications, Suresh is committed to advancing the field through
sustainable and impactful solutions that redefine industry standards and
improve quality of life.

SHANTHI KARPURAPU received the Bachelor of Technology degree in
chemical engineering from Osmania University, Hyderabad, India and the
Masters technology degree in chemical engineering from Institute of
Chemical Technology, Mumbai, India.
She has over a decade of experience leading, designing, and developing test
automation solutions for various platforms across healthcare, banking, and
manufacturing industries using Agile and Waterfall methodologies. She is
experienced in building reusable and extendable automation frameworks for
web applications, REST, SOAP, and microservices. She is a strong follower
of the shift-left testing approach, a certified AWS Cloud practitioner, and a
machine learning specialist. She is passionate about utilizing AI-related
technologies in software testing and the healthcare industry.

UNNATI NETTUR currently pursuing an undergraduate degree in
Computer Science at Virginia Tech, Blacksburg, VA, USA. She possesses
an avid curiosity about the constantly evolving field of technology and
software development, with a particular interest in Artificial Intelligence.
She is passionate about gaining experience in building innovative and
creative solutions for current issues in the field of software engineering.

LIKHIT SAGAR GAJJA pursuing a Computer Science Bachelor’s degree
at BML Munjal University, Haryana, INDIA. He is evident in showing his
passion for the dynamic field of technology and software development. His
specific interests include Artificial Intelligence, Prompt Engineering, and
Game Designing technologies, highlighting his dedication to obtaining
hands-on experience and developing innovative solutions for real-time
issues in software engineering.

SRAVANTHY MYNENI earned master of science in information
technology and management from Illinois institute of technology, Chicago,
Illinois in 2017 and Bachelor’s degree in computer science in 2013. She is
currently working as an engineer focused on data engineering and analysis.
She has 8+ years of experience in designing, building and deploying data
centric solutions using Agile and Waterfall methodologies. She is
enthusiastic about data analysis, data engineering and AI application to
provide solutions for real world problems.

AKHIL DUSI currently pursuing Masters of Information Sciences at
University of Indiana Tech, Indiana, USA. He is a passionate researcher
and developer with a diverse background in software development,
cybersecurity, and emerging technologies. He has a proven ability to
deliver innovative and practical solutions. His work includes developing
web and mobile-based applications, conducting vulnerability assessments
and penetration testing, and leveraging cloud platforms for efficient
infrastructure management. He is certified in cybersecurity and machine
learning, reflecting a strong commitment to continuous learning and
staying at the forefront of technological advancements. His research
interests focus on artificial intelligence, IoT, and secure system design,
with a vision to drive impactful innovations.




10

