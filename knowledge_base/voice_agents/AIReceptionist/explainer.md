> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# AI Receptionist -- Open Source, Self-Hosted, No Compromises — In Plain Language

## What is this about?
This is a robot receptionist that answers a business phone for you.

It is free, open-source software you run on your own computer or
server. When someone calls your business number, the robot picks up,
greets the caller, answers common questions, passes the call to the
right person, takes a message, or even books an appointment.

The key idea: it talks almost like a real person. It listens and
speaks in one smooth step, instead of the older clunky way where a
robot had to write down what you said, think, and then read the
answer out loud in a robotic voice.

One warning comes with it: on 2026-06-03, the company behind the
voice technology (OpenAI) shut down an older test version of its
voice service. After that date, the robot only works with a regular
paid access key. The old login method connects the call but leaves
the caller hearing silence.

The project is still being actively built. The basics work — voice
chats, answering common questions, passing calls along, taking
messages — but rough edges and breaking changes are expected.

## Why does it matter?
Most small businesses have three bad choices: miss calls, pay a
human to sit by the phone, or pay $200–500 every month for a
commercial robot receptionist service.

Those paid services often sound robotic, interrupt people, pause
awkwardly for one to three seconds before answering, keep your
callers' data on their computers, and are hard to change or move
away from. Changing a greeting or adding a new call rule can mean
filing a feature request.

This project offers a fourth choice: run your own receptionist with
a much more natural voice, and pay only for the minutes you use —
roughly $0.20–0.30 per minute of talking, with no extra monthly fee
to the project makers.

It also matters for privacy and control. Because you host it
yourself, call recordings and messages stay on your machines. And
because you get the full recipe (the source code), you can change
the greeting, hours, answers, and personality yourself.

## How does it work?
Think of it as three parts: ears and mouth, phone wires, and an
instruction card.

1. Ears and mouth: the voice brain. The system uses OpenAI's
Realtime service (a version called `gpt-realtime-2.1`). This is a
single smart voice model that hears speech and speaks back directly
in under a second, with natural pauses and turn-taking — much like
the voice mode in ChatGPT. You pick a voice and connect it with
your paid OpenAI key.

2. Phone wires: the delivery system. Real phone calls arrive over
the internet through standard phone-line companies such as Twilio
or Telnyx, using widely used calling technologies called SIP and
LiveKit. One running copy of the robot can serve several businesses
at once: each phone number is pointed to its own instruction card
through a routing rule.

3. Instruction card: a simple settings file. Each business gets a
plain text file that lists the business name, greeting, personality,
opening hours, what to say after hours, where to send each kind of
call, answers to common questions, and where messages should go.
No coding is needed — you just edit the file.

When a call comes in, the flow is roughly: the call arrives, the
right instruction card is loaded, a short recording notice is played
where the law requires it, the robot greets the caller and chats,
then acts. It can look up an answer, pass the call to a person,
save a message, and store a recording plus a written transcript.

Extra skills plug into the same flow. Messages can go to a file, an
email, or another app over the internet, with automatic retries. The
robot can notice the caller's language and switch to Spanish or
French if you allow it. It can check a Google Calendar, offer up to
three nearby open times, repeat the chosen time back for a spoken
"yes", and then book the visit. Old recordings and transcripts are
cleaned up automatically on a schedule, for example after 90 days.

## Where can this be used?
Any small or medium business that gets routine calls could use this:

- Doctor, dentist, or vet offices: answer opening-hour and price
questions, book visits, take messages after hours.
- Tradespeople (plumbers, electricians, repair shops): catch calls
while on a job, forward urgent calls, save the rest as messages.
- Offices and agencies: greet callers, route them to the right
person or department, handle nights and weekends with a message.
- Multi-shop owners: run one robot for several businesses, each
with its own phone number and settings file.
- Callers in other languages: serve English, Spanish, or French
automatically, and politely redirect anything else back to the
main language.

It fits best where calls are short and routine — a few minutes
each, a handful to a few dozen per day. Very busy front desks with
many calls a day pay more in per-minute voice charges, so the cost
needs a closer look at high volume.

## Conclusions & takeaways
The main message is simple: a natural-sounding phone receptionist
no longer has to mean an expensive monthly subscription with robotic
voices and locked-in data.

By combining a high-quality direct voice model with standard
internet phone lines and simple per-business settings files, a small
shop can run its own receptionist, keep its data, and pay only for
the minutes it uses — often about the same or less than commercial
services, with a much better experience for callers.

The trade-off is that you (or someone you hire) must set it up and
look after it: a computer to run it, a phone-line provider, an
OpenAI key, and the settings files. And you must use the current
connection method (a standard API key with the newer voice model),
because the older test connection stopped working in June 2026.

In short: if you are paying hundreds per month for a robot that
sounds like a robot, this project says — try running your own that
sounds like a person.

## Jargon decoder
| Term | What it means in plain language |
|---|---|
| Speech-to-speech | A voice system that hears and speaks directly, without separate write-down and read-aloud steps. |
| Cascaded STT-to-LLM-to-TTS pipeline | The older clunky way: write down speech, think up text, then read it aloud — slower and more robotic. |
| Realtime API | OpenAI's service that powers the natural, fast voice brain used here. |
| API key (`sk-...`) | A secret code that lets the robot use the paid voice service; you are billed by minutes used. |
| SIP trunk / SIP provider | The internet phone company (like Twilio or Telnyx) that carries real calls to the robot. |
| LiveKit | Helper software that moves live voice and call signals between the phone line and the robot. |
| YAML config | A simple readable settings file listing greeting, hours, FAQs, and routing for one business. |
| Call transfer | Passing a live caller to a human or department, like saying "one moment please". |
| Transcript / recording | A written copy and an audio copy of the call, saved so staff can review later. |
| AGPL-3.0 license | The sharing rule: free to use and change, but if you sell it as an online service you must share your changes too. |
