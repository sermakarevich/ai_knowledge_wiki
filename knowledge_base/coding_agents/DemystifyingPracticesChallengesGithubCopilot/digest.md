> [[index|Wiki]] | [[summary|Summary]]
# September 13, 2023     1:2   WSPC/INSTRUCTION FILE                     ws-ijseke — Digest

## 1. [[wiki/01-introduction-and-paper-overview|Introduction and Paper Overview]]
**In one sentence:** This study mines 303 Stack Overflow posts and 927 GitHub Discussions to map how practitioners use GitHub Copilot — languages, IDEs, technologies, functions, purposes, benefits, limitations, and expected features — concluding it is a double-edged sword.
- GitHub Copilot, the "AI Pair Programmer" powered by OpenAI Codex and launched in June 2021 after training on billions of lines of open-source GitHub code, suggests code or entire functions in IDEs as a plug-in.
- The dataset totals 303 SO posts and 927 GitHub Discussions collected before June 18th, 2023, including 134 new posts and 272 new discussions added to extend the prior SEKE 2023 conference paper.
- Top usage facts: major languages are JavaScript and Python, main IDE is Visual Studio Code, most common technology is Node.js, and leading implemented function is data processing.
- Main purpose is helping generate code, significant benefit is useful code generation, main limitation is difficulty of integration, and most common expected feature is integration with more IDEs.
- The gap addressed is lack of empirically-rooted studies on practices, challenges, and expected features: prior work such as [7] and [8] focused on correctness and understanding of suggested code, while Bird et al. [5] studied initial experiences via three studies.
- Contributions are (1) identifying languages, IDEs, and technologies used with Copilot, (2) reporting functions, purposes, benefits, limitations/challenges, and expected features, and (3) enlarging the dataset to strengthen external validity.
- Extension over the SEKE 2023 paper [9] adds the latest data, new RQ1.4 on purposes, new RQ2.3 on expected features, and more implications for developers and the Copilot team.

## 2. [[wiki/02-capabilities-and-limitations-of-copilot|Capabilities and Limitations of Copilot]]
**In one sentence:** Prior empirical studies find Copilot has real limitations as a developer assistant — language-independent correctness/comprehensibility issues including overly complex code, and assessment overhead that can exceed doing the task manually — motivating this study's broader focus on practices, challenges, and expected features.
- Dakhel et al. [13] empirically evaluated Copilot's capabilities and concluded it shows limitations as an assistant for developers.
- Nguyen and Nadi [14] empirically evaluated the correctness and comprehensibility of Copilot-suggested code across programming languages.
- Copilot's suggestions for different programming languages do not differ significantly in correctness/comprehensibility, per Nguyen and Nadi [14].
- A noted shortcoming is Copilot generating complex code (Nguyen and Nadi [14]).
- Bird et al. [5] ran three studies of how developers use Copilot and found developers spent more time assessing Copilot suggestions than doing the task by themselves.
- Sarkar et al. [15] compared programming with Copilot to previous conceptualizations of programmer assistance, examining similarities/differences and issues in applying LLMs to programming.
- Against prior work (e.g., [8], [13]), this study aims instead to understand practices, challenges, and expected features of Copilot use across various aspects of usage.

## 3. [[wiki/03-research-design-and-data-items|Research Design, Data Items, and Start of Results (Languages and IDEs)]]
**In one sentence:** The study defines eight data items (D1–D8) mapped to RQ1.1–RQ2.3, analyzes languages/IDEs/technologies with descriptive statistics and functions/purposes/benefits/challenges/expected features with constant comparison via multi-author coding, and begins results showing JavaScript and Python each at one fifth of language mentions and Visual Studio Code at 48.0% of IDE mentions.
- Eight data items D1–D8 map one-to-one onto research questions: programming language (RQ1.1), IDE (RQ1.2), technology (RQ1.3), function (RQ1.4), purpose (RQ1.5), benefit (RQ2.1), limitation and challenge (RQ2.2), and expected feature (RQ2.3).
- RQ1.1, RQ1.2, and RQ1.3 were analyzed with descriptive statistics, while RQ1.4, RQ1.5, and all of RQ2 were analyzed qualitatively with the Constant Comparison method comparing emergent codes for similarities and differences to form categories.
- Coding proceeded in three checks: the first and third authors coded filtered posts/discussions with the Table 1 data items, the first author reviewed the third author's coding for correctness, then the first author merged codes into higher-level concepts/categories and the second author examined them, with divergences discussed until all three authors agreed.
- RQ1.1 found 19 programming languages used with Copilot, with JavaScript and Python the most frequent at one fifth each, followed by frequent C# and Java use, while HTML+CSS, TypeScript, Golang, C, Rust, PHP, and Kotlin appeared 3–12 times each (1.5% to 6.1%) and the rest (e.g., Perl, Ruby, Visual Basic) appeared only once.
- RQ1.2 found 25 IDE types used with Copilot, dominated by Visual Studio Code at 48.0% (Copilot initially worked only with VS Code), with Visual Studio, IntelliJ IDEA, NeoVim, and PyCharm together at 38.2% and the remainder rarely mentioned, possibly due to integration issues reported under RQ2.2.
- Results presentation is split: RQ1.1 to RQ1.4 are visualized in Fig 2, and RQ1.5 plus RQ2.1 to RQ2.3 are given in Tables 3, 4, 5, and 6, with full analysis results provided in [24].

## 4. [[wiki/04-languages-and-ides-results|Languages and IDEs Used with Copilot (RQ1.1–RQ1.2)]]
**In one sentence:** This chunk is a garbled OCR/text-extraction of Fig. 2 panels (a)–(b), which report the shares of programming languages (RQ1.1) and IDEs (RQ1.2) used with Copilot, led by entries at 19.4% on the language side and Visual Studio Code at 48.0% on the IDE side.
- The chunk contains no prose, only extracted figure labels: panel titles, percentage values, a "most used (top 5)" annotation, "(%)" axis marks, and the Fig. 2 caption.
- Panel (a) is labeled verbatim "(a) RQ1.1: Programming Languages" with a "most used (top 5)" annotation; two 19.4% values are printed in the language column, one adjacent to the "Python" label.
- Other language shares printed in the chunk include Java (10.7%), C++ (8.7%), HTML+CSS (6.1%), TypeScript (4.6%), Golang (3.1%), JavaScript (1.5%), R (1.0%), Ruby (0.6%), and Perl, Nim, Lua, and Visual Basic at 0.5% each.
- Panel (b) is labeled verbatim "(b) RQ1.2: Integreted Development Environments" (typo "Integreted" as extracted), also with a "most used (top 5)" annotation.
- The clearest IDE shares printed are Visual Studio Code (48.0%), Visual Studio (14.7%), IntelliJ IDEA (8.7%), PhpStorm (2.7%), and DataSpell, Xcode, and CodeSpaces at 0.1% each.
- The values 7.1, 7.7, 8.7, 14.7, and 48.0 are printed together as a group next to "IntelliJ IDEA" / "most used (top 5)"-adjacent labels, with NeoVim and PyCharm labels nearby, but the exact 7.1% vs 7.7% assignment is garbled in extraction order.
- Because the extraction interleaves columns and fragments words, exact rankings beyond the explicitly labeled "most used (top 5)" / single largest values cannot be recovered from this chunk alone.

## 5. [[wiki/05-technologies-and-functions-results|Technologies and Functions Used with GitHub Copilot (RQ1.3–RQ1.4)]]
**In one sentence:** Among 23 technologies used with Copilot Node.js dominates at more than 45%, and among 14 implemented functions data processing is the main one, followed by test (15.1%) and front-end element control (13.2%).
- Figure 2c presents 23 technologies used with Copilot, comprising frameworks, APIs, and libraries.
- Node.js accounts for more than 45% and is the major technology used with Copilot, described as one of the most popular back-end runtime environments for JavaScript.
- The Node.js dominance is presented as reasonable because JavaScript is also the most frequently used language with Copilot (see results of RQ1.1).
- .NET (for Web development) and Vue, React, Flutter, and Ajax (frameworks for front-end development) were mentioned less often compared to Node.js.
- The remaining technologies are rarely used with Copilot and each appears only once, including machine-learning-related ones (e.g., Pandas, Dlib, and OpenCV) and front-end ones (e.g., Htmx, Vanilla JS, and Next.js).
- Figure 2d shows 14 functions implemented by using Copilot, with data processing as the main function, indicating developers tend to use Copilot to write functions working with data.
- Besides data processing, only test (15.1%) and front-end element control (13.2%) account for more than 10% each.
- Developers also use Copilot for string processing, image processing, and algorithm, with image processing and algorithm at the same share (7.5% each); the rest are seldom implemented, mentioned by developers twice or once.

## 6. [[wiki/06-purposes-benefits-and-challenges|Purposes, Benefits, Limitations and Challenges (RQ2.2–RQ2.3)]]
**In one sentence:** Users report 15 limitations topped by IDE-integration difficulty (114, 28.1%) and access difficulty (69, 17.0%), plus code-generation limits, poor quality, and privacy concerns, and respond with 29 expected features led by support for more IDEs (32, 28.8%) and shortcut customization (12, 10.8%).
- Table 5 lists 15 limitations and challenges (RQ2.2); the top two are difficulty of integration (114, 28.1%) and difficulty of accessing Copilot (69, 17.0%).
- Integration difficulty means plug-ins stop working after Copilot installation, shortcut-setting conflicts, no support for some editors, plus server instability, no proxy support, and region access restrictions blocking access.
- Code-generation constraints include too few solutions ("multiple solution is too little", GitHub #37304) and a ~1000-character response limit (GitHub #15122), reported by 48 users (11.8%).
- Poor generated-code quality was reported by 36 users (8.9%), with quotes "GitHub Copilot suggest solutions that don't work" (SO #73701039) and quality that "becomes unacceptable" as files get larger (GitHub #9282).
- Code-privacy threat was reported by 29 users (7.1%), who worried Copilot may use their code information without permission.
- Unfriendly user experience (25, 6.2%) contrasts with the benefit-tail quote that Copilot is "a lot more fun to use and does not annoy me like some other AI systems" (GitHub #7254), whose other products are unnamed.
- Difficulty of subscription (22, 5.4%) increased significantly versus previous work [9], attributed in the chunk to free-plan restrictions, e.g. "so looks like people with a free plan are stuck on a rate-limit for now with no way out" (GitHub #43893).
- Table 6 lists 29 expected features (RQ2.3), led by integration with more IDEs (32, 28.8%), shortcut customization (12, 10.8%), and suggestions only when requested (8, 7.2%) because always-on suggestions are interruptive.

## 7. [[wiki/07-implications-and-discussion|Implications and Discussion]]
**In one sentence:** The study derives empirically grounded implications urging use of mainstream IDEs, leveraging Copilot for front-end and ML work, releasing specialized Copilot versions, weighing its double-edged trade-offs, and adding code-explanation and suggestion-customization features to enable effective use.
- Mainstream IDEs (VS Code, Visual Studio, IntelliJ IDEA, NeoVim, PyCharm) account for 86.2% of Copilot usage, with smoother installation and easier community solutions on SO/GitHub Discussions.
- Using Copilot with lesser-known IDEs (e.g., Sublime Text) causes integration difficulty because the IDE is not officially supported and few peers can offer fixes, so practitioners are advised to use mainstream IDEs while GitHub should support more IDEs.
- Practitioners most often pair JavaScript with front-end element control and Python with ML tasks (data and image processing), reflecting JavaScript's web-client dominance and Python's rich ML libraries such as OpenCV.
- Needed Copilot variants include a team version, a CLI version, and an on-premises version, alongside existing Copilot Labs (experimenting with new ideas), Copilot X (enhancement with new features), and Copilot Nightly (experimental, less well tested changes).
- Copilot is a double-edged sword: benefits such as useful code generation contradict limitations such as limitation to code generation, requiring trade-offs over integration, user experience, budget, and code privacy.
- Understanding generated code is contested — some praise Copilot's code interpretation while others report difficulty understanding output and request explanation features such as auto-generated code comments in the IDE.
- Users demand suggestion customization: changeable accept-suggestion keybinding (currently only Tab), configurable color/font/format to distinguish their code from suggestions, and partial acceptance (line by line or next word only), plus filters, configurable IDE UI, and selectable training sources.

## 8. [[wiki/08-threats-to-validity-and-conclusion|Threats to Validity and Conclusion]]
**In one sentence:** The authors set aside internal validity, mitigate manual-coding bias, limited generalizability from two data sources, and replication risk through multi-author agreement (pilot Cohen's Kappa 0.773) and an open dataset, and conclude from 303 SO posts and 927 GitHub discussions that Copilot is used mainly with JavaScript/Python, VS Code, and Node.js for data processing and code generation, valued for useful code integration but limited by difficulty of integration, with support for more IDEs the most expected feature.
- Internal validity is explicitly not considered because the study "did not investigate the relationships between variables and results"; only three threats are discussed per the guidelines in [16].
- Construct validity threat comes from manual data labelling, extraction, and analysis ("may lead to personal bias"), countered by pilot labelling to reach author agreement, two-author extraction/analysis, a full recheck by the first author of the third author's results, and continuous consultation with the second author.
- External validity is only partially alleviated by using two popular communities — SO (widely used in software engineering studies) and GitHub Discussions (a new GitHub feature for specific topics [17]) — while the authors admit the sources "may not be representative enough" for all Copilot practices, challenges, and expected features.
- Reliability shows a pilot Cohen's Kappa of 0.773 ("a decent consistency") between two authors, but the authors acknowledge residual risk from "the small number of posts used in the pilot" and from three-author manual work resolved by discussion "until there was no any disagreements".
- Replicability is supported by publishing the full dataset of extracted data and labelling results from SO posts and GitHub discussions online for validation and replication [24].
- Conclusions rest on 303 SO posts (search term "copilot") plus 927 GitHub discussions under the "Copilot" category, yielding eight main results: JavaScript/Python top languages, VS Code dominant IDE, Node.js major technology, data processing main function, code generation leading purpose, useful code integration top benefit, difficulty of integration top limitation/challenge, and integration with more IDEs top expected feature.
- Next steps are interviews or an online survey to supplement repository mining and further work on improving developer understanding of generated code (see Section 5); the work was supported by NSFC Grant No. 62172311 and the Special Fund of Hubei Luojia Laboratory.

## The argument in five moves
1. Copilot (OpenAI Codex "AI pair programmer", June 2021) is widely used but empirically under-studied, so the authors mine 303 SO posts and 927 GitHub Discussions to map practices, challenges, and expected features.
2. They code eight data items (languages, IDEs, technologies via descriptive statistics; functions, purposes, benefits, limitations, expected features via constant comparison) with multi-author agreement (pilot Kappa 0.773) and an open dataset.
3. Usage concentrates on JavaScript/Python, VS Code (48.0%, 86.2% mainstream IDEs), Node.js (>45%), and data-processing functions for code generation, with front-end (JavaScript) and ML (Python) pairings.
4. The payoff is useful code generation but the dominant cost is difficulty of IDE integration (28.1%) plus access, generation-limit, quality, privacy, and subscription frictions, mirrored by demands for more IDEs, shortcut/format customization, on-request suggestions, and team/CLI/on-premises versions.
5. Hence Copilot is a double-edged sword requiring trade-offs over integration, experience, budget, and privacy, with validity bounded by two data sources and manual coding, pointing to interviews/surveys and better code explanation next.
