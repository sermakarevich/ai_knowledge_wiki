> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# FreedomIntelligence/LoopSpeech — In Plain Language
## What is this about?
LoopSpeech is the official repository for a research idea called
Self-Listening for full-duplex speech models.
A full-duplex voice assistant can listen and speak at the same time,
so you can interrupt it, just like a real conversation.
The problem it tackles has a vivid name: "What did I just say?"
Imagine the assistant is reading out a list — say, three restaurants —
and you cut in with "Wait, repeat the last one."
To answer well, it must know which item you actually heard,
not just which item it had already written down internally.
LoopSpeech gives the model a way to track its own realized speech:
the sound that truly reached your speaker.
Its headline result is a jump in anchoring accuracy —
answering consistently with the last item actually played —
from 7.8% (a matched model without this trick) to 73.0%.
Note the status: this is a preprint, and code, models, data,
and the public paper link are still to be added.
## Why does it matter?
Talking to a voice assistant feels broken when it confidently
repeats the wrong thing after you interrupt it.
That happens because of what the authors call the anchoring gap:
the gap between what the model believes it said
and what was really played to you.
Inside the machine, three steps run out of sync:
writing the words, turning words into audio, and playing the audio.
The model may have already "written" item three
while your speaker has only finished item one.
So when you ask "Where did you stop?" or "Continue from there,"
a model without playback grounding guesses from its internal draft
and gets it wrong.
This matters for every interruption-style request:
"What did you just say?", "Repeat the last item,"
"Where did you stop?", "Continue from there."
Fixing it makes hands-free, barge-in conversation trustworthy
instead of frustrating.
The comparison makes the point concrete:
a strong commercial baseline scored 43.8% on this test,
the matched model without Self-Listening scored only 7.8%,
and the Self-Listening model reached 73.0%.
## How does it work?
Think of it the way humans monitor themselves:
you hear your own voice as you speak, so you know how far you got.
Self-Listening gives the model an equivalent feedback loop.
It organizes each conversation as three streams
lined up on one shared clock that ticks every 40 milliseconds:
First, your speech — the audio coming in from you.
Second, the played model speech — only the model's audio
that has already reached your side of the playback.
Not the draft, not the queued audio: just what you could have heard.
Third, the model's text — its reply words plus special control tokens
that manage overlap, stopping on interruption,
continuing after a backchannel like "uh-huh,"
waiting, and staying silent.
The clever part: the already-played audio is fed back
through the model's normal speech-listening pathway.
That gives it a running, causal record of what you heard,
without slowing down word generation or audio playback.
Under the hood, the system builds on the Thinker part
of Qwen2.5-Omni-7B for understanding and deciding,
with a frozen MOSS-TTS-Realtime module that turns text
into streaming speech.
To check all this, the authors built AnchorSpeech:
a time-aligned collection for training and testing
exactly these interruption moments.
Its test asks a simple question: after an interruption,
is the model's answer consistent with the last finished item
that was actually played — rather than with text
that only existed inside the model?
Importantly, stopping speed and reply speed barely changed,
so the gain comes from better grounding, not from stalling.
## Where can this be used?
Anywhere a voice assistant should survive being interrupted:
phone-based customer support that reads out options, order updates,
or troubleshooting steps while the caller jumps in.
In-car assistants where the driver cuts in with "repeat that"
while directions or messages are still playing.
Language-learning or accessibility tools that read lists aloud
and must resume exactly where the listener lost track.
Smart speakers and wearables where barge-in ("stop, go back")
is the normal way people talk.
Meeting or lecture helpers that narrate summaries and must answer
"what did you just say?" without hallucinating the next bullet.
More broadly, any real-time voice agent built on a full-duplex model
could adopt the pattern: feed actually-played audio back in
as a third stream alongside user audio and model text.
The evaluation recipe travels too: test post-interruption replies
against what was played, not what was generated.
## Conclusions & takeaways
The core lesson is easy to remember:
what the model meant to say is not what you heard —
so ground it in playback, not in drafts.
Self-Listening closes that anchoring gap with a small
architectural idea: three time-aligned streams, one of which
is the model's own played voice coming back as input.
The payoff reported is large (+65.2 points over the matched model,
+29.2 points over the strongest commercial baseline tested)
at essentially no cost in stop or response latency.
There is a caveat: tests on Full-Duplex-Bench v1.5 show sub-second
responses in interruption and backchannel cases, but also a trade-off
between anchoring skill and conventional turn-taking skill —
being good at "where did I stop?" can cost a little elsewhere.
And the practical caveat: the repo is still a preprint shell,
so treat the numbers as paper claims until code, checkpoints,
data, and demos land.
If you remember one sentence: a talking machine that listens
to itself, the way people do, interrupts far more gracefully.
## Jargon decoder
| Term | What it means in plain language |
|---|---|
| Full-duplex | Listening and speaking at the same time, so either side can interrupt. |
| Self-Listening | Feeding the model's own already-played voice back in so it knows what you heard. |
| Anchoring gap | The mismatch between what the model thinks it said and what actually played. |
| Played model speech | Only the audio that already reached your speaker — the ground truth of what you heard. |
| Control tokens | Special markers in the text stream that say things like stop, wait, stay silent, or keep going. |
| Thinker branch (Qwen2.5-Omni-7B) | The base AI brain used here for understanding speech and deciding what to say. |
| MOSS-TTS-Realtime | The text-to-speech module that turns reply words into streaming audio; used frozen, unchanged. |
| AnchorSpeech | The training and test collection built for interruption moments and playback consistency. |
| Anchoring accuracy | How often the post-interruption reply matches the last item actually played. |
| Stop / response latency | How fast the model halts after you cut in, and how fast it starts its recovery reply. |
