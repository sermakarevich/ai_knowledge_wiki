> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# SPACE Framework Mapping of Productivity (RQ3)
**In one sentence:** Framed by the SPACE framework, 90% (35/39) of studies take a multidimensional view of productivity but only 15% (6/39) cover four or more dimensions, with Satisfaction (77%), Performance (64%), and Efficiency (59%) dominating while Activity (31%) and Communication (26%) remain underexplored.
## Key points
- 90% (35/39) of studies adopt a multidimensional perspective and only 4 are uni-dimensional, but just 44% (17/39) examine three or more SPACE dimensions and 15% (6/39) address four or more.
- The most co-occurring dimensions are Satisfaction, Performance, and Efficiency, with the single most frequent combination being Satisfaction-Performance-Efficiency (5/39).
- Satisfaction is the most studied dimension at 77% (30/39), captured mainly through self-reported instruments, with developer experience as the dominant sub-dimension, cognitive load second (NASA-TLX or custom surveys), self-efficacy via validated and custom tools, and well-being examined by zero studies.
- Performance (64%, 25/39) centers on final outcomes, mostly the quality sub-dimension (unit tests, functional correctness, code smells), while the impact sub-dimension appears in only 3 studies via business metrics such as cost savings, product quality improvements, and delivery speed.
- Efficiency (59%, 23/39) is studied via three sub-dimensions — temporal efficiency (task-completion metrics or perceptions), automation (offloading boilerplate [58, 60]), and interruptions and flow (reduced interruptions versus new LLM-introduced distractions).
- Activity (31%, 12/39) is measured as counts and frequencies such as acceptance rate and tasks completed, with Ziegler et al. [65] using finer granularity (acceptance rate, suggestions shown rate, completions changed or unchanged).
- Communication (26%, 10/39) is the least investigated dimension: 7/10 studies examine human-LLM collaboration (interaction patterns) and only 3/10 examine human-human collaboration with LLM in the loop, leaving team dynamics and over-reliance effects (Section 6.2.5) as a gap.
---
## Multidimensionality and overlap (Fig. 8)
90% (35 out of 39) adopt a multidimensional perspective; only four studies are uni-dimensional. Only 44% (17/39) examine three or more SPACE dimensions, and just 15% (6/39) address four or more dimensions. The most co-occurring combinations involve Satisfaction, Performance, and Efficiency; the most frequent combination is Satisfaction-Performance-Efficiency (5 out of 39). Figure 8 shows the distribution of investigated SPACE dimensions and their overlap (Satisfaction 30, Performance 25, Activity 12, Communication 10, Efficiency 23).
**Covers:** Fig. 8; multidimensional vs uni-dimensional counts

## Satisfaction (77%, 30/39)
Satisfaction captures developers' feelings about work with LLM-assistants, mainly via self-reported instruments. The analysis reports five fine-grained sub-dimensions, naming developer experience, self-efficacy, trust, and cognitive load (Fig. 7 lists Self-Efficacy, Developer Experience, Cognitive Load, Trust, plus Quality/Impact under Performance and Activity/Communication/Efficiency sub-dimensions). Developer experience is the main focus: developers' perceptions, feelings, and values regarding interactions with LLM-assistants [46], perceived importance, ease of use (e.g., developers' feedback, Technology Acceptance Model (TAM)). Cognitive load is second, assessed via NASA-TLX or custom surveys. Self-efficacy — belief in one's ability to complete tasks — uses validated and custom-designed tools. Well-being is examined by none of the empirical studies, aligning with [105] on overlooked well-being/mental health in SE research.
**Covers:** Satisfaction sub-dimensions; developer experience, cognitive load, self-efficacy, well-being gap

## Performance (64%, 25/39)
Performance concerns final outcomes of development activities. Most studies investigate the quality sub-dimension using passing unit tests, functional correctness, and code smells (see Quality metrics table below). The impact sub-dimension appears in only three studies and investigates final product outcomes [19]: business-related metrics including cost savings, product quality improvements, and delivery speed (see section 5.3.4).
**Covers:** Performance: quality vs impact sub-dimensions

## Quality metrics by study (Table 11)
| Metric | Primary Studies |
|---|---|
| Passing Unit Tests | [51, 57, 67, 68, 87] |
| Functional Correctness and Accuracy | [52, 59, 67, 77] |
| Code Smells | [61, 76, 86] |
| BLEU Score | [54, 59] |
| Halstead Complexity Measures | [73, 77] |
| Cyclomatic Complexity | [50, 86] |
| Translation Error Rate | [51] |
| Maintainability Index | [73] |
| Cognitive Complexity | [76] |
| Defect Density | [86] |
| Defect Rate | [76] |
| Technical Debt | [86] |
| Code Coverage | [86] |
**Covers:** Table 11 verbatim

## Efficiency (59%, 23/39)
Efficiency reflects capacity to complete tasks efficiently with minimal interruptions or time delays, minimizing unnecessary delays and optimizing flow of task handoffs [19]. Three sub-dimensions: temporal efficiency, automation, interruptions and flow. Temporal perspective dominates, measured via task completion metrics or developer perceptions. Automation: LLM-assistants offload repetitive tasks such as boilerplate code [58, 60]. Interruptions and flow: some studies highlight reduced cognitive interruptions, others note new distractions introduced by the LLM-assistant.
**Covers:** Efficiency sub-dimensions

## Activity (31%, 12/39)
One of the least explored dimensions; often paired with efficiency and performance; focuses on counts and frequency measures while performing a task [19]. Measured as counts of actions or tasks during LLM interactions (e.g., acceptance rate, number of tasks completed) [54, 55, 65, 73]. Ziegler et al. [65] measures activity at finer granularity: count of actions during Copilot interactions (acceptance rate, suggestions shown rate, completions changed or unchanged).
**Covers:** Activity measures and example

## Communication (26%, 10/39)
Least investigated dimension; focuses on how developers and teams communicate and share knowledge [19]. Majority (7 out of 10) investigate human-LLM collaboration, including interaction patterns between participants and LLM-assistants; only three (3 out of 10) examine human-human collaboration with LLM in the loop. Gap in understanding LLM-assistant effects on team communication/coordination, also highlighted by [105, 106]. Given concerns about reduced team collaboration from over-reliance (see Section 6.2.5), future studies should investigate team dynamics in LLM-assisted workflows.
**Covers:** Communication: 7/10 vs 3/10 split; team-dynamics gap

## RQ3 Summary (verbatim)
> RQ3 - Summary
> Our analysis, framed by the SPACE framework, reveals that the majority of studies (90%, 35 out of 39) adopt a multidimensional view of productivity in SE, mostly combining two or more SPACE dimensions. However, only 15% (6 out of 39) of the studies examine four or more SPACE dimensions. Satisfaction (77%, 30 out of 39) is the most frequently investigated, followed by Performance (64%, 25 out of 39) and Efficiency (59%, 23 out of 39). In contrast, Activity (31%, 12 out of 39) and Communication (26%, 10 out of 39) is the least explored dimensions.
**Covers:** RQ3-Summary box verbatim; Section 8 Discussion opening (39-study synthesis via McLuhan's Tetrad [107], practitioner takeaways, open issues) begins but belongs to chunk 11
