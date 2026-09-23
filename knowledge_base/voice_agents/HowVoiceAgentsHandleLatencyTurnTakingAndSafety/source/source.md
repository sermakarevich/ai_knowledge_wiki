> PDF location: https://www.youtube.com/watch?v=gVCU2RoZheQ (no source.pdf fetched; youtube source — see Source field below)
# How Voice Agents Handle Latency, Turn-Taking, and Safety | Interview With Kræn Hansen
Source: https://www.youtube.com/watch?v=gVCU2RoZheQ
Kind: youtube
Fetched: 2026-09-22T07:42:24.371566+00:00
Tool: yt

 When we turn text into speech,   we also allow the text model, the LLM,   to express itself.   And it can laugh, or it can whisper,   or it can do more expressiveness.   Latency, that is like the
major pain point   of voice agents.   I would say latency is perceived, right?   You can have audio cues around.   You wanna make sure for the user   that the connection is not dropped.   Could you just describe to me like,   what is, for someone who has
just really understood   the term voice agents, what
is a voice agent?   So it's this experience of like
opening up a conversation,   using your voice to have a conversation   with a machine, basically.   On a slightly more technical level,   you take your speech, you
turn it into text,   using, for example, speech-to-text
and the ElevenLabs model,   and then you have a large language model,   text-based, that can reason,   or understand what's being said,   and it generates output text   that then gets turned into speech
again on the other side.   Something special about our
platform, for example,   is that when we turn text into speech,   we also allow the text model, the LLM,   to express itself, and it can laugh,
or it can whisper,   or it can do more expressiveness.   It doesn't sound as robotic,   and the voice model is very expressive   and very human-like in that sense.   It's pretty uncanny.   Sometimes when I get support tickets,   I have to ask the reporter, like,   who is the real person and
who is the agent,   because I can't tell them apart
when I'm just listening.   Do you think it passes that curve
of the uncanny valley?   It's basically when something
is so almost human   that it kind of looks a bit creepy?   There's still some latency artifacts,   depending on how expressive
you want to go,   or how much the, so in my understanding,   the LLM takes about 40 to
70% of the pipeline,   in terms of latency,   and that sometimes turns into speech   that sounds more hesitant than
you want, for example,   and it starts bearing meaning,   and in that sense, it basically
shows off.   And it's actually, in that sense,
it's sometimes better,   maybe, to have a little longer latency   so you know it's not pretending
to be human   in that sense, right?   But it's also about how you
prompt it, right?   We have security guidelines around   how you're supposed to structure
your prompt.   Around that, you have to declare,   like, if somebody asks, are you a robot?   Are you an agent, or are you human?   It should declare itself as
non-human, right?   I think as long as you're not using
a product like this,   and we also have safety guidelines   and safety ways of verifying that,   that you're not trying to
impose as a human,   I think that's fine.   One of the things you said
there was latency,   and I guess that is the major pain point   of voice models and voice agents,   is something that a lot of the companies,   like ChatGPT, have talked about,   it's a struggle to get that real
conversation going.   So could you do no, or could
you talk about   some of the technical challenges
of latency   and how you address them?   I would say latency is perceived, right?   So there's different levels of problems
that you can have.   And my understanding is you
wanna make sure   for the user that the connection
is not dropped,   for example.   You can do that with, for example,   if you're calling into a voice agent   and you have background noise,
like an office,   or you have like music playing
or whatever,   you can hear that, okay, the connection
hasn't dropped.   It's not like that is happening.   If the agent is doing some
task that takes time,   you can have audio cues around,   if it's doing a tool calling,
for example,   the agent can say, oh, I'm gonna
look you up in the system.   And then you can hear like
clicking noises from,   like a keyboard clicking, for example,   to just audiously like try to convey   that something is happening.   It's not as if it hasn't hurt you.   You don't have to repeat yourself,   but you get feedback on the way, right?   Agency can be on the numbers,
problematic,   but still you can have an entire platform   that takes care of turn taking   and like making sure that the
perceived latency   is not a problem in the conversation,
right?   It's also about you can speak
while I'm talking   without interrupting me,   but these agents are basically right now,   the way it works is there's a
turn taking algorithm,   like either you talk or I talk
as an agent, right?   There's ways that you can
do, for example,   with our speech-to-text,   well, it's gonna know the difference
between you saying,   yeah, yeah, okay, like affirming
what it's saying.   Sure. Yeah, sure, like sure.   Because that sometimes can cut
it off if you like.   Yeah, exactly, if it's too
stupid in that sense,   it will cut it off and you
will interrupt me.   We have ways of being more
intelligent about   what is actually the intent of
the user when they speak   so they don't interrupt and
cause a turn take.   There's a lot of things that you can do,   then underlying, like so you
have the text to speak,   the speech to text, the LLM
and the text to speech   at the end, you can tune parameters.   In general, the faster you make
it, the less expressive   or the less correct you make it, right?   We also have guardrails in
the product where   if you are doing banking services,   you might not wanna have the
LLM tell the user   like financial advice, for example.   And you can have like another
LLM standing on the side   and then cutting off the conversation   if it goes off the rails basically.   And you can do that in a streaming mode   where it just lets audio through
and then cuts   if it hears something it shouldn't.   Or you can have it in a blocking mode   where everything is verified before
it goes into the audio.   And depending on which of
the two you choose,   there's like an architectural
decision there   on how safe you want it.   One adds more latency than the other.   So all of these are tunable, right?   There's also stuff around maybe
when you call up   and you get the secretary that
needs to route you,   maybe that doesn't need to have
a high intelligence model.   Maybe it can be like a faster model.   And then we have ability to like delegate   into another sub agent that will
have more brain capacity,   so to speak, right?   So you can tune it and you can model it   to fit your use case basically.   It's like an agent call center
you have brain.   Yeah, yeah, definitely.   And you can choose if you wanna
have a different voice   when you transfer or you're gonna
keep the same voice   but now you're in like lone advice mode   and then you go to another node or...   Sure, because like maybe
it's like talking   to a secretary talking to like the person   who's gonna give you a loan.   You kind of want that breaking
rapport tonality   with the loan to have people like
respect the authority   of the agent you're talking to.   Sometimes you wanna make it obvious,   sometimes you just wanna change the model   and then now we're in a different setting   but it's the same person speaking   or same agent speaking.   So you can decide.   Could you tell us a bit about
the SDKs you're building   and like what are you involved
in specifically   as a React Native developer or someone
in the React space?   What is a cool thing I could
pick up from ElevenLabs   and integrate into my app?   I mean, we are very heavy
on code generation.   We have an open API spec for
the entire API surface   and we use that a lot to generate
the SDK surface   for the main server side SDK.   So in that sense, code generation
is a thing   that you can leverage or a
pattern you can copy.   Right now, I also talked about
that yesterday here   at the App.js.   We have a call JavaScript library
that is universal   and it's not a React library.   It's like platform and framework
agnostic.   And then we have a React package
on top of that   that implements React specific paradigms,   hooks and provider and stuff like that.   And then we expose that through
a React Native package   that also injects the audio
input capabilities   specific to React Native.   So this idea about like a layered SDK   where you progressively add on like
a common set of features   that you add on the framework
specific features   and then the platform specific framework   specific features at the end   and then have that entire cascading
SDK architecture, I guess,   is a pattern that I've seen also
in my previous work   at MongoDB and Realm.   We did the same thing where you
have a universal core   and then you build upon it to make
it more framework specific.   And you can have other UI frameworks   in that thing as well.   So you guys offer like UI out of the box   if you wanna like build like
almost like a chat box   type of thing, you know?   We do have both like a headless thing   where you bring your own UI   and then we have UI components as well,   a different package for showing
the agent or we also have   another package for like embedding
the chat bubble   that you can see in a product, right?   We get the chat and you can
have the conversation.   So what's the next steps?   What's next for you?   What's next for ElevenLabs?   Like what's the next hard
problem to solve?   There are so many ElevenLabs is, we
have 400 people, right?   And we have research internally.   So I'm constantly amazed
of all the things   that gets out of research.   They're really cranking out a lot
of interesting features   and new verticals, new products
that we're building.   So we do have the foundational,
we have the research,   we have the services and we're
also building a lot   of different vertical products
and top of that   targeting different markets,
different ways.   We make it more flexible.   One reason thing we did is something
called speech engine   which is where I talked about
ElevenLabs Agents platform   where you have it all integrated.   And we also have the services where
you can do your own   text to speech and speech to text   and then you bring your own
LLM in that scenario.   Or you have something now in between   where you only bring the brain   and the rest is handled by the platform.   So that is exceptionally good if
you have a chat interface   or you already have your chat,
a text-based chat   and you just wanna give it a voice.   The speech engine is really the
thing to use there.   I think in general, I wanna
start, try to be more,   that's for my work is like, I
wanna be more agentic.   We are already very agentic,   but I wanna see how far we can push that   in terms of keeping our many SDKs aligned   and feature parity.   So like try to automate more about,
for example, deriving.   We know about spec driven development   in agentic engineering where
you have a spec   and then you derive your implementation.   We have the implementation now
and it's sometimes   it's a little different from SDK to SDK.   So I wanna do the opposite.   I wanna generate the specification
from the implementation   and then I wanna compare
that specification   across the different SDKs and
basically converge   on an experience across all the
different languages   and platforms as my next goal.   Vibe alignment.   Yeah, vibe align.   It's hard to maintain so much code,   but it's also really worth it.   I think when you get to pick and
choose the technology   that's best for your use case, right?   Yeah, I was very impressed by
the music in ElevenLabs.   I know that was a recent release.   I've had play around with it,   some really great stuff being there.   Before that, like, Suno
was like the real,   really only service which did something   which was pretty decent, but ElevenLabs
Music is pretty.   It's fun.   And a lot of your products
are pretty up there   in quality, you know?   Thank you so much. 

