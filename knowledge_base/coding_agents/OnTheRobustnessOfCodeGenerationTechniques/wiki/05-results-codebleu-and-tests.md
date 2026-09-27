> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# CodeBLEU Scores, Test Outcomes, and Paraphrasing Impact

**In one sentence:** Test-passing methods have much higher CodeBLEU similarity to targets (median ~0.80 vs ~0.40) yet 25% of passing methods score <0.50 and 25% of failing methods score >~0.60, while 408/892 (46%) manual paraphrases change the recommendation and cost correct predictions, showing both similarity metrics and testing are imperfect evaluators.

## Key points

- Test-passing methods have median CodeBLEU ~0.80 (Levenshtein ~0.10) versus ~0.40 (Levenshtein ~0.58) for test-failing methods, across all/failing/passing distributions.
- 25% of test-passing methods have CodeBLEU <0.50, and 25% of test-failing predictions have CodeBLEU >~0.60, so high similarity does not guarantee passing tests nor low similarity failing tests.
- Fig. 4 example (CodeBLEU 0.45, tests pass): the recommended method captures the target's basic logic but avoids the second `if` by calling `remove` directly after the null check, which is functionally equivalent since `java.util.List.remove` preliminarily checks containment.
- Fig. 5 example (165 token-level edits, NTLev=63%, tests pass): the recommended method also treats 3D points while the original treats only 2D points, so behavior differs and the tests fail to capture the difference.
- Of 892 manually paraphrased descriptions, 408 (46%) yield different code than the original description; of 112 test-passing predictions (original) and 122 (paraphrased), only 98 overlap, leaving 38 correct recommendations obtainable only one way (14 original-only, 24 paraphrase-only).
- Manual paraphrases differ from originals by >70% of words in 50% of cases, and the 408 changed code pairs differ by a median of ~30% of code tokens; PEGASUS and TP automatic paraphrases confirm the pattern, with TP changing substantially fewer description words because it only translates English-to-French-and-back.
- Construct threats: passing tests are used as a proxy for correctness on high-coverage methods (median statement coverage 100%), complemented by CodeBLEU and normalized token-level Levenshtein distance, while automated whole-recommendation acceptance cannot simulate selective developer reuse.

---

## CodeBLEU and Levenshtein vs test outcomes

CodeBLEU [49] is "computed between the recommended methods and the target one (i.e., the one implemented by the original developers). Higher values indicate higher similarity between the compared methods. Instead, in the right box plot, we show the normalized Levenshtein distance, for which lower values indicate higher similarity."

| Group | Median CodeBLEU | Median Levenshtein |
|---|---|---|
| Test-passing methods | ~0.80 | ~0.10 |
| Test-failing methods | ~0.40 | ~0.58 |

> "As expected, higher (lower) values of CodeBLEU (Levenshtein distance) are associated with test-passing methods."

> "it is interesting to notice that 25% of test-passing methods have a rather low CodeBLEU <0.50."

> "25% of test-failing predictions exhibit high values (>~0.60) of CodeBLEU, indicating a high code similarity that, however, does not reflect in test-passing recommendations."

**Covers:** CodeBLEU/Levenshtein distributions for all vs failing vs passing predictions

## Fig. 4: low CodeBLEU but passing and equivalent

> "Fig. 4 shows an example of recommended method having a CodeBLEU with the target method of 0.45 and passing the related tests. The recommended method, while substantially different from the target, captures the basic logic implemented in it."

Target logic: "first checks if the object chemObjectListeners is null and, if not, it proceeds removing from the listeners list the element matching the one provided as parameter (i.e., col). The method synthesized by Copilot avoids the second if statement by directly performing the remove operation after the null check."

> "Note that there the two implementations are equivalent: The remove method of java.util.List preliminarily checks whether the passed element is contained in the list before removing it."

> "While the check in the original method has no functional role, together with the introduction of the listeners variable, it might have been introduced to make the method more readable and self-explanatory."

**Covers:** Fig. 4 equivalent-implementation example

## Fig. 5: passing tests but different behavior

> "Fig. 5. Example of recommended methods that pass the unit tests but would require 165 edit actions to match the target method."

> "Levenshtein distance: 165"

> "Fig. 5 shows an example of prediction passing the tests but that, accordingly to the Levenshtein distance, would require 165 token-level edits to match the target prediction (NTLev=63%)."

> "it is clear that, in this case, the two methods do not have the same behavior since the recommended one also treats 3D points, while the original one only 2D points. In other words, the tests fail to capture the difference in the behavior."

Two observations drawn:

> "metrics such as CodeBLEU and Levenshtein distance may result in substantially wrong assessments of the quality of a prediction. Indeed, while the discussed predictions have low CodeBLEU/high Levenshtein values and, thus, would be considered as unsuccessful predictions in most of the empirical evaluations, it is clear that they are valuable recommendations for a developer, even when not 100% correct (see Fig. 5)."

> "also the testing-based evaluation shows, as expected, some limitations as in the second example, in which the two methods do not implement the same behavior but both pass the tests."

**Covers:** Fig. 5 divergent-behavior example; metric and testing limitations

## Impact of paraphrasing the input descriptions

| Paraphrase set | Changed recommendations |
|---|---|
| Manual (892 descriptions) | 408 (46%) different from original-description output |
| PEGASUS (666 descriptions) | 327 resulted in changes |
| TP/back-translation (688 descriptions) | 328 resulted in changes |

> "Out of the 892 manually paraphrased descriptions, 408 (46%) result in different code recommendations as compared to the original description."

> "out of the 112 test-passing predictions obtained with the original description and the 122 obtained with the manually paraphrased description, only 98 are in overlap, indicating that there are 38 correct recommendations only generated either by the original (14) or the paraphrased (24) description."

Fig. 6 (manual, light blue, left): "Description" boxplot = "the percentage of words that must be changed to convert the paraphrased description into the original one"; "Code" boxplot = original-description method vs paraphrased-description method.

> "the paraphrased descriptions can be substantially different as compared to the original ones, with 50% of them requiring changes to more than 70% of their words."

> "the different methods recommended in the 408 cases under analysis, can be substantially different, with a median of ~30% of code tokens that must be changed to convert the recommendation obtained with the original description into the one obtained using the paraphrased description."

Automatic paraphrases (PEGASUS middle, TP right of Fig. 6) confirm the findings; "the main difference ... is that TP changes a substantially lower number of words in the original description as compared to PEGASUS and to the manual paraphrasing" because "TP just translates the original description back and forth from English to French, thus rarely adding new words to the sentence."

Answer to RQ1 (verbatim):

> "Answer to RQ1. Different (but semantically equivalent) natural language descriptions of the same method are likely to result in different code recommendations generated by DL-based code generation models. Such differences can result in a loss of correct recommendations (~28% of test-passing methods can only be obtained either with the original or the paraphrased descriptions)."

**Covers:** manual + PEGASUS/TP paraphrase impact; Fig. 6; Answer to RQ1

## Threats to validity (as stated in chunk)

Construct: "we exploit the passing tests as a proxy for the correctness of the recommendations generated by Copilot. We acknowledge that passing tests does not imply code correctness. However, this it can provide hints about the code behavior. To partially address this threat we focused our study on methods having high statement coverage (median = 100%). Also, we complemented this analysis with the CodeBLEU and the normalized token-level Levenshtein distance."

Execution: "we automatically invoked Copilot rather than using it as actual developers would do: We automatically accepted the whole recommendations and did not simulate a scenario in which a developer selects only parts of the provided recommendations."

Internal: RQ2 paraphrase equivalence checked by multiple authors, but "in RQ1 we relied on a single author to paraphrase the original description" (subjectivity bias; mitigated by Java experience averaging seven years); original descriptions are first sentences of Doc Comments which "may be of low quality and not representative," mitigated by similar effectiveness with manually written descriptions.

**Covers:** Section IV Threats to Validity (construct, execution, internal) as included in chunk

**Covers:** chunk 05-achieved-in-terms-of-codebleu-49.md (CodeBLEU/test results, Fig. 4–6, paraphrasing impact, Answer to RQ1, threats)
