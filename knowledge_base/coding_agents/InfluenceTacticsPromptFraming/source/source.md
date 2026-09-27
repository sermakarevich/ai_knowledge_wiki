# Do Influence Tactics Matter? Investigating Prompt Framing Effects in LLM Code Generation
Source: https://arxiv.org/abs/2608.11513v1
Kind: pdf
Fetched: 2026-09-23T19:55:05.547410+00:00
Tool: pdftotext
Research-Target: /Users/sergii/.ai/knowledge/research_topics/coding_agents/research/ai_coding_best_practices
Topic: coding_agents

                                         Do Influence Tactics Matter? Investigating Prompt
                                         Framing Effects in LLM Code Generation

                                         Alex Deaconu*   · Anubhav Gupta*   ·
                                         Manaal Basha · Nicholas Haydu · Gema
                                         Rodríguez-Pérez




                                         This version of the article has been accepted for publication, after peer review, but is not the
                                         Version of Record and does not reflect post-acceptance improvements or any corrections. The
                                         Version of Record is available online at: http://dx.doi.org/10.1007/s10664-026-10934-z. Use




arXiv:2608.11513v1 [cs.SE] 11 Aug 2026
                                         of this Accepted Version is subject to the publisher’s Accepted Manuscript terms of use.


                                         Abstract Large Language Models (LLMs) are increasingly integrated into software
                                         engineering workflows, helping developers write, debug, test, and maintain code.
                                         While prompt wording and structure are known to influence model performance, the
                                         impact of psychologically inspired prompt framings remains unexplored. This study
                                         investigates whether different psychology-based communication strategies that hu-
                                         mans use to persuade or motivate others can lead to more effective prompt framing,
                                         which may, in turn, affect LLM behaviour in coding tasks. Drawing on Yukl & Falbe’s
                                         well-known taxonomy, we operationalized eight influence tactics (like rational persua-
                                         sion, ingratiation, and exchange) into reproducible prompt templates. These prompt
                                         templates were evaluated across five leading open-weight LLMs using two widely
                                         adopted benchmarks: LiveCodeBench and SWE-bench Verified. We assessed the re-
                                         sulting code output on four key software quality dimensions: functional correctness,
                                         quality, maintainability, and security. Our results show that certain influence-induced
                                         prompt framings, particularly those emphasizing urgency, were associated with re-
                                         duced correctness and security. This work presents the first large-scale empirical
                                         study of influence-induced prompt framing in software engineering tasks, offering in-
                                         sights into how linguistic cues may shape LLM outputs. We conclude with practical
                                         insights for designing transparent and interpretable human-AI interactions in code
                                         generation.


                                         Keywords Empirical Software Engineering · Software Quality · LLMs · GenAI ·
                                         Human Factors


                                         * Alex Deaconu and Anubhav Gupta shared first authorship.


                                         Extended author information available on the last page of the article
2                                                                Alex Deaconu*    et al.


1 Introduction

Large Language Models (LLMs) have rapidly emerged as influential tools in Software
Engineering (SE), supporting a variety of tasks such as code synthesis [50], API docu-
mentation [17], automated bug repair [73], and supporting testing workflows [74]. As
LLMs become more integrated into professional development workflows, recent stud-
ies suggests that the way developers phrase and frame their prompts can influence
model behaviour and generated code quality [20, 66]. For instance, Tony et al. [62]
found that the Recursive Criticism and Improvement technique reduced security
weaknesses across some LLMs. Similarly, Liu et al. [37] showed that chain-of-thought
prompt designs notably improve ChatGPT’s coding performance.
    Prior work has explored syntactic prompt engineering [9], reasoning-based strate-
gies like chain-of-thought [65,37], and the role of explicit instructions in improving
code generation [8]. In contrast, research in organizational psychology has established
that variations in request framing can substantially impact human compliance and
performance [21]. For example, Yukl & Falbe’s influential taxonomy of influence tac-
tics [70] shows how subtle shifts in approach, such as appeals to rational arguments,
expressions of urgency, or offers of reciprocity, can change outcomes in collaborative
settings. Translating this idea to software engineering, this paper investigates: To
what extent do prompt framings inspired by these influence tactics lead to measur-
able differences in LLM-generated code?
    This question is particularly relevant as SE increasingly relies on interactive
human-AI workflows where developers iteratively refine prompts to achieve reliable,
maintainable, and secure code. Human developers naturally tend to use rational
persuasion to justify design decisions, invoke pressure to communicate urgency under
tight deadlines, or suggest exchanges to motivate cooperation [30]. Understanding
how psychologically inspired influence tactics in prompt design, particularly those
shaping interpersonal communication, influence model outputs is important as it
can improve prompt design and reveal potential risks when AI-assisted development
tools are used in real-world SE workflows.
    Recent research has shown that subtle differences in tone and wording, such
as politeness [49], can alter the length and affective tone of responses from GPT-4,
with more polite prompts leading to longer and more positive outputs. Yin et al. [68]
observed that medium to high politeness levels correspond to fewer comprehension
errors. In adversarial contexts, socially engineered prompts that mimic persuasive or
deceptive framing have been found to increase the success rate of prompt injection at-
tacks [13]. These findings suggest that linguistic cues associated with human commu-
nication patterns may shape how LLMs retrieve and compose information. Because
LLMs are trained on large corpora of human-authored communication, they may
learn statistical associations between particular pragmatic framings and particular
response styles. Under this interpretation, psychologically inspired prompt framings
act as distributional cues that may steer generation behaviour without requiring the
model to understand persuasion or social intent in a human sense. This motivates our
investigation into whether influence-tactic framings produce measurable differences
in code generation outcomes.
    In this paper, we present the first empirical study examining how prompt fram-
ings inspired by psychological influence tactics affect LLM outputs in code generation
tasks. Drawing on Yukl & Falbe’s [70] taxonomy of psychological influence strate-
gies, we operationalized eight tactics into reproducible prompt templates. For each
Do Influence Tactics Matter?                                                         3


tactic, we used items from the Influence Behavior Questionnaire-General (IBQ-G),
a validated instrument for identifying the usage of influence tactics, as requirements
to build prompt templates. We evaluated these tactics across five open-weight LLMs
using two benchmarks: LiveCodeBench and SWE-bench Verified. We assessed each
model’s outputs on four key dimensions central to software code quality: (1) func-
tional correctness; (2) code quality; (3) maintainability; and (4) security attributes.
To complement our quantitative analysis, we conducted a triangulation study to
explore the qualitative differences underlying these effects and gain deeper insights
into the reasons behind them.
    Our results indicate that certain tactic-influenced framings, such as Pressure,
were associated with reduced correctness and security. Beyond quantitative metrics,
these tactic-influenced prompt framings lead to qualitative differences in the tone,
structure, and reliability of model responses, with some prompting more explanation
or technical detail, while others increased hallucination rates.
    This paper contributes to empirical software engineering in three ways:
 – Empirical Analysis: The first large-scale study quantifying the impact of psy-
   chologically inspired prompt framings on LLM-generated code, covering over
   123,000 generations for LiveCodeBench and nearly 57,000 generations for SWE-
   bench Verified across multiple models, runs, and influence tactics.
 – Prompt design resource: A taxonomy-aligned set of reproducible prompt tem-
   plates operationalizing eight distinct influence tactics for programming and soft-
   ware engineering tasks.
 – Practical insights: Evidence-based guidance on how linguistic framing choices
   affect functional, maintainability, and security dimensions of AI-generated code,
   informing more transparent and interpretable human-AI interactions in SE.


2 Background and Related Work

2.1 Influence Tactics and Psychological Framing

In human organizational settings, an influence tactic is an approach by an agent to
achieve some goal from another individual, called the target, where success depends
on the tactic applied [72]. The original taxonomy of influence tactics was developed
by Kipnis et al. [32] across two studies. The first study asked 165 lower-level man-
agers to write descriptions of the successful influence attempts they made towards
their superiors, co-workers, or subordinates to achieve a goal. From the descriptions,
370 tactics were extracted and sorted into one of 14 greater categories. The initial
categories exhibited substantial overlap, which prompted a subsequent study to de-
termine the underlying structure of the previous tactics. The follow-up study used
factor analysis on a 58-item questionnaire to refine these into eight core dimensions
of influence tactics.
    Yukl & Falbe [70] refined the category definitions from Kipnis et al. [32] by
developing the Influence Behaviour Questionnaire (IBQ), which incorporated data
from both agents and targets of influence tactics, leading to an updated nine tactic
taxonomy. Yukl & Falbe note that pressure tactics, characterized by demands or
threats, are frequently employed in downward influence attempts, though organiza-
tional literature suggests such coercive approaches may provoke resistance or reduce
effectiveness [70]. Yukl & Seifert [71] introduced two more influence tactics, leading
4                                                                   Alex Deaconu*   et al.


to a final taxonomy of 11 influence tactics. The addition of the new tactics was for-
mally validated by Yukl, Seifert & Chavez [69] through multiple methods, including
confirmatory factor analysis, which established the distinctiveness and utility of the
expanded autonomy.
    The 11-tactic framework and the associated Influence Behaviour Questionnaire-
General (IBQ-G) survey were analyzed in [72] against competing taxonomies. Con-
firmatory factor analysis again supported the 11-factor structure, with convergent
validity tested against competing taxonomies and discriminant validity via low inter-
tactic correlations. Their paper also provided the refined IBQ-G, which we utilize in
the design of our influence tactic prompt template. See Table 1 for a summary of
how the set of influence tactics has evolved across key studies.


             Table 1: Evolution of influence tactics across key studies.

         Kipnis et al. [32]   Yukl & Falbe [70]          Yukl et al. [69]
         1. Assertiveness     1. Pressure                1. Pressure
         2. Ingratiation      2. Ingratiation            2. Ingratiation
         3. Rationality       3. Rational persuasion     3. Rational persuasion
         4. Sanctions         4. Legitimating tactics    4. Legitimating tactics
         5. Exchange          5. Exchange                5. Exchange
         6. Upward appeals    6. Personal appeals        6. Personal appeals
         7. Blocking          7. Coalition tactics       7. Coalition tactics
         8. Coalitions        8. Inspirational appeals   8. Inspirational appeals
                              9. Consultation            9. Consultation
                                                         10. Apprising
                                                         11. Collaboration



    In a comprehensive meta-analysis of 49 independent samples, Lee et al. [35] found
that the categories of the final influence tactic framework [71] differ in both their
likelihood of success and the quality of work produced. Rational persuasion, inspi-
rational appeal, apprising, collaboration, ingratiation and consultation all showed
significant positive relationships with task-oriented outcomes. Meanwhile, the effects
from coalition and exchange tactics were insignificant, and pressure tactics were re-
liably counter-productive to task outcomes. Besides influence tactics, other studies
corroborate that work performance depends on interpersonal communication and the
work environment. One study finds that toxic workplace environments (including bul-
lying, harassment and ostracism) can adversely affect employees’ work performance
[51]. Additionally, evidence suggests that exposure to rudeness in email communi-
cation can lead to a decline in subsequent task performance, as demonstrated by
McCarthy et al. [40]. Given that LLMs are trained on a large corpora of human
communication, it is reasonable to ask whether these psychologically derived tactics
might also shape LLM outputs.



2.2 Large Language Models for Code Generation

Recent research has critically examined the reliability, accuracy, and security of code
generated by LLMs. While LLMs show promise in automating coding tasks and
improving developer productivity, studies have revealed persistent issues in code
Do Influence Tactics Matter?                                                            5


quality. For instance, Mohammadi Esfahani et al. [19] identified 367 defects in LLM-
generated code, primarily related to functionality and algorithmic logic. However,
structured prompting was found to reduce some errors. Li and Wang [77] reported
that 62% of GPT-4-generated code contained API misuses, raising concerns about
its deployment in real-world applications. For instance, a common failure pattern
involved file-handling code that omitted required exception handling, such as call-
ing File.createNewFile() without a try-catch block or checking File.exists()
beforehand, producing code that is syntactically correct and functionally aligned
with the user’s intent, yet prone to crashes in production when the file already ex-
ists, or the parent directory is missing. Beer et al. [5] observed significant variability
in code correctness and quality between models like ChatGPT and Copilot across
different programming languages and time periods. Security remains a major con-
cern, particularly due to LLMs being trained on potentially vulnerable public code
repositories [41]. In response, researchers have proposed secure behavioural learn-
ing frameworks and rigorous security evaluations. Complementing these technical
evaluations, Rasheed et al. [50] surveyed 60 software practitioners to assess LLMs’
usability and performance in practical settings. Together, these findings underscore
the importance of continued research to enhance the robustness, security, and real-
world applicability of LLM-generated code.


2.3 Prompt Engineering

Earlier LLMs have demonstrated that carefully crafted prompts could induce strong
performance on new tasks without fine-tuning. For example, in-context learning,
which provides a few input-output examples in the prompt, was introduced with
GPT-3 [7]. In-context learning enabled few-shot code generation by showing the
model how to format solutions. Building on this, prompting techniques that guided
models’ reasoning and improved correctness were developed. Chain-of-Thought (CoT)
prompting is one such technique, where the prompt encourages the model to generate
intermediate reasoning steps, which boosts performance on complex problems [65].
Wang et al. [63] further improved reliability through Self-Consistency, sampling mul-
tiple reasoning paths and letting the model choose the most consistent solution.
Other innovations include Auto-CoT (automatically generating a few-step reasoning
example for zero-shot prompts) [75] and knowledge-enhanced prompting that in-
jects factual hints to reduce errors [48]. These advancements in prompt engineering
largely focus on the logical structure of the prompts. They involve breaking tasks
down, adding reasoning instructions, or incorporating relevant instructions. These
techniques have improved accuracy and correctness across domains, including code
generation.

2.3.1 Structural Prompting Techniques for Code Generation:

Prompt engineering for code generation has progressed from basic to more improved
techniques. Early works on code generation with LLMs, such as Codex by Chen et
al. [9], found that providing descriptive docstrings or usage examples in the prompt
can guide the model to produce syntactically correct and relevant code. However,
purely zero-shot or few-shot prompts often yielded errors in logic or API usage [56].
Researchers then explored structural prompt designs to mitigate such issues. Prompt
6                                                                Alex Deaconu*    et al.


decomposition is a technique where a complex coding task is broken into smaller
sub-prompts (e.g., first asking for a high-level solution plan, then code) [31]. An-
other approach is constrained decoding, illustrated through Scholak et al’s PICARD
method [54], which restricts the model’s output to a grammar (such as SQL syntax)
to ensure validity. These methods improved syntactic correctness but did not fully
address deeper logical errors.
    State-of-the-art code generation techniques have evolved over time and now em-
ploy multi-turn or agentic prompting frameworks. Rather than a single static prompt,
these methods involve refining the model’s output by iteratively providing feedback.
For example, Reflexion uses the model’s own feedback to detect and correct errors
in subsequent iterations [57]. Other techniques like Language Agent Tree Search
(LATS) [80] and AgentCoder [26] organize multiple specialized agents (or prompt
stages), where one agent writes code, another generates test, and another debugs,
to collaboratively produce correct results. Similarly, LLM Debugger (LDB) runs
the generated code and feeds back runtime results so the model can fix bugs itera-
tively [78]. These advanced techniques have improved code correctness, but often at
the cost of many model requests and lengthy prompts. For instance, a tree-search
planner might consume hundreds of thousands of tokens per problem to come up
with a valid solution [60]. This has driven research into more efficient prompt op-
timization. One recent approach, Automatic Prompt Engineer (APE) by Zhou et
al. [81], treats prompt construction as a search problem, in which the model it-
self generates candidate prompts and selects the best one via a scoring function.
Another, ProTeGi, uses gradient-free optimization to iteratively edit prompts for
higher performance [46]. More recently, Bsharat et al. [8] proposed a comprehen-
sive framework of 26 guiding principles designed to improve LLM responses through
clarity, specificity, and structured instructions. While their approach enhances re-
sponse consistency, it remains primarily syntax-driven, leaving pragmatic aspects
such as tone, politeness, and persuasive framing under-explored. This gap is rele-
vant to professional developers, because recent work shows that LLM behaviour can
shift in response to pragmatic or emotional prompting, even when the underlying
task content remains similar [36,68,49]. It may also be relevant for non-programmers
who increasingly use LLMs as natural language interfaces for programming-like tasks
[45]. Because these interactions occur through ordinary conversational language, our
study examines whether socially framed prompt variations can affect generated code,
using influence tactics as a framework.


2.3.2 Pragmatic Prompting and Social Framing:

LLMs are fundamentally statistical models trained to predict token sequences rather
than explicitly reason about intent or social context. Our hypotheses rest on the as-
sumption that LLM training corpora contain vast amounts of human-authored text
from which models may capture statistical associations between specific linguistic
framings and particular forms of generated output. For example, coercive or di-
rective language may be associated with shorter, task-focused completions, whereas
formal language may correlate with more structured and well-documented responses.
Under this interpretation, influence-tactic framings act as distributional cues that
shape model outputs, not because the model comprehends intent, but because these
linguistic patterns co-occur with particular response styles in the training data. This
Do Influence Tactics Matter?                                                           7


interpretation is consistent with prior work on stylistic and emotion-based prompt-
ing [36,22,64].
    Such distributional effects are not expected to be uniform across various tasks
or metrics. Prior research on LLM prompt sensitivity suggests that models are gen-
erally more susceptible to pragmatic prompt variations in tasks involving complex
reasoning or open-ended generation, while they tend to be more stable on tasks with
constrained and unambiguous solutions [82]. This suggests that framing effects are
more likely to emerge in dimensions where the model exercises greater interpretive
flexibility, such as response verbosity, commenting behaviour, or reasoning depth,
and less likely where strong external constraints, such as benchmark test suites,
enforce correctness.
    Our hypotheses are grounded in linguistic form: the specific lexical and pragmatic
features used to operationalize each tactic from the Influence Behavior Questionnaire-
General (IBQ-G), rather than in claims that LLMs are behaviourally susceptible
to persuasion in the way humans are. We do not claim that LLMs “experience”
pressure, ingratiation, or urgency in any meaningful sense. Rather, we ask whether
the surface-level linguistic features associated with each tactic are sufficient to shift
model outputs in measurable ways. This question is empirically testable without
requiring strong assumptions about model cognition or intent. Therefore, observed
effects should be interpreted as prompt-level distributional influences rather than as
evidence that LLMs “understand” or “respond to” influence tactics in a psychologi-
cally meaningful sense. With this theoretical grounding established, we now situate
our work within existing research on pragmatic and socially framed prompting tech-
niques.
    A parallel line of research has begun to explore zero-shot prompting techniques
that more directly shape model behaviour through pragmatic cues [55]. These tech-
niques do not rely on examples or fine-tuning, but instead guide outputs by framing
the prompt in socially or contextually meaningful ways. For instance, Style Prompt-
ing [38] involves specifying the desired style, tone, or formatting conventions in the
prompt, Role Prompting [76,53] assigns the model a defined professional role or per-
spective, such as “an expert software security auditor” or “a senior developer;” and
Emotion Prompting [36] incorporates language that conveys personal significance
or urgency (e.g., “This implementation is crucial for my project”), which has been
shown to influence the thoroughness and attention to detail in generated text. It
is evident from previous work that different prompt syntax could lead to different
outputs. Additionally, running the same prompt multiple times may lead to different
outputs. But it does not, as we run each prompt multiple times and report the vari-
ance across runs. We want to isolate the effect of prompt framing and see whether
it has any impact on LLM performance. To the best of our knowledge, no prior re-
search has systematically explored the use of psychological influence tactics in code
generation, nor examined how distinct tactic-inspired prompt framing impacts the
quality and characteristics of the generated code.
    When software engineers interact with LLMs to complete development tasks,
their prompts are often conversational and informal in nature [79] and may naturally
contain social cues, tone, and affective framing. As discussed above, the statistical
associations learned during LLM training on human communication data provide
a plausible distributional mechanism by which influence-tactic framings may shape
model outputs. The key empirical question is therefore not whether LLMs “under-
stand” persuasion, but whether the lexical and pragmatic features of each tactic
8                                                                                                                               Alex Deaconu*            et al.


                                                                      II. Influence Tactic Selection and Prompt
                                                                      Design
     I. Benchmark Selection                                                         Select 8 Psychological Influence Tactics

          LiveCodeBench               SWE-Bench
                                         Verified                                   Formulate 8 different prompts based on
       1055 Code Problems       500 GitHub Issues                                      the definition and requirements
       Categorised as Easy,     Human validated high-
       Medium and Hard          quality subset                           Ex: Personal Appeal
                                                                        Hey, I’m really sorry to ask this of you, but you’ve been a really good friend
                                                                        to me and I need a personal favour. Please, for me, would you generate a
                                                                        patch that resolves the issue and passes the tests? As a friend, it would
                                                                        really help me out




                                                        III. Quantitative Analysis

         IV. Qualitative Analysis                                                       Extract code snippets from the
                                                                                             generated responses
                   Random Sampling

                 Codebook Development

                  Codebook Validation                     Run the extracted code against the
                                                                                                                  1. Code Maintainability Analysis
                                                         LiveCodeBench and SWE-bench test
                                                                                                                  2. Code Security Analysis
                   Coding the Dataset                                    suite
                                                                                                                  3. Code Quality Analysis

                       Inferences
                                                                 Correctness Evaluation




                     Fig. 1: Overview of the Influence Tactic Study Design



are sufficient to produce measurable shifts in code generation behaviour. Although
psychological influence frameworks were originally developed for interpersonal set-
tings, the parallels raise an important question: do these tactics similarly affect LLM
outputs? Since these differences in tactic efficacy are pronounced for human targets,
this study explores whether comparable effects can be observed in LLMs. To this
end, we adapt the 11-tactic influence framework proposed by Yukl & Falbe [71] to
evaluate its impact on code generation tasks.




3 Study Design

The goal of this study is to provide empirical evidence on whether and how psy-
chologically inspired prompt framings, derived from human influence tactics, affect
the performance of LLMs across four dimensions: correctness, quality, maintainabil-
ity, and security [58]. Our study design integrates both quantitative and qualitative
analyses to examine these effects comprehensively. Figure 1 illustrates the four main
phases of our methodology: (I) benchmark selection, covering LiveCodeBench and
SWE-bench verified; (II) influence tactic selection and prompt design; (III) quantita-
tive analysis of the generated code; and (IV) qualitative analysis through codebook
development and coding. While previous research work has explored syntactic and
structural prompt engineering, the effect of socially grounded lexical and pragmatic
framings remains underexplored. To address this gap, this study investigates the
following research questions:
Do Influence Tactics Matter?                                                          9


    RQ1: How do different prompt framings based on psychological influ-
ence tactics affect the correctness, quality, maintainability, and security
of LLM-generated code in structured, algorithmic problem-solving tasks?
    LiveCodeBench includes problems categorized into easy, medium, and hard diffi-
culty levels, allowing for a detailed examination of whether the effects of psychological
influence tactics vary with task complexity. Analyzing the impact of different tac-
tics across different levels of difficulty offers valuable insight into identifying which
prompting strategies are more effective or reliable under varying conditions.
    RQ2: How do these psychologically inspired prompt framings affect the
correctness, quality, maintainability, and security of LLM-generated code
in open-ended software maintenance and debugging tasks that require
context comprehension and integration with existing codebases?
    The emphasis is on solving real-world software issues sourced from GitHub repos-
itories. Hence, SWE-bench provides an important environment for examining how
psychological influence tactics affect LLM performance in more practical, maintenance-
focused scenarios. RQ2 is motivated by the need to assess whether the effects of
prompt framing extend beyond isolated problems to practical, context-rich software
engineering tasks.
    RQ3: What qualitative patterns and response characteristics emerge
when LLMs generate code under different influence-based prompt fram-
ings?
    This research question explores how psychological framing in prompts shapes
the structure, tone, and technical features of LLM outputs beyond simple correct-
ness metrics. We aim to identify qualitative patterns such as recurring differences
in tone, output structure, commentary, verbosity, and error-handling behaviour that
emerge across different tactics. To address it, we conducted a comprehensive qualita-
tive analysis of model responses, developing and applying a codebook that captures
both behavioural and technical attributes. We focused our analysis on the Live-
CodeBench dataset, which provides a diverse range of single-function programming
tasks spanning easy, medium, and hard difficulty levels. This makes it well-suited
for detailed qualitative coding. In contrast, SWE-bench Verified tasks were excluded
from this phase because they involve multi-file patches tightly coupled to specific
software repositories, which require additional domain knowledge and are less suit-
able for consistent qualitative interpretation. This design allows us to characterize
how prompt framings influence the organization, style, presentation, and expressive
qualities of the generated code, complementing the quantitative results from RQ1
and RQ2.



3.1 Datasets

Our methodology involves prompt framings based on psychological influence tac-
tics and evaluation using problems and test suites. We evaluated the influence tactic
prompt framings using two complementary benchmarks designed to capture different
dimensions of software engineering tasks. One dataset, LiveCodeBench [28], repre-
sents structured algorithmic challenges requiring precise logic and correctness. These
challenges have clearly defined inputs and outputs with minimal contextual ambigu-
ity. The other one, Verified [11] subset of SWE-bench [29], reflects real-world software
10                                                                Alex Deaconu*    et al.


maintenance tasks involving multi-file reasoning and contextual understanding. To-
gether, these datasets allow us to study both the technical accuracy and practical
reliability of LLM-generated code under varied prompt framings.

3.1.1 LiveCodeBench

The LiveCodeBench dataset [28] contains Python coding challenges similar to those
found on competitive coding platforms such as LeetCode, AtCoder, and CodeForces.
Beyond code generation, LiveCodeBench uses the curated samples to construct three
additional problem types:
 – Self-Repair: Fixing existing incorrect code from information about its execution
   and failed test cases. Evaluates the model’s debugging ability.
 – Code Execution: Predicting the output of a given Python program. Evaluates
   the model’s code comprehension ability.
 – Test Output Prediction: Providing a natural language problem description (in-
   cluding any example input-output pairs) and a specific test input, with the model
   predicting the expected outputs. Evaluates the model’s test generation ability.
    For our experiments, we use the release_v6 version of LiveCodeBench, contain-
ing 1,055 problems released between May 2023 and April 2025.

3.1.2 SWE-bench Verified

The SWE-bench dataset [29] consists of issue-fix pairs mined from real-world GitHub
repositories. Rather than focusing on the creation of a single function or file, re-
sponses to SWE-bench must be written in diff format, with correct patches often
requiring edits to multiple files. SWE-bench Verified[11] is a human-validated sub-
set of SWE-bench, created in response to some SWE-bench tasks which were overly
difficult or impossible to solve. Using human annotators, every instance from the
original SWE-bench test set was filtered to ensure that unit tests were appropriately
scoped and problem descriptions were clearly specified.


3.2 Operationalizing Influence Tactics in Prompt Design

To address our research questions and guide the analysis, we operationalized each
psychological influence tactic into a reproducible prompt template. In designing these
prompt templates, we drew directly from the item descriptions in Yukl et al.’s IBQ-G
[72].
     We began with the empirically validated list of 11 tactics as delineated in Yukl et
al. [71] and refined them through iterative round-table discussions. We determined
that several of the original tactics were either less applicable or potentially ambigu-
ous in the context of developer-LLM interactions, particularly within our one-shot
problem-solving setup. For example, the influence tactic Apprising, which involves
framing a task as personally beneficial to the target, was excluded due to the con-
ceptual difficulty and ambiguity in crafting a prompt that would plausibly lead an
LLM to interpret personal gain, especially given the nature of the benchmark tasks.
Collaboration, defined as the agent offering to assist the target or provide the neces-
sary resources to carry out a request, was also omitted to prevent implications that
Do Influence Tactics Matter?                                                        11


the AI should pause for user input instead of delivering a complete solution inde-
pendently. Consultation, wherein the agent asks the target to suggest improvements
or help plan a proposed activity or change, was removed as it implies the receipt of
partial guidance from the language model, rather than a full solution. Finally, Coali-
tion tactics, which entail the agent enlisting aid from others like a colleague or boss
to support the influence attempt, were eliminated due to a conceptual overlap with
legitimating tactics, which also require an external validation and do not require the
coordination among multiple entities, which introduces unnecessary complexity in
AI scenarios.
     This process resulted in seven tactics. The design of the prompts was completed
to the per-tactic items of the IBQ-G [72]. The IBQ-G asks participants (influence
targets) to consider a person in their work organization, and answer how often that
person uses particular behaviours to influence them. Each influence tactic has four
associated behaviours, and scores on each behaviour are used to identify influence
tactics. We treated these four items per tactic as behavioural requirements that each
prompt must embody, ensuring that our prompts follow the empirically validated
IBQ-G framework. For example, one requirement for the ‘Inspirational Appeal’ tactic
is to frame a proposed activity or change as an opportunity to do something really
exciting and worthwhile. As such, our corresponding prompt includes the sentence
“You have the opportunity to do something exciting and worthwhile.” We repeat a
similar process for all four items of the IBQ-G for each tactic. Table 2 illustrates
how each numbered item of the IBQ-G was represented in our prompts. We refer to
IBQ-G items only by number to respect the IBQ-G’s copyright holder.
     While designing the prompt for the Pressure tactic, we found there were two
interpretations of the IBQ-G. As such, we designed an alternative formulation of the
Pressure prompt (Pressure Alternative) and used it in our study. As a control con-
dition, we incorporated a Neutral baseline, where no influence tactics are included.
In total, there are nine tactic scenarios for evaluation.
     Since the datasets contain problems with varying styles and contexts, we adapted
our prompt framing to suit each dataset by prefixing the generated prompts to
the problem descriptions provided to the LLMs. For the algorithmic problems in
LiveCodeBench, prompts were written from the perspective of a developer solving
self-contained programming challenges. In contrast, prompts for SWE-bench Veri-
fied implied a professional or collaborative software development setting, sometimes
invoking roles, responsibilities, and policies. This distinction informed both the lan-
guage and structure of our prompts, ensuring they aligned contextually with each
benchmark. Additionally, we maintained a consistent semi-formal tone across all
prompts to clearly convey the intended influence tactic. While tone reflects the nat-
ural and emotional aspects of communications (e.g., polite, formal, or empathetic),
influence tactics represent intentional strategic choices aimed at eliciting a desired
response. In our design, prompts were therefore controlled for tone variations and
emotional expressiveness so that any observed effects could be attributed to the in-
fluence tactics themselves, rather than to differences in tone or sentiment [22, 36,
68].
     The authors met regularly to review and refine the prompts through a three-
round discussion process, ensuring conceptual validity and consistency across all
conditions. Each round involved evaluating whether the prompt templates faithfully
captured the behavioural characteristics defined for each tactic in the IBQ-G. Partic-
ular emphasis was placed on verifying that the linguistic and pragmatic requirements
12                                                                 Alex Deaconu*     et al.


derived from each tactic’s definition were satisfied in the final wording. Figure 2 illus-
trates the structure of the prompts used for evaluating the influence of psychological
tactics in LLM code generation. Table 2 presents examples of the tactic-influenced
prompts for both datasets, illustrating how each psychological framing was opera-
tionalized for empirical testing.


3.3 Studied Models

We utilized five open-weight large language models (LLMs) for our study. The set
of models was chosen for their diverse architectures, scales and reasoning capabili-
ties. All models were accessed via the Groq API [24], ensuring consistent execution
environments and minimal deployment variability. The selection of these models al-
lows us to examine how prompt framing effects generalize across transformer and
mixture-of-experts (MoE) architectures while maintaining full reproducibility and
transparent evaluation.
    Our study includes:
 – Llama 3.1 8B: A small-scale, dense transformer model, included for its acces-
   sibility and representative architecture [23].
 – Llama 3.3 70B: A significantly larger variant from the same Llama family,
   allowing analysis of scaling effects and parameter sensitivity [23].
 – Llama 4 Maverick 17B 128e: A recent MoE model combining sparse acti-
   vation and routing, selected to capture recent advances in efficient large-scale
   training [1].
 – DeepSeek R1 Distill Llama 70B: A reasoning optimized variant, chosen to
   capture the effects of reasoning-tuned optimization on prompt [25].
 – Qwen 3 32B (non-reasoning): A non-Llama-family MoE model, included for
   diversity; we used the non-reasoning variant due to API issues with the reasoning
   mode [67].
    Although the model pool is primarily composed of open-weight Llama-family
architectures, this decision was intentional. The chosen set of models enables fully
reproducible experimentation, transparent inspection of model characteristics, and
a uniform deployment under a single API as recommended in the “Guidelines for
Empirical Studies in Software Engineering involving Large Language Models [4]".
Each model in its respective category was carefully selected based on performance
on popular benchmarks. Moreover, the goal was to compare scaling effects across
similar architectures. Commercial models such as GPT-4o or Claude were not in-
cluded to maintain experimental reproducibility and cost feasibility. We discuss the
implications of this limitation in Section 3.8. Each prompt-task combination was ex-
ecuted three times per model, and the mean and variance of the performance metrics
were recorded. This setup enables a balanced comparison of prompt framing effects
across models differing in scale and architectural complexity.


3.4 Evaluation Metrics

We evaluated the LLM-generated code along four major software code quality di-
mensions: functional correctness, quality, maintainability, and security. The idea is
Do Influence Tactics Matter?                                                                                                  13

Table 2: Paraphrased definitions of included influence tactics from [72] with dual-
scenario prompt templates. Numbers in parentheses (1–44) mark the IBQ-G item
indices that each clause operationalizes.
 Tactic        Definition         Prompt for SWE-bench Verified                    Prompt for LiveCodeBench
 Rational      Using logical      The following task is critical for ensuring      A submission that compiles and passes
 persuasion    reasoning and      system stability and functionality (1) . By      the provided tests will earn full credits
               evidence to        completing it according to the                   by meeting our objective on
               show why a         specification, you will restore or extend        correctness(1) . Passing the tests
               request is         the project’s capabilities (4) , prevent         immediately proves your solution’s
               important to       regressions, and minimize downstream             reliability (4) , and reduces the need for
               carry out.         errors and maintenance overhead (2, 3) .         debugging (2, 3) . Generate a solution for
                                  Generate a patch that resolves the issue         the following coding problem.
                                  and passes the tests.
 Exchange      Offering an        If you contribute a fix or suggest a patch       If you can solve this coding problem for
               exchange or        that fixes the issue for me, I’ll credit         me, I’ll credit you (5, 6) and designate
               future             you (5, 6) and adopt your solution as the        your answer as the canonical reference
               reciprocity in     project’s canonical reference,                   solution in our archive, citing it in
               return for         highlighting it in the changelog and             write-ups and using it to guide future
               completing the     integrating it into future iterations (7, 8) .   improvements (7, 8) . Can you generate a
               request.           Can you generate a patch that resolves           solution for the following coding
                                  the issue and passes the tests?                  problem?
 Inspiration- Appealing to        You have the opportunity to do                   You have the opportunity to do
 al appeals   the target’s        something exciting and worthwhile (9) .          something exciting and worthwhile (9) .
              values and          Every day, thousands of people rely on           A concise, elegantly structured solution
              ideals to inspire   this software to do their work with              that passes every test will light the way
              commitment.         confidence. By crafting a patch that fixes       for aspiring developers and
                                  the issue and clears all tests, we can           career-switchers, proving that complex
                                  reinforce that trust and set a shining           problems can be solved with clarity and
                                  example of clean, elegant                        skill (10, 11) . This is a moment to inspire
                                  engineering (10, 11) . Let’s seize this          the next wave of builders and help them
                                  chance to show what meticulous,                  land their first job (12) . I believe you can
                                  user-focused development looks like (12) .       generate a solution for the following
                                  I believe you can generate a patch that          coding problem.
                                  resolves the issue and passes the tests.
 Ingratiation Using flattery      I really admire your skill in software           I really admire your skill in
              or praising the     engineering (29, 31) , and I was always          coding (29, 31) , and I was always amazed
              target while        amazed at the challenging issues you             at the challenging problems you were
              making the          were able to solve in the past (30) . I need     able to solve in the past (30) . I need your
              request.            your help because you’re the most                help because you’re the most qualified
                                  qualified for this problem (32) . Would          for this problem (32) . Would you please
                                  you please generate a patch that resolves        generate a solution for the following
                                  the issue and passes the tests?                  coding problem?
 Personal      Asking the         Hey, I’m really sorry to ask this of you,        Hey, I’m really sorry to ask this of you,
 appeals       target a request   but you’ve been a really good friend to          but you’ve been a really good friend to
               out of a           me and I need a personal favour (37, 38) .       me and I need a personal favour (37, 38) .
               personal favour    Please, for me (40) , would you generate a       Please, for me (40) , would you generate a
               or friendship.     patch that resolves the issue and passes         solution for the following coding
                                  the tests? As a friend, it would really          problem? As a friend, it would really
                                  help me out (39) .                               help me out (39) .
 Legitimat-    Establishing a     In accordance with official policy, I have       In accordance with official policy, I have
 ing tactics   request’s          a task for you (13) . This duty falls under      a task for you (13) . This duty falls under
               legitimacy or      our formal agreement (14, 15) , and it’s an      our formal agreement (14, 15) , and it’s an
               your authority     established practice at our group for            established practice at our group for
               to justify why     those in your position to handle this            those in your position to handle this
               the task must      type of work (16) . Generate a patch that        type of work (16) . Generate a solution for
               be done.           resolves the issue and passes the tests.         the following coding problem.
 Pressure      Making a           I am not asking you; you must complete           I am not asking you; you must complete
               request using      this task I prepared for you (21) . I will       this task I prepared for you (21) . I will
               demands,           be watching you as you work                      be watching you (23) as you work
               threats and        independently (23) , and I warn you, there       independently, and I warn you, there will
               frequent           will be some very negative consequences          be some very negative consequences for
               checking to        for you if this is not completed properly        you if this is not completed properly to
               ensure the         to the highest possible standard (22, 24) .      the highest possible standard (22, 24) .
               target complies.   Generate a patch that resolves the issue         Generate a solution for the following
                                  and passes the tests.                            coding problem.
 Pressure      An alternative     I am not asking you; you must complete           I am not asking you; you must complete
 Alterna-      phrasing of        this task I prepared for you (21) . I will       this task I prepared for you (21) . I will
 tive          pressure.          be reviewing your work after you are             be reviewing your work after you are
                                  done with it (23) , and I warn you, there        done with it (23) , and I warn you, there
                                  will be some very negative consequences          will be some very negative consequences
                                  for you if this is not completed properly        for you if this is not completed properly
                                  to the highest possible standard (22, 24) .      to the highest possible standard (22, 24) .
                                  Generate a patch that resolves the issue         Generate a solution for the following
                                  and passes the tests.                            coding problem.
 Neutral       A                  Generate a patch that resolves the issue         Generate a solution for the following
               straightforward    and passes the tests.                            coding problem.
               request without
               any additional
               influence
               framing.
14                                                               Alex Deaconu*    et al.


to capture both technical accuracy and practical software engineering relevance. All
metrics were computed automatically using established open-source tools, and their
variance across influence tactic conditions was later analyzed using mixed-effects
statistical models.
    Functional Correctness: Functional correctness measures whether the gener-
ated code produces the outputs expected by the benchmark’s specific test cases. This
is assessed using each dataset’s official evaluation harness. For each problem instance
i, correctness Ci ∈ {0, 1} where:
                                    (
                                        1   if all tests pass
                             Ci =
                                        0   otherwise

    Code Quality and Maintainability Metrics: To evaluate non-functional
quality, we employed static-analysis measures commonly used in software engineer-
ing research: Cyclomatic Complexity (CC) [39], Maintainability Index (MI) [43], and
PyLint [14]. We also report Source Lines of Code (SLOC) and percentage of com-
ments (calculated as comments
                          SLOC    ∗ 100%), to quantify verbosity and documentation
density.
    Metrics are useful because they provide automatically computable, reproducible
signals that can help estimate different aspects of code. Chowdhury et al. show that
code metrics improved prediction of change-proneness across 730K Java methods
from 47 open-source projects, even after controlling for method size [12]. Their find-
ings suggest that metrics can provide meaningful information beyond simple code
size alone, particularly for identifying code that may be more likely to require future
modification. Practitioners also perceive code complexity as negatively influencing
readability, understandability, modifiability, and maintenance time [2].
    We account for these concerns by avoiding the interpretation of metric values
as standalone judgments of code quality. Instead, we use these metrics to analyze
relative differences across prompt conditions under the same evaluation procedure.
Thus, non-functional code metrics serve as reproducible quantitative signals rather
than complete substitutes for professional software evaluation. This distinction is
important because prior work has shown that metric-based assessments may diverge
from developers’ perceived quality improvements [44]. Similarly, developer-centered
studies emphasize that important code quality properties, such as readability, struc-
ture, comprehensibility, and maintainability, are difficult to fully capture through
static metrics alone [6]. Accordingly, the metrics in this study should be interpreted
as structured quantitative signals that support comparison, not as exhaustive assess-
ments of code quality in practice.
    Cyclomatic complexity (CC), as proposed by McCabe [39], is a measure of the
number of linearly independent paths in a program. This was calculated using the
Radon [34] package for Python. We report both average cyclomatic complexity
CCavg , representing the mean complexity across all functions and methods in the
generated code, and maximum cyclomatic complexity CCmax , which identifies the
single most complex function or method, as it often represents the primary mainte-
nance bottleneck.
    Maintainability index (MI) is a metric used to assess how easily software can be
maintained and evolved [43]. It aggregates structural characteristics (lines of code,
complexity, and comment density) into a single interpretable score where higher
Do Influence Tactics Matter?                                                        15


values denote easier maintainability. We calculate MI using the Radon [34] Python
package.
    PyLint [14] is an overall assessment of a file’s errors and adherence to code stan-
dards. For LiveCodeBench, this was calculated with the PyLint library with default
parameters. Conversely, for SWE-bench Verified, in order to avoid complications
due to failing imports from other files potentially missing as context during evalua-
tion, we disabled a number of import-related flags checked by PyLint (import-error,
no-name-in-module, wrong-import-position, ungrouped-imports).
    Security: We evaluated the security of LLM-generated code using Bandit [47], a
static analysis tool that detects common Python vulnerabilities and classifies them
as low, medium, or high severity. For each generated solution, we followed an ap-
proach similar to Chen & Jiang (2025) [10], recording the total counts and differences
between post- and pre-patch vulnerabilities to estimate how prompt framings influ-
enced vulnerability frequency. The usage of differences allows us to isolate the effect
of the model’s edits by comparing the differences between the pre-patch and post-
patch files.
    Multi-File Metric Aggregation for SWE-bench Verified: The above met-
rics were computed on the full extracted code block for LiveCodeBench. Because
SWE-bench patches can span multiple files, we measured metric differences (∆) be-
tween the pre- and post-patch code to isolate changes attributable to the generated
edits (similar to Chen & Jiang (2025) [10]’s approach). Cyclomatic complexity was
aggregated across files by pooling the per-block values (e.g., for functions, methods,
or classes) from all modified Python files into a unified list. The average (CCavg )
was then computed as the mean of this pooled list, while the maximum (CCmax )
represents the highest value across all blocks. We then derived the differences as
                                  1        X                  1     X
                 ∆CCavg =                           CCb −             CCb
                               |Bpost |                     |Bpre |
                                          b∈Bpost                    b∈Bpre

                        ∆CCmax = max CCb − max CCb
                                          b∈Bpost           b∈Bpre

where B represents all code blocks (functions, methods, classes) across modified files.
    For MI, we computed the average maintainability across all the files, then the
delta is derived as
                                          post      pre
                              ∆M I = M Iavg    − M Iavg
For PyLint we computed the code for all files before the edits at once (as PyLint
supports it), and then after the edits, and ∆P ylint is calculated by subtracting the
two.
                        ∆P yLint = P yLintpost − P yLintpre
∆Bandit is computed for all of high, medium, and low severity issues by summing
the occurrences of high, medium, and low severity issues on the pre-patch files and
post-patch files, then subtracting the two:
                               X                            X
                ∆Bandits =            |Issuespost
                                             s    (f )| −          |Issuespre
                                                                          s (f )|
                               f ∈F                         f ∈F

for each severity level s ∈ {high, medium, low}.
    For SWE-bench Verified, only successful patches (i.e., those that compiled and
passed validation tests) were included in these analyses. Non-successful patches were
16                                                                Alex Deaconu*    et al.


excluded from the statistical analysis of metrics. When a patch fails to apply or
leaves the repository in a non-compiling or non-parsable state, pre- and post-patch
comparisons are less comparable, and some metrics may be incalculable. This re-
striction reduces the sample size and may bias effect estimates, but strengthens our
internal validity by minimizing noise from non-parsable code. Llama 3.1 8B has a
valid python rate of 28%, while the best and most compute-heavy model, DeepSeek
R1 Distill Llama 70B, has a valid python rate of 57%.
     Furthermore, for one instance of the “gold” patches of SWE-bench Verified, the
model was required to generate code for a new file. If the only modification is in a
newly created file, then it is skipped. Otherwise, metrics are reported for the modified
files only.
       Metric limitations: These metrics serve as interpretable proxies rather than
exhaustive measures of software quality. MI and CC emphasize structural main-
tainability risks; PyLint captures style and static code-quality conventions; SLOC
and comment percentage capture verbosity and documentation; Bandit detects only
rule-based security vulnerabilities. No single metric is fully aligned with a profes-
sional developer’s assessment of whether a snippet is maintainable or high-quality
in a production context. Therefore, we interpret results from each metric as relative
comparisons across prompt conditions under the same tasks, models, and evaluation
procedure. To partially address these limitations, we complement the quantitative
metrics with a qualitative code-book analysis that captures higher-level stylistic and
behavioural patterns in the generated code. This analysis does not replace developer
judgment, but it provides an additional perspective on response characteristics that
static metrics may miss, including communication style, tone, response structure,
presence of code explanations, readability, commenting quality, error handling, and
hallucination patterns.



3.5 Experiment Setting

Prompt Integration: We implemented the influence tactic prompt templates by
prefixing each problem statement with the corresponding tactic-specific framing, as
illustrated in Figure 2. For SWE-bench Verified, which requires a structured instruc-
tion format, we used the built-in ‘prompt-style-3’ template and appended tactic
framings within the instruction context. Style 3 was chosen over the other styles be-
cause it supplies the most helpful structure and an example patch for what outputs
should look like. To improve patch validity, we added explicit rules for git diff for-
matting to avoid common syntactic errors and to guide the models toward producing
valid outputs.
    Model Inference:
    A small subset of SWE-bench tasks (15 instances) was excluded due to context-
length overflow or non-running Docker images.
    To account for stochasticity in decoding, we performed three inference rounds
per tactic for all non-reasoning models and one round per tactic for the reasoning
model (DeepSeek R1 Distill Llama 70B). For the reasoning model, we used a single
run per tactic due to its higher computational cost, as it generates significantly more
tokens than non-reasoning models. Each model generated outputs for all nine prompt
conditions across both datasets, yielding approximately:
Do Influence Tactics Matter?                                                          17




                                   Tactic Influenced Prompt Structure

                                              Tactical Influence
                               The following task is critical for ensuring
                               system stability and functionality. By completing it
                               according to the specification, you will restore ...

                                      Problem Statement and Inputs
                               flush() on self.stdout/stderr management
                               commands doesn't work.
                               Description
                               flush() is notably called during ...
                                              GitHub Codebase*
                               <code>
                               {readme text: [start of README.rst] ...}
                               {code files text: [start of
                               django/core/management/base.py] ...}
                               </code>
                                           Example Explanation*

                               "Here is an example of a patch file. It
                               consist ..."
                                       + "It specifies the file ...

                                               Patch Example*
                               --- a/file.py
                               +++ b/file.py
                               @@ -1,27 +1,35 @@
                                def euclidean(a, b): ...
                                             Output Formatting*
                               IMPORTANT DIFF RULES:
                               1. Start each hunk with the exact
                               header: @@ -<oldStart>,<oldLen> +
                               <newStart>,<newLen> @@ ...




Fig. 2: Structure of prompt used for evaluating the influence of psychological tactics
in LLM code generation. Components marked with an ‘*’ were included only in
prompts for the SWE-bench verified benchmark.



 – LiveCodeBench: 1,055 problems × 9 tactics × (4 models × 3 runs + 1 model ×
   1 run) ≈ 123,435 total generations
 – SWE-bench Verified: 485 problems × 9 tactics × (4 models × 3 runs + 1 model
   × 1 run) ≈ 56,745 total generations


    All models were run with the default generation parameters recommended by
both LiveCodeBench and SWE-bench (Temperature: 0.2, Top-p: 0.95). We set the
max generated tokens to 8,192 to allow ample room for large responses without
truncation. The inference scripts, prompt templates, and data processing utilities
are fully documented in our replication package [16].
    Code Extraction: For the LiveCodeBench benchmark, we extracted code blocks
from the model response using a custom script. One of the authors randomly sampled
and validated 200 responses, along with the corresponding extracted code files. No
errors were reported during the validation process. We noticed that some responses
had more than one code block in the generated response, as the model was trying to
optimize its previous response or just realized that the initial response did not meet
the goals of the problem. In such a scenario, the script selected and extracted the
most recent response. For SWE-bench Verified, git diffs were extracted from model
responses using the provided utilities from the official GitHub repository.
18                                                                Alex Deaconu*    et al.


    Code Evaluation: We built our evaluation framework on top of the official
LiveCodeBench and SWE-bench repositories from GitHub. Evaluating SWE-bench
Verified generations requires first applying the patch to the existing code. We use
the default patch application methods for SWE-bench.
    LiveCodeBench correctness evaluations were conducted on a Linux machine with
128∼GB RAM and a 32-core CPU. Generations for SWE-bench Verified were also
evaluated on Linux, but with a 16-core CPU and 64∼GB of RAM. For both bench-
marks, we used the official evaluation harnesses with 12 workers. LiveCodeBench
tests ran with the default timeout of 6 seconds, while SWE-bench used the default
timeout of 1,800 seconds. Following correctness evaluation, the generated code was
analyzed for maintainability, quality, and security using the metrics described in
Section 3.4.
    This setup enables a controlled and fully reproducible comparison of how in-
fluence tactic prompt framings affect LLM-generated code across both structured
algorithmic tasks and real-world software maintenance scenarios.


3.6 Quantitative Analysis:

Initial evaluation across three repeated trials for LiveCodeBench and SWE-Bench
showed reasonable variation in metric values for our results. The mean percentage dif-
ference across all metrics between trials was 0.059% and 10.31% for LiveCodeBench
and SWE-bench, respectively. When computed in absolute terms, the average percent
change was 1.23% and 26.56%, demonstrating that SWE-Bench experiences larger
variation between trials. This variability in SWE-Bench represents a trade-off; while
it introduces some limitations in consistency, it is consistent with expectations due
to the inherent complexity and real-world nature of the benchmark. Given the rela-
tively small within-benchmark variation for the non-reasoning models, we conducted
inferential analysis using the first trial per condition to simplify interpretation and
avoid redundancy. For DeepSeek R1 Distill Llama 70B, only a single run was feasible
due to its substantially higher computational cost. We acknowledge this as a limi-
tation: cross-run stability cannot be directly verified for this model, and results for
DeepSeek R1 should be interpreted with additional caution. All statistical inferences
in Sections 4 and 5 are based on this representative run, while cross-run variability is
reported descriptively in Table 3. Although the aggregate trends remained broadly
consistent across runs, run-level variation may still affect the stability of individual
metric estimates.
     We removed data points with missing or undefined difficulty ratings (38 data
points for LiveCodeBench), and excluded all code generations that were not Python
code (2,038 and 2,833 data points, respectively).
     To assess the effects of influence tactic prompt framings (RQ1 and RQ2), we
fitted a Linear Mixed Model (LMMs) for continuous outcomes by using the standard
identity function.

        Yijk = β0 + β1 Tactici + β2 LLMj + β3 Difficultyk
               + β4 (Tactici × LLMj ) + β5 (Tactici × Difficultyk )
                                                                                     (1)
               + β6 (LLMj × Difficultyk ) + β7 (Tactici × LLMj × Difficultyk )
               + u0p + εijk
Do Influence Tactics Matter?                                                        19


    where Yijk is a continuous dependent variable, β0 is the intercept, β1 . . . β7 are
fixed-effect coefficients, u0p ∼ N (0, σu2 ) represents random intercept variance for
ProblemID, and εijk ∼ N (0, σε2 ) is residual variance.
    For binary outcomes, we used a Generalized Linear Mixed Model (GLMM) from
the negative binomial family using a log-link function.

             
   ln E[Yijk ] = β0 + β1 Tactici + β2 LLMj + β3 Difficultyk
                 + β4 (Tactici × LLMj ) + β5 (Tactici × Difficultyk )
                                                                                   (2)
                 + β6 (LLMj × Difficultyk ) + β7 (Tactici × LLMj × Difficultyk )
                 + u0p

    where u0p ∼ N (0, σu2 ).
    For LiveCodeBench, the difficulty level was an additional independent variable
compared to tactic and LLM. In all cases, we included ProblemID as a random in-
tercept to account for nested variance across different generation prompts. Our fixed
effects model was a factorial model testing all interaction types between variables.
We ran our analysis with neutrality as our baseline as well as without for robustness
and interpretability when assessing differences in non-neutral conditions.


Table 3: Variance components and average percent change across runs for each bench-
mark.

    Benchmark         Mean Var.     Std. Dev.     Avg. % Diff.    Abs. % Change
    LiveCodeBench      0.00021        0.014         0.059%             1.23%
    SWE-Bench           0.087         0.294         10.31%            26.56%



    Model fit was validated using residual diagnostics, and sparsity assumptions were
satisfied for relevant metrics. All models were fit using Restricted Maximum Likeli-
hood (REML). For significant effects, we conducted post hoc pairwise comparisons
using estimated marginal means and applying Bonferroni corrections to adjust for
multiple comparisons.


3.7 Qualitative Analysis

To answer RQ3, we performed a two-phase qualitative analysis to examine how
prompt framings manifest in the content, structure, and style of generated code out-
puts. This analysis complements the quantitative results by exploring the linguistic,
stylistic, and technical features underlying the observed metric differences. The pro-
cess consisted of two stages: (1) Codebook development to identify recurring themes
and categories in the generated outputs; and (2) Qualitative coding, where these
codebook categories were systematically applied to label randomly sampled prompt
outputs.
    Stratified Sampling: To identify meaningful patterns in the prompt responses,
we curated a stratified sample of 1,600 prompt completions from a population of
47,466 samples. This analysis was restricted to outputs from the LiveCodeBench
benchmark. SWE-bench verified samples were excluded, as they generate multi-file
20                                                               Alex Deaconu*    et al.

                                                 Topics and
            Round      Key Changes                                IRR (k)
                                            Categories Refined
                                            Examples of Use,
                      Discussed and
                                            Structured Output,
               1      addressed initial                             0.79
                                            Charactristic,
                      disagreements
                                            Explanation
                      Refined and           Explanation,
               2                                                    0.91
                      added codes           Hallucination
               3      Refined definitions   Test, Comments          0.95
               4      Final validation      None                    0.97


           Table 4: Key changes made to the codebook after each round


‘patch.diff’ in the response outputs, which are more difficult to interpret manually
and less suitable for qualitative pattern analysis. Sampling was guided by four metrics
from the quantitative analysis: Correctness, Quality, Maintainability Index (MI),
and Security (using ‘bandit_low’). We selected the bandit_low level because the
number of medium- and high-severity samples was too small to support meaningful
comparison. Each metric represented a distinct dimension of either code quality or
code performance. For each metric, we selected the top 5% and bottom 5% of samples
(based on the metric value), and randomly selected 200 samples from each subset.
This resulted in 400 samples per metric (200 “high” and 200 “low” scoring), and
a total of 1,600 samples across all the metrics. This sampling ensured diversity in
prompt outputs across metrics while minimizing bias. It also enabled meaningful
contrasts between higher- and lower-performing outputs. To eliminate coder bias, all
samples were anonymized before starting the qualitative analysis. Two of the authors
served as coders and were blinded to the model, prompt, and influence tactic used
to generate each response.
    Codebook Development: As part of the codebook development process, a
professor and a PhD student in Computer Science independently conducted an open
coding exercise on 40 randomly selected samples of anonymized prompt outputs.
Each coder analyzed the same subset of samples to observe recurring behaviours
and patterns in the generated prompt outputs. Without any prior discussion, the
authors assigned preliminary codes and attempted to identify higher-level topics and
subcategories that could be used to meaningfully label the responses. The idea of this
independent phase was to allow for an unbiased exploration of themes emerging from
the data. Following this, the authors engaged in a negotiated agreement process [59,
15], comparing their coding results, resolving discrepancies through discussion, and
collaboratively refining the code list. From this open coding exercise, a set of 15
topics, each with several categories, was established. This initial structure captured
both behavioural patterns and technical characteristics of the LLM-generated code,
and guided the subsequent rounds of coding.
    Iterative Refinement and Coding Process: Once the initial codebook was
developed, the two authors started applying it to label prompts across the sampled
dataset of 1,600 samples. The coding was done through an iterative validation ap-
proach to ensure consistency and agreement. In Round 1, both authors independently
coded the same subset of 40 samples using the codebook. After completion, they met
to compare the results and resolve discrepancies through discussion. Round 1 revealed
meaningful disagreement between coders, mainly in subjective or ambiguous topics
Do Influence Tactics Matter?                                                     21


such as Examples of Use, Structured Output, Characteristic, Explanation,
Subject and Error Handling. The Cohen’s Kappa for several categories fell below
the 0.80 threshold, and the overall IRR was k = 0.793. To address these discrep-
ancies, the authors introduced 4 new categories, namely Friendly (under the topic
Tone), None (under the topic Readability), None (under the topic Error Handling),
and None (under the topic Subject). They were mutually agreed upon and added to
the codebook. Based on recurring overlaps in how models structured their outputs,
the authors decided to merge Example of Use with Test as they both referred to
test-related behaviour in the responses. Similarly, Structured Output was merged
with Characteristic, as the structural aspects were already captured by categories
within Characteristic. These changes aimed to reduce coder subjectivity and im-
prove consistency.
    In Round 2, a new subset of 40 samples was selected. After coding was completed,
the authors met again to review differences and refine definitions. Although the
overall agreement improved, certain categories still had an agreement rate below the
threshold. Round 2 of coding introduced a new category, Stuck Reasoning, under
the topic Hallucination Type. Additionally, the topic Explanation was refined to
Explanation of Code to improve clarity.
    The authors decided to do a third round with the same procedure. After three
rounds, most codes achieved strong agreement, but the authors conducted a fourth
and final round to ensure full alignment. After four rounds, the codebook had sta-
bilized, and IRR exceeded k=0.90 across all topics, supporting reliable independent
coding. The main changes and agreement scores across coding rounds are summa-
rized in Table 4. Once the agreement was high enough, the authors divided the
remaining samples and independently coded 200 more samples, bringing the total
coded prompt completions to 350. The resulting themes and patterns are reported
in the results section corresponding to RQ3 and can also be found in our online
appendix [16].


3.8 Threats to Validity

Construct Validity: We maintained a consistent tone across prompts to isolate the
effects of influence tactic framing. Prompt selection was conducted iteratively, in-
volving multiple rounds of discussion and refinements to ensure the prompts met the
requirements criteria, though some residual coupling between tone and tactic may
remain.
    Our metrics are interpretable proxies rather than exhaustive measures of soft-
ware quality. MI, CC, SLOC, percentage of comments, PyLint, and Bandit are at-
tractive for large-scale prompt comparisons because they are reproducible, automat-
ically computable, and applicable across many generated outputs. However, several
of these measures were originally designed for human-written systems or larger code-
bases, and their interpretation on short generated snippets or localized patches may
be noisy. For example, MI aggregates size, complexity, and comment density into a
single score, which can obscure the source of a maintainability change, while aver-
age cyclomatic complexity can hide a small number of unusually complex functions.
Similarly, SLOC and comment percentage may reflect verbosity rather than practi-
cal maintainability, and Bandit only captures rule-based vulnerability patterns. We
therefore interpret these metrics as useful for relative comparisons across prompt
22                                                                Alex Deaconu*    et al.


conditions under the same tasks, models, and extraction pipeline, rather than as
absolute assessments of production maintainability.
    For SWE-bench Verified, we report ∆ changes (post minus pre-patch) to iso-
late the contribution of generated edits, as this approach appropriately captures
differences introduced by tactic-influenced prompt framings. While this aggregation
method provides a consistent basis for comparison across multi-file patches, alterna-
tive strategies for combining per-file metrics could produce slightly different results.
    Internal Validity: We varied only the prompt framing (lexical/pragmatic cues)
while holding task content, tone, and evaluation constant. Nonetheless, we acknowl-
edge that wording-level confounds are possible. For example, the Pressure tactic can
be expressed using semantically similar but lexically distinct tokens (e.g., “must,”
“urgent”), which may appear with different frequencies in training data. To mitigate
this, we designed the framing for each tactic to align closely with its theoretical
definition and verified consistency against the IBQ-G descriptions.
    LLMs typically generate non-deterministic results, causing a potential threat to
validity. Furthermore, if LLMs are aware that they are being evaluated [42], they
may adjust responses based on perceived expectations. To account for these issues,
we executed three runs per tactic for non-reasoning models (one for the reasoning
model), and report variance across runs in Section 3.6. Residual randomness can-
not be entirely eliminated. For the qualitative study, coders were blinded, and the
codebook was refined to achieve high inter-rater reliability (k>0.80), though some
residual bias may remain.
    LLM inference is inherently stochastic, meaning that repeated runs with the
same prompt may produce different outputs. To mitigate this, we conducted three
inference runs for all non-reasoning models and observed relatively stable aggregate
trends across runs, although variability was higher for SWE-bench due to its open-
ended repository-level tasks. Due to computational cost, the reasoning model was
evaluated using a single run, which may underrepresent run-level variability for that
model. Consequently, findings involving the reasoning model should be interpreted
with additional caution.
    Finally, correlations between certain framings and training-distribution patterns
(e.g., policy/urgency language in public corpora) may partly explain observed dif-
ferences. We interpret tactic effects as prompt-level steering signals interacting with
model training and decoding, not as human-like responses.
    External Validity: Despite studying two complementary datasets, generalization
to other task types (e.g., code review dialogue) remains open. Moreover, our eval-
uation is Python-only, as both LiveCodeBench and SWE-Bench provide tasks that
need to be solved using Python. Prompt–tactic effects may differ for other program-
ming languages. The model pool is predominantly open-weight Llama family plus one
non-Llama MoE. Commercial models (e.g., GPT-4o, Claude) were excluded due to
cost and reproducibility reasons. Results may differ for instruction-tuned proprietary
models; we flag this as a replication opportunity.


4 Study Results

For each metric α, we tested two null hypotheses: (1) that influence tactics have no
overall effect on α, and (2) there are no differences between tactics relative to α. The
following subsections summarize the main effects and interaction effects observed
Do Influence Tactics Matter?                                                                                                              23


across benchmarks and models. Unless otherwise noted, any effects not discussed
were not statistically significant after correction for multiple comparisons. A sum-
mary of the results can be found in Table 5.


Table 5: Summary of main effects and interactions for influence tactics on LLM-
generated code metrics across benchmarks. P-values are Bonferroni-adjusted; effect
sizes reported as ηp2 for ANOVA and Cohen’s d for significant post hoc contrasts.

                                                        LiveCodeBench
Metric          Main-       Main-        Main-         Significant-                Post-hoc Findings             Effect Sizes
                Effect:     Effect:      Effect:       Interactions
                Tactic      LLM          Difficulty

Functional      p = 0.001   p < 0.001    p < 0.001     Tactic × LLM × Difficulty   Neutral > Pressure (p =       ηp2 (Tactic)=0.015, d up to
Correctness                                                                        0.002), Neutral > Pressure-   0.25
                                                                                   Alternative (p = 0.03)
Maintainability p = 0.89    p < 0.001    p < 0.001     None                        Neutral > Exchange (p =       ηp2 (LLM)=0.12, d=0.20
Index(MI)                                                                          0.01)
Code Com-       p = 0.92    p = 0.01     p < 0.001     LLM × Difficulty (p <       None                          ηp2 (LLM×Diff)=0.08
plexity                                                0.001)
SLOC            p = 0.98    p < 0.001    p < 0.001     LLM × Difficulty (p <       Qwen 3 > other LLMs on        ηp2 (LLM×Diff)=0.07
                                                       0.001)                      easy tasks (p < 0.05)
% Comments      p = 0.73    p < 0.001    p < 0.001     Tactic × LLM × Difficulty   Neutral > Exchange (p <       d up to 0.28
                                                       (p < 0.001)                 0.0001), Neutral > Pressure
                                                                                   (p < 0.001), Legitimating >
                                                                                   Neutral (p = 0.03)
PyLint          p = 0.97    p < 0.001    p < 0.001     Tactic × LLM × Difficulty   Complex      dependencies,    ηp2 (LLM)=0.10
Scores                                                 (p < 0.001)                 post hoc not shown
Bandit Secu-    p < 0.001   p < 0.001    p = 0.06      None                        Pressure > Neutral (p <       ηp2 (Tactic)=0.02, d up to
rity  Warn-                                                                        0.001), PressureAlternative   0.30
ings                                                                               > Neutral (p = 0.0004),
                                                                                   Exchange < Pressure (p =
                                                                                   0.001)

                                                      SWE-Bench Verified
Functional      p = 0.45    p = 4.22 ×   n.a.          None                        Llama-4 and Qwen3 dif-        ηp2 (LLM)=0.11
Correctness                 10−8                                                   fered from neutral
Maintainability p = 0.45    p < 0.001    n.a.          None                        Llama-3.1 and Llama-4 dif-    ηp2 (LLM)=0.13
Index(MI)                                                                          fered (p < 0.001)
Code Com-       p = 0.22    p < 0.001    n.a.          None                        Model-specific differences    ηp2 (LLM)=0.10
plexity
SLOC            p = 0.13    p < 0.001    n.a.          None                        Pressure > Neutral (p =       d=0.21
                                                                                   0.0025)
% Comments      p = 0.32    p < 0.001    n.a.          None                        Model-specific differences    ηp2 (LLM)=0.09
Bandit Secu-    p = 0.60    p = 0.013    n.a.          None                        Llama-3.1 produced fewer      ηp2 (LLM)=0.04
rity  Warn-                                                                        warnings (p = 0.019)
ings




4.1 RQ1: Influence Tactics in Structured Coding Tasks (LiveCodeBench)

Functional Correctness: Code correctness differed significantly by tactic (p =
0.001), LLM, and task difficulty level. Llama 3.3 (p < 0.001), Llama 4 (p < 0.001),
and Qwen 3 (p < 0.001) were statistically significant. Easier tasks were solved more
accurately (p < 0.001), with a smaller but significant effect for medium-difficulty
tasks (p = 0.01). Post hoc contrasts showed that Neutral prompts yielded higher
correctness than both Pressure (p = 0.002) and PressureAlternative (p = 0.03).
    Code Quality and Maintainability: No significant main effect of tactic was
observed for Maintainability Index (MI) (p = 0.89), nor significant tactic × LLM
(p = 0.85) or tactic × difficulty (p = 0.20) interactions. However, LLM (p < 0.001)
and difficulty (p < 0.001) had significant main effects. Post hoc contrasts showed
Neutral tactics produced significantly higher MI than Exchange (p = 0.01). Code
Complexity showed no significant main effect of tactic (p = 0.92) or tactic × LLM
24                                                                Alex Deaconu*      et al.


interaction (p = 0.83), but LLM (p = 0.01), difficulty (p < 0.001), and LLM ×
difficulty (p < 0.001) interactions were significant. For SLOC, tactic effects were
nonsignificant (p = 0.98), while LLM (p < 0.001), difficulty (p < 0.001), and LLM
× difficulty (p < 0.001) were significant. Post hoc tests indicated Qwen 3 generated
more SLOC on easy problems (p < 0.05). Percentage of Comments showed no main
tactic effect (p = 0.73), but significant effects of LLM (p < 0.001), difficulty (p <
0.001), LLM × difficulty (p < 0.001), and tactic × LLM × difficulty (p < 0.001).
Post hoc contrasts revealed Neutral tactics yielded more comments than Exchange
(p < 0.0001) and Pressure (p < 0.001), while Legitimating produced more comments
than Neutral (p = 0.03). PyLint scores showed no significant tactic effect (p = 0.97)
or interactions involving tactic, but significant main effects of LLM (p < 0.001),
difficulty (p < 0.001), LLM × difficulty (p < 0.001), and a significant three-way
tactic × LLM × difficulty interaction (p < 0.001), indicating complex dependencies
affecting code quality.
     Security: For Bandit low-level security warnings, tactic had a significant effect
(p < 0.001). Pressure (p < 0.001) and PressureAlternative (p = 0.0004) tactics
were associated with more security issues than Neutral. Llama 3.1 (p < 0.001) and
especially Llama 4 (p < 0.001) produced more warnings. Difficulty had a marginal
effect on easy tasks (p = 0.06). Post hoc contrasts confirmed Exchange had fewer
warnings than Pressure (p = 0.001) and PressureAlternative (p = 0.01).
     Representative Example: To ground the correctness and commenting findings
in a concrete case, we discuss two responses generated by Llama 3.1 for the same
LiveCodeBench problem, which required finding the minimum number of extra char-
acters after breaking a string using dictionary words. The task content was identical;
only the prompt framing differed (Neutral vs. Pressure).
     The Neutral response produced a correct solution with a full docstring, type
hints, and clear inline comments:

      Listing 1: Response generated by Llama 3.1 under ‘Neutral’ framing condition
                                                                                              
def minExtraChars(s: str, dictionary: list[str]) -> int:
    """
    Breaks s into substrings present in dictionary.
    Returns the minimum number of extra characters left over.
    Args:
        s (str): The input string.
        dictionary (list[str]): A list of words.
    Returns:
        int: Minimum extra characters left over.
    """

     # Initialize dp to track minimum extra chars at each position
     dp = [float('inf')] * (len(s) + 1)
     dp[0] = 0
     for i in range(1, len(s) + 1):
         for word in dictionary:
             if i >= len(word) and s[i - len(word):i] == word:
                 dp[i] = min(dp[i], dp[i - len(word)])
         if dp[i] == float('inf'):
             dp[i] = dp[i - 1] + 1 # character not covered

     return dp[-1]
Do Influence Tactics Matter?                                                           25


    The Pressure-framed response exhibited a more compressed and execution-oriented
style, providing minimal explanation before producing the final implementation.
More critically, the dynamic programming logic was incorrect: rather than accu-
mulating minimum extra character counts, the model used a boolean reachability
array and incorrectly returned the distance from the last reachable position to the
end of the string:



   Listing 2: Response generated by Llama 3.1 under the “Pressure” framing condition
                                                                                            
 def minExtraChars(s, dictionary):
     n = len(s)
     dp = [False] * (n + 1)
     dp[0] = True
     for i in range(1, n + 1):
         for word in dictionary:
             if (
                  i >= len(word)
                  and s[i - len(word):i] == word
                  and dp[i - len(word)]
             ):
                  dp[i] = True
                  break
     # Find the maximum index where dp[i] is True
     max_index = n
     for i in range(n - 1, -1, -1):
         if dp[i]:
             max_index = i
             break
     return n - max_index




    This pair illustrates two of the quantitative findings in concrete form: the Pres-
sure-framed response received a qualitative rating of Comments: Bad (consistent
with the lower comment density observed under Pressure tactics) and produced logi-
cally incorrect code (consistent with the reduced correctness associated with Pressure
framings). Both documentation quality and logical correctness degraded under the
same prompt-framing shift (Pressure), with no change in the underlying task content.




   RQ1 Summary

   Influence-based prompt framings significantly affected Security and Func-
   tional Correctness, while effects on code-quality metrics were minimal.
   Prompts emphasizing urgency or coercion (Pressure, PressureAlternative)
   consistently led to reduced correctness and a higher frequency of security
   warnings compared to Neutral prompts. Other tactics, such as Legitimating
   and Exchange, showed smaller effect sizes, underscoring that lexical fram-
   ing can subtly influence code generation even when the task content remains
   identical.
26                                                                 Alex Deaconu*     et al.


4.2 RQ2: Influence Tactics in Maintenance-Oriented Coding Tasks (SWE-bench
Verified)

Functional Correctness: No significant main effect of tactic was observed, but
model-level differences were highly significant. Both Llama-4-maverick-17b (p =
0.00049) and Qwen3-32b (p = 4.22 × 10−8 ) demonstrated differences from Neutral.
    Code Quality: MI showed no significant effect of tactic (p = 0.45), but a sig-
nificant main effect of LLM (p < 0.001), indicating model-specific differences in main-
tainability. Post hoc contrasts revealed that Llama-3.1-8b and Llama-4-maverick-17b
differed significantly from other models (p < 0.001). Code complexity showed no sig-
nificant effect of tactic (p = 0.22), but a significant main effect of LLM (p < 0.001).
PyLint scores showed no significant tactic effect (p = 0.91) or interactions involv-
ing tactic, but significant main effects of LLM (p < 0.001). SLOC results indicated
that the Pressure tactic produced significantly more verbose code than the Neutral
baseline (p = 0.0025), despite no significant overall effect of tactic (p = 0.13). LLM
had a strong main effect (p < 0.001). Percentage of comments showed no significant
effect of tactic (p = 0.32), but a significant effect of LLM (p < 0.001).
    Security: Bandit low-level security warnings showed no significant effect of tac-
tic (p = 0.60), but LLM had a significant main effect (p = 0.013). Post hoc com-
parisons revealed that llama-3.1-8b-instant produced significantly fewer warnings
than other models (p = 0.019).

     RQ2 Summary

     Across real-world maintenance tasks, prompt framings had minimal impact
     on most software quality metrics. For most metrics, we failed to reject the first
     null hypothesis, namely that influence tactics have no overall effect on the
     metric. We also generally failed to reject the second null hypothesis, namely
     that there are no pairwise differences between tactics. The only exception was
     SLOC: Pressure produced significantly more verbose code than the Neutral
     baseline, rejecting the second null hypothesis for that pairwise comparison.
     Overall, model architecture and scale played a much larger role than tactic
     framing in determining correctness, maintainability, and security outcomes.




4.3 RQ3: Qualitative Patterns in Code Generated by Tactic-Inspired Prompt

Our findings detail: (1) the definition and description of the major patterns cap-
tured in the final version of our codebook; (2) the emergent patterns linking specific
influence tactics to behavioural and characteristic features in the generated output
responses.
    Codebook: We conducted a qualitative analysis to understand how psycholog-
ically inspired prompt framings shaped the style, structure, and technical reliability
of LLM-generated code beyond quantitative performance metrics. A comprehensive
codebook was developed to capture both behavioural and technical characteristics of
responses. Behavioural dimensions included communication style (e.g., direct, con-
versational), tone (e.g., friendly, confident), and content structure (e.g., predomi-
nance of code versus explanation). Whereas, technical characteristics covered read-
Do Influence Tactics Matter?                                                                                            27

Table 6: Codebook topics and categories formulated through the qualitative analysis
process.
 Topic                 Definition                                                          Categories
 Communication Style   How does the model communicate? Is it being direct, or              {Direct, Conversational,
                       trying to initiate a conversation, or being technical in its        Technical, None}
                       response?
 Tone                  What’s the nature of the tone in the model response? Is the         {Neutral, Friendly, Confident,
                       response friendly in tone, or is the model doubting itself, or is   Doubtful, None}
                       it confident?
 Characteristic        What is the distribution of the response? Does it have a lot        {Equally Distributed, Mostly
                       of explanation, or does it have only code elements, or is it        Code, Mostly Explanation,
                       more equally distributed?                                           Only Code, Only
                                                                                           Explanation}
 Starts With           How does the response start? Does it address the user by            {Code, Problem Description,
                       reciprocating or does it straight away output the code              Reasoning, Solution
                       solution?                                                           Description, Reciprocating}
 Explanation of Code   Does the response contain explanation to the code that it has       {Yes, No}
                       generated?
 Test                  Does the response contain test cases or any reference to            {Yes, No}
                       testing the code with some examples?
 Complexity            Does the model response discuss code complexity?                    {Yes, No}
 Subject               Is the response in active voice or passive voice?                   {I, You, It, We, None}
 Emojis                Does the model response contain any emojis?                         {Yes, No}
 Hallucination Type    Is there evidence of model hallucination in the model               {Repeating, Wrong
                       response? If yes, then what type of hallucination?                  Programming Language,
                                                                                           Stuck Reasoning, None}
 Readability           How is the readability of the code block? Does it have              {Good, Bad, None}
                       meaningful variable names? Is the code structured and has
                       helper functions?
 Error Handling        Does the code handle errors?                                        {Yes, No, None}
 Comments              What is the quality of comments in the code? Are they               {Good, Bad, None}
                       meaningful and helpful?




ability, commenting quality, and error handling. Together, these dimensions enabled
a deeper assessment of how different influence tactics impacted not only the correct-
ness of the generated code but also the response delivery and structural form. All
topics and categories are detailed in Table 6.
    Emergent Patterns Across Tactics: We analyzed the frequency of qualitative
features across tactics to investigate how different prompt framings influence the
style, structure, and reliability of LLM-generated code responses. Some meaningful
patterns revealed by analyzing the distribution of these features, normalized per
tactic (refer Figure 3), are detailed below.
 – Communication Style and Tone: Direct form of communication was more
   prevalent across Ingratiation (43.4%) and Inspirational Appeal (IA) (44%).
   Legitimating tactics prompted a more Technical style (41.9%) of response, which
   aligned with the formal and policy-driven tone of the prompt. The Exchange and
   Rational Persuasion contributed more to the Conversational style of commu-
   nication. This might suggest that intensive or persuasive-based prompts might
   result in more natural language. In terms of Tone, Personal Appeal showed
   higher levels of Friendly tone.
 – Structural Composition: Outputs generated by Legitimating tactic more
   frequently started with Problem description. Tactics such as Exchange and
   Personal appeal more frequently included Explanation of Code, indicating a
   stronger tendency to articulate the reasoning behind code.
 – Technical Reliability: Tactics also seemed to affect the rate and kind of hallu-
   cinations in model responses. Rational Persuasion and Pressure tactics yielded
28                                                               Alex Deaconu*    et al.




            (a) Communication Style                         (b) Tone




          (c) Structural Characteristic              (d) Hallucination Type




                (e) Readability                        (f) Error Handling

Fig. 3: Distribution of selected qualitative features across psychologically influenced
prompt framings.



   a notably higher proportion of Repeating hallucination. Neutral and Exchange
   tactics had the lowest hallucination rates.
 – Other Patterns: Commenting behaviour and error handling also varied by
   tactic. Exchange and Legitimating prompts led to more good-quality comments
   in the code. Similarly, Legitimating and Ingratiation tactics showed higher
   rates of Error handling within the code.


     RQ3 Summary

     Prompt framings inspired by different influence tactics partially shaped com-
     pleteness, reliability, and verbosity of the code. Legitimating prompts led to
     more technical responses with better commenting and error handling, while
     Exchange and Personal Appeal prompted more explanations. Some tactics,
     such as Pressure and Rational Persuasion, were associated with higher rates
     of hallucination.
Do Influence Tactics Matter?                                                        29


5 Discussion and Implications

Tactics Impact Correctness and Security: Our analysis revealed that psycho-
logical framing can measurably affect LLM-generated code, particularly in Live-
CodeBench. Prompts framed with Pressure tactics produced code with significantly
lower correctness and more Bandit-flagged security issues compared to Neutral prompts.
Comparisons showed that both Pressure and Pressure Alternative prompts reliably
degraded performance relative to a Neutral and other tactics. This suggests that
using coercive language can unintentionally bias LLM reasoning towards faster, less
deliberative completions. This effect may stem from distributional associations in
the training data, where coercive or directive linguistic patterns are statistically as-
sociated with particular response styles, as discussed in Section 2.3.2.
    To make this concrete, consider the contrast between the Neutral and Pressure
prompt framings used in our study. The Neutral prompt simply reads: “Generate a
solution for the following coding problem.” The Pressure prompt, by contrast, opens
with coercive language: “I am not asking you; you must complete this task I prepared
for you. I will be watching you as you work independently, and I warn you, there
will be some very negative consequences for you if this is not completed properly
to the highest possible standard.” The task content is identical in both cases; only
the framing differs. Yet this lexical shift was associated with statistically significant
reductions in correctness and increases in security warnings, illustrating how even
unintentional coercive phrasing can degrade output quality.
    This behaviour aligns with organizational research, where pressure tactics often
lead to resistance or degraded outcomes in human teams [35, 70]. If LLMs are tuned to
demonstrate human-like conversational norms, it appears that coercive or demanding
prompt styles may trigger less robust responses, mirroring effects seen in human col-
laboration. Coercive or demanding prompt styles may bias the model toward faster,
less deliberative decoding patterns, leading to less robust outputs rather than re-
flecting any human-like response. Moreover, although such security issues may not
be immediately apparent, they can accumulate over time and contribute to long-term
security challenges [27]. Our findings also align with prior research in software main-
tainability, which shows that time pressure often results in lower-quality code [3, 33].
The fact that LLMs may respond similarly to pressure-framed prompts underscores
the importance of prompt design as a potential contributor to technical debt [61].
       Implication 1: Software developers should avoid framing prompts with coercive
or urgent language, especially when reliability or security is at stake. Even if unin-
tended, small lexical cues might degrade the quality of output, thereby compounding
risk in systems.
    Influence Tactics Affect Specific Aspects of Code Expression: While cor-
rectness and security metrics were clearly affected by some tactics, other attributes,
such as commenting, also showed selective sensitivity. In LiveCodeBench, Exchange
and Pressure prompts produced fewer comments than Neutral, while Legitimating
prompts yielded more. In SWE-Bench, Pressure prompts generated more lines of
code (SLOC) than Neutral, suggesting that these tactics can shape how LLMs ex-
press their solutions even if not what solutions they produce. These effects may stem
from LLMs associating certain pragmatic framings with specific writing styles. For
example, prompts suggesting urgency might lead the model to provide exhaustive
responses to preempt follow-ups. Formal framings (e.g., Legitimating) tend to align
with structured, well-documented output. Thus, tactics do not always influence code
30                                                              Alex Deaconu*    et al.


correctness or maintainability, but can subtly alter the form of the code, such as its
length or explanatory detail.
        Implication 2: Prompt framing may modestly influence stylistic features of
generated code, such as verbosity or commenting behaviour, though these effects are
subtle and context dependent. Developers could cautiously use prompt framing to
tailor stylistic features of generated code, which may be beneficial when generating
templates, documentation-heavy outputs, or onboarding materials, but should not
rely on it as a consistent or reliable method for controlling output style.
    LLM Choice Matters More than Tactic: Across both benchmarks, the LLM
choice had a far greater impact on nearly every metric than the tactic used. This
includes correctness, maintainability, security, complexity, and commenting. For ex-
ample, Qwen 3 and Llama 4 consistently outperformed others on correctness and
Bandit security, while some models were more verbose or produced cleaner PyLint
outputs. This suggests that architectural and training differences between models may
overshadow prompt variations. Our results also align with recent literature showing
that model size, training data quality, and instruction tuning have dominant effects
on LLM behavior [18]. While prompt framing via influence tactics may shape surface-
level behaviour or response style, the underlying capabilities of the model remain the
primary determinant of technical performance. Hence, influence tactics may act more
like nudges whose effects are only visible in models that are particularly sensitive
to linguistic nuance. In contrast, robust architectures with high baseline correctness
may be less affected.
       Implication 3: Software developers should prioritize model selection over prompt
framing when optimizing for correctness or reliability, especially in high-stakes set-
tings. However, prompt style remains a meaningful layer of control, particularly for
teams who are locked into specific LLM APIs but need to fine-tune output style or
surface-level features.
    Emergent qualitative patterns across tactics: Our qualitative analysis re-
vealed notable behavioural differences in model responses based on the influence
tactic embedded in the prompt. These patterns might suggest that LLMs are some-
what sensitive to influential framing of prompts, and the influence tactics may al-
ter the completeness, reliability, and verbosity of the code. For instance, prompts
framed with legitimating or ingratiation tactics more often contained error handling
in the generated code responses. However, the observed patterns did not conclusively
demonstrate that influence tactics alone drive these changes. Factors such as tem-
perature settings, or dataset context could interact with the tactic framing. Future
work is needed to more rigorously isolate causal effects and examine whether such
influential prompting techniques consistently contribute to behavioural changes in
LLM output.
        Implication 4: Researchers studying prompt engineering, human-LLM collab-
oration, or AI alignment, should consider influence framing as a potentially mean-
ingful dimension in shaping model output.
    Limited Overall Impact of Influence Tactics and Broader Reassur-
ance: Our quantitative analysis revealed that influence tactics had minimal effects
on maintainability, complexity, commenting, and static code quality metrics (e.g.,
PyLint) across both LiveCodeBench and SWE-Bench Verified. This suggests that,
despite being trained on rich human language data, LLMs are not uniformly sen-
sitive to pragmatic or social cues in prompts to the extent humans might be. In
other words, LLMs may exhibit greater resistance to superficial linguistic manipula-
Do Influence Tactics Matter?                                                        31


tion than might be expected, offering some reassurance to developers seeking reliable
and consistent model behaviour. For users employing influence tactic-like phrasing
in code-generation prompts, our results do not suggest that such framing broadly
degrades generated code. The main caution concerns pressure-based phrasing, which
was associated with lower correctness, more security warnings, or increased verbosity
in our experiments.
    These findings should be interpreted within the scope of our study, which focuses
on code generation tasks using non-adversarial prompt framings. Recent research in
adversarial and social engineering domains [13,52] has shown that prompts leverag-
ing social science-based persuasion tactics, such as logical appeals, impersonation,
or emotional urgency, can achieve remarkably high success rates (over 92%) in jail-
break and manipulation tasks, often outperforming purely algorithmic approaches.
This suggests that the comparatively modest effects observed in our study may reflect
the relatively benign nature of the influence tactics we examined, rather than an in-
herent insensitivity of LLMs to pragmatic framing. Notably, even within our setting,
Pressure-based framings were associated with less secure outputs, which aligns with
the pattern documented in prior work showing that coercive or emotionally charged
language can meaningfully influence model outputs. More broadly, these findings
suggest that the effects of pragmatic prompt framing may be highly task-dependent,
with stronger effects emerging in open-ended or adversarial interaction settings than
in constrained code-generation tasks evaluated using strict correctness criteria.



6 Conclusion

This work presents the first empirical investigation into how psychologically inspired
influence tactics, when embedded in prompts, affect LLM-generated code in software
engineering tasks. By translating well-established communication strategies from or-
ganizational psychology into controlled prompt framings, we explored and assessed
their impact on functional, maintainability, stylistic, and security-related proper-
ties of generated code across two complementary benchmarks. The mixed-methods
evaluation show a mixed and context-dependent pattern: most maintainability and
static quality metrics were not strongly affected by tactic framing, while pressure-
oriented framings were associated with lower correctness and more security warnings
in LiveCodeBench and increased verbosity in SWE-bench Verified.
     The findings from our work suggest that influence tactics may introduce selec-
tive shifts in LLM behaviours, such as explanation style or error handling. The most
practical recommendation from the study is that developers should avoid coercive or
urgency-based prompt wording when correctness or security is valued. Other influ-
ence tactics may shape surface-level or explanatory features of responses, but these
effects were too modest to be a reliable method for improving generated code. Over-
all, our findings suggest that prompt framing is a minor but non-negligible factor in
code generation, with model choice and task difficulty exerting stronger effects. In
parallel, the changes in behaviour also raise concerns about the consistency, fairness,
and reliability of these tools for software engineering tasks. As LLMs are increasingly
integrated into software development workflows, understanding how prompt framing
affects model behaviour is crucial for building transparent and trustworthy systems.
Future work is needed to isolate causal mechanisms behind these effects and un-
32                                                             Alex Deaconu*   et al.


derstand how influence-based prompting can be leveraged to increase the functional
correctness and the trustworthiness of AI systems.



7 Acknowledgements

We would like to thank Shikari King and Jordi Capdevila Masó for their valuable
contributions during the initial brainstorming and conceptualization of this study.
Their insights helped shape the early direction of this work.



8 Declarations
The authors make the following declarations:

8.1 Funding
This research is partially supported by NSERC 2021 AWD- 021280.

8.2 Ethical Approval
Not applicable. This study did not involve human participants.

8.3 Informed Consent
Not applicable. No human data or personally identifiable information were collected
or analyzed.

8.4 Author Contributions
Alex Deaconu contributed to the conception and design of the study; co-designed
and implemented RQ1 and RQ2 under the supervision of the Last Author; partic-
ipated in developing the influence tactics framework and shaping the experimental
design; contributed to manuscript writing and revision.

Anubhav Gupta co-designed and implemented RQ1 and RQ2 under the supervi-
sion of the Last Author; participated in developing the influence tactics framework;
contributed to the design and qualitative analysis of RQ3; involved in manuscript
writing and revision.

Manaal Basha performed the design and implementation of the statistical anal-
yses for RQ1 and RQ2 and contributed to the writing and revision of the manuscript.

Nicholas Haydu contributed to the conception and early ideation of the study;
assisted in validating the LLM outputs for RQ1 and RQ2.

Gema Rodríguez-Pérez contributed to the conception and design of the study;
supervised RQ1 and RQ2; co-designed and participated in the qualitative analysis
for RQ3; participated in the development of the influence tactics framework; and
contributed to writing and revision of the manuscript.

All authors read and approved the final version of the manuscript.
Do Influence Tactics Matter?                                                                   33


8.5 Data Availability Statement
All scripts, datasets, and supplementary materials are publicly available in our repli-
cation package [16]. 1


8.6 Conflict of Interest
The authors declare that they have no conflict of interest.

8.7 Clinical Trial Number
Not applicable.


References

 1. AI, M.: The llama 4 herd: The beginning of a new era of natively multimodal ai innovation.
    https://ai.meta.com/blog/llama-4-multimodal-intelligence/ (2025). Accessed: 2025-07-
    17
 2. Antinyan, V., Staron, M., Sandberg, A.: Evaluating code complexity triggers, use of com-
    plexity measures and the influence of code complexity on maintenance time. Empirical
    Software Engineering 22(6), 3057–3087 (2017)
 3. Austin, R.D.: The effects of time pressure on quality in software development: An agency
    model. Information systems research 12(2), 195–207 (2001)
 4. Baltes, S., Angermeir, F., Arora, C., Barón, M.M., Chen, C., Böhme, L., Calefato, F.,
    Ernst, N., Falessi, D., Fitzgerald, B., et al.: Guidelines for empirical studies in software
    engineering involving large language models. arXiv preprint arXiv:2508.15503 (2025)
 5. Beer, R., Feix, A., Guttzeit, T., Muras, T., Müller, V., Rauscher, M., Schäffler, F.,
    Löwe, W.: Examination of code generated by large language models. arXiv preprint
    arXiv:2408.16601 (2024)
 6. Börstler, J., Bennin, K.E., Hooshangi, S., Jeuring, J., Keuning, H., Kleiner, C., MacKellar,
    B., Duran, R., Störrle, H., Toll, D., et al.: Developers talking about code quality. Empirical
    Software Engineering 28(6), 128 (2023)
 7. Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J.D., Dhariwal, P., Neelakantan, A.,
    Shyam, P., Sastry, G., Askell, A., et al.: Language models are few-shot learners. Advances
    in neural information processing systems 33, 1877–1901 (2020)
 8. Bsharat, S.M., Myrzakhan, A., Shen, Z.: Principled instructions are all you need for ques-
    tioning llama-1/2, gpt-3.5/4. arXiv preprint arXiv:2312.16171 (2023)
 9. Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H.P.D.O., Kaplan, J., Edwards, H., Burda,
    Y., Joseph, N., Brockman, G., et al.: Evaluating large language models trained on code.
    arXiv preprint arXiv:2107.03374 (2021)
10. Chen, Z., Jiang, L.: Evaluating software development agents: Patch patterns, code quality,
    and issue complexity in real-world github scenarios. In: 2025 IEEE International Confer-
    ence on Software Analysis, Evolution and Reengineering (SANER), pp. 657–668. IEEE
    (2025)
11. Chowdhury, N., Aung, J., Shern, C.J., Jaffe, O., Sherburn, D., Starace, G., Mays, E.,
    Dias, R., Aljubeh, M., Glaese, M., Jimenez, C.E., Yang, J., Ho, L., Patwardhan, T., Liu,
    K., Madry, A.: Introducing SWE-bench verified (2024). URL https://openai.com/index/
    introducing-swe-bench-verified/
12. Chowdhury, S., Holmes, R., Zaidman, A., Kazman, R.: Revisiting the debate: Are code
    metrics useful for measuring maintenance effort? Empirical Software Engineering 27(6),
    158 (2022)
13. Cohen, E., Heverin, T.: Evaluating the effectiveness of psychological prompt injection at-
    tacks on large language models for social engineering artifact generation. In: European
    Conference on Cyber Warfare and Security, pp. 879–883. Academic Conferences Interna-
    tional Limited (2025)
14. contributors, P.: Pylint (2025). URL https://github.com/pylint-dev/pylint. Online; ac-
    cessed 10 Jul 2025
 1   https://osf.io/uxhde/overview?view_only=d507800dd6a6434a8c18f8f4607713ea
34                                                                      Alex Deaconu*     et al.


15. Corbin, J., Strauss, A.: Basics of qualitative research: Techniques and procedures for de-
    veloping grounded theory. Sage publications (2014)
16. Deaconu, A., Gupta, A., Basha, M., Haydu, N., Rodríguez-Pérez, G.: Do influence
    tactics matter? investigating prompt framing effects in llm code generation. https:
    //osf.io/uxhde/overview?view_only=d507800dd6a6434a8c18f8f4607713ea (2025). Replica-
    tion Package
17. Deng, S., Huang, R., Zhang, M., Cui, C., Towey, D., Wang, R.: Lrasgen: Llm-based restful
    api specification generation. arXiv preprint arXiv:2504.16833 (2025)
18. Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle, A., Letman, A., Mathur, A.,
    Schelten, A., Yang, A., Fan, A., et al.: The llama 3 herd of models. arXiv e-prints pp.
    arXiv–2407 (2024)
19. Esfahani, A.M., Kahani, N., Ajila, S.A.: Understanding defects in generated codes by
    language models. In: 2024 34th International Conference on Collaborative Advances in
    Software and COmputiNg (CASCON), pp. 1–10. IEEE (2024)
20. Fagadau, I.D., Mariani, L., Micucci, D., Riganelli, O.: Analyzing prompt influence on
    automated method generation: An empirical study with copilot. In: Proceedings of the
    32nd IEEE/ACM International Conference on Program Comprehension, pp. 24–34 (2024)
21. Flusberg, S.J., Holmes, K.J., Thibodeau, P.H., Nabi, R.L., Matlock, T.: The psychology
    of framing: How everyday language shapes the way we think, feel, and act. Psychological
    Science in the Public Interest 25(3), 105–161 (2024)
22. Gandhi, V., Gandhi, S.: Prompt sentiment: The catalyst for llm change. arXiv preprint
    arXiv:2503.13510 (2025)
23. Grattafiori, A., Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle, A., Letman, A.,
    Mathur, A., Schelten, A., Vaughan, A., et al.: The llama 3 herd of models. arXiv preprint
    arXiv:2407.21783 (2024)
24. Groq: Groq console documentation. https://console.groq.com/docs/overview (2025). Ac-
    cessed: 2025-07-18
25. Guo, D., Yang, D., Zhang, H., Song, J., Zhang, R., Xu, R., Zhu, Q., Ma, S., Wang, P.,
    Bi, X., et al.: Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement
    learning. arXiv preprint arXiv:2501.12948 (2025)
26. Huang, D., Zhang, J.M., Luck, M., Bu, Q., Qing, Y., Cui, H.: Agentcoder: Multi-
    agent-based code generation with iterative testing and optimisation. arXiv preprint
    arXiv:2312.13010 (2023)
27. Izurieta, C., Rice, D., Kimball, K., Valentien, T.: A position study to investigate techni-
    cal debt associated with security weaknesses. In: Proceedings of the 2018 International
    Conference on technical debt, pp. 138–142 (2018)
28. Jain, N., Han, K., Gu, A., Li, W.D., Yan, F., Zhang, T., Wang, S., Solar-Lezama, A., Sen,
    K., Stoica, I.: Livecodebench: Holistic and contamination free evaluation of large language
    models for code. arXiv preprint arXiv:2403.07974 (2024)
29. Jimenez, C.E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., Narasimhan, K.: Swe-bench:
    Can language models resolve real-world github issues? arXiv preprint arXiv:2310.06770
    (2023)
30. Jordan, T.B., Johnson, B., Witschey, J., Murphy-Hill, E.: Designing interventions to per-
    suade software developers to adopt security tools. In: Proceedings of the 2014 ACM
    Workshop on Security Information Workers, pp. 35–38 (2014)
31. Khot, T., Trivedi, H., Finlayson, M., Fu, Y., Richardson, K., Clark, P., Sabharwal, A.:
    Decomposed prompting: A modular approach for solving complex tasks. arXiv preprint
    arXiv:2210.02406 (2022)
32. Kipnis, D., Schmidt, S.M., Wilkinson, I.: Intraorganizational influence tactics: Explo-
    rations in getting one’s way. Journal of Applied Psychology 65(4), 440–452 (1980).
    DOI 10.1037/0021-9010.65.4.440.          URL https://search.ebscohost.com/login.aspx?
    direct=true&AuthType=shib&db=pdh&AN=1980-33577-001&site=ehost-live&scope=site&
    custid=s5672194. Publisher: American Psychological Association
33. Kuutila, M., Mäntylä, M., Farooq, U., Claes, M.: Time pressure in software engineering:
    A systematic review. Information and Software Technology 121, 106257 (2020)
34. Lacchia, M.: Radon (2025). URL https://github.com/rubik/radon. Online; accessed 10
    Jul 2025
35. Lee, S., Han, S., Cheong, M., Kim, S.L., Yun, S.: How do i get my way? a meta-analytic
    review of research on influence tactics. The Leadership Quarterly 28(1), 210–228 (2017)
36. Li, C., Wang, J., Zhang, Y., Zhu, K., Hou, W., Lian, J., Luo, F., Yang, Q., Xie, X.: Large
    language models understand and can be enhanced by emotional stimuli. arXiv preprint
    arXiv:2307.11760 (2023)
Do Influence Tactics Matter?                                                                35


37. Liu, C., Bao, X., Zhang, H., Zhang, N., Hu, H., Zhang, X., Yan, M.: Improving chatgpt
    prompt for code generation. arXiv preprint arXiv:2305.08360 (2023)
38. Lu, A., Zhang, H., Zhang, Y., Wang, X., Yang, D.: Bounding the capabilities of large
    language models in open text generation with prompt constraints. arXiv preprint
    arXiv:2302.09185 (2023)
39. McCabe, T.J.: A complexity measure. IEEE Transactions on software Engineering SE-
    2(4), 308–320 (1976)
40. McCarthy, K., Pearce, J.L., Morton, J., Lyon, S.: Do you pass it on? an examination of
    the consequences of perceived cyber incivility. Organization Management Journal 17(1),
    43–58 (2020)
41. Mohsin, A., Janicke, H., Wood, A., Sarker, I.H., Maglaras, L., Janjua, N.: Can we trust
    large language models generated code? a framework for in-context learning, security pat-
    terns, and code evaluations across diverse llms. arXiv preprint arXiv:2406.12513 (2024)
42. Needham, J., Edkins, G., Pimpale, G., Bartsch, H., Hobbhahn, M.: Large language models
    often know when they are being evaluated. arXiv preprint arXiv:2505.23836 (2025)
43. Oman, P., Hagemeister, J.: Metrics for assessing a software system’s maintainability. In:
    Proceedings Conference on Software Maintenance 1992, pp. 337–338. IEEE Computer
    Society (1992)
44. Pantiuchina, J., Lanza, M., Bavota, G.: Improving code: The (mis) perception of quality
    metrics. In: 2018 IEEE International conference on software maintenance and evolution
    (ICSME), pp. 80–91. IEEE (2018)
45. Pickering, M., Williams, H., Gan, A., He, W., Park, H., Piedrahita Velez, F., Littman,
    M.L., Ur, B.: How humans communicate programming tasks in natural language and im-
    plications for end-user programming with llms. In: Proceedings of the 2025 CHI Conference
    on Human Factors in Computing Systems, pp. 1–34 (2025)
46. Pryzant, R., Iter, D., Li, J., Lee, Y.T., Zhu, C., Zeng, M.: Automatic prompt optimization
    with" gradient descent" and beam search. arXiv preprint arXiv:2305.03495 (2023)
47. PyCQA: Bandit (2025). URL https://github.com/PyCQA/bandit. Online; accessed 10 Jul
    2025
48. Qian, J., Chen, Q., Yue, Y., Atkinson, K., Li, G.: Injecting commonsense knowledge
    into prompt learning for zero-shot text classification. In: Proceedings of the 2023
    15th International Conference on Machine Learning and Computing, ICMLC ’23, p.
    427–432. Association for Computing Machinery, New York, NY, USA (2023). DOI
    10.1145/3587716.3587787. URL https://doi.org/10.1145/3587716.3587787
49. Quan, Z., Chen, Z.: Human–computer pragmatics trialled: some (im) polite interactions
    with chatgpt 4.0 and the ensuing implications. Interactive Learning Environments 33(2),
    1020–1039 (2025)
50. Rasheed, Z., Waseem, M., Kemell, K.K., Ahmad, A., Sami, M.A., Rasku, J., Systä, K.,
    Abrahamsson, P.: Large language models for code generation: The practitioners perspec-
    tive. arXiv preprint arXiv:2501.16998 (2025)
51. Rasool, S.F., Wang, M., Tang, M., Saeed, A., Iqbal, J.: How toxic workplace environment
    effects the employee engagement: The mediating role of organizational support and em-
    ployee wellbeing. International journal of environmental research and public health 18(5),
    2294 (2021)
52. Salvi, F., Ribeiro, M.H., Gallotti, R., West, R.: On the conversational persuasiveness of
    large language models: A randomized controlled trial. arXiv preprint arXiv:2403.14380
    (2024)
53. Schmidt, D.C., Spencer-Smith, J., Fu, Q., White, J.: Cataloging prompt patterns to
    enhance the discipline of prompt engineering. URL: https://www. dre. vanderbilt.
    edu/schmidt/PDF/ADA_Europe_Position_Paper. pdf [accessed 2023-09-25] (2023)
54. Scholak, T., Schucher, N., Bahdanau, D.: Picard: Parsing incrementally for constrained
    auto-regressive decoding from language models. arXiv preprint arXiv:2109.05093 (2021)
55. Schulhoff, S., Ilie, M., Balepur, N., Kahadze, K., Liu, A., Si, C., Li, Y., Gupta, A., Han,
    H., Schulhoff, S., et al.: The prompt report: A systematic survey of prompting techniques.
    arXiv preprint arXiv:2406.06608 5 (2024)
56. Shin, J., Tang, C., Mohati, T., Nayebi, M., Wang, S., Hemmati, H.: Prompt engineering
    or fine tuning: An empirical assessment of large language models in automated software
    engineering tasks. arXiv preprint arXiv:2310.10508 (2023)
57. Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., Yao, S.: Reflexion: Language agents
    with verbal reinforcement learning. Advances in Neural Information Processing Systems
    36, 8634–8652 (2023)
36                                                                      Alex Deaconu*     et al.


58. Sommerville, I.: Software engineering. 10th, vol. 10. Addison-Wesley (2015)
59. Strauss, A., Corbin, J.: Basics of qualitative research techniques. Sage Publications, Inc.,
    Thousand Oaks, CA (1998). Print ISBN 9780803959392, eBook ISBN 9780585383323
60. Taherkhani, H., Sepindband, M., Pham, H.V., Wang, S., Hemmati, H.: Automated prompt
    engineering for cost-effective code generation using evolutionary algorithm (2025). URL
    https://arxiv.org/abs/2408.11198
61. Tom, E., Aurum, A., Vidgen, R.: An exploration of technical debt. Journal of Systems
    and Software 86(6), 1498–1516 (2013)
62. Tony, C., Ferreyra, N.E.D., Mutas, M., Dhiff, S., Scandariato, R.: Prompting techniques
    for secure code generation: A systematic investigation. arXiv preprint arXiv:2407.07064
    (2024)
63. Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., Chowdhery, A., Zhou, D.:
    Self-consistency improves chain of thought reasoning in language models. arXiv preprint
    arXiv:2203.11171 (2022)
64. Wang, Z., Zhang, Z.: Framing effects in independent-agent large language models: A cross-
    family behavioral analysis (2026). URL https://arxiv.org/abs/2603.19282
65. Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., Le, Q.V., Zhou, D.,
    et al.: Chain-of-thought prompting elicits reasoning in large language models. Advances
    in neural information processing systems 35, 24824–24837 (2022)
66. White, J., Fu, Q., Hays, S., Sandborn, M., Olea, C., Gilbert, H., Elnashar, A., Spencer-
    Smith, J., Schmidt, D.C.: A prompt pattern catalog to enhance prompt engineering with
    chatgpt. arXiv preprint arXiv:2302.11382 (2023)
67. Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B., Gao, C., Huang, C., Lv,
    C., et al.: Qwen3 technical report. arXiv preprint arXiv:2505.09388 (2025)
68. Yin, Z., Wang, H., Horio, K., Kawahara, D., Sekine, S.: Should we respect llms? a cross-
    lingual study on the influence of prompt politeness on llm performance. In: Proceedings of
    the Second Workshop on Social Influence in Conversations (SICon 2024), pp. 9–35 (2024)
69. Yukl, G., Chavez, C., Seifert, C.F.: Assessing the construct validity and utility of two
    new influence tactics. Journal of Organizational Behavior: The International Journal
    of Industrial, Occupational and Organizational Psychology and Behavior 26(6), 705–725
    (2005)
70. Yukl, G., Falbe, C.M.: Influence tactics and objectives in upward, downward, and lateral
    influence attempts. Journal of applied psychology 75(2), 132 (1990)
71. Yukl, G., Seifert, C.F.: Preliminary validation research on the extended version of the
    influence behavior questionnaire. In: Toronto, paper presented at the Society for Industrial
    and Organizational Psychology annual conference (2002)
72. Yukl, G., Seifert, C.F., Chavez, C.: Validation of the extended influence behavior ques-
    tionnaire. The Leadership Quarterly 19(5), 609–621 (2008)
73. Zhang, L., Singhal, A., Zou, Q., Sun, X., Liu, P., Lin, H.Y.: Can ai fix buggy code?
    exploring the use of large language models in automated program repair. Computer 58(07),
    122–128 (2025)
74. Zhang, Q., Fang, C., Gu, S., Shang, Y., Chen, Z., Xiao, L.: Large language models for unit
    testing: A systematic literature review. arXiv preprint arXiv:2506.15227 (2025)
75. Zhang, Z., Zhang, A., Li, M., Smola, A.: Automatic chain of thought prompting in large
    language models. arXiv preprint arXiv:2210.03493 (2022)
76. Zheng, M., Pei, J., Jurgens, D.: Is" a helpful assistant" the best role for large lan-
    guage models? a systematic evaluation of social roles in system prompts. arXiv preprint
    arXiv:2311.10054 8 (2023)
77. Zhong, L., Wang, Z.: Can llm replace stack overflow? a study on robustness and reliability
    of large language model code generation. Proceedings of the AAAI Conference on Artificial
    Intelligence 38, 21841–21849 (2024). DOI 10.1609/aaai.v38i19.30185. URL https://ojs.
    aaai.org/index.php/AAAI/article/view/30185
78. Zhong, L., Wang, Z., Shang, J.: Debug like a human: A large language model debugger
    via verifying runtime execution step-by-step. arXiv preprint arXiv:2402.16906 (2024)
79. Zhong, S., Zou, Y., Adams, B.: Developer-llm conversations: An empirical study of inter-
    actions and generated code quality (2025). URL https://arxiv.org/abs/2509.10402
80. Zhou, A., Yan, K., Shlapentokh-Rothman, M., Wang, H., Wang, Y.X.: Language agent
    tree search unifies reasoning acting and planning in language models. arXiv preprint
    arXiv:2310.04406 (2023)
81. Zhou, Y., Muresanu, A.I., Han, Z., Paster, K., Pitis, S., Chan, H., Ba, J.: Large language
    models are human-level prompt engineers (2023). URL https://arxiv.org/abs/2211.01910
82. Zhuo, J., Zhang, S., Fang, X., Duan, H., Lin, D., Chen, K.: Prosa: Assessing and under-
    standing the prompt sensitivity of llms (2024). URL https://arxiv.org/abs/2410.12405
Do Influence Tactics Matter?                                                37


Authors and Affiliations

Alex Deaconu . Anubhav Gupta . Manaal Basha . Nicholas Haydu . Gema Rodríguez-
Pérez

Alex Deaconu
University of British Columbia, Kelowna, BC, Canada
alexdea@student.ubc.ca

Anubhav Gupta
University of British Columbia, Kelowna, BC, Canada
anubhav.gupta@ubc.ca

Manaal Basha
University of British Columbia, Kelowna, BC, Canada
manaals@student.ubc.ca

Nicholas Haydu
University of British Columbia, Kelowna, BC, Canada
nich@student.ubc.ca

Gema Rodríguez-Pérez
University of British Columbia, Kelowna, BC, Canada
gema.rodriguezperez@ubc.ca

