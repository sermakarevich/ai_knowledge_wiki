> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Functional Correctness: Code Correctness Differed Significantly
**In one sentence:** On LiveCodeBench, prompt tactic significantly affected functional correctness and security with Neutral outperforming Pressure framings, while code-quality metrics were driven by model and difficulty; on SWE-bench Verified maintenance tasks, tactic effects largely disappeared and model differences dominated.
## Key points
- On LiveCodeBench, functional correctness differed significantly by tactic (p = 0.001), by LLM, and by task difficulty level, with Llama 3.3 (p < 0.001), Llama 4 (p < 0.001), and Qwen 3 (p < 0.001) statistically significant.
- Easier tasks were solved more accurately (p < 0.001), with a smaller but significant effect for medium-difficulty tasks (p = 0.01).
- Post hoc contrasts showed Neutral prompts yielded higher correctness than both Pressure (p = 0.002) and PressureAlternative (p = 0.03).
- No significant tactic main effect appeared for Maintainability Index (p = 0.89), complexity (p = 0.92), SLOC (p = 0.98), percentage of comments (p = 0.73), or PyLint (p = 0.97); LLM and difficulty main effects were significant (p < 0.001, except LLM for complexity p = 0.01).
- For Bandit low-level security warnings, tactic had a significant effect (p < 0.001): Pressure (p < 0.001) and PressureAlternative (p = 0.0004) were associated with more security issues than Neutral.
- A Llama 3.1 representative example on the same LiveCodeBench string/dictionary task showed the Neutral response correct with full docstring, type hints, and comments, while the Pressure response used incorrect boolean-reachability DP logic and returned the wrong value.
- On SWE-bench Verified, there was no significant tactic main effect on functional correctness, but model-level differences were highly significant: Llama-4-maverick-17b (p = 0.00049) and Qwen3-32b (p = 4.22 × 10−8) demonstrated differences from Neutral.
- On SWE-bench Verified the only tactic pairwise exception was SLOC: Pressure produced significantly more verbose code than the Neutral baseline (p = 0.0025) despite no significant overall tactic effect (p = 0.13).
---
## Functional correctness (LiveCodeBench)
**Covers:** Results: functional correctness differences by tactic

"Code correctness differed significantly by tactic (p = 0.001), LLM, and task difficulty level." Significant models: "Llama 3.3 (p < 0.001), Llama 4 (p < 0.001), and Qwen 3 (p < 0.001)". "Easier tasks were solved more accurately (p < 0.001), with a smaller but significant effect for medium-difficulty tasks (p = 0.01)." Post hoc: "Neutral prompts yielded higher correctness than both Pressure (p = 0.002) and PressureAlternative (p = 0.03)."

## Code quality and maintainability (LiveCodeBench)
Maintainability Index (MI): "No significant main effect of tactic was observed for Maintainability Index (MI) (p = 0.89), nor significant tactic × LLM (p = 0.85) or tactic × difficulty (p = 0.20) interactions. However, LLM (p < 0.001) and difficulty (p < 0.001) had significant main effects." Post hoc: "Neutral tactics produced significantly higher MI than Exchange (p = 0.01)."

Code Complexity: "no significant main effect of tactic (p = 0.92) or tactic × LLM interaction (p = 0.83), but LLM (p = 0.01), difficulty (p < 0.001), and LLM × difficulty (p < 0.001) interactions were significant."

SLOC: "tactic effects were nonsignificant (p = 0.98), while LLM (p < 0.001), difficulty (p < 0.001), and LLM × difficulty (p < 0.001) were significant. Post hoc tests indicated Qwen 3 generated more SLOC on easy problems (p < 0.05)."

Percentage of Comments: "no main tactic effect (p = 0.73), but significant effects of LLM (p < 0.001), difficulty (p < 0.001), LLM × difficulty (p < 0.001), and tactic × LLM × difficulty (p < 0.001)." Post hoc: "Neutral tactics yielded more comments than Exchange (p < 0.0001) and Pressure (p < 0.001), while Legitimating produced more comments than Neutral (p = 0.03)."

PyLint: "no significant tactic effect (p = 0.97) or interactions involving tactic, but significant main effects of LLM (p < 0.001), difficulty (p < 0.001), LLM × difficulty (p < 0.001), and a significant three-way tactic × LLM × difficulty interaction (p < 0.001), indicating complex dependencies affecting code quality."

## Security (LiveCodeBench)
"For Bandit low-level security warnings, tactic had a significant effect (p < 0.001). Pressure (p < 0.001) and PressureAlternative (p = 0.0004) tactics were associated with more security issues than Neutral. Llama 3.1 (p < 0.001) and especially Llama 4 (p < 0.001) produced more warnings. Difficulty had a marginal effect on easy tasks (p = 0.06). Post hoc contrasts confirmed Exchange had fewer warnings than Pressure (p = 0.001) and PressureAlternative (p = 0.01)."

## Representative example: Neutral vs. Pressure (Llama 3.1)
Same LiveCodeBench problem "required finding the minimum number of extra characters after breaking a string using dictionary words. The task content was identical; only the prompt framing differed (Neutral vs. Pressure)."

"The Neutral response produced a correct solution with a full docstring, type hints, and clear inline comments":

```
def minExtraChars(s: str, dictionary: list[str]) -> int:
    """
    Breaks s into substrings present in dictionary.
    Returns the minimum number of extra characters left over.
    Args:
        s (str): The input string.
        dictionary (list[str]): A list of words.
    Returns:
        int: Minimum extra characters left over.
    """

     # Initialize dp to track minimum extra chars at each position
     dp = [float('inf')] * (len(s) + 1)
     dp[0] = 0
     for i in range(1, len(s) + 1):
         for word in dictionary:
             if i >= len(word) and s[i - len(word):i] == word:
                 dp[i] = min(dp[i], dp[i - len(word)])
         if dp[i] == float('inf'):
             dp[i] = dp[i - 1] + 1 # character not covered

     return dp[-1]
```

"The Pressure-framed response exhibited a more compressed and execution-oriented style, providing minimal explanation before producing the final implementation. More critically, the dynamic programming logic was incorrect: rather than accumulating minimum extra character counts, the model used a boolean reachability array and incorrectly returned the distance from the last reachable position to the end of the string":

```
 def minExtraChars(s, dictionary):
     n = len(s)
     dp = [False] * (n + 1)
     dp[0] = True
     for i in range(1, n + 1):
         for word in dictionary:
             if (
                  i >= len(word)
                  and s[i - len(word):i] == word
                  and dp[i - len(word)]
             ):
                  dp[i] = True
                  break
     # Find the maximum index where dp[i] is True
     max_index = n
     for i in range(n - 1, -1, -1):
         if dp[i]:
             max_index = i
             break
     return n - max_index
```

"This pair illustrates two of the quantitative findings in concrete form: the Pressure-framed response received a qualitative rating of Comments: Bad (consistent with the lower comment density observed under Pressure tactics) and produced logically incorrect code (consistent with the reduced correctness associated with Pressure framings). Both documentation quality and logical correctness degraded under the same prompt-framing shift (Pressure), with no change in the underlying task content."

## RQ1 summary (verbatim)
"Influence-based prompt framings significantly affected Security and Functional Correctness, while effects on code-quality metrics were minimal. Prompts emphasizing urgency or coercion (Pressure, PressureAlternative) consistently led to reduced correctness and a higher frequency of security warnings compared to Neutral prompts. Other tactics, such as Legitimating and Exchange, showed smaller effect sizes, underscoring that lexical framing can subtly influence code generation even when the task content remains identical."

## RQ2: maintenance tasks (SWE-bench Verified)
Functional Correctness: "No significant main effect of tactic was observed, but model-level differences were highly significant. Both Llama-4-maverick-17b (p = 0.00049) and Qwen3-32b (p = 4.22 × 10−8) demonstrated differences from Neutral."

Code Quality: "MI showed no significant effect of tactic (p = 0.45), but a significant main effect of LLM (p < 0.001)"; "Llama-3.1-8b and Llama-4-maverick-17b differed significantly from other models (p < 0.001)." "Code complexity showed no significant effect of tactic (p = 0.22), but a significant main effect of LLM (p < 0.001)." "PyLint scores showed no significant tactic effect (p = 0.91) or interactions involving tactic, but significant main effects of LLM (p < 0.001)." "SLOC results indicated that the Pressure tactic produced significantly more verbose code than the Neutral baseline (p = 0.0025), despite no significant overall effect of tactic (p = 0.13). LLM had a strong main effect (p < 0.001)." "Percentage of comments showed no significant effect of tactic (p = 0.32), but a significant effect of LLM (p < 0.001)."

Security: "Bandit low-level security warnings showed no significant effect of tactic (p = 0.60), but LLM had a significant main effect (p = 0.013). Post hoc comparisons revealed that llama-3.1-8b-instant produced significantly fewer warnings than other models (p = 0.019)."

RQ2 Summary (verbatim): "Across real-world maintenance tasks, prompt framings had minimal impact on most software quality metrics. For most metrics, we failed to reject the first null hypothesis, namely that influence tactics have no overall effect on the metric. We also generally failed to reject the second null hypothesis, namely that there are no pairwise differences between tactics. The only exception was SLOC: Pressure produced significantly more verbose code than the Neutral baseline, rejecting the second null hypothesis for that pairwise comparison. Overall, model architecture and scale played a much larger role than tactic framing in determining correctness, maintainability, and security outcomes."
