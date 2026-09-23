> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# IHBench: Evaluating Post-Interruption Recovery in Voice Agents with Structured Workflows
**In one sentence:** IHBench is a benchmark that evaluates post-interruption recovery — whether a voice agent resumes a state-machine-driven workflow at the correct step after a mid-utterance user interruption — across 10 enterprise domains, 6 interruption types, and 27 audio-language model configurations scored on task fulfillment and recovery quality.
## Key points
- Voice agents in structured workflows (customer service, healthcare scheduling, account management) must handle frequent interruptions while maintaining multi-step progress.
- Existing speech-model benchmarks focus on interruption timing — barge-in detection, endpointing, and turn-taking dynamics — leaving post-interruption recovery unmeasured.
- IHBench (Interruption Handling Benchmark) injects six interruption types at controlled mid-utterance points in state-machine-driven workflows across 10 enterprise domains.
- Each interruption ships with a per-interruption evaluation rubric generated alongside the data, scored on two axes: task fulfillment and recovery quality.
- The paper evaluates 27 audio-language model configurations from OpenAI, Google, and the open-weight community, with wide variation between models.
- Closed-weight models are consistently more robust: they win far more often on task fulfillment and degrade roughly 3.3× more slowly as conversations grow longer.
- Closed-weight models show no audio-versus-text modality gap, whereas open-weight models lose ground on all three reported dimensions (win rate, degradation, modality gap).
- A human study validates the LLM judge against human annotators, and a cross-benchmark analysis against AudioMultiChallenge frames recovery quality as a largely distinct capability axis.
---
## Paper identity
**Covers:** Paper abstract, benchmark goal, and contributions (arXiv:2606.19595v1 [cs.LG] 17 Jun 2026)

| Field | Value (from chunk) |
|---|---|
| Title | IHBench: Evaluating Post-Interruption Recovery in Voice Agents with Structured Workflows |
| Authors | Ahmad Salimi, Wentao Ma, Yuzhi Tang, Dongming Shen, Mu Li, Alex Smola |
| Affiliations | Boson AI — Toronto, ON, Canada; Santa Clara, CA, USA |
| arXiv | 2606.19595v1 [cs.LG] 17 Jun 2026 |

## The gap: after the interruption
Existing benchmarks for speech-capable models focus on the timing of interruptions:

- barge-in detection
- endpointing
- turn-taking dynamics

They leave unmeasured what happens after the interruption, posed as three questions:

> "does the agent resume the workflow at the correct step? Does it address the user's interjection? Does it avoid re-delivering content the user already heard?"

## IHBench design (as stated in abstract)
> "We introduce IHBench (Interruption Handling Benchmark), a benchmark that evaluates post-interruption recovery in voice agents executing state-machine-driven workflows across 10 enterprise domains."

- Workflows are state-machine-driven; example deployment domains named: customer service, healthcare scheduling, account management.
- Six interruption types are injected at controlled points mid-utterance.
- Per-interruption evaluation rubrics are generated alongside the data.
- Each interruption is scored on two axes: task fulfillment and recovery quality.

## Headline evaluation claims
> "We evaluate 27 audio-language model configurations from OpenAI, Google, and the open-weight community."

- Models vary widely, and recovery quality depends strongly on the interruption type.
- Closed-weight models are consistently more robust to interruptions than open-weight ones:
  - win far more often on task fulfillment;
  - degrade roughly 3.3× more slowly as conversations grow longer;
  - show no audio-versus-text modality gap, whereas the open-weight models lose ground on all three.
- A human study validates the LLM judge against human annotators.
- A cross-benchmark analysis against AudioMultiChallenge indicates that recovery quality is a largely distinct capability axis.
