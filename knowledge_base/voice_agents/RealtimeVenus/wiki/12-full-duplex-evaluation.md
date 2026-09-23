> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Full-duplex interruption–continuation trade-off evaluation

**In one sentence:** Realtime-Venus sustains speech well through non-interruptive overlaps but lags stronger interrupters on interruption response, while its tool-use and delegation results show competitive selection with weaker argument grounding and opposite delegation failure modes across the two frontends.

## Key points

- Realtime-Venus-Audio achieves the highest continuation rates for user backchannels and background speech, and ranks second to Realtime-Venus-Omni for speech directed to others, but its interruption-response rate is lower than Joy-Duplex, GPT-4o, and Gemini 3.1 Live.
- Strong continuation does not necessarily imply strong interruption handling, and the four overlap scenarios are reported separately because they require different actions and aggregation would need an explicit weighting scheme.
- On Full-Duplex-Bench v3 tool use, Realtime-Venus-Omni achieves 86.0% tool selection F1, 53.1% argument accuracy, and 43.0% Pass@1, while Realtime-Venus-Audio achieves 82.0%, 52.2%, and 42.0%, ranking second and fourth in tool selection F1.
- GPT-Realtime leads all three tool-use metrics at 87.6%, 68.0%, and 60.0%, and both Realtime-Venus frontends remain below it in argument accuracy and complete-episode success (Pass@1).
- On the in-house delegate benchmark, Realtime-Venus-Omni achieves 75.93% overall routing accuracy versus 68.89% for Realtime-Venus-Audio (a 7.04 percentage-point gap), with both at 75.00% in the reasoning category.
- Delegation strengths diverge: Realtime-Venus-Audio has higher delegation recall on external capabilities (92.22% versus 68.33%) while Realtime-Venus-Omni has higher non-delegation specificity on routine interaction (84.44% versus 39.44%).
- The asynchronous design lets background reasoning and tool execution proceed while the frontend keeps receiving inputs and managing speech, and memory augmentation supports hour-scale video understanding with improvements across all evaluated duration bins.

---

## Interruption–continuation trade-off (Table 6 context)

Table 6 distinguishes overlaps requiring a new response from those requiring continued speech. Realtime-Venus-Audio achieves the highest continuation rates for user backchannels and background speech, and ranks second to Realtime-Venus-Omni for speech directed to others. However, its interruption-response rate is lower than those of Joy-Duplex, GPT-4o, and Gemini 3.1 Live. Thus, strong continuation does not necessarily imply strong interruption handling. Further evaluation should consider ambiguous overlaps and response-transition timing. The four scenarios are reported separately because they require different actions; aggregation would require an explicit weighting scheme.

## Tool use (FDB-v3, Table 7)

Table 7 reports Full-Duplex-Bench v3 results for Realtime-Venus with both frontends. The tool-use baselines comprise the cascaded system, Gemini 2.5 Live (Google, 2025), Gemini 3.1 Live, Grok (xAI, 2025), Ultravox (Quigley, 2025), GPT-Realtime (OpenAI, 2025), and NemotronLabs VoiceChat-11B (NVIDIA, 2026).

Table 7 Full-Duplex-Bench v3 tool-use results (%). Higher is better for all metrics.

| Model | Tool selection F1 ↑ | Argument accuracy ↑ | Pass@1 ↑ |
|---|---|---|---|
| Cascaded | 80.3% | 56.2% | 45.0% |
| Gemini 2.5 Live | 78.6% | 59.3% | 49.0% |
| Gemini 3.1 Live | 81.7% | 58.8% | 54.0% |
| Grok | 79.7% | 54.2% | 43.0% |
| Ultravox | 79.4% | 51.3% | 41.0% |
| GPT-Realtime | 87.6% | 68.0% | 60.0% |
| NemotronLabs VoiceChat-11B | 82.5% | 42.2% | 33.0% |
| Realtime-Venus-Omni | 86.0% | 53.1% | 43.0% |
| Realtime-Venus-Audio | 82.0% | 52.2% | 42.0% |

Notes. Tool selection denotes F1. Pass@1 requires all expected tool calls, no extra calls, and correct arguments for every call.

## Selection versus task completion

Both frontends remain below GPT-Realtime in argument accuracy and complete-episode success. Realtime-Venus-Audio achieves 52.2% argument accuracy and 42.0% Pass@1, compared with 53.1% and 43.0%, respectively, for Realtime-Venus-Omni. These metrics use different success criteria, so their difference cannot be interpreted as an intermediate-stage failure rate. The results motivate closer evaluation of argument grounding, retention of spoken constraints, and coordination across multiple calls. Identifying limiting factors requires examining individual execution trajectories, including failures after appropriate tool selection.

## Delegate benchmark: construction, categories, protocol

We construct an internal delegate benchmark to evaluate whether real-time interaction models can correctly decide when to delegate. Given a user request, the model must determine whether to handle it directly within the conversational frontend or issue a delegation request to Realtime-Venus-Harness. The benchmark evaluates delegation accuracy, including both necessary delegation and avoidance of unnecessary delegation.

The benchmark has two input modes with different levels of difficulty: omni input, which provides audio–visual observations to Realtime-Venus-Omni, and audio input, which provides audio-only observations to Realtime-Venus-Audio.

Task categories:

- External capabilities contains requests that require external capabilities and should therefore trigger delegation.
- Routine interaction contains requests that the frontend should handle directly without delegation.
- Reasoning includes both requests requiring delegation and requests that can be handled directly, testing whether the model can distinguish reasoning tasks that require delegation from those suitable for direct handling.

Evaluation protocol: the model's routing decision is compared with the reference label for each request. Overall accuracy measures correct routing across the benchmark. The external capabilities category reports delegation recall. The routine interaction category reports non-delegation specificity. The reasoning category reports routing accuracy within the mixed category.

## Delegate benchmark results (Table 8) and discussion

Table 8 Delegation decision performance on in-house Delegate Benchmark (%).

| Model | Overall | External capabilities | Routine interaction | Reasoning |
|---|---|---|---|---|
| Realtime-Venus-Omni | 75.93 | 68.33 | 84.44 | 75.00 |
| Realtime-Venus-Audio | 68.89 | 92.22 | 39.44 | 75.00 |

Notes. Overall and reasoning: routing accuracy; external capabilities: delegation recall; routine interaction: non-delegation specificity. Higher is better for all metrics.

Realtime-Venus-Omni achieves an overall routing accuracy of 75.93%, exceeding Realtime-Venus-Audio by 7.04 percentage points. Realtime-Venus-Audio achieves higher delegation recall in the external capabilities category (92.22% versus 68.33%), whereas Realtime-Venus-Omni achieves higher non-delegation specificity in the routine interaction category (84.44% versus 39.44%). Both variants achieve 75.00% routing accuracy in the reasoning category.

Discussion: Realtime-Venus-Audio recognizes most requests requiring external capabilities but frequently delegates routine requests that should be handled locally. Realtime-Venus-Omni more reliably avoids unnecessary delegation, but misses a larger proportion of requests requiring external capabilities. The benchmark evaluates the correctness of delegation decisions; successful execution of delegated tasks and integration of their results into the ongoing conversation require additional evaluation.

## Conclusion and future work

Across the evaluated settings, Realtime-Venus demonstrates competitive multimodal understanding and strong conversational continuity under non-interruptive speech. Its asynchronous design provides access to external capabilities while keeping interaction active: background reasoning and tool execution proceed while the frontend continues receiving inputs and managing speech. Memory augmentation further supports hour-scale video understanding, with improvements across all evaluated duration bins.

Future work will explore finer-grained streaming chunks to better capture brief events and improve the timing of conversational responses, extend the context window to support longer interactions (retaining relevant information and tracking evolving user intent), and investigate more complex and diverse tasks requiring multi-step reasoning, coordinated tool use, and asynchronous execution, with attention to managing concurrent operations and recovering from delayed or failed tool calls.

**Covers:** chunk 12-interruption-continuation-trade-off-table-6-dist; plan covers "Full-duplex interruption–continuation trade-off evaluation"; source sections on interruption–continuation trade-off, FDB-v3 tool use (Table 7), selection vs. completion, delegate benchmark §7.6 (Tables 8), conclusion §8
