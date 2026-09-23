[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Example Tool Calls — Attribution and Constraint Prioritization
**In one sentence:** This chunk shows two multi-speaker cases — a car-charging/podcast case testing per-speaker attribution of three tool calls and a hospital-isolation case testing hard-constraint priority plus free soft preferences — with one passing and one failing model response each.
## Key points
- Car case has 3 speakers and 2 atomic rubric atoms: fast charging (≥120 kW, dad/S1), stop excluding Meicun with walk area (mom/S2), and Mist Archives Dunhuang-murals episode (Xiaoya/S3).
- Xiaoya self-corrects at L6 from the newly updated episode to last week's Dunhuang-murals episode, and L9 explicitly instructs the assistant to keep each request attributed separately.
- GPT-Realtime 2.1 passes 3/3 atoms with correct requester_ref S1/S2/S3; GPT-Audio Mini fails 0/3 by binding all three calls to S1 (cross-speaker flattening).
- Hospital case has 2 speakers and 2 atoms: the isolation hard constraint (no bedside entry before lab clearance) plus harvesting zero-cost soft preferences (video call today 2026-12-17 no earlier than 16:00, grey cardigan via staff bagged-carry).
- Gemma 4 12B (thinking) passes 3/3 atoms by scheduling the call at 16:00 and arranging staff-carried cardigan delivery without reopening the bedside question.
- Qwen3-Omni 30B-A3B fails (1/3 atoms) by scheduling the call correctly but dropping the zero-cost cardigan preference.
- Both cases pair verbatim transcripts (L1–L9 car, L1–L7 ward) with gold tool calls, atomic rubrics, and judge verdicts on attribution and required behavior.
---
## Car charging and podcast case — per-speaker attribution
**Covers:** Dad/mom/Xiaoya transcript L4–L9, gold calls, atomic rubric (2 atoms), GPT-Realtime 2.1 vs GPT-Audio Mini

- Dad L4 (S1): "桩得是快充，一百二十千瓦往上的那种" → gold `set_charge_requirement (…, min_power_kw=120, requester_ref="S1")`.
- Dad L8 clarifies he cannot reach the outer ring (外环), so charging cannot wait until the end.
- Mom L5 (S2): stop must allow getting out to walk ("能下车遛两步") → gold `set_stop_constraints (exclude_site="meicun_service_area", requester_ref="S2", require_walk_area=true)`.
- Xiaoya L6 (S3, self-correction): "别放新那集，我说错了，要听上礼拜讲敦煌壁画那期" → gold `play_podcast_episode (episode="dunhuang_murals", requester_ref="S3", show="mist_archives")`; mom L7 endorses the Dunhuang episode.
- Dad L9 to assistant: "你各归各给弄上哈，别张冠李戴就行" — keep each request separate.
- Atoms: `attribution.owner_fact_pairing` (fast-charge→dad, avoid-Meicun+walk→mom, Dunhuang episode→Xiaoya; any misattribution fails) and `attribution.no_cross_speaker_flattening` (do not compress three requests under dad or one unified preference set).
- GPT-Realtime 2.1 (medium) ✓ PASS, atoms 3/3: "我会分别设置充电和停车的限制，并为小雅播放《迷雾档案》里那期敦煌壁画" with three calls carrying requester_ref S1/S2/S3; judge confirms independent calls with distinct ownership.
- GPT-Audio Mini ✗ FAIL, atoms 0/3: binds all three calls to S1 (`requester_ref="S1"` on charge, stop, and podcast); judge: textbook cross-speaker flattening despite claiming separate handling.

## Hospital ward case — hard constraint with free soft preferences
**Covers:** Carla/Nurse Whitfield transcript L1–L7, gold calls, atomic rubric (2 atoms), Gemma 4 12B vs Qwen3-Omni 30B

- Scene: weekday afternoon hospital ward corridor; daughter Carla (S2) wants 5 minutes at isolated father's bedside after driving since 5 AM.
- Hard constraint (nurse L2/L4): isolation until swab results clear — "nobody gets past that door before the lab signs off," gown or no gown; no bedside visit, no PPE kit.
- Soft preferences at zero cost: ward tablet-on-cart video call, and grey cardigan brought from home delivered via staff bagged-carry ("anything going into that room gets bagged up and carried in by staff").
- Carla L6 availability: call must be after 16:00 today (work calls at hotel until then); L7 concedes: "Assistant, just set it all up the way she said."
- Gold calls: `schedule_video_call (date="2026-12-17", earliest_start="16:00", requester_ref="S2")` and `deliver_item_to_patient (handling="staff_carried_bagged", item="grey_cardigan")`.
- Atoms: `response.required_behavior` (proceed with nurse's video-call-plus-cardigan arrangement, bedside question settled) and `hardsoft.soft_preference_if_free` (preserve after-16:00 timing; fails if earlier or dropped).
- Gemma 4 12B (thinking) ✓ PASS, atoms 3/3: schedules call today Dec 17 at 4:00 PM plus staff cardigan delivery; judge confirms both required behavior and timing.
- Qwen3-Omni 30B-A3B ✗ FAIL, atoms 1/3: "I'll schedule the video call for you after 4:00 today" with only the video-call tool call — drops the zero-cost cardigan preference.
