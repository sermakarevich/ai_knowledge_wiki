> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Interruption Types
**In one sentence:** IHBench defines six interruption types spanning cooperative (normal, filler) through directive (impatient, correction) to adversarial (pushback, topic switch) intents, each with a type-specific recovery requirement.
## Key points
- Correction means the user corrects something said in a prior turn (e.g. "Actually wait, use my work email instead"); recovery requires accepting the correction without pushback, integrating the corrected value, and continuing.
- Topic switch means the user introduces an unrelated request (e.g. "Oh by the way, can you check my outstanding invoices?"); recovery requires addressing the new topic, then steering back to the original workflow without blending the two.
- Filler is a brief backchannel that does not change the task (e.g. "mm-hm," "yeah," "right"); recovery requires exactly continuing the interrupted utterance from where it was cut off, without repeating, restarting, or acknowledging the filler.
- Pushback means the user challenges or resists the assistant's claim or request (e.g. "I'm not comfortable giving that out over the phone"); recovery requires empathetic de-escalation and offering alternatives.
- The six types were chosen to span interruption intents observed in real customer-service conversations, ordered from cooperative (normal, filler) through directive (impatient, correction) to adversarial (pushback, topic switch).
- The distribution of interruption types across the benchmark is reported in Appendix A.
---
## Correction
**Covers:** Section 3 interruption-type definition (Correction)

> "Correction. The user corrects something they previously said in a prior turn (e.g., "Actually wait, use my work email instead"); recovery requires accepting the correction without pushback, integrating the corrected value, and continuing."

## Topic switch
**Covers:** Section 3 interruption-type definition (Topic switch)

> "Topic switch. The user introduces an unrelated request (e.g., "Oh by the way, can you check my outstanding invoices?"); recovery requires addressing the new topic, then steering back to the original workflow without blending the two."

## Filler
**Covers:** Section 3 interruption-type definition (Filler)

> "Filler. A brief backchannel that does not change the task (e.g., "mm-hm," "yeah," "right"); recovery requires exactly continuing the interrupted utterance from where it was cut off, without repeating, restarting, or acknowledging the filler."

## Pushback
**Covers:** Section 3 interruption-type definition (Pushback)

> "Pushback. The user challenges or resists the assistant's claim or request (e.g., "I'm not comfortable giving that out over the phone"); recovery requires empathetic de-escalation and offering alternatives."

## Type spectrum and selection
**Covers:** Section 3 type spectrum and distribution note

> "These types were chosen to span the space of interruption intents observed in real customer-service conversations, from cooperative (normal, filler) through directive (impatient, correction) to adversarial (pushback, topic switch). The distribution of interruption types across the benchmark is reported in Appendix A."

| Spectrum band | Types named in chunk |
|---|---|
| Cooperative | normal, filler |
| Directive | impatient, correction |
| Adversarial | pushback, topic switch |
