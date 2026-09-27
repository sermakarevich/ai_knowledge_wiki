> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Reply generation and examples: enrollment flow and EXTRACT judges
**In one sentence:** This chunk shows the full enrollment-form call flow with retry/skip logic and Hindi scripts, and defines LLM-as-a-judge scoring for EXTRACT fields including acknowledgement and name criteria using openai/gpt-5.4-mini at temperature 0.
## Key points
- The full call flow of the enrollment form is shown in Figure 3, covering name, district, clinic name, pregnancy status, gestational age, child's name/DOB, clinic-linkage and WhatsApp numbers, and Aadhaar last 4 digits with Retry 1 / Retry 2 / skip-to-next-question logic.
- All LLM judges receive the conversation history together with the agent output being graded and produce a boolean score for whether the output adheres to the judge criteria, following the LLM-as-a-judge paradigm (Zheng et al. 2023), with temperature set to 0 for every LLM judge inference.
- Each extracted field is scored either by exact match or by an LLM judge (Table 8), as is the acknowledgement the agent emits alongside the extraction, and openai/gpt-5.4-mini is used as the judge model.
- The turn is scored on the extraction call the agent makes: the caller's name is open-ended and sent to an LLM judge, and the acknowledgement is judged against a rubric since it has no single correct answer.
- Acknowledgement passes with any real-word receipt, back-channel, reassurance, praise, or transition phrase in any language (e.g. thik hai, achcha, ji haan, samajh gaya, koi baat nahi, "okay", "yes", "alright", "got it", "thank you", "no problem"); only a missing acknowledgement or non-lexical sound/filler fails.
- Name passes when the captured value refers to the SAME name as "Mrinmayee Kshirsagar" when read aloud, treated as EQUAL when differing only by letter casing, leading/trailing or internal word spacing, or reasonable alternative romanisation/transliteration of the same spoken Hindi name (e.g. 'ksh').
- The Hindi intro script introduces a free maternal and child health service via Anganwadi contact, asks questions by voice, reassures that "Aapki di gayi saari jaankari hamare saath surakshit rahegi", and prompts "Apna poora naam bataiye", with mid-call ("Now only 3 questions are left."), last-question ("This is the last question."), ending ("Thank you for sharing. We will connect you to the service soon."), and incomplete-end ("Sorry, we could not record your information now, so the call is ending. Thank you.") scripts.
---
## Enrollment call flow (Figure 3)
Start the Call then Intro Script:
> "Hello! This is an automated call from a free maternal and child health service. You contacted the clinic to join. We will ask a few questions; please answer by voice. Your information stays safe with us."
Field sequence with retry behaviour from the chunk:
- Name e.g. "Sunita Devi" — Retry 1, then skip to next question
- District, choose one: Kamrup Metropolitan, Gaya, Leh, Mayurbhanj, Dakshina Kannada — Retry 1, Retry 2
- Clinic name e.g. "City Clinic" — Retry 1, then skip to next question
- Are you pregnant? Yes branch — Retry 1, Retry 2
- Gestational age e.g. "5" (months) — Retry 1, Retry 2
- Child's name e.g. "Aarav" (via No branch) — Retry 1
- Child's DOB e.g. "15-04-2025" — Retry 1, Retry 2
- Mid-Call Script ("only 3 questions left"): plays "Now only 3 questions are left."
- Phone linked to clinic? / Number linked to clinic e.g. "9876543210" — Retry 1, Retry 2, skip to next question
- WhatsApp = calling number? Yes / No; WhatsApp number e.g. "9876543210" — Retry 1, Retry 2, skip to next question
- Last-Question Script: plays "This is the last question."
- Last 4 digits of Aadhaar card e.g. "4321" — Retry 1, Retry 2, skip to next question
- Ending Script: plays "Thank you for sharing. We will connect you to the service soon." then End the Call; Incomplete-end Script: plays "Sorry, we could not record your information now, so the call is ending. Thank you."
## LLM judges (general)
> "All LLM judges receive the conversation history, together with the agent output being graded, as the input, and produce a boolean score indicating whether the agent's output adheres to the judge criteria, following the LLM-as-a-judge paradigm (Zheng et al. 2023). The temperature is set to 0 for every LLM judge inference."
## EXTRACT judges
> "Each extracted field is scored either by exact match or by an LLM judge (Table 8), as is the acknowledgement the agent emits alongside the extraction. openai/gpt-5.4-mini is used as the judge model."
The following instructions are added as the system prompt for the LLM judge, in which `{{criteria}}` is replaced by the criteria for the field being scored:
> "You are a highly accurate evaluator checking whether the value an agent produced for a single tool-call argument satisfies a given criteria. You will be given the tool name, the argument name, and the actual value the agent produced for that argument. Mark match true only if the actual value satisfies the following criteria, and false otherwise: {{criteria}}"
> "An example is given below."
## Worked example: name turn
Assistant (Hindi intro excerpt):
> "Namaste! Yah ek automated call hai, ek nishulk maatru evam shishu swasthya seva ki taraf se. Aapne hamari seva se judne ke liye Anganwadi se sampark kiya hai. Yah ek muft seva hai, jismein aapko maa aur bachche ke swasthya se judi upyogi jaankari milegi. Hamari seva se judne ke liye hum aapse kuch sawal poochhenge. Kripya unke jawab bolkar dein."
User:
> "Mera poora naam Mrinmayee Kshirsagar hai (My full name is Mrinmayee Kshirsagar.)"
The chunk states:
> "Evaluation. The turn is scored on the extraction call the agent makes. One field, the caller's name, is open-ended and so is sent to an LLM judge with the criteria below; the acknowledgement is judged against a rubric, since it has no single correct answer. Both criteria follow."
Full Hindi intro sentence in the chunk:
> "Aapki di gayi saari jaankari hamare saath surakshit rahegi. Apna poora naam bataiye (Namaste! This is an automated call from a free maternal and child health service. You contacted the Anganwadi to join our service. This is a free service through which you will receive useful information about mother and child health. To enroll you in our service we will ask you a few questions. Please answer them by speaking. All the information you give will stay safe with us. Please tell me your full name.)"
## Acknowledgement criteria (verbatim)
> "Acknowledgement criteria. A brief acknowledgement of the user's previous answer, made of real words (not a non-lexical sound, grunt, or filler). This is encompassing and NOT restricted to any specific words: accept a receipt, back-channel, reassurance, praise, or transition phrase in any language, for example (but not strictly limited to) thik hai, achcha, ji haan, samajh gaya, koi baat nahi, "okay", "yes", "alright", "got it", "thank you", "no problem". Do not require any particular phrase, a 'hearing-only' tone, or extra brevity; phrases that imply the agent understood or accepted the answer (e.g. samajh gaya, "got it") are acceptable. Only a missing acknowledgement, or a non-lexical sound/filler, should fail this criterion."
## Name criteria (verbatim)
> "Name criteria. The captured value refers to the SAME name as "Mrinmayee Kshirsagar" when read aloud. Treat them as EQUAL when they differ only by: letter casing; leading/trailing or internal word spacing; or a reasonable alternative romanisation / transliteration of the same spoken Hindi name, for example 'ksh'"
**Covers:** Chunk 05-aapki-di-gayi-saari-jaankari-hamare: Figure 3 enrollment call flow with Start/Intro/Mid-Call/Last-Question/Ending/Incomplete-end scripts, Appendix B LLM judges overview, B.1 EXTRACT judges with system prompt, acknowledgement and name criteria with Mrinmayee Kshirsagar example
