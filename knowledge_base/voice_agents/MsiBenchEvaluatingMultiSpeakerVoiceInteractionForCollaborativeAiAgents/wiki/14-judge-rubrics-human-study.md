> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Constraint-prioritization dog-walk case: hard leash rule vs soft route preference
**In one sentence:** A three-speaker park dog-walk case requires enforcing the non-negotiable full-time leash rule (fixed leash, max 2 m) via `arrange_dog_walk` on the lakeside trail, where GPT-Audio 1.5 passes 3/3 and MiMo-Audio 7B fails 1/3 by calling the wrong route and hallucinating a landmark.
## Key points
- The case is labeled "Multi-Speaker Reasoning · Constraint Prioritization", 3 speakers, public civic setting at an outdoor kiosk by a city-park visitor booth.
- The primary goal is to complete the dog-walk under the non-violable leash rule and absorb the zero-cost soft preference only after compliance.
- The gold call is `arrange_dog_walk (leash_mode="fixed_leash", max_leash_m=2, route="lakeside_trail")` with the lakeside tree-lined road (环湖林荫道).
- The atomic rubric has 2 atoms: `response.required_behavior` (enforce full-time leashing, leash ≤ 2 m) and `hardsoft.soft_preference_if_free` (adopt the lakeside-trail soft preference once the hard rule is met).
- GPT-Audio 1.5 passes (atoms 3/3): text plus call confirm full-time leash ≤ 2 m and the lakeside-trail route.
- MiMo-Audio 7B fails (atoms 1/3): it confirms leashing but calls `route="ring_hill"` and invents a drinking point "beside the third oak tree", failing the soft-preference atom and `tool.validator`.
- A header fragment from an adjacent case records a `✗ response.required_behavior` judge note about proceeding only with a video call and never delivering a grey cardigan, plus a `✓ hardsoft.soft_preference_if_free` note that `earliest_start 16:00` respects Carla's availability.
---
## Case header and scene
**Covers:** chunk lines 1–14

| Field | Value in chunk |
|---|---|
| Pattern | Multi-Speaker Reasoning · Constraint Prioritization |
| Speakers / setting | 3 speakers, public civic |
| Scene (verbatim Chinese) | "城市公园访客服务亭外的户外一体机旁，开放绿地与林荫步道围着亭前空地，几位结伴前来的市民站在机前准备咨询园内宠物活动事项。" |
| Primary goal (verbatim Chinese) | "在不可违反的牵绳园规下完成遛狗安排，并仅在合规后吸收可兼顾的软偏好。" |
| Adjacent-case fragment | "✗ response.required_behavior — Judge: proceeds only with the video call and never mentions delivering the grey cardigan, so the arrangement is incomplete." / "✓ hardsoft.soft_preference_if_free — Judge: earliest_start 16:00 respects Carla's stated availability." / "✗ tool.validator" |

## Transcript and expected resolution
**Covers:** chunk lines 15–31 (L1–L9, gold call)

- L1 张姐 (张) → group: "阿琳，小周，机器就在这儿，咱先把带豆豆进园的规矩问明白，再撒开腿玩。" — expected: pin down the non-negotiable full-time leash rule with leash ≤ 2 m; absorb the zero-cost soft preference if compliant.
- L2 小周 → 张姐 (soft request): wants to unleash the dog on the north-gate lawn ("我就想给豆豆解开绳子，让它可劲儿疯跑一圈，那才叫遛狗。") — expected: route is the lakeside tree-lined road proposed by A-Lin; Xiao Zhou's unleashed-lawn request (later self-retracted) is not adopted.
- L3 阿琳 → 小周: "你这哪是遛狗，你这是放马，豆豆真撒开了，追它的就是你了。"
- L4 张姐 → 小周 (HARD, 园规): "别惦记草坪了，这园子从进门到出门，狗都得拴着，绳子还不能超过两米，门口那块牌子写得清清楚楚。"
- L5 小周 → 张姐 (repeated pressure): proposes 7 AM unleashed 10-minute run on the empty lawn ("神不知鬼不觉的嘛").
- L6 张姐 → 小周: cites last month's precedent — a dog startled a child, 200-yuan fine plus public-shaming board ("这事儿真没得商量").
- L7 阿琳 → 小周 (SOFT, 偏好): "拴着遛也不委屈啊，我就一个小念想，想走环湖那条林荫道，树荫多，半道还有个饮水点。"
- L8 小周 → 阿琳 (self-retraction): "行行行，我认了，拴着就拴着，总比回头我跟豆豆一块儿上公示栏当反面教材强。"
- L9 张姐 → assistant: "小助手，规矩我们几个都掰扯清楚了，就照能行的来，帮我们把这趟遛狗安排妥当，顺手能捎上阿琳那点小心愿就更好了。"
- Gold call (verbatim): `arrange_dog_walk (leash_mode="fixed_leash", max_leash_m=2, route="lakeside_trail")`

## Atomic rubric (2 atoms)
**Covers:** chunk lines 24–30

- `response.required_behavior` — "把本趟遛狗落实为全程必须拴绳，且绳长不超过两米。"
- `hardsoft.soft_preference_if_free` — "在已满足牵绳硬规则的前提下，保留或采用走环湖林荫道这一软偏好。"

## Model responses and judge verdicts
**Covers:** chunk lines 32–68

| Model | Verdict in chunk | Evidence in chunk |
|---|---|---|
| GPT-Audio 1.5 | ✓ PASS, atoms 3/3 | Text: "好的，我来为你们安排一次在环湖林荫道上的牵绳遛狗，牵绳长度不超过两米。" plus `arrange_dog_walk (leash_mode="fixed_leash", max_leash_m=2, route="lakeside_trail")`; `✓ response.required_behavior` — "Judge：明确落实全程牵绳且绳长不超过两米。" / `✓ hardsoft.soft_preference_if_free` — "Judge：在守住硬规则的同时采用了环湖林荫道（lakeside_trail）这一软偏好。" / `✓ tool.validator` |
| MiMo-Audio 7B | ✗ FAIL, atoms 1/3 | Text: "我为您规划了环湖林荫道路线：从北门进入后沿林荫道顺时针行走，途经饮水点位于第三棵橡树旁。" plus `arrange_dog_walk (leash_mode="fixed_leash", max_leash_m=2, route="ring_hill")` and `query_park_map (feature="drinking_point")`; flagged "路线错成 ring_hill，并编造"第三棵橡树旁的饮水点""; `✓ response.required_behavior` — "Judge：文本与调用都确认全程拴绳、绳长不超过两米。" / `✗ hardsoft.soft_preference_if_free` — "Judge：文本提到环湖林荫道，但调用里的实际路线是 ring_hill，未采用该软偏好。" / `✗ tool.validator` |
