> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Related Work, Conclusions and Future Work
**In one sentence:** Prior work finds Copilot boosts perceived productivity but not always task success or code quality, and this study concludes that in ~46% of 892 Java methods semantically equivalent descriptions yield different recommendations, so developers must learn to write proper descriptions.
## Key points
- GitHub Copilot is framed as the state-of-the-art code recommender, advertised as an "AI pair programmer" [1], [22].
- Imai [25] found Copilot increases productivity (number of added lines of code) but decreases quality in the produced code as an alternative to a human pair programmer.
- Ziegler et al. [67] found that the acceptance rate of suggested solutions is the best predictor for perceived productivity.
- Vaithilingam et al. [59] ran an experiment with 24 developers and found Copilot does not improve task completion time and success rate, though developers prefer it as a starting point that saves online search effort.
- Nguyen and Nadi [43] evaluated Copilot on LeetCode questions across languages: correctness ranged between 57% (Java) and 27% (JavaScript), while generated solutions had low Cyclomatic and Cognitive Complexity [13] for all languages.
- This study generated 892 non-trivial Java methods from the original description (first sentence in the Javadoc) plus manually and automatically paraphrased descriptions, finding ~46% of cases gave different code recommendations.
- Some correct recommendations could only be obtained using one of the semantically equivalent descriptions, unlike prior work focused on correctness/productivity, this work focuses on robustness to different inputs.
---
## Related work on GitHub Copilot
**Covers:** chunk section "GitHub Copilot has been recently introduced" (related work)

> "GitHub Copilot has been recently introduced as the state-of-the-art code recommender, and advertised as an "AI pair programmer" [1], [22]."

| Study | Setup | Finding (from chunk) |
|---|---|---|
| Imai [25] | Copilot vs human pair programmer | Increased productivity (i.e., number of added lines of code), but decreased quality in the produced code |
| Ziegler et al. [67] | Case study on usage measurements predicting productivity | Acceptance rate of the suggested solutions is the best predictor for perceived productivity |
| Vaithilingam et al. [59] | Experiment with 24 developers | Does not improve task completion time and success rate; developers prefer Copilot because it "recommends code that can be used as a starting point and saves the effort of searching online" |
| Nguyen and Nadi [43] | LeetCode questions, multiple languages; correctness via LeetCode test cases, understandability via Cyclomatic Complexity and Cognitive Complexity [13] | Correctness between 57% (Java) and 27% (JavaScript); low complexity for all programming languages |

Scope distinction stated in chunk:

> "While we also measure the effectiveness of the solutions suggested by Copilot, our main focus is on understanding its robustness when different inputs are provided."

## Conclusions and future work
**Covers:** chunk section "VI. Conclusions and Future Work"

> "We investigated the extent to which DL-based code recommenders tend to synthesize different code components when starting from different but semantically equivalent natural language descriptions."

Method restated in conclusions:

- Selected GitHub Copilot as the tool representative of the state-of-the-art.
- Asked it to generate 892 non-trivial Java methods starting from natural language descriptions.
- For each method used: (i) the original description, extracted as the first sentence in the Javadoc; and (ii) paraphrased descriptions, both manually modified and via automated paraphrasing tools after assessing their reliability.

Main results (verbatim):

> "We found that in ~46% of cases semantically equivalent but different method descriptions result in different code recommendations."

> "We observed that some correct recommendations can only be obtained using one of the semantically equivalent descriptions as input."

Implication (verbatim):

> "Our results highlight the importance of providing a proper code description when asking DL-based recommenders to synthesize code."

> "In the new era of AI-supported programming, developers must learn how to properly describe the code components they are looking for to maximize the effectiveness of the AI support."

Future work:

- Answer the first research question in vivo rather than in silico via a controlled experiment with developers to assess the impact of the different code descriptions they write on the received recommendations.
- Investigate how to customize the automatic paraphrasing techniques to further improve their performance on software-related text (such as methods' descriptions).

Supporting notes in chunk: funding from the European Research Council (ERC) under the European Union's Horizon 2020 research and innovation programme (grant agreement No. 851720); replication package at https://github.com/antonio-mastropaolo/robustness-copilot.
**Covers:** chunk 07-github-copilot-has-been-recently-introduced.md (related work on Copilot, conclusions/future work, acknowledgments/references)
