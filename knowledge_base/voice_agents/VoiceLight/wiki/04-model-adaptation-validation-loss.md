[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Model Adaptation and Validation-Loss Tuning

**In one sentence:** Validation-loss tuning warm-started prior weights with a fresh optimizer, 15% synthetic replay, and 1,884 human boundaries to select the 750-step deployed adapter on human validation, whose tool and turn-completion gains are validation-only and do not transfer across the explicitly separated offline protocols.

## Key points

- Tuning warm-started prior weights with a fresh optimizer, 15% synthetic replay, and 1,884 human boundaries (1,038 HOLD and 846 end-of-turn examples), selecting the resulting 750-step checkpoint on human validation.
- The final `adapter-best.pt` is step 750 with the pinned Nemotron revision listed in Table 6, one lookahead token, 80 ms encoder frames, and the four taps above; human validation selected it while synthetic validation could not.
- At runtime, forward hooks capture the exact features produced by persistent streaming ASR, a bounded latest-value queue supersedes stale adapter work, and loading or inference failure degrades the predictor without stopping ASR or the voice session.
- Assistant-token validation loss bottomed after pass 4 then rose even while free-generation protocol metrics improved; the directly comparable zero-update loss was 4.5398 and was omitted from Figure 3 to preserve resolution.
- On held-out synthetic states the final adapter emitted 200/210 expected calls, 198/210 exact tool names, 200/210 schema-valid arguments, 198/210 concise bridges, 90/90 correct no-tool responses, and 180/180 valid post-result continuations, which demonstrate acquisition of the generator's conversational protocol rather than factual accuracy or general tool intelligence.
- Synthetic pretraining exposed the transfer gap directly: completion AUROC was 0.9260 on 893 held-out synthetic examples but 0.5646 on 789 clean human validation labels, rising only to 0.5972 after human fine-tuning, with the deployed step-750 checkpoint reaching 65.04% EOT recall (426/655), 3.73% false cutoffs (5/134 HOLD), and 2.0 s p95 commitment latency on validation.
- The locked V1 test (1,673 causal silence candidates from 11 conversations, only 37 HOLD) evaluates historical step 3,500, not the deployed step-750 adapter: it crossed its learned threshold on only 205 of 1,636 EOT cases so most turns used the 800 ms timeout, preserving a low false-cutoff rate but not beating the Silero or LiveKit timing baselines.

---

## Validation-loss tuning and the deployed adapter

Validation-loss tuning warm-started those weights with a fresh optimizer, 15% synthetic replay, and 1,884 human boundaries: 1,038 HOLD and 846 end-of-turn (EOT) examples. The resulting 750-step checkpoint was selected on human validation.

The final adapter-best.pt is step 750, with the pinned Nemotron revision listed in Table 6, one lookahead token, 80 ms encoder frames, and the four taps above. Per the chunk:

> "Human validation selected it; synthetic validation could not."

At runtime, forward hooks capture the exact features produced by persistent streaming ASR. A bounded latest-value queue supersedes stale adapter work, and loading or inference failure degrades the predictor without stopping ASR or the voice session.

## Offline evaluation protocols and checkpoint lineage

The offline protocols evaluate several checkpoints with different roles. Per the chunk, Section 6 keeps those roles explicit rather than transferring results between artifacts.

### 6.1 Protocols and checkpoint lineage

The project uses separate evaluation protocols for separate claims. Tool-use evaluation measures behavior on held-out synthetic conversation states. Turn completion has two non-comparable protocols: the original V1 benchmark scores future silence under a yield-oriented target and opens a locked test split only after policy selection on validation, whereas V2 scores semantic completion at speech boundaries. V2 stopped at validation because no detector met its predefined deployment gate, so its test split remained sealed. Deployment evidence is an operator-run microphone case study, not a substitute for a controlled conversational study.

Table 2: Turn-adapter checkpoint lineage. Parenthesized values are training steps. "Validation" and "test" name distinct locked inventories; evidence is not transferred between artifacts.

| Checkpoint (step) | Role and evidence |
|---|---|
| Synthetic (2,250) | Pretraining seed; synthetic and human validation |
| Historical (3,500) | V1 locked test and V2 validation |
| Human fine-tune (750) | Deployed adapter; human validation and runtime only |
| Completion challenger (625) | Later experiment; V2 validation only |

Figure 3: Recorded assistant-token validation loss after each logical pass. Per the chunk:

> "The directly comparable zero-update loss was 4.5398 and is omitted to preserve resolution. Loss bottomed after pass 4, then rose even while free-generation protocol metrics improved."

## Synthetic tool-protocol results

### 6.2 Synthetic tool-protocol results

The final adapter emitted 200/210 expected calls, 198/210 exact tool names, 200/210 schema-valid arguments, 198/210 concise bridges, 90/90 correct no-tool responses, and 180/180 valid post-result continuations. Per the chunk, these descriptive gains demonstrate acquisition of the generator's conversational protocol:

> "They do not establish factual accuracy, robust web search, or general tool intelligence because evaluation points share the training generator and schema."

## Causal turn-completion results

### 6.3 Causal turn-completion results

Synthetic pretraining exposed the transfer problem directly. Completion AUROC was 0.9260 on 893 held-out synthetic examples but 0.5646 on 789 clean human validation labels. Human fine-tuning raised human AUROC to 0.5972. At its selected validation policy, the deployed step-750 checkpoint reached 65.04% EOT recall (426/655), 3.73% false cutoffs (5/134 HOLD cases), and 2.0 s p95 commitment latency. Per the chunk:

> "These are validation results, not locked-test results, and the head remained a poor standalone probability estimator."

For the policy metrics, a HOLD candidate is a silence followed by continuation from the same speaker, while EOT denotes a completed user turn. False cutoff is the fraction of HOLD candidates committed as EOT; EOT recall counts completed turns committed before the timeout. Latency measures the causal delay from the candidate boundary to commitment, capped by the earlier of the timeout or the observed opportunity end.

The locked V1 test contains 1,673 causal silence candidates from 11 conversations, including only 37 HOLD cases. Threshold, minimum delay, and timeout were selected on validation and frozen before test. Table 4 shows the central negative result: the Voice-Light checkpoint preserved a low false-cutoff rate but crossed its learned threshold on only 205 of 1,636 EOT cases. Most turns therefore used the 800 ms timeout, and the learned policy did not beat the Silero or LiveKit timing baselines. Per the chunk:

> "This test evaluates historical step 3,500, not the deployed step-750 adapter."

**Covers:** §5 validation-loss tuning (fresh optimizer, 15% replay, 1,884 boundaries, step-750 adapter-best.pt) and runtime hooks/queue; §6–§6.3 offline protocols, Table 2 lineage, Figure 3 loss (4.5398 baseline, bottom after pass 4), §6.2 tool-protocol counts, §6.3 validation AUROC/recall/latency and locked V1 negative result.
