> [[index|Wiki]] | [[summary|Summary]]

# Honcho — In Plain Language

## What is this about?
Imagine you hire a brilliant personal assistant with a notebook. Every time you talk, meet someone, or send an email, they write down what happened. Later they connect the dots: you like morning meetings, you changed jobs, you always ask for short summaries. When you ask them something, they do not dump the whole notebook on your desk. They give you a short, useful answer based on what they learned.

That is what Honcho does for software. It is a memory layer that sits next to a chatbot or agent and remembers people over days, weeks, and months.

The opposite would be a filing cabinet. A filing cabinet stores papers but never reads them, never notices patterns, and never throws out old notes that are no longer true. Honcho tries to be the assistant, not the cabinet.

## Why does it matter?
Most chatbots forget. You tell them your name, your project, or your preferences, and next week they ask again. That feels broken and wastes time.

The common fix is to re-read everything every time. That means stuffing the whole chat history into each question. It is slow, it costs extra money, and after a while the history gets too long to fit anyway.

Honcho matters because it offers a middle path: keep learning in the background, tidy up what was learned, and then hand the chatbot only the small set of notes it needs for the current question.

Repeating yourself is more than annoying. In customer support it means longer tickets. In tutoring it means re-teaching what was already taught. In coding help it means re-explaining your setup every day.

Paying to re-read everything also adds up. Longer histories mean longer inputs, slower answers, and higher bills. A tidy set of conclusions is cheaper to use than the full raw history.

## How does it work?
Think of Honcho as the notebook-assistant working in shifts. Each shift has one clear job, from writing things down to answering from the notes.

Here is the daily routine, step by step:

1. Write down what happened. Every chat message, email, document, or note is saved in order inside a conversation thread. The save is fast, so the app does not wait.

2. Think about what it means right away. In the background, a small reasoning worker reads each new message and writes down simple conclusions: what was said directly, and what must follow from it.

3. Connect dots across days. What you learn in one conversation is attached to your profile, so it can help in a different conversation later. One person can take part in many threads, and one thread can include many people.

4. Tidy up notes during sleep. From time to time, when enough new notes have piled up and things have been quiet for a while, a consolidation worker reviews older conclusions. It fixes contradictions, removes outdated facts, and spots patterns like habits and preferences.

5. Answer the boss's questions from notes. When the app needs help, a question-answering worker searches the tidy notes, picks the relevant ones, and writes a short answer. Simple questions get a cheap, quick lookup. Hard questions can use deeper thinking for a higher price.

6. Keep viewpoints honest. By default Honcho builds its own view of each person from everything that person said. It can also build limited views, where one person only remembers what they actually saw in shared conversations, so game characters or teammates do not magically know everything.

Together this means fast writes, thoughtful background learning, and answers that come from tidy notes rather than raw history.

## Where can this be used?
Any app where people return over time and expect to be remembered will benefit. The same notebook pattern fits many jobs:

AI companions that remember your life, goals, and preferences across many chats instead of starting fresh each time.
For example, a companion recalls that you run in the mornings and prefer short answers.

Coding agents that remember your project setup, style rules, and past decisions without you repeating them.
For example, an agent recalls your test command and your naming rules.

Game characters that remember shared jokes, fights, and alliances with each player separately.
For example, one character treats you as an old friend and a stranger as a stranger.

Tutors that track what a student already knows, where they struggle, and how they learn best.
For example, a tutor skips mastered topics and practices weak ones.

Support bots that recall past tickets, what was already tried, and what worked.
For example, a bot does not ask for your order number twice.

Productivity helpers that remember meetings, action items, and habits, and brief you before the next meeting.
For example, a helper brings last week's decisions into today's agenda.

## Conclusions & takeaways
What to remember in a month: Honcho turns scattered messages into a living profile that improves over time, then answers from that profile instead of re-reading everything.

Three practical points follow from that. First, background thinking keeps chats fast while still learning. Second, periodic tidy-ups keep memory correct when facts change. Third, different price levels let you choose between a quick lookup and a deep research-style answer.

Think of it this way: cheap questions get a quick glance at the notebook, while hard questions pay for careful re-reading and synthesis.

Honest limits: asking hard questions costs extra, and the cheapest lookups are shallow. Vendor test scores look strong but need independent checking before you trust them for your case. And the system only learns from data you give it, so empty or messy input means empty or messy memory. Privacy and separation matter too, so keep customers, projects, or environments in separate areas.

If you set it up well, the reward is simple: less repeating, faster answers, and an assistant that feels like it knows you.

## Jargon decoder
| Term | What it means in plain language |
| ---- | ------------------------------- |
| Agent | A program that can take steps and answer on its own, like a junior helper |
| Memory layer | An extra storage-and-thinking service that remembers people for the main app |
| RAG (Retrieval-Augmented Generation) | Looking up old text and pasting it into the answer, without much thinking |
| Vector search | Finding notes by meaning, not by exact words |
| Token | A small chunk of text the computer reads; billing is often per chunk |
| Embedding | A list of numbers that captures the meaning of a piece of text |
| Reasoning model | A model trained to draw careful conclusions, not just write fluent text |
| Representation | The full learned profile of one person: facts, conclusions, and summaries |
| Benchmark | A standard test used to compare how well different systems perform |
| SDK (Software Development Kit) | A ready-made code library you install to talk to a service |
| API (Application Programming Interface) | A defined way for one program to ask another program to do something |
| Open source | Code that anyone can read, use, and improve under a public license |
