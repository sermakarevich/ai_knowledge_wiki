> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Limitations and Challenges of Using GitHub Copilot
**In one sentence:** Copilot is limited by few and sometimes poor-quality suggestions, code-privacy worries and uneven user experience, and works best as a double-edged sword when paired with mainstream IDEs and suitable languages rather than lesser-known setups.
## Key points
- Practitioners complained Copilot offers too few solutions, with one developer saying "multiple solution is too little" (GitHub #37304), limiting code generation.
- Practitioners reported poor generated-code quality, including suggestions that "don't work" (SO #73701039) and quality that "becomes unacceptable" as code files get larger (GitHub #9282).
- Developers worried about code privacy threats, fearing Copilot may use their code information without permission.
- Some practitioners reported an unfriendly user experience with Copilot, contrary to others who found it better than other AI-assisted programming tools.
- Most developers integrate Copilot in mainstream IDEs (Visual Studio Code, Visual Studio, IntelliJ IDEA, NeoVim, PyCharm), which reach 85.9% of IDE use with Copilot; lesser-known IDEs such as Sublime Text bring integration difficulty.
- Integration difficulty comes from incorrect installation in chosen IDEs and from Copilot not supporting certain IDEs, so the authors recommend practitioners use mainstream IDEs where fixes are easy to find on SO or GitHub Discussions.
- Practitioners tend to use JavaScript for front-end work (e.g., front-end element control) and Python for machine learning work (e.g., data and image processing, e.g., OpenCV), matching RQ1/RQ3/RQ4 results.
- Using Copilot is described as a double-edged sword: benefits such as useful code generation contradict limitations and challenges, so developers should weigh integration, user experience, budget, and code privacy before deciding.
---
## Restrictions on generation, quality, privacy, and experience
**Covers:** RQ6 limitations discussion (chunk lines 3–18)

Copilot has restrictions: it sometimes offers few solutions, which are not enough for users and limit code generation — "multiple solution is too little" (GitHub #37304). Practitioners also complained about poor quality of generated code: "GitHub Copilot suggest solutions that don't work" (SO #73701039), and when code files became larger the suggested quality "becomes unacceptable" (GitHub #9282). Developers paid much attention to code privacy threat, worried Copilot may use their code information without permission. Contrary to developers who said Copilot gave a better user experience than other AI-assisted programming tools, some practitioners reported an unfriendly user experience when coding with Copilot.

## Integration of Copilot with IDEs
**Covers:** Section V Implications — IDE integration (chunk lines 20–39)

| Claim | Detail from chunk |
|---|---|
| Mainstream IDEs | Visual Studio Code, Visual Studio, IntelliJ IDEA, NeoVim, and PyCharm |
| Share | 85.9% of IDE use with Copilot is mainstream IDEs (from RQ2 and RQ6) |
| Problem case | Lesser-known IDEs (e.g., Sublime Text) make the Copilot plug-in hard to integrate |
| Causes of difficulty | Developers may install Copilot incorrectly in their chosen IDEs; Copilot does not support certain IDEs at the moment |
| Why mainstream is easier | Smooth install, and problems can be solved via SO or GitHub Discussions because many developers encountered similar issues |
| Recommendation | Use mainstream IDEs with Copilot to reduce integration difficulty; authors note Copilot may support more IDEs in the future |

## Front-end and machine-learning use
**Covers:** Section V Implications — front-end / ML support (chunk lines 3–19, right column)

From RQ1, RQ3, and RQ4, practitioners often write JavaScript and Python when using Copilot and tend to pair Copilot with front-end and machine-learning technologies (frameworks, APIs, libraries) to implement front-end functions (e.g., front-end element control) and machine-learning functions (e.g., data processing and image processing). JavaScript is the foundation of many popular front-end frameworks and most websites use it client-side; Python is the first choice for machine-learning development with rich libraries such as OpenCV. It is therefore reasonable that developers use Copilot with JavaScript for front-end and Python for machine-learning code generation.

## Potentials and perils: a double-edged sword
**Covers:** Section V Implications — potentials and perils (chunk lines 21–48)

Trained on billions of lines of code, Copilot can turn natural-language prompts into coding suggestions across dozens of programming languages and make developers code faster and easier [4]. RQ5 and RQ6 show many benefits contradict its limitations and challenges (e.g., useful code generation vs. limitation to code generation). Developers deciding to use Copilot should consider tool integration, user experience, budget, code privacy, and other aspects, and make trade-offs. In short, Copilot is like a double-edged sword: if used with appropriate languages and technologies to correctly implement required functions in developers' IDEs, it optimizes workflow by letting AI do redundant work; otherwise it brings difficulties and restrictions that leave developers frustrated and constrained. Study results help practitioners weigh advantages and disadvantages for an informed decision.

## Towards effective use, validity, and conclusions
**Covers:** Sections V–VII tail in chunk (chunk lines 40–111)

| Subsection | Claims present in chunk |
|---|---|
| Effective use (future work) | Investigate Copilot practices via questionnaire and interview; study when challenges appear as advantages vs. disadvantages and how to convert disadvantages into advantages; explore user types (developers, educators, students), when/how they use Copilot, and for what specific purposes; next step is when to use Copilot, for what purposes, and by whom |
| Construct validity | Manual data labelling, extraction, and analysis may cause personal bias; mitigated by pilot labelling to reach author agreement on SO posts, extraction/analysis by two authors with recheck by first author, and continuous consultation between first and second authors |
| External validity | Two sources (SO, widely used in SE studies, and GitHub Discussions, a newer GitHub topic-discussion feature [14]) partially alleviate the threat, but selected sources may not represent all Copilot practices and challenges |
| Reliability | Pilot SO labelling by two authors with Cohen's Kappa 0.773 (decent consistency), though pilot used few posts; three authors discussed results until no disagreements; dataset with extracted data and labelling from SO posts and GitHub discussions shared online for validation/replication [20] |
| Conclusions | Empirical study of SO and GitHub Discussions from practitioners' perspective; searched "copilot" on SO and collected all "Copilot"-category GitHub discussions, yielding 169 SO posts and 655 GitHub discussions; identified languages, IDEs, technologies, implemented functions, benefits, limitations, and challenges as first-hand developer information |
