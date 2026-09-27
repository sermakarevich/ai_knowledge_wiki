> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Code Metrics Computation (Experiment Setup)
**In one sentence:** The study evaluates refactoring quality with code metrics for complexity, cohesion, coupling, and modularity, extracted with the Understand static-analysis tool and described in Table 1.
## Key points
- Code metrics are used as proxies for quality attributes such as maintainability and complexity [31].
- The collected metrics cover four quality attributes: complexity, cohesion, coupling, and modularity.
- Modularity metrics assess how far the system is divided into independent components, aiding maintenance and testing.
- Coupling metrics measure inter-class interdependence, where lower coupling is preferred for modularity and flexibility.
- Cohesion metrics measure how closely related a class's responsibilities are, with higher cohesion linked to clarity and design quality [35].
- Metrics are extracted with the Understand tool [36], a static code analysis tool.
- Table 1 lists each metric with its description, quality attribute, and rationale for inclusion (e.g., Avg/Max/Sum Cyclomatic for complexity, Percent Lack of Cohesion variants for cohesion).
---
## 2.2.3 Code Metrics Computation
Code metrics "provide valuable insights into the quality of the code, such as maintainability, and complexity [31]." The authors "collect code metrics that are used to evaluate complexity, cohesion, coupling, and modularity," with "description of the collected code metrics ... listed in Table 1."
- "Modularity metrics help assess the degree to which the system is divided into independent components, which promotes ease of maintenance and testing."
- "Coupling metrics indicate the degree of interdependence between classes, where lower coupling is preferred for better modularity and flexibility."
- "Cohesion metrics measure how closely related the responsibilities of a class are, with higher cohesion typically leading to improved code clarity and design quality [35]."
- Extraction: "We use the Understand tool [36], which is a static code analysis tool to extract code metrics."

## Table 1 — Description of Metrics Used in the Study [37]
| Metric | Description | Quality attribute | Rationale for inclusion |
|---|---|---|---|
| Count Class Coupled | Number of other classes coupled to. | Coupling | Helps identify tightly coupled classes, indicating potential areas for refactoring to reduce complexity. |
| Count Class Coupled Modified | Number of other non-standard classes coupled to. | Coupling | Focuses on the complexity introduced or modified during changes, relevant for assessing refactoring impact. |
| Count Class Derived | Number of immediate subclasses. | Modularity | High values may indicate a deep inheritance hierarchy, affecting maintainability and ease of modification. |
| Count Decl Class Variable | The number of class-level variables declared in a class. | Modularity | A large number of class variables can reduce cohesion and increase the potential for errors. |
| Count Decl Instance Variable | The number of instance variables declared in a class. | Modularity | High instance variable counts may signal a class doing too much, reducing its maintainability. |
| Percent Lack of Cohesion | The percentage of methods in a class that do not share instance variables. | Cohesion | Indicates the degree of cohesion in a class, with higher values suggesting poor design and low cohesion. |
| Percent Lack of Cohesion Modified | A variation of PercentLackOfCohesion, modified for accessor methods. | Cohesion | Assesses the impact of changes on class cohesion, useful for understanding the effects of refactoring. |
| Avg Cyclomatic | The average cyclomatic complexity for all nested functions or methods. | Complexity | Provides an overall view of the code's complexity, helping to identify areas that may need simplification. |
| Cyclomatic | The McCabe cyclomatic complexity of a single method or function. | Complexity | Directly measures the complexity of a method, indicating potential difficulties in testing and understanding. |
| Max Cyclomatic | The maximum cyclomatic complexity of any method in a class or project. | Complexity | Highlights the most complex methods, which could be refactoring targets to improve maintainability. |
| Sum Cyclomatic | The total cyclomatic complexity of all methods in a class or project. | Complexity | Summarizes the overall complexity, aiding in assessing the overall maintainability and testability of the codebase. |

**Covers:** Section 2.2.3 Code Metrics Computation + Table 1 (chunk 03/12)
