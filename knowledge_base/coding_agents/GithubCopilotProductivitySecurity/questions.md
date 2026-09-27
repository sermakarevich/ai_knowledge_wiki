---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Date of publication xxxx 00, 0000, date of current version xxxx 00, 0000

### Q1. What is the central thesis and method of this survey paper?
> [!tip]- Answer
> The paper is a selective literature survey synthesizing academic journals, industry reports, and official GitHub/OpenAI documentation on Copilot's productivity and security impact. Its thesis is that Copilot accelerates coding and prototyping while raising persistent security, quality, and IP concerns requiring best practices for responsible adoption. See [[wiki/01-github-copilot-role-overview|GitHub Copilot Role Overview]].

### Q2. What models and training data underlie GitHub Copilot according to the overview?
> [!tip]- Answer
> Copilot launched in 2021 with OpenAI and was originally powered by Codex, described as a GPT-3 variant for code trained on public GitHub repositories including 159 GB of Python code from 54 million repositories. Copilot Chat now operates on GPT-4o with early access to o1, described as excelling in complex reasoning tasks. See [[wiki/01-github-copilot-role-overview|GitHub Copilot Role Overview]].

### Q3. What are Copilot's key features and IDE integrations?
> [!tip]- Answer
> Copilot integrates with Visual Studio Code, Visual Studio, Neovim, and JetBrains, giving real-time autocomplete and whole-function generation from natural-language descriptions while refining suggestions from user input and project context. Table 1 lists Code Completion, Copilot Chat, Copilot in the CLI, PR Summaries (Enterprise only), Text Completion Beta (Enterprise only), and Knowledge Bases for contextual references. See [[wiki/02-copilot-features-models-ides|Copilot Features, IDE Integration, and Adoption]].

### Q4. How large is Copilot adoption and what research method does the paper use?
> [!tip]- Answer
> The chunk cites about 14.5 million Visual Studio downloads, 20 million in Visual Studio Code, 10 million in JetBrains, plus 400+ organizations per GitHub's 2023 report, with growth expected after Copilot for Business. The method is explicitly a selective rather than exhaustive systematic survey of academic databases, industry white papers, technical reports, and official docs to distill challenges, solutions, and best practices. See [[wiki/02-copilot-features-models-ides|Copilot Features, IDE Integration, and Adoption]].

### Q5. What are the five common productivity use cases in Table 2?
> [!tip]- Answer
> Table 2 lists routine task automation for experienced developers (unit tests, database queries), learning and skill development for juniors including the 'Explain this' tutor feature, and code refactoring via redundancy detection and reusable blocks. It adds code review through PR summaries highlighting key areas, and TDD support by generating test cases early to raise initial code quality. See [[wiki/03-productivity-use-cases-studies|Productivity Improvements Associated with Copilot]].

### Q6. What productivity gains did Solohubov et al. and Moradi Dakhel et al. report?
> [!tip]- Answer
> Solohubov et al. on Dart/Flutter CRUD tasks reported roughly 70% effort reduction for simple tasks and about 20% for more complex ones. Moradi Dakhel et al., with 95 Upwork-recruited professional programmers building a JavaScript HTTP server, found AI-assisted developers finished approximately 55.8% faster. See [[wiki/03-productivity-use-cases-studies|Productivity Improvements Associated with Copilot]].

### Q7. What robustness and quality caveats temper the early productivity findings?
> [!tip]- Answer
> Mastropaolo et al. found semantically equivalent descriptions changed output about 46% of the time across 892 Java methods, while Nguyen and Nadi found clear low-complexity LeetCode solutions but also suboptimal code and reliance on undefined helpers. Yetistiren et al. found ChatGPT outperformed Copilot and CodeWhisperer on correct Python solutions with input quality as key, while Mehmood et al. found AI-generated test cases comparable to manual ones. See [[wiki/03-productivity-use-cases-studies|Productivity Improvements Associated with Copilot]].

### Q8. Why is suggestion acceptance rate a misleading productivity proxy?
> [!tip]- Answer
> Acceptance rate correlates strongly with perceived productivity but does not fully reflect developer experience, and Copilot does not always shorten completion time because generated code often needs extra debugging. Mozannar et al., using data from 535 programmers, proposed a utility-theoretic display/withhold framework, found many likely-rejected suggestions avoidable, stressed the programmer's latent unobserved state, and warned that optimizing on acceptance can lower suggestion quality. See [[wiki/04-productivity-literature-context|Productivity Literature Context]].

### Q9. What did the ANZ Bank, ZoomInfo, and GitHub enterprise studies report?
> [!tip]- Answer
> The six-week ANZ Bank experiment found the Copilot group 42.36% faster overall (beginners 52.27%, intermediates 41.6%, advanced 40.48%), while ZoomInfo with 400+ developers found 33% suggestion and 20% lines-of-code acceptance with 72% satisfaction, strong on boilerplate but weak on domain logic. GitHub's 95-participant experiment found 55% faster completion with 88% feeling more productive, and the GitHub–Accenture study found 8.69% more PRs, 15% higher merge rate, and 84% more successful builds. See [[wiki/04-productivity-literature-context|Productivity Literature Context]].

### Q10. How does effectiveness vary by context, and what did Pearce et al. find on security?
> [!tip]- Answer
> Impact varies with developer experience and coding context, with beginners possibly gaining more relatively while relying on suggestions that do not always follow best practices, so acceptance and merge rates alone miss the validation cost. Pearce et al. evaluated Copilot across 89 scenarios covering 25 CWEs, especially the MITRE Top 25, and found 44% of generated code contained security issues such as hardcoded credentials and unsanitized input enabling SQL injection or XSS. See [[wiki/05-productivity-reflections-security-intro|Context-Dependent Effectiveness and Security Concerns Intro]].

### Q11. What is the 24.5% JavaScript finding and how did GitHub respond in 2023?
> [!tip]- Answer
> The study found 24.5% of JavaScript snippets had security issues spanning 38 CWE categories, including CWE-330 (insufficient randomness), CWE-78 (OS command injection), and CWE-94 (code-generation control), with eight in the 2023 CWE Top-25, likely rooted in training-data flaws. GitHub launched a 2023 AI-based vulnerability prevention system blocking insecure patterns in real time (hardcoded credentials, SQL and path injections), though newer versions only reduced rather than eliminated risks so human oversight remains essential. See [[wiki/06-security-findings-vulnerabilities|24.5% of the JavaScript Snippets Exhibited Security Issues]].

### Q12. What best practices cover training, transparency, and legal/ethical risk?
> [!tip]- Answer
> Teams should train developers, document configurations and usage practices, and keep a feedback loop with GitHub to refine the tool with accountability. For IP and privacy, the 'Finding Matching Code' feature surfaces matching code with license counts and types, while sensitive inputs need clear usage policies since they risk unintended data exposure. See [[wiki/07-best-practices|Ensuring Developers Are Well Equipped: Transparency, Legal Care, and Future Work]].

### Q13. What future work does the paper propose on transparency, customization, and evaluation?
> [!tip]- Answer
> It proposes explaining each suggestion with its reasoning and sources, deeper academic/industry studies of long-term developer–AI effects across Copilot, Cursor AI, CodeWhisperer, and Codey, and personalization via model choice, workspaces files, user profiles, custom instructions, and saved session preferences. It also calls for standardized metrics (acceptance rate, correctness, reproducibility, similarity, validity, accuracy, vulnerabilities) and large-scale real-time evaluations across many languages covering standards, security, and maintainability. See [[wiki/08-future-work|Future work: transparency, customization, metrics, and evaluation]].

### Q14. What does the references chunk actually contain, including the pneumonia-heading artifact?
> [!tip]- Answer
> The chunk holds only reference entries 8–41 on Copilot productivity, security, and GitHub docs/blogs plus a Suresh Babu Nettur biography fragment, with no pneumonia-detection body text. The 'Pneumonia Detection in Chest X-Ray' heading is a cross-domain artifact, matching only a reference tail (arXiv:2501.16249) carried over from the source PDF. See [[wiki/09-conclusion-references|Conclusion and References (8 Pneumonia Detection in Chest X-Ray)]].

### Q15. What are the educational and professional backgrounds of the five authors?
> [!tip]- Answer
> Shanthi Karpurapu holds B.Tech and M.Tech degrees in chemical engineering with 10+ years in test automation, while Sravanthy Myneni holds an M.S. from Illinois Tech (2017) with 8+ years in data engineering. Unnati Nettur (Virginia Tech CS undergraduate), Likhit Sagar Gajja (BML Munjal CS bachelor's, interests in AI/prompt engineering/games), and Akhil Dusi (Indiana Tech information sciences master's, cybersecurity/ML certified, web/mobile and pentesting work) complete the team. See [[wiki/10-author-biographies|Author Biographies]].

### Q16. Should your team adopt Copilot broadly given this survey's evidence?
> [!tip]- Answer
> Adopt it selectively for boilerplate, simple tasks, and prototyping where 40–55% speedups are best supported, while requiring mandatory review, testing, and SAST/DAST plus IP/privacy guardrails given the 24.5–44% insecure-output rates and debugging costs. Hold back unrestricted use on complex, domain-specific, or security-sensitive code until standardized benchmarks, explanations, and training-data safeguards mature. See [[wiki/08-future-work|Future work: transparency, customization, metrics, and evaluation]].
