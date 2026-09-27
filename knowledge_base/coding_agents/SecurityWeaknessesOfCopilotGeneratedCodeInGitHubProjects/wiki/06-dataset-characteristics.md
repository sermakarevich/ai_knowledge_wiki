> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Dataset characteristics: lines of code and application domains
**In one sentence:** Files containing Copilot-generated code vary widely in size (mean 183.38 LoC, median 74) and fall into six application domains dominated by Utility Tool and Web Application code, which the authors scan with CodeQL plus Bandit/ESLint before filtering duplicates.
## Key points
- Python files (n described in Fig. 9): mean 218.22 LoC, median 92.00, min 7.00, max 4394.00, std dev ±447.71.
- JavaScript files: mean 136.89 LoC, median 63.00, min 8.00, max 4005.00, std dev ±292.81.
- Combined Python+JavaScript: mean 183.38 LoC, median 74.00, min 7.00, max 4394.00, std dev ±390.83.
- Generated code was categorized into six application domains: Game, Web Application, Utility Tool, AI Application, Network Communication, and Others, after authors discussed "until they reached a consensus."
- Python is led by Utility Tool (39.0%), followed by Game (15.9%), Web Application (15.6%), AI Application (15.6%), Network Communication (8.2%), and Others (5.4%).
- JavaScript is led by Web Application (49.8%), followed by Utility Tool (30.1%), Game (8.5%), Network Communication (5.7%), AI Application (2.8%), and Others (2.8%).
- The authors chose static over dynamic analysis because "the static analysis has higher coverage and is able to analyze programs without executing them," while dynamic analysis "suffers from limited coverage and can be expensive."
- Each snippet was scanned with two tools (CodeQL plus Bandit for Python / ESLint for JavaScript); initial filtering removed 14 duplicate results by Bandit and 2 by ESLint, keeping one copy.
---
## Lines of code (Fig. 9)
**Covers:** "The number of lines per code snippet" + Fig. 9 (chunk lines 1–18)

| Metric | Python | JavaScript | Python+JavaScript |
|---|---|---|---|
| Mean | 218.22 | 136.89 | 183.38 |
| Median | 92.00 | 63.00 | 74.00 |
| Min | 7.00 | 8.00 | 7.00 |
| Max | 4394.00 | 4005.00 | 4394.00 |
| Std Dev | ±447.71 | ±292.81 | ±390.83 |

> Fig. 9. Distribution of LoC of the files where AI-generated code was present

## Application domains (Table 3)
**Covers:** domain categorization + Table 3 (chunk lines 20–23, 38–51)

> "In total, we categorized the generated code into six application domain categories: Game, Web Application, Utility Tool, AI Application, Network Communication, and Others."

| Category | Description | Python | JavaScript |
|---|---|---|---|
| Utility Tool | Involves scripts, command-line tools, and other programs that simplify daily tasks. | 39.0% | 30.1% |
| Web Application | Code related to front-end, back-end development, and server-side operations. | 15.6% | 49.8% |
| AI Application | Code for machine learning, deep learning, natural language processing, or other intelligent applications. | 15.6% | 2.8% |
| Game | Contains code related to game development, using engines such as Unity, Unreal, and Godot. | 15.9% | 8.5% |
| Network Communication | Involves code for implementing network protocols, client/server communication. | 8.2% | 5.7% |
| Others | Code that does not fit into the above categories. | 5.4% | 2.8% |

## Scan setup and filtering (context in this chunk)
**Covers:** Sections 3.3–3.3.2 as present in this chunk (chunk lines 25–35, 53–116)

- Tools per snippet: "we used two static analysis tools for security checks on each code snippet (i.e., CodeQL plus one dedicated tool for the specific language, Bandit for Python, and ESLint for JavaScript)."
- CodeQL suites used: "<language>-security-and-quality.qls"; "the python-security-and-quality.qls test suite for Python provides 168 security checks, and the JavaScript test suite provides 203 security checks."
- Bandit: "a Python's static security analysis tool"; "we enabled all security rules by default"; "Bandit had a total of 73 security check rules."
- ESLint: security rules via "the eslint-plugin-security plugin for security checks, which is an ESLint plugin containing 14 security check rules," plus "eslint-plugin-no-secrets and eslint-plugin-xss."
- Snippet scope: "we considered the code snippet from the Repository label to be the entire code file, while the code snippet from the Code label exists in the code file."
- Dedup: "we manually removed the duplicate analysis results that were reported by the two tools (14 duplicate results by Bandit and 2 duplicate results by ESLint), keeping only one for further analysis."
- Mapping note: "the detection rules of these static analysis tools do not have a one-to-one correspondence with CWEs"; authors "manually mapped the detection rules to the CWEs" with correspondences in replication package.

**Covers:** chunk "The number of lines per code" (Fig. 9 LoC stats; six-category domain Table 3; Sections 3.3–3.3.2 scan/filtering excerpt as included in this chunk)
