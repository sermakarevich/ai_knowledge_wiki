> PDF location: https://www.youtube.com/watch?v=pbQ1NwdQVLc (no source.pdf fetched; youtube source — see Source field below)
# Reducing Voice Agent Latency with Forced End-of-Utterance
Source: https://www.youtube.com/watch?v=pbQ1NwdQVLc
Kind: youtube
Fetched: 2026-09-22T07:43:06.061348+00:00
Tool: yt

If you're building a voice agent, you've probably run into this problem
before your user finishes speaking. And then nothing for a couple of seconds. That space can kill
the flow of conversation and make it feel weird for your end user. But how come this happens? And what can we do about it? This latency comes from deciding
when the speaker is finished. Traditionally, you're at the mercy
of a speech detect system. Silence buffer, forcing you to wait
until the user's finished talking. Silence buffer, forcing you to wait
until the user's finished talking. The system is detected a period of silence
and has finalized the transcript. Before you can even think
about getting a response from the LLM. Now, this behavior is fine
for notetaking and captions, but for conversational voice agents, you
need something faster and more decisive. So today I'll show you
how you can use Speechmatics force end of utterance feature to take control
and remove that awkward latency Here's a simple script that lets us use the force
end of utterance feature. As you can see, it's as simple
as calling force end of utterance Now, when you send off this message,
it tells the system. I'm done talking. Give me the finalized transcript. Now, you can hook up any one of your turn
detection models, like VAD or Push-to-talk to trigger this,
but to demonstrate today I 3D printed this big red button which will trigger
the force end of utterance messages. This visualization shows
partial transcripts still being processed at the top, with finalized transcripts
and forced end of utterance at the bottom. So when I press this button, the server will immediately
give us the final transcript. Let's see what it can do. Hi, there. Could you book me a table for two
tonight at 7 p.m., please? Let's try this. Remind me to check the oven in 15 minutes. As soon as I hit this button the force end of utterance
message gets sent, and you can see how quickly we get the final result back
in under 250 milliseconds. So that's pretty quick. This behavior is available
in the Speechmatics voice SDK as well as a real-time API
and real-time SDK. So whether you're integrating
at a high level or low level, you can control exactly
when you get your transcripts. This is also coming soon to voice agent
frameworks like Pipecat and LiveKit, so you can get faster, smarter results
without wiring everything yourself. So there you have it. If you're building voice agents
and want natural responsiveness and lightning fast transcription
under 250 milliseconds. Speechmatics force end of 
utterance has you covered. Follow us for more updates. Or check out the Speechmatics docs
to learn more. Thanks for watching.

