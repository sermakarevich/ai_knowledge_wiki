[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Threats to Validity and Conclusion
**In one sentence:** The authors set aside internal validity, mitigate manual-coding bias, limited generalizability from two data sources, and replication risk through multi-author agreement (pilot Cohen's Kappa 0.773) and an open dataset, and conclude from 303 SO posts and 927 GitHub discussions that Copilot is used mainly with JavaScript/Python, VS Code, and Node.js for data processing and code generation, valued for useful code integration but limited by difficulty of integration, with support for more IDEs the most expected feature.
## Key points
- Internal validity is explicitly not considered because the study "did not investigate the relationships between variables and results"; only three threats are discussed per the guidelines in [16].
- Construct validity threat comes from manual data labelling, extraction, and analysis ("may lead to personal bias"), countered by pilot labelling to reach author agreement, two-author extraction/analysis, a full recheck by the first author of the third author's results, and continuous consultation with the second author.
- External validity is only partially alleviated by using two popular communities — SO (widely used in software engineering studies) and GitHub Discussions (a new GitHub feature for specific topics [17]) — while the authors admit the sources "may not be representative enough" for all Copilot practices, challenges, and expected features.
- Reliability shows a pilot Cohen's Kappa of 0.773 ("a decent consistency") between two authors, but the authors acknowledge residual risk from "the small number of posts used in the pilot" and from three-author manual work resolved by discussion "until there was no any disagreements".
- Replicability is supported by publishing the full dataset of extracted data and labelling results from SO posts and GitHub discussions online for validation and replication [24].
- Conclusions rest on 303 SO posts (search term "copilot") plus 927 GitHub discussions under the "Copilot" category, yielding eight main results: JavaScript/Python top languages, VS Code dominant IDE, Node.js major technology, data processing main function, code generation leading purpose, useful code integration top benefit, difficulty of integration top limitation/challenge, and integration with more IDEs top expected feature.
- Next steps are interviews or an online survey to supplement repository mining and further work on improving developer understanding of generated code (see Section 5); the work was supported by NSFC Grant No. 62172311 and the Special Fund of Hubei Luojia Laboratory.
---
## Construct validity
**Covers:** Section 6, paragraph 2

> "Construct validity indicates whether the theoretical and conceptual constructs are correctly measured and interpreted."

- Source of threat: "We conducted data labelling, extraction, and analysis manually, which may lead to personal bias."
- Mitigations stated: "the data labelling of SO posts was performed after the pilot labelling to reach an agreement between the authors"; "data extraction and analysis was also conducted by two authors, and the first author rechecked all the results produced by the third author"; "the first author continuously consulted with the second author to ensure there are no divergences."

## External validity
**Covers:** Section 6, paragraph 3

> "External validity indicates the the degree of generalization of the study results, i.e., the extent to which the results can be generalized to other contexts."

- Choice: "We chose two popular developer communities (SO and GitHub Discussions) because SO has been widely used in software engineering studies and GitHub Discussions is a new feature of GitHub for discussing specific topics [17]."
- Claimed effect: "These two data sources can partially alleviate the threat to external validity."
- Residual limitation: "we admit that our selected data sources may not be representative enough to understand all the practices, challenges, and expected features of using Copilot."

## Reliability
**Covers:** Section 6, paragraph 4

> "Reliability indicates the replicability of a study yielding the same or similar results."

- Pilot: "conducted a pilot labelling before the formal labelling of SO posts with two authors, and the Cohen's Kappa coefficient is 0.773, indicating a decent consistency."
- Residual threat: "We acknowledge that this threat might still exist due to the small number of posts used in the pilot."
- Process: "All the steps in our study, including manual labelling, extraction, and analysis of data were conducted by three authors"; "the three authors discussed the results until there was no any disagreements in order to produce consistent results."
- Artifact: "the dataset of this study that contains all the extracted data and labelling results from the SO posts and GitHub discussions has been provided online for validation and replication purposes [24]."

## Conclusions
**Covers:** Section 7, paragraphs 1–2

- Design: "We conducted an empirical study on SO and GitHub discussions"; "used 'copilot' as the search term to collect data from SO and collected all the discussions under the 'Copilot' category in GitHub discussions"; "Finally, we got 303 SO posts and 927 GitHub discussions related to Copilot."
- Scope of results: "identified the programming languages, IDEs, technologies used with Copilot, functions implemented by Copilot, and the benefits, limitations, and challenges of using Copilot, which are first-hand information for developers."
- Eight main results quoted: "(1) JavaScript and Python are the most frequently discussed programming languages by developers with Copilot. (2) Visual Studio Code is the dominant IDE used with Copilot. (3) Node.js is the major technology used with Copilot. (4) Data processing is the main function implemented by Copilot. (5) To help generate code is the leading purpose of users using Copilot. (6) Useful code integration is the most common benefit mentioned by developers when using Copilot. (7) Difficulty of integration is the most frequently encountered limitations and challenges when developers use Copilot. (8) Copilot can be integrated with more IDEs is the most expected feature of users."

## Future work and acknowledgements
**Covers:** Section 7, paragraph 3 and Acknowledgements

- "In the next step, we plan to explore the practices of using Copilot by conducting interviews or an online survey to get practitioners' perspectives on using Copilot, which can supplement our existing data collected from repository mining."
- "we also plan to further explore various aspects of Copilot, especially how to improve the understanding of developers on the generated code (see Section 5)."
- "This work has been supported by the Natural Science Foundation of China (NSFC) under Grant No. 62172311 and the Special Fund of Hubei Luojia Laboratory."
