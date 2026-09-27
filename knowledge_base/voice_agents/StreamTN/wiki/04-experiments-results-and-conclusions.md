> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Experiments, Results, and Conclusions
**In one sentence:** StreamTN (4-frame delay) reaches 0.8937 Micro-F1 / 0.8931 Micro-Precision at 213 ms FPD — matching BiLSTM while streaming — with regular categories above 0.95, math/chemical formulas as the hardest cases, full-parameter fine-tuning beating LoRA and system-prompt variants, and longer delay steadily trading latency for accuracy.
## Key points
- Baseline comparison: StreamTN achieves 0.8937 ± 0.0009 Micro-F1 and 0.8931 ± 0.0022 Micro-Precision, comparable to BiLSTM (0.8941 ± 0.0015 / 0.8677 ± 0.0012) while supporting incremental processing, and well above WeTextProcessing (0.7853 / 0.7586), FlatTN (0.7569 ± 0.0019 / 0.7390 ± 0.0017), and Qwen3-0.6B (0.4872 / 0.5282).
- Per-category peaks: physical units (0.977 Micro-F1), capital amounts (0.975), and time expressions (0.967) perform best; integers and decimals, fractions and percentages, and years and dates all exceed 0.95 Micro-F1.
- Hardest categories: complex mathematical equations (0.750 Micro-F1) and chemical formulas (0.791 Micro-F1), attributed to "specialized notation, long verbalizations, and structural diversity" increasing character-level normalization difficulty.
- Ablation on tuning: replacing full-parameter fine-tuning with LoRA drops performance to 0.6335 ± 0.0012 Micro-F1 and 0.6250 ± 0.0015 Micro-Precision, indicating "updating only low-rank adapters is insufficient to learn the precise transformations required by TN."
- Ablation on prompting: adding a system prompt yields "a small but consistent decrease" to 0.8852 ± 0.0018 Micro-F1 and 0.8824 ± 0.0021 Micro-Precision, showing StreamTN can "generate structured normalized text without carefully engineered prompts."
- Delay trade-off: increasing delay from 1 to 16 frames raises Micro-F1 from 0.7030 to 0.9239 and Micro-Precision from 0.7135 to 0.9303, while FPD rises from 75 ms to 756 ms; the non-streaming model is highest (0.9639 / 0.9620) but "cannot produce normalized output until the entire sequence has been received."
- Adopted setting: the 4-frame configuration is adopted "as a practical trade-off between normalization quality and responsiveness," achieving 0.8937 Micro-F1 and 0.8931 Micro-Precision with 213 ms FPD.
---
## Baseline comparison
**Covers:** method comparison table (Table I portion in chunk)

| Method | Micro-F1 | Micro-P |
|---|---|---|
| WeTextProcessing [28] | 0.7853 | 0.7586 |
| Qwen3-0.6B [19] | 0.4872 | 0.5282 |
| FlatTN [15] | 0.7569 ± 0.0019 | 0.7390 ± 0.0017 |
| BiLSTM [29] | 0.8941 ± 0.0015 | 0.8677 ± 0.0012 |
| StreamTN | 0.8937 ± 0.0009 | 0.8931 ± 0.0022 |

## Model performance across different categories (Table II)
**Covers:** Section "2) Model Performance Across Different Categories" + Table II

"Table II reports the micro-averaged precision, recall, and F1-score of StreamTN across 14 TN categories."

"StreamTN performs best on physical units, capital amounts, and time expressions, achieving Micro-F1 scores of 0.977, 0.975, and 0.967, respectively."

"Strong results are also obtained for integers and decimals, fractions and percentages, and years and dates, all of which exceed 0.95 Micro-F1."

"These categories generally follow regular and frequently observed normalization patterns."

"In contrast, complex mathematical equations and chemical formulas remain the most challenging categories, with Micro-F1 scores of 0.750 and 0.791, respectively."

"Their specialized notation, long verbalizations, and structural diversity increase the difficulty of character-level normalization."

"Overall, the small standard deviations indicate that StreamTN performs consistently across training seeds."

TABLE II — MICRO PRECISION, RECALL, AND F1 SCORES OF DIFFERENT TN TYPES:

| TN Type | Micro-P | Micro-R | Micro-F1 |
|---|---|---|---|
| Integers and Decimals | 0.959 ± .006 | 0.963 ± .004 | 0.961 ± .004 |
| Ordinal Numbers | 0.923 ± .010 | 0.929 ± .005 | 0.926 ± .007 |
| Phone Numbers | 0.919 ± .008 | 0.917 ± .008 | 0.918 ± .008 |
| Years and Dates | 0.949 ± .009 | 0.957 ± .009 | 0.953 ± .009 |
| Time | 0.956 ± .002 | 0.978 ± .003 | 0.967 ± .001 |
| Fractions and Percentages | 0.964 ± .009 | 0.947 ± .006 | 0.955 ± .007 |
| Military Passwords | 0.925 ± .003 | 0.924 ± .004 | 0.925 ± .003 |
| Capital Amounts | 0.970 ± .004 | 0.979 ± .001 | 0.975 ± .002 |
| Amount Reading | 0.927 ± .006 | 0.919 ± .011 | 0.923 ± .007 |
| Physical Units | 0.976 ± .003 | 0.978 ± .003 | 0.977 ± .003 |
| Chemical Formulas | 0.785 ± .008 | 0.797 ± .006 | 0.791 ± .006 |
| Daily Chemicals | 0.913 ± .008 | 0.884 ± .009 | 0.898 ± .007 |
| Simple Math Equations | 0.956 ± .005 | 0.943 ± .005 | 0.950 ± .005 |
| Complex Math Equations | 0.749 ± .014 | 0.751 ± .007 | 0.750 ± .009 |

## Ablation study (Table III)
**Covers:** Section "C. Ablation Study — 1) Impact of LoRA Fine-Tuning and System Prompt" + Table III

"Table III evaluates LoRA-based parameter-efficient fine-tuning and system-prompt conditioning within the StreamTN framework."

"The full StreamTN model achieves the best results, with a Micro-F1 of 0.8937 ± 0.0009 and a Micro-Precision of 0.8931 ± 0.0022."

"Replacing full-parameter fine-tuning with LoRA reduces Micro-F1 to 0.6335 ± 0.0012 and Micro-Precision to 0.6250 ± 0.0015, indicating that updating only low-rank adapters is insufficient to learn the precise transformations required by TN."

"Adding a system prompt also yields a small but consistent decrease, producing a Micro-F1 of 0.8852 ± 0.0018 and a Micro-Precision of 0.8824 ± 0.0021."

"Overall, the ablation results demonstrate the importance of full-parameter fine-tuning and show that StreamTN can generate structured normalized text without carefully engineered prompts."

| Method | Micro-F1 | Micro-P |
|---|---|---|
| StreamTN | 0.8937 ± 0.0009 | 0.8931 ± 0.0022 |
| w/ LoRA Fine-tuning | 0.6335 ± 0.0012 | 0.6250 ± 0.0015 |
| w/ System Prompt | 0.8852 ± 0.0018 | 0.8824 ± 0.0021 |

## Impact of streaming strategy (Table IV)
**Covers:** Section "2) Impact of Streaming Strategy" + Table IV

"Table IV reports the performance of StreamTN under different delay-frame configurations."

"The non-streaming model achieves the highest Micro-F1 (0.9639) and Micro-Precision (0.9620) because it has access to the complete input sequence, but it cannot produce normalized output until the entire sequence has been received."

"Within the streaming framework, increasing the delay allows the model to observe more contextual information before normalization, thereby resolving ambiguities in context-dependent expressions and substantially improving normalization performance."

"Specifically, as the delay increases from 1 to 16 frames, Micro-F1 rises from 0.7030 to 0.9239 and Micro-Precision from 0.7135 to 0.9303."

"This improvement, however, is accompanied by an increase in FPD from 75 ms to 756 ms."

"We therefore adopt the 4-frame configuration in the main experiments as a practical trade-off between normalization quality and responsiveness; it achieves a Micro-F1 of 0.8937 and a Micro-Precision of 0.8931 with an FPD of 213 ms."

TABLE IV — STREAMTN PERFORMANCE UNDER DIFFERENT DELAY FRAMES. FPD (MS) DENOTES FIRST PACKET DELAY IN MILLISECONDS. THE CONFIGURATION MARKED WITH ∗ INDICATES THE SETTING ADOPTED IN OUR MAIN EXPERIMENTS.

| Strategy | Delay frame | Micro-F1 | Micro-P | FPD (ms) |
|---|---|---|---|---|
| Non-Streaming | - | 0.9639 ± 0.0011 | 0.9620 ± 0.0012 | - |
| Streaming | 1 frame | 0.7030 ± 0.0010 | 0.7135 ± 0.0018 | 75 |
| Streaming | 2 frames | 0.7952 ± 0.0015 | 0.8062 ± 0.0026 | 121 |
| Streaming | 4 frames∗ | 0.8937 ± 0.0009 | 0.8931 ± 0.0022 | 213 |
| Streaming | 8 frames | 0.9072 ± 0.0011 | 0.9093 ± 0.0020 | 394 |
| Streaming | 16 frames | 0.9239 ± 0.0008 | 0.9303 ± 0.0015 | 756 |

## Conclusions
**Covers:** Section "IV. CONCLUSIONS"

"This paper presented StreamTN, a Chinese text normalization model designed for low-latency cascaded spoken dialogue systems."

"StreamTN combines task-specific fine-tuning with a dual-track architecture that processes incoming text and normalized output on separate tracks, allowing normalization to proceed before the complete input is available."

"On our benchmark, the four-frame configuration achieved a Micro-F1 of 0.8937 with a first-packet delay of 213 ms."

"Its normalization performance was comparable to the BiLSTM baseline while supporting incremental processing, and additional input context produced further improvements at the cost of higher latency."

"The category-level results show that most errors occur in structurally complex mathematical and chemical expressions."

"We will release the model and benchmark to support further work on streaming text normalization."

"Future work will focus on these difficult categories and extend StreamTN to additional languages and application domains."
