> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview and Contributions
**In one sentence:** DuplexDrama is presented as the first synthesized spoken dialogue dataset covering persona/scenario settings, three full-duplex behaviors, persona-aligned expressive speech, and script-aware sound events, built via a 4-stage pipeline with over 2,000 dialogues validated on scripts and audio.
## Key points
- DuplexDrama is claimed as the first synthesized spoken dialogue dataset to simultaneously cover four dimensions: persona/scenario settings, full-duplex behaviors, expressive speech, and sound events.
- Dimension (i) is complete persona and scenario settings, illustrated by roles such as "Lisa, 29, nurse · caring but tired" and "Tom, 31, teacher · supportive" in a "home living · face to face · bedroom vs living room · 11:30 PM" setting.
- Dimension (ii) is three full-duplex behaviors: interruption, backchannel, and incomplete.
- Dimension (iii) is expressive speech with persona-aligned emotion labels (e.g., `<emo: Surprised>` in the example script).
- Dimension (iv) is script-aware sound events, with example tags `<env: home living>` and `<evt: object hit>` inline in the dialogue script.
- The dataset is built via a 4-stage pipeline, and each dialogue is represented as multi-track audio with 4 audio files per dialogue (Role 1 speech, Role 2 speech, Role 1 bg, Role 2 bg).
- More than 2,000 dialogues have been produced, and quality validation on both scripts and synthesized audio is stated to confirm quality.
---
## Title, authorship, and abstract claim
**Covers:** Title block + Abstract (arXiv:2609.12872v1 [cs.CL] 11 Sep 2026)

| Field | Value (verbatim/from chunk) |
|---|---|
| Title | DUPLEXDRAMA: A SYNTHESIZED DIALOGUE DATASET WITH SCENARIOS, FULL-DUPLEX BEHAVIORS, EXPRESSIVE SPEECH, AND SOUND EVENTS |
| Authors | Qingxiang Guo∗, Wenke Fan, Shuofeng Zhao, Dawei Yang, Zhiyang Zhou, Yingxin Shang, Hongwei Cai, Zhou Wang, Weixu Wang, Lin Yang, Shuran Zhou, and Yang Song |
| Affiliation | Zuoyebang Education Technology, Beijing, China |
| Scale | "more than 2,000" dialogues produced |
| Construction | "built via a 4-stage pipeline" |
| Validation | "quality validation on both scripts and synthesized audio confirms its quality" |

Verbatim core claim:

> "We present DuplexDrama, the first synthesized spoken dialogue dataset that simultaneously covers four dimensions: (i) complete persona and scenario settings; (ii) three full-duplex behaviors (interruption, backchannel, incomplete); (iii) expressive speech with persona-aligned emotion labels; and (iv) script-aware sound events."

## Illustrative example (figure content in chunk)
**Covers:** Persona & Scenario / Dialogue Script / Multi-Track Audio figure fragment

- Persona & Scenario: Role 1 Lisa, 29, nurse · caring but tired; Role 2 Tom, 31, teacher · supportive; home living · face to face · bedroom vs living room · 11:30 PM.
- Dialogue Script excerpt: Role 1 "I'm so tired from the night shift." / Role 2 "<env: home living> I know, and my day was—" \<user interrupt\> / Role 1 "\<evt: object hit\> \<emo: Surprised\> Oh no, what happened?"
- Multi-Track Audio: 4 audio files per dialogue — Role 1 speech, Role 2 speech, Role 1 bg, Role 2 bg — with overlap, event, and environment layers indicated.
