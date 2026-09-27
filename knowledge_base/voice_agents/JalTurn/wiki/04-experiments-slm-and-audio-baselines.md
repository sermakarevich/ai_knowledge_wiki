> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experiments: setups and comparison with SLM-based systems
**In one sentence:** On Mandarin Easy-Turn JAL-Turn matches or slightly beats the SLM-based EasyTurn on complete turns (96.67% vs 96.33%) at 12 ms versus 263 ms latency, while trailing on backchannels (80% vs 91%), giving a substantially more favorable quality–latency trade-off overall.
## Key points
- Evaluation uses Mandarin Easy-Turn (~1145 hours), multilingual STurn-v3 (~700 hours, 23 languages), and a large-scale in-house corpus of real-world Japanese dialogues, with 9:1 train/validation splits and original test sets for Easy-Turn/STurn-v3 plus 500 human-labeled real-world business samples for the in-house test.
- Training is end-to-end on a single H100 GPU for 10 epochs in PyTorch with AdamW (lr 1×10−4, weight decay 0.001, batch 64) and cosine annealing to 1×10−6; metrics are accuracy, F1-score, and latency for full-duplex responsiveness.
- On Easy-Turn Table 1, states are complete (cp), incomplete (incp), backchannel (bc), and wait, where JAL-Turn scores 96.67% / 93.67% / 80% / 92% at 12 ms latency.
- JAL-Turn achieves the best cp accuracy (96.67%) at 12 ms, markedly exceeds Paraformer+TEN Turn Detection (86.67% cp, 89.3% incp, 91% wait, 204 ms) and STurn-v2 (78.67% cp, 62% incp, 27 ms), reducing latency from 204 ms / 27 ms to 12 ms.
- Against SLM-based EasyTurn (96.33% cp, 97.67% incp, 91% bc, 98% wait, 263 ms), JAL-Turn is within 4.0 points on incp and 6.0 points on wait, slightly improves cp (96.67% vs 96.33%), but underperforms on bc (80% vs 91%).
- The chunk conjectures the bc gap stems from the intrinsically context-dependent nature of backchannels — often short, semantically light responses whose role is better determined with explicit lexical/semantic cues.
- Despite the bc gap, the chunk concludes JAL-Turn offers a substantially more favorable quality–latency trade-off with competitive state-wise accuracy under strict real-time constraints.
---
## 4.1 Experimental setups
**Covers:** Section 4.1 (4.1.1 Datasets; 4.1.2 Implementation Details); evaluation protocol and training config

Datasets: "experiments on the public Mandarin dataset Easy-Turn (approximately 1145 hours), multilingual STurn-v35,6 dataset (containing approximately 700 hours of speech in 23 languages), and a large-scale in-house corpus of real-world Japanese dialogues."

Splits: "For Easy-Turn and STurn-v3, we use the original test set for evaluation, while splitting the training set into training and validation sets with a 9:1 ratio. For the in-house Japanese corpus, we partition all in-house data into training and validation sets using the same 9:1 split as well. Regarding the test set, we additionally collected 500 samples from real-world business data for evaluation which are labeled by human. These data covered various attributes such as gender, age, and business scenario."

Training: "In all experiments, JAL-Turn is trained end-to-end using a single H100 GPU for 10 epochs within the PyTorch framework. We use the AdamW optimizer with an initial learning rate of 1 × 10−4, a weight decay of 0.001, and a batch size of 64. The learning rate is scheduled using a cosine annealing strategy, decaying to a minimum value of 1 × 10−6."

Metrics: "Regarding evaluation metrics, we use accuracy and F1-score for turn-taking detection. In addition, we use latency to quantify the responsiveness of the system in full-duplex scenarios."

Baseline framing in chunk: "we evaluate JAL-Turn against three categories of baselines on two public multilingual benchmarks and an in-house Japanese corpus. Specifically, we consider: (1) audio-only methods, including STurn-v2 and STurn-v3; (2) LLM-based pipelines, including GPT-5.17, Qwen3-0.6B8, and Gemini-2.5-Flash9, where SenseVoice is first used to produce ASR transcripts and the resulting text is then" [sentence truncated in chunk].

## 4.2.1 Comparison with SLM-based systems (Easy-Turn)
**Covers:** Section 4.2.1; Mandarin Easy-Turn corpus, Table 1

> "We first compare JAL-Turn with representative strong baselines on the Mandarin Easy-Turn corpus (Table 1). Here, Acccp, Accincp, Accbc, and Accwait denote the turn-taking detection accuracy for the complete, incomplete, backchannel, and wait states, respectively (higher is better)."

| Model | Acccp | Accincp | Accbc | Accwait | Latency (ms) |
|---|---|---|---|---|---|
| Paraformer+TEN Turn Detection | 86.67 | 89.3 | - | 91 | 204 |
| STurn-v2 | 78.67 | 62 | - | - | 27 |
| Easy-Turn | 96.33 | 97.67 | 91 | 98 | 263 |
| JAL-Turn | 96.67 | 93.67 | 80 | 92 | 12 |

> "JAL-Turn achieves the best performance on the cp state (96.67%) while operating at an extremely low end-to-end latency of 12 ms."
> "Compared with Paraformer [25]+TEN Turn Detection and STurn-v2, JAL-Turn yields markedly higher accuracy of the complete and incomplete states, and reduces latency from 204 ms / 27 ms to 12 ms."
> "Against EasyTurn, JAL-Turn attains comparable performance on incp and wait (within 4.0 and 6.0 points, respectively) and slightly improves cp accuracy (96.67% vs. 96.33%)."
> "However, JAL-Turn underperforms on the bc state (80% vs. 91%), which we conjecture stems from the intrinsically context-dependent nature of backchannels: they are often short, semantically light responses whose role is better determined with explicit lexical/semantic cues."
> "Crucially, despite this gap on bc, JAL-Turn offers a substantially more favorable quality–latency trade-off overall, delivering competitive state-wise accuracy under strict real-time constraints."

## Audio-only spillover present in this chunk (Tables 2–3)
**Covers:** chunk-contained fragment of Section 4.2.2; Tables 2–3 values as printed (not the focus of 4.2.1)

Table 2 (multilingual STurn-v3) as printed: STurn-v2 65.12 / 0.679 / 149 ms; STurn-v3 93.10 / 0.931 / 12 ms; JAL-Turn 93.27 / 0.934 / 36 ms.

Table 3 (in-house Japanese corpus) as printed: STurn-v2 55.46 / 0.427 / 140 ms; STurn-v3 71.94 / 0.736 / 13 ms; JAL-Turn 92.03 / 0.925 / 38 ms.

Note: the chunk's running text also states a different latency phrasing — "latencies of 22 ms on the public dataset and 43 ms on the in-house corpus" with reductions "149 ms → 22 ms" and "138 ms → 43 ms" versus older STurn-v2 — reproduced verbatim here because both phrasings appear in the chunk without reconciliation.
