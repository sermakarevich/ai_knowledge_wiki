> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Study Design and Data Collection
**In one sentence:** The study tests Copilot robustness on 892 Java methods by feeding it original Javadoc first-sentences versus semantically equivalent paraphrases (PEGASUS, Translation Pivoting, and manual) under Full and Non-full code context via automated VS Code invocations.
## Key points
- Study asks RQ0 (can automated paraphrasing test DL-based generator robustness?) and RQ1 (does Copilot output change with semantically equivalent descriptions?).
- Context: 892 Java methods from 33 repositories, selected from 1,401 repos filtered by ≥300 commits, 50 contributors, 25 stars, Maven build success, jUnit + JaCoCo dependencies, ≥75% statement coverage, Javadoc first-sentence ≥10 tokens.
- Original description is defined as the first sentence of the method's Doc Comment (up to the first "."), following prior Java summarization datasets.
- RQ0 pilots two paraphrasers: PEGASUS (sequence-to-sequence DL model for abstractive summarization, fine-tuned for paraphrasing) and Translation Pivoting (English→French→English heuristic); TP failed to produce a distinct paraphrase in 100/892 cases vs 1/892 for PEGASUS.
- RQ1 uses up to three paraphrases per method (PEGASUS, TP, manual by four authors), max 2,575 semantically equivalent paraphrases (up to 891 PEGASUS + 792 TP + 892 manual) after excluding generation failures and non-equivalent outputs.
- Copilot is invoked by emptying the target method body to `{}` and replacing the Doc Comment with one description, in two scenarios: Full context (code before + after) and Non-full context (only preceding code), up to 6,934 total invocations (892 originals + up to 2,575 paraphrases × 2).
- Automation uses AppleScript on a MacBook Pro driving VS Code (open file, cursor in braces, press return, wait up to 20 s), keeping only the first valid method extracted via Java Parser from each recommendation.
---
## Research questions
**Covers:** Section II, RQ0–RQ1

> "RQ0 : To what extent can automated paraphrasing techniques be used to test the robustness of DL-based code generators? Not always natural language processing techniques can be used out of the box on software-related text [35]."

> "RQ1 : To what extent is the output of GitHub Copilot influenced by the code description provided as input by the developer?"

RQ1 specifically asks whether Copilot generates different recommendations for different semantically equivalent natural language descriptions.

## Context selection
**Covers:** Section II-A, 892 Java methods

Selection pipeline stated in chunk:

- Start: all GitHub Java repositories with at least 300 commits, 50 contributors, and 25 stars → 1,401 repositories (forks excluded; GitHub search tool by Dabic et al.).
- Keep Maven projects whose latest release builds, with jUnit and JaCoCo (POM-declared) → 214 repositories.
- Keep methods with at least 75% statement coverage (JaCoCo reports), having a Javadoc Doc Comment whose first sentence has ≥10 tokens.

Result: 892 Java methods from 33 repositories.

| Metric (Table I) | Avg | Median | St. Dev. |
|---|---|---|---|
| # Tokens | 154.3 | 92.0 | 218.2 |
| # Parameters | 1.6 | 1.0 | 1.2 |
| # Cyclomatic Complexity | 5.3 | 3.0 | 7.6 |
| % Coverage | 96.1 | 100.0 | 6.7 |

The chunk notes coverage is high by design, and that passing tests are used as a proxy for correctness ("passing tests does not imply correctness").

## Data collection: paraphrases (RQ0 setup)
**Covers:** Section II-B, PEGASUS and Translation Pivoting

- PEGASUS [66]: sequence-to-sequence DL model pre-trained with self-supervised objectives for abstractive summarization and fine-tuned for paraphrasing [5].
- Translation Pivoting (TP): heuristic translating original English description to French and back to English to obtain a paraphrase.
- Validity check: of 1,683 paraphrases (892 per tool minus 101 invalid/distinct-failures), each was independently inspected by two authors as semantically equivalent or not; conflicts (11.9% PEGASUS, 16.54% TP) resolved by a third author.

## Data collection: Copilot invocations (RQ1 setup)
**Covers:** Section II-B, Full vs Non-full context, Fig. 1

- Manual paraphrases: 892 methods split into four sets, one author each, writing a semantically equivalent but different description from code + original description; available for all methods.
- Per-method files: up to four Java file versions (original + paraphrasedPEGASUS + paraphrasedTP + paraphrasedmanual), each with emptied method body and Doc Comment replaced by one description.
- Fig. 1 example (Hook/getEmbeddings/hasContent): Full context provides code preceding and following the emptied method (developer adding a method to an existing file); Non-full context provides only preceding code (developer writing sequentially).
- No open Copilot API at study time, so invocation went through the VS Code plugin automated with AppleScript; recommendation could be empty or contain extra methods, so only the first valid method (Java Parser method node) is kept.

**Covers:** Section II (Study Design) through Section II-B data collection; headline results (~46% changed recommendations) belong to later results pages, not this chunk.
