[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# SSL vs ASR Encoder Adaptability — A Stronger Test of Whether FL Can Adapt an SSL Encoder
**In one sentence:** The chunk sets up a stronger test of whether FL can adapt an SSL encoder to ASR by contrasting WavLM (SSL) with Whisper (ASR-supervised) encoders under IID multilingual versus single-speaker non-IID partitions, with centralized results showing ASR pretraining decisively beats SSL pretraining (0.072 vs 0.24 WER).
## Key points
- The chunk frames the comparison as "a stronger test of whether FL can adapt an SSL encoder to the downstream ASR task", i.e. WavLM-Large (SSL) versus Whisper (ASR-supervised) paired with the same TinyLlama-1.1B decoder.
- Voxtral-Mini is an end-to-end multimodal Speech-LLM composed of a Whisper-large-v3-based audio encoder and a 30-layer Ministral-3B text decoder, jointly pretrained on audio understanding and ASR.
- All experiments use Multilingual LibriSpeech (MLS): 685.7 h federated training pool, MLS dev for validation, MLS test as held-out benchmark (138 h, 19,492 samples) across 8 European languages.
- The multilingual partition (A, approximately IID) assigns a multilingual mixture of utterances to each client irrespective of speaker identity as a control isolating heterogeneity from architecture choice; the speaker partition (B, non-IID) assigns all utterances of one speaker to one client (K=316), creating simultaneous linguistic and acoustic heterogeneity.
- Speaker leakage is inherited from LibriVox/MLS splits: centralized training carries 3.5% leakage; partition (A) contaminates 59/316 clients (18.7%, 60,825 of 1,726,583 samples); partition (B) has 8/316 clients (2.5%, 4,747 of 169,586 samples) overlapping test speakers — so "the actual degradation caused by FL non-IID conditions is slightly less severe than the raw distance to the upper bounds suggests".
- Training uses Flower with Ray backend, E=10 local epochs per round, AdamW with max lr 1e-4, cosine decay, batch 16, bf16; partition (B) trains T=40 rounds while partition (A) is reported at T=9 because its "rapid convergence leading to early WER optimization collapse".
- Only LoRA adapters (rank r=8, α=16, dropout 0.05; Voxtral α=32) on encoder (q, k, v) and LLM decoder (q, v) plus the fully-trained connector are trainable/transmitted; the connector (except Voxtral) is initialised from scratch so "it must learn to bridge the modalities entirely from the federated fine-tuning data".
- Centralized ceilings: Whisper+EuroLLM WER 0.0660 vs Whisper+TinyLlama 0.0719 ("confirming the multilingual LLM advantage even without non-IID pressure"); WavLM+TinyLlama 0.2409 (3.3× higher), "showing that ASR pretraining of the encoder decisively beats SSL pretraining for ASR".
---
## Connector and Voxtral-Mini setup
The connector "C, see Fig. 1, bridges the acoustic encoder and the LLM decoder in two steps": first a frame-stacking operation with stride 2 concatenating each pair of consecutive encoder output frames, second a single trainable linear layer projecting to the LLM input dimension. This design "is shared by Whisper+TinyLlama, Whisper+EuroLLM, and WavLM+TinyLlama, where only the single linear projection is trained from scratch", while "Voxtral uses a different connector, downsampling the audio by a factor of 4", followed by further layers (cut off in chunk).

FedProx adds a proximal term "where µ>0 penalises deviation, e.g. due to narrow acoustic distribution in client data, from the current global model θ(t)".

## Dataset and partitioning (MLS)
"All experiments use the Multilingual LibriSpeech (MLS) corpus [17], an audiobook corpus covering 8 European languages derived from LibriVox recordings. We use the official MLS train splits as the federated training pool (685.7 h total), the MLS dev split for validation during training, and the MLS test split as the held-out evaluation benchmark (138 h, 19,492 samples)."

Table 1 — MLS training data by language (stratified by speaker partition, 316 clients):

| Language | Hours | Speakers/Clients |
|---|---|---|
| French | 251.6 | 15 |
| German | 160.9 | 19 |
| English | 105.3 | 256 |
| Spanish | 83.8 | 9 |
| Italian | 27.3 | 7 |
| Polish | 25.7 | 1 |
| Portuguese | 18.5 | 5 |
| Dutch | 12.7 | 4 |
| Total | 685.7 | 316 |

Multilingual partition (approximately IID): "serves as a control to isolate the effect of data heterogeneity from architecture choice. A random multilingual mixture of utterances is assigned to each client irrespective of speaker identity, approximating the IID assumption." Leakage note: "The centralized training pools this full set and therefore carries a 3.5% speaker leakage. For FL experiments, partition (A) in Table 2, same identities overlap contaminating 59 clients out of K=316 clients (18.7%). These clients contain utterances from test or dev sharing same speakers, totalling 60,825 of 1,726,583 training samples (i.e the same 3.5% speaker leakage)." Crucially, "these are different utterances of the same speaker, not duplicate audio".

Speaker partition (non-IID): "assigns all utterances of a single MLS speaker to one client. With K=316 clients, this creates the strongest possible non-IID distribution: each client's data is drawn from a single acoustic identity, language, and recording environment, producing simultaneous linguistic (each client speaks at most one language) and acoustic (microphone, room, speaking rate) heterogeneity." Overlap: "8 of 316 clients (2.5%) correspond to speakers also present in the MLS test split, accounting for 4,747 of 169,586 training samples (2.8%), while 3.5% of centralized training data and 18.7% of clients in partition (A) share speakers with the test set."

## Training configuration
"All FL experiments use the Flower simulation framework with Ray as the backend [22]. Experiments on the non-IID speaker partition (B) train for T = 40 global rounds. For the multilingual partition (A), results are reported at T = 9 global rounds (‡ in Table 2). This is because the multilingual mixture in partition (A) exhibits rapid convergence leading to early WER optimization collapse."

"All hyper-parameter choices — encoder learning-rate multiplier λ, FedProx coefficient µ, and local epochs E — were selected on the MLS dev set, and the test split is used only to evaluate each selected checkpoint. Local clients perform E=10 local epochs per round, using AdamW optimiser with maximum learning rate η=10−4, cosine decay, batch size 16, and half precision bf16. Centralized (non-FL) training uses the same AdamW optimiser with cosine decay over a maximum of 10 epochs; the best-validation-WER checkpoint is selected (typically around epoch 4)."

"Evaluation uses the MLS test split with overall WER reported across all 8 languages combined. All models are fine-tuned with LoRA [18] adapters (rank r=8, α=16, dropout 0.05; Voxtral uses α=32) applied to the attention projections of the speech encoder (q, k, v) and LLM decoder (q, v), together with the fully-trained connector; only these parameters are trainable and are transmitted between clients and the FL server, reducing communication cost over full fine-tuning." WER convention: "Unless stated otherwise, WER values are reported as proportions (e.g., 0.1415 corresponds to 14.15%)."

## Centralized and IID upper bounds (Table 2, WER on MLS test)
"Centralized training (non-FL) on the pooled partition sets the per-architecture performance ceiling (Table 2); all centralized models converge within 4–7 epochs."

Table 2 — WER on MLS test set. B: non-IID speaker partition. A: approximately IID multilingual partition. Gap: WER relative to corresponding FedAvg baseline; negative = improvement. †: best encoder learning rate multiplier (0.02×LLM lr). ‡: reported at round 9.

| System | Encoder Setting | WER | Gap |
|---|---|---|---|
| Whisper + TinyLlama-1.1B |||| 
| Centralized | frozen | 0.0719 | — |
| FedAvg | frozen (B) | 0.1415 | — |
| FedAvg | frozen (A)‡ | 0.1284 | −0.0131 |
| FedAvg | unfrozen (B)† | 0.1418 | +0.0003 |
| FedProx µ=0.001 | frozen (B) | 0.1499 | +0.0084 |
| FedProx µ=0.001 | frozen (A)‡ | 0.1386 | +0.0102 |
| FedProx µ=0.05 | frozen (B) | 0.1615 | +0.0200 |
| FedProx µ=0.1 | frozen (B) | 0.1843 | +0.0428 |
| Whisper + EuroLLM-1.7B-Instruct |||| 
| Centralized | frozen | 0.0660 | — |
| FedAvg | frozen (B) | 0.1330 | — |
| FedAvg | frozen (A)‡ | 0.1224 | −0.0106 |
| FedAvg | unfrozen (B) | 0.1778 | +0.0448 |
| FedAvg | unfrozen† (B) | 0.1170 | −0.0160 |
| FedProx µ=0.001 | frozen (B) | 0.1217 | −0.0113 |
| WavLM-Large + TinyLlama-1.1B |||| 
| Centralized | frozen | 0.2409 | — |
| FedAvg | frozen (B) | 0.5559 | — |
| FedAvg | unfrozen (B) | 0.5338 | −0.0221 |
| Voxtral-Mini-3B-2507 |||| 
| Centralized | frozen | 0.1238 | — |
| FedAvg | frozen (B) | 0.1442 | — |
| FedAvg | unfrozen (B) | 0.1362 | −0.0080 |
| FedProx µ=0.001 | frozen (B) | 0.1492 | +0.0050 |
| FedProx µ=0.001 | unfrozen (B) | 0.1468 | +0.0106 |

Ceiling comparison verbatim: "Whisper+EuroLLM reaches WER 0.066 versus 0.072 for Whisper+TinyLlama, confirming the multilingual LLM advantage even without non-IID pressure; WavLM+TinyLlama reaches 0.24 (3.3× higher than the Whisper variant), showing that ASR pretraining of the encoder decisively beats SSL pretraining for ASR."

**Covers:** §§2.1.1, 3.2–3.3, 4.1; Table 1 (MLS hours/speakers) and Table 2 (centralized/FedAvg/FedProx WER, partitions A/B); per-language Table 3 header only (body in chunk 04)
