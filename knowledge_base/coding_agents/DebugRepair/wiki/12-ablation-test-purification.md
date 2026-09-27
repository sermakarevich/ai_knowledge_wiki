> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Ablation: Effectiveness of Test Purification
**In one sentence:** Removing test semantic purification drops correct fixes from 224 to 164 (a 26.8% decrease) because unpurified failing tests contain irrelevant scenarios that produce redundant runtime output, and purification cuts the average runtime-output token count by 18.6%.
## Key points
- Removing test semantic purification reduces the number of correct fixes from 224 to 164, a 26.8% decrease.
- Real-world failing tests often contain irrelevant test scenarios that obscure the failure-triggering logic.
- Those irrelevant scenarios bring about redundant runtime outputs collected from the inserted print statements.
- Applying test purification reduces the average token count of collected runtime output by 18.6% versus the unpurified setting.
- The token reduction was measured quantitatively on the runtime output collected from print statements during the repair process.
- Purification minimizes redundant runtime outputs, ensuring the concentration of LLMs during bug fixing.
- The paper's joint RQ4 answer states that removing any single module drops correct fixes by 19.9%–26.8%, proving all components are jointly essential.
---
## Effectiveness of test purification
**Covers:** ablation on test purification component effectiveness (chunk 12-effectiveness-of-test-purification-removing-test)

Removing test semantic purification leads to a substantial performance decline, with the number of correct fixes dropping from 224 to 164, corresponding to a 26.8% decrease. The chunk attributes this to real-world failing tests often containing irrelevant test scenarios that obscure the failure-triggering logic and bring about redundant runtime outputs. To quantitatively validate this, the authors analyze the runtime output collected from the inserted print statements during the repair process: applying test purification reduces the average token count of the collected runtime output by 18.6% compared to the unpurified setting, which indicates purification effectively minimizes redundant runtime outputs, ensuring the concentration of LLMs during bug fixing.

## Answer to RQ4 (verbatim)
**Covers:** chunk's stated answer to RQ4

> Answer to RQ4: The effectiveness of DebugRepair comes from the joint contribution of its three core components and its hybrid instrumentation design. Removing any single module leads to a substantial drop in correct fixes (19.9%–26.8%), proving that all components are jointly essential. Further ablation within the simulated debugging stage shows that both LLM-based instrumentation and the rule-based fallback are necessary.
