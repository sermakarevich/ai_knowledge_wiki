---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Practices and Challenges of Using GitHub Copilot:

### Q1. What does the opening chunk of the paper actually contain, and what can be cited from it?

> [!tip]- Answer
> It contains only the title "Practices and Challenges of Using GitHub Copilot: An Empirical Study", the authors Beiqi Zhang, Peng Liang, Xiyu Zhou, Aakash Ahmad and Muhammad Waseem with Wuhan University, Hubei Luojia Laboratory and Lancaster University Leipzig affiliations, plus a cut-off abstract fragment. No body, numbers, tables, or findings are present, so this page must not be cited for any paper result. See [[wiki/01-overview|Overview: Practices and Challenges of Using GitHub Copilot]].

### Q2. What research gap motivated the study, and what are the six research questions?

> [!tip]- Answer
> Prior work clustered on correctness, quality, security, and expectations of Copilot-suggested code but left real-world practices and challenges empirically unstudied. The authors therefore define RQ1 programming languages, RQ2 IDEs, RQ3 technologies, RQ4 implemented functions, RQ5 benefits, and RQ6 limitations and challenges, each with a rationale about helping developers choose tools or decide whether to use Copilot. See [[wiki/02-research-design|Research Design: Related Work, Questions, and Data Method]].

### Q3. What data did the authors collect on 23 November 2022, and how did they analyse it?

> [!tip]- Answer
> They collected 169 Copilot-related Stack Overflow posts (557 hits for "copilot", 521 unique URLs, filtered by the inclusion criterion of providing Copilot-referring information with pilot Cohen's Kappa 0.773) plus all 655 discussions under the "Copilot" category of GitHub product categories, chosen to complement SO's Q&A format. Items D1–D6 were counted only when explicitly mentioned as used with Copilot with same-developer repeats counted once, and RQ1–RQ3 were analysed with descriptive statistics while RQ4–RQ6 used the Constant Comparison method with a three-author code–review–consensus workflow. See [[wiki/02-research-design|Research Design: Related Work, Questions, and Data Method]].

### Q4. What do the RQ1–RQ3 results show about languages and technologies, and what caveat applies?

> [!tip]- Answer
> The legible Fig. 2 fragments list Node.js at 41.7%, .Net at 15.0%, Vue at 6.7%, React at 5.0%, and Ajax at 3.3% as the most-used top 5, with a long tail at 1.7–2.2% including PyTorch, Pandas, OpenCV, Spring, Flutter, GraphQL, and MongoDB. Because the figure extraction is garbled, the exact IDE values and the mapping of each percentage to its RQ cannot be reliably reconstructed from this chunk alone. See [[wiki/03-languages-ides-technologies-functions|RQ1–RQ4: Languages, IDEs, Technologies, and Implemented Functions]].

### Q5. Which functions did developers implement most with Copilot, and what is the single headline benefit number?

> [!tip]- Answer
> Fragmentary RQ4 labels show data processing at 26.7% leading, followed by test and front-end element control at 11.1% each, image processing around 9–11%, plus URL-building algorithm at 6.7% and smaller shares for text processing, calculation, and filtering. The complete Table III headline is that useful code generation dominates the benefits with 24 cases at 49.0%, far ahead of faster development at 16.3% and better code quality at 10.2%. See [[wiki/03-languages-ides-technologies-functions|RQ1–RQ4: Languages, IDEs, Technologies, and Implemented Functions]].

### Q6. What are the top three reported benefits of Copilot, with their supporting evidence?

> [!tip]- Answer
> Most developers cited useful code generation, which reduced workload and helped when they had no idea how to write code, exemplified by Copilot excelling at repetitive tests (GitHub #9282). Faster development came second with 8 cases, described as saving "a lot of time" (GitHub #35850), and better code quality third with 5 cases, described as usually shorter and more correct — "often Copilot is smarter than me" (SO #74512186). See [[wiki/04-benefits|RQ5: Benefits of using GitHub Copilot]].

### Q7. What remaining benefits complete the paper's Table III of ten?

> [!tip]- Answer
> Copilot adapts to users' code patterns by learning their style with machine-learning models, and three developers reported a better user experience than other AI tools, calling it more fun and less annoying (GitHub #7254). The full table of ten adds powerful code interpretation and conversion, frequent plugin updates, free access for students, strong integration capability across editors, and ease of study and use at low cost. See [[wiki/04-benefits|RQ5: Benefits of using GitHub Copilot]].

### Q8. What limitations and challenges qualify Copilot's benefits?

> [!tip]- Answer
> Practitioners complained Copilot offers too few solutions ("multiple solution is too little", GitHub #37304) and sometimes poor-quality suggestions that "don't work" (SO #73701039) or become "unacceptable" as files grow (GitHub #9282), alongside code-privacy worries and reports of unfriendly user experience. Integration concentrates in mainstream IDEs (VS Code, Visual Studio, IntelliJ IDEA, NeoVim, PyCharm at 85.9% of IDE use), with friction in lesser-known IDEs like Sublime Text from bad installs or missing support, while usage pairs JavaScript with front-end work and Python with machine-learning work. See [[wiki/05-limitations-and-challenges|Limitations and Challenges of Using GitHub Copilot]].

### Q9. Your team asks whether to adopt Copilot for a new project. What should you recommend?

> [!tip]- Answer
> Recommend deliberate adoption, not default adoption: treat Copilot as a double-edged sword whose useful code generation contradicts its generation limits, quality lapses, privacy exposure, and uneven experience. Match it to mainstream IDEs, suitable languages, and fitting tasks (e.g., JavaScript front-end or Python ML work), weigh integration, user experience, budget, and code privacy explicitly, and revisit when, for what purposes, and by whom it helps as that future work matures. See [[wiki/05-limitations-and-challenges|Limitations and Challenges of Using GitHub Copilot]].
