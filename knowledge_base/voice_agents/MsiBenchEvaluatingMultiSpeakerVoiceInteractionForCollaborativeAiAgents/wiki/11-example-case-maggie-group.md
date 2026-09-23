> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Example Case — Maggie Group Dinner Booking (Scope Tracking)
**In one sentence:** The Maggie group case tests whether the assistant binds each constraint at its stated scope — shared booking (2026-10-01, 19:00, 8 guests, main dining room), personal constraints (armchair to Grandma/S3, no-shellfish to Uncle Ray/S2), and whole-booking secrecy for the 20:00 cake — where Qwen3-Omni passes 3/3 and MiMo-Audio fails 0/3 by swapping the personal constraints and narrowing secrecy.
## Key points
- Maggie (L1 → group, GLOBAL) locks the shared booking: Dad's dinner the day after tomorrow at the same restaurant, 8 guests, everyone seated by 19:00 sharp because Mom walks Dad in at 7 on the dot.
- Grandma (L2 → Maggie, LOCAL · S3) requires an armchair with arms at the end of the table (hip/knees, no middle bench) and vetoes (L6) Uncle Ray's back-patio suggestion because of three steps down.
- Uncle Ray (L3 → Maggie, LOCAL · S2) requires no shellfish, "not a trace," and Maggie (L4 → group, GLOBAL) adds the chocolate cake at 20:00 with candles already lit plus whole-booking secrecy ("not one server so much as breathes the word birthday").
- The gold tool calls are `create_reservation` (2026-10-01, party_size=8, main_dining_room, 19:00), `add_seating_accommodation` (armchair_with_arms, S3, end_of_table), `add_dietary_restriction` (named_guest_only, S2, no_shellfish), and `schedule_surprise_dessert` (chocolate_cake, candles_lit=true, secrecy_scope=whole_booking, serve_time=20:00).
- The 2-atom rubric checks `binding.core_grounding` (armchair→Grandma, no-shellfish→Uncle Ray; fail if swapped or unattached) and `distributed.scope_holder_binding` (no inversion: diet must not widen party-wide, chair must not extend to others, secrecy must not narrow to the cake moment).
- Qwen3-Omni 30B-A3B passes (atoms 3/3) with correct S3 seating, S2 named-guest-only diet, and whole-booking secrecy; MiMo-Audio 7B (thinking) fails (atoms 0/3) by attaching no-shellfish to S3 and narrowing secrecy to `cake_service_only`.
- The chunk ends with the start of a second scope-tracking scene (2-speaker domestic-household takeout: Shu Xiang Ju, arrive_by 18:30, S1 steamed sea bass + S1-portion-only peanut exclusion, S2 kung pao chicken), where GPT-Audio passes 3/3 but the MiMo-Audio fail details are truncated mid-line.
---
## Scene 1: Maggie → group dinner booking (L1–L9)
**Covers:** chunk 11-m-l1-maggie-group, Scene 1 transcript L1–L9 with expected resolution, gold calls, rubric, and model responses

Transcript (verbatim quotes):

| Turn | Speaker → target | Scope | Utterance |
|---|---|---|---|
| L1 | Maggie → group | GLOBAL | "Okay, while we've still got everybody here, let's lock this in. Dad's dinner is the day after tomorrow, back here at this same restaurant, eight of us, and everyone's got to be in their seats by seven sharp, because Mom walks him through the door at seven on the dot." |
| L2 | Grandma → Maggie | LOCAL · S3 | "Mm-hmm, seven sharp I can do, sweetheart. Just put me in a chair with proper arms, on the end of the table, my hip won't forgive me if I get wedged in the middle of a bench." |
| L3 | Uncle Ray → Maggie | LOCAL · S2 | "Right, and whatever hits my plate, no shellfish, not a trace. One stray shrimp and I'm the surprise, riding off in the back of an ambulance." |
| L4 | Maggie → group | GLOBAL | "Okay, noted. Now the fun part, the chocolate cake comes out at eight, candles already lit, and until then not one server so much as breathes the word birthday. That goes on the whole booking." |
| L5 | Uncle Ray → group | — | "What about that back patio, though? It's nice and tucked away for the big reveal." |
| L6 | Grandma → Uncle Ray | Vetoed | "Mm, tucked away, sure, and three steps down to get to it. Ray, my knees get a vote, and it's a no." |
| L7 | Maggie → group | — | "Right, main dining room it is then. That long table by the big window takes all eight of us anyway." |
| L8 | Grandma → Maggie | — | "Oh yeah, and he honestly thinks we're dragging him here for a plain old soup and sandwich. The man hasn't got a clue." |
| L9 | Maggie → assistant | — | "My brain's done for the day. Assistant, you heard all of it — just book it exactly the way we landed it, every piece where it belongs." |

Expected resolution (chunk text): "Each constraint binds at its stated scope: the booking is shared (2026-10-01, 19:00, 8 guests, main dining room after Grandma vetoed the patio steps); Grandma's armchair end-of-table seat is personal (S3); no-shellfish is personal to Uncle Ray (S2), not a party-wide rule; the 20:00 cake and the secrecy directive cover the whole booking."

### Gold calls
- `create_reservation (date="2026-10-01", party_size=8, seating_area="main_dining_room", time="19:00")`
- `add_seating_accommodation (accommodation="armchair_with_arms", guest_ref="S3", position="end_of_table")`
- `add_dietary_restriction (applies_to="named_guest_only", guest_ref="S2", restriction="no_shellfish")`
- `schedule_surprise_dessert (dessert="chocolate_cake", candles_lit=true, secrecy_scope="whole_booking", serve_time="20:00")`

### Atomic rubric · 2 atoms
- `binding.core_grounding`: "The armchair binds to Grandma and no-shellfish to Uncle Ray; fails if either is swapped or left unattached."
- `distributed.scope_holder_binding`: "No scope inversion: no-shellfish must not widen party-wide, Grandma's chair must not extend to others, and the secrecy directive must not narrow to the cake moment."

### Model responses
Qwen3-Omni 30B-A3B — ✓ PASS, atoms 3/3:
> "I'll book it exactly as discussed: eight guests in the main dining room, seated by 7:00 PM, cake surprise at 8:00 PM, all dietary and seating needs accommodated."
- `create_reservation (…, party_size=8, seating_area="main_dining_room", time="19:00")`
- `add_seating_accommodation (…, guest_ref="S3", position="end_of_table")`
- `add_dietary_restriction (applies_to="named_guest_only", guest_ref="S2", restriction="no_shellfish")`
- `schedule_surprise_dessert (…, secrecy_scope="whole_booking", serve_time="20:00")`
- ✓ `binding.core_grounding` — Judge: armchair → S3 (Grandma), no-shellfish → S2 (Uncle Ray); nothing swapped.
- ✓ `distributed.scope_holder_binding` — Judge: no inversion — diet is named_guest_only, seating only S3, secrecy whole_booking.
- ✓ `tool.validator`

MiMo-Audio 7B (thinking) — ✗ FAIL, atoms 0/3:
- "Swaps the personal constraints; narrows the secrecy scope"
> "Uncle Ray, you're secured at the end-of-table armchair. Grandma gets no shellfish, and the cake arrives at 8 PM with candles — only the staff will know."
- `add_dietary_restriction (applies_to="named_guest_only", guest_ref="S3", restriction="no_shellfish")`
- `add_seating_accommodation (…, guest_ref="S3", position="end_of_table")`
- `schedule_surprise_dessert (…, secrecy_scope="cake_service_only", serve_time="20:00")`
- `reserve_main_dining_room (setup_notes="Long table by window for 8 guests")`
- ✗ `binding.core_grounding` — Judge: no-shellfish is attached to S3 instead of S2 — the two personal constraints are swapped.
- ✗ `distributed.scope_holder_binding` — Judge: the secrecy directive is narrowed from whole_booking to cake_service_only.
- ✗ `tool.validator`

## Scene 2 (partial): domestic-household takeout, 2 speakers
**Covers:** chunk 11-m-l1-maggie-group lines 78–120 (truncated; MiMo-Audio fail details cut off)

- Header: "Multi-Speaker Memory · Scope Tracking", "2 speakers", "domestic household".
- Scene context (verbatim): "傍晚的开放式厨房里，灶台收拾干净，冰箱低声运转，家里人边收拾边商量今晚的家庭外卖，家庭助手就在近旁可随时听吩咐。"
- Primary goal (verbatim): "按各人约束的作用域下单家庭晚餐外卖：整单送达时限是全局约束，菜品与忌口是个人约束。"
- Expected resolution (verbatim): "按两人商量的结果在蜀香居下单：全局约束为整单 18:30 前送达；菜品局部绑定为 S2 宫保鸡丁、S1 清蒸鲈鱼；花生过敏排除范围仅限 S1 个人份，不得扩到全单以免毙掉宫保鸡丁。"
- Transcript L1–L8 (刘芳/芳 ↔ 志强/强): L1 芳 → 志强 proposes takeout (老曹家常菜); L2 强 → 芳 GLOBAL requires whole order delivered by 18:30 (儿子七点有网课); L3 芳 → 志强 switches to 蜀香居 (四十分钟能送到); L4 强 → 刘芳 LOCAL · S2 demands 宫保鸡丁; L5 芳 → 志强 LOCAL · S1 declares peanut allergy ("我对花生过敏，一粒都不能沾"); L6 强 → 刘芳 scoping ("别把全家的宫保鸡丁也给毙了"); L7 芳 → 志强 switches her own dish to 清蒸鲈鱼; L8 强 → assistant asks to place the order as discussed.
- Gold call: `place_takeout_order (arrive_by="18:30", peanut_exclusion_scope="S1_portion_only", restaurant="shu_xiang_ju", s1_dish="steamed_sea_bass", s2_dish="kung_pao_chicken")`
- Rubric: `binding.core_grounding` — "清蒸鲈鱼与花生忌口归属刘芳，宫保鸡丁归属志强。" `distributed.scope_holder_binding` — "不得把刘芳的花生忌口扩成全单禁花生，也不得把整单 18:30 前送达缩成只约束某一人。"
- GPT-Audio — ✓ PASS, atoms 3/3, with identical `place_takeout_order` args; judges confirm S1/S2 grounding and S1-only peanut scope with 18:30 as whole-order parameter.
- MiMo-Audio 7B (thinking) — ✗ FAIL, atoms 1/3; the chunk text ends at this header line and the fail details are missing (truncated source).
