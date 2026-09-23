> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# RL Improves Interruption Response and Pause Handling
**In one sentence:** On source-clean and synthetic duplex probes, RL sharply improves when to wait through pauses and when to respond to interruptions, while background-speech recovery, semantic score, and takeover latency show flat or mixed changes.
## Key points
- Correct response after interruption on source-clean FDB-v1.5 rises from 72.5% to 82.5% with RL (Figure 4).
- Continuation after a user backchannel rises from 71.4% to 80.6%.
- Background-speech recovery changes from 60% to 59%, effectively flat.
- Recovery after speech directed elsewhere rises from 42% to 48%.
- On synthetic pause items, barge-in falls from 26.5% to 9%, a difference of −17.5 percentage points.
- On the synthetic interruption task, response rate rises from 96% to 97.7%, while semantic score changes from 3.94 to 3.88 and mean takeover latency increases by 40 ms.
- The chunk's conclusion is explicit: "Thus better response timing does not imply uniform improvement in every interaction measure."
---
## Interruption response on FDB-v1.5
**Covers:** Section 6.2, FDB-v1.5 paired results

| Condition | SFT | RL |
|---|---|---|
| Interruption | 72.5 | 82.5 |
| Background speech | 60 | 59 |
| Other conversation | 42 | 48 |
| User backchannel | 71.4 | 80.6 |

Units are success rate (%) per Figure 4b. Figure caption states panel (b) is "FDB-v1.5 success on 498 paired examples" and "Table 11 reports the condition sizes and success rates."

## Pause handling: waiting through a pause
**Covers:** Section 6.2, synthetic pause barge-in

| Metric | SFT | RL | Change |
|---|---|---|---|
| Barge-in rate (%) | 26.5 | 9 | −17.5 pp |

Figure caption states panel (a) is "Source-clean synthetic pause barge-in averaged across three runs per model; error bars show population standard deviation." Lower is better.

## Responding under overlap: rate vs quality and latency
**Covers:** Section 6.2, synthetic interruption task (Table 5)

| Metric | SFT | RL |
|---|---|---|
| Response rate (%) | 96 | 97.7 |
| Semantic score | 3.94 | 3.88 |
| Mean takeover latency | — | +40 ms vs SFT |

> "Thus better response timing does not imply uniform improvement in every interaction measure."
