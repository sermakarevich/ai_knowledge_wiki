# Retrieval practice — AI in software development: interview with Jellyfish CEO Andrew Lau

## Journey and the transformation thesis

1. What three-year prediction does Lau make about the software development life cycle, and how does he emotionally characterize it?

<details>
<summary>Answer</summary>
He fundamentally believes the life cycle will be completely redefined within three years, calling that prospect exciting and scary for the industry.
</details>

2. Why does Lau claim this change is bigger than agile or cloud?

<details>
<summary>Answer</summary>
Because it is not just technical but human — roles, skills, and collaboration models all evolve, redefining what people actually do rather than merely changing methods or infrastructure.
</details>

3. What breaks if a leadership team treats AI coding tools as a faster version of the existing 20-year workflow?

<details>
<summary>Answer</summary>
They optimize coding while the rest of the pipeline (review, testing, governance) stays fixed, so bottlenecks shift downstream and total delivery barely improves — the exact failure the systems-thinking argument predicts.
</details>

## Adoption data and the three phases

4. State the two headline numbers: the share of tracked organizations seeing at least a 25 percent gain, and the gain seen at 80–100 percent adoption.

<details>
<summary>Answer</summary>
More than 60 percent of 600-plus tracked organizations see at least 25 percent productivity improvement; companies with 80–100 percent developer adoption saw gains of more than 110 percent in the joint research with OpenAI.
</details>

5. Name the three transformation walls in order, and identify which is hardest.

<details>
<summary>Answer</summary>
Enablement/training/cultural nudges first, then finding the right tools and models fitting each codebase and team, and hardest of all redefining roles, processes, and incentives.
</details>

6. Why do newer companies have an easier path, and what mechanism do they use instead of reorganization?

<details>
<summary>Answer</summary>
They are not bound by legacy structures, so team ratios and responsibilities evolve naturally over hiring cycles rather than through sudden reorganizations.
</details>

7. A firm reports 90 percent of developers tried an AI tool once but gains of only 10 percent. Using Lau's depth finding, what would you diagnose?

<details>
<summary>Answer</summary>
Trial is not adoption: the 110-percent gains required 80–100 percent sustained developer adoption, so the firm is likely stuck at the first wall (enablement and genuine workflow integration) and measuring dabbling rather than depth.
</details>

## The three-layer measurement model

8. List Lau's three measurement layers with one example metric for each.

<details>
<summary>Answer</summary>
Adoption (quantitative and qualitative usage); throughput and process efficiency (pull-request rate, cycle time, latency); outcomes (road map progress, defect rates, customer impact).
</details>

9. Why does faster coding with no pipeline telemetry fail to improve delivery, in systems-thinking terms?

<details>
<summary>Answer</summary>
The life cycle is a single flow, so accelerating coding while review or compliance lags leaves total throughput unchanged — the bottleneck simply moves to requirements, testing, or governance, creating downstream friction.
</details>

10. Your team doubled code output but customer-impact metrics are flat. Which layer is failing and what do you instrument next?

<details>
<summary>Answer</summary>
Layer three (outcomes) is failing; instrument pipeline telemetry stage by stage — review latency, test queues, release cadence — to find where the extra code is stuck or degrading quality (e.g. defect rates).
</details>

## The next wave of AI tooling

11. Where has most AI tooling progress happened so far, and where does Lau expect the next wave?

<details>
<summary>Answer</summary>
So far in IDE-based tools for individual developers writing code; next in code review and agentic systems coordinating work across PDLC stages.
</details>

12. What is the "truth" problem in testing, and why does it block full-scale transformation?

<details>
<summary>Answer</summary>
Quality cannot be fully automated without defining truth, and many legacy systems lack that specification — so without new ways to formalize intent (redefining correctness), there is nothing for test automation to check against.
</details>

13. What open question does Lau raise for regulated industries, and what must organizations do until it is resolved?

<details>
<summary>Answer</summary>
Whether an agent can count as an independent validator where independence and accuracy must be proven — we are not there yet, so organizations must embed controls earlier in the process.
</details>

## Human and AI roles and the closing prescription

14. State Lau's inversion of the historic assumption about what is hard in software development.

<details>
<summary>Answer</summary>
For decades coding was thought to be the hard part; it turns out describing what to build is harder, so with generative tools writing code easily, defining intent in the spec becomes the core human task.
</details>

15. Which three capabilities does the shift reward, and what hiring mistake follows from ignoring them?

<details>
<summary>Answer</summary>
Clarity, systems thinking, and guiding AI toward the right outcomes; hiring for raw implementation speed or syntax fluency while undervaluing specification skill and architectural judgment.
</details>

16. Recite the four-part closing prescription for succeeding at this shift.

<details>
<summary>Answer</summary>
Diagnostics, enablement, role redefinition, and change management.
</details>
