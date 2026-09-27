> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Benchmark Form and Simulated Users
**In one sentence:** The benchmark defines an enrollment form with skip/end failure handling and conditional fields, five simulated users with LLM-generated transcripts recorded under four acoustic conditions, and assembles 960 calls that yield 1,880 unit tests per LLM.
## Key points
- The enrollment form covers Name, District, Clinic name, pregnancy/child fields, clinic-linked and WhatsApp phone numbers, and Aadhaar last 4 digits, each with an example answer and an on-fail action of skip or end.
- Indented fields are conditional on the parent response, and after a few failed retries the agent either skips to the next field or ends the call per Table 1.
- Five simulated user profiles each have fixed personal details, with three representations per field: the value (e.g. "Sunita Devi"), a natural spoken transcript (e.g. "My name is Sunita Devi"), and its recording, generated sequentially by GPT-5.5 under ARMMAN constraints.
- District names were deliberately selected from outside the pilot state, with phonetically hard names/districts and numbers with many spoken variations to stress-test transcription.
- Each transcript was recorded in four versions (ideal plus three variations: background noise, random close/far microphone distance, random fast/slow pace) by five native Hindi-speaking women aged 18–35 from Uttar Pradesh and Maharashtra, with supervisor checks on every clip.
- Each simulated user follows 2 × 3 × 4 × 2 = 48 distinct form paths, giving 5 × 48 = 240 calls, and recording each under four acoustic conditions yields 240 × 4 = 960 calls with a single acoustic condition kept throughout each call.
- Deduplicating tests with identical inputs across all 960 calls yields 1,880 EXTRACT unit tests and 1,880 REPLY unit tests, of which 920 require a reply and 960 check end-call decisions.
- Closed-ended fields and skip flags are scored by exact match while open-ended names and acknowledgements use a calibrated binary LLM judge, and REPLY replies are graded across five dimensions (right question, Hindi adherence, single line, no acknowledgment, no echoing).
---
## Enrollment form (Table 1)
| Field | Example answer | On fail |
|---|---|---|
| Name | Sunita Devi | skip |
| District | Mayurbhanj | end |
| Clinic name | City Clinic | skip |
| Pregnant? | yes / no | end |
| yes: Gestational age | 5 months | end |
| no: Child's name | Aarav | end |
| Child's DOB | 15-04-2025 | end |
| Phone linked to clinic? | yes / no | skip |
| no: Number linked | 9876543210 | skip |
| Phone linked to WhatsApp? | yes / no | skip |
| no: WhatsApp number | 9876543210 | skip |
| Aadhaar last 4 digits | 4321 | skip |

> "When a caller fails to give a valid answer after a few retries, the agent either skips to the next field (skip) or ends the call (end). Indented fields are conditional: whether they are asked depends on the parent field's response. Aadhaar is India's national ID."

## Simulated users and transcripts (3.2)
- Five simulated user profiles, each with fixed personal details corresponding to the fields to capture.
- Per field: value, desired form entry / ground truth for form completion ("Sunita Devi"); reference transcript, a naturally spoken rendering ("My name is Sunita Devi"); and the recording of that transcript.
- Value and transcript generated sequentially by an LLM under field-specific constraints defined with ARMMAN: phonetically hard names and district names, numbers with many spoken variations; district names from outside the pilot state.
- Optional fields get two linguistic transcript variants: one with the value, one where she says she does not know it; generation uses "OpenAI's GPT-5.5 (OpenAI 2026)".

## Audio data collection (3.3)
- Recordings mimic public-clinic conditions with three acoustic variations plus the ideal condition, giving four recordings per transcript: background noise (ambient chatter and nearby speakers), microphone distance (close or far, random), speaking pace (fast or slow, random).
- Five native Hindi speakers matching the target demographic: all female, aged 18–35, from Uttar Pradesh and Maharashtra; trained with sample recordings and directives such as "record in a noisy environment, or keep the mic at least 25 cm away, or speak slowly".
- A separate set of human supervisors listened to every clip to ensure requirements were met.

## From transcripts to calls (3.4)
- Each call stitches one simulated user's transcripts with one recording per field; form branching means one simulated user produces multiple calls (e.g. one pregnant, one not); calls never mix values across users; one acoustic condition per call.
- Path count per user: 2 pregnancy branches × 3 clinic-link branches (linked, not linked with correct value, not linked but unable to recall) × 4 WhatsApp branches (same, not same and answered, not same but unable to recall, cannot recall if same) × 2 Aadhaar branches (answered or not known) = 48; totals 240 calls, 960 with acoustic conditions.
- EXTRACT unit tests: per turn, latest user response plus preceding conversation history as input, expected form values as ground truth; accurate extraction passes both exact-match checks and LLM judgments; mean extraction accuracy reported.
- REPLY unit tests add the rule-based layer's tool call (expected extraction values passed through validation/flow-control) to isolate response accuracy; REPLY either phrases the next question or ends the call (tool call, exact match); accurate response passes all five LLM judgments or ends the call at the right time; mean response accuracy reported.

**Covers:** Table 1 and Sections 3.2–3.4 (plus the Section 4 evaluation-design text as present in this chunk)
