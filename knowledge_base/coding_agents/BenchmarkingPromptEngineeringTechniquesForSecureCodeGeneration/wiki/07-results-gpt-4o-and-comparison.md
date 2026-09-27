> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# GPT-4o Results and Cross-Model Comparison
**In one sentence:** On GPT-4o every tested prompt technique reduced vulnerabilities versus baseline, with the pe-03-a prefix best among single prompts at 56% reduction and RCI best overall at up to 68.7%, and cross-model comparison shows more advanced models are more sensitive to prompt alterations while RCI works for all models but improves most on the advanced ones.
## Key points
- Only a subset of attempts was run on GPT-4o due to higher LLM cost, selecting the most interesting attempts from Table I.
- All tested prompt engineering attempts on GPT-4o reduced vulnerability risk versus the 7.43% baseline, with single-prompt prefix pe-03-a most effective at 3.27% (−56.0% relative difference).
- RCI on GPT-4o baseline snippets cut vulnerabilities by 64.7% (2.62%), and RCI applied to pe-03-a snippets improved from 56% to 68.7% fewer vulnerabilities (2.33%) versus the original baseline.
- The adversarial pe-negative prompt raised GPT-4o vulnerabilities to 18.76%, 152.7% above baseline, showing the strongest intentional-vulnerability effect among models.
- Cross-model comparison (Figure 6) shows increasing sensitivity to prompt alterations for more advanced models: generic modifications had no positive impact on GPT-3.5-turbo, while GPT-4o-mini and especially GPT-4o improved significantly.
- The most effective simple (single-prompt) technique was the prefix "You are a developer who is very security-aware and avoids weaknesses in the code".
- GPT-3.5-turbo had the most secure baseline, possibly due to incomplete code indicated by lower average AST height, aligning with Bhatt et al. [11]'s "Negative correlation between insecure code test case pass rate and code quality" thesis.
- RCI gave the best improvement and benefits from combining proactive prevention (pe-03-a) with iterative refinement, but has higher cost/time from multiple large calls and shows diminishing returns (already seen by the third iteration on GPT-4o-mini).
---
## GPT-4o results (Table IV)
**Covers:** Section C. GPT-4o / Table IV / Figure 5

Only a subset of the attempts from Table I were executed with GPT-4o:

> "Only a subset of the attempts from Table I were executed with GPT-4o. This was mainly due to the higher costs of using this LLM. We decided to run the most interesting attempts."

> "All of the tested prompt engineering attempts were successful in reducing the risk of vulnerabilities compared to the baseline."

| ID | Filtered Vuln. Sample (%) (a) | diff (%) (b) | Vuln. per Sample (c) |
|---|---|---|---|
| rci-from-pe-03-a-iter-1 | 2.33 | +68.7 | 0.43 |
| rci-from-baseline-iter-1 | 2.62 | +64.7 | 0.40 |
| pe-03-a | 3.27 | +56.0 | 1.09 |
| pe-02-a | 3.61 | +51.3 | 1.06 |
| pe-01-b | 3.96 | +46.7 | 1.05 |
| pe-01-c | 4.21 | +43.3 | 0.82 |
| pe-02-b | 4.50 | +39.3 | 1.10 |
| pe-01-a | 4.80 | +35.3 | 1.07 |
| baseline | 7.43 | +0.0 | 1.27 |
| pe-negative | 18.76 | −152.7 | 1.57 |

Table notes (verbatim): "a Scanners Agree Filtered Vulnerable Samples (average of OFVP)", "b Relative Difference to Baseline Attempt (higher is better)", "c Scanners Combined Average Vulnerabilities per Sample (unfiltered)".

Key verbatim claims:

> "Among the single-prompt attempts, the prompt-prefix technique "pe-03-a" was the most effective with a 56% reduction."

> "RCI reduced vulnerabilities in the baseline code snippets by 64.7% while employing RCI on the snippets from "pe-03-a" resulted in an additional improvement from 56% to 68.7% fewer vulnerabilities compared to the original baseline snippets."

> "When prompting the model to create vulnerable code in the "pe-negative" approach, the "Scanners Agree Filtered Vulnerable Samples" metric was 152.7% above baseline."

Figure 5 is the box plot "Vulnerability Distribution per Attempt GPT-4o" over "Observed Vulnerability Percentages (OFVP)" (0–20).

## Performance comparison across LLMs (Discussion V.A, Figure 6)
**Covers:** V. Discussion / A. Performance Comparison / Figure 6

> "To compare the results of the three LLMs with each other, we illustrated the "Scanners Agree Filtered Vulnerable Samples" for each attempt and each LLM in a bar chart in Figure 6."

> "The results show an increasing sensitivity to prompt alterations for more advanced models."

> "While generic prompt modifications had no positive impact on GPT-3.5-turbo regarding code security, the more recent GPT-4o-mini model generated significantly more secure code with our prompt additions. We observed the biggest effect on the large GPT-4o model."

> "The same is true for the model's ability to introduce vulnerabilities on purpose with our "pe-negative" adversary attempt where GPT-4o showed the best ability."

> "Of the simple techniques, which do not require sending additional prompts to the LLM, the prefix "You are a developer who is very security-aware and avoids weaknesses in the code" was the most effective in reducing the risk of vulnerable code."

> "While the RCI technique, which refines the code with additional prompts, was successful for all models, including GPT-3.5-turbo, its effectiveness increased significantly with the more advanced models."

> "Interestingly, GPT-3.5-turbo had the most secure baseline. The lower average AST height indicates that this might be due to incomplete code."

Supporting citation context (verbatim): Bhatt et al. [11] found a "Negative correlation between insecure code test case pass rate and code quality" and proposed the thesis that "Models that are more capable at coding tend to be more prone to insecure code suggestions".

RCI summary and cost (verbatim claims):

> "In summary, we can say that RCI provided the best improvement. It was able to improve the code with additional iterations. However, this will not work indefinitely; we already observed diminishing improvements by the third iteration on GPT-4o-mini."

> "RCI does have the disadvantage of considerably higher costs due to multiple calls with large inputs and outputs. It is also time-consuming to make multiple calls."

> "Combining RCI and an attempt like "pe-03-a" could boost the results and reduce the number of necessary iterations, reducing cost and time. This approach combines proactive vulnerability prevention in the initial code generation with iterative improvements in code security."

Figure 6 header (truncated in chunk): GPT-3.5-turbo / GPT-4o-mini / GPT-4o.

## Sample size (Discussion V.B)
**Covers:** B. Sample Size

> "Figure 3, Figure 4 and Figure 5 also highlight the inherent variability in LLM-generated output, which necessitates generating multiple samples for robust evaluation."

> "Code generation can vary significantly across different executions, even with identical prompts on the same model."

Baseline sample-size experiment: compared security assessment outcomes from sets of 10 and 100 samples per prompt; "While some fluctuations were observed, increasing the sample size to 100 did not result in substantial shifts in the distribution's central tendencies (i.e., average, median, and quartiles) when compared to the results from 10 samples."

> "Given these observations, 10 samples may offer a reasonable balance between computational efficiency and statistical reliability for this specific evaluation. However, it is important to acknowledge that larger sample sizes could reveal additional insights."

## Functionality check with HumanEval (Discussion V.C, Table V)
**Covers:** C. Functionality / Table V

Method (verbatim steps): converted HumanEval [19] prompts to the internal dataset format to reuse the benchmark tool from section III for augmentation, generation, and extraction; added the prefix "Complete the following code, and output the complete program:\n" to all prompts prior to regular augmentation; converted the extracted-code data file to the HumanEval framework format and ran its evaluation scripts. Only four attempts on GPT-4o-mini with the usual sample size of 10 were tested since this was not the main focus.

| Attempt | pass@1 | pass@10 |
|---|---|---|
| baseline | 86.77% | 95.12% |
| pe-03-a | 86.65% | 94.51% |
| ptfscg rci-from-pe-03-a-iteration-1 | 76.89% | 93.90% |
| ptfscg rci-from-baseline-iteration-1 | 76.65% | 94.51% |

> "The results of the HumanEval samples show very similar values for pass@10. The pass@1 values dropped about 10% for both RCI attempts. This might be due to the LLM trying to make the code more secure."

> "The default sample size for HumanEval is 200, indicating that 10 samples might not be enough to get accurate numbers. Still, these numbers are a good first indication. As this was out of scope for our project we did not investigate the matter further."

> "It is worth mentioning that neither of our scanners detected any vulnerabilities in the generated code for HumanEval." (chunk truncates the following clause: "This might be because the tasks are not designed to provoke any...")

**Covers:** Chunk 07-e-0-e-c-f-a (Tables III tail/IV/V; Figures 5–6 headers; sections C. GPT-4o and V.A–V.C); OCR garbled, figure values taken from tables and prose only.
