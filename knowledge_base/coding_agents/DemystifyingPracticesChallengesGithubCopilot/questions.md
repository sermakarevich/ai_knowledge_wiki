---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: September 13, 2023     1:2   WSPC/INSTRUCTION FILE                     ws-ijseke

### Q1. What study is this in one sentence, and what dataset and headline results does it report?

> [!tip]- Answer
> This study mines 303 Stack Overflow posts and 927 GitHub Discussions collected before June 18th, 2023 to map Copilot languages, IDEs, technologies, functions, purposes, benefits, limitations, and expected features. Headline results are JavaScript and Python as top languages, Visual Studio Code as dominant IDE, Node.js as top technology, data processing as leading function, code generation as main purpose and benefit, integration difficulty as top limitation, and support for more IDEs as top expected feature. It concludes Copilot is a double-edged sword requiring careful trade-offs. See [[wiki/01-introduction-and-paper-overview|Introduction and Paper Overview]].

### Q2. How does this study position itself against prior Copilot capability studies?

> [!tip]- Answer
> Prior work evaluated Copilot as an assistant: Dakhel et al. found limitations, Nguyen and Nadi found language-independent correctness and comprehensibility issues including overly complex code, and Bird et al. found developers spent more time assessing suggestions than doing tasks alone. Sarkar et al. compared Copilot programming with earlier programmer-assistance concepts and LLM application issues. This study instead maps practices, challenges, and expected features across many usage aspects from developer communities. See [[wiki/02-capabilities-and-limitations-of-copilot|Capabilities and Limitations of Copilot]].

### Q3. What are data items D1–D8, their research questions, and their analysis methods?

> [!tip]- Answer
> D1–D8 map one-to-one onto RQ1.1–RQ2.3: programming language, IDE, technology, implemented function, purpose, benefit, limitation and challenge, and expected feature. RQ1.1–RQ1.3 use descriptive statistics while RQ1.4, RQ1.5, and all of RQ2 use Constant Comparison qualitative coding of emergent codes into categories. Coding was done by the first and third authors, rechecked by the first author, merged into higher-level categories, examined by the second author, and resolved by discussion until full agreement. See [[wiki/03-research-design-and-data-items|Research Design, Data Items, and Start of Results]].

### Q4. What do Fig. 2 panels (a)–(b) report about languages and IDEs used with Copilot?

> [!tip]- Answer
> Panel (a) covers 19 languages with JavaScript and Python each near one fifth at the top, followed by C# and Java, then shares such as Java 10.7%, HTML+CSS 6.1%, TypeScript 4.6%, and a long tail of once-mentioned languages like Perl, Ruby, and Visual Basic. Panel (b) covers 25 IDE types dominated by Visual Studio Code at 48.0%, with Visual Studio at 14.7%, IntelliJ IDEA at 8.7%, NeoVim and PyCharm near 7–8%, and rare mentions such as PhpStorm 2.7% and DataSpell, Xcode, and CodeSpaces at 0.1%. The extraction is garbled so only the labeled top values and explicitly attached shares are reliable. See [[wiki/04-languages-and-ides-results|Languages and IDEs Used with Copilot]].

### Q5. Which technologies are used with Copilot and why does Node.js dominate?

> [!tip]- Answer
> Figure 2c lists 23 technologies including frameworks, APIs, and libraries, with Node.js above 45% as the major technology. This is presented as reasonable because JavaScript is the most frequent Copilot language and Node.js is a leading JavaScript back-end runtime. The rest are far less common: .NET, Vue, React, Flutter, and Ajax appear occasionally, while ML items like Pandas, Dlib, and OpenCV and front-end items like Htmx, Vanilla JS, and Next.js each appear only once. See [[wiki/05-technologies-and-functions-results|Technologies and Functions Used with GitHub Copilot]].

### Q6. What functions do developers implement with Copilot?

> [!tip]- Answer
> Figure 2d lists 14 implemented functions led by data processing, showing developers mainly use Copilot to write data-handling code. Only test at 15.1% and front-end element control at 13.2% exceed 10% besides the leader. String processing, image processing, and algorithm follow, with image processing and algorithm tied at 7.5% each, while remaining functions were mentioned only twice or once. See [[wiki/05-technologies-and-functions-results|Technologies and Functions Used with GitHub Copilot]].

### Q7. What are the top limitations and challenges of using Copilot?

> [!tip]- Answer
> Table 5 lists 15 limitations led by difficulty of integration at 114 mentions (28.1%), covering plug-in breakage, shortcut conflicts, unsupported editors, server instability, missing proxy support, and region restrictions. Next are difficulty of accessing Copilot at 69 (17.0%) and code-generation constraints at 48 (11.8%), such as too few solutions and a roughly 1000-character response limit. Poor generated-code quality (36, 8.9%), code-privacy threat (29, 7.1%), unfriendly user experience (25, 6.2%), and a rising difficulty of subscription (22, 5.4%) round out the major complaints. See [[wiki/06-purposes-benefits-and-challenges|Purposes, Benefits, Limitations and Challenges]].

### Q8. What features do users most expect from Copilot?

> [!tip]- Answer
> Table 6 lists 29 expected features led by integration with more IDEs at 32 mentions (28.8%), mirroring the top integration limitation. Developers also want shortcut customization at 12 (10.8%), such as replacing Tab with a custom key, and on-request-only suggestions at 8 (7.2%) because always-on suggestions interrupt. Further asks include a team version and proxy support at 7 each, format customization, partial acceptance of suggestions, and compatibility with tools like ReSharper. See [[wiki/06-purposes-benefits-and-challenges|Purposes, Benefits, Limitations and Challenges]].

### Q9. What implications does the study draw for effective Copilot use?

> [!tip]- Answer
> Practitioners should prefer mainstream IDEs (VS Code, Visual Studio, IntelliJ IDEA, NeoVim, PyCharm, jointly 86.2%), which install smoothly and have community fixes, while GitHub should support more IDEs. JavaScript pairs with front-end element control and Python with ML work like data and image processing via libraries such as OpenCV, and the authors call for team, CLI, and on-premises variants alongside Labs, X, and Nightly. They urge customizable keybindings, suggestion appearance, partial acceptance, filters, and in-IDE code explanations to resolve the contested comprehensibility of generated code. See [[wiki/07-implications-and-discussion|Implications and Discussion]].

### Q10. (Evaluation) Should you treat the eight headline results as settled general facts when deciding to adopt Copilot?

> [!tip]- Answer
> No, treat them as indicative but bounded: the evidence comes only from Stack Overflow and GitHub Discussions, which the authors admit may not represent all practices, and manual labelling risks bias despite pilot agreement at Cohen's Kappa 0.773 and three-author resolution plus an open replication dataset. For an adoption decision, pilot Copilot in your own mainstream IDE and stack, weigh integration, privacy, budget, and subscription frictions from RQ2.2, and supplement with interviews or a survey as the authors propose before generalizing. See [[wiki/08-threats-to-validity-and-conclusion|Threats to Validity and Conclusion]].
