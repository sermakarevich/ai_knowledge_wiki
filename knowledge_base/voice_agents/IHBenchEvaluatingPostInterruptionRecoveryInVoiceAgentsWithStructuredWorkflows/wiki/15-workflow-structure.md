[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Workflow structure: stages, skip/failure and termination conditions
**In one sentence:** The chunk specifies a Disaster Housing Assistance state-machine workflow (steps 4–8: assess access/safety, gather availability, obtain consent, book, confirm/close) with explicit skip/terminate conditions and a terminal-success definition, illustrated by conversation excerpt messages 0–7 and the start of the message-1 interruption rubric.
## Key points
- Step 4 assesses access and safety needs (hazards, utilities, debris/blocked access, gates/lock codes, parking, pets, mobility/medical needs, restricted areas) and captures whether someone 18+ with photo ID can be present.
- Step 5 explains inspection duration (60–90 minutes) and allowed windows — Weekdays AM (8–12), PM (12–4), Late (4–6), limited Saturday AM, all Central Time — and asks for 2–3 preferred date/windows from the earliest available date.
- Step 6 discloses that SDHA uses contracted inspectors needing name, damaged property address, and contact number/email, asks explicit consent to share these and to send confirmation via the chosen contact method, with skip condition "Never" and hard-stop termination if consent is declined after clarification.
- Step 7 proposes the earliest matching slot from preferences and policy windows, confirms booking with a confirmation number, and reminds that an adult 18+ must be present, pets secured, and a clear path maintained.
- Step 8 reads back final date/window, address, access notes, presence requirement, and confirmation number, sends confirmation if consented, and provides the conversation reference ID plus reschedule/cancel recap, with skip condition "Never" and success termination when details are read back accurately with the confirmation number.
- Terminal success requires verified identity, confirmed address, collected access/safety notes, in-policy availability, explicit consent, a booked allowed-window slot no earlier than the earliest available date, confirmation number (INS-20260309-18427), and a complete final summary with reference ID (CR-20260305-6102); hard-stop failure covers unverifiable identity after two attempts, refused consent, withdrawn application, or declined proceed.
- The excerpt (messages 0–7) shows verification pushback: the user resists re-verification (case ID DR-4827315) and date-of-birth disclosure, and eventually provides "Marisol Ortega, date of birth November second, nineteen eighty four."
---
## 4) Assess Access and Safety Needs
**Covers:** workflow step 4; chunk pages 14–15

Ask about accessibility and special requirements: safety hazards, utilities status, debris/blocked access, gates or lock codes, parking constraints, pets on site, occupants with mobility/medical needs, restricted areas. Capture whether someone 18+ with photo ID can be present.

> ". . . [skip conditions, failure handling, terminate conditions]"

## 5) Gather Availability Preferences
**Covers:** workflow step 5

Explain inspection duration (60–90 minutes), presence requirement, and allowed windows: Weekdays AM (8–12), PM (12–4), Late (4–6), and limited Saturday AM, all in Central Time. Ask for 2–3 preferred date/windows starting from the earliest available date.

> ". . . [skip conditions, failure handling, terminate conditions]"

## 6) Obtain Consent to Share Details
**Covers:** workflow step 6

Disclose that SDHA uses contracted inspectors who need the applicant's name, damaged property address, and contact number/email to coordinate access and reminders. Ask for explicit consent to share these details with the assigned inspector and to send the appointment confirmation via their chosen contact method.

| Condition | Value in chunk |
|---|---|
| Skip conditions | Never. |
| Terminate conditions | Hard-stop if the user declines consent to share required contact details after clarification and confirms they do not wish to proceed. |

## 7) Propose and Book Appointment
**Covers:** workflow step 7

Using the user's preferences and policy windows, propose the earliest matching slot. On confirmation, state the inspection is booked and provide the confirmation number. Remind them an adult 18+ must be present, secure pets, and maintain a clear path.

> ". . . [skip conditions, failure handling, terminate conditions]"

## 8) Confirm Details and Close
**Covers:** workflow step 8

Read back the final date/window, damaged property address, key access notes, presence requirement, and the confirmation number. If consented, state you will send the confirmation. Provide the conversation reference ID and recap how to reschedule or cancel.

| Condition | Value in chunk |
|---|---|
| Skip conditions | Never. |
| Terminate conditions | Success when appointment details are read back accurately and the confirmation number is provided. |

In any failure case, close politely and provide the conversation reference ID. A fragment also states the assistant "confirms they want to stop" before terminating.

## Completion definition
**Covers:** terminal success and hard-stop failure definitions

Terminal success: Caller identity verified, damaged property address confirmed, access/safety notes collected, availability gathered within policy, explicit consent obtained, inspection slot booked in an allowed window starting no earlier than the earliest available date, confirmation number (INS-20260309-18427) provided, and complete final summary read back including conversation reference ID (CR-20260305-6102).

Hard-stop failure: Identity cannot be verified after two attempts; user refuses required consent; user withdraws application; user declines to proceed and confirms they want to stop (fragment: "confirms they want to stop. In any failure case, close politely and provide the conversation reference ID.").

## G.2 Conversation Excerpt (messages 0–7)
**Covers:** Disaster Housing Assistance excerpt, messages 0–7

- [0] Assistant [INTERRUPTED]: "Hi, this is the State Disaster Housing Assistance program calling about your disaster assistance application to coordinate your home inspection. This call will include verifying your case, scheduling an inspection window, and getting consent to share your contact details" [Undelivered: "with the inspector. Am I speaking with Marisol Ortega, and is now a good time to proceed? We can continue in English or Spanish. Also, for any follow-ups, what's your preferred contact method, call, text, or email?"]
- [1] User [pushback]: "Hold on, why are we verifying my case again? I already sent all that with my application. I mean, do you not have it on your end?"
- [2] Assistant [INTERRUPTED]: "I get it, you already provided that. We do a quick verification to protect your privacy before we talk about your case or schedule. It'll be fast. Could you please read your case ID for me? After that I'll confirm" [Undelivered: "your full name and date of birth."]
- [3] User [impatient]: "Yeah, it's DR-4827315. Let's keep this quick, please."
- [4] Assistant [INTERRUPTED]: "Thanks, that matches our records. To finish verification, please state your full legal name and your date of birth." [Undelivered: "This is just to protect your privacy, and then we'll go straight to scheduling."]
- [5] User [pushback]: "Wait, why do you need my date of birth if I already gave you the case ID? I mean, is that not enough to verify me? I'd rather not say that over the phone without a good reason."
- [6] Assistant [INTERRUPTED]: "I hear you, and I understand the concern. We use your date of birth with the case ID to securely match your record and protect your privacy. Without that quick check I can't move forward with scheduling. Please state your full legal name and date of birth. We'll use it only to verify your case on this call, and I'm" [Undelivered: "not asking for anything like SSN or financial info."]
- [7] User [impatient]: "Yeah, fine. Marisol Ortega, date of birth November second, nineteen eighty four. Let's just move on, please."

## G.3 Evaluation Rubric (Interruption at Message 1) — start
**Covers:** rubric header and Task Fulfillment Criterion opening (chunk cuts off mid-criterion)

Rubric for interruption at message 1 (pushback). Task Fulfillment Criterion: "The assistant briefly explains that verification is required before discussing case details to protect the applicant's privacy and to confirm they are speaking with the right person, then immediately requests the user to provide all three required verification elements by asking the user to read their case ID and to state their full legal name and date of birth (in one clear prompt or sequentially)."
