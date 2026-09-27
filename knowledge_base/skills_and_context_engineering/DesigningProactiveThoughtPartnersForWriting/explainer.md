> [[index|Wiki]] | [[summary|Summary]]

# Designing Proactive Thought Partners for Writing — In Plain Language

## What is this about?

Imagine you hire a couple of cooking assistants before a big dinner. You brief them in advance: "You watch the sauce, you watch the timing. Only tap me on the shoulder when I pause or taste something — and don't grab the spoon, just ask me a helpful question." Then you cook. They stay quiet, they watch, and now and then one taps you lightly: "That sauce looks thin — what could make it richer?" You can nod, chat about it, or say "you fix it" — or just keep cooking and let them fade into the background.

This work is about building that kind of helper for writing. Today you have two extremes. On one side are backseat drivers like autocomplete: they jump in all the time, but only with tiny help like finishing your word or sentence. On the other side are brilliant consultants like chatbots: they can brainstorm and give feedback, but only if you stop what you are doing, open a new window, and ask them a good question.

The missing middle is a thought partner: a helper you brief in advance about what kind of thinking help you want, that watches quietly while you write and taps you on the shoulder at moments you agreed on, with a question that makes you think — not an order.

## Why does it matter?

The everyday problem is simple: writing is stop-and-start thinking. One minute you need an idea, the next minute you need the right words, the next minute you need to check if your argument makes sense. Nobody can predict in advance which help you will need.

With today's tools, you either get interrupted with shallow help you did not ask for, or you have to interrupt yourself to ask for deep help. Stopping to write a clever prompt breaks your flow, and it is hardest exactly when you are stuck and "don't even know what question to ask." What changes here is the direction of help: instead of you always pulling help toward you, the help is pushed to you gently, at a moment you pre-approved, in a form that is easy to ignore.

In a one-week test with 16 everyday writers, people liked this push style when the timing fit. Satisfaction averaged about 8 out of 10 and even rose over the week as people learned to set up their helpers better.

Across 66 real writing sessions — personal, school, work, creative, and technical pieces — usability scored in the Excellent range and helpfulness averaged about 8 out of 10. People especially valued not having to leave their draft to ask for help. One person said the hardest part of chatbots is "I don't even know what question to ask" — here the helper brings the question to you.

Good timing turned out to be about fit, not the signal alone. A pause can mean "I am stuck, help me" or "I am concentrating, go away." So the same event is only treated as a maybe-moment, and the helper checks your rules and your current text before deciding to appear.

## How does it work?

1. **Brief your helpers before you start.** You create one or more partners and give each a name, a job, and rules for when to speak up. For example: "Evidence Partner — your job is to spot claims that need examples. Speak up when I pause or finish a sentence, but only if a claim really looks unsupported."

2. **They watch quietly while you write.** The helpers see your goal for the session, your current text, where your cursor is, and simple signals like pausing for 5 seconds, finishing a sentence, or selecting text. They do not act on every signal.

3. **A quick judge picks who taps your shoulder.** When one of those agreed moments happens, a fast check (a lightweight Artificial Intelligence, or AI, model) compares the moment against the rules you wrote. At most two partners are allowed to act, so you are never flooded. A small tag with the partner's name appears off to the side, next to where you are writing.

4. **Each tap is a short recap plus a question, not an order.** If you click the tag, you see something like: "You just moved from general ideas to famous athletes — what specific story, like a tough training routine, could prove your point here?" The question style is on purpose: it leaves the decision with you.

5. **You choose how far to go: ignore, chat, or let them draft.** Ignore: just keep typing and the tag fades away after about 15 seconds, no clicking needed. In the test, people ignored about 6 in 10 taps to protect their flow. Chat for inspiration: open the card and ask for alternatives or argue back, without changing your draft. Let them draft: press a button to have the partner insert or rewrite text, which you can then keep or undo. About 84 in 100 inserted texts were kept, mostly when people already knew what they wanted to say but struggled with wording.

Small design details keep this polite. Tags sit off to the side of the page, stay small, and fade away on their own. Each message starts with a short recap that shows the helper understood you, which builds trust — though people skipped the recap when they already knew what they wanted next. The one exception: when you miss something you did not know existed, a bare question is not enough and people wanted a direct answer with examples.

## Where can this be used?

Inside writing, the uses people actually invented were mostly about thinking, not fixing grammar. About 8 in 10 custom helpers were for deeper work: finding background facts, building an argument, questioning one-sided reasoning, or brainstorming ideas. Examples from the test included a Research Partner, an Ethical Partner, a Synthesis Partner, and a plain-language work partner. People used suggestions to get new ideas and to catch themselves drifting off track.

Outside writing, the same pattern fits anywhere people do long thinking work:

- **Coding:** a design-review helper that only speaks when you pause after a function, asking "what happens if this input is empty?" instead of rewriting your code.
- **Studying and research:** a counter-argument helper that taps you when you finish a paragraph of notes and asks what evidence would weaken your summary.
- **Emails and work documents:** a tone helper you brief with "warn me only when I sound too casual in a client draft," plus a clarity helper for long reports.
- **Agentic assistants (AI systems that can take steps on their own):** the same deal — you set the job and the moments in advance, the system offers a next step as a question, and you decide whether to ignore it, discuss it, or let it act.
- **Reading and editing someone else's draft:** a gap-spotter that only appears when you select a paragraph and pause, asking which side of the argument is missing.
- **Planning and journaling:** a reflection helper you brief with "ask me what I avoided today," set to appear only at the end of a session.

Setup itself turned out to be useful. People treated briefing their helpers as planning: they pictured the finished piece or named where they usually get stuck, then wrote rules to match. Over time the best setups were narrow experts rather than one general helper, and people refined them after seeing which tags they kept ignoring.

## Conclusions & takeaways

The big lesson is that good proactive help is not just about smart timing. It is about three things together: you get to shape the help in advance, you can easily ignore it or dig deeper in the moment, and it shows up in a light, polite form that does not take over your screen or your decisions.

Honest limits matter too. This was a small exploration with 16 experienced English-speaking writers who already used AI (Artificial Intelligence) tools, over just one week, with everyday writing — not secret or high-stakes work. It shows how people use such helpers and what they like, but it does not prove that writing gets better, faster, or more original. Timing is still imperfect: the same pause can mean "I am stuck" or "I am thinking hard, leave me alone." Watching everything you type also raises privacy questions — what is stored, for how long, and whether traces are reused — so future versions need clear pause, delete, and local-processing controls. And results come from one specific setup with one family of models, so quality may vary elsewhere.

Practical tips from the test: make ignoring free with no pop-ups to close, keep drafting as a deliberate second step rather than the default (especially for reflection nudges, where the question alone is often enough), and let people test and revise their helpers after real use — for example when a helper fires too often or almost never. Treat inferred states as guesses, never as facts about the writer.

If you remember one sentence: brief small helpers in advance, let them nudge you with questions at moments you chose, and keep ignoring them as easy as possible.

## Jargon decoder

| Term | What it really means |
| --- | --- |
| Proactive AI (proactive Artificial Intelligence) | Help that speaks up on its own when it thinks you need it, instead of waiting for you to ask. |
| Mixed-initiative | You and the system take turns leading — sometimes you act, sometimes it offers help, like a dance. |
| Technology probe | A simple working tool built to learn from real use, not a finished product to grade. |
| Event trigger | A simple agreed signal to check in, such as a 5-second pause, finishing a sentence, or selecting text. |
| Contextual heuristic | Your written rule for "only bother me when...", such as "only when a claim lacks an example." |
| LLM decision engine (LLM means Large Language Model) | A fast AI (Artificial Intelligence) reader that checks the moment against your rules and picks at most two helpers to show. |
| Graduated commitment | Three levels of saying yes: ignore it, use it as inspiration, or let it change your draft. |
| Rhetorical framing | How the message is phrased — here as a gentle question rather than a command — so you stay in charge. |
| Diary study | A test where people use the tool in daily life for days and write short notes after each session. |
| Prospective planning | Setting up helpers by picturing the finished work and where you usually get stuck, before you start. |
| Peripheral cue | A small signal off to the side that you can notice or ignore, like a sticky note at the edge of your desk. |
| Self-monitoring | Noticing your own drift — for example catching that you are off-topic or one-sided — with a little help. |

*Built only from the wiki pages, without reading the source paper.*
