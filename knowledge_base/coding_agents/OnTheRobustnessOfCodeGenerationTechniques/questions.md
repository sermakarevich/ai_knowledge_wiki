---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: On the Robustness of Code Generation Techniques:

### Q1. What robustness question does the paper pose about GitHub Copilot, and why is the developer's "proper" input central?

> [!tip]- Answer
> The paper asks whether Copilot-style generators are robust to wording, i.e. whether semantically equivalent descriptions yield different code recommendations. The abstract framing is that the developer's ability to provide "proper" inputs becomes central to boosting recommendation effectiveness. It studies this with GitHub Copilot as the concrete example. See [[wiki/01-overview-and-research-questions|On the Robustness of Code Generation]].

### Q2. What are RQ0 and RQ1, and how was the 892-method context selected?

> [!tip]- Answer
> RQ0 asks to what extent automated paraphrasing techniques can be used to test the robustness of DL-based code generators. RQ1 asks to what extent Copilot's output is influenced by the developer-provided code description. The context is 892 Java methods from 33 repositories, filtered from 1,401 repos by ≥300 commits, 50 contributors, 25 stars, Maven build success, jUnit plus JaCoCo dependencies, ≥75% statement coverage, and a Javadoc first-sentence of ≥10 tokens. See [[wiki/02-study-design-and-data-collection|Study Design and Data Collection]].

### Q3. How did the study generate paraphrases and invoke Copilot in Full versus Non-full context?

> [!tip]- Answer
> Per method it used up to three paraphrases: PEGASUS, Translation Pivoting (English→French→English), and a manual rewrite by one of four authors, totaling up to 2,575 semantically equivalent paraphrases. Copilot was invoked by emptying the target method body to `{}` and replacing the Doc Comment with one description, in Full context (code before plus after) and Non-full context (only preceding code), via AppleScript driving VS Code with up to a 20 s wait while keeping only the first Java-Parser-valid method. See [[wiki/02-study-design-and-data-collection|Study Design and Data Collection]].

### Q4. How are description change and code similarity quantified (NTLev, CodeBLEU, Levenshtein)?

> [!tip]- Answer
> Description distance is the normalized token-level Levenshtein distance `NTLev(do, dp) = TLev(do, dp) / max({|do|, |dp|})`, i.e. the share of changed words between original and paraphrased descriptions. Code similarity between each synthesized method and the developer-written target is measured with Levenshtein distance and CodeBLEU, where CodeBLEU considers overlapping n-grams plus syntactic and semantic match, unlike BLEU. Passing tests on high-coverage methods (median 100%) complement these metrics as a proxy for correctness. See [[wiki/03-data-analysis-metrics|Data Analysis: Levenshtein Distance and CodeBLEU]].

### Q5. What did RQ0 find about PEGASUS versus Translation Pivoting, and what does the replication package contain?

> [!tip]- Answer
> Of 892 descriptions, PEGASUS produced 666 (74.7%) equivalent, 225 (25.2%) non-equivalent, and 1 (0.1%) invalid, while Translation Pivoting produced 688 (77.1%) equivalent, 104 (11.7%) non-equivalent, and 100 (11.2%) invalid, reaching ~87% correct when invalids are excluded. The authors conclude both paraphrasers can serve as starting-point robustness probes after filtering out non-equivalent outputs. The replication package provides the manual and automatic paraphrases, AppleScript trigger code, CodeBLEU/Levenshtein code, the 892 methods plus tests, PEGASUS/TP scripts, and all raw outputs. See [[wiki/03-data-analysis-metrics|Data Analysis: Levenshtein Distance and CodeBLEU]].

### Q6. How do the Fig. 4 examples show passing tests despite low textual similarity?

> [!tip]- Answer
> Fig. 4 reports a recommended method with CodeBLEU 0.45 versus the oracle that still passes unit tests. The `removeListener` recommendation keeps the null check but simplifies the body to `lazyChemObjectListeners().remove(col)`, which is functionally equivalent since `List.remove` checks containment. The `translateAllPositive` recommendation likewise passes while restructuring minima initialization, looping, and point shifting relative to the oracle. See [[wiki/04-illustrative-examples|Illustrative Examples: Recommended Methods That Pass Tests Despite Low CodeBLEU]].

### Q7. What is the relationship between CodeBLEU/Levenshtein similarity and test outcomes, and why are both evaluators imperfect?

> [!tip]- Answer
> Test-passing methods have median CodeBLEU ~0.80 (Levenshtein ~0.10) versus ~0.40 (~0.58) for test-failing methods, yet 25% of passing methods score CodeBLEU <0.50 and 25% of failing predictions score >~0.60. The Fig. 4 case (0.45, passing, equivalent logic) shows similarity metrics can wrongly mark valuable recommendations as failures. The Fig. 5 case (165 token edits, NTLev 63%, passing but treating 3D as well as 2D points) shows tests can also miss real behavioral differences. See [[wiki/05-results-codebleu-and-tests|CodeBLEU Scores, Test Outcomes, and Paraphrasing Impact]].

### Q8. What happens when the input description is paraphrased: how often does the recommendation change, and what correct answers are lost or gained?

> [!tip]- Answer
> Of 892 manual paraphrases, 408 (46%) yield different code than the original description, with PEGASUS (327) and TP (328) confirming the pattern and a median ~30% of code tokens changed. Of 112 test-passing predictions from original descriptions and 122 from paraphrased ones, only 98 overlap, leaving 38 correct recommendations obtainable only one way (14 original-only, 24 paraphrase-only). Manual paraphrases changed >70% of words in half the cases, so even large wording differences that preserve meaning shift the output. See [[wiki/05-results-codebleu-and-tests|CodeBLEU Scores, Test Outcomes, and Paraphrasing Impact]].

### Q9. What limits generalization of the findings, and how does prior work contextualize them?

> [!tip]- Answer
> The claim is deliberately about differences across paraphrases rather than absolute performance, since the 892 open-source methods may have been in Copilot's training data. Generalization is limited to Java high-coverage methods with verbose Javadoc first-sentences produced via a custom Copilot-invocation toolchain, so larger and multi-language replications are needed. This matches prior findings that synthetic benchmarks overstate accuracy (Proksch et al., Hellendoorn et al.) and that block-level generation is far harder than few-token completion (~29% vs ~69% in Ciniselli et al.). See [[wiki/06-discussion|Discussion, Threats to Validity, and Related Work]].

### Q10. Given that ~46% of equivalent descriptions change the recommendation and some correct answers are obtainable only one way, what should developers and teams do when using Copilot?

> [!tip]- Answer
> Developers should treat the description as a first-class input: write careful, precise Javadoc-style descriptions and retry with a reworded equivalent description when the first recommendation fails, since wording alone can recover otherwise lost correct solutions. Teams should not accept untested suggestions at face value but validate with tests plus review, because similarity scores and even passing tests can misjudge behavioral equivalence. This reword-and-verify habit directly follows from the study's implication that developers must learn to describe wanted code properly. See [[wiki/07-implications-conclusions|Related Work, Conclusions and Future Work]].
