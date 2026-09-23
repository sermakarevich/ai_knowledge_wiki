> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# alphaparkinc/genpark-voice-turn-taking-endpointing-detector-skill — In Plain Language

## What is this about?

This is a tiny traffic cop for voice conversations between humans and AI.

When you talk to a voice assistant, two hard questions come up constantly:
when did the person stop talking, and when is it okay to interrupt?

This skill answers both. It listens to a live stream of short audio slices,
decides whether each slice contains speech or silence, and then outputs
one of three simple verdicts: keep listening, cut off the agent because
the user jumped in, or hand the finished turn to the AI to reply.

The whole thing is one small Python file with no extra installs needed.
It runs on plain Python 3.9 or newer, using only the standard library.

It also ships with a short demo, a plugin manifest, and a wrapper so
other AI tools can call it over a standard protocol called MCP.

## Why does it matter?

Talking to a machine feels broken if the timing is wrong.

If the assistant jumps in too early, it cuts you off mid-sentence.
If it waits too long, every exchange has an awkward dead pause.
If it keeps talking while you are trying to correct it, you feel ignored.

This skill is the piece that fixes that timing. It is the difference
between a conversation that flows and one that feels like a walkie-talkie.

Because it reacts to very short slices of audio, interruptions feel fast
rather than laggy. Because it waits for a tunable cushion of silence,
it does not mistake a normal breath or pause for "I am done."

And because it has zero dependencies, it is easy to drop into voice
robots, phone systems, and agent swarms without dependency headaches.

## How does it work?

Think of it as a scorekeeper watching a conveyor belt of audio frames.

Each frame arrives with two numbers: how loud it is (energy in decibels)
and how long it lasts (for example, 20 or 100 milliseconds).

Step 1 — Is this speech or silence? The scorekeeper compares the loudness
against a threshold, by default minus 28 decibels. Louder than that counts
as speech; quieter counts as silence. No fancy neural network, just a
simple loudness check.

Step 2 — Has speech really started? One loud blip could be a cough or
noise. So the detector waits for 3 loud frames in a row before it trusts
that the user has actually started talking.

Step 3 — Did the user interrupt the agent? If the agent is currently
speaking and real user speech shows up, the detector raises the
barge-in flag. That verdict means: stop the agent's audio right now.

Step 4 — Is the turn finished? Once speech has started, every quiet frame
adds to a silence counter. When that counter reaches about 450 milliseconds
of silence (a setting you can change), the turn is marked complete.

Step 5 — Pick a verdict. Interruption wins first. Finished turn wins
second. Otherwise the answer is simply: continue listening.

Every frame also gets logged in a small audit trail, so you can see
exactly why each decision was made.

## Where can this be used?

Anywhere a human talks back and forth with a voice AI:

- Voice assistants and smart speakers that need to know when to reply.
- Customer-service phone bots where callers often interrupt with corrections.
- In-car or hands-free helpers where quick cut-ins matter for safety.
- Meeting transcription helpers that need to split speech into clean turns.
- Multi-agent voice swarms where many AI voices share one audio channel.
- Prototypes and classrooms, because students can run the demo in seconds
  with no installs and see a speech-then-silence example turn into
  a "dispatch reply" decision.

The MCP wrapper makes it especially handy as a plug-in tool: another
agent can send it a request and get back a structured verdict without
caring how the loudness math works inside.

## Conclusions & takeaways

This is plumbing, not magic — but good plumbing is what makes
conversation feel human.

The big idea is simple: confirm speech with a few frames, forgive short
pauses, and only declare the turn over after a real pocket of silence.
Handle interruptions as a separate fast path so the agent can shut up
immediately when the user speaks.

The trade-off it manages is universal in voice design: respond fast
without cutting people off. The three knobs — how much silence ends
a turn, how loud counts as speech, and how many frames confirm speech —
let each product tune that balance for quiet offices or noisy streets.

If you remember one thing, remember this: endpointing is just deciding
when silence means "your turn." This skill does that job in a few dozen
lines of dependency-free Python.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Voice activity detection (VAD) | Deciding whether a short audio slice contains human speech or just background quiet. |
| Endpointing | Deciding the user has finished their turn, so the AI is allowed to reply. |
| Barge-in | The user starts talking while the agent is still speaking, and the agent should stop and listen. |
| Audio frame | A tiny slice of sound, often 20 to 100 milliseconds long, examined one at a time. |
| Energy threshold (dB) | A loudness cutoff; sounds louder than this count as speech, quieter ones count as silence. |
| Silence duration | How much continuous quiet has piled up since the user last spoke. |
| Turn-taking | The back-and-forth rules for who speaks now, borrowed from human conversation. |
| LLM synthesis dispatch | Handing the finished user utterance to the language model so it can generate a spoken reply. |
| MCP (Model Context Protocol) | A standard plug-in format that lets AI tools call each other over simple messages. |
| Frame audit | A row-by-row log showing what the detector saw and decided for each audio slice. |
