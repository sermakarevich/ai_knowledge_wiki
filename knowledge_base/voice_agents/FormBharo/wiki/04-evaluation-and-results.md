> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Evaluation and model selection: STT, extraction, form completion, and reply

**In one sentence:** Sequential unit and integration tests show Scribe v2 is the best STT for downstream form accuracy, frontier LLMs saturate extraction on clean transcripts but reorder under real speech, the rule-based layer recovers some errors yet form completion degrades more than per-turn extraction, and weighted cost–latency–accuracy trade-offs select Gemini 3.5 Flash for EXTRACT and GPT-5.4-mini for REPLY.

## Key points

- Integration chains stages: EXTRACT's actual output is passed through rule-based validation and flow control instead of expected values, extraction accuracy is measured for every STT × EXTRACT pair and response accuracy for every STT × EXTRACT × REPLY combination, and the gap to reference-transcript runs quantifies transcription-error impact.
- STT ranking uses LLM-WER rather than WER because the metrics disagree (Nova-3 has the best WER yet second-worst LLM-WER); Chirp 3 has the best LLM-WER but costs at least twice any other model, GPT-4o-transcribe is least accurate, so both are eliminated and Scribe v2, Saaras v3, and Nova-3 continue to integration tests.
- On reference transcripts extraction saturates (GPT-5.5 99.79%, Gemini 3.5 Flash 99.36%, two Claude models 99.15%), median drops under real transcripts are only 0.42 to 3.14 points, but GLM-5.1 collapses by 35 points with Scribe v2 transcripts while the four most accurate models lose at most 4.63 points.
- The extraction leaderboard changes on real speech: best real-speech accuracy is 98.94% (Gemini 3.5 Flash and Claude Sonnet 4.6 on Scribe v2), Claude Opus 4.8 leads on Saaras v3 (96.22%), and Gemini 3.5 Flash leads on Nova-3 (96.38%).
- Form completion differs from per-turn extraction because the rule-based layer normalizes errors (e.g. Gemini 3 Flash: 95.96% extraction but 100% completion on reference via fixing numeric-as-string type mismatches), yet median completion drops more than extraction drops (7.67 points Saaras v3, 7.38 Scribe v2, 13.56 Nova-3), with a ~41-point worst-case decline for GLM-5.1 on Scribe v2 as uncorrected errors accumulate across turns.
- Scribe v2 is selected as STT for strongest downstream medians (97.29% extraction, 91.84% form completion) and smallest median drops versus reference; EXTRACT selection on Scribe v2 transcripts applies p95 latency below 5 s and completion above 90% (excluding Gemini Pro and Gemini 2.5 Flash), then weighted-sum scalarization with `w_l = 0.1` selects Gemini 3.5 Flash, which trails Claude Sonnet 4.6 by only 0.51 points while responding faster at less than half the per-turn cost.
- REPLY errors propagate by a median 2.23 points (range 1.06–3.40); with p95 below 4 s and accuracy above 95% plus Pareto filtering, GPT-5.4-mini is selected over Gemini 3 Flash, ranking highest throughout `0.5 ≤ w_a ≤ 0.9`.

---

## Evaluation design

EXTRACT and REPLY are tested both as units and chained. To build the tool call for REPLY, EXTRACT's actual output is passed through the rule-based validation and flow control, instead of the expected extraction values used in the unit tests.

Each EXTRACT model drives its own set of REPLY runs. Because each stage feeds the next, extraction accuracy is measured for every STT × EXTRACT pair, and response accuracy for every STT × EXTRACT × REPLY combination. The gap between reference-transcript and STT-transcript runs quantifies the impact of transcription errors on form completion.

## Setup

Five STT models and 11 LLMs are benchmarked across accuracy, latency (p95), and cost. Temperature is set to 0 for non-reasoning models. Reasoning models use "medium" reasoning effort for EXTRACT and "low" for REPLY. Full implementation details and 95% confidence intervals are in the appendix.

## Speech-to-Text

Table 3 shows the two metrics disagree: Nova-3 has the best WER yet the second-worst LLM-WER. Models are therefore ranked by LLM-WER, which was built to address the shortcomings of WER. Chirp 3 has the best LLM-WER but costs at least twice as much as any other model, while Scribe v2 performs close to Chirp 3 at a fraction of the cost. GPT-4o-transcribe is the least accurate. Eliminating these two leaves Scribe v2, Saaras v3, and Nova-3, which are carried into the integration tests.

## Data extraction

Table 4 compares various LLMs on per-turn extraction accuracy, computed using reference transcripts and the transcripts of the three STT models as inputs.

Frontier models saturate extraction accuracy on reference transcripts with the top models scoring almost perfectly: GPT-5.5 leads at 99.79%, with Gemini 3.5 Flash (99.36%) and the two Claude models (99.15%) just behind. Robustness to STT errors varies: the median drop is modest, from 0.42 percentage points to 3.14 (Table 6). The four most accurate models lose at most 4.63 points regardless of the STT model. But weaker models degrade much more: GLM-5.1 collapses by 35 points with Scribe v2 transcripts. The next-worst drop is still 11.2 points. The extraction accuracy leaderboard changes when real transcripts are used: GPT-5.5 is no longer the winner. The best extraction accuracy under real-speech is 98.94% (Gemini 3.5 Flash and Claude Sonnet 4.6) with transcripts from Scribe v2. Claude Opus 4.8 leads under Saaras v3 (96.22%) and Gemini 3.5 Flash leads under Nova-3 transcripts (96.38%).

## Form completion

Similar to extraction accuracy, Table 5 reports form-completion accuracy across all the LLMs being tested. The rule-based layer recovers extraction errors.

On reference transcripts, Gemini 3 Flash achieves 95.96% per-turn extraction accuracy but 100% form-completion accuracy. Per-turn extraction evaluates the output of the EXTRACT LLM, whereas form completion evaluates the values ultimately stored in the form after the rule-based layer processes it. All the extraction errors for this model arise from a type mismatch: a numeric field being returned as a string. The rule-based layer normalizes it before storing the value, preserving 100% form-completion accuracy. The text states:

> "This highlights a benefit of our hybrid design which enables smaller models to perform better end-to-end even if their per-turn inference is not perfect."

The best model end-to-end differs from the best model per-turn. Under reference transcripts, GPT-5.5 leads extraction accuracy (99.79%), whereas Gemini 3 Flash and Gemini 3.5 Flash tie for the highest form-completion accuracy at 100%.

Form completion degrades more than per-turn extraction with error-prone real-speech transcripts: median form-completion accuracy drops by 7.67 percentage points with Saaras v3, 7.38 points with Scribe v2, and 13.56 points with Nova-3 (Table 6), compared with median per-turn extraction drops of only 0.42–3.14 points. The largest model-specific decline is ∼41 points for GLM-5.1 with Scribe v2. Although the rule-based layer recovers some extraction errors, uncorrected errors can accumulate across turns to produce a larger degradation end-to-end.

## Model selection

STT, EXTRACT, and REPLY models in the pipeline (Figure 1) are selected sequentially because each downstream component consumes the outputs of the components before it: first the STT model, then the best LLM for EXTRACT using that STT model's transcripts, and finally REPLY with the selected STT and EXTRACT models fixed. The deployment objective is to balance task performance, p95 latency, and cost, subject to component-specific deployment constraints.

STT selection: Scribe v2 provides the strongest downstream performance. It achieves the highest median extraction accuracy (97.29%) and form-completion accuracy (91.84%), while producing the smallest median drops relative to the model performance on reference transcripts (Table 6). Scribe v2 is therefore selected as the STT model.

EXTRACT selection: with Scribe v2 fixed, EXTRACT models are compared using form-completion accuracy on its transcripts, together with latency and cost. Models failing deployment constraints — p95 latency below 5 s and form-completion accuracy above 90% — are discarded. This excludes Gemini Pro, despite its leading form-completion accuracy, and Gemini 2.5 Flash, leaving six candidates. Among those, Claude Sonnet 4.6 achieves the highest form-completion accuracy, Mistral Medium 3.5 has the lowest p95 latency (1.75 s), and GPT-5.4-mini is the cheapest ($0.0011). No model leads all three axes, and all six candidates lie on the Pareto frontier (Figure 2). Figure 2 is described as:

> "Cost–quality–latency trade-off among EXTRACT models satisfying the deployment constraints. The logarithmic x-axis shows cost per turn, the y-axis shows form-completion accuracy using Scribe v2 transcripts, and marker area encodes p95 latency per turn (bigger is slower). All six models are Pareto-optimal across the three objectives."

The three axes are min–max normalized within the frontier, reversing latency and cost so higher is preferred:

| Axis | Formula |
|---|---|
| Accuracy | `ã_i = (a_i − a_min) / (a_max − a_min)` |
| Latency | `ℓ̃_i = (ℓ_max − ℓ_i) / (ℓ_max − ℓ_min)` |
| Cost | `c̃_i = (c_max − c_i) / (c_max − c_min)` |

Models are ranked with weighted-sum scalarization (Marler and Arora 2010):

`U_i = w_a ã_i + w_l ℓ̃_i + w_c c̃_i, i* = arg max_i U_i`, where `w_a + w_l + w_c = 1`.

As a baseline, under equal weights, Mistral Medium 3.5 ranks highest (U = 0.81), followed by GPT-4.1 (U = 0.78). Mistral combines the lowest latency with 91.84% form-completion accuracy and a cost of $0.0080 per turn. Claude Sonnet 4.6, the most accurate candidate, scores lower (U = 0.51) because it is slower and more expensive. Since the hard latency constraint already excludes too-slow models, the remaining latency differences get lower weight, `w_l = 0.1`. Accuracy remains the primary objective, so `w_a` is swept from 0.5 to 0.9 with `w_c = 1 − w_a − w_l`. Only two models lead across this range: Gemini 3.5 Flash for `0.50 ≤ w_a ≤ 0.61`, and Claude Sonnet 4.6 for `0.62 ≤ w_a ≤ 0.90` (full table in the Appendix). Gemini 3.5 Flash is selected for EXTRACT: it trails Claude Sonnet 4.6 by only 0.51 percentage points on form-completion accuracy while responding faster and costing less than half as much per turn.

## Response generation

REPLY has the narrowest role in the pipeline: it either phrases the selected question naturally or ends the call, so a smaller, faster model may suffice. With Scribe v2 and Gemini 3.5 Flash fixed for transcription and extraction, five LLMs are compared for REPLY. The selected EXTRACT model's actual outputs on Scribe v2 transcripts are passed through the rule-based layer to construct the decision passed to REPLY. Table 7 reports response accuracy:

| Model | Reference | Scribe v2 |
|---|---|---|
| Claude Sonnet 4.6 | 100.00 | 97.77 |
| GPT-4.1 | 100.00 | 96.60 |
| GPT-5.4-mini | 98.09 | 96.70 |
| Gemini 3 Flash | 97.23 | 96.17 |
| Gemini 3.5 Flash | 97.02 | 94.73 |

Table 7: REPLY response accuracy with Gemini 3.5 Flash as the EXTRACT LLM.

The Reference column uses the expected extraction values with reference transcripts to prepare the inputs, whereas for Scribe v2, the outputs of EXTRACT on Scribe v2 transcripts are used (per Section 4). Errors propagate: response accuracy decreases for all five models, with declines from 1.06 to 3.40 percentage points and a median of 2.23 points. No single model is best across accuracy, latency, and cost: Claude Sonnet 4.6 is most accurate on Scribe v2 transcripts (97.77%), Gemini 3 Flash has the lowest p95 latency (2.66 s), and GPT-5.4-mini is cheapest ($0.0008 per turn). Deployment constraints of p95 latency below 4 s and response accuracy above 95% exclude Claude Sonnet 4.6 on latency and Gemini 3.5 Flash on accuracy, leaving three candidates; Pareto filtering leaves GPT-5.4-mini and Gemini 3 Flash. Using the same weighted-sum scalarization with `w_l = 0.1`, GPT-5.4-mini ranks highest throughout `0.5 ≤ w_a ≤ 0.9` (details in the Appendix). GPT-5.4-mini is therefore selected for REPLY.

## Field scoring and related context in chunk

Table 8 states how each form field is scored during EXTRACT evaluation: open-ended text fields use an LLM judge, every closed-ended field uses exact match:

| Field | Scoring |
|---|---|
| Name | LLM judge |
| District | exact |
| Clinic name | LLM judge |
| Child's name | LLM judge |
| Pregnant? | exact |
| Gestational age | exact |
| Child's DOB | exact |
| Calling number linked to clinic? | exact |
| Number linked to clinic | exact |
| WhatsApp = calling number? | exact |
| WhatsApp number | exact |
| Aadhaar last 4 digits | exact |

The chunk also contains the paper's Sections 6–7 in abbreviated form: related work contrasts component-level transcription/slot-filling cascades and voice benchmarks (VoiceBench, VoiceAgentBench, EVA-Bench) with FormVoiceAgentBench's noisy-audio form-completion scoring, and the conclusion states that component-level accuracy does not predict end-to-end form completion because errors both propagate and cancel, with the rule-based layer helping smaller, cheaper models meet deployment constraints; listed limits include scripted answers, single-acoustic-variation calls, five simulated users/annotators, Hindi-only data, and no TTS evaluation.

**Covers:** Sections 5–7 (Setup §5.1, STT §5.2, Extraction §5.3, Form Completion §5.4, Model Selection §5.5, Response Generation §5.6, Related Work §6, Conclusion §7) plus Table 7, Table 8, and Figure 2 description
