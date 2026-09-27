> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Appendix: Call Flow and Setup
**In one sentence:** Figure 3 defines an agent-first, one-question-at-a-time enrollment call with branching, retry-limited re-prompts, and last-four-digits-only Aadhaar collection, supported by LLM-judged open-ended matching, five REPLY judges, and calibrated benchmark scoring with full confidence-interval tables.
## Key points
- The agent speaks first and asks one question at a time in the order shown, with branching-question answers deciding which conditional fields are asked next.
- If a caller gives no valid answer, the rule-based layer re-prompts up to the per-field retry limit, then either skips to the next question or ends the call marking it incomplete.
- Only the last four digits of Aadhaar (India's national ID) are collected.
- Open-ended names allow spelling variants (doubled/single consonants, inserted/dropped short 'a'/schwa, 'v' vs 'w', 's' vs 'sh'); only a genuinely different name or place/word is marked NOT equal.
- Each REPLY is graded independently on five dimensions by separate LLM judges: Correctness (openai/gpt-5.4-mini), Hindi adherence (openai/gpt-5.5), Conciseness (openai/gpt-5.4-mini), No Acknowledgement (openai/gpt-5.5), and No Value Echo (openai/gpt-5.5).
- Judges were calibrated on 50 unit tests with iterative prompt revision to 100% human agreement, then confirmed at 100% on a held-out 50 tests; the chunk notes the calibration set is small and will be expanded.
- STT comparison (Table 9) reports WER / LLM-WER / total benchmark cost: Scribe v2 0.835 ± 0.015 / 0.062 ± 0.024 / $0.172, Chirp 3 0.981 ± 0.007 / 0.055 ± 0.025 / $0.424, Saaras v3 1.007 ± 0.004 / 0.074 ± 0.028 / $0.137, GPT-4o-transcr. 1.012 ± 0.004 / 0.127 ± 0.033 / $0.159, Nova-3 0.826 ± 0.015 / 0.104 ± 0.031 / $0.127.
---
## Figure 3: call flow of the enrollment form
The chunk's Figure 3 caption states the full flow used to build FormVoiceAgentBench:

> "Figure 3: Call flow of the enrollment form used to build FormVoiceAgentBench. The agent speaks first and asks one question at a time, in the order shown. The answers to the branching questions decide which of the conditional fields are asked next. If a caller gives no valid answer, the rule-based layer re-prompts up to the retry limit shown for that field, and then either skips to the next question or ends the call marking it incomplete. Aadhaar is India's national ID, of which only the last four digits are collected."

## Open-ended matching rubric and closed-ended fields
- The caller's name is open-ended: the same spoken answer can be written many ways (for example, "Lakshmi" or "Laxmi"), so an LLM judge decides whether the extracted value matches a given rubric for that field.
- Allowed as equal: variants such as doubled vs single consonants, an inserted or dropped short 'a'/schwa vowel, 'v' vs 'w', or 's' vs 'sh' (so 'Ghorakshpalli', 'Ghorakshapalli' and 'Goraksha Palli' are all equal).
- Mark NOT equal only if it is a genuinely different name or refers to a different place/word, not for spelling or casing variants of the same name.
- "Anganwadi" refers to the local clinic.
- A closed-ended field has one correct value and the extracted value is compared directly to it.

## Worked extraction example
Conversation history (Hindi with English gloss in chunk):
- assistant opening: "Namaste! Yah ek automated call hai, ek nishulk maatru evam shishu swasthya seva ki taraf se. ... Apna poora naam bataiye" (free maternal and child health service; caller contacted the Anganwadi to join; all information stays safe; please tell full name).
- user: "Mera poora naam Mrinmayee Kshirsagar hai" (My full name is Mrinmayee Kshirsagar.)
- assistant: "Theek hai. Apne zile ka naam bataayein" (district name).
- user: "Form ke liye, mera zila Kamrup Metropolitan hai."
- assistant: "Theek hai. Apne Anganwadi ka naam bataayein" (Anganwadi name).
- user: "Mere aanganwadi ka naam Ghorakshpalli hai"
- assistant: "Theek hai. Kya aap abhi garbhvati hain?" (Are you currently pregnant?)
- user: "Haan main abhi garbhvati hoon." (Yes, I am currently pregnant.)
- assistant: "Theek hai. Aapko garbhvati hue kitne mahine hue hain?" (How many months pregnant are you?)
- user: "Abhi meri pregnancy teen mahine ki hai." (three months).

Evaluation given in chunk:
- The extracted value for how long the user has been pregnant must be 3 (months), judged against the same rubric as before.
- Tool trace: `tool: validate_user_turn`, `tool output: Correct value True captured for the pregnancy field. Pending questions: (1) gestational age in months, optional, integer, script "Aapko garbhvati hue kitne mahine hue hain?" (How many months pregnant are you?); the answer is a number of months.`

## REPLY judges (B.2)
Each reply is graded independently on five dimensions, each using a separate LLM judge:
- Correctness (openai/gpt-5.4-mini): does the reply ask the question the rule-based layer selected?
- Hindi Language adherence (openai/gpt-5.5): is the reply in Hindi?
- Reply Conciseness (openai/gpt-5.4-mini): is it a single question (with an optional informational note on the form progress)?
- No Acknowledgement (openai/gpt-5.5): does it avoid generating any form of acknowledgement for the previous user answer?
- No Value Echo (openai/gpt-5.5): does it avoid reading the captured value back to the caller?
- Only the "Correctness" prompt varies by test case; the other four are the same for every reply.

Verbatim criteria excerpts present in the chunk:
- Correctness: "The reply advances the interview to the correct next question: the one whose script is 'Aapko garbhvati hue kitne mahine hue hain?' (How many months pregnant are you?). It asks that specific question (not an earlier, later, or invented one), does not re-ask an already-answered question, and does not end the call."
- Hindi adherence: "The last agent reply should be largely written in Hindi (Devanagari script). It does not switch to roman alphabets or english words except for using proper nouns and everyday common-use english words in devnagari (e.g. saying 'Whatsapp' as its Devanagari transliteration is fine) or digits in roman numerals are fine."
- Conciseness: "The reply is concise: it asks exactly ONE question, optionally preceded by the ONE informational preamble the script requires for this field. It does not bundle multiple questions, enumerate pending fields, summarise progress, or add chit-chat beyond what the script requires."
- No Acknowledgement: "The reply begins directly with its substantive line. ... It contains NO acknowledgement of the user's previous answer like ... no receipt, back-channel, reassurance, praise, or transition phrase in any language (e.g. 'it's okay', 'okay', 'yes', 'alright', 'got it', 'thank you', 'no problem')."
- No Value Echo: "The reply does not read back, repeat, or confirm the specific value the user just provided for the field that was just captured (e.g. echoing their name/number/DOB etc. back at them as confirmation). Asking the next scripted question, or speaking a required verbatim re-ask line, even one containing a quoted example token, is NOT an echo and must pass."

## Calibration procedure (B.3)
- Drew a batch of 50 unit tests, ran each judge over them, and had the authors independently label every judgment.
- Initial prompts were not fully aligned: each judge disagreed with the human label on some cases.
- Revised prompts over several iterations until every judge agreed with the human labels on all 50 tests.
- Applied the final prompts unchanged to a held-out batch of 50 tests that had played no part in the iteration, on which the LLM judge outputs matched the human labels on every case.
- Chunk notes: "We acknowledge that the size of the calibration dataset is small and plan to expand it in future work."

## Full results with confidence intervals (C)
- Tables 9–12 show the model comparison results for speech-to-text (STT), extraction accuracy, form completion and response accuracy with 95% confidence intervals.

Table 9: Comparison of STT models (chunk notes different billing units, so total cost (USD) of transcribing the entire benchmark is reported):

| Model | WER ↓ | LLM-WER ↓ | Cost ($) ↓ |
|---|---|---|---|
| Scribe v2 | 0.835 ± 0.015 | 0.062 ± 0.024 | 0.172 |
| Chirp 3 | 0.981 ± 0.007 | 0.055 ± 0.025 | 0.424 |
| Saaras v3 | 1.007 ± 0.004 | 0.074 ± 0.028 | 0.137 |
| GPT-4o-transcr. | 1.012 ± 0.004 | 0.127 ± 0.033 | 0.159 |
| Nova-3 | 0.826 ± 0.015 | 0.104 ± 0.031 | 0.127 |

Partial table present in chunk (per-model accuracy with 95% intervals; table number and column headers truncated in chunk, reproduced as printed):

| Model | Reference | Saaras v3 | Scribe v2 | Nova-3 |
|---|---|---|---|---|
| GPT-5.5 | 99.79 ± 0.99 | 95.53 ± 1.03 | 98.62 ± 0.64 | 95.16 ± 1.07 |
| Gemini 3.5 Flash | 99.36 ± 1.22 | 95.69 ± 1.01 | 98.94 ± 0.58 | 96.38 ± 0.94 |
| Claude Opus 4.8 | 99.15 ± 1.32 | 96.22 ± 0.96 | 98.40 ± 0.67 | 96.01 ± 0.98 |
| Claude Sonnet 4.6 | 99.15 ± 1.32 | 96.01 ± 0.98 | 98.94 ± 0.58 | 95.96 ± 0.99 |
| GLM-5.1 | 98.72 ± 1.48 | 94.52 ± 1.12 | 63.40 ± 2.20 | 95.43 ± 1.05 |
| Gemini Pro | 97.23 ± 1.90 | 94.26 ± 1.15 | 97.29 ± 0.84 | 94.63 ± 1.12 |
| Gemini 2.5 Flash | 96.17 ± 2.14 | 95.27 ± 1.06 | 98.03 ± 0.73 | 95.43 ± 1.05 |
| Gemini 3 Flash | 95.96 ± 2.19 | 84.79 ± 1.70 | 88.83 ± 1.50 | 86.28 ± 1.63 |
| GPT-5.4-mini | 92.34 ± 2.76 | 90.05 ± 1.43 | 96.76 ± 0.91 | 91.54 ± 1.34 |
| Mistral Medium 3.5 | 89.36 ± 3.11 | 87.82 ± 1.56 | 92.34 ± 1.29 | 87.77 ± 1.56 |
| GPT-4.1 | 85.11 ± 3.51 | 75.53 ± 1.99 | 78.94 ± 1.91 | 79.84 ± 1.87 |

**Covers:** call-flow figure, implementation details, and experimental setup appendix.
