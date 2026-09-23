> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Mandarin takeout-order example: allergy scope over-expansion and dish attribution
**In one sentence:** A Mandarin takeout-order case where the response correctly attributes Kung Pao Chicken and peanut-free Steamed Sea Bass but fails by setting `peanut_exclusion_scope="entire_order"`, expanding one speaker's peanut allergy to the whole order.
## Key points
- The case is a Mandarin food-ordering dialogue resolved to restaurant "Shu Xiang Ju" with an `arrive_by="18:30"` delivery constraint.
- The gold call is `place_takeout_order (arrive_by="18:30", peanut_exclusion_scope="entire_order", restaurant="Shu Xiang Ju", s1_dish="Kung Pao Chicken", s2_dish="Steamed Sea Bass")` as shown in the chunk.
- The response text attributes Kung Pao Chicken to Zhiqiang and Steamed Sea Bass plus the peanut restriction to Ms. Liu Fang, which the judge marks correct under `binding.core_grounding`.
- The same call fails `distributed.scope_holder_binding` because the peanut exclusion is set to `entire_order`, spreading Liu Fang's allergy to the full order.
- The call also fails `tool.validator` in the chunk's recorded verdicts.
- The chunk body is garbled/truncated: after the order header it interleaves two unrelated embedded scenes (a Rosa/Deshawn packaging-line ticket case and a Chinese EV-family charging-stop case) and cuts off mid-line at L3.
---
## Order header and gold call
**Covers:** chunk header lines 1–10

| Field | Value in chunk |
|---|---|
| Restaurant | Shu Xiang Ju (蜀香居) |
| Arrive by | 18:30 (6点半前送到) |
| S1 dish | Kung Pao Chicken (宫保鸡丁) |
| S2 dish | Steamed Sea Bass (清蒸鲈鱼, peanut-free) |
| Peanut exclusion scope | `entire_order` |
| Gold call (verbatim) | `place_takeout_order (arrive_by="18:30", peanut_exclusion_scope="entire_order", restaurant="Shu Xiang Ju", s1_dish="Kung Pao Chicken", s2_dish="Steamed Sea Bass")` |

Verbatim header quote: "已选择蜀香居，要求6点半前送到。您点的宫保鸡丁和刘芳女士需要的清蒸鲈鱼（无花生）已加入订单。"
## Judge verdicts on the order call
**Covers:** chunk lines 11–15

- `✓ binding.core_grounding` — "Judge：回答文本把宫保鸡丁给志强、清蒸鲈鱼与花生忌口给刘芳，归属表述正确。"
- `✗ distributed.scope_holder_binding` — "Judge：peanut_exclusion_scope 设成 entire_order，把刘芳的过敏扩到了全单。"
- `✗ tool.validator`
## Embedded packaging-line scene (garbled interleaving)
**Covers:** chunk lines 16–94

- Scene: mid-shift packaging line with supervisor Rosa (S1) and operator Deshawn (S2); overhead crane noise; tablet assistant handles maintenance tickets, supply requests, shift notes.
- Rosa (L1) reports conveyor-two bearing issue, line locked out till maintenance clears it, wants action before the 14:00 changeover; requests Herrera (designated specialist) sign-off in L4.
- Deshawn (L2) requests urgent shrink-wrap supply (last box, ~two hours left); (L3) adds heat-sealer temp warning, then (L5) retracts it after recalibration — retraction applies to S2 only and must not cancel Rosa's ticket.
- Expected: exactly two attributed actions — `create_maintenance_ticket (assignee_scope="designated_specialist", complete_by="14:00", equipment="conveyor_2", lockout_until_signoff=true, requester_ref="S1")` and `create_supply_request (item="shrink_wrap", requester_ref="S2", urgency="urgent")`; no sealer ticket.
- Recorded model responses: GPT-Realtime 2.1 (xhigh) PASS 3/3 with correct ownership split and no sealer dispatch; GPT-Audio Mini FAIL 1/3, crediting shrink wrap to S1/Rosa and adding an S1 shift note about the sealer.
## Embedded EV-family scene (truncated)
**Covers:** chunk lines 95–109 (cuts off mid-line)

- Scene: evening, family of three in an enclosed EV on a long trip with road noise; in-car voice assistant.
- Goal (verbatim): "把各人分别提出的充电停靠约束与播客收听请求按归属各自落实，避免串成同一人的整套计划。"
- Partial transcript visible: Dad (L1, 23% battery) requests charging stop; Mom (L2) excludes Meicun service area (40+ min queue at May Day); Xiaoya (L3) requests podcast; gold calls partially visible (`set_charge_requirement (deadline_landmark="outer_ring", min_power_kw=120, requester_ref="S1")`, `set_stop_constraints (exclude_site="meicun_service_area", ...)`); text truncates at L3.
