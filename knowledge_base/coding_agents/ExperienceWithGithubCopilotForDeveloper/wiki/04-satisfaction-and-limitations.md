> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Potential Limitations and Related Work
**In one sentence:** The authors list eight envisioned but unobserved limitations of GitHub Copilot (data exposure, IP, vulnerabilities, privacy, compliance, over-reliance, bad patterns, lost creativity) and survey related work showing mixed productivity and correctness results, concluding their own benefits-and-limitations findings are mostly in alignment with that literature.
## Key points
- Eight potential limitations are envisioned despite not being observed: sensitive-data exposure, IP infringement, security vulnerabilities, telemetry privacy, compliance violations, over-reliance, reinforcement of insecure patterns, and reduced creativity/productivity.
- GitHub's own report [34] finds acceptance rate of shown suggestions is a better predictor of perceived productivity than alternative measures, and the authors adopt the same measure in §6.
- Reported correctness varies widely by study: ~60% Java / ~30% JavaScript on LeetCode [15], 70–95% by human graders on intro assignments [19], ~29% correct / ~20% incorrect / rest partially correct with ~92% valid code [30].
- Test-generation and robustness results are weak: ~55% of generated tests fail inside an existing suite and ~92% outside it [11]; ~50% of suggestions differ on semantically equivalent prompts with correctness affected in ~30% of cases [14].
- Project-level effects are mixed: +6.5% productivity from individual output plus participation but +42% integration time [20], versus +40–50% task-time boost growing with difficulty in a ~1,000-engineer, four-week corporate deployment [2].
- Prompt language and privacy matter: worst Copilot performance in Chinese among Chinese/English/Japanese with all degrading as difficulty rises [12], and ~8% of test cases leak sensitive personal information from the Codex model [16].
- Usage patterns: JavaScript/Python, VS Code, and data processing dominate discussions [33]; Copilot ranks second to ChatGPT on HumanEval [29]; generated code is mostly small, low-complexity, sparsely commented functions with fewer modifications than human code [32].
---
## Potential (unobserved) limitations
**Covers:** pp. 17, "Though we have not observed yet, we can envision..."

Though not observed, the authors envision these limitations:

- Sensitive Data Exposure: Copilot may inadvertently suggest or generate code containing sensitive or proprietary information due to its training on public repositories.
- Intellectual Property Issues: Copilot might suggest snippets resembling copyrighted or proprietary code, leading to potential infringement.
- Code Quality and Vulnerabilities: generated code could contain security vulnerabilities, requiring thorough review before integration.
- Data Privacy: if telemetry data is collected, there could be privacy concerns over how it is stored and used.
- Compliance Risks: some industries have strict compliance requirements, and Copilot may unintentionally violate these by generating code or comments not in line with regulatory guidelines.
- Over-reliance on AI: developers might become too reliant on AI suggestions, overlooking best practices in favor of quicker implementation.
- Unintended Patterns: Copilot might reinforce problematic or insecure coding patterns learned from public repositories.
- Creativity/productivity: Copilot "helps with writing code but may make developers less creative and even less productive eventually"; developers should "balance working fast with coming up with their own ideas" and think about how to use it without relying on it too much.

## Related work
**Covers:** Section 12, pp. 18–20 (refs [2]–[34] as cited in chunk)

Context: many factors affect developer productivity (summary in [6], preview in §3); this section covers only factors Copilot can impact (see [7, 25, 8, 17, 21]).

Tool background (verbatim quotes from chunk):

- Launch news in [9], plus [26]; launched as "a new AI pair programmer that helps you [developers] write better code."
- Description: "GitHub Copilot draws context from the code you're working on, suggesting whole lines or entire functions. It helps you quickly discover alternative ways to solve problems, write tests, and explore new APIs without having to tediously tailor a search for answers on the internet. As you type, it adapts to the way you write code—to help you complete your work faster."
- Copilot uses a version of Codex, originally a GPT language model from OpenAI fine-tuned on publicly available code from GitHub [3]; the Codex paper discusses over-reliance, misalignment, bias and representation, economic/labor impacts, security, environmental, and legal implications, plus risk mitigation.

| Study | Finding (exact numbers from chunk) |
|---|---|
| [34] GitHub researchers (survey + IDE measurements: suggestion counts, acceptances, code contributed/accepted) | "find that acceptance rate of shown suggestions is a better predictor of perceived productivity than the alternative measures" |
| [15] LeetCode problems, LeetCode tests | Correctness ~60% Java, ~30% JavaScript |
| [20] open-source GitHub development | +6.5% project-level productivity (individual productivity + participation); +42% integration time |
| [33] Stack Overflow + GitHub discussions | JS and Python most common languages; VS Code most used IDE; data processing most common generation function; integration challenges confirm [20] |
| [11] test generation on open-source projects | ~55% of generated tests fail inside an existing suite; ~92% fail outside one; "not a panacea" |
| [30] systematic limits/benefits evaluation | Valid code ~92% success; correct ~29%, incorrect ~20%, rest partially correct |
| [14] robustness via semantically equivalent prompts | ~50% of cases give a different function than expected; correctness affected in ~30% of cases |
| [24] Copilot Codex vs. Davinci on simple assignments | Negative on Copilot vs. Davinci; students must know limits and fix generated code |
| [19] intro-programming tasks | Correctness ~70% to ~95% by human graders (more positive) |
| [5] sorting/basic data structures + tasks vs. humans | Correct most of the time, still not as good as human programmers |
| [2] corporate deployment, ~1,000 engineers, 4 weeks, surveys + controlled experiments | Notable boost in productivity, code quality, job satisfaction; ~40–50% less time on tasks, gap growing with difficulty |
| [31] collaboration on open source | More maintenance-related than code-development contributions |
| [23], [22] bug fixing / unit-test models trained on GitHub code | Both claim positive productivity impact |
| [29] Copilot vs. CodeWhisperer vs. ChatGPT on HumanEval | Copilot second after ChatGPT |
| [32] Copilot + ChatGPT code hosted at GitHub (dismisses HumanEval as unrepresentative) | Top two models; Python/Java/TypeScript most common for data processing/transformation, C/C++/JavaScript for algorithms/data structures/UI; mostly small low-complexity sparsely commented functions with fewer modifications than human code |
| [12] prompting in Chinese/English/Japanese | Worst in Chinese; all three drop with question difficulty |
| [16] semi-automated extraction of sensitive personal info from Codex | Privacy leaks in ~8% of test cases |
| [13] instructor perspectives | No consensus yet; short-term split on banning vs. allowing AI |

Authors' alignment note (verbatim gist): "After this related work review, we feel our findings regarding benefits and limitations of GitHub Copilot are mostly in alignment with those of the relevant related work but the exact figures naturally differ due to such reasons as types of tasks, interview questions vs. production work, programming languages, students vs. developers, etc."

## Conclusions and Future Work (opening only)
**Covers:** Section 13 opening (chunk truncates here)

- Chunk ends at: "In addition to sharing our comprehensive evaluation methodology, our study provides several key insights into the enterprise-scale deployment of GitHub Copilot for developers:" — no further conclusions content is present in this chunk.
- Note: no developer-satisfaction survey results appear in this chunk despite the plan.md Covers label; only the unobserved-limitations list, Related Work §12, and the §13 opening sentence above are covered here.
