[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# RQ4 Results Context and Validity Under Identical Conditions
**In one sentence:** Experiments run under identical server, hardware, and software setups still face internal, external, and construct validity limits, while related work and the conclusion position StarCoder2 as stronger than developers on implementation smells but weaker on complex design smells, with one-shot prompting improving quality.
## Key points
- Experiments used the same server with consistent hardware and software setups, so rerunning on a different server with comparable resources "should not significantly affect the results."
- StarCoder2 hallucination remains an internal-validity risk because apparently correct output may be logically or syntactically invalid, skewing unit-test pass rates and refactoring-effectiveness measures despite verification by tests and inspection.
- Random single-commit sampling limits internal validity: different project settings or commit subsets could change outcomes, and multi-commit refactorings are missed, potentially underestimating complexity or scope.
- Training-data isolation is incomplete: projects were chosen outside the StarCoder2 training dataset, but similar code patterns or practices could still be present and advantage the model.
- External validity is bounded to a limited set of open-source Java projects from the Apache dataset and to StarCoder2-15B-Instruct-v0.1, so results may not transfer to other languages, domains, LLMs, or versions, though the replication package is public and the evaluation is designed to be adaptable.
- Construct validity rests on code-smell reduction, code-quality-metric improvement, and unit-test pass rates, which may miss readability and performance, and on RMiner3.0, DesigniteJava, and Understand, where different tools "may get different results."
- Conclusion numbers: StarCoder2 achieves 43.36% implementation code-smell reduction versus 24.27% for developers, excels at systematic refactorings while developers handle context-dependent design smells better, and benefits significantly from one-shot prompting.
---
## Identical conditions
All experiments "were conducted under identical conditions across the same server, using consistent hardware and software setups." The chunk claims running on a different server "should not significantly affect the results, as long as comparable computational resources are used," which "mitigates the concern of hardware or server variability as a threat to internal validity."

## Threats to internal validity
- Model hallucination: "StarCoder2 may generate code that appears correct but is not logically or syntactically valid," which "could alter the accuracy of our results, particularly in evaluating unit test pass rates and refactoring effectiveness." Mitigation claimed: "verifying the output through unit test evaluations and inspecting for invalid code," but "hallucinations remain an inherent risk in LLM-generated code."
- Commit sampling: "a randomly selected set of representative commits," but "variations in the project settings or the choice of different subsets of commits could lead to differing outcomes."
- Single-commit scope: "Some of the refactorings might span multiple commits, however, our approach focuses on analyzing refactorings within a single commit," risking "missing refactorings that are spread over several commits, potentially underestimating the complexity or scope of certain changes."
- Training overlap: projects selected "not included in the StarCoder2 training dataset," yet "there is still a possibility that similar code patterns or practices could be present in the training set of the model, which might give the LLM an advantage."

## Threats to external validity
"Our experiments are conducted on a limited set of open-source Java projects from the Apache dataset. Therefore, the findings may not be directly applicable to projects in other programming languages or domains." Mitigation: "We make the replication package publicly available to allow other researchers to test across a more diverse set of projects and languages." Model scope: "based on the latest open-source version of StarCoder2-15B-Instruct-v0.1, as of the date of our study"; the "evaluation approach is designed to be adaptable" to future StarCoder2 versions and other vendors' LLMs, but "different LLMs or different versions of StarCoder may generate different results."

## Threat to construct validity
"We primarily rely on code smell reduction, code quality metrics improvement, and unit test pass rates as indicators of refactoring quality. However, these metrics may not fully capture all dimensions of code quality, such as readability and performance." Tooling: "We used Rminer3.0, DesigniteJava, and Understand to gather our metrics for analysis which are the best in the state of practices for Java, however different tools may get different results."

## Related work (§5)
The section categorizes work into "(1) code generation approaches before and after the rise of LLMs, (2) code refactoring using LLMs, and (3) prompt engineering and fine-tuning techniques to enhance LLM performance."

### 5.1 Code generation: pre-LLM and post-LLM
Pre-LLM work "primarily relied on rule-based systems and traditional program synthesis techniques" using "formal methods and predefined rules," limiting complex tasks. Examples: "DeepCoder [2]" synthesizing "from input-output pairs, but struggling with more complex scenarios," and "AlphaCode [23]" showing "remarkable improvements in generating functional code from natural language descriptions" for competitive programming. Post-LLM: "Codex [13]" generates "through natural language prompts" and was "evaluated for its ability to repair programs using test-based repair tools, showcasing strengths in code completion but also highlighting limitations in handling complex tasks due to a lack of semantic understanding." "Xu et al. [51]" systematically evaluate models like Codex, emphasizing "strengths ... in automating code generation and refactoring tasks, while also pointing out the limitations ... in understanding deeper program semantics." Differentiator: "focusing on the code refactoring capability of LLMs like StarCoder2, comparing their performance with that of developers, specifically evaluating the reduction of code smells and improvements in code quality metrics, which has been less explored in prior research."

### 5.2 Code refactoring using LLMs
Prior result table:

| Study | Setup | Reported outcome |
|---|---|---|
| Shirafuji et al. [42] with GPT-3.5, 10 candidates (pass@10) | Generate 10 candidates | 95.68% of programs successfully refactored |
| Same study | Cyclomatic complexity | 17.35% reduction |
| Same study | Average lines of code | 25.84% decrease |

Differentiator: "not only comparing LLM-generated refactorings with those performed by developers but also by analyzing the effectiveness of different refactoring types," evaluating "how these refactorings reduce code smells and improve key software metrics."

### 5.3 Prompt engineering and fine-tuning
- Few-shot: "Brown et al. [4] demonstrate that few-shot prompting techniques can guide LLMs to generate higher-quality code, improving overall refactoring outcomes."
- Chain-of-Thought (CoT): "asks LLMs to first generate intermediate reasoning steps before outputting code," but "GPT-3.5-turbo with CoT prompting achieves only 53.29% Pass@1 in the HumanEval benchmark."
- Structured CoTs (SCoTs), Li et al. [21]: introduces "programming structures (i.e., sequential, branch, and loop) explicitly into the LLM's reasoning process"; "outperforms CoT prompting by up to 13.79% in Pass@1" on "HumanEval, MBPP, and MBCPP," and "human developers prefer the programs generated by SCoT prompting over those from CoT prompting."
- Fine-tuning: "Recent research [41] has shown that task-specific fine-tuning, combined with prompt design, can further enhance the ability" for "complex refactoring tasks," leveraging "domain-specific data to refine the model's understanding of code structure and quality."
- This study: "investigating how modifications to input prompts, including zero-shot, one-shot, and chain-of-thought prompting, can improve the refactoring capabilities of StarCoder2" to "maximize the model's effectiveness in reducing code smells and improving code metrics."

## Conclusion (§6)
Verbatim core claims: "StarCoder2 outperforms developers in reducing implementation code smells, achieving a reduction rate of 43.36%, compared to developers' code smell reduction rate of 24.27%." Also: "StarCoder2 shows better performance when performing systematic refactorings, while developers better handle more complex, context-dependent design code smells." And: "prompt engineering techniques, particularly one-shot prompting, significantly improve refactoring quality, emphasizing the role of prompt design in maximizing the performance of StarCoder2 in refactoring." Closing: results "highlight the complementary strengths of LLMs, particularly StarCoder2, and human expertise," with future work on "fine-tuning strategies" and "more diverse projects and programming languages."

**Covers:** RQ4 results and validity discussion under identical conditions (identical-conditions claim; internal / external / construct threats; §5 Related Work 5.1–5.3; §6 Conclusion)
