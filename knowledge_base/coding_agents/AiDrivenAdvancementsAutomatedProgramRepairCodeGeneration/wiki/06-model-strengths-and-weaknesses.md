> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Model Strengths and Weaknesses: Codex, CodeT5, GraphCodeBERT and Peers

**In one sentence:** The survey groups code models by training strategy — general-language pre-training (Codex, CodeT5, GraphCodeBERT, Phind), specialized code-dataset pre-training (OpenCodeInterpreter, StarCoder2, SPT Code, Magicoder), self-supervised/bootstrapped methods (DeepSeek-Coder, WizardCoder, Mixtral, Smaug), and direct-distillation alignment (Zephyr) — and pairs each model's mechanism with its benchmark result and limitation.

## Key points

- Codex, fine-tuned from GPT models with 12 billion parameters on natural-language data then public GitHub code, beats GPT-3 and GPT-J on HumanEval by a large margin and gains accuracy via repeated-sampling iterative problem solving, but is unreliable on code with many dependencies and complicated control flows due to inconsistent variable handling.
- CodeT5's unified encoder-decoder architecture handles both programming and natural languages and uses developer-assigned identifiers to improve code semantics, making it a top performer on CodeXGLUE tasks such as defect detection and code translation, but its focus on identifier recovery leaves structural code relationships under-learned.
- GraphCodeBERT goes beyond token sequences with data-flow graphs, pre-trained on CodeSearchNet, which supports code search and clone detection via knowledge of value transmission between variables, but it can fall behind on complex logic needing broader control-flow structures.
- Phind fine-tunes CodeLlama-34B on a proprietary dataset of about 80,000 structured programming problems with DeepSpeed ZeRO 3 and Flash Attention 2, attaining a 73.8% HumanEval pass rate with a rigorous decontamination process.
- OpenCodeInterpreter converts filtered single-turn query-response pairs into multi-turn dialogues, mimics human dialogue including regenerating outputs, and uses deliberately produced erroneous code plus simulated human feedback to teach debugging, which is relevant for platforms such as LeetCode.
- Magicoder's OSS-INSTRUCT method creates realistic code instructions from open-source snippets and outperforms many state-of-the-art models even with smaller parameter size, but risks inheriting biases from seed snippets and producing low-quality outputs.
- DeepSeek-Coder combines instruction fine-tuning on billions of tokens, Fill-In-the-Middle training, and a 128K-token context window for long projects; WizardCoder's Evol-Instruct auto-generates complex instructions to cut human effort; Mixtral's Sparse Mixture of Experts activates only some of its 47 billion parameters at inference for math/code efficiency but complicates multi-GPU load balancing; Smaug's DPO-Positive refines responses from preferred/dispreferred pairs but struggles on low-edit-distance preference datasets.

---

## Models pre-trained on general language datasets

**Covers:** chunk section "Models like Codex [15], CodeT5 [21]," (survey pp. 16–17)

| Model | Base / data | Key mechanism | Reported result | Stated limitation |
|---|---|---|---|---|
| Codex [15] | Fine-tuned from GPT models with 12 billion parameters on natural-language data, then public GitHub code; powers GitHub Copilot / OpenAI API | Iterative problem solving: repeated sampling raises solve likelihood | Wins by a large margin over GPT-3 and GPT-J on HumanEval | Inconsistent treatment of variables in intricate scenarios; unreliable with many dependencies and complicated control flows |
| CodeT5 [21] | Unified encoder-decoder for programming + natural languages; uses developer-assigned identifiers | Bimodal learning of code semantics | Top performer on CodeXGLUE tasks (incl. defect detection, code translation) | Centered on identifier recovery; would benefit from learning structural relationships natural in code |
| GraphCodeBERT [6] | Pre-trained on CodeSearchNet; data-flow graphs instead of token sequences only | Represents value transmission between variables; structure-aware pre-training | Capable at code search and clone detection | May be left behind on more complex logic needing broader control-flow structures |
| Phind [1] | Fine-tunes CodeLlama-34B on ~80,000 structured programming problems; DeepSpeed ZeRO 3 + Flash Attention 2 | Rigorous decontamination to guarantee dataset integrity/validation | 73.8% pass rate on HumanEval | None stated in chunk beyond the shared group framing |

## Models pre-trained on specialized code datasets

**Covers:** chunk section "In contrast to the ones listed above…" (survey pp. 16–17)

| Model | Key mechanism | Reported strength | Stated limitation / caveat |
|---|---|---|---|
| OpenCodeInterpreter [26] | Filters coding queries for complexity; turns single-turn pairs into multi-turn dialogues; mimics human dialogue incl. regenerating outputs until debugging improves; simulated human feedback + deliberately produced erroneous code | More effective debugging learning; relevant for LeetCode-style issues | None stated beyond method description |
| StarCoder2 [2] | Language model fine-tuned on large-scale programming data; interactive feedback using user responses and revisions | Converts normal text into code snippets with great success; output more relevant/accurate | None stated |
| SPT Code [14] | Encodes source-code sequences; two-step process: pre-train on massive code datasets, then task-specific fine-tuning | Representations used for code completion and translation; enhanced learning/generation | None stated |
| Magicoder [22] | OSS-INSTRUCT: creates realistic code instructions from open-source snippets | Outperforms many state-of-the-art models even with smaller parameter size | Likely inherits biases from seed snippets, leading to low-quality outputs |

## Self-supervised and bootstrapped methods

**Covers:** chunk section "Furthermore, models like DeepSeek-Coder [7]…" incl. Fig. 6 reference (survey p. 17)

| Model | Key mechanism | Reported strength | Stated limitation / caveat |
|---|---|---|---|
| DeepSeek-Coder [7] | Pre-trained on large open-source code corpus; instruction fine-tuning with billions of tokens; Fill-In-the-Middle training (learns from its outputs); 128K-token context window | Robust prediction/completion of snippets; handles long coding projects | None stated |
| WizardCoder [24] | Evol-Instruct: automatic generation of complex instructions | Minimizes human effort; improves difficult-task performance; improves over Alpaca and Vicuna | May lag ChatGPT in some areas |
| Mixtral [3] | Sparse Mixture of Experts; activates only some of its 47 billion parameters for inference | Advantage in mathematics and code generation while conserving resources | Intricate structure may cause multi-GPU load-balancing trouble |
| Smaug [16] | Direct Preference Optimization (DPO); DPO-Positive uses preferred/dispreferred output pairs | Improves alignment and performance | May struggle with preference datasets featuring low edit distances |

Reference in chunk: "Fig. 6. Learning techniques for different AI models".

## Distillation-alignment and survey conclusion

**Covers:** chunk sections "Finally, models like Zephyr [4]…" and "7 Conclusion" (survey pp. 17–18)

- Zephyr [4]: direct distillation transfers knowledge from a teacher model to a student model to improve alignment with human intentions; enables zero-shot generalization to untaught tasks; collects human feedback to become more interpretable for various language tasks.
- Overall synthesis stated in chunk: "these different methods show the ever-changing progress in AI models in programming tasks, and this is because different training techniques give different results and performance to the models."
- Conclusion (Section 7): the paper covered recent literature on LLMs and AI for automated program repair and code generation, curating up-to-date research to familiarize researchers with state-of-the-art developments, effective use cases, and open challenges; it compares included tools to help select the best open-source models for improvements in use cases lacking reliable AI fixes.

**Covers:** chunk 06-models-like-codex-15-codet5-21.md, survey pp. 16–18 (models survey + Section 7 Conclusion as present in chunk)
