[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Discussion and Limitations: The Negative Result
**In one sentence:** The learned completion policy failed to beat simple deployable timing baselines on the locked real-conversation test, so the contribution is a bounded hybrid controller with explicit evidence limits rather than a learned endpointer replacement.
## Key points
- The principal result is a bounded way to integrate uncertain learned evidence into a streaming controller, not a learned endpointer that replaces silence timing.
- Immediate onset remains acoustic, early reactions are reversible, private work is discarded safely, and a deadline provides progress when the learned model is late or unavailable.
- The adapter remained an optional signal after its standalone completion policy failed the locked gate; instrumentation changed the design rather than justifying the original model.
- Synthetic turn pretraining gave strong in-domain ranking but transferred weakly to human completion labels.
- Synthetic tool fine-tuning improved a shared-generator protocol holdout but did not establish general reasoning or retrieval quality.
- Qwen3-4B was selected for deployment after an engineering integration review, not a controlled model-quality comparison.
- The locked V1 turn test has only 11 conversations and 37 HOLD cases, so one error changes false cutoff by 2.70 percentage points and candidates within a conversation are correlated.
- A learned policy should replace the hybrid controller only if it improves the latency-versus-false-cancel frontier on conversation-disjoint human labels with participant-level intervals, controlled overlap scenarios, and final-topology action latencies.
---
## Principal result
**Covers:** Section 10, opening paragraphs

The principal result is not a learned endpointer that replaces silence timing. It is a bounded way to integrate uncertain learned evidence into a streaming controller. Immediate onset remains acoustic, early reactions are reversible, private work is discarded safely, and a deadline provides progress when the learned model is late or unavailable. This separation allowed the adapter to remain an optional signal after its standalone completion policy failed the locked gate.

> "The negative result is equally central: the historical learned completion policy did not beat simple deployable timing baselines on the locked real-conversation test."

Instrumentation therefore changed the design rather than being used to justify the original model. The resulting contribution is described as a reproducible hybrid system and a set of explicit evidence boundaries for future controlled turn-taking evaluation.

## Transfer failures
**Covers:** Section 10, transfer-failure paragraph

The experiments expose two transfer failures:

- Synthetic turn pretraining produced strong in-domain ranking but transferred weakly to human completion labels.
- Synthetic tool fine-tuning improved a shared-generator protocol holdout but did not establish general reasoning or retrieval quality.
- Qwen3-4B was selected for deployment after an engineering integration review, not a controlled model-quality comparison.

Together, these results argue for measuring learned components at the boundary where they will be used rather than inferring deployment value from training-domain metrics.

## Limitations of the turn evidence
**Covers:** Section 10, limitations paragraph

- The locked V1 turn test contains 11 conversations and only 37 HOLD cases, so one error changes false cutoff by 2.70 percentage points and candidates within a conversation are correlated.
- Possible training-source overlap prevents a clean Smart Turn superiority comparison.
- V2 excludes 216 ambiguous cases and lacks the planned independent human label audit.
- Most importantly, the deployed step-750 adapter was not evaluated on the locked V1 test, and its floor-take and backchannel heads have not been calibrated against an independently annotated natural-conversation test set.

## Deployment study limits
**Covers:** Section 10, deployment-study paragraph

- The deployment study adds only three unscripted sessions from one operator.
- It is not a user study and does not establish naturalness, interruption accuracy, or latency distributions across users, accents, noise, echo, networks, or GPU types.
- The system is English-first, human audio remains restricted by source terms, and factual generation depends on a small language model and external retrieval.

## Stronger evaluation required
**Covers:** Section 10, closing paragraph

A stronger evaluation would use conversation-disjoint human labels, participant-level confidence intervals, controlled overlap scenarios, and final-topology action latencies. A learned policy should replace the hybrid controller only if it improves the latency-versus-false-cancel frontier on that evidence.

## Conclusion
**Covers:** Section 11 Conclusion

Voice-Light demonstrates an artifact-backed path from causal conversational data to a public full-duplex cascaded agent [25, 26]. The system shares streaming ASR features with a small turn adapter, prepares responses speculatively, executes typed tools, controls playback reversibly, and records only acknowledged audio as durable assistant history. Its three-session case study shows sub-second median server response while retaining scale-to-zero deployment.

## Reproducibility snapshot
**Covers:** Appendix A, Table 6 and build/validation commands

Table 6: Principal revisions, hashes, and recorded validation for the final runtime. Full commands and additional hashes are recorded in the repository runbooks [26].

| Artifact | Revision, hash, or recorded result |
|---|---|
| Report source | Committed TeX, figure assets, and build instructions in the source repository |
| Runtime source snapshot | e2f79adc on master; evaluated two-GPU deployment d78115d2 |
| Qwen3-4B-Instruct-2507 | cdbee75f17c01a7cc42f958dc650907174af0554 |
| Qwen3-0.6B summarizer | c1899de289a04d12100db370d81485cdf75e47ca |
| Nemotron Streaming 0.6B | ebe59e5a817142986528bbbee5dba8db7b38ed50 |
| Kyutai TTS 1.6B | f65439609986c392cb12df63938abcc550c3fb15 |
| Deployed adapter step 750 | SHA-256 d5c8e02c61dc9c230eac57992278383b81f14e3b71935b8dc684fe5da4171011 |
| Release engineering checks | 630 Python tests (1 skipped, 1 integration deselected), 38 browser tests, Ruff clean; not scientific evaluation |

Build and validation commands (from the repository root on Windows, for the release PDF built from committed source):

```
.\.venv\Scripts\ruff.exe format --check --exclude .cache .
.\.venv\Scripts\ruff.exe check --exclude .cache .
.\.venv\Scripts\python.exe -m pytest tests\voice_agent tests\training\turn_taking
    -m "not integration" --import-mode=importlib
node --test tests\browser\*.test.mjs
tectonic --outdir output\pdf docs\technical-report\voice-light-technical-report.tex
```

Model-dependent integration tests and the deployed microphone acceptance session require the documented external services, GPU environment, and uncommitted credentials; they are not implied by the local command sequence above.
