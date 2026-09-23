---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: hyzhang24/DuplexSLA

### Q1. What is DuplexSLA in one sentence, and what gap in duplex backbones does it close?

> [!tip]- Answer
> DuplexSLA is a native full-duplex Speech–Language–Action foundation model that jointly decodes assistant audio and a structured action stream on a shared 160 ms chunk timeline. It closes the gap where duplex backbones lacked a native channel for in-conversation planning and tool calling, unifying listening, speaking, planning, and tool use on a single conversational clock. See [[wiki/01-overview|Overview]].

### Q2. What are the three channels of the dual-stream three-channel formulation, and what are their rates and layouts?

> [!tip]- Answer
> The user audio channel carries continuous user audio features at an 80 ms stride, and the assistant audio channel carries discrete speech tokens in a TA4 layout — 1 text anchor + 4 audio tokens at 40 ms stride per chunk. The action channel is a rate-limited textual stream (≤10 tokens per chunk) carrying delayed transcripts, planning text, interaction-control labels, and structured tool calls. See [[wiki/01-overview|Overview]].

### Q3. How are the three channels decoded, and what backbone and training regime power them?

> [!tip]- Answer
> All three channels are decoded jointly by a single backbone initialised from Step-Audio-2-mini (~7B parameters). It is adapted via continued pretraining plus post-training on duplex dialogue, turn-taking, and tool-call data. See [[wiki/01-overview|Overview]].

### Q4. How does semantic-driven turn-taking work, and how do planning and tool calls proceed without halting speech?

> [!tip]- Answer
> The model emits pause, interrupt, and backchannel decisions internally from its own semantic state rather than relying on an external semantic VAD. Planning text and structured tool calls are emitted on the action channel without halting assistant audio, with tool calls anchored to their own chunks so multi-action and backchannel-triggered tool use interleave with ongoing speech. See [[wiki/01-overview|Overview]].

### Q5. What is the repo's release status, open-source plan, and license?

> [!tip]- Answer
> As of the snapshot, only the DuplexSLA technical report (PDF, released 2026/05) is out; inference code, Hugging Face checkpoints, and the DuplexSLA-Bench evaluation harness and data are still pending. DuplexSLA-Bench is planned to cover pause, interrupt, and backchannel turn-taking plus single-action, multi-action, and backchannel-triggered tool calling. The project is released under the MIT License. See [[wiki/01-overview|Overview]].

### Q6. What does the repository's `.gitignore` exclude, and why do model weights stay untracked?

> [!tip]- Answer
> The 58-line `.gitignore` excludes macOS artefacts, Python build outputs, virtual environments, IDE/editor files, Jupyter checkpoints, logs, and caches. It also excludes model weights (`*.pt`, `*.pth`, `*.bin`, `*.safetensors`, `*.ckpt`), which the file notes will be hosted on Hugging Face rather than tracked in git. See [[wiki/02-top-level-files|Top-level-files]].

### Q7. Would you recommend building a real-time voice agent on this repo today for in-conversation tool use?

> [!tip]- Answer
> Not yet as a code dependency: with inference code, checkpoints, and DuplexSLA-Bench still unreleased, there is nothing to run or measure, so treat the repo as a design reference for the shared-clock three-channel layout and semantic turn-taking. Revisit once the Hugging Face artefacts and bench harness land and can be evaluated against your latency and tool-use requirements. See [[wiki/01-overview|Overview]].
