> [[index|Wiki]] | [[summary|Summary]]
# Practices and Challenges of Using GitHub Copilot: — Digest
## 1. [[wiki/01-overview|Overview: Practices and Challenges of Using GitHub Copilot]]
**In one sentence:** This chunk is truncated/garbled — it contains only the paper title, author/affiliation block, and a cut-off fragment of the abstract's opening sentence, so no substantive claim from the paper can be summarised from it.
## Key points
- The chunk contains the paper title "Practices and Challenges of Using GitHub Copilot: An Empirical Study" and nothing beyond the abstract's opening fragment.
- The listed authors are Beiqi Zhang, Peng Liang, Xiyu Zhou, Aakash Ahmad, and Muhammad Waseem.
- Affiliations given are the School of Computer Science, Wuhan University; Hubei Luojia Laboratory; and Lancaster University Leipzig (School of Computing and Communications).
- Contact emails listed are {zhangbeiqi, liangp, xiyuzhou, m.waseem}@whu.edu.cn and a.ahmad13@lancaster.ac.uk.
- The only abstract text present is the fragment "With the advances in machine learning, there is a" followed by "[3]. Released on June 2021, GitHub Copilot has recently" — the sentence is cut off mid-phrase.
- Because the body, numbers, mechanisms, tables, and quotes are absent from this chunk, no findings, statistics, or conclusions are stated here; do not cite this page for paper results.
## 2. [[wiki/02-research-design|Research Design: Related Work, Questions, and Data Method]]
**In one sentence:** Prior work on Copilot focused on code correctness, quality, security and expectations but left practices and challenges unstudied, so the authors define six research questions (RQ1–RQ6) and answer them with 169 Stack Overflow posts and 655 GitHub Discussions collected on 23 November 2022, analysed by descriptive statistics (RQ1–RQ3) and constant comparison (RQ4–RQ6).
## Key points
- Gap claim: existing studies focus on correctness and understanding of Copilot-suggested code, with little empirically-rooted evidence on practices and challenges of using Copilot in programming activities.
- Six RQs cover programming languages (RQ1), IDEs (RQ2), technologies (RQ3), functions implemented (RQ4), benefits (RQ5), and limitations/challenges (RQ6), each with an explicit rationale for helping developers choose tools or decide whether to use Copilot.
- SO collection: search term "copilot" returned 557 posts, reduced to 521 unique URLs after deduplication, then to 169 Copilot-related posts after manual filtering with inclusion criterion that the post must provide information referring to Copilot.
- Pilot labelling agreement: two authors labelled 10 SO posts with Cohen's Kappa 0.773, described as decent agreement between the two coders.
- GitHub Discussions collection: all 655 discussions under the "Copilot" category of "GitHub product categories" were included, chosen because Discussions support varied intentions (e.g., reporting errors, discussing development) complementary to SO's Q&A format.
- Extraction rule: an item (D1–D6) was counted only if explicitly mentioned as used with Copilot, and repeated mentions of the same item by the same developer in one post/discussion counted once, while mentions by multiple developers could make instance counts exceed post/discussion counts.
- Analysis split: RQ1–RQ3 use descriptive statistics while RQ4–RQ6 use the Constant Comparison method, with RQ4 categories built from developers' own descriptions of functions and a three-author code–review–consensus workflow.
## 3. [[wiki/03-languages-ides-technologies-functions|RQ1–RQ4: Languages, IDEs, Technologies, and Implemented Functions]]
**In one sentence:** The chunk's Figure 2 (RQ1–RQ4) is largely garbled in extraction but preserves fragmentary percentage labels for languages/technologies alongside the full Table III of Copilot benefits, led by useful code generation at 49.0%.
## Key points
- The chunk centers on Fig. 2 covering RQ1–RQ4 (programming languages, IDEs, technologies, implemented functions), but the extracted figure text is garbled and fragmented.
- Legible language/technology labels include Node.js (41.7%), .Net (15.0%), Vue (6.7%), React (5.0%), and Ajax (3.3%), with a "most used (top 5)" annotation and scale "3.3 5.0 6.7 15.0 41.7".
- Other fragmentary labels include Three.js (1.7%), Spring (1.7%), Framework (1.7%), PyTorch (1.7%), Pandas (1.7%), OpenCV (1.7%), Dlib (1.7%), Doom (1.7%), Flutter (1.7%), GraphQL (2.2%), gRPC (1.7%), Htmx (1.7%), Jinja (1.7%), LibTorch (1.7%), MongoDB (1.7%), Next.js (1.7%), and Ajax (3.3%).
- Fragmentary implemented-function labels include Data processing (26.7%), Test (11.1%), Image processing (8.9% / 11.1% in different fragments), Front-end element control (11.1%), String processing, Text processing (4.4%), Calculation (4.4%), URL building Algorithm (6.7%), and Filtering (2.2%).
- The chunk also contains the complete TABLE III (Benefits, RQ5): useful code generation leads with 24 cases (49.0%), followed by faster development with 8 (16.3%) and better code quality with 5 (10.2%).
- Because the figure extraction is garbled, exact IDE (RQ2) values and the mapping of each percentage to its RQ cannot be reliably reconstructed from this chunk alone.
## 4. [[wiki/04-benefits|RQ5: Benefits of using GitHub Copilot]]
**In one sentence:** Developers most valued Copilot for useful code generation that reduced workload and helped when they had no idea how to write code, plus faster development, shorter and more correct code, adaptation to their code patterns, and a more fun, less annoying experience than other AI tools.
## Key points
- Most developers cited useful code generation: it reduced their workload and gave help when they had no idea how to write code.
- Faster development: Copilot "saves developers a lot of time" (GitHub #35850).
- Better code quality: Copilot-suggested code is usually shorter and more correct than developer-written code — "often Copilot is smarter than me" (SO #74512186).
- Adaptation to user style: Copilot uses machine learning models to learn developers' code style and adapt to their code patterns.
- Better user experience, mentioned by three developers, including feeling that Copilot is more fun and less annoying than other AI-assisted programming tools (GitHub #7254).
- The paper's Table III lists 10 benefits in total; the chunk excerpt details the benefits above without reproducing the full table.
## 5. [[wiki/05-limitations-and-challenges|Limitations and Challenges of Using GitHub Copilot]]
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
## The argument in five moves
1. Prior Copilot research covered correctness, quality, security, and expectations but left real-world practices and challenges unstudied, motivating six research questions (RQ1–RQ6).
2. The authors answer them empirically with 169 Stack Overflow posts and 655 GitHub Discussions from 23 November 2022, using descriptive statistics for languages/IDEs/technologies and constant comparison for functions/benefits/limitations.
3. Usage concentrates in mainstream IDEs and pairs JavaScript with front-end work and Python with machine-learning work, with data processing, tests, and front-end control among the implemented functions.
4. The payoff developers report is useful code generation that cuts workload, faster development, shorter and more correct code, adaptation to personal code patterns, and a more fun experience — led by useful code generation at 49.0%.
5. The costs qualify that payoff: too few and sometimes non-working suggestions, privacy worries, uneven user experience, and integration friction outside mainstream IDEs.
6. Hence Copilot is a double-edged sword to be adopted deliberately — matched to suitable languages, technologies, and IDEs, weighing integration, experience, budget, and privacy — with future work on when, for what purposes, and by whom it is best used.
