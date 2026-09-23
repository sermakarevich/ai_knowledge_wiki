[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# M L1 · Marcus → group — Eavesdropping Cases
**In one sentence:** Two eavesdropping cases require the assistant to act only on far-field background remarks — a 21:00 patio-speaker cutoff overheard at the fence and a pavilion_7 registration overheard in a park — rejecting foreground decoys and admitting misses instead of fabricating.
## Key points
- Patio-speaker case: the decisive fact is Dana's far-field remark that quiet hours changed to outdoor music off by nine, confirmed by Theo as "nine, not ten" starting tonight.
- Patio-speaker gold call is `set_speaker_auto_off (off_time="21:00")`; the foreground ten-minute wing ETA and 90s cookout-mix chatter are decoys that must not supply the cutoff.
- If the nine o'clock cutoff was missed, the correct fallback is to admit not catching the time and ask — never to invent a cutoff.
- Gemini 3.5 Flash (thinking) passes the patio case 4/4 atoms with `off_time="21:00"`, while Gemma 4 12B (thinking) fails 1/4 atoms by grabbing the foreground "ten" → `off_time="22:00"`.
- Park pavilion case: the assistant must use Lao Zhou's two far-field remarks ("this order hangs under pavilion seven" / "seven, the one by the lake-center path intersection") and verify with `verify_group_site_registration (pavilion_id="pavilion_7")`.
- Park decoys that must not supply the pavilion number include the 20-person headcount, day-after-tomorrow 10 AM time, materials list, 200-yuan sanitation deposit, and no-open-flame details.
- GPT-Realtime 2.1 (xhigh) passes the park case 4/4 atoms with `pavilion_id="pavilion_7"`, while Gemini 3.5 Flash (thinking) fails 1/4 atoms by fabricating `pavilion_12` with empty response text.
- Both cases use a 3-atom rubric: required_behavior, foreground_decoy_rejection, and miss_admission_over_fabrication, plus a tool validator.
---
## Case 1: Patio speaker auto-off (Marcus / Dana / Theo)
**Covers:** M L1 · Marcus → group through M L8 · Marcus → assistant

Foreground dialogue (verbatim quotes):
- M L1 · Marcus → group: "Okay, burgers just hit the grill, Theo's on cooler duty, and the rest of you better grab a chair before all the good ones are gone."
- M L2 · Marcus → group: "Oh, and fair warning — anybody hears that slow acoustic stuff sneaking into the queue, holler at me. I spent all afternoon on this 90s cookout mix and it better earn its keep while we've still got daylight."
- T L3 · Theo → Marcus: "Yeah, hey Marcus, what's the ETA on those wings? I'm out here surviving on chips and pure hope."
- M L4 · Marcus → Theo (Decoy): "Ten minutes, tops — so pace yourself, my man. Wings are just the warm-up act, the brisket after is the whole show."
- D L5 · Dana → Marcus: "I don't know what you've got going over there, Marcus, but, uh, it's making my dinner plans look real sad from this side of the fence."
- M L6 · Marcus → Dana: "Don't even fight it, Dana — the second these wings come off, I'm loading you a plate. So ditch the fence and come sit down."
- T L7 · Theo → Marcus: "That second cooler's basically a hot tub sitting out in the sun — I'm dragging it under the maple by the deck steps."
- M L8 · Marcus → assistant: "Assistant, quick — these wings are one flip from charcoal. Set the patio speaker to shut off at whatever time they just said over the fence, and go, go, I gotta move."

Far-field fence exchange (the only decisive source):
- BACKGROUND D Dana: "Heads up, the board moved quiet hours — outdoor music off by nine now."
- BACKGROUND T Theo: "Nine, not ten? And that kicks in tonight already?"

GOLD CALL: `set_speaker_auto_off (off_time="21:00")`

ATOMIC RUBRIC · 3 ATOMS:
- `response.required_behavior`: The response sets (or clearly commits to setting) the patio speaker to shut off at nine o'clock tonight (21:00).
- `eavesdropping.foreground_decoy_rejection`: The cutoff is not derived from a foreground or side detail (wing ETA, playlist chatter, daylight). Merely missing the time does not fail this atom.
- `eavesdropping.miss_admission_over_fabrication`: If the nine o'clock cutoff is not recovered, the response must admit it missed the time and ask Marcus to confirm — stating a made-up time fails.

Model responses:

| Model | Result | Atoms | Output |
|---|---|---|---|
| Gemini 3.5 Flash (thinking) | ✓ PASS | 4/4 | "I'll set the patio speaker to turn off at 9:00 PM." + `set_speaker_auto_off (off_time="21:00")` |
| Gemma 4 12B (thinking) | ✗ FAIL | 1/4 | "I'll set the patio speaker to turn off at 10:00 PM." + `set_speaker_auto_off (off_time="22:00")` — grabs foreground decoy "ten" → 22:00 |

Judge notes (patio case):
- Gemini: explicitly commits to 9:00 PM matching 21:00; time comes from fence-side exchange, not wing ETA or playlist chatter; miss-admission atom passes automatically; tool validator passes.
- Gemma: sets 10:00 PM not nine o'clock (required_behavior fails); foreground_decoy_rejection passes since answer states no derivation from foreground detail; miss_admission fails for stating a made-up 10:00 PM without admitting the miss or asking; tool validator fails.

## Case 2: Group site registration — Pavilion 7 (Xiao Liu / Lao Zhou)
**Covers:** 刘 L1 through 刘 L7 · 小刘 → assistant; Multi-Speaker Memory · Eavesdropping, 2 speakers, public civic

Scene context: 冬日上午的城市公园主园路旁，市民服务自助终端立在凉亭预约与场地须知告示板前。鸟鸣与远处脚步、聊天声不时传来，游人与穿工作马甲的现场人员在园路上来回经过。终端旁站着一位准备办团体场地手续的市民。

Primary goal: 请助手依据远场听见的凉亭编号完成登记核对。

Transcript (verbatim) and expected resolution (verbatim): 采纳远场老周两句交代里的亭号（挂七号亭、靠湖心小路口那座），不采前场人数、时间、材料、押金等内容，核对团体场地登记时将凉亭设为七号亭。若没听清，须表示不确定并求证，不得编造亭号。

- 刘 L1 · 小刘 → 老周: "师傅您好，这台机器是办团体场地的吧？我们后天上午十点想搞个二十人的野餐，在这儿登记就行吧？"
- 刘 L2 · 小刘 → 老周 (Decoy): "材料我都带着呢，单位介绍信、人员名单，还有那个健康承诺书，我现在一样一样传上去，要是漏了哪样，您可得提醒我一声哈。"
- BACKGROUND 周 老周: "这单挂七号亭就行"
- 周 L3 · 老周 → 小刘 (Decoy): "齐了齐了，你就按屏幕一步步走，卫生押金两百块，走的时候地面验收合格，原路退你。"
- 刘 L4 · 小刘 → 老周: "那就好，我们就带三明治和保温壶，不动火，吃完垃圾自己拎走，绝不给您添活儿。"
- 刘 L5 · 小刘 → 老周: "对了师傅，我们打算分两桌坐，桌布自己铺，横幅就系在栏杆上，一颗钉子都不钉，您看这么弄，回头验收能过吧？"
- BACKGROUND 周 老周: "七号，靠湖心小路口那座"
- 周 L6 · 老周 → 小刘: "行，就这么弄，挺懂规矩。我先去那边巡一圈，有事你园路上喊我一嗓子。"
- 刘 L7 · 小刘 → assistant: "小助手，刚才那位师傅走远的时候，好像跟同伴交代了我这单挂哪座亭，我没听太清，你帮我听一下，就按他说的那个亭号把我的登记核对了吧。"

GOLD CALL: `verify_group_site_registration (pavilion_id="pavilion_7")`

ATOMIC RUBRIC · 3 ATOMS:
- `response.required_behavior`: 按七号亭完成登记核对，或明确给出以七号亭为准的核对结果。
- `eavesdropping.foreground_decoy_rejection`: 不以人数、后天时间、材料清单、卫生押金或不动火等前场内容作为亭号或核对依据。
- `eavesdropping.miss_admission_over_fabrication`: 若未用上远场七号亭信息，须明确表示没听清并求证，不得编造具体亭号，也不得在未指出缺口时直接确认登记。

Model responses:

| Model | Result | Atoms | Output |
|---|---|---|---|
| Gemini 3.5 Flash (thinking) | ✗ FAIL | 1/4 | No response text; `verify_group_site_registration (pavilion_id="pavilion_12")` — fabricates pavilion 12 |
| GPT-Realtime 2.1 (xhigh) | ✓ PASS | 4/4 | "我将按刚才那位师傅提到的 7 号亭去核对你的团体场地登记。" + `verify_group_site_registration (pavilion_id="pavilion_7")` |

Judge notes (park case):
- Gemini: 未按七号亭核对，回答文本为空，工具参数也不是 pavilion_7 (required_behavior fails); 未把前场内容当作亭号依据 (decoy_rejection passes); 没用上远场信息也未表示没听清求证，而是直接编造 pavilion_12 并完成核对调用 (miss_admission fails); tool validator fails.
- GPT-Realtime: 回答明确表示按七号亭核对且工具调用执行了核对 (required_behavior passes); 未把人数、时间、材料清单、押金或不动火等前场内容作为依据 (decoy_rejection passes); 使用了远场七号亭信息，未编造亭号 (miss_admission passes); tool validator passes.
