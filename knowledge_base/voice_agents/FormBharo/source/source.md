# FormBharo: Designing and Evaluating a Voice Agent for Conversational Form Filling in Rural India
Source: https://arxiv.org/abs/2608.06027
Kind: pdf
Fetched: 2026-09-22T08:13:35.567550+00:00
Tool: pdftotext

                                           FormBharo: Designing and Evaluating a Voice Agent for Conversational Form
                                                                    Filling in Rural India
                                                                                 Aman Dalmia, Sanskriti Midha, Jigar Doshi
                                                                           Artpark, Indian Institute of Science, Bengaluru, Karnataka, India
                                                                                      {aman.dalmia, jigar, sanskriti}@artpark.in



                                                                     Abstract                                  and Khera 2017). Documentation already consumes much of
                                                                                                               their day (Khandre, Jakasania, and Raut 2023) and dozens of
                                          In India, almost every social benefit starts with a form, yet        overlapping reporting systems add to this burden, requiring
                                          the people who need these benefits most are often unable to          the same data to be re-entered across apps and paper regis-
                                          read or write. Reaching them requires a spoken conversation.
                                          Today that work falls to frontline health workers who enroll
                                                                                                               ters (Nongrum et al. 2025). This caps enrollment at worker
                                          beneficiaries one at a time, a poor use of their stretched capac-    capacity rather than need. Additionally, these records are the
                                                                                                               administrator’s source of truth for allocating resources, so




arXiv:2608.06027v1 [cs.CL] 6 Aug 2026
                                          ity. We built FormBharo (“fill the form” in Hindi), a voice
                                          agent that fills a structured form over a phone call under tight     errors and delays in enrollment slow the system’s response.
                                          latency and cost budgets by pairing Large Language Mod-                 Voice-based services have already demonstrated
                                          els (LLMs) with deterministic, rule-based validation and flow        population-scale reach in low- and middle-income countries
                                          control. It is being piloted with ARMMAN, an NGO run-                (LMICs). For example, the outbound prerecorded-call
                                          ning large-scale maternal and child mobile-health programs           service Kilkari reached more than 10 million subscribers
                                          in India, to enroll low-income, Hindi-speaking mothers in an-
                                                                                                               (LeFevre et al. 2022) and delivered ∼1.2 million calls
                                          tenatal and postnatal care. To our knowledge, it is the first con-
                                          versational voice agent piloted to fill an enrollment form for       per day (Bashingwa et al. 2021). Early interactive voice
                                          this population. We openly release FormVoiceAgentBench,              response (IVR) systems commonly relied on touch-tone
                                          a new benchmark pairing human-recorded Hindi audio with              input, which users preferred over low-quality speech recog-
                                          3,760 multi-turn conversation tests across 960 simulated calls,      nition (Patel et al. 2010). However, Sherwani et al. (2009)
                                          to evaluate our agent’s components (transcription, extraction,       found that a carefully designed speech interface achieved
                                          reply generation) and end-to-end form completion under real          significantly higher task-completion rates than an equivalent
                                          acoustic variations. Form completion drops by up to ∼41 per-         touch-tone interface among both low-literate and literate
                                          centage points when LLMs receive error-prone real-speech             users. LLM-powered voice agents are now making real-time
                                          transcripts instead of reference transcripts. The rule-based         spoken interaction increasingly practical (Mukherjee 2026),
                                          controls recover many turn-level extraction errors, helping
                                                                                                               creating new opportunities for service delivery. A mother
                                          smaller, cheaper models match or surpass frontier models on
                                          form completion. Component-level performance does not pre-           can call a number and enroll by speaking naturally with an
                                          dict end-to-end performance: GPT-5.5 leads turn-level extrac-        agent in her own words and language, with nothing to read,
                                          tion accuracy on reference transcripts (99.8%) but ranks lower       type, or install.
                                          on form completion. Since errors both propagate and cancel              Doing this reliably is hard. Voice agents work well with
                                          across the pipeline, the optimal choice of models emerges            a cooperative speaker in a quiet room, but performance
                                          only through end-to-end evaluation. Finally, no single model         degrades with background noise, telephone-channel distor-
                                          is the best across accuracy, cost, and latency at once, so we        tion, underrepresented regional accents, unusual speaking
                                          use a Pareto-based weighted-sum scalarization for selecting a        rates, mispronunciations, and disfluencies (Chen et al. 2026;
                                          deployable configuration that balances the three.
                                                                                                               Bhanushali et al. 2022). Hindi-English code-mixing intro-
                                                                                                               duces another challenge (Diwan et al. 2021), as do structured
                                                                                                               values such as phone numbers and dates, which can be spoken
                                                              1    Introduction                                in many ways but must resolve to a single value (Mohammadi
                                        Access to nearly every social benefit in India runs through a          et al. 2026). These problems compound in form-filling calls:
                                        form a citizen must complete to enroll (Indus Action 2026).            callers hesitate, they correct themselves mid-answer, and the
                                        Yet, the people with the greatest need for these programs are          form branches on earlier answers, so an incorrectly captured
                                        often disproportionately low-income and less literate, leav-           field can send the agent down the wrong path.
                                        ing them least equipped to access the benefits: more than half            We present FormBharo, a hybrid voice agent that fills a
                                        the women in the lowest wealth quintile cannot read at all (In-        structured form over a phone call under tight latency and
                                        ternational Institute for Population Sciences (IIPS) and ICF           cost constraints (Figure 1). A speech-to-text (STT) model
                                        (2021)). Enrollment therefore falls to frontline health workers        transcribes the caller’s speech. An LLM, EXTRACT, extracts
                                        who sign up beneficiaries one conversation at a time (Drèze            the relevant form values. A rule-based layer then validates
Figure 1: FormBharo’s architecture. EXTRACT extracts the form values from the transcribed text. The rule-based layer validates
the extracted values, updates the form state, skips inactive branches, and selects the next question to ask. REPLY phrases the
next question which is spoken back to the user through a TTS model. The “Anganwadi name” is the public clinic’s name.


them, updates the form state and picks the next question to           models, we discard those that fail to satisfy our deployment
ask. A second LLM, REPLY, phrases the question naturally,             constraints, keep the Pareto-optimal ones, and rank the rest by
which a text-to-speech (TTS) model speaks back to the caller.         weighted-sum scalarization (Marler and Arora 2010), with
If all the fields have been answered, the LLM decides to              the weights reflecting our deployment’s priorities.
end the call instead. FormBharo is being piloted in rural                Our contributions are summarized below:
Maharashtra, India, enrolling low-income, Hindi-speaking
                                                                       • We frame the call-based conversational form-filling task
mothers in an antenatal and postnatal care program. The pilot
                                                                         for low-literacy users in LMICs and characterize the chal-
runs in collaboration with ARMMAN (ARMMAN 2008),
                                                                         lenges that make it hard.
a nonprofit in India that operates large-scale mobile-health
programs for maternal and child health among underserved               • We present FormBharo, to our knowledge the first con-
communities.                                                             versational voice agent piloted to fill an enrollment form
   To evaluate our agent, we release FormVoiceAgentBench,                for this population.
a benchmark pairing human-recorded Hindi audio with 3,760              • We share our evaluation design methodology and openly
multi-turn conversation tests across 960 simulated calls, built          release FormVoiceAgentBench, a new benchmark in
on the enrollment form from our pilot without exposing any               Hindi that implements it.
real caller’s data1 . Unit tests are used to evaluate the quality      • We compare different model choices and share our find-
of transcription, data extraction, and reply generation indi-            ings from component-level and end-to-end evaluations
vidually. Integration tests chain them to measure end-to-end             across accuracy, latency, and cost.
form completion with real-speech input.
   Our experiments show that component-level performance
does not predict form completion: LLMs that lead turn-level
                                                                                     2    System Architecture
extraction accuracy with reference transcripts as inputs rank         FormBharo is a voice agent that fills a structured form over a
lower once the components are chained. The rule-based layer           phone call by asking one question at a time. The design prin-
recovers many extraction errors, helping smaller, cheaper             ciple is to use LLMs only where they add value: interpret-
models match or surpass frontier models on form completion.           ing user inputs, turning unstructured answers into structured
Since errors both propagate and cancel across the pipeline,           fields, phrasing the next question naturally to be spoken back
the best configuration emerges only through end-to-end eval-          to the user, and deciding when the form is complete. Ev-
uation. Finally, no single model is the best across accuracy,         erything else stays rule-based: validation, retries, branching,
cost, and latency at once. To pick the best combination of            and choosing the next question.
                                                                         Figure 1 shows the call flow. Once the Voice Activ-
   1                                                                  ity Detection (VAD) model detects that the caller has
     Code and data will be made available here: https://github.com/
dalmia/AAAI-FormBharo-final/tree/main/code                            stopped speaking, an STT model transcribes the audio. The
EXTRACT LLM reads the transcript together with the conver-                       Statistic                           Count
sation history and extracts every field answered in that turn,                   Simulated users                          5
so the agent does not re-ask questions already answered.                         Form fields                             12
                                                                                 Acoustic conditions per utterance        4
The form has fields of several types: free text, number, date,
                                                                                 Unique audio recordings                380
boolean, and categorical. For categorical fields, EXTRACT                        Calls (unique call scripts)            240
returns the index of the chosen option rather than the option                    Calls (with acoustic variations)       960
text. In parallel, EXTRACT generates a short acknowledge-                        Unit tests (total)                   3,760
ment that the TTS model speaks back to reduce perceived                            EXTRACT                            1,880
latency.                                                                           REPLY                              1,880
   The rule-based layer validates each extracted value against
field-specific built-in guards, such as a specified minimum                    Table 2: FormVoiceAgentBench statistics.
length, 10 digits for a phone number, or a date restricted
to the past. When a value is missing or fails validation, it
checks whether the maximum number of retries for that field                        3    FormVoiceAgentBench
is reached. If retries remain, the validation error is passed
to REPLY LLM along with the conversation history, which               FormVoiceAgentBench is a Hindi benchmark, grounded in
asks the question again. Once retries are exhausted for a             the maternal and child health enrollment form from our pi-
required field, the rule-based layer ends the call. For an op-        lot, that pairs 380 audio recordings with 3,760 multi-turn
tional field, it either ends the call or skips it, depending on the   conversation tests across 960 simulated calls (Table 2) with-
field-specific setting. EXTRACT also detects when the caller          out exposing any Personally Identifiable Information (PII)
declines or does not know the answer to an optional field             from real callers. It evaluates the agent at two levels. Unit
(the skip flag). That field is then skipped without triggering        tests score each component in isolation: predicted transcripts
a retry. When validation passes, the values are written to the        against reference transcripts, extracted form data against the
form state, the single source of truth for which fields have          expected values, reply quality and ability to end the call given
been answered. The form has several branches conditioned              that the extraction was perfectly accurate. Integration tests
on the values of earlier fields. For example, gestational age is      chain the components to measure end-to-end form comple-
asked only if the caller says she is pregnant. The rule-based         tion.
flow-control evaluates whether any of the form’s branches
have been activated or disabled, and decides the next ques-           3.1   Form Structure
tion to ask. This decision is injected into the conversation
history of REPLY LLM as a tool call. It phrases the question          The form has 12 fields (Table 1) which follow a fixed order
naturally for the TTS model to speak back to the caller, or           including conditional branching. If the caller is pregnant, the
ends the call if the form is complete.                                agent asks her gestational age. Otherwise, it asks her recently
                                                                      born child’s name and date of birth. If her calling number is
   Finally, if the user starts speaking while the agent’s infer-
                                                                      not linked to the clinic, the agent asks for the linked number;
ence is running, the current turn is terminated immediately
                                                                      otherwise it skips ahead. Similarly, the agent asks for her
and the agent goes back to waiting for the user to stop speak-
                                                                      WhatsApp number if it differs from her calling number. The
ing, so interruptions are handled gracefully.
                                                                      other fields are always asked.

     Field                         Example answer On fail
     Name                          Sunita Devi     skip
                                                                      3.2   Simulated Users and Transcripts
     District                      Mayurbhanj      end                We define five simulated user profiles, each with fixed per-
     Clinic name                   City Clinic     skip
                                                                      sonal details, corresponding to the fields we intend to capture.
     Pregnant?                     yes / no        end
       yes: Gestational age        5 months        end                   Each form field has three representations: the value, the
       no: Child’s name            Aarav           end                desired form entry and the ground truth for measuring form
            Child’s DOB            15-04-2025      end                completion (“Sunita Devi”); the reference transcript, a natu-
     Phone linked to clinic?       yes / no        skip               rally spoken rendering of the value, phrased as a caller would
       no: Number linked           9876543210      skip               say it in a real conversation (“My name is Sunita Devi”);
     Phone linked to WhatsApp?     yes / no        skip               and the recording of that transcript. The value and the tran-
       no: WhatsApp number         9876543210      skip               script are generated sequentially by an LLM, under field-
     Aadhaar last 4 digits         4321            skip               specific constraints defined with ARMMAN: names and dis-
                                                                      trict names with phonetically hard spellings, and numbers
Table 1: The enrollment form for testing FormBharo. When
                                                                      with many spoken variations that make them hard to tran-
a caller fails to give a valid answer after a few retries, the
                                                                      scribe. District names were deliberately selected from outside
agent either skips to the next field (skip) or ends the call
                                                                      the pilot state for adequate stress-testing.
(end). Indented fields are conditional: whether they are asked
depends on the parent field’s response. Aadhaar is India’s               For optional fields, we generate two linguistic variants of
national ID.                                                          the transcript: one where the caller responds with the value
                                                                      and the other where she says she does not know it. We use
                                                                      OpenAI’s GPT-5.5 (OpenAI 2026) for the generation.
3.3   Audio Data Collection                                      as the ground truth. So, one call produces many tests. Dedu-
Each transcript was recorded to mimic the conditions in a        plicating tests with identical inputs across all 960 calls yields
public clinic across three acoustic variations: background       1,880 unit tests.
noise (ambient chatter and nearby speakers), microphone             The extracted values for closed-ended fields like numbers,
distance (close or far, chosen at random), and speaking pace     dates, and booleans are scored by computing the exact match
(fast or slow, chosen at random). Combined with the ideal        with the expected values. The skip flag is scored the same
acoustic condition, this gives four recordings per transcript.   way. Outputs for open-ended fields like names are harder
   Five native Hindi speakers were selected to match the         to rate since the expected value can have many phonetic
target demographic: all female, aged 18–35, drawn from two       forms (“Lakshmi” versus “Laxmi”), so we use a calibrated
states (Uttar Pradesh and Maharashtra) to cover differences      binary LLM judge (details are in the Appendix) to evaluate
in accent and colloquialisms. Annotators were trained with       them. Since EXTRACT also generates a short open-ended ac-
sample recordings and recorded each answer under specific        knowledgement, we use the LLM judge to evaluate its quality
directives. For example, “record in a noisy environment, or      against a rubric. An example is provided in the Appendix.
keep the mic at least 25 cm away, or speak slowly”. A separate   An accurate extraction passes both the exact-match checks
set of human supervisors listened to every clip to ensure the    and the LLM judgments. We report the mean extraction ac-
recordings met the requirements.                                 curacy.
                                                                 REPLY LLM We similarly prepare unit tests from the calls
3.4   From Transcripts to Calls                                  to measure response accuracy, with two key differences.
We assemble each call by stitching together a simulated          Along with the latest user response and the preceding con-
user’s transcripts with one recording per field. Since the       versation history, REPLY additionally receives a tool call
form branches, a simulated user can follow several paths,        carrying the decision of the rule-based layer as an input too
and each path becomes its own call. For example, the same        (Section 2). For the unit tests, we construct this tool call by
simulated user produces one call in which she is pregnant        passing the expected extraction values through the rule-based
and another in which she is not. Calls never mix values from     validation and flow-control step, so that measuring response
different simulated users. Each call uses a single acoustic      accuracy can be isolated from extraction errors.
condition throughout (e.g. noisy environment or speaking            Secondly, REPLY either phrases the next question or ends
slowly), since a caller’s environment does not change mid-       the call when the form is complete. The end-call decision
call.                                                            is a tool call, evaluated by exact match. Since the generated
   Each simulated user follows 2 × 3 × 4 × 2 = 48 distinct       reply can be phrased in many equally correct ways, we again
paths through the form, one call per path: two pregnancy         rely on calibrated binary LLM judges to rate them. However,
branches (pregnant or not), three branches for whether the       unlike what we did for EXTRACT, each reply is graded across
calling number is linked to the clinic (linked, not linked       five independent dimensions: 1) asking the right question, 2)
and correct value provided, or not linked but not able to        adherence to Hindi, 3) single line response, 4) no acknowl-
remember the linked number), four choices for whether the        edgment (since EXTRACT handles that), and 5) not echoing
WhatsApp number is the same as the calling number (same,         the caller’s answer back. The LLM judge calibration details
not same and answered, not same but unable to recall the         and an example are in the Appendix. An accurate response
WhatsApp number, cannot recall if they are the same), and        either passes all the LLM judgments or ends the call at the
two branches for the Aadhaar digits (answered or not known).     right time. We report the mean response accuracy.
Across the five simulated users this gives 5 × 48 = 240 calls,      As with EXTRACT, deduplicating the tests across the 960
and recording each under the four acoustic conditions yields     simulated calls, each call producing many tests, yields 1,880
240 × 4 = 960.                                                   unit tests: 920 require a reply, while the remaining 960 check
                                                                 whether REPLY ends the call correctly.
                4    Evaluation Design
4.1   Unit Tests                                                 4.2   Integration Tests
Speech-to-Text Word Error Rate (WER) is commonly                 Integration tests chain the components, so the output of one
used for comparing STT models. However, it is a poor met-        feeds into the next, and the agent is judged on completing the
ric for transcription quality on Indic languages (Sarvam AI      form, not on any single turn.
2026) and for agents (Pipecat AI 2026b): it counts every            First, we replace the reference transcripts in the unit-test
surface difference as an error, even when the meaning is         inputs with transcripts produced by the STT models, so tran-
unchanged. We therefore also report LLM-WER (Sarvam AI           scription errors propagate to the LLMs. Next, we evaluate
2026), which discards mismatches that an LLM classifies as       each call as a whole. We start from an empty form and go
semantically equivalent or phonetically similar and recom-       through the call’s turns in order. At each turn, we write the
putes WER over the genuine errors.                               values extracted for that turn’s unit test into the form, as the
                                                                 agent would in a live call. The form after the last turn is the
EXTRACT LLM To evaluate data extraction, we prepare              predicted final form. Comparing this against the expected val-
unit tests from every call. For each turn, we create a unit      ues gives the form-completion accuracy: the fraction of form
test using the latest user response paired with the preceding    fields captured correctly at the end of the call. We compute
conversation history as input and the expected form values       it using both reference transcripts and the transcripts pro-
 Model                 WER ↓      LLM-WER ↓       Cost (USD) ↓        Model             Reference Saaras v3 Scribe v2 Nova-3
 Scribe v2              0.835          0.062              0.172       Gemini 3 Flash     100.00    85.24     89.48    83.92
 Chirp 3                0.981         0.055               0.424       Gemini 3.5 Flash   100.00    90.74     92.50    87.09
 Saaras v3              1.007          0.074              0.137       GPT-5.5             99.95    89.97     89.37    84.73
 GPT-4o-transcribe      1.012          0.127              0.159       Claude Sonnet 4.6   99.66    91.55     93.01    84.54
 Nova-3                0.826           0.104             0.127        GLM-5.1             99.56    90.92     58.66    86.09
                                                                      Claude Opus 4.8     99.41    92.22     92.03    85.83
Table 3: Comparison of STT models. Since models have                  Gemini 2.5 Flash    99.06    91.76     92.39    85.50
different billing units, the total cost of transcribing the entire    Gemini Pro          98.90    92.55     93.47    86.53
benchmark is reported.                                                GPT-5.4-mini        98.35    90.68     90.10    84.40
                                                                      GPT-4.1             95.99    88.82     91.50    86.33
                                                                      Mistral Medium 3.5 92.83     90.39     91.84    83.37
 Model             Reference Saaras v3 Scribe v2 Nova-3
 GPT-5.5            99.79     95.53     98.62    95.16               Table 5: Form-completion accuracy using reference tran-
 Gemini 3.5 Flash   99.36     95.69     98.94 96.38
                                                                     scripts and the outputs of the three STT models as inputs.
 Claude Opus 4.8    99.15     96.22     98.40    96.01
 Claude Sonnet 4.6  99.15     96.01     98.94    95.96
 GLM-5.1            98.72     94.52     63.40    95.43                                 Extraction accuracy   Form completion
 Gemini Pro         97.23     94.26     97.29    94.63
 Gemini 2.5 Flash   96.17     95.27     98.03    95.43                     Model       Median (%) ∆ (pp) Median (%) ∆ (pp)
 Gemini 3 Flash     95.96     84.79     88.83    86.28                     Saaras v3     94.52     −3.14     90.74     −7.67
 GPT-5.4-mini       92.34     90.05     96.76    91.54                     Scribe v2     97.29     −0.42     91.84     −7.38
 Mistral Medium 3.5 89.36     87.82     92.34    87.77                     Nova-3        95.16     −3.14     85.50     −13.56
 GPT-4.1            85.11     75.53     78.94    79.84
                                                                     Table 6: Median extraction and form-completion accuracy
Table 4: Per-turn extraction accuracy using reference tran-          with real-speech transcripts as inputs. ∆ denotes the median
scripts and the transcripts from the three STT models as             change relative to reference transcripts. Both degrade under
inputs.                                                              transcription noise.


duced by each STT model as inputs. The gap between them              5.3    Data Extraction
quantifies the impact of transcription errors on form com-
                                                                     Table 4 compares various LLMs on per-turn extraction accu-
pletion. Finally, we chain EXTRACT and REPLY. To build
                                                                     racy, computed using reference transcripts and the transcripts
the tool call for REPLY, we pass EXTRACT’s actual output
                                                                     of the three STT models as inputs.
through the rule-based validation and flow control, instead
                                                                        Frontier models saturate extraction accuracy on reference
of the expected extraction values used in the unit tests.
                                                                     transcripts as inputs with the top models scoring almost
   Each EXTRACT model drives its own set of REPLY runs.
                                                                     perfectly: GPT-5.5 leads at 99.79%, with Gemini 3.5 Flash
Because each stage feeds the next, extraction accuracy is
                                                                     (99.36%) and the two Claude models (99.15%) just behind.
measured for every STT × EXTRACT pair, and response ac-
                                                                     Robustness to STT errors varies across LLMs: the median
curacy for every STT × EXTRACT × REPLY combination.
                                                                     drop is modest, from 0.42 percentage points to 3.14 (Table 6).
                                                                     The four most accurate models lose at most 4.63 points re-
             5    Experiments & Analysis                             gardless of the STT model. But weaker models degrade much
5.1   Setup                                                          more: GLM-5.1 collapses by 35 points with Scribe v2 tran-
                                                                     scripts. The next-worst drop is still 11.2 points. The extrac-
We benchmark five STT models and 11 LLMs across accu-                tion accuracy leaderboard changes when real transcripts are
racy, latency (p95), and cost. The temperature is set to 0 for       used: GPT-5.5 is no longer the winner. The best extraction
non-reasoning models. The reasoning models use “medium”              accuracy under real-speech is 98.94% (Gemini 3.5 Flash and
reasoning effort for EXTRACT and “low” for REPLY. Full               Claude Sonnet 4.6) with transcripts from Scribe v2. Claude
implementation details and 95% confidence intervals can be           Opus 4.8 leads under Saaras v3 (96.22%) and Gemini 3.5
found in the appendix.                                               Flash leads under Nova-3 transcripts (96.38%).
5.2   Speech-to-Text                                                 5.4    Form Completion
Table 3 shows that the two metrics disagree: Nova-3 has              Similar to extraction accuracy, Table 5 reports form-
the best WER yet the second-worst LLM-WER. We therefore              completion accuracy across all the LLMs being tested. The
rank models by LLM-WER, which was built to address the               rule-based layer recovers extraction errors.
shortcomings of WER. Chirp 3 has the best LLM-WER but                    On reference transcripts, Gemini 3 Flash achieves 95.96%
costs at least twice as much as any other model, while Scribe        per-turn extraction accuracy but 100% form-completion ac-
v2 performs close to Chirp 3 at a fraction of the cost. GPT-4o-      curacy. Per-turn extraction evaluates the output of EXTRACT
transcribe is the least accurate. Eliminating these two leaves       LLM, whereas form completion evaluates the values ulti-
Scribe v2, Saaras v3, and Nova-3, which we carry into the            mately stored in the form after the rule-based layer processes
integration tests.                                                   it. All the extraction errors for this model arise from a type
mismatch: a numeric field being returned as a string. The           Next, we rank the models using weighted-sum scalariza-
rule-based layer normalizes it before storing the value, pre-    tion (Marler and Arora 2010):
serving 100% form-completion accuracy. This highlights a
benefit of our hybrid design which enables smaller models              Ui = wa ãi + wℓ ℓ̃i + wc c̃i ,   i⋆ = arg max Ui ,
                                                                                                                     i
to perform better end-to-end even if their per-turn inference
is not perfect.                                                  where wa + wℓ + wc = 1. These weights can be tuned to
   The best model end-to-end differs from the best model per-    reflect the deployment priorities.
turn. Under reference transcripts, GPT-5.5 leads extraction         As a baseline, under equal weights, Mistral Medium 3.5
accuracy (99.79%), whereas Gemini 3 Flash and Gemini 3.5         ranks highest (U = 0.81), followed by GPT-4.1 (U = 0.78).
Flash tie for the highest form-completion accuracy at 100%.      Mistral combines the lowest latency with 91.84% form-
   Form completion degrades more than per-turn extrac-           completion accuracy and a cost of $0.0080 per turn. Claude
tion with error-prone real-speech transcripts: median form-      Sonnet 4.6, the most accurate candidate, scores lower (U =
completion accuracy drops by 7.67 percentage points with         0.51) because it is slower and more expensive. The hard la-
Saaras v3, 7.38 points with Scribe v2, and 13.56 points with     tency constraint already excludes models that are too slow
Nova-3 (Table 6), compared with median per-turn extraction       for deployment, so we assign the remaining latency differ-
drops of only 0.42–3.14 points. The largest model-specific       ences a lower weight, wℓ = 0.1. Because accuracy remains
decline is ∼41 points for GLM-5.1 with Scribe v2. Although       the primary objective, we sweep wa from 0.5 to 0.9, with
the rule-based layer recovers some extraction errors, uncor-     wc = 1 − wa − wℓ . Only two models lead across this range:
rected errors can accumulate across turns to produce a larger    Gemini 3.5 Flash for 0.50 ≤ wa ≤ 0.61, and Claude Sonnet
degradation end-to-end.                                          4.6 for 0.62 ≤ wa ≤ 0.90 (full table in the Appendix). We
                                                                 select Gemini 3.5 Flash for EXTRACT: it trails Claude Son-
5.5   Model Selection                                            net 4.6 by only 0.51 percentage points on form-completion
We select the STT, EXTRACT, and REPLY models in the              accuracy while responding faster and costing less than half
pipeline (Figure 1) sequentially because each downstream         as much per turn.
component consumes the outputs of the components before
it. We first select the STT model, then identify the best LLM
for EXTRACT using that STT model’s transcripts, and fi-
nally evaluate REPLY with the selected STT and EXTRACT
models fixed. The deployment objective is to balance task
performance, p95 latency, and cost, subject to component-
specific deployment constraints.
    STT selection. Scribe v2 provides the strongest down-
stream performance. It achieves the highest median ex-
traction accuracy (97.29%) and form-completion accuracy
(91.84%), while producing the smallest median drops rela-
tive to the model performance on reference transcripts (Ta-
ble 6). We therefore select Scribe v2 as the STT model.
    EXTRACT selection. With Scribe v2 fixed as the
STT model, we compare EXTRACT models using form-
completion accuracy on its transcripts, together with la-
tency and cost. We discard models that fail our deployment       Figure 2: Cost–quality–latency trade-off among EXTRACT
constraints: p95 latency below 5 s and form-completion ac-       models satisfying the deployment constraints. The logarith-
curacy above 90%. This excludes Gemini Pro, despite its          mic x-axis shows cost per turn, the y-axis shows form-
leading form-completion accuracy, and Gemini 2.5 Flash,          completion accuracy using Scribe v2 transcripts, and marker
leaving behind six candidates. Among those, Claude Sonnet        area encodes p95 latency per turn (bigger is slower). All six
4.6 achieves the highest form-completion accuracy, Mistral       models are Pareto-optimal across the three objectives. The
Medium 3.5 has the lowest p95 latency (1.75 s), and GPT-         model selected for deployment is highlighted.
5.4-mini is the cheapest ($0.0011). No model leads all three
axes, and all six candidates lie on the Pareto frontier (Fig-
ure 2), so selecting a deployable model requires balancing
these competing objectives. First, we min–max normalize          5.6    Response Generation
the three axes within the frontier. Since lower latency and      REPLY has the narrowest role in the pipeline (Section 2): it
cost are better, we reverse their scales so that higher values   either phrases the selected question naturally or ends the call.
are always preferred:                                            So, a smaller, faster model may suffice. With Scribe v2 and
                                                                 Gemini 3.5 Flash for transcription and extraction, we com-
                 ai − amin                ℓmax − ℓi              pare five LLMs for REPLY. The selected EXTRACT model’s
        ãi =                ,    ℓ̃i =             ,
                amax − amin             ℓmax − ℓmin              actual outputs on Scribe v2 transcripts are passed through the
                             cmax − ci                           rule-based layer to construct the decision passed to REPLY.
                      c̃i =             .                        Table 7 reports the resulting response accuracy. The Refer-
                            cmax − cmin
         Model                Reference     Scribe v2             lingual, code-switched, spontaneous, telephonic, geograph-
         Claude Sonnet 4.6     100.00         97.77
                                                                  ically diverse, and low-resource speech (Diwan et al. 2021;
         GPT-4.1               100.00         96.60               Bhanushali et al. 2022; Bhogale et al. 2026; Javed et al. 2023,
         GPT-5.4-mini           98.09         96.70               2024; Pulikodan et al. 2026; Joshi et al. 2025). However,
         Gemini 3 Flash         97.23         96.17               these resources evaluate transcriptions or other component-
         Gemini 3.5 Flash       97.02         94.73               level speech tasks such as speaker identification. In our paper,
                                                                  in addition to transcriptions, we score per-field correctness
Table 7: REPLY response accuracy with Gemini 3.5 Flash as         on a real Indian enrollment form.
the EXTRACT LLM.                                                     Voice agents and form-filling. Recent benchmarks such
                                                                  as VoiceBench (Chen et al. 2026) and VoiceAgentBench
                                                                  (Jain et al. 2025) evaluate voice systems on outcomes beyond
ence column is computed using the expected extraction val-        transcription such as spoken question answering, instruction
ues with reference transcripts to prepare the inputs, whereas     following and tool selection, using predominantly synthetic
for Scribe v2, the outputs of EXTRACT on Scribe v2 tran-          speech. Closest to us, EVA-Bench evaluates task accuracy
scripts are used to prepare the tests (Section 4).                and interaction quality over simulated multi-turn enterprise
   Errors propagate through the pipeline. Response accuracy       calls (Bogavelli et al. 2026). None of them, however, target a
decreases for all five models when errors from transcription      constrained, structured task like form completion.
and extraction flow through to REPLY. The decline ranges             Related application systems assess latency and conversa-
from 1.06 to 3.40 percentage points, with a median of 2.23        tional quality, form usability, clinician-reviewed speech to
points, capturing the combined effect of transcription and ex-    EMR generation, or sampled production records (Cuadra
traction errors. No single model is the best across accuracy,     et al. 2024; Mustafa et al. 2026; Mukherjee et al. 2026). In
latency, and cost. Claude Sonnet 4.6 is the most accurate         contrast, FormVoiceAgentBench scores many models on form
on Scribe v2 transcripts (97.77%), Gemini 3 Flash has the         completion using noisy audio in a low-resource language.
lowest p95 latency (2.66 s), and GPT-5.4-mini is the cheap-
est ($0.0008 per turn). Our deployment constraints of p95                              7    Conclusion
latency below 4 s and response accuracy above 95% exclude
Claude Sonnet 4.6 on latency and Gemini 3.5 Flash on accu-        We presented FormBharo, a phone-call-based conversational
racy, leaving three candidates. Pareto filtering leaves GPT-      form-filling voice agent being piloted in a live maternal
5.4-mini and Gemini 3 Flash. Using the same weighted-sum          and child health enrollment program in rural Maharashtra,
scalarization method defined earlier with wℓ = 0.1, GPT-          India, and described FormVoiceAgentBench, a benchmark
5.4-mini ranks highest throughout 0.5 ≤ wa ≤ 0.9 (details         for evaluating it, along with our findings. Our results show
are in the Appendix). Therefore, we select GPT-5.4-mini for       that component-level accuracy does not predict end-to-end
REPLY.                                                            form completion, with errors both propagating and cancel-
                                                                  ing across the pipeline. The rule-based layer recovers many
                                                                  model errors, helping smaller, cheaper models meet deploy-
                   6    Related Work                              ment constraints. This is critical in LMICs, where cost and
Deployed AI for public services. A growing body of AI-            latency constrain deployment at scale.
for-social-impact research studies how AI reshapes access to         The current benchmark is limited in several ways. It cap-
services for under-served users. Jo et al. (2025) show LLM as-    tures scripted, well-formed answers, but real callers also give
sistants can lower administrative burdens while adding new        wrong, partial, or self-corrected values. Each call applies
compliance and trust costs, and studies of digital welfare        only a single acoustic variation at a time, so combinations
systems document similar transfers of burden to claimants         within the same call, such as a distant microphone in a noisy
(Watson, Parnaby, and Kharrufa 2024). Closest to our de-          room, remain untested. The benchmark is based on five sim-
sign, Kothari et al. (2026) decompose a clinical LLM-             ulated users, with audio recorded one turn at a time by five
summarization task into semi-structured attributes that can       annotators from two states rather than through full live calls,
be validated separately rather than trusting one end-to-end       limiting its conversational, linguistic, and demographic di-
prompt. This matters for equity: Poole-Dayan, Roy, and Kab-       versity. The dataset is also limited to Hindi, though our in-
bara (2026) found that the LLM’s response quality drops           tended users are multilingual. Finally, we did not evaluate
for users with lower English proficiency and literacy. Our        TTS output quality.
callers fit that profile, so any non-English system needs to be
evaluated rigorously.
                                                                                     Ethical Statement
    Spoken understanding and Indic speech. Spoken slot
filling and dialogue state tracking often use an STT-to-LLM       No real user data was used to build the dataset. The spo-
cascade that transcribes and extracts values, where recogni-      ken scripts were recorded by paid annotators who are native
tion errors propagate into slot and state errors (Yoon et al.     Hindi speakers. The broader intended impact of FormBharo
2023; Jacqmin et al. 2023; Ganesan et al. 2021; Sun et al.        is to widen access to care for an under-served population,
2024); Si et al. (2023) show that a low WER does not guar-        but this also increases the risks. Since incorrect data cap-
antee task accuracy. Indic and code-mixed resources supply        ture could instead delay or deny access, deployment at scale
realistic acoustic and linguistic variation, including multi-     requires more rigorous testing with adequate guardrails and
fallback mechanisms in place to confirm or correct captured       Diwan, A.; Vaideeswaran, R.; Shah, S.; Singh, A.; Srini-
information when required.                                        vasa Raghavan, K. M.; Khare, S.; Unni, V.; Vyas, S.; Ra-
                                                                  jpuria, A.; Yarra, C.; Mittal, A. R.; Ghosh, P. K.; Jyothi, P.;
                   Acknowledgments                                Bali, K.; Seshadri, V.; Sitaram, S.; Bharadwaj, S.; Nanavati,
                                                                  J.; Nanavati, R.; and Sankaranarayanan, K. 2021. MUCS
We thank Amrita Mahale, Parina Anand and Hetvi Lodaya             2021: Multilingual and Code-Switching ASR Challenges for
at ARMMAN for designing the enrollment form, testing the          Low Resource Indian Languages. In Proceedings of Inter-
agent through successive iterations, and sharing the insights     speech 2021, 2446–2450. ISCA.
from the field that guided its design. We thank the Vaani         Drèze, J.; and Khera, R. 2017. Recent Social Security Ini-
team at ARTPARK for their help with data collection and           tiatives in India. World Development, 98: 555–572.
annotation. Finally, we are grateful to the frontline health
workers and mothers who tested FormBharo and shared their         Exotel. 2026. Exotel: Cloud Telephony and Contact Center
feedback.                                                         Platform. https://exotel.com. Accessed: 2026-08-01.
                                                                  Ganesan, K.; Bamdev, P.; B, J.; Venugopal, A.; and Tushar,
                                                                  A. 2021. N-Best ASR Transformer: Enhancing SLU Per-
                        References                                formance using Multiple ASR Hypotheses. In Proceedings
ARMMAN. 2008. ARMMAN — Advancing Reduction in                     of the 59th Annual Meeting of the Association for Compu-
Mortality and Morbidity of Mothers, Children and Neonates.        tational Linguistics and the 11th International Joint Con-
https://armman.org.                                               ference on Natural Language Processing (Volume 2: Short
Bashingwa, J. J. H.; Mohan, D.; Chamberlain, S.; Arora, S.;       Papers), 93–98. Association for Computational Linguistics.
Mendiratta, J.; Rahul, S.; Chauhan, V.; Scott, K.; Shah, N.;      Google Cloud. 2026. Chirp 3: HD Voices — Text-
Ummer, O.; Ved, R.; Mulder, N.; and LeFevre, A. E. 2021.          to-Speech. https://cloud.google.com/text-to-speech/docs/
Assessing exposure to Kilkari: a big data analysis of a large     chirp3-hd. Accessed: 2026-08-01.
maternal mobile messaging service across 13 states in India.      Indus Action. 2026. Administrative Burden in India’s Wel-
BMJ Global Health, 6(Suppl 4): e005213.                           fare System: Examining the Learning, Compliance and Psy-
Bhanushali, A.; Bridgman, G.; G, D.; Ghosh, P. K.; Kumar,         chological Costs Faced by Vulnerable Citizens in Accessing
P.; Kumar, S.; Kolladath, A. R.; Ravi, N.; Seth, A.; Seth,        Social Protection Programs. https://indusaction.org/case-
A.; Singh, A.; Sukhadia, V. N.; Umesh, S.; Udupa, S.; and         study/. Accessed: 2026-07-23.
Durga Prasad, L. V. S. V. 2022. Gram Vaani ASR Challenge          International Institute for Population Sciences (IIPS); and
on Spontaneous Telephone Speech Recordings in Regional            ICF. 2021. National Family Health Survey (NFHS-5), 2019–
Variations of Hindi. In Proceedings of Interspeech 2022,          21: India Report. Technical Report FR375, International
3548–3552. ISCA.                                                  Institute for Population Sciences, Mumbai.
Bhogale, K.; Dhir, M.; Walecha, A.; Kaur, M.; Chhabra, V.;        Jacqmin, L.; Druart, L.; Estève, Y.; Favre, B.; M Rojas,
Pareek, A.; Sidh, H.; Manik, M.; Jain, S.; Singh, B.; Singh,      L.; and Vielzeuf, V. 2023. OLISIA: a Cascade System
U.; Javed, T.; Banga, S.; and Khapra, M. M. 2026. Voice           for Spoken Dialogue State Tracking. In Proceedings of
of India: A Large-Scale Benchmark for Real-World Speech           the Eleventh Dialog System Technology Challenge, 95–104.
Recognition in India. arXiv:2604.19151.                           Prague, Czech Republic: Association for Computational Lin-
                                                                  guistics.
Bogavelli, T.; Gauthier Melançon, G.; Stankiewicz, K.;
                                                                  Jain, D.; Shukla, H.; Rajeev, G.; Kulkarni, A.; Khatri, C.; and
Bamgbose, O.; Riols, F.; Nguyen, H. H.; Mehndiratta, R.;
                                                                  Agarwal, S. 2025. VoiceAgentBench: Are Voice Assistants
Brin, L. D.; Marinier, J.; Subramani, H.; Madamala, A.;
                                                                  Ready for Agentic Tasks? arXiv:2510.07978.
Nemala, S. K.; and Sunkara, S. 2026. EVA-Bench: A
New End-to-end Framework for Evaluating Voice Agents.             Javed, T.; Bhogale, K.; Raman, A.; Kumar, P.; Kunchukuttan,
arXiv:2605.13841.                                                 A.; and Khapra, M. M. 2023. IndicSUPERB: A Speech Pro-
                                                                  cessing Universal Performance Benchmark for Indian Lan-
Chen, Y.; Yue, X.; Zhang, C.; Gao, X.; Tan, R. T.; and Li, H.     guages. Proceedings of the AAAI Conference on Artificial
2026. VoiceBench: Benchmarking LLM-Based Voice As-                Intelligence, 37(11): 12942–12950.
sistants. Transactions of the Association for Computational
Linguistics, 14: 378–398.                                         Javed, T.; Nawale, J.; George, E.; Joshi, S.; Bhogale, K.;
                                                                  Mehendale, D.; Sethi, I.; Ananthanarayanan, A.; Faquih, H.;
Cuadra, A.; Breuch, J.; Estrada, S.; Ihim, D.; Hung, I.; Askar-   Palit, P.; Ravishankar, S.; Sukumaran, S.; Panchagnula, T.;
yar, D.; Hassanien, M.; Fessele, K. L.; and Landay, J. A.         Murali, S.; Gandhi, K.; R, A.; M, M.; Vaijayanthi, C.; Karun-
2024. Digital Forms for All: A Holistic Multimodal Large          ganni, K.; Kumar, P.; and Khapra, M. 2024. IndicVoices: To-
Language Model Agent for Health Data Entry. Proceedings           wards Building an Inclusive Multilingual Speech Dataset for
of the ACM on Interactive, Mobile, Wearable and Ubiquitous        Indian Languages. In Findings of the Association for Com-
Technologies, 8(2): 1–39.                                         putational Linguistics: ACL 2024, 10740–10782. Bangkok,
Dalmia, A.; and Doshi, J. 2025. Calibrate: An Open-Source         Thailand: Association for Computational Linguistics.
Evaluation Platform for AI Agents. https://calibrate.artpark.     Jo, J.; Zhang, H.; Cai, J.; and Goyal, N. 2025. AI Trust
ai/. ARTPARK, Indian Institute of Science. Code: https:           Reshaping Administrative Burdens: Understanding Trust-
//github.com/artpark-sahai-org/calibrate.                         Burden Dynamics in LLM-Assisted Benefits Systems. In
Proceedings of the 2025 ACM Conference on Fairness, Ac-           Nongrum, M.; Dhaliwal, B.; Na, Y.; Jamir, T.; Shekhawat,
countability, and Transparency (FAccT), 1172–1183. New            S.; Rao, K. D.; Ramani, S.; Albert, S.; and Closser, S. 2025.
York, NY, USA: ACM.                                               Disconnected data: mHealth data systems and challenges for
Joshi, S.; George, E. I.; Javed, T.; Bhogale, K.; Narasimhan,     primary health care workers in India. SSM - Health Systems,
N.; and Khapra, M. M. 2025. Recognizing Every Voice:              5: 100124.
Towards Inclusive ASR for Rural Bhojpuri Women. In Pro-           OpenAI. 2026. GPT-5.5 System Card. https://openai.com/
ceedings of Interspeech 2025, 4243–4247. ISCA.                    index/gpt-5-5-system-card/. Accessed: 2026-07-23.
Khandre, R. R.; Jakasania, A.; and Raut, A. 2023. “We             OpenRouter. 2026. OpenRouter: A Unified API for Large
are working for seven days a week”: Time motion study of          Language Models. https://openrouter.ai. Accessed: 2026-
accredited social health activists from central India. Medical    07-31.
Journal Armed Forces India, 79(Suppl 1): S142–S149.
                                                                  Patel, N.; Chittamuru, D.; Jain, A.; Dave, P.; and Parikh, T. S.
Kothari, A.; Vossler, P.; Digitale, J.; Forouzannia, M.; Rosen-   2010. Avaaj Otalo: A Field Study of an Interactive Voice
berg, E.; Lee, M.; Bryant, J.; Molina, M.; Marks, J.; Zier, L.;   Forum for Small Farmers in Rural India. In Proceedings
and Feng, J. 2026. When the Domain Expert Has No Time             of the SIGCHI Conference on Human Factors in Computing
and the LLM Developer Has No Clinical Expertise: Real-            Systems, CHI ’10, 733–742. ACM.
World Lessons from LLM Co-Design in a Safety-Net Hos-
pital. In Proceedings of the AAAI Conference on Artificial        Pipecat AI. 2026a. Pipecat: Open Source Framework for
Intelligence, volume 40, 38754–38762.                             Voice and Multimodal Conversational AI. https://github.
                                                                  com/pipecat-ai/pipecat. Accessed: 2026-07-31.
Kunchukuttan, A. 2020. The IndicNLP Library. https:
//github.com/anoopkunchukuttan/indic_nlp_library.           Ac-   Pipecat AI. 2026b. stt-benchmark: Benchmarking Speech-
cessed: 2026-08-01.                                               to-Text with Semantic WER and TTFS Latency. https://
LeFevre, A. E.; Shah, N.; Scott, K.; Chamberlain, S.; Ummer,      github.com/pipecat-ai/stt-benchmark. Accessed: 2026-07-
O.; Bashingwa, J. J. H.; Chakraborty, A.; Godfrey, A.; Dutt,      23.
P.; Ved, R.; and Mohan, D. 2022. The impact of a direct to        Poole-Dayan, E.; Roy, D.; and Kabbara, J. 2026. LLM Tar-
beneficiary mobile communication program on reproductive          geted Underperformance Disproportionately Impacts Vul-
and child health outcomes: a randomised controlled trial in       nerable Users. In Proceedings of the AAAI Conference on
India. BMJ Global Health, 6(Suppl 5): e008838.                    Artificial Intelligence, volume 40, 39116–39124.
Marler, R. T.; and Arora, J. S. 2010. The weighted sum            Pulikodan, S.; Singh, A.; Basu, A.; Desai, N.; J, P. K.;
method for multi-objective optimization: new insights. Struc-     Bhat, P. D.; Dharmaraju, R.; Gupta, R.; Udupa, S.; Kumar,
tural and Multidisciplinary Optimization, 41(6): 853–862.         S.; Sharma, S.; Sanka, V.; Tewari, D.; Dhand, H.; Kamat,
Mohammadi, S.; Paldhe, M.; Chhabra, A.; Son, Y.; and Se-          A.; Singh, S.; Vashishth, S.; Talukdar, P.; Acharya, R.; and
shagiri, V. 2026. LingVarBench: Benchmarking LLMs on              Ghosh, P. K. 2026. VAANI: Capturing the Language Land-
Entity Recognitions and Linguistic Verbalization Patterns in      scape for an Inclusive Digital India. arXiv:2603.28714.
Phone-Call Transcripts. In Proceedings of the 19th Confer-        Sarvam AI. 2026. Evaluating Indian Language ASR. https:
ence of the European Chapter of the Association for Com-          //www.sarvam.ai/blogs/evaluating-indian-language-asr. Ac-
putational Linguistics (Volume 5: Industry Track), 545–561.       cessed: 2026-06-29.
Rabat, Morocco: Association for Computational Linguistics.
                                                                  Sherwani, J.; Palijo, S.; Mirza, S.; Ahmed, T.; Ali, N.; and
Mukherjee, R. 2026.           What exactly is an AI voice         Rosenfeld, R. 2009. Speech vs. Touch-tone: Telephony In-
agent? And why does it matter in enterprise communica-            terfaces for Information Access by Low Literate Users. In
tion? https://www.techradar.com/pro/what-exactly-is-an-ai-        Proceedings of the 3rd International Conference on Infor-
voice-agent. Accessed: 2026-07-24.                                mation and Communication Technologies and Development
Mukherjee, S.; Sanz Ausin, M.; Aggarwal, K.; Datta, D.;           (ICTD), 447–457. IEEE.
Puri, S.; Jin, W.; Laud, T.; Manjunath, N.; Ding, J.; Paudel,
                                                                  Si, S.; Ma, W.; Gao, H.; Wu, Y.; Lin, T.-E.; Dai, Y.; Li, H.;
B.; Schellenberger, J.; Huo, Z. F.; Shen, W.; Shirazian, N.;
                                                                  Yan, R.; Huang, F.; and Li, Y. 2023. SpokenWOZ: A Large-
Potter, N.; Perkari, S.; Filippova, D.; Morozov, A.; Mease, A.;
                                                                  Scale Speech-Text Benchmark for Spoken Task-Oriented Di-
Muppalla, V.; Shakir, G.; Miller, A.; Ghukasyan, J.; Raglow-
                                                                  alogue Agents. In Advances in Neural Information Process-
Defranco, M.; Taylor, M.; Mahal, H.; and Agnew, J. 2026.
                                                                  ing Systems 36 (NeurIPS 2023), Datasets and Benchmarks
Perfecting Human-AI Interaction at Clinical Scale: Turning
                                                                  Track, 39088–39118.
Production Signals into Safer, More Human Conversations.
arXiv:2603.29893.                                                 Silero Team. 2024. Silero VAD: Pre-Trained Enterprise-
Mustafa, M.; Shahnawaz, A.; Ammara, U.; Abrar, M.;                Grade Voice Activity Detector. https://github.com/snakers4/
Ahtisham, B.; Qureshi, F. U.; Shahin, M.; and Ahmed, B.           silero-vad. Accessed: 2026-07-31.
2026. Awaaz-e-Sehat: A Mobile Voice-based AI System               Sun, G.; Feng, S.; Jiang, D.; Zhang, C.; Gasic, M.; and Wood-
for EMR Generation and Clinical Decision Support in Low-          land, P. 2024. Speech-based Slot Filling using Large Lan-
resource Maternal Healthcare. Proceedings of the ACM on           guage Models. In Findings of the Association for Compu-
Interactive, Mobile, Wearable and Ubiquitous Technologies,        tational Linguistics: ACL 2024, 6351–6362. Bangkok, Thai-
10(1): 16:1–16:37.                                                land: Association for Computational Linguistics.
Vaessen, N. 2024. jiwer: Evaluate Automatic Speech Recog-                 Field                              Scoring
nition Systems. https://github.com/jitsi/jiwer. Accessed:                 Name                               LLM judge
2026-08-01.                                                               District                           exact
                                                                          Clinic name                        LLM judge
Watson, C.; Parnaby, A. W.; and Kharrufa, A. 2024.                        Child’s name                       LLM judge
Precarious Experiences: Citizens’ Frustrations, Anxieties                 Pregnant?                          exact
and Burdens of an Online Welfare Benefit System.                          Gestational age                    exact
arXiv:2405.08515.                                                         Child’s DOB                        exact
Yoon, J.; Hwang, S.; Ran, H.; Bang, J.-U.; and Kim, K.-E.                 Calling number linked to clinic?   exact
                                                                          Number linked to clinic            exact
2023. Adapting Text-based Dialogue State Tracker for Spo-                 WhatsApp = calling number?         exact
ken Dialogues. In Proceedings of the Eleventh Dialog System               WhatsApp number                    exact
Technology Challenge, 81–88. Prague, Czech Republic: As-                  Aadhaar last 4 digits              exact
sociation for Computational Linguistics.
Zheng, L.; Chiang, W.-L.; Sheng, Y.; Zhuang, S.; Wu, Z.;          Table 8: How each form field is scored during EXTRACT
Zhuang, Y.; Lin, Z.; Li, Z.; Li, D.; Xing, E. P.; Zhang, H.;      evaluation. Open-ended text fields are evaluated using an
Gonzalez, J. E.; and Stoica, I. 2023. Judging LLM-as-a-           LLM judge, whereas every closed-ended field is scored by
Judge with MT-Bench and Chatbot Arena. In Advances in             exact match.
Neural Information Processing Systems (NeurIPS).

                                                                     Aapki di gayi saari jaankari hamare saath surakshit
                 A       Enrollment Form                             rahegi. Apna poora naam bataiye (Namaste! This is
The full call flow of the enrollment form is shown in Figure 3.      an automated call from a free maternal and child
                                                                     health service. You contacted the Anganwadi to join
                     B    LLM Judges                                 our service. This is a free service through which you
All LLM judges receive the conversation history, together            will receive useful information about mother and child
with the agent output being graded, as the input, and produce        health. To enroll you in our service we will ask you
a boolean score indicating whether the agent’s output adheres        a few questions. Please answer them by speaking. All
to the judge criteria, following the LLM-as-a-judge paradigm         the information you give will stay safe with us. Please
(Zheng et al. 2023). The temperature is set to 0 for every LLM       tell me your full name.)
judge inference.                                                     user: Mera poora naam Mrinmayee Kshirsagar hai
                                                                     (My full name is Mrinmayee Kshirsagar.)
B.1   EXTRACT Judges
Each extracted field is scored either by exact match or by an        Evaluation. The turn is scored on the extraction call
LLM judge (Table 8), as is the acknowledgement the agent             the agent makes. One field, the caller’s name, is open-
emits alongside the extraction. openai/gpt-5.4-mini                  ended and so is sent to an LLM judge with the cri-
is used as the judge model. The following instructions are           teria below; the acknowledgement is judged against
added as the system prompt for the LLM judge, in which               a rubric, since it has no single correct answer. Both
{{criteria}} is replaced by the criteria for the field               criteria follow.
being scored:                                                        Acknowledgement criteria. A brief acknowledgement
   You are a highly accurate evaluator checking whether              of the user’s previous answer, made of real words (not a
   the value an agent produced for a single tool-call ar-            non-lexical sound, grunt, or filler). This is encompass-
   gument satisfies a given criteria.                                ing and NOT restricted to any specific words: accept
   You will be given the tool name, the argument name,               a receipt, back-channel, reassurance, praise, or tran-
   and the actual value the agent produced for that argu-            sition phrase in any language, for example (but not
   ment.                                                             strictly limited to) thik hai, achcha, ji haan, samajh
                                                                     gaya, koi baat nahi, “okay”, “yes”, “alright”, “got it”,
   Mark match true only if the actual value satisfies the
                                                                     “thank you”, “no problem”. Do not require any par-
   following criteria, and false otherwise:
                                                                     ticular phrase, a ‘hearing-only’ tone, or extra brevity;
   {{criteria}}                                                      phrases that imply the agent understood or accepted
  An example is given below.                                         the answer (e.g. samajh gaya, “got it”) are acceptable.
                                                                     Only a missing acknowledgement, or a non-lexical
   Conversation history                                              sound/filler, should fail this criterion.
   assistant: Namaste! Yah ek automated call hai, ek
   nishulk maatru evam shishu swasthya seva ki taraf se.             Name criteria. The captured value refers to the SAME
   Aapne hamari seva se judne ke liye Anganwadi se                   name as “Mrinmayee Kshirsagar” when read aloud.
   sampark kiya hai. Yah ek muft seva hai, jismein aapko             Treat them as EQUAL when they differ only by: letter
   maa aur bachche ke swasthya se judi upyogi jaankari               casing; leading/trailing or internal word spacing; or
   milegi. Hamari seva se judne ke liye hum aapse kuch               a reasonable alternative romanisation / transliteration
   sawal poochhenge. Kripya unke jawab bolkar dein.                  of the same spoken Hindi name, for example ‘ksh’
                                                 Start the Call




                                                                         plays: "Hello! This is an automated call from a free maternal
                                                                         and child health service. You contacted the clinic to join. We will
                                                  Intro Script           ask a few questions; please answer by voice. Your information
                                                                         stays safe with us."




                    e.g. "Sunita Devi"               Name                                                                  Retry 1             skip to next question




                    choose one:
                    Kamrup Metropolitan,
                    Gaya, Leh,
                                                    District                                                               Retry 1               Retry 2
                    Mayurbhanj,
                    Dakshina Kannada




                    e.g. "City Clinic"           Clinic name                                                               Retry 1             skip to next question




                                                    Are you
                                 Yes                                                                                       Retry 1               Retry 2
                                                   pregnant?




e.g. "5" (months)        Gestational age                                                                                   Retry 1               Retry 2




                                                        No                        Child's name                             Retry 1


                                                                                     e.g. "Aarav"




                                                                                   Child's DOB                             Retry 1               Retry 2


                                                                                  e.g. "15-04-2025"



                                                                            plays: "Now only 3 questions are left."
                                                  Mid-Call Script
                                             ("only 3 questions left")




                                                  Phone linked
                                                                                                                           Retry 1               Retry 2               skip to next question
                                                    to clinic?




                                                                                  Number linked
                                                        No                                                                 Retry 1               Retry 2               skip to next question
                                                                                    to clinic

                                                                                  e.g. "9876543210"
                        Yes


                                                  WhatsApp =
                                                                                                                           Retry 1               Retry 2               skip to next question
                                                calling number?




                                                        No                     WhatsApp number                             Retry 1               Retry 2               skip to next question


                                                                                  e.g. "9876543210"
                        Yes

                                                                         plays: "This is the last question."
                                             Last-Question Script




                                                 Last 4 digits of
                        e.g. "4321"                                                                                        Retry 1               Retry 2               skip to next question
                                                  Aadhaar card




                                                                                                                                                                                                                       plays: "Sorry, we could not record your information
                                                                                                                                                                                               Incomplete-end Script   now, so the call is ending. Thank you."




    plays: "Thank you for sharing. We will       Ending Script                                                                                                                                    End the Call
    connect you to the service soon."




Figure 3: Call flow of the enrollment form used to build FormVoiceAgentBench. The agent speaks first and asks one question
at a time, in the order shown. The answers to the branching questions decide which of the conditional fields are asked next. If
a caller gives no valid answer, the rule-based layer re-prompts up to the retry limit shown for that field, and then either skips to
the next question or ends the call marking it incomplete. Aadhaar is India’s national ID, of which only the last four digits are
collected.
   vs ‘ksha’, doubled vs single consonants, an inserted or        has been pregnant must be 3 (months). The acknowl-
   dropped short ‘a’/schwa vowel, ‘v’ vs ‘w’, or ‘s’ vs ‘sh’      edgement is judged against the same rubric as before.
   (so ‘Ghorakshpalli’, ‘Ghorakshapalli’ and ‘Goraksha
   Palli’ are all equal). Mark it NOT equal only if it         B.2   REPLY Judges
   is a genuinely different name or refers to a different      Each reply is graded independently on five dimensions, each
   place/word, not for spelling or casing variants of the      using a separate LLM judge:
   same name.
                                                                  Correctness (openai/gpt-5.4-mini): does the
   The field scored above, the caller’s name, is open-ended:      reply ask the question the rule-based layer selected?
the same spoken answer can be written many ways (for ex-          Hindi Language adherence (openai/gpt-5.5):
ample, “Lakshmi” or “Laxmi”). An LLM judge therefore              is the reply in Hindi?
decides whether the extracted value matches a given rubric
                                                                  Reply Conciseness (openai/gpt-5.4-mini): is
for that field. “Anganwadi” refers to the local clinic.
                                                                  it a single question (with an optional informational
   A closed-ended field has one correct value and the ex-
                                                                  note on the form progress)?
tracted value is compared directly to it. The example below
illustrates this.                                                 No Acknowledgement (openai/gpt-5.5): does
                                                                  it avoid generating any form of acknowledgement for
   Conversation history                                           the previous user answer?
   assistant: Namaste! Yah ek automated call hai, ek              No Value Echo (openai/gpt-5.5): does it avoid
   nishulk maatru evam shishu swasthya seva ki taraf se.          reading the captured value back to the caller?
   Aapne hamari seva se judne ke liye Anganwadi se
                                                                 The full prompt for each is given in the example below.
   sampark kiya hai. Yah ek muft seva hai, jismein aapko
                                                               Only the “Correctness” prompt varies by test case; the other
   maa aur bachche ke swasthya se judi upyogi jaankari
                                                               four are the same for every reply.
   milegi. Hamari seva se judne ke liye hum aapse kuch
   sawal poochhenge. Kripya unke jawab bolkar dein.            Example. A REPLY test case is shown below, with the
   Aapki di gayi saari jaankari hamare saath surakshit         same conventions.
   rahegi. Apna poora naam bataiye (Namaste! This is
                                                                  Conversation history
   an automated call from a free maternal and child
   health service. You contacted the Anganwadi to join            assistant: Namaste! Yah ek automated call hai, ek
   our service. This is a free service through which you          nishulk maatru evam shishu swasthya seva ki taraf se.
   will receive useful information about mother and child         Aapne hamari seva se judne ke liye Anganwadi se
   health. To enroll you in our service we will ask you           sampark kiya hai. Yah ek muft seva hai, jismein aapko
   a few questions. Please answer them by speaking. All           maa aur bachche ke swasthya se judi upyogi jaankari
   the information you give will stay safe with us. Please        milegi. Hamari seva se judne ke liye hum aapse kuch
   tell me your full name.)                                       sawal poochhenge. Kripya unke jawab bolkar dein.
                                                                  Aapki di gayi saari jaankari hamare saath surakshit
   user: Mera poora naam Mrinmayee Kshirsagar hai
                                                                  rahegi. Apna poora naam bataiye (Namaste! This is
   (My full name is Mrinmayee Kshirsagar.)
                                                                  an automated call from a free maternal and child
   assistant: Theek hai. Apne zile ka naam bataayein (All         health service. You contacted the Anganwadi to join
   right. Please tell me the name of your district.)              our service. This is a free service through which you
   user: Form ke liye, mera zila Kamrup Metropolitan              will receive useful information about mother and child
   hai. (For the form, my district is Kamrup Metropoli-           health. To enroll you in our service we will ask you
   tan.)                                                          a few questions. Please answer them by speaking. All
   assistant: Theek hai. Apne Anganwadi ka naam                   the information you give will stay safe with us. Please
   bataayein (All right. Please tell me the name of your          tell me your full name.)
   Anganwadi.)                                                    user: Mera poora naam Mrinmayee Kshirsagar hai
   user: Mere aanganwadi ka naam Ghorakshpalli hai                (My full name is Mrinmayee Kshirsagar.)
   (The name of my Anganwadi is Ghorakshpalli.)                   assistant: Theek hai. Apne zile ka naam bataayein (All
   assistant: Theek hai. Kya aap abhi garbhvati hain?             right. Please tell me the name of your district.)
   (All right. Are you currently pregnant?)                       user: Form ke liye, mera zila Kamrup Metropolitan
   user: Haan main abhi garbhvati hoon. (Yes, I am cur-           hai. (For the form, my district is Kamrup Metropoli-
   rently pregnant.)                                              tan.)
   assistant: Theek hai. Aapko garbhvati hue kitne                assistant: Theek hai. Apne Anganwadi ka naam
   mahine hue hain? (All right. How many months preg-             bataayein (All right. Please tell me the name of your
   nant are you?)                                                 Anganwadi.)
   user: Abhi meri pregnancy teen mahine ki hai. (My              user: Mere aanganwadi ka naam Ghorakshpalli hai
   pregnancy is three months along right now.)                    (The name of my Anganwadi is Ghorakshpalli.)
                                                                  assistant: Theek hai. Kya aap abhi garbhvati hain?
   Evaluation. The extracted value for how long the user          (All right. Are you currently pregnant?)
user: Haan main abhi garbhvati hoon. (Yes, I am cur-           with its substantive line. Examples: the question, the
rently pregnant.)                                              re-ask, or a required informational/skip script like stat-
tool: validate_user_turn                                       ing the progress update of the form completion so far,
tool output: Correct value True captured for the preg-         etc. It contains NO acknowledgement of the user’s
nancy field. Pending questions: (1) gestational age in         previous answer like one or more of the following but
months, optional, integer, script “Aapko garbhvati hue         not strictly limited to them: no receipt, back-channel,
kitne mahine hue hain?” (How many months pregnant              reassurance, praise, or transition phrase in any lan-
are you?); the answer is a number of months.                   guage (e.g. “it’s okay”, “okay”, “yes”, “alright”, “got
                                                               it”, “thank you”, “no problem”).
Evaluation. The reply the agent produces next is sent
to all five judges. Each judge receives the conversation       No Value Echo. You are a highly accurate evaluator
above and their respective system prompts.                     checking whether an agent’s reply avoids echoing the
                                                               user’s just-provided value. You will be given a con-
Correctness. You are a highly accurate evaluator eval-         versation between a user and an agent along with
uating the response of an agent to a user’s message.           the agent’s response to the final user message. You
You will be given a conversation between a user and            need to evaluate if the response adheres to the eval-
an agent along with the response of the agent to the fi-       uation criteria: The reply does not read back, repeat,
nal user message. You need to evaluate if the response         or confirm the specific value the user just provided
adheres to the evaluation criteria: The reply advances         for the field that was just captured (e.g. echoing their
the interview to the correct next question: the one            name/number/DOB etc. back at them as confirma-
whose script is “Aapko garbhvati hue kitne mahine              tion). Asking the next scripted question, or speaking
hue hain?” (How many months pregnant are you?).                a required verbatim re-ask line, even one containing
It asks that specific question (not an earlier, later, or      a quoted example token, is NOT an echo and must
invented one), does not re-ask an already-answered             pass. The chat history will contain a tool call prior to
question, and does not end the call.                           the last agent message. You are not supposed to check
                                                               the agent message against that tool call message. You
Hindi Language adherence. You are a highly accurate            need to compare the last agent message with only the
evaluator checking the language of an agent’s reply.           user messages prior to it.
You will be given a conversation between a user and
an agent along with the agent’s response to the final       B.3    Calibration Procedure
user message. You need to evaluate if the last agent        Every judge was calibrated against human labels before being
response adheres to the evaluation criteria: The last       used to score the benchmark. We drew a batch of 50 unit tests,
agent reply should be largely written in Hindi (De-         ran each judge over them, and had the authors independently
vanagari script). It does not switch to roman alphabets     label every judgment. The initial prompts were not fully
or english words except for using proper nouns and ev-      aligned: each judge disagreed with the human label on some
eryday common-use english words in devnagari (e.g.          cases. We revised the prompts over several iterations until
saying “Whatsapp” as its Devanagari transliteration is      every judge agreed with the human labels on all 50 tests. We
fine) or digits in roman numerals are fine. If you think    then applied the final prompts unchanged to a held-out batch
there has been any violation, give concrete examples        of 50 tests that had played no part in the iteration, on which
of the violation in your reasoning.                         the LLM judge outputs matched the human labels on every
                                                            case. We acknowledge that the size of the calibration dataset
Reply Conciseness. You are a highly accurate eval-
                                                            is small and plan to expand it in future work.
uator checking whether an agent’s reply is concise.
You will be given a conversation between a user and
an agent along with the agent’s response to the final          C    Full Results with Confidence Intervals
user message. You need to evaluate if the response ad-      Tables 9–12 show the model comparison results for speech-
heres to the evaluation criteria: The reply is concise:     to-text (STT), extraction accuracy, form completion and re-
it asks exactly ONE question, optionally preceded by        sponse accuracy with 95% confidence intervals.
the ONE informational preamble the script requires
for this field. It does not bundle multiple questions,       Model                  WER ↓      LLM-WER ↓ Cost ($) ↓
enumerate pending fields, summarise progress, or add         Scribe v2        0.835 ± 0.015 0.062 ± 0.024   0.172
chit-chat beyond what the script requires.                   Chirp 3          0.981 ± 0.007 0.055 ± 0.025   0.424
                                                             Saaras v3        1.007 ± 0.004 0.074 ± 0.028   0.137
No Acknowledgement. You are a highly accurate eval-          GPT-4o-transcr. 1.012 ± 0.004 0.127 ± 0.033    0.159
uator checking whether an agent’s reply is free of any       Nova-3          0.826 ± 0.015 0.104 ± 0.031   0.127
acknowledgement of the user’s previous answer. You
will be given a conversation between a user and an          Table 9: Comparison of STT models. Since models have
agent along with the agent’s response to the final user     different billing units, the total cost (USD) of transcribing
message. You need to evaluate if the response adheres       the entire benchmark is reported.
to the evaluation criteria: The reply begins directly
                         Model                Reference    Saaras v3    Scribe v2     Nova-3
                         GPT-5.5            99.79 ± 0.99 95.53 ± 1.03 98.62 ± 0.64 95.16 ± 1.07
                         Gemini 3.5 Flash   99.36 ± 1.22 95.69 ± 1.01 98.94 ± 0.58 96.38 ± 0.94
                         Claude Opus 4.8    99.15 ± 1.32 96.22 ± 0.96 98.40 ± 0.67 96.01 ± 0.98
                         Claude Sonnet 4.6  99.15 ± 1.32 96.01 ± 0.98 98.94 ± 0.58 95.96 ± 0.99
                         GLM-5.1            98.72 ± 1.48 94.52 ± 1.12 63.40 ± 2.20 95.43 ± 1.05
                         Gemini Pro         97.23 ± 1.90 94.26 ± 1.15 97.29 ± 0.84 94.63 ± 1.12
                         Gemini 2.5 Flash   96.17 ± 2.14 95.27 ± 1.06 98.03 ± 0.73 95.43 ± 1.05
                         Gemini 3 Flash     95.96 ± 2.19 84.79 ± 1.70 88.83 ± 1.50 86.28 ± 1.63
                         GPT-5.4-mini       92.34 ± 2.76 90.05 ± 1.43 96.76 ± 0.91 91.54 ± 1.34
                         Mistral Medium 3.5 89.36 ± 3.11 87.82 ± 1.56 92.34 ± 1.29 87.77 ± 1.56
                         GPT-4.1            85.11 ± 3.51 75.53 ± 1.99 78.94 ± 1.91 79.84 ± 1.87

      Table 10: Per-turn extraction accuracy using reference transcripts and the outputs of the three STT models as inputs.

                        Model                Reference     Saaras v3    Scribe v2     Nova-3
                        Gemini 3 Flash     100.00 ± 0.00 85.24 ± 0.77 89.48 ± 0.60 83.92 ± 1.01
                        Gemini 3.5 Flash   100.00 ± 0.00 90.74 ± 0.61 92.50 ± 0.53 87.09 ± 0.76
                        GPT-5.5             99.95 ± 0.09 89.97 ± 0.73 89.37 ± 0.64 84.73 ± 0.80
                        Claude Sonnet 4.6   99.66 ± 0.23 91.55 ± 0.71 93.01 ± 0.50 84.54 ± 0.77
                        GLM-5.1             99.56 ± 0.27 90.92 ± 0.75 58.66 ± 1.46 86.09 ± 0.75
                        Claude Opus 4.8     99.41 ± 0.31 92.22 ± 0.61 92.03 ± 0.56 85.83 ± 0.88
                        Gemini 2.5 Flash    99.06 ± 0.38 91.76 ± 0.70 92.39 ± 0.52 85.50 ± 0.73
                        Gemini Pro          98.90 ± 0.42 92.55 ± 0.52 93.47 ± 0.45 86.53 ± 0.70
                        GPT-5.4-mini        98.35 ± 0.48 90.68 ± 0.75 90.10 ± 0.55 84.40 ± 0.79
                        GPT-4.1             95.99 ± 0.70 88.82 ± 0.74 91.50 ± 0.53 86.33 ± 0.74
                        Mistral Medium 3.5 92.83 ± 0.68  90.39 ± 0.68 91.84 ± 0.49 83.37 ± 0.76

Table 11: End-to-end form-completion accuracy using reference transcripts and the outputs of the three STT models as inputs.

                      Model                     Response accuracy         Latency (ms)      Cost ($/turn)
                                             Reference       Scribe v2
                      Claude Sonnet 4.6 100.00 ± 0.00 97.77 ± 0.75 5148 ± 392  0.0146 ± 0.0000
                      GPT-4.1           100.00 ± 0.00 96.60 ± 0.91 3647 ± 656  0.0025 ± 0.0001
                      GPT-5.4-mini       98.09 ± 1.28 96.70 ± 0.85 3356 ± 523 0.0008 ± 0.0000
                      Gemini 3 Flash     97.23 ± 1.49 96.17 ± 0.96 2661 ± 239 0.0017 ± 0.0000
                      Gemini 3.5 Flash   97.02 ± 1.28 94.73 ± 1.11 3496 ± 1322 0.0052 ± 0.0001

           Table 12: REPLY response accuracy using reference transcripts and transcripts from Scribe v2 as inputs.


                 D     Model Selection                              after 0.2 s of silence, and ignores any audio that scores below
D.1    EXTRACT Selection                                            0.7 confidence or 0.6 loudness. The agent waits a further 0.4
                                                                    s after that before marking the turn as completed, so a caller
Table 13 gives the optimal EXTRACT model using the                  pausing mid-answer is not cut off. If the caller has not spo-
weighted-sum scalarization method for 0.50 ≤ wa ≤ 0.90              ken for more than 3.0 s since the agent stopped speaking, we
with wℓ = 0.1.                                                      re-prompt. Each audio file in the benchmark is 16 kHz mono
                                                                    16-bit PCM.
D.2    REPLY Selection
GPT-5.4-mini is optimal throughout 0.50 ≤ wa ≤ 0.90                 Models. All LLM calls are served through OpenRouter
(wℓ = 0.1), among the models on the Pareto frontier (Fig-           (OpenRouter 2026). We set the temperature to 0 for non-
ure 4), with a consistent composite score of U = 0.9 across         reasoning models, and the reasoning effort to “medium” for
the sweep.                                                          EXTRACT and “low” for REPLY. For both, we cap the out-
                                                                    put at 16,000 tokens and pass the most recent 200 turns of
                                                                    the conversation as input. For TTS, we use Google Cloud
             E    Implementation Details                            Chirp 3 HD (Google Cloud 2026) with the female Hindi
Orchestration and telephony. We use Pipecat (Pipecat AI             voice Achernar, slowed to 0.9× the default speed so the
2026a) for orchestration and Exotel (Exotel 2026) for tele-         questions are easier to follow.
phony, which delivers 8 kHz µ-law audio over a WebSocket.
For VAD, we use Silero (Silero Team 2024) at the same 8 kHz         Evaluation harness. All STT and LLM evaluations were
sample rate. It marks the start of speech after 0.1 s, the end      run using Calibrate (Dalmia and Doshi 2025).
                                    wa wc Model                  U wa wc Model              U wa wc Model              U
                                   0.50 0.40 Gemini 3.5 Flash 0.763 0.64 0.26 Sonnet 4.6 0.776 0.78 0.12 Sonnet 4.6 0.843
                                   0.51 0.39 Gemini 3.5 Flash 0.763 0.65 0.25 Sonnet 4.6 0.781 0.79 0.11 Sonnet 4.6 0.848
                                   0.52 0.38 Gemini 3.5 Flash 0.763 0.66 0.24 Sonnet 4.6 0.786 0.80 0.10 Sonnet 4.6 0.852
                                   0.53 0.37 Gemini 3.5 Flash 0.763 0.67 0.23 Sonnet 4.6 0.791 0.81 0.09 Sonnet 4.6 0.857
                                   0.54 0.36 Gemini 3.5 Flash 0.763 0.68 0.22 Sonnet 4.6 0.795 0.82 0.08 Sonnet 4.6 0.862
                                   0.55 0.35 Gemini 3.5 Flash 0.763 0.69 0.21 Sonnet 4.6 0.800 0.83 0.07 Sonnet 4.6 0.867
                                   0.56 0.34 Gemini 3.5 Flash 0.764 0.70 0.20 Sonnet 4.6 0.805 0.84 0.06 Sonnet 4.6 0.871
                                   0.57 0.33 Gemini 3.5 Flash 0.764 0.71 0.19 Sonnet 4.6 0.810 0.85 0.05 Sonnet 4.6 0.876
                                   0.58 0.32 Gemini 3.5 Flash 0.764 0.72 0.18 Sonnet 4.6 0.814 0.86 0.04 Sonnet 4.6 0.881
                                   0.59 0.31 Gemini 3.5 Flash 0.764 0.73 0.17 Sonnet 4.6 0.819 0.87 0.03 Sonnet 4.6 0.886
                                   0.60 0.30 Gemini 3.5 Flash 0.764 0.74 0.16 Sonnet 4.6 0.824 0.88 0.02 Sonnet 4.6 0.890
                                   0.61 0.29 Gemini 3.5 Flash 0.764 0.75 0.15 Sonnet 4.6 0.829 0.89 0.01 Sonnet 4.6 0.895
                                   0.62 0.28 Sonnet 4.6       0.767 0.76 0.14 Sonnet 4.6 0.833 0.90 0.00 Sonnet 4.6 0.900
                                   0.63 0.27 Sonnet 4.6       0.772 0.77 0.13 Sonnet 4.6 0.838

Table 13: Optimal EXTRACT model under weighted-sum scalarization for 0.50 ≤ wa ≤ 0.90, with wℓ = 0.1 and wc =
1 − wa − wℓ , and its composite score U .




Response accuracy (%)
                                GPT-5.4-mini
                        96.8%

                        96.6%

                        96.4%

                        96.2%               Gemini 3 Flash

                         96%

                                      $0.001        $0.0015       $0.002

                                            Cost (USD)

Figure 4: Cost–quality–latency trade-off among REPLY
models satisfying the deployment constraints. The logarith-
mic x-axis shows cost per turn, the y-axis shows response
accuracy using Scribe v2 transcripts, and marker area en-
codes p95 latency per turn (bigger is slower). Both models
are Pareto-optimal across the three objectives. The model
selected for deployment is highlighted.


Environment. Experiments were run from a MacBook
Pro (Apple M4 Pro, 24 GB) on macOS 15.7 with
Python 3.11, using pipecat-ai 1.2.1, openai 2.15.0,
instructor 1.13.0, pydantic 2.12.3, jiwer (Vaessen
2024) 4.0.0, indic-nlp-library (Kunchukuttan 2020)
0.92, pydub 0.25.1 and numpy 2.2.6.
Determinism. No random seeds were set: every model is
served by a hosted API that offers no determinism guarantee,
so identical settings can still produce different outputs. Each
configuration was evaluated once over the full test suite, so
the confidence intervals in Section C reflect variation across
test items rather than across repeated runs.

