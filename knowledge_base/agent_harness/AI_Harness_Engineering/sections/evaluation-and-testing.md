> **Guide:** [[../summary]] | **Deep dive:** [[../details]]

## Evaluation & Testing

Evaluation is engineering, not quality assurance. You define success criteria before building, measure rigorously, and catch regressions early. This section covers golden datasets, LLM-as-judge, and statistical rigor.

### What to Measure

| Dimension | How |
|-----------|-----|
| **Correctness** | Does the agent answer accurately? Use golden datasets + LLM-as-judge |
| **Safety** | Does it refuse bad requests? Does it avoid generating PII? Regression suites |
| **Cost** | Token usage, model routing efficiency, cache hit rates |
| **Latency** | P50, P95, P99 response time; SLOs |
| **Composition** | Can the agent's output feed downstream? Integration tests |

### Golden Datasets

Small, curated test sets (100-1000 examples) covering:
- Happy paths (the agent should succeed)
- Edge cases (unusual but valid inputs)
- Known failure modes (things that broke before)
- Safety tests (things the agent should refuse)

Update quarterly as you learn more.

### LLM-as-Judge

Use a different LLM to score outputs:
```
Question: Can I downgrade my plan?
Agent output: Yes, you can downgrade to Core. No penalty.
Judge prompt: "Is this correct given the policy: 30-day money-back guarantee?"
Judge score: 5/5 (Correct; policy allows downgrades anytime)
```

Validate the judge independently (it has biases).

### Statistical Rigor

- Report confidence intervals, not point estimates
- Report sample sizes (n=100? n=10000?)
- Report effect sizes (0.5% improvement vs 5%?)
- Distinguish significant from noisy improvements

### Regression Testing

Before deploying:
1. Run new version against golden datasets
2. Compare to previous version
3. Catch breaking changes early

### Interview Questions

- "Design a golden dataset for a customer support agent. What edge cases?"
- "How do you measure whether guardrails work without false negatives?"
- "Your new prompt improves correctness 2% but costs 20% more. What do you do?"

### Future Sections (To be expanded)

- Golden dataset construction
- LLM-as-judge design and validation
- A/B testing frameworks
- Regression test infrastructure
- Eval-as-a-service patterns
