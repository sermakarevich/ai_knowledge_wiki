[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Data Analysis: Levenshtein Distance and CodeBLEU
**In one sentence:** The study filters paraphrases to semantically equivalent ones for RQ0/RQ1, quantifies description change with normalized token-level Levenshtein distance and code similarity with CodeBLEU plus code-level Levenshtein distance, and publishes all data and scripts in a replication package.
## Key points
- For RQ0, the authors report the number and percentage of the 892 automatically generated paraphrases (PEGASUS and TP) classified as semantically equivalent, and exclude non-equivalent ones from RQ1.
- For RQ1, description distance is measured as normalized token-level Levenshtein distance `NTLev(do, dp) = TLev(do, dp) / max({|do|, |dp|})`, where `TLev` is the token-level Levenshtein distance between original and paraphrased descriptions.
- Synthesized-vs-target code similarity is measured with Levenshtein distance and CodeBLEU [49], where CodeBLEU considers overlapping n-grams plus syntactic and semantic match, unlike BLEU [46].
- The replication package [6] provides six artifacts: manually defined and automatically generated paraphrases, AppleScript for Copilot triggering, CodeBLEU/Levenshtein code, 892 methods plus tests, PEGASUS/TP generation scripts, and all raw outputs.
- In the chunk's RQ0 spillover, PEGASUS yields 666 (74.7%) equivalent / 225 (25.2%) non-equivalent / 1 (0.1%) invalid and TP yields 688 (77.1%) / 104 (11.7%) / 100 (11.2%) out of 892, with TP at ~87% correct when invalid outputs are excluded.
- Full-context and Non-full-context results are described as similar, so only Full-context results are discussed in the paper while Non-full-context results are left to the replication package [6].
---
## C. Data Analysis
**Covers:** C. Data Analysis (RQ0 reporting, NTLev definition, CodeBLEU/code-Levenshtein definition)

Concerning RQ0, the chunk states the authors report the number and percentage of the 892 methods for which automatically generated paraphrases (PEGASUS and TP) were classified as semantically equivalent to the original description. This is framed as showing how reliable these tools are for testing DL-based code generators and as allowing exclusion of non-equivalent paraphrases from RQ1.

To answer RQ1, description distance is defined as the percentage of changed words via normalized token-level Levenshtein distance [31] (NTLev) between the original (`do`) and any paraphrased description (`dp`):

```text
              TLev(do, dp)
NTLev(do, dp) = -----------------
                max({|do|, |dp|})
```

with `TLev` the token-level Levenshtein distance between the two descriptions.

Code similarity is measured with:

- "Levenshtein distance and the CodeBLEU [49] between each synthesized method and the target one (i.e., the one originally implemented by the developers)."
- "CodeBLEU measures how similar two methods are. Differently from the BLEU score [46], CodeBLEU evaluates the predicted code considering not only the overlapping n-grams but also syntactic and semantic match of the two pieces of code (predicted and reference) [49]."

## D. Replication Package
**Covers:** D. Replication Package (six listed artifacts)

Verbatim framing: "The code and data used in our study are publicly available [6]." The six items are:

| # | Artifact |
|---|---|
| (i) | dataset of manually defined and automatically generated paraphrases |
| (ii) | AppleScript code used to automate the Copilot triggering |
| (iii) | code used to compute the CodeBLEU and the Levenshtein distance |
| (iv) | dataset of 892 methods and related tests used in the study |
| (v) | scripts used to automatically generate the paraphrased descriptions using PEGASUS and TP |
| (vi) | all raw data output of the experiments |

## Results spillover present in this chunk
**Covers:** Opening of Results/Discussion through RQ0 counts (Full vs Non-full context note, Table II, Answer to RQ0)

- Context note: "in RQ1 we conducted our experiments both in the Full context and in the Non-full context scenario. Since the obtained findings are similar, due to space limitations we only discuss in the paper the results achieved in the Full context scenario (i.e., the case in which we provide Copilot with all code preceding and following the method object of the prediction). The results achieved in the Non-full context scenario are available in our replication package [6]."
- Table II as printed in the chunk ("Number of semantically equivalent or nonequivalent paraphrased descriptions obtained using PEGASUS and TP"):

| Technique | Equivalent | Nonequivalent | Invalid |
|---|---|---|---|
| PEGASUS | 666 (74.7%) | 225 (25.2%) | 1 (0.1%) |
| TP | 688 (77.1%) | 104 (11.7%) | 100 (11.2%) |

- Supporting text: "Out of the 892 original descriptions on which they have been run, PEGASUS generated 666 (75%) semantically equivalent descriptions, while TP went up to 688 (77%). If we do not consider the invalid paraphrases, i.e., the cases for which the techniques do not actually provide any paraphrase, the latter obtains ~87% of correctly generated paraphrases."
- Testing-tool claim: "These findings suggest that the two paraphrasing techniques can be adopted as testing tools to assess the robustness of DL-based code recommenders. In particular, once established a reference description (e.g., the original description in our study), these tools can be applied to paraphrase it and verify whether, using the reference and the paraphrased descriptions, the code recommenders generate different predictions."
- Verbatim answer box: "Answer to RQ0. State-of-the-art paraphrasing techniques can be used as starting point to test the robustness of DL-based code recommenders, since they are able to generate semantically equivalent descriptions of a reference text in up to 77% of cases."
