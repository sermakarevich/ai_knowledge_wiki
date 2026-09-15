> [[index|Wiki]] | [[summary|Summary]]

# The Bitter Lesson of Tool Calling — In Plain Language

## What is this about?

When an AI chatbot needs to "do" something outside of talking — look up a weather forecast, check a database, do math — it uses what's called a "tool call." Today, the standard way this works is like filling out a rigid form: the AI picks a form (a "function"), fills in each blank one at a time, and sends it off. This is called **JSON tool calling**, and it's how almost every AI assistant you've used works under the hood.

This paper asks a simple question: what if, instead of filling out a form, the AI just wrote a short computer program (a Python script) that does the same thing? Modern AI models are already good at writing code — so instead of "fill in form A, then fill in form B," the model could write "do A, then do B" as three lines of code. The researchers call this **programmatic tool calling**, or PTC for short.

They tested this idea rigorously: 14 different AI models (from Anthropic and OpenAI), a standard exam for tool use (called BFCL v4), and three extra stress tests designed to find where each approach breaks.

## Why does it matter?

Every AI agent — coding assistants, research assistants, customer-service bots — lives or dies by how well it can call external tools. If one interface is structurally better, it affects the reliability, speed, and cost of essentially every AI agent built going forward, not just one product. It also reframes a debate: is the "form-filling" interface a fundamental requirement, or is it just a crutch that early, less-capable models needed — one that stronger, more code-fluent models have outgrown?

## How does it work?

Think of it like ordering at a restaurant two different ways:

1. **JSON tool calling (the form-filling way).** For every dish you want, the waiter hands you a printed order slip. You fill in "dish name: pasta, size: large" and hand it back. If you want three dishes, you fill out three slips, one at a time, waiting for each to be confirmed before starting the next.
2. **Programmatic tool calling (the note-writing way).** Instead, you write one note: "bring me pasta (large), a salad, and a water — bring the water first since I'm thirsty." The kitchen reads the whole note at once and handles everything in one go.

For a single dish, both ways work fine. But the note-writing approach gets dramatically better as your order gets complicated — many dishes at once (parallel fan-out), or dishes that depend on each other ("after the soup arrives, bring the same broth for the risotto" — sequential chaining). The form-filling way needs a new trip back to the kitchen for every dependent step, and past a certain number of dishes, the waiter starts literally dropping items from the order. The note-writing way just... writes a longer note.

That's essentially what the paper measures. In programmatic tool calling, the model writes one Python script that calls all the tools it needs — even if that means looping through 100 items or passing one tool's output into the next — and it all executes in a single step. In JSON tool calling, each call is a separate round-trip, and the researchers found real AI models literally start dropping tool calls once they need to make around 70-100 of them at once.

The catch: writing code correctly is a *harder* skill than filling out a form. Three of the older or smaller AI models tested kept making one specific mistake — writing the escape sequence `\n` (which is text meant to represent a newline) instead of an actual newline character, which breaks their scripts. That single, oddly specific bug accounts for nearly all of programmatic tool calling's losses in this study, and it disappears in newer models.

## Where can this be used?

- **Coding assistants and dev-tool agents** (e.g., an AI that edits files, runs commands, greps a codebase): these already lean on code-capable models, so programmatic tool calling is a natural fit and likely already partially in use in tools like Claude Code.
- **Agents doing bulk/repetitive lookups** (checking 50 records, cross-referencing many API calls): this is exactly the "parallel fan-out" scenario where the paper shows the largest gains.
- **Multi-step workflows** (book a flight, then a hotel using the flight's arrival time, then a rental car using the hotel's location): the "chaining" scenario, where programmatic tool calling avoids extra round-trips.
- **Any agent-building framework choosing a tool-interface standard** for a new product: this paper is direct, practical evidence for that architecture decision, not just an academic curiosity.

## Conclusions & takeaways

- For current-generation, code-capable models, letting the model write code to call tools is at least as good as — and often meaningfully better than — the standard JSON tool-calling form, especially as tasks get more complex.
- The main way it fails is a narrow, specific formatting bug in older models, not a fundamental flaw in the approach.
- The gains are not free: writing code costs more input tokens under moderate loads (fewer tool calls), a trade-off that reverses once tasks get large enough (many tool calls at once).
- The improvement doesn't come from "PTC understands tools better" — it comes from removing structural bottlenecks (extra round-trips, per-response call limits) that the JSON interface imposes but code execution doesn't have.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Tool calling | An AI model asking to run an external action (look something up, do math, send an email) instead of just answering in text |
| JSON tool calling | The standard way this works today: the model fills in a structured, form-like object for each action |
| Programmatic tool calling / codemode | The alternative tested here: the model writes a small program that performs the actions, instead of filling out forms |
| BFCL v4 | "Berkeley Function-Calling Leaderboard v4" — a standardized exam used to grade how well AI models call tools correctly |
| Fan-out | Doing many independent things at once (e.g., looking up 50 records in parallel) |
| Chaining | Doing things in sequence where each step needs the previous step's result |
| Context rot / flooding | Cramming an AI's working memory with lots of extra, mostly irrelevant information (like giving someone 128 tool manuals when they only need 2) and seeing how much its performance degrades |
| Echo-return stub | A fake version of a tool used for testing that just repeats back what it was given, instead of doing the real action — used here so the benchmark is safe and repeatable |
| Enumeration accuracy | Whether the model actually made every required tool call, as opposed to just guessing the right final answer without doing the work |
| Wilson confidence interval | A statistical range showing how much a reported percentage could be off due to a small sample size |
| Model generation | How recently a model was trained/released — the paper's key finding is that this predicts success better than which company made the model |
