[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Introduction and Paper Overview
**In one sentence:** This study mines 303 Stack Overflow posts and 927 GitHub Discussions to map how practitioners use GitHub Copilot — languages, IDEs, technologies, functions, purposes, benefits, limitations, and expected features — concluding it is a double-edged sword.
## Key points
- GitHub Copilot, the "AI Pair Programmer" powered by OpenAI Codex and launched in June 2021 after training on billions of lines of open-source GitHub code, suggests code or entire functions in IDEs as a plug-in.
- The dataset totals 303 SO posts and 927 GitHub Discussions collected before June 18th, 2023, including 134 new posts and 272 new discussions added to extend the prior SEKE 2023 conference paper.
- Top usage facts: major languages are JavaScript and Python, main IDE is Visual Studio Code, most common technology is Node.js, and leading implemented function is data processing.
- Main purpose is helping generate code, significant benefit is useful code generation, main limitation is difficulty of integration, and most common expected feature is integration with more IDEs.
- The gap addressed is lack of empirically-rooted studies on practices, challenges, and expected features: prior work such as [7] and [8] focused on correctness and understanding of suggested code, while Bird et al. [5] studied initial experiences via three studies.
- Contributions are (1) identifying languages, IDEs, and technologies used with Copilot, (2) reporting functions, purposes, benefits, limitations/challenges, and expected features, and (3) enlarging the dataset to strengthen external validity.
- Extension over the SEKE 2023 paper [9] adds the latest data, new RQ1.4 on purposes, new RQ2.3 on expected features, and more implications for developers and the Copilot team.
---
## Abstract
**Covers:** Title block, authors, abstract (p. 1)

Paper: "Demystifying Practices, Challenges and Expected Features of Using GitHub Copilot" by Beiqi Zhang, Peng Liang (corresponding), Xiyu Zhou (Wuhan University, Hubei Luojia Laboratory), Aakash Ahmad (Lancaster University Leipzig), Muhammad Waseem (Wuhan University); arXiv:2309.05687v1 [cs.SE] 11 Sep 2023; venue header International Journal of Software Engineering and Knowledge Engineering, World Scientific.

Verbatim framing:

> "With the advances in machine learning, there is a growing interest in AI-enabled tools for autocompleting source code. GitHub Copilot, also referred to as the 'AI Pair Programmer', has been trained on billions of lines of open source GitHub code, and is one of such tools that has been increasingly used since its launch in June 2021."

Method stated: searched and manually collected 303 SO posts and 927 GitHub discussions; identified languages, IDEs, technologies, functions implemented, benefits, limitations, and challenges.

Eight headline results, verbatim numbered list: "(1) The major programming languages used with Copilot are JavaScript and Python, (2) the main IDE used with Copilot is Visual Studio Code, (3) the most common used technology with Copilot is Node.js, (4) the leading function implemented by Copilot is data processing, (5) the main purpose of users using Copilot is to help generate code, (6) the significant benefit of using Copilot is useful code generation, (7) the main limitation encountered by practitioners when using Copilot is difficulty of integration, and (8) the most common expected feature is that Copilot can be integrated with more IDEs."

Closing judgment:

> "Our results suggest that using Copilot is like a double-edged sword, which requires developers to carefully consider various aspects when deciding whether or not to use it."

Keywords: GitHub Copilot, Stack Overflow, GitHub Discussions, Repository Mining.

## Introduction
**Covers:** Section 1, pp. 2–3

- LLMs and ML for autocompleting source code are increasingly popular; LLMs incorporate powerful NLP capabilities [1], ML approaches widely applied to source code [2], making LLM synthesis of general-purpose code possible [1]; generative pre-trained models trained on large code corpora attempt reasonable auto-completion [3].
- Copilot, released June 2021, emerged as an "AI pair programmer", powered by OpenAI Codex, suggesting code or entire functions in IDEs as a plug-in [4].
- Claimed gap: "little evidence and lack of empirically-rooted studies (e.g, [3], [5], [6]) on the role of AI-assisted programming tools"; existing studies such as [7] and [8] focus on correctness and understanding of Copilot-suggested code; Bird et al. [5] investigated initial experiences and challenges via three studies, while this study explores practices, challenges, and expected features from developer communities.
- Paradigm claim: "The emergence of Copilot has shifted the paradigm of pair programming, and it is challenging for software development teams to adopt this approach and tool on a large scale [5]."

## Contributions and extension over SEKE 2023
**Covers:** Contributions list, extension list, paper structure (pp. 2–3)

Contributions: (1) identified programming languages, IDEs, and technologies used with Copilot; (2) provided functions implemented, purposes, benefits, limitations/challenges, and expected features; (3) collected and added more SO/GitHub Discussions data "(134 posts and 272 discussions, leading to 303 posts and 927 discussions in total) for purposes of enhancing the external validity".

Extension of conference paper [9] in Proceedings of the 35th SEKE 2023: (1) extended dataset with latest data formulated before June 18th, 2023 (303 SO posts and 927 GitHub discussions in total); (2) explored purposes in RQ1.4; (3) investigated expected features in RQ2.3; (4) more implications.

Structure: Section 2 related work, Section 3 research design, Section 4 results, Section 5 discussion, Section 6 threats to validity, Section 7 conclusions with future directions.

## Related work lead-in (in chunk)
**Covers:** Section 2.1 opening (p. 3)

Chunk begins Section 2.1 "Analyzing the Code Generated Using Copilot": Sandoval et al. [10] user study found LLMs have positive impact on correctness of functions with no decisive impact on safety correctness; Imai [11] found Copilot-generated code inferior to human-written code; Yetistiren et al. [8] assessed validity, correctness, efficiency and found Copilot promising; Madi et al. [6] on readability/visual inspection warn programmers should beware generated code; Wang et al. [12] via mixed methods found effectiveness and code quality matter more than other expectations.
