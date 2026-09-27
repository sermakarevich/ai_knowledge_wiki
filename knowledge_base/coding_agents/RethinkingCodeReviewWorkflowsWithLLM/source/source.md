# Rethinking Code Review Workflows with LLM
Source: https://arxiv.org/abs/2505.16339v1
Kind: pdf
Fetched: 2026-09-23T19:57:17.318645+00:00
Tool: pdftotext
Research-Target: /Users/sergii/.ai/knowledge/research_topics/coding_agents/research/ai_coding_best_practices
Topic: coding_agents

                                               Rethinking Code Review Workflows with LLM
                                                      Assistance: An Empirical Study
                                                                 Fannar Steinn ADalsteinsson∗† , Björn Borgar Magnússon∗† , Mislav Milicevic∗ ,
                                                                               Adam Nirving Davidsson∗ , Chih-Hong Cheng†‡
                                                                                         ∗ WirelessCar Sweden AB, Gothenburg, Sweden
                                                                                  † Chalmers University of Technology, Gothenburg, Sweden
                                                                                         ‡ University of Gothenburg, Gothenburg, Sweden



                                            Abstract—Code reviews are a critical yet time-consuming              diagnostic and one exploratory. The first question (RQ1)




arXiv:2505.16339v1 [cs.SE] 22 May 2025
                                         aspect of modern software development, increasingly challenged          focuses on understanding current code review practices within
                                         by growing system complexity and the demand for faster de-              the company and identifying opportunities for AI assistance,
                                         livery. This paper presents a study conducted at WirelessCar
                                         Sweden AB, combining an exploratory field study of current              while the second question (RQ2) explores how developers
                                         code review practices with a field experiment involving two             perceive and interact with two variations of LLM-based tools
                                         variations of an LLM-assisted code review tool. The field study         during review tasks.
                                         identifies key challenges in traditional code reviews, including          To address these research questions, we conducted a two-
                                         frequent context switching, insufficient contextual information,
                                         and highlights both opportunities (e.g., automatic summarization        phase empirical study (Sec. IV) at WirelessCar Sweden AB.
                                         of complex pull requests) and concerns (e.g., false positives and         • Phase 1 involved a field study through semi-structured
                                         trust issues) in using LLMs. In the field experiment, we developed
                                                                                                                     interviews to uncover practical challenges in existing
                                         two prototype variations: one offering LLM-generated reviews
                                         upfront and the other enabling on-demand interaction. Both                  code review workflows and to identify potential areas
                                         utilize a semantic search pipeline based on retrieval-augmented             where AI assistance could be beneficial. Importantly,
                                         generation to assemble relevant contextual information for the              based on these findings, we designed and implemented
                                         review, thereby tackling the uncovered challenges. Developers               two variations of LLM-assisted review tools, one being an
                                         evaluated both variations in real-world settings: AI-led reviews
                                                                                                                     AI-led co-reviewer and the other an interactive assistant,
                                         are overall more preferred, while still being conditional on the
                                         reviewers’ familiarity with the code base, as well as on the severity       integrated with retrieval-augmented generation (RAG) to
                                         of the pull request.                                                        provide contextual support.
                                            Index Terms—Large Language Models; Code Review; Empir-                 • In Phase 2, we evaluated these tools in a real-world field
                                         ical Software Engineering                                                   experiment involving practicing developers. The results
                                                                                                                     show that while the AI-led mode was generally preferred,
                                                                   I. I NTRODUCTION                                  especially for large or unfamiliar pull requests, prefer-
                                            Code review (CR) is a cornerstone of modern software                     ences were context-dependent. Participants valued the
                                         engineering, ensuring code quality, defect detection, and team              tool’s ability to provide faster understanding, improved
                                         knowledge sharing. Nevertheless, as software systems scale                  thoroughness, and helpful contextual insights, though is-
                                         and development cycles accelerate, traditional manual code                  sues such as trust, false positives, and interface limitations
                                         review practices struggle with inefficiencies, reviewer fatigue,            were noted.
                                         and inconsistent outcomes. The rapid development of Large                  Altogether, our findings (Sec. V) suggest that LLMs can
                                         Language Models (LLMs) [1]–[3] has enabled AI to demon-                 meaningfully augment, rather than replace, human reviewers,
                                         strate strong capabilities across various software engineering          and highlight the importance of adaptive integration strategies
                                         tasks, including code generation and bug detection. While their         that respect developers’ workflow preferences and domain
                                         integration into the coding activities has been smooth, the full        knowledge. Furthermore, our results point to clear design
                                         potential of LLMs in code review remains underexplored.                 directions for future tools: AI assistance should be seamlessly
                                            Through a combination of observational research and field            embedded into existing developer environments (e.g., GitHub,
                                         experiments conducted at WirelessCar Sweden AB1 (where                  IDEs, Slack), offer concise and structured feedback with mini-
                                         some but not all teams are permitted to utilize AI in develop-          mal latency, and support both proactive and reactive interaction
                                         ment), this study investigates how LLMs can be meaningfully             modes. For maximal utility, the assistant must be context-
                                         integrated into modern code review workflows to improve                 aware and capable of leveraging relevant project artifacts
                                         developer experience and potentially support review efficiency.         like code diffs, source files, and requirement tickets. Notably,
                                         The research is structured around two core questions: one               participants also envisioned the assistant being valuable during
                                                                                                                 the pre-review phase, helping authors improve pull requests
                                           The first two authors contributed equally to this work.
                                           Correspondence to: chihhong@chalmers.se                               before submission. These practical insights inform how LLMs
                                           1 https://www.wirelesscar.com/                                        can be responsibly and effectively integrated into real-world
software development workflows.                                       RQ1: What practices, challenges, and expectations char-
                     II. R ELATED W ORK                               acterize modern code review processes, and where do
                                                                      developers see potential for AI-based assistance?
   Since the emergence of ChatGPT, large language models
have seen widespread adoption in all software engineering             This question aims to identify how code reviews are cur-
tasks, such as code generation, test case creation, or documen-     rently performed within the company, what challenges devel-
tation. We refer readers to a review paper [4] published in 2024    opers face, and how AI can be introduced in the code review
for a summary of recently conducted research activities. In         process, what tasks it can effectively support, and the optimal
particular, recent works [5]–[10] have explored the application     balance between automation and human involvement.
of AI, in specific LLMs, to automate or support code review
tasks. The early result from Tufano et al. [10] presents a
deep learning model trained to replicate reviewer-suggested           RQ2: How do developers perceive LLM-assisted code
code changes, aiming to partially automate the code review            review tools, and what is the preferred interaction?
process. In the era of LLMs, the work from Tufano et al. [5]
evaluates the measurable impact of AI-generated code reviews           This question explores the qualitative aspects of AI usage,
in controlled experiments over code with injected issues and        including developer trust, satisfaction, and potential barriers
code smells. It focuses on the performance of the LLM itself        to adoption, by considering different interaction modes. By
and the quantifiable effects on issue detection, time spent,        answering this question, insights are provided into the usabil-
and reviewer behavior. The work from Alami et al. [9] per-          ity, limitations, and acceptance of AI-assisted code reviews,
forms qualitative, interview-based exploration of developers’       helping to inform design decisions and future development of
emotional and cognitive responses to AI-provided feedback           such tools.
compared to human-provided feedback in code reviews. The
                                                                                        IV. M ETHODOLOGY
work from Vijayvergiya et al. [7] showcases the deployment
and evaluation of a large-scale automated system that enforces         Towards the above research questions, grounded in the
coding standards and code smells using LLMs in code reviews.        literature review, we adopt a two-phase research design that is
The work from Lin et al. [6] studies how to fine-tune LLM           aimed at understanding both the current code review processes
for better issue detection in code reviews. Similarly, the work     in a natural environment and then intervening with an AI-based
from Rasheed et al. [8] develops a multi-agent LLM-based            solution to observe the effects (see Fig. 1 for the research
system for performing autonomous code reviews, focused on           flowchart). Phase 1 involves an exploratory case study at
technical accuracy, issue detection, and actionable suggestions.    WirelessCar to thoroughly understand existing manual code
   Summarizing the above results, one of the critical gaps is the   review practices, identify specific pain points, and potential
study of the preferred interaction for an engineer assigned with    AI application areas. The goal is to identify typical workflow
the code-review task in collaboration with an LLM-enabled           steps, uncover key pain points, clarify why certain inefficien-
review assistant, which leads to the primary focus of our work      cies arise, how success is evaluated, capture the technical and
(RQ2). We focus on understanding how LLMs can support,              organizational environment, and where AI might offer possible
not replace, reviewers via practical integration strategies. We     improvements. Phase 2 aims to assess how software developers
do not consider LLMs as human replacements mainly due               at WirelessCar experience and evaluate the integration of a
to the fundamental concern that LLMs are still prone to hal-        software artifact featuring LLM-assisted code review tools into
lucinations [11]. Another differentiator is the introduction of     their review process, thereby identifying design implications
semi-structured interviews and thematic analysis to understand      and best practices.
the real potential of LLMs in code reviews, reflecting the pain        Importantly, rather than focusing on performance metrics
points of an organization developing complex software (RQ1).        or direct comparisons to existing tools as conducted in prior
Understanding the pain points (RQ1) leads to the design of          works, our emphasis on Phase 2 is on capturing qualitative
experiments and prototypical LLM-assisted code review tools         insights into how developers interact with the AI assistant,
to assess the preferred interaction (RQ2).                          what kinds of support they find valuable, and how such a
                                                                    tool might be ideally integrated into real-world code review
                 III. R ESEARCH Q UESTIONS                          practices. To make such an assessment possible, we created
   This study investigates how LLMs can be meaningfully             two variations of LLM-enabled review, namely the AI-led
integrated into modern code review workflows to improve             mode (co-reviewer) and the interactive mode. The design
developer experience and potentially support review efficiency.     of the two modes is based on challenges and improvement
The research is structured around two core questions: one           opportunities identified during Phase 1 as well as insights
diagnostic and one exploratory. The first question focuses on       collected from the literature.
understanding current code review practices and identifying            Due to our research being qualitative in nature, in both
opportunities for AI assistance, while the second question          phases, semi-structured interviews were conducted to receive
explores how developers perceive and interact with LLM-             feedback, and thematic analysis [12] has been applied to
based tools during review tasks.                                    analyze the interview scripts being collected.
     Literature
                                                                                                                     TABLE I
       review                                                                                     OVERVIEW OF I NTERVIEW PARTICIPANTS IN P HASE 1
  Conduct Database
     search with          Screen                        Insights from                        Participant ID   Role                           Team
                                      Data Analysis
   Defined search         Papers                          literature
       Terms                                                                                 P1               Quality Assurance Specialist   Team A
                                                                                             P2               Application Developer          Team A
                                                                                             P3               Software Engineer              Team A
                                                                                             P4               Software Engineer              Team A
      Phase 1                                                                                P5               Security Engineer              Team B
                                                                                             P6               Software Engineer              Team C
       Design
      Interview
                                                                                             P7               Software Engineer              Teams D & B
      Questions
                         Conduct       Thematic                          RQ1 (Modern
                                                         Results
                        Interviews     Analysis                          Code Review)    security engineers, and quality assurance specialists across
       Select
     Participants
                                                                                         four development teams. Teams ranged in size from under five
                                                                                         members to around sixteen members. The interviewees had
                                                                                         different areas of expertise, with varying levels of experience
                                                                                         and skill. The goal was to include individuals who could
      Phase 2
                                                                                         discuss both strategic and day-to-day review practices. Data
        Design
                                                                                         saturation was reached after the seventh interview, as no
                          Develop                        Conduct
     Experiment &
                        LLM- review
                                       Conduct
                                                      Post- Experiment
                                                                                         new information or themes were emerging. This decision is
      LLM- review                     Experiment
        modes
                           tools                        Interviews                       grounded in the principle that qualitative data collection can
                                                                              RQ2        be considered sufficient when additional interviews fail to
                                                                         (Developer
                                       Thematic
                                                         Results
                                                                          interaction    yield new insights [15]. Data saturation is defined as the
                                       Analysis                          with AI tools
                                                                         during code
                                                                                         point at which no new themes are observed in the data,
                                                                            review )     and studies show that although saturation often occurs within
                                                                                         twelve interviews, the basic elements of major themes are
                                                                                         frequently present as early as six [15]. The current sample
                  Fig. 1. Flowchart detailing the research workflow
                                                                                         is somewhat heterogeneous in terms of role and team, and
A. Phase 1: Understanding the existing manual code review                                the consistency of responses across participants suggested that
practices (field study)                                                                  the core aspects had been adequately captured. Although an
                                                                                         eighth interview had been scheduled, the participant canceled,
   In our field study, semi-structured interviews were con-                              but given that saturation had already been achieved, it was
ducted. Such a format balances consistency where all partic-                             decided not to reschedule the interview.
ipants receive a core set of similar questions with flexibility                             All interviews were held in English and conducted in
where researchers can ask follow-up or clarifying questions                              the participant’s active work environment, either on-site at
as fits the flow of the interview [13]. The interview ques-                              WirelessCar’s office or remotely via Microsoft Teams (two
tions were developed around domains such as code review                                  participants were interviewed remotely). This alignment with
processes, challenges in code reviews, measuring code review                             genuine working conditions is consistent with a field study
success, and current and potential AI use cases to cover                                 approach since it allows developers to reference real pull
the previously mentioned objectives. The interviews were                                 requests, team communication channels, and examples of
designed to fit comfortably within a 30-minute timeframe.                                ongoing tasks. They could describe, for example, how a large
However, in practice, the interviews ranged from 15 to 40                                refactoring pull request (PR) or an urgent bug fix impacted
minutes each, with most lasting approximately half an hour.                              their review process in real-time. Conducting interviews in this
   We used convenience sampling [14] by interviewing peo-                                natural setting helps reinforce the authenticity of participant
ple within the WirelessCar who were able and willing to                                  responses and results in findings consistent with everyday
participate. Participants were recruited via announcements on                            workflows at WirelessCar.
Slack channels and informal Slack messages that announced
the study’s purpose and form of the interview. Interviewees
                                                                                         B. Phase 2: Evaluating the LLM-enabled code review (field
who handled different parts of the code and were reviewers at
                                                                                         experiment)
varying seniorities were sought. Additionally, some intervie-
wees were from the same development team to gain multiple                                   1) Data Collection: To explore developer experience with
perspectives from the same team. Despite being limited in                                the AI assistant during code reviews, two data collection meth-
randomness, we believe our sampling still enables insights into                          ods were employed to capture user perspectives and behavioral
a relatively wide range of review practices.                                             interaction patterns. The primary data source consisted of
   A total of seven participants were interviewed and are                                post-interaction interviews with each participant. These were
listed in Table I. The interviewees varied in gender and                                 supported by a secondary data source consisting of researcher
age, and the sample included software engineers, developers,                             observation notes recorded during review sessions.
                          TABLE II
OVERVIEW OF E XPERIMENT AND I NTERVIEW PARTICIPANTS IN P HASE 2

    Participant ID   Role                           Team
    P1               Quality Assurance Specialist   Team A
    P2               Application Developer          Team A
    P3               Software Engineer              Team A
    P5               Security Engineer              Team B
    P7               Software Engineer              Teams D & B
    P8               Software Engineer              Team E
    P9               Software Engineer              Team A
    P10              Software Engineer              Team E
    P11              Software Engineer              Team F
    P12              Software Engineer              Team G

   Participants were recruited again through convenience sam-
pling, where individuals who participated in the earlier phase
of the study were invited to return for Phase 2. However,
only five were available and agreed to participate again. To
reach a total of ten participants, five additional individuals
were recruited via internal Slack channels, where the study’s
purpose and structure were briefly described. Of the ten
participants, four belonged to the team responsible for the pull
requests used in the experiment, while the remaining six were
from other teams, allowing comparison across varying levels
of codebase familiarity. Table II provides an overview of the
participants, including their roles and team affiliations. The
code used in the experiment originated from Team A, which          Fig. 2. Screenshot of the LLM-assisted code review interface in Mode
is the team associated with the familiar participants.             B, reviewing a pull request from an open-source project available at
   2) Experiment Setup: The field experiment is designed to        https://github.com/ogen-go/ogen/pull/1440.
evaluate the developers’ experiences with LLM-based code
review assistance under two distinct interaction modes that             query the AI for clarification or more details about the
were selected based on the findings from the Phase 1 field              summarized areas. This mode directly targeted the chal-
study. As indicated by the interview data in that earlier               lenge previously identified as lacking immediate context,
phase, developers most frequently identified a need for clearer         particularly for large or complex PRs.
up-front summaries of code changes as well as on-demand               • Mode B: Interactive Assistant – In this mode, the
explanations for specific architectural or contextual details.          reviewer reviewed the code in their typical manner. The
   In each iteration of the experiment, a single participant en-        AI assistant did not proactively provide a summary or
gaged in a traditional code review scenario, conducted within           suggest issues upfront. Instead, the reviewer was free to
their familiar development environment using their usual tools          consult the AI on demand, requesting clarifications about
and platforms. In addition to these standard resources, the             specific parts of the code or asking higher-level architec-
participant was provided access to our created LLM code                 tural questions. Reviewers were encouraged to ask tar-
review assistant as illustrated in Fig. 2. The task assigned to         geted queries rather than requesting an overall summary
the participant was to perform two code reviews, each on a              of the changes. Here, the AI assistant only responded
different pull request from two separate repositories within the        when explicitly prompted. This design choice not only
company. The participant followed a different interaction mode          reflected the Phase 1 feedback on needing a lightweight,
with the AI assistant for each review. All sessions took place          on-demand tool but also addressed an identified challenge
in conditions that mirrored each participant’s normal working           in related studies [5], where automatically highlighted
situation as closely as possible.                                       lines can cause reviewers to miss other important areas.
   The two interaction modes are described below:                       By making the AI passive, reviewers maintained their
   • Mode A: Co-Reviewer – In this mode, the AI assistant               usual workflow and examined the entire codebase without
      automatically generated a summary of the code under               unconsciously depending on the AI’s initial hints.
      review, highlighting major changes and any potential            To minimize review variability while still enabling com-
      points of interest or concern, before the reviewer started   parison across interaction types, two specific pull requests
      their own examination. The reviewer could then use this      of similar size and complexity were selected from the Wire-
      information to guide their review, optionally asking the     lessCar codebase. The selected pull requests each involved
      AI-assistant follow-up questions. The participant could      a moderate amount of change, requiring genuine reviewer
effort without being excessively large or trivial. Before the
first experiment session, a pilot run was conducted with two                                                     Agent
                                                                                                              Co- Reviewer
internal developers who were not part of the main participant
pool. The pilot involved a walkthrough of the tool, the review
task, and the interaction modes, followed by an informal test
of the tool using the selected pull requests. The pilot was used
to assess the suitability of the selected PRs, detect any major
usability or technical issues in the tool, and evaluate whether
the introduction and guidance provided to participants were                                                                   Sub- Agent
                                                                                                                               start_review
sufficiently clear and effective. Each participant in the actual
experiment then reviewed both PRs, using Mode A for one PR
                                                                            search_pr   search_code   search_requirement
and Mode B for the other. The assignment of modes to PRs
was rotated across participants to mitigate ordering effects.
By having all participants conduct the same two code reviews
with alternating modes, this approach allowed for a more
controlled comparison of interaction styles while ensuring the
                                                                                                         search_code       search_requirement
tasks remained realistic and relevant to actual code review
practices.
                                                                             Fig. 3. Agentic tool structure in Co-Reviewer mode.
   To investigate how varying levels of codebase familiarity
may influence the use of the AI assistant, both developers be-     on GitHub: frontend2 and backend3 . While not intended to
longing to the team that owns the selected PRs and developers      be a production-level system, the artifact was designed to be
from unrelated teams were invited to participate. Phase 1 in-      realistic and usable enough to engage developers meaning-
terviews indicated that limited contextual knowledge can have      fully. It supported live interaction through a chat interface,
negative effects on the review quality, and therefore, measuring   maintained session-specific context, and allowed researchers
differences in AI reliance across these two participant groups     to configure session parameters such as interaction mode and
was expected to produce further insights.                          PR data source.
                                                                      The artifact consisted of a chat interface connected to a
   Before starting the code review sessions, each participant
                                                                   backend system that integrated OpenAI’s o4-mini4 language
was given a short onboarding briefing to explain the tool’s
                                                                   model via API. The artifact was also supported by a Retrieval
features as well as the structure and setup of both the study
                                                                   Augmented Generation (RAG) infrastructure built with Lla-
and the experiment. The two different interaction modes were
                                                                   maIndex5 . This setup enabled the AI assistant to produce more
introduced, along with guidance on how to effectively prompt
                                                                   informed and context-aware responses by using project data
the AI assistant to obtain useful and relevant responses. The
                                                                   such as code diffs, related source code files, and associated
participant then completed the two review sessions consecu-
                                                                   feature requirements (Jira tickets). The RAG index had to be
tively. While no in-depth feedback or direct assistance was
                                                                   manually prepared and indexed before experiments, ensuring
provided during the sessions, limited guidance was offered
                                                                   complete control over the data available to the model in each
when needed, for example, if participants inquired about spe-
                                                                   experimental session. As highlighted by the literature and the
cific ways of interacting with the assistant. Participants were
                                                                   Phase 1 interview results (see Sec. V-A2), lacking a broader
also encouraged to think aloud during the experiment, often
                                                                   repository context can lead to superficial AI feedback that
verbalizing their reasoning, confirming the AI’s suggestions,
                                                                   overlooks critical design or architectural concerns. This RAG
or commenting on its usefulness. If the assistant’s response did
                                                                   setup ensured that the LLM can reference deeper project-level
not meet expectations, participants were occasionally guided to
                                                                   information on demand. This setup not only enhanced the
try rephrasing or retrying the query. Researchers were present
                                                                   AI assistant’s capacity to generate context-aware suggestions
to observe the sessions, record notes, and perform the post-
                                                                   but also directly targeted the gap in existing tools and recent
session data collection. Following the review sessions, short
                                                                   studies on the subject.
semi-structured interviews were conducted with the participant
to reflect on their experience across the two modes and in            Internally, the assistant interacts with three core semantic
comparison to their regular code review workflow.                  tools:
                                                                     •   search_pr: accesses PR diffs and metadata.
   3) Artifact Implementation: The software artifact developed       •   search_code: provides the full, unmodified source
for this study was a web-based chat interface designed to                code of the repository.
explore and evaluate different interaction styles in AI-assisted
code reviews. Its primary purpose was to enable structured          2 https://github.com/BearPays/code-review-assistant-ui
experimentation by allowing researchers to observe how de-          3 https://github.com/BearPays/code-review-assistant-back
velopers interact with AI assistance in different contexts. The     4 https://platform.openai.com/docs/models/o4-mini

source code for the artifact is freely available (under GPLv3)      5 https://www.llamaindex.ai/
   •  search_requirements: contains the feature require-                           time to regain focus, and one interviewee highlighted the time
      ment (the Jira ticket) motivating the PR.                                    lost cause of this:
   In Mode A (Co-Reviewer), a fourth tool, start_review,
was added. This tool contained a sub-agent that was designed                         “As soon as you need to context switch, even if it’s just
to perform an initial, structured code review based on the full                      a three-minute thing, it’s 20 minutes of lost time.” [P7]
PR data and guided by a detailed review-specific prompt. Un-
like the main agent, this sub-agent did not use search_pr, as                         Several interviewees explained that they sometimes lack
all PR data was injected into its initial context via a prompt.                    sufficient context when reviewing the code. Sometimes,
This ensured that the agent considers everything in the PR                         important details about why the change was made or its
data and examines each file change. By retrieving the PR data                      expected impact are missing from the PR description. This
via a query engine, the agent might not consider all the data                      increases the time it takes for the reviewer to comprehend the
as required when generating a complete code review of all                          PR and effectively point out defects or problems.
changes. The agentic structure for this setup is shown in Fig. 3.                     3) Current Use of AI in Software Development: The inter-
                                                                                   views revealed that common AI tools like GitHub Copilot7
                               V. R ESULTS                                         and ChatGPT8 are commonly used for development tasks.
                                                                                   Interviewees mentioned tasks like writing boilerplate code,
A. Results from Phase 1
                                                                                   assisting with syntax, and quickly generating documentation.
   Six themes emerged from the thematic analysis of the                            One example mentioned was:
qualitative data and can be seen in Table III.
   1) Observed Code Review Process: When reviewing the                               “[...] as to help to create the boilerplate stuff, it’s out-
informal review process at WirelessCar and their practices,                          standing, right? I mean, you do it in 30 seconds instead
it appears to be similar to the typical asynchronous, tool-                          of a couple of hours. So I try to use it as much as possible
supported nature of modern code review (MCR) practices.                              during the development process.”                       [P7]
However, the reliance on informal assignment and com-
munication sometimes through Slack introduces variability,
                                                                                      However, not all teams are allowed to use AI-generated
which might contrast with the structured practice of assigning
                                                                                   code or share information (such as source code) with AI tools.
a specific reviewer to the code patch commonly found in
                                                                                   Furthermore, the teams that are allowed to use AI tools only
MCR practices. Additionally, WirelessCar places significant
                                                                                   utilize them via an enterprise subscription, where the data
emphasis on contextual understanding and relies heavily on
                                                                                   provided is not used for training the models utilized by the
team members with domain expertise to assess the critical
                                                                                   tools. This ensures that no data is leaked from the organization
components. This contrasts with the broader responsibility-
                                                                                   via the use of AI tools.
sharing model commonly found in large organizations that                              All interviewees who use AI tools reported positive experi-
apply MCR.6                                                                        ences in their development work. None of the interviewees
   2) Common Challenges in Code Reviews: One of the                                reported using AI tools as part of the formal code review
most frequently mentioned challenges across the developer                          process. One interviewee did mention that some reviewers
interviews was the issue of delayed reviews. Situations were                       might occasionally paste code into tools like ChatGPT for
described where PRs remained unreviewed for extended peri-                         clarification or explanation during reviews. However, beyond
ods, often requiring repeated reminders for a reviewer to take                     such informal use, AI has not been formally integrated into
action. One interviewee described it as:                                           the code review workflow in any of the interviewed teams.
                                                                                      4) Potential AI Use Cases in Code Review: The intervie-
   “Sometimes you need to ping people more often, and                              wees expressed interest in potential AI integrations with the
   sometimes the PR is very big, so people don’t dare to                           code review processes. They mentioned features like sum-
   pick it up”                                     [P2]                            marizing PR changes and accompanying descriptions where
                                                                                   AI could generate a concise summary and help reviewers
   Several interviewees reported difficulties regarding review-                    to quickly understand the intent of a code change. One
ing large or complex PRs. PRs that combine new features,                           interviewee mentioned:
refactoring, and changes to infrastructure often become over-
whelming. They note that this can result in more superficial                         “When you create the pull request, an AI bot could say,
reviews or longer delays.                                                            ’Hey, you’re trying to achieve this—do you want this as
   Context switching was also noted as another major chal-                           your summary or description?”                     [P5]
lenge. Developers mentioned that the cognitive burden of
pausing ongoing work to review code, not at all related to                            Interviewees also mention possibilities such as AI assisting
their current work, to be challenging. This requires additional                    in validating whether code meets stated requirements. Addi-
  6 Due to space limits, quotes collected from the interview as well as detailed     7 https://github.com/features/copilot

findings are not listed.                                                             8 https://chatgpt.com/
                                                                 TABLE III
                           I DENTIFIED THEMES AND THEIR DESCRIPTIONS FROM ANALYSIS OF INTERVIEW DATA IN P HASE 1.

     Theme                                       Description
     Informal Review Process and Practices       Describes how teams coordinate and manage code reviews in practice, including informal
                                                 communication, tool use, and the absence of structured processes or metrics.
     Review Strategies and Evaluation Focus      Captures what developers focus on during the actual code review process.
     Learning, Knowledge, and Review Expertise   Explores how code reviews serve as opportunities for learning and knowledge sharing within
                                                 teams. It also captures the role of reviewer expertise in conducting effective reviews and the
                                                 challenges that arise when reviewers lack sufficient understanding of the codebase or architecture.
     Code Review Challenges                      Identifies recurring challenges and inefficiencies encountered in the code review process.
     Current AI adoption                         Describes the current state of AI tool usage in development and code review.
     Possible AI adoption in code reviews        Describes developers’ expectations, suggestions, and concerns regarding future AI assistance in
                                                 code reviews.
                                                                TABLE IV
                              I DENTIFIED THEMES AND THEIR DESCRIPTIONS FROM ANALYSIS OF DATA FROM P HASE 2.

    Theme                                         Description
    Accuracy, Reliability, and Trust              Focuses on the perceived correctness of AI-generated feedback, concerns about over-reliance,
                                                  and varying levels of trust in the assistant’s recommendations.
    Efficiency and Thoroughness                   Captures how the assistant affects review speed, cognitive load, issue detection, and the overall
                                                  thoroughness of the code review process.
    Integration Expectations and Limitations      Highlights developer expectations for seamless integration, responsive design, and context-aware
                                                  suggestions, while also surfacing frustrations related to current UX and tooling limitations.
    Usage Contexts and                            Describes how interaction with the assistant varied based on review context, including preferences
    Interaction Patterns                          for different modes, alternative usage strategies, and team-specific practices.


tionally, interviewees highlighted the potential for AI to detect          stated:
hidden bugs or vulnerabilities, such as race conditions, de-
pendency issues, or other subtle defects that human reviewers                 “As I see it, they were quite accurate [...] It was quite
might overlook. As one developer put it:                                      nice, not all of them, but a lot of them.”          [P9]

  “An AI would probably be able to identify a race condi-                     In multiple cases, the assistant’s output was described as
  tion, for instance, which, as I said, is an example that’s               confirming the developer’s own thoughts or surfacing
  borderline impossible to catch on the fly. In three minutes,             something they might not have otherwise caught. Observa-
  you’re never going to find that.”                      [P7]              tion notes also reflect this, with one session noting that “the
                                                                           user said the AI caught exactly what he was looking for in
   Finally, some interviewees mentioned potential drawbacks                a certain file.” In another session, the reviewer remarked that
of integrating AI into the code review process. These were                 “the summary gave something that he would not have seen.”
mostly concerns about security risks and false positives, which
could reduce the reviewer’s trust in the AI assistant and divert              Several participants also reported instances where the as-
their attention from real issues. As one interviewee put it:               sistant produced incorrect or unclear suggestions. One par-
                                                                           ticipant questioned whether the tool was even “doing what it
  “The problem with those kinds of checks is that, if they’re              was asked,” while another described the assistant incorrectly
  not good enough, you stop reading them. We see that all                  flagging a missing import. One participant noted:
  the time, you get flooded with false positives, and then
  you miss the real issues because you start ignoring the                     “Sometimes it says some slightly strange things.”                   [P8]
  feedback.”                                            [P7]
                                                                              When asked about concerns, participants expressed different
B. Results from Phase 2                                                    perspectives. Several participants warned of the risk of over-
                                                                           relying on the assistant, especially in Mode A, where the
  Table IV provides an overview of the themes along with                   assistant led the review:
descriptions of the themes.
  1) Accuracy, Reliability, and Trust: Participants frequently                “It feels like I might get a bit colored by getting the
commented on the accuracy of the assistant’s feedback and                     improvements from the LLM [...] I feel like maybe I could
how this influenced their trust in the tool. Several interviewees             miss something else, because I would focus on those
described the assistant as generally accurate and capable                     improvements a lot.”                                 [P3]
of identifying relevant issues. For example, one participant
  While some view using AI tools as risky, not all participants       “But I really like the integration with the requirements
saw the assistant as risky. Some viewed it as a low-stakes            part, because if I open up [a PR] and I don’t know what
addition to the workflow, especially when its use remained            it’s about. [...] The first thing I do every time is I open
optional, even if it is not always accurate:                          the [Jira] ticket anyway, because I need to see what is
                                                                      supposed to have been achieved here. So I think that’s a
  “As long as there’s an opt-out option, there’s no real harm         really nice functionality to have”                     [P3]
  in it.”                                                [P5]
                                                                       However, some participants noted that the assistant occa-
                                                                    sionally surfaced low-priority or unclear findings. This was
  “If we miss 10 [issues] today, we might miss two with a
                                                                    also observed during review sessions, where participants some-
  tool like this.”                                  [P9]
                                                                    times expressed difficulty distinguishing important findings
                                                                    from minor ones, especially in lengthy summaries gener-
   The role of trust emerged as a key factor in shaping how         ated by the assistant.
participants viewed the tool. A few emphasized that for the
tool to be useful or even used in general, it must be trusted,        3) Design Expectations and Limitations: Many participants
but not blindly. Misplaced trust in the tool could lead to wasted   shared expectations about how an AI assistant for code review
effort if the tool isn’t accurate:                                  should behave and be integrated. A recurring theme was
                                                                    the desire for seamless integration into existing workflows
  “So I think that worked really well, especially with larger       and tools. Rather than switching to a new interface, several
  [PRs] [...] you can at least use it if you trust it.” [P7]        participants expressed that it would be preferable to access
                                                                    the assistant directly from familiar environments like GitHub,
                                                                    Slack, or their IDEs. As one participant put it:
  “I could go on for hours, just to realize I can never
  do this. Then I’ve just lost a few hours trying to pursue           “I think most of the developers don’t want to use some-
  something that wasn’t possible.”                     [P5]           thing new, like a [new] UI, but rather have an integration
                                                                      to what exists.”                                    [P11]
   2) Efficiency and Thoroughness: A strong theme was the
AI’s impact on code review efficiency and the thoroughness or          Building on this, another participant described a preference
quality of reviews. Developers reported that the AI assistant       for having the assistant’s comments embedded directly into
could speed up the review process, reduce reviewers’                GitHub’s interface, with expandable in-line comment boxes,
workload on tedious tasks, and potentially catch more               while also having the ability to further ask questions in a chat
issues, although some participants remarked that it sometimes       interface. Yet another participant described how having it in
focuses on low-priority findings, introducing noise.                the pipeline through a Slack bot could be useful.

                                                                      “Maybe a Slack auto bot could even be triggered on each
   Beyond efficiency, participants also pointed to improve-           message [...] and a full review could be dropped as a
ments in review quality. Some noted that the assistant could          message under that thread.”                       [P11]
identify issues that might otherwise go unnoticed:
                                                                      Beyond integration, participants also critiqued how the LLM
  “There are probably findings you get in the report that           assistant’s output was presented. Several interviewees felt that
  you don’t find when you do it manually.”         [P10]            the LLM feedback was overly long or difficult to scan. One
                                                                    participant noted:
   Additionally, interviewers felt that the assistant would be
particularly helpful on large pull requests where it would be         “I mean, what’s important is that it very clearly lists the
difficult for a human reviewer to catch everything:                   file. I’d rather have it list the file and the line number and
                                                                      be very specific, in a short way.”                        [P5]
  “It’s taken someone two weeks to write it [...] giving it
  15 minutes, you won’t have a chance to understand it,               Response time was another point of friction. While some
  at least not well enough to find the hard stuff. I would          delays were tolerated, long wait times were cited as a major
  imagine that the tool would actually raise a flag for a           barrier to adopting the tool in real development workflows:
  potential deadlock or race condition as well.”      [P7]
                                                                      “I think the speed and accuracy are mainly what need to
  For some participants, the assistant reduced the effort in-         be improved. [...] I wouldn’t use this if it took, I don’t
volved in reviewing by removing the need to search through            know, how many minutes it took for it to respond.” [P3]
the codebase or external documentation:
   One participant reflected on whether the quality of in-         Many participants saw the assistant, especially mode A, as
teraction also depended on their own ability to ask good         valuable for newcomers:
questions:
                                                                   “I think if I were in a new team, and I am unsure what
  “Maybe my way of asking questions was also wrong. I did          is happening, then it could be really good to start with a
  not always feel like I got the response that I was asking        summary.”                                            [P8]
  for. So, I might need to learn how to be more detailed in
  my questions.”                                     [P10]
                                                                   “Yeah, if you can write questions like ’What is this?’ or
                                                                   ’What is this really about?’, it could also be a very good
  Many limitations were traced to a lack of access to broader
                                                                   tool to get to know the codebase and to learn as a new
context, such as architectural documentation, internal
                                                                   guy.”                                                 [P9]
conventions, or metadata:
                                                                   Additionally, some saw mode A as useful in teams where
  “Ideally, you want to inject as much relevant information
                                                                 code review standards are lower or in teams that prefer
  as possible [...] like the JIRA ticket, relevant [documen-
                                                                 other methods for reviewing code, such as pair program-
  tation] pages, the codebase itself, the README, and any
                                                                 ming. In such cases, the assistant would serve as a fallback
  similarly named repositories that might be connected to
                                                                 mechanism.
  the same service.”                                    [P5]
                                                                   “I think it would be great for those who usually just skim
   Some participants also highlighted that the LLM-assistant’s     through and say, ’It looks good to me’. [...] I think the
usefulness depended in part on how good the documen-               biggest effect would be for those developers, I guess, and
tation and PR descriptions are to begin with. During the           those teams.”                                         [P5]
testing, one reviewer reflected that the tool could help keep
the documentation up-to-date by suggesting updates that align
                                                                   Mode B was less preferred in general, but some participants
with PR changes.
                                                                 remarked that in cases where they are already familiar with
                                                                 the codebase or if they wanted to maintain full control
   4) Usage Contexts and Interaction Patterns: Participants
                                                                 over the review process, they would prefer Mode B:
expressed a range of preferences, strategies, and situational
factors that shaped how they interacted with the AI assistant,
often shaped by the review context. These patterns included        “But if it’s in some codebase I already know, some
both the predefined interaction modes: Mode A (Co-Reviewer)        codebase where we have a lot of experience and have
and Mode B (Interactive Assistant), as well as emergent            worked in it a lot. It could probably be nice to have [Mode
workflows that blended or extended beyond them.                    B].”                                                   [P8]

   Many participants found Mode A (Co-Reviewer) espe-              In some cases, participants preferred a combination of
cially helpful for getting oriented in a pull request. They      both modes or expressed that the preferred interaction mode
described the high-level summaries and suggestions provided      depended on the situation:
at the beginning of the review as useful for gaining quick
context, particularly in unfamiliar or complex codebases:
                                                                   “I think I’m 50/50 [...] both are useful. One is on demand,
                                                                   the other one is on its own.”                          [P1]
  “I prefer this one [Mode A] where you actually get the
  overview directly [...] it had a lot of good pointers, that
                                                                   Several participants proposed additional usage patterns
  it already found.”                                  [P12]
                                                                 that were not strictly defined by the study design. For instance,
                                                                 some saw mode A as useful for the author before submitting
  “The first engine [Mode A] that gave me a breakdown of         the PR, rather than during review:
  everything [...] that was quite clever, and I would gladly
  use that.”                                           [P7]        “I feel it might not be as much of a review help. I think
                                                                   it might be a pre-review help.”                    [P10]
   Mode A was also described as particularly useful for low-
risk PRs:                                                          Others proposed an alternative interaction mode where
                                                                 engineers conducted a human-led review first and then used
  “Let’s say the change is relatively small and it’s not         the assistant to validate or catch anything they might have
  causing any risk, then I would definitely go with the first    missed:
  one [Mode A], where I let AI do most of the work.” [P11]
  “You start out with it just to sum up what the code is           pull requests. However, concerns around trust, false positives,
  doing. Then I look for issues, and then I can ask, ’Are          response latency, and integration friction remain. While most
  there any further issues?”                         [P3]          participants preferred the AI-led mode in unfamiliar or low-
                                                                   risk scenarios, preferences were context-dependent, with some
   Participants also frequently noted that Mode A was espe-        favoring human-led reviews when code familiarity or critical-
cially helpful for large PRs:                                      ity increased.
                                                                      This study contributes practical insights into how LLMs can
                                                                   complement human reviewers, rather than replace them. Our
  “Especially for large PRs, it’s nice to get the breakdown
                                                                   findings suggest a promising path forward: integrating AI as-
  on what’s happening [...] because usually, you always
                                                                   sistance more tightly into existing development environments,
  have to do that sort of manually anyway.”             [P3]
                                                                   improving response quality and speed, and offering adaptive
                                                                   interaction modes tailored to developer needs.
   However, there was also some uncertainty about how ef-
fective the assistant would be at scale. One participant                                        R EFERENCES
expressed concerns about the assistant’s ability to handle very     [1] J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman,
large codebases or complex business logic:                              D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat et al., “Gpt-4
                                                                        technical report,” arXiv preprint arXiv:2303.08774, 2023.
                                                                    [2] A. Yang, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Li, D. Liu,
  “I think it’s going to be a bottleneck for such things,               F. Huang, H. Wei et al., “Qwen2.5 technical report,” arXiv preprint
                                                                        arXiv:2412.15115, 2024.
  because there will be so many moving parts in it, so much         [3] T. Mesnard, C. Hardin, R. Dadashi, S. Bhupatiraju, S. Pathak, L. Sifre,
  business logic going around.”                        [P1]             M. Rivière, M. S. Kale, J. Love et al., “Gemma: Open models based
                                                                        on gemini research and technology,” arXiv preprint arXiv:2403.08295,
                                                                        2024.
                      VI. I MPLICATIONS                             [4] X. Hou, Y. Zhao, Y. Liu, Z. Yang, K. Wang, L. Li, X. Luo, D. Lo,
   Our study yields several practical implications for integrat-        J. Grundy, and H. Wang, “Large language models for software engi-
                                                                        neering: A systematic literature review,” ACM Transactions on Software
ing LLMs into code review workflows. First, AI assistance               Engineering and Methodology, vol. 33, no. 8, pp. 1–79, 2024.
should be embedded within developers’ existing tools (such          [5] R. Tufano, A. Martin-Lopez, A. Tayeb, S. Haiduc, G. Bavota et al.,
as GitHub, GitLab, IDEs, or Slack) to minimize friction and             “Deep learning-based code reviews: A paradigm shift or a double-edged
                                                                        sword?” arXiv preprint arXiv:2411.11401, 2024.
support natural adoption. Second, output must be concise,           [6] H. Y. Lin, P. Thongtanunam, C. Treude, and W. Charoenwet, “Improving
well-structured, and actionable, prioritizing critical findings         automated code reviews: Learning from experience,” in International
with precise references to affected files and lines. Fast re-           Conference on Mining Software Repositories (MSR). ACM, 4 2024,
                                                                        pp. 278–283.
sponse times are essential to preserve reviewer flow, although      [7] M. Vijayvergiya, M. Salawa, I. Budiselić, D. Zheng, P. Lamblin,
more comprehensive agentic reviews may be acceptable when               M. Ivanković, J. Carin, M. Lewko, J. Andonov, G. Petrović, D. Tarlow,
integrated into automated pipelines. Supporting both proactive          P. Maniatis, and R. Just, “AI-assisted assessment of coding practices
                                                                        in modern code review,” in Proceedings of the 1st ACM International
(AI-led summaries) and reactive (on-demand Q&A) modes of                Conference on AI-Powered Software.            Association for Computing
interaction is key, with a general developer preference for             Machinery, 2024, pp. 85–93.
AI-led summaries in large or unfamiliar pull requests. For          [8] Z. Rasheed, M. A. Sami, M. Waseem, K.-K. Kemell, X. Wang,
                                                                        A. Nguyen, K. Systä, and P. Abrahamsson, “AI-powered code review
meaningful support, the assistant must be context-aware and             with LLMs: Early results,” arXiv preprint arXiv:2404.18496, 2024.
have access to relevant information such as code diffs, source      [9] A. Alami and N. A. Ernst, “Human and machine: How software
files, and requirement documents. While our tool addressed              engineers perceive and engage with AI-assisted code reviews compared
                                                                        to their peers,” arXiv preprint arXiv:2501.02092, 2025.
this via a retrieval-augmented setup, participants still high-     [10] R. Tufano, L. Pascarella, M. Tufano, D. Poshyvanyk, and G. Bavota,
lighted the need for deeper contextual integration. Finally, an         “Towards automating code review activities,” in 2021 IEEE/ACM 43rd
LLM-enabled assistant also shows promise as a pre-review                International Conference on Software Engineering (ICSE). IEEE, 2021,
                                                                        pp. 163–174.
aid, helping authors catch simple issues before submitting         [11] L. Huang, W. Yu, W. Ma, W. Zhong, Z. Feng, H. Wang, Q. Chen,
a pull request, thus improving code quality upstream in the             W. Peng, X. Feng, B. Qin et al., “A survey on hallucination in large
development lifecycle.                                                  language models: Principles, taxonomy, challenges, and open questions,”
                                                                        ACM Transactions on Information Systems, vol. 43, no. 2, pp. 1–55,
                VII. C ONCLUDING R EMARKS                               2025.
                                                                   [12] V. Braun and V. C. and, “Using thematic analysis in psychology,”
   This paper presented a field study and field experiment              Qualitative Research in Psychology, vol. 3, no. 2, pp. 77–101, 2006.
conducted at WirelessCar to explore the integration of Large       [13] O. A. Adeoye-Olatunde and N. L. Olenik, “Research and scholarly
                                                                        methods: Semi-structured interviews,” JACCP, vol. 4, no. 10, pp. 1358–
Language Models (LLMs) into real-world code review work-                1367, 2021.
flows. The study surfaces persistent challenges in current         [14] I. Etikan, S. A. Musa, R. S. Alkassim et al., “Comparison of convenience
review practices, such as context switching, reviewer fatigue,          sampling and purposive sampling,” American journal of theoretical and
                                                                        applied statistics, vol. 5, no. 1, pp. 1–4, 2016.
inconsistent review depth, and developer perceptions of how        [15] G. Guest, A. Bunce, and L. Johnson, “How many interviews are
LLMs can augment the process. By evaluating two interaction             enough?: An experiment with data saturation and variability,” Field
modes (AI-led reviews and on-demand assistance), we found               Methods, vol. 18, no. 1, pp. 59–82, 2006.
that developers generally value AI-generated summaries and
contextual clarifications, particularly in large or unfamiliar

