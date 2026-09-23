> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# MSI-Bench: Evaluating Multi-Speaker Voice Interaction for Collaborative AI Agents — In Plain Language

## What is this about?

Most voice assistants are built for one person talking to one helper.

MSI-Bench asks what happens when that assumption breaks: a kitchen full
of family, a hospital ward, a group dinner, a park full of background
chatter — several people talking, sometimes at once, each with their own
role, permissions, and secrets.

The paper introduces a test suite of 1,152 short multi-speaker audio
scenes, half in English and half in Mandarin. In each scene, the AI
assistant overhears a conversation between two or three people and must
decide what to do next: act, speak up, stay silent, or ask for
clarification.

The twist is that the right answer depends on *who said what* — not just
the words of the last request. Who authorized the action? Who is allowed
to hear the answer? Whose constraint applies to whom?

## Why does it matter?

Real assistants already live in shared spaces: smart speakers, cars,
hospital rooms, reception kiosks. A naive assistant that obeys whoever
spoke last will:

- reveal a birthday gift to the birthday person,
- let a child authorize a phone-plan change only a parent can approve,
- apply one guest's peanut allergy to the whole group's order,
- or invent an answer when it simply didn't hear.

The results show this is not a solved problem. The strongest tested
system handles every requirement correctly in only about two-thirds of
English cases (66.8%) and about half of Mandarin cases (54.5%). The best
open-weight system manages only 34.0% and 19.3%.

Memory is the weakest area, and many models fail at simple restraint:
they answer even when nobody was talking to them.

## How does it work?

Each test case is a small scripted world with fixed characters,
relationships, and a goal. The building process has four stages:

1. **Inputs.** Choose a setting from eight everyday domains (home,
   shopping, school, healthcare, leisure, transport, civic life, work)
   and define who is present and what they want.
2. **Planning.** A planner script writes the conversation flow, including
   traps: secrets to keep, unauthorized requests, conflicting wishes.
3. **Generation.** The dialogue, the correct tool calls (e.g. book a
   table, set a timer, register a loan), and a step-by-step grading
   checklist ("atomic rubric") are written out.
4. **Synthesis.** The dialogue is turned into realistic audio with cloned
   voices placed at different distances, background noise, and room echo,
   then hand-checked. Of 1,420 candidates, 1,152 passed review.

Testing covers three skill families, two patterns each:

- **Memory:** catch a key fact from faint background speech; track which
  constraint belongs to which person (e.g. the armchair is Grandma's, the
  no-shellfish rule is Uncle Ray's).
- **Instruction following:** keep secrets from the wrong listener
  (selective disclosure); refuse or defer actions the speaker has no
  right to order (speaker authority).
- **Reasoning:** untangle interleaved requests without mixing up whose is
  whose; satisfy a hard rule first (leash the dog, no entry before lab
  clearance) and fit in soft wishes only where they still fit.

Grading is done by an automated judge checking each rubric item, and it
agrees with human graders 82.6% of the time.

## Where can this be used?

- **Smart-home and car assistants** that must tell family members apart
  and keep surprises, PINs, and purchase approvals straight.
- **Healthcare and accessibility helpers** that enforce safety rules
  (isolation, medication, allergies) while still honoring small comfort
  requests like scheduling a video call.
- **Customer-service and front-desk agents** that hear staff, customers,
  and bystanders and must act only on properly authorized instructions.
- **Meeting and classroom tools** that summarize who asked for what and
  refuse to merge one person's correction into another person's request.
- **Benchmark builders** who need a template for testing group
  conversation: scene setup, decoy details, gold tool calls, and
  checklists that separate hearing failures from thinking failures.

## Conclusions & takeaways

- Group conversation is a distinct skill: knowing who spoke, who may
  decide, who may hear, and when to stay quiet.
- Experiments that swap audio for clean text transcripts show open models
  mostly fail at *hearing* (gains of 21–44 points on text), while top
  commercial models mostly fail at *reasoning* (still wrong 10–22% of the
  time with perfect transcripts).
- Adding a third speaker barely changes scores — the bottleneck is not
  headcount but keeping track of roles and permissions.
- Quiet background speech is fragile: as noise rises, capture collapses,
  and some models invent facts instead of admitting they missed them.
- The practical bar is "speaker-scoped behavior plus restraint": ground
  every action in the right speaker, disclose only to the right audience,
  and say nothing — or ask — when unsure.

## Jargon decoder

| Term | Plain meaning |
| ---- | ------------- |
| Speaker-scoped decision making | Choosing based on *who* said it, not just what was said. |
| Selective disclosure | Keeping a secret from one listener while helping others normally. |
| Speaker authority | Only the person with permission (owner, parent, account holder) can approve an action. |
| Atomic rubric | A grading checklist split into tiny yes/no items. |
| Gold tool call | The single correct machine action for the scene, e.g. book the 19:00 table. |
| Transcript lift / ablation | Re-running the test with clean text instead of audio to see if hearing was the problem. |
| SNR (signal-to-noise ratio) | How loud the important voice is compared to background noise. |
| Fabrication / hallucination | Inventing a fact (a time, a place) instead of admitting it was missed. |
| Conversational restraint | Staying silent or asking when nobody addressed you or the facts are unclear. |
