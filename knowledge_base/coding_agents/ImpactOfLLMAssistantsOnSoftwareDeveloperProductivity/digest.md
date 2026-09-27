> [[index|Wiki]] | [[summary|Summary]]

# The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study — Digest

## 1. [[wiki/01-introduction-and-contributions|Introduction and Contributions]]

**In one sentence:** This systematic review and mapping of 39 peer-reviewed studies (January 2014–December 2024) finds LLM-assistants mostly benefit developer productivity but carry critical risks, with code-quality effects unresolved and most studies exploratory and multi-dimensional but narrow in scope.

## Key points

- The review synthesizes 39 peer-reviewed studies published between January 2014 and December 2024 on LLM-assistants and developer productivity.
- Commonly reported gains are accelerated development, minimized code search, and automation of trivial and repetitive tasks.
- Commonly reported risks are cognitive offloading and reduced team collaboration.
- Whether LLM-assistants improve or degrade code quality remains unresolved, with contradictory outcomes contingent on context and evaluation criteria.
- 90% of studies examine at least two SPACE dimensions, but only 15% extend beyond three dimensions.
- Satisfaction, Performance, and Efficiency are the most investigated SPACE dimensions; Communication and Activity remain underexplored.
- Most studies are exploratory (59%) and methodologically diverse, but lack longitudinal and team-based evaluations.

## 2. [[wiki/02-background-developer-productivity|Background: Developer Productivity from Peopleware to SPACE]]

**In one sentence:** Software developer productivity is a complex, human-centric construct with no universal definition, historically reduced to output ratios like LOC or task time but now assessed through multidimensional frameworks (DevEx, SPACE) that the review uses to map LLM-assistant effects via four research questions and a Kitchenham-guided protocol validated on 17 control papers with 9,756 initial search hits.

## Key points

- Developer productivity has no universal definition or measurement consensus despite decades of research [24, 25, 26, 27], because diverse variables influence it [17].
- Historically it was quantified as output-to-input ratios such as lines of code (LOC) [24, 28] or task completion time [29], which fail to capture human, social, and organizational dimensions.
- DeMarco and Lister's Peopleware [22] established that the biggest obstacles to productivity are sociological and organizational, not technical, requiring management of people, environment, and culture.
- Grinter et al. [23] showed software architecture and team structure are deeply interconnected, so misalignment creates communication bottlenecks and coordination overhead that worsen with scale.
- Noda et al.'s Developer Experience (DevEx) model [31, 32] operationalizes day-to-day experience via three dimensions: feedback loops, cognitive load, and flow state.
- Forsgren et al.'s SPACE framework [19] characterizes productivity across five dimensions — Satisfaction and well-being, Performance, Activity, Communication and collaboration, Efficiency and flow — and is increasingly used in AI-assisted development studies [33–39].
- The review's overarching objective spans three dimensions: (1) methodological strategies/procedures/instruments, (2) reported benefits and risks of LLM assistance, and (3) which productivity dimensions were investigated; it is guided by RQ0–RQ3 and Kitchenham and Charters guidelines [40].

## 3. [[wiki/03-methodology-search-and-selection|Methodology: Search and Selection]]

**In one sentence:** The review selects primary studies using three inclusion and five exclusion criteria applied to a 9,756-record search across six digital libraries, filtered through PRISMA screening to 39 included studies plus snowballing.

## Key points

- Three inclusion criteria require English-language, full-text-accessible papers from 2014 or later investigating AI/LLM effects on developer productivity.
- Five exclusion criteria remove out-of-scope (EC1), out-of-focus (EC2), non-peer-reviewed or secondary publication types (EC3), short papers under four pages (EC4), and inaccessible full texts (EC5).
- Six libraries were searched (ACM, IEEE Xplore, ScienceDirect, Web of Science, Scopus, SpringerLink) with title/abstract/keyword restriction and NEAR/5 proximity operators in IEEE Xplore, Web of Science, and Scopus only.
- The search string has three AND-joined segments (AI/LLM technology, software-developer actor, productivity concept), refined over five iterations until it retrieved all 17 control papers.
- Initial search yielded 9,756 records; after removing 803 duplicates, 8,953 were screened by title and abstract and 8,725 excluded, leaving 228 for full-text review.
- Full-text screening excluded 189 papers (EC2 out-of-focus largest at 128, EC1 15, EC3 27, EC4 11, EC5 3, ~IC1 5), leaving 39 studies, plus 5 from two weeks of forward/backward snowballing (44 evaluated, 5 excluded, 39 total included).
- Screening was conservative (unclear title/abstract cases advanced to full text): first author screened all records over 47 days in Rayyan with second/last-author validation across three consensus meetings, followed by a 10-week full-text phase with consultation on unclear cases.

## 4. [[wiki/04-quality-assessment-and-publication-trends|Quality Assessment and Publication Trends]]

**In one sentence:** After scoring each study on a five-point Likert scale and excluding 5 studies below a 50% quality threshold to leave 39 primary studies, the review finds a ChatGPT-driven surge peaking in 2024 (77% of studies) synthesized via Kitchenham-guided qualitative thematic analysis.

## Key points

- Each quality criterion was graded Excellent (4), Very Good (3), Good (2), Fair (1), Poor (0), with detailed scores in the supplemental appendix.
- Studies failing a minimum 50% average-score threshold were excluded: 5 excluded, leaving a final set of 39 primary studies.
- The majority of studies were rated above 3, with full quality-assessment results in the replication package material.
- Synthesis of RQ findings took three months using qualitative synthesis consistent with Kitchenham's guidelines, with initial plus three targeted thematic iterations (RQ1 methods, RQ2 benefits/risks, RQ3 SPACE mapping).
- Only four included studies were published between 2014 and 2022; interest rose in 2022 with ChatGPT's release and peaked in 2024 with 77% of all included studies.
- Of 154 authors, 147 have one publication, 6 have two, and Igor Steinmacher has three — reflecting a new topic just building momentum.
- By venue focus, 46% are Software Engineering and Computer Science, 18% (7 of 39) Human-Computer Interaction, plus 13% Information Systems and Decision Science, 10% Human-Aspects and Socio-Economic Impact, 8% AI for Software Engineering, and 5% Software Engineering Education.
- The most evaluated tools are ChatGPT (15 studies) and GitHub Copilot (14 studies), followed by Tabnine (3), GPT-4 (3), CodeWhisperer (3), and GPT-3.5 (2), with all others used once.

## 5. [[wiki/05-study-characteristics-tools-and-strategies|Study Characteristics, Tools and Strategies (RQ0 Summary and RQ1 Start)]]

**In one sentence:** The field is almost entirely post-ChatGPT (35/39 studies), concentrated in SE/CS venues, and methodologically dominated by laboratory experiments (38%) triangulated through mixed methods with heavy reliance on self-reported data (90%).

## Key points

- 35 out of 39 primary studies (90%) were published after the release of ChatGPT in November 2022; only 4 studies (2014–2022) precede it and rely on pre-LLM paradigms.
- Authorship is fragmented: 147 out of 154 authors contributed a single publication, while only 7 authors published two or more papers.
- By venue, 18 studies appeared in Software Engineering and Computer Science venues, followed by 7 in Human-Computer Interaction venues.
- Laboratory experiments are the most common research strategy at 38% (15/39), used to isolate LLM-assistant effects on specific tasks in controlled environments.
- Field studies are second at 23% (9/39), prioritizing ecological validity by observing developers in real-world settings without researcher intervention; sample studies (large-scale surveys) account for 15% (6/39).
- Less frequent strategies: experimental simulations 13% (5/39), field experiments 5% (2/39), and judgment studies 5% (2/39, structured expert opinion via interviews/questionnaires).
- 90% of studies (35/39) leverage self-reported data (surveys, interviews); 41% (16/39) use experimental settings; 69% (27/39) adopt a mixed-method approach, most commonly user experiment paired with survey (10 studies).
- Research objectives are balanced rather than conclusive: 59% (23/39) formative (exploring/refining tools) vs 41% (16/39) summative (evaluating effectiveness/impact); analysis is 67% mixed quantitative+qualitative (26/39), 21% qualitative-only (8/39), 13% quantitative-only (5/39).

## 6. [[wiki/06-measurement-instruments-and-data-sources|Measurement Instruments and Data Sources (RQ1)]]

**In one sentence:** Self-reported methods (mostly author-designed surveys/interviews) predominate across the 39 empirical studies while only 15 use validated instruments and behavioral/performance metrics cluster in high-control experiments, with time-to-completion the top metric (31%), acceptance rate a common but cautioned-against metric, NASA-TLX cognitive-load findings mixed, and econometric studies reporting 24% throughput / 26% quality gains alongside a throughput–quality trade-off (r = −0.45).

## Key points

- Self-reported methods predominate and are often designed by study authors to capture user experience, perceived productivity, trust, or ease of use (e.g., post-task surveys, open-ended feedback).
- Only 15 out of 39 empirical studies incorporate validated instruments, including the SPACE framework, NASA-TLX for mental workload, TAM for technology acceptance, self-efficacy questionnaires, or emotional affect questionnaire.
- Behavioral and performance metrics focus on quantifiable outcomes — time to completion, acceptance rate of AI-generated suggestions, code quality metrics, and interaction patterns — and are mostly associated with high-control designs such as laboratory experiments, field experiments, or experimental simulation.
- Time to completion is the most frequently used performance metric at 31% (12 out of 39), mostly measured in laboratory experiments under controlled conditions, plus one field study comparing throughput/cycle time before/after Copilot, one experimental simulation using "person/days," and one study measuring issue-report-to-resolution time.
- Acceptance rate of LLM suggestions is a commonly used behavioral metric, with a Meta study of Code Compose counting accepted suggestions and proportion of LLM-authored code, while a GitHub study finds strong correlation between accepted-suggestion frequency and perceived productivity but cautions against using the metric in isolation.
- Six studies (6 out of 39) measure cognitive workload with NASA-TLX (mental demand, physical demand, temporal demand, performance, effort, frustration) in comparative experimental settings, with mixed findings: improvements in some, neutral effects in others, and one study reporting significantly worse frustration.
- Econometric studies using TCQ and RBV frameworks report that coding shows the highest GenAI gains (24% throughput, 26% quality on average across 1,000+ large firms, 2021–2023), while a survey of 70 large global companies confirms throughput gains but finds increased throughput negatively correlated with code quality (r = −0.45).
- Field studies and sample studies still employ diverse instruments but primarily rely on self-reported methods such as surveys, interviews, and users' open-ended feedback, whereas time-to-completion and code-quality metrics are mainly associated with laboratory experiments.

## 7. [[wiki/07-benefits-task-acceleration-and-automation|Benefits: Task Acceleration and Automation]]

**In one sentence:** LLM-assistants improve developer productivity by accelerating development, minimizing online code search, automating trivial/repetitive tasks, reducing task-initiation overhead, and supporting knowledge acquisition and code-adjacent work.

## Key points

- Self-reported acceleration is widespread: "accelerate coding" was the second most frequent theme in open-ended feedback on a code-completion tool (14 responses, 20%), and 52% of 90 developers in a 10-week field study perceived productivity boosts from GitHub Copilot, with ratings increasing week-over-week.
- Quantitative studies report reduced task completion time, including a pension-plan website SDLC case study where effort fell from 75 person-days to 22 person-days (71% productivity gain), and controlled experiments reporting 21%–45% efficiency gains depending on task type.
- A matched analysis of 608 GitHub project teams found human-bot teams showed significantly higher productivity across all team sizes based on repository activity metrics.
- Minimizing online code search is the most frequently reported benefit: developers prefer LLM-assistants over Stack Overflow and search engines (Google, Bing), gaining flow maintenance ("stay in the flow"), faster syntax recall, unfamiliar-API discovery, and an alternative when search fails — though one PyCharm-plugin study [50] found no significant time/correctness difference and one 44-participant study [67] found Stack Overflow better for debugging.
- Automation centers on repetitive coding, boilerplate generation, and reduced keystrokes/typing effort, with unit-test generation and CI/CD automation as key use cases; a Delphi study with 14 industry professionals anticipates automating all routine tasks to free time for complex work.
- Task-initiation overhead is reduced at early project stages via lower entry barriers, proof-of-concept building, initial code scaffolding, and planning/initial structuring of ideas.
- Knowledge acquisition is both a direct and indirect benefit: 75% of respondents found assistants helpful for learning, 69% of participants in a code-translation study reported enhanced learning (e.g., new aspects of Python), and assistants lower the entry barrier to new frameworks.

## 8. [[wiki/08-benefits-evidence-and-code-quality|Benefits Evidence and Code Quality]]

**In one sentence:** Further evidence shows LLM-assistants support learning, code-adjacent tasks, task initiation, troubleshooting, and measurably improve code quality in several studies, while introducing risks around unmet requirements and over-reliance.

## Key points

- Expert consultation is the most common ChatGPT use case at 62% of analyzed conversations, and 75% of survey respondents call ChatGPT a helpful learning tool [56].
- LLM-assistants lower the barrier to learning new frameworks and 14 experts identify enhancing learning and teaching as the most probable future scenario [64, 83, 80].
- For task initiation, 55% of participants (17 out of 31) in a controlled experiment used ChatGPT primarily to generate initial code scaffolding before shifting to independent refinement [57].
- Ten projects built with LLM-assistants show an 18% improvement across six code-quality metrics (including cyclomatic complexity, coverage, smells, technical debt, defect density) versus ten without [86].
- A five-team Copilot case study finds code smells reduced in three of five teams and defect counts decreased in all five teams after adoption [76].
- Code translation with TransCoder support yields a 51% reduction in error rate versus the control group, though ChatGPT beats Stack Overflow on algorithmic/library tasks but loses on debugging tasks [51, 67].
- Benchmarked code-generation correctness ranges from 31.1% (Amazon CodeWhisperer) to 65.2% (ChatGPT), and 50% of participants cite missing or misunderstood requirement context with ChatGPT 3.5 [78, 68].
- Over-reliance risks include eroded critical thinking in novices/students and observed automation complacency (all three Parasuraman–Manzey characteristics) in a programming exam with Google Bard [61, 69, 88, 72].

## 9. [[wiki/09-risks-flow-disruption-and-over-reliance|Disrupt the Flow — LLM-Assistants as a Source of Interruption]]

**In one sentence:** Studies find that LLM-assistants can disrupt developer flow through unwanted suggestions, interface switching, verbose answers, and competing tools, imposing temporal and cognitive costs with developers spending an average of 51.5% of coding-session time in LLM-interaction states.

## Key points

- LLM-assistants can disrupt developer flow, with interruptions attributed to unwanted suggestions [82], interface switching, and verbose answers [73].
- In a laboratory experiment [73], some professional developers find Copilot distracting because the speed of code suggestions does not allow sufficient time for code understanding.
- Distraction also occurs when LLM-assistants work in tandem and compete to display suggestions [54].
- Authors of [71] model user behavior with tools such as Copilot and find developers spend an average of 51.5% of coding-session time in LLM interaction states.
- Those LLM interaction states comprise verifying suggestions, prompt crafting, and deferring thought.
- In open-source contexts, human-bot teams may experience notification fatigue from increased automated activity [53].
- Together, these findings highlight the temporal and cognitive costs that LLM-assistants may introduce.

## 10. [[wiki/10-space-framework-mapping|SPACE Framework Mapping of Productivity (RQ3)]]

**In one sentence:** Framed by the SPACE framework, 90% (35/39) of studies take a multidimensional view of productivity but only 15% (6/39) cover four or more dimensions, with Satisfaction (77%), Performance (64%), and Efficiency (59%) dominating while Activity (31%) and Communication (26%) remain underexplored.

## Key points

- 90% (35/39) of studies adopt a multidimensional perspective and only 4 are uni-dimensional, but just 44% (17/39) examine three or more SPACE dimensions and 15% (6/39) address four or more.
- The most co-occurring dimensions are Satisfaction, Performance, and Efficiency, with the single most frequent combination being Satisfaction-Performance-Efficiency (5/39).
- Satisfaction is the most studied dimension at 77% (30/39), captured mainly through self-reported instruments, with developer experience as the dominant sub-dimension, cognitive load second (NASA-TLX or custom surveys), self-efficacy via validated and custom tools, and well-being examined by zero studies.
- Performance (64%, 25/39) centers on final outcomes, mostly the quality sub-dimension (unit tests, functional correctness, code smells), while the impact sub-dimension appears in only 3 studies via business metrics such as cost savings, product quality improvements, and delivery speed.
- Efficiency (59%, 23/39) is studied via three sub-dimensions — temporal efficiency (task-completion metrics or perceptions), automation (offloading boilerplate [58, 60]), and interruptions and flow (reduced interruptions versus new LLM-introduced distractions).
- Activity (31%, 12/39) is measured as counts and frequencies such as acceptance rate and tasks completed, with Ziegler et al. [65] using finer granularity (acceptance rate, suggestions shown rate, completions changed or unchanged).
- Communication (26%, 10/39) is the least investigated dimension: 7/10 studies examine human-LLM collaboration (interaction patterns) and only 3/10 examine human-human collaboration with LLM in the loop, leaving team dynamics and over-reliance effects (Section 6.2.5) as a gap.

## 11. [[wiki/11-synthesis-and-socio-technical-implications|In-depth synthesis across studies using the McLuhan Tetrad]]

**In one sentence:** The authors use McLuhan's Tetrad to argue that LLM-assistants enhance speed on well-scoped tasks, obsolesce traditional search/Q&A, retrieve neglected practices like documentation and legacy work, but reverse into over-reliance, lost judgment, and weakened collaboration when pushed to extremes.

## Key points

- Traditional productivity models including SPACE clarify measurement but do not capture how LLM-assistants redefine development practices, decision-making, and team dynamics across the software life cycle [56, 76, 77].
- McLuhan's Tetrad complements SPACE by shifting from measurement to interpretation, asking four questions: what the medium enhances, obsolesces, retrieves, and reverses when pushed to the extreme [107].
- Enhancement is task-contingent: gains concentrate in accelerating development, lowering entry barriers for complex tasks, supporting knowledge acquisition, debugging/troubleshooting, boilerplate generation, syntax recall, scaffolding, and exploratory prototyping.
- Reversal arises from uncritical use: excessive trust causes cognitive offloading and automation complacency, shifting developers from code production to reviewing output, eroding autonomy [106], reflective engagement, and code quality when output is accepted without validation.
- Obsolescence displaces traditional online search for syntax/libraries and Q&A platforms such as Stack Overflow, which risks diminishing independent verification, evaluation of competing solutions, and search/validation skills needed when LLM outputs are incorrect or incomplete.
- Retrieval revives previously diminished practices: code documentation, requirements elicitation with frequent client communication [108], and legacy-system work on platforms such as COBOL or Uniface [80, 84], though legacy support is currently limited [63].
- Three overarching lessons: (1) gains are task-contingent and strongest for well-scoped repetitive activities; (2) uncritical reliance creates diminishing returns via validation overhead and eroded reflective practice; (3) LLM-assistants reshape rather than replace expertise toward evaluation, judgment, and coordination.

## 12. [[wiki/12-recommendations-for-practitioners|Recommendations for Practitioners: Calibrated Trust and Workflow Practices]]

**In one sentence:** Developers and organizations should cultivate calibrated, critical trust in LLM-assistants — treating outputs as drafts requiring validation, reallocating effort to review and workflow adaptation, and governing adoption with quality and ethical safeguards — to gain productivity without sacrificing quality, autonomy, collaboration, or skills.

## Key points

- Recommendation 1 prescribes four operations: treat all LLM-generated code as preliminary output requiring testing and review; cross-reference suggestions against official docs for unfamiliar APIs; acknowledge missing project context and hallucination risk; and code unassisted periodically to preserve competencies.
- The developer role shifts from coder to reviewer: Mozannar et al. [71] report participants spend over 50% of their time in evaluation activities (prompting, reviewing suggestions, editing completions), and Weisz et al. [51] find code translation becomes a reviewing rather than writing task.
- Time saved in generation can be lost in evaluation and refinement, especially for complex tasks, producing diminishing productivity returns if unmanaged [75]; this mirrors the "ironies of automation" [109] where automation shifts users from production to evaluation.
- New central skills are prompt engineering, critical evaluation of AI-generated code, and contextual judgment, plus awareness of automation bias and complacency; training should emphasize verification, debugging, reflective AI use, and collaboration preserving knowledge sharing.
- Recommendation 3 (workflow): customize tool settings to control suggestion frequency and interruptions (Copilot-style disruptions reported in [54, 73, 82]); preserve pair programming, code reviews, and architectural discussion; set norms for colleague-vs-LLM consultation; document LLM-assisted decisions in commits/design records.
- Organizational evidence shows a moderate negative correlation (r = −0.45) between throughput and code quality (Section 6.2.4); Recommendation 4 advises readiness assessment, task-appropriateness policies, enhanced review for high-risk modules, collaboration monitoring, and periodic governance revisits.
- Recommendation 5 (ethics): mandate disclosure of AI-assisted contributions with ownership/review/traceability frameworks; integrate ethical review and bias testing into QA; favor transparent, traceable tools, given the black-box transparency deficit (no sources/references, hindering validation [58, 63]).

## 13. [[wiki/13-recommendations-for-researchers|Recommendations for Researchers: Shared Measures and Future Directions]]

**In one sentence:** Researchers should adopt shared, validated evaluation frameworks, extend multidimensional SPACE coverage (especially Communication), account for confounders like expertise and task complexity, and run longitudinal, field, and team-based studies that triangulate quantitative and qualitative evidence.

## Key points

- Recommendation 1 calls for shared evaluation frameworks and validated instruments to enable comparability, plus longitudinal, field, and team-based studies of long-term outcomes.
- Future work should use standardized cognitive-load measures to reconcile inconsistent findings, and track productivity, code quality, and skill development over extended periods rather than single sessions.
- 90% of studies examine at least two SPACE dimensions (a positive multidimensional shift), but only 15% extend beyond three dimensions, leaving room for more complete evaluation.
- Satisfaction, Performance, and Efficiency are the most investigated SPACE dimensions, while Communication — especially human-human collaboration — remains the least investigated.
- Novices show higher immediate gains but greater over-reliance and long-term skill erosion, while experts achieve sustained efficiency through selective and critical use; LLMs do well on isolated well-defined tasks but validation overhead offsets speed gains in complex context-rich projects.
- Recommendation 3 requires modelling expertise, task complexity, and domain context as covariates, stratifying by novice versus expert, operationalizing complexity, documenting organizational context, and replicating across populations, tools, and contexts.
- The primary evidence base is 59% formative and 38% laboratory experiments (strong internal but limited ecological validity), lacks standardized metrics for code quality and cognitive load, and is temporally concentrated with 77% of included studies published in 2024.

## 14. [[wiki/14-conclusion-threats-and-validity|Conclusion: Benefits, Risks, and Research Gaps]]

**In one sentence:** Synthesizing 39 peer-reviewed studies, the authors conclude that LLM-assistants accelerate development and lower task-initiation overhead but carry risks of over-reliance, flow disruption, and reduced collaboration, with mixed code-quality effects and major gaps in multi-dimensional and team-level evidence.

## Key points

- The review systematically identifies and analyzes 39 peer-reviewed studies by methodological strategy, evaluation practice, and productivity dimension covered.
- Reported benefits include reduced task-initiation overhead, accelerated development, and support for code-adjacent tasks.
- Reported risks include over-reliance on LLM-assistants especially affecting novice programmers, disruptions to developer flow, and reduced team communication or collaboration.
- Code-quality outcomes are mixed, with studies reporting both improvements and degradations depending on context, task design, and evaluation criteria.
- Most studies (90%) consider multiple productivity dimensions, but relatively few extend beyond three dimensions.
- Communication and, more specifically, human-human collaboration remain underexplored productivity dimensions.
- The authors call for team-based studies capturing the dynamic and socio-technical nature of software development as LLM-assistants embed deeper into everyday workflows.
- Transparency is supported by a publicly available replication package [20], and the work was funded by NSERC Discovery Grant RGPIN-2024-06511.

## 15. [[wiki/15-references-part-1|References Part 1 — Page et al. [47] Onward]]

**In one sentence:** This chunk lists bibliography entries [47] through [81], anchored by the PRISMA 2020 reporting guideline and spanning systematic-review methods, code generation/translation, pair programming, and 2024–2025 empirical studies of LLM assistants.

## Key points

- The chunk contains 35 numbered references, [47] through [81] inclusive, spread across manuscript pages 40–41.
- The anchor entry [47] is Matthew J Page et al., "The PRISMA 2020 statement: an updated guideline for reporting systematic reviews," BMJ 372 (2021), doi 10.1136/bmj.n71.
- By year, the entries break down as 2016 × 1, 2021 × 3, 2022 × 3, 2023 × 3, 2024 × 23, and 2025 × 2, showing heavy concentration in 2024.
- Method entries include systematic-review guidance ([47] PRISMA 2020; [48] Lenarduzzi et al. 2021 on technical debt prioritization; [49] Garousi and Mäntylä 2016 on reviews in software testing).
- Code-generation/translation entries include [50] Xu, Vasilescu, and Neubig (TOSEM 31.2, 2022, pp. 1–47) and [51] Weisz et al. (IUI 2022, pp. 369–391).
- Human–AI collaboration entries include [52] Kuttal et al. (CHI 2021, pp. 1–20) on substituting a human with an agent in pair programming and [53] Newton et al. (Topics in Cognitive Science 16.3, 2024, pp. 450–484).
- The tail of the chunk ([64] Al Haque et al. 2025; [79] Ngwenyama, Kanita, and Rowe 2025) extends coverage into 2025 publications.

## 16. [[wiki/16-references-part-2|References Part 2 — Mendes et al. [82] Onward]]

**In one sentence:** This chunk is the paper's closing bibliography entries [82]–[109] plus the manuscript submission footer, listing cited works on AI assistants, productivity, usability, and automation complacency without presenting new findings.

## Key points

- The chunk contains only bibliography entries [82] through [109], with no results, analysis, or argument beyond citation metadata.
- Entries [82]–[88] cite 2024 primary studies on AI code assistants, including Mendes et al. (CHASE 2024, pp. 144–152), Mbizo et al., Pinto et al., Coutinho et al., Chen (TiMi studio), Gardella et al., and Frankford et al.
- Entries [89]–[102] cite methodological and theoretical foundations, including Stol and Fitzgerald (TOSEM 27.3, 2018), Glass et al. (2002), Hartson et al. (2001), Hart and Staveland NASA-TLX (1988), TAM, computer self-efficacy, and Parasuraman and Manzey on automation complacency (2010).
- Entries [103]–[109] cite reports and recent works, including the Google DevOps Research and Assessment 2022 State of DevOps Report, Sikand et al. (2024), Qiu et al. (TOSEM 34.5, 2025), Abrahão et al. (TOSEM 34.5, 2025), McLuhan (1977), and Simkute et al. (2025, pp. 2898–2919).
- Barke, James, and Polikarpova "Grounded Copilot" (Proc. ACM Programming Languages 7.OOPSLA1, 2023, pp. 85–111) is listed as entry [101].
- The chunk ends with the manuscript footer lines "Received 2 July 2025; revised 4 Feb 2026; accepted 17 March 2026" and "Manuscript submitted to ACM".

## The argument in five moves

1. Developer productivity is a multidimensional, human-centric construct without a single valid metric, so the review frames LLM-assistant effects through SPACE and assembles a Kitchenham-guided corpus of 39 peer-reviewed studies selected from 9,756 records with quality screening.
2. The evidence base is new, narrow, and method-bound — post-ChatGPT, exploratory, lab-heavy, and reliant on self-reported and incomparable instruments — which limits what can be claimed about lasting or team-level productivity.
3. Within those bounds, LLM-assistants reliably accelerate well-scoped work by speeding coding, displacing search, automating boilerplate, scaffolding starts, and aiding learning, debugging, and code-adjacent tasks, with several studies showing quality gains.
4. The same assistance reverses at the extreme into unmet requirements, mixed quality, flow disruption, cognitive offloading, and weakened human-human collaboration, meaning time saved in generation is often repaid in validation, interruption, and skill costs.
5. The review therefore prescribes calibrated trust, reviewer-oriented skills, workflow and governance adaptation for practitioners, and shared measures plus longitudinal, field, and communication-centered designs for researchers.
