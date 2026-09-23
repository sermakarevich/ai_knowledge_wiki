> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# LiveKit on Telnyx: Lower Cost, Low Latency Voice AI Infrastructure — In Plain Language

## What is this about?

Imagine you built a voice assistant — software that can talk on the phone
like a person. To make that work, you need several pieces: a way to carry
the call audio, a way to turn speech into text, a brain that decides what
to say, and a way to turn the answer back into spoken voice.

LiveKit is a popular open toolkit that handles the first piece: carrying
real-time audio and video between callers and software agents. Many
developers run their voice agents on LiveKit's own hosting service,
called LiveKit Cloud.

Telnyx is a phone company that owns its own worldwide calling network — the wires, servers, and connections that carry phone calls across the globe.

This announcement says: you can now run your LiveKit voice agents on Telnyx's network instead of LiveKit Cloud. Telnyx hosts the whole thing for you — your agent plus the speech models — on equipment it owns itself.

The promise is simple: the same LiveKit tools developers already know,
but cheaper to run, faster to respond, and with proper phone-company
features built in from the start.

## Why does it matter?

Voice AI is growing up. A year or two ago, most voice agents were demos
and experiments. Now companies want to put them on real customer phone
lines, handling thousands of calls a day.

At that scale, three problems show up on standard cloud hosting:

1. **The bill gets big.** Every minute of talking costs money — for the
   call itself, plus fees for the speech-recognition and voice-generation
   services, which are often resold from other companies at a markup.

2. **Pauses feel awkward.** If the agent takes a second to answer, callers
   notice. They start saying "hello? are you still there?" Each extra hop
   — sending audio off to some other company's server and waiting for a
   reply — adds delay.

3. **Phone features are missing.** Real call centers need clear HD sound,
   clean transfers ("let me connect you to billing"), verified caller ID
   so calls are not flagged as spam, and recordings for legal compliance.
   Generic cloud hosting does not always provide these.

Telnyx's pitch is that owning the full chain — the phone network, the
computers running the AI models, and the hosting for your agent — solves
all three problems at once. For a business planning to run voice agents
in production, that difference decides whether the project is affordable
and pleasant enough for real customers.

## How does it work?

Think of a phone call to an AI agent as a relay race with four runners:

1. The caller speaks. The audio travels over the phone network.
2. A speech-to-text model writes down what was said.
3. A language model decides on a reply.
4. A text-to-speech model reads the reply out loud to the caller.

Normally, each runner can be in a different building — even a different
city. The audio has to travel between them over the internet, and every
trip adds milliseconds of delay.

Telnyx puts all four runners on the same track. Here is how:

- **Your agent moves in.** You take the agent program you already wrote
  (typically a file called `agent.py`), pack it with a setup file
  (a Dockerfile), zip it up, and send it to Telnyx through a single
  command. Telnyx builds it and runs it on its own servers. You also
  switch your connection address from LiveKit Cloud to Telnyx, using the
  same dashboard or command-line tool you already use.

- **The voice models live next door.** Instead of renting speech-to-text
  and text-to-speech from outside providers, Telnyx runs those models on
  its own graphics processors (GPUs) — the powerful chips AI needs —
  sitting in the same data centers as its phone equipment.

- **Calls stay local.** Telnyx has phone connection points around the
  world. A call gets answered close to where it comes from, and the AI
  processing happens right there too. No long detour to an outside
  service and back.

The result Telnyx reports: about 200 milliseconds from the moment you
stop speaking to the moment the agent starts answering — roughly the
length of a blink, short enough that most people do not sense a pause.

On top of that, because Telnyx is an actual phone carrier, the boring
but important phone features come along for free: sharp HD voice sound,
one-step call transfers, verified caller ID, and built-in call recording
with compliance controls.

## Where can this be used?

Anywhere a business answers the phone at volume and wants software to
help — or to take the call end to end:

- **Customer support lines.** An agent answers common questions instantly,
  day or night, and hands tricky cases to a human with a clean transfer.
- **Appointment booking and reminders.** Clinics, repair shops, and
  salons can let callers schedule, reschedule, and confirm by voice.
- **Order status and delivery updates.** Shoppers call in, the agent
  looks up the order and reads out where it is.
- **Lead qualification and sales callbacks.** The agent asks the first
  round of questions, then passes genuinely interested callers to a
  salesperson.
- **Surveys and follow-ups.** After a visit or purchase, the agent calls
  back to collect feedback in natural conversation.
- **Internal help desks.** Employees call one number for IT or HR
  questions and get answers without waiting on hold.

In short, any phone workflow that today means "wait on hold, then repeat
yourself to three people" is a candidate.

## Conclusions & takeaways

- Voice agents are moving from experiments to everyday business phone
  lines, so the infrastructure underneath them has to be cheap, fast,
  and dependable.
- Telnyx's answer is to run the familiar LiveKit toolkit on hardware and
  phone lines it owns outright, cutting out middlemen.
- The headline claims: roughly half the cost of LiveKit Cloud, replies
  starting in about 200 milliseconds, and carrier-grade phone features
  included rather than bolted on.
- For developers, the switch is deliberately low-friction: same code,
  same tools, just a new address plus a zip-file upload — then point a
  phone number at the agent and start taking calls.
- The big idea worth remembering: **where the AI sits matters.** Putting
  the smarts right next to the phone lines removes delays and fees that
  no amount of clever coding can fix from far away.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| LiveKit | An open toolkit for sending live audio and video between people and software. |
| LiveKit Cloud | LiveKit's own paid hosting service for running voice and video apps. |
| Voice AI agent | A program that talks on the phone like a person: it listens, thinks, and speaks. |
| STT (speech-to-text) | Technology that writes down what a caller just said. |
| TTS (text-to-speech) | Technology that reads a written reply out loud in a natural-sounding voice. |
| GPU infrastructure | Banks of powerful computer chips that AI models need to think quickly. |
| Point of presence | A local Telnyx data center where calls connect and get processed nearby. |
| Colocation | Putting the phone equipment and the AI computers in the same place to cut travel time. |
| Round-trip time | How long from when you finish speaking until the agent starts answering. |
| SIP REFER | The standard phone-network trick for transferring a live call to someone else. |
| STIR/SHAKEN attestation | A verification stamp on caller ID proving the call is really from who it claims. |
| AMR-WB | A sound format that makes phone calls clearer, often called HD voice. |
