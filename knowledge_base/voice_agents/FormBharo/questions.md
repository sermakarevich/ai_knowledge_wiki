---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: FormBharo: Designing and Evaluating a Voice Agent for Conversational Form Filling in Rural India

### Q1. Why does FormBharo target spoken phone-call form filling, and who is the pilot population?

> [!tip]- Answer
> In India almost every social benefit starts with a form, yet more than half the women in the lowest wealth quintile cannot read at all, so enrollment falls to frontline health workers signing up beneficiaries one conversation at a time. Documentation already consumes much of these workers' day across dozens of overlapping systems, capping enrollment at worker capacity rather than need. FormBharo is piloted with ARMMAN to enroll low-income, Hindi-speaking mothers in antenatal and postnatal care by voice, with nothing to read, type, or install. See [[wiki/01-introduction-and-motivation|Introduction and Motivation]].

### Q2. What is the paper's central evaluation claim about component-level versus end-to-end accuracy?

> [!tip]- Answer
> Form completion drops by up to ~41 percentage points when LLMs receive error-prone real-speech transcripts instead of reference transcripts, and turn-level extraction leaders reorder once components are chained. GPT-5.5 leads turn-level extraction on reference transcripts (99.8%) but ranks lower on form completion, because errors both propagate and cancel across the pipeline. Hence model choice emerges only through end-to-end evaluation, balanced via Pareto-based weighted-sum scalarization across accuracy, cost, and latency. See [[wiki/01-introduction-and-motivation|Introduction and Motivation]].

### Q3. How is work split between LLMs and rule-based logic in the FormBharo pipeline?

> [!tip]- Answer
> LLMs are used only where they add value: the EXTRACT LLM turns the STT transcript plus history into structured field values (categorical fields as option indices) plus a short latency-masking acknowledgement, and the REPLY LLM phrases the next question naturally for TTS or ends the call. Everything else stays rule-based: validation, retries, branching, next-question choice, and the form state as single source of truth. VAD gates turn-taking, and interruptions terminate the running turn so the agent waits for the caller to finish. See [[wiki/02-system-architecture|System Architecture: Hybrid LLM plus Rule-Based Pipeline]].

### Q4. What happens when an extracted value is missing, invalid, or declined?

> [!tip]- Answer
> The rule-based layer checks each value against field-specific guards such as minimum length, 10 digits for a phone number, or a past-only date, then consults per-field retry limits. If retries remain it passes the validation error plus history to REPLY to re-ask; a required field that exhausts retries ends the call, while an optional field is skipped or ends the call per its setting. A caller decline or "don't know" is detected by EXTRACT as a skip flag and skips the field without retries, and branching (e.g. gestational age only if pregnant) is evaluated rule-side and injected into REPLY as a tool call. See [[wiki/02-system-architecture|System Architecture: Hybrid LLM plus Rule-Based Pipeline]].

### Q5. What does the 12-field enrollment form contain, and what do skip versus end mean?

> [!tip]- Answer
> The form covers Name, District, Clinic name, pregnancy status with conditional gestational age or child's name/DOB branches, clinic-linked and WhatsApp phone numbers with their conditional number fields, and Aadhaar last 4 digits. Indented fields are conditional on the parent response, and after a few failed retries the agent either skips to the next field (skip) or ends the call marking it incomplete (end) per Table 1. Only the last four digits of Aadhaar, India's national ID, are ever collected. See [[wiki/03-benchmark-form-and-users|Benchmark Form and Simulated Users]].

### Q6. How are the 960 benchmark calls built, and how is EXTRACT scored?

> [!tip]- Answer
> Five simulated user profiles each carry fixed details with a value, a GPT-5.5-generated natural spoken transcript, and a recording, with districts from outside the pilot state and phonetically hard names and numbers to stress transcription. Each user follows 2 x 3 x 4 x 2 = 48 form paths (240 calls), each recorded under four acoustic conditions (ideal, background noise, random mic distance, random pace) for 960 calls with one condition per call. Deduplication yields 1,880 EXTRACT unit tests scored by exact match for closed-ended fields and skip flags and by a calibrated binary LLM judge for open names and acknowledgements. See [[wiki/03-benchmark-form-and-users|Benchmark Form and Simulated Users]].

### Q7. Why is Scribe v2 selected for STT, and how does real speech reorder extraction rankings?

> [!tip]- Answer
> Models are ranked by LLM-WER rather than WER because the metrics disagree (Nova-3 has the best WER yet second-worst LLM-WER); Chirp 3 leads LLM-WER but costs at least twice any rival and GPT-4o-transcribe is least accurate, so both are eliminated. On reference transcripts extraction saturates (GPT-5.5 99.79%, Gemini 3.5 Flash 99.36%), but under real speech the leaderboard changes, with best real-speech accuracy 98.94% (Gemini 3.5 Flash and Claude Sonnet 4.6 on Scribe v2) and GLM-5.1 collapsing ~35 points. Scribe v2 is selected for the strongest downstream medians (97.29% extraction, 91.84% completion) and smallest drops versus reference. See [[wiki/04-evaluation-and-results|Evaluation and Model Selection]].

### Q8. How does the rule-based layer both help and fail to save form completion, and which EXTRACT and REPLY models are selected?

> [!tip]- Answer
> The rule-based layer normalizes some errors (e.g. Gemini 3 Flash at 95.96% extraction yet 100% completion on reference via numeric-as-string fixes), letting smaller cheaper models match frontier ones, but median completion still drops more than extraction (7.38 points on Scribe v2, up to ~41 worst-case for GLM-5.1) as uncorrected errors accumulate. With Scribe v2 fixed, p95-below-5s and above-90%-completion filtering plus weighted-sum scalarization (w_l = 0.1) selects Gemini 3.5 Flash for EXTRACT, trailing Claude Sonnet 4.6 by 0.51 points at less than half the per-turn cost. For REPLY, errors propagate a median 2.23 points, and GPT-5.4-mini is selected over Gemini 3 Flash, ranking highest throughout 0.5 <= w_a <= 0.9. See [[wiki/04-evaluation-and-results|Evaluation and Model Selection]].

### Q9. How are EXTRACT outputs judged, and what passes the acknowledgement and name criteria?

> [!tip]- Answer
> Each extracted field is scored by exact match or by an openai/gpt-5.4-mini LLM judge at temperature 0 receiving conversation history plus output and returning a boolean per the LLM-as-a-judge paradigm. The acknowledgement passes with any real-word receipt, back-channel, reassurance, praise, or transition phrase in any language (thik hai, samajh gaya, "got it"); only a missing acknowledgement or non-lexical filler fails. The name passes when it refers to the same spoken name as "Mrinmayee Kshirsagar", tolerating casing, spacing, and reasonable romanisation variants such as 'ksh'. See [[wiki/05-reply-generation-and-examples|Reply Generation and Examples]].

### Q10. What five dimensions grade each REPLY, and how were the judges calibrated?

> [!tip]- Answer
> Each reply is graded independently by separate judges: Correctness (gpt-5.4-mini, asks the rule-selected question), Hindi adherence (gpt-5.5, Devanagari), Conciseness (gpt-5.4-mini, exactly one question), No Acknowledgement (gpt-5.5), and No Value Echo (gpt-5.5, never reads the captured value back). Only the Correctness prompt varies per test case; the other four are fixed, and the call flow is agent-first, one question at a time, with retry-limited re-prompts then skip or incomplete-end. Judges were revised iteratively to 100% human agreement on 50 unit tests and confirmed at 100% on a held-out 50, though the authors note the calibration set is small. See [[wiki/06-appendix-call-flow-and-setup|Appendix: Call Flow and Setup]].

### Q11. A clinic operator asks whether to deploy the cheapest accurate configuration today or wait for a larger calibration and multi-condition study — what do you recommend?

> [!tip]- Answer
> Recommend deploying the paper's Pareto-filtered pick (Scribe v2, Gemini 3.5 Flash for EXTRACT, GPT-5.4-mini for REPLY) only as a constrained pilot, since Table 13 shows Gemini 3.5 Flash leads only for w_a 0.50–0.61 while Claude Sonnet 4.6 wins above 0.62, so the "best" config flips with accuracy weighting. Insist on expanding the 50+50 judge calibration, testing mixed acoustic conditions within a call, and re-running end-to-end completion before scale-up, because confidence intervals reflect item variation from single runs of nondeterministic hosted APIs. Treat the cost saving as provisional until those gaps are closed. See [[wiki/07-appendix-detailed-tables|Appendix: Detailed Tables]].
