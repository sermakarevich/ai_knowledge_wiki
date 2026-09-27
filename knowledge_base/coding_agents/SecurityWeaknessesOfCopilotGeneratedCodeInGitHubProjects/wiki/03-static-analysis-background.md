> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Static Analysis Background
**In one sentence:** Static analysis is a low-cost, high-coverage but unsound/imprecise way to detect vulnerabilities without execution, so the study combines general-purpose CodeQL with language-specific tools (Cppcheck, Bandit) to cover multiple languages and perspectives.
## Key points
- Vulnerability detection uses static, dynamic, or hybrid analysis, and detecting vulnerabilities is critical to improve security and ensure quality.
- Static analysis offers greater coverage and analyzes programs without executing them, but it can be unsound and imprecise.
- Dynamic analysis is more sound and precise because it captures actual runtime behaviour, but it can be incomplete and lacks coverage.
- Static analysis tools are widely used for security analysis due to ease of use and low cost compared with dynamic analysis.
- Common tools listed via OWASP and Snyk include CodeQL (general-purpose automatic analysis), FindBugs/SpotBugs for Java, ESLint for JavaScript, Bandit for Python, and GoSec for Go.
- Prior work examples: Kaur et al. compared tools on C/C++ and Java; Tomasdottir et al. studied ESLint; Pearce et al. used CodeQL on generated Python and C++; Siddiq et al. used Bandit on generated Python.
- Using multiple tools discovers weaknesses from different perspectives and levels, avoiding omissions and improving accuracy.
- This study first scanned collected snippets with CodeQL (open-source; supports Java, JavaScript, C++, C#, Python; finds weaknesses based on known weaknesses/rules), then supplemented with language-tailored tools (Cppcheck and Bandit).
---
## Static vs dynamic analysis
**Covers:** pp. 6–7, Section 2.4 paras 1–2

| Property | Static analysis | Dynamic analysis |
|---|---|---|
| Execution needed | No — analyzes programs without executing them | Yes — captures actual program behaviour at runtime |
| Coverage | Greater coverage | Incomplete, lacks coverage |
| Soundness/precision | Can be unsound and imprecise | More sound and precise |
| Cost/ease | Ease of use and low cost; widely used for security analysis | Higher cost than static (implied by comparison) |

Verbatim: "Static analysis offers greater coverage and allows users to analyze programs without the need to execute them, but it can be unsound and imprecise."
Verbatim: "dynamic analysis is more sound and precise (as it captures actual program behaviour at runtime) but can be incomplete and lacks coverage."
Verbatim: "Due to their ease of use and low cost compared to dynamic analysis, static analysis tools are widely used for security analysis."

## Tool landscape and prior use
**Covers:** pp. 6–7, Section 2.4 paras 2–3

| Tool | Scope in chunk |
|---|---|
| CodeQL | General-purpose automatic analysis tool; used by Pearce et al. on generated Python and C++ code |
| FindBugs/SpotBugs | Java |
| ESLint | JavaScript programs; most commonly used JavaScript static analysis tool among developers (Tomasdottir et al. empirical study) |
| Bandit | Python; used by Siddiq et al. to check Python code generated using a test dataset |
| GoSec | Go programs |
| Cppcheck | Language-tailored supplement in this study (with Bandit) |

Context: "OWASP and Snyk provide a list of commonly used static analysis tools for security analysis" and "Those tools have been widely used in previous security analysis research."
Additional prior-use notes in chunk: Kaur et al. "compared static analysis tools for vulnerability detection in analyzing C/C++ and Java source code"; Lisa et al. "reported on users' goals, motivations, and strategies when using static analysis tools."

## This study's analysis setup
**Covers:** pp. 6–7, Section 2.4 para 4

- Rationale: "By using multiple tools for analysis, potential weaknesses in the code can be discovered from different perspectives and levels, avoiding omissions and improving the accuracy of the analysis."
- Step 1: "Our study first used CodeQL to scan the collected code snippets."
- CodeQL: "an open-source tool that supports multiple languages, including Java, JavaScript, C++, C#, and Python" and "can find weaknesses in a codebase based on known weaknesses/rules."
- Step 2: "to obtain more comprehensive analysis results, we supplemented the scan of code in different languages with static analysis tools (i.e., Cppcheck and Bandi[t]) tailored to specific languages."

## Chunk spillover (figures / Section 3 start)
**Covers:** pp. 6–8 fragments also present in chunk body

- Fig. 1 (p. 6): "Two methods of using Copilot in action" — (a) Method 1: Copilot completes a function using the function name; (b) Method 2: Copilot implements the function in the comment.
- Fig. 2 (p. 7): "More suggestions provided by Copilot."
- Section 3 "RESEARCH DESIGN" begins: describes RQs (3.1), collecting/filtering Copilot-generated snippets (3.2), security analysis plus filtering raw static-analysis results (3.3), and using Copilot Chat to fix identified weaknesses (3.4).
- Fig. 3 (p. 8): "Overview of the research process" pipeline (search terms → filter snippets → dataset features → scan with CodeQL/Bandit/ESLint → manual filter → analyze/CWE Top-25 → Copilot Chat fixes); full RQ/design detail belongs to chunk 04, not summarized here.
