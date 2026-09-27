> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The Non-Quantifiable Metrics

**In one sentence:** Codex was kept inside a secure PR-levelled pipeline with a 16.7% PR rejection rate, contributed lasting value mostly as a "copy paste machine" for rote server/database/JSX work while failing at novel backend logic and performant client analytics code, and remains worth reusing only with human ownership and an isolated pipeline.

## Key points

- All 30 Codex commits were levelled through PRs into the codebase, with 5 rejected — a 16.7% rejection rate.
- One rejected PR was a trivial Tailwind CSS version change handled manually instead; one was a wrong-instruction debugging PR with 400 additions and only 5 deletions, deleted as code-stuffing.
- One rejected PR was a code-merging problem from Codex working off an old branch, later absorbed via a different branch and instruction — "but a speedbump".
- The final two rejected PRs were "prime examples of agentic over-engineering": an overcomplicated client analytics timing stack and over-complicated trial-restriction evaluation with unwanted test code, both binned for comprehension, maintainability and design reasons (the trial one redone by the human in ~10 minutes).
- Lasting agent contributions were mostly mechanical — server route handling, database access, in-memory cache management, and JSX including basically all admin-panel code — because those are rote, conventional patterns memorisable from abundant examples.
- Novel backend work around data enrichment, event handling, and per-datum management still had to come from the human; root files (Dockerfile, Docker Compose, Ansible, Kubernetes manifests) were battle-tested human copies with nothing for AI to do.
- Client analytics code in `client/` needed to be performant, clear, modular, minimal and dependency-free, but Codex output failed "horribly" — partly blamed on low-quality JS training material and weak JS-side tooling (Go builds were checked, JS was "winging it") — while Codex one-shotting the client upgrade page CSS/classes untouched was "glorious".
- Verdict: yes to AI again in this manner with the isolated pipeline as a required part of the process, strongest as research/typing-automation and throwaway/supporting/isolated code, not yet viable for novel independent work; at $20/month "absolutely worth more than that".

---

## The non-quantifiable metrics

Codex was built into a secure pipeline from the beginning. All 30 commits were levelled through PRs; 5 of those PRs were rejected (16.7%).

| Rejected PR | Cause | Outcome |
|---|---|---|
| Tailwind CSS version change | Trivial change | Handled manually; "I should have just handled this myself and never bothered with the bot" |
| Debugging PR (400 additions, 5 deletions) | Wrong instruction (author's mistake) | Deleted as code-stuffing into the codebase |
| Code-merging problem | Codex working from an old branch | Replaced/absorbed via a different branch and instruction; "Twas but a speedbump" |
| Client analytics code | Agentic over-engineering | Binned; see verbatim below |
| Trial restrictions | Agentic over-engineering + unwanted test code | Closed; redone by human in ~10 minutes |

Verbatim on the client analytics rejection ("literally described as trash by the human"):

> "just utter trash"

> "It vomited variables everywhere and turned what had originally been a handful of human-written lines into an overcomplicated muddled stack of crap. It made simple things, such as measuring timing on the frontend, a totally unjustifiable mess."

> "This one really pissed me off if I'm honest as I wanted to take the easy way out and have the bot do it, but it failed miserably."

On the trial-restrictions PR: "It included test code that was not really wanted and a load of over-complicated evaluation for trial accounts versus full accounts. That was so far off track that I did it separately in like 10 minutes and closed the PR."

On both: "Both were prime examples of agentic over-engineering. It was better condensed into a simpler, cleaner, faster model by a human with experience. I'll be honest, I'm not sure if either of them actually worked. I took one look at the code and binned both for comprehension, maintainability and design reasons."

## The copy paste machine

Lasting agent contributions were mostly mechanical: server route handling, database access, and in-memory cache management, plus a lot of kept JSX including basically all of the admin panel code.

Author's explanation: server/database handling is rote and common — "so many server frameworks, ORMs, database calls, and frontend examples out there" — condensing into "relatively simple patterns with usually one conventional, 'good' way of doing it" that the model can memorise and "spat out on demand". Frontend JSX copy-paste from open-source component libraries was already the norm before LLMs ("Your website needs a button, some text, and a readable layout, that's a solved problem"); the LLM is "just a sped up, easily customised version of this".

Where it falls over is the novel stuff: "The backend code around data enrichment, event handling, and how each individual bit of data gets managed still needed to come from me if it was going to be done correctly and efficiently. There is nothing in the AI dataset, or sitting neatly out there on the web, that can hand that information back."

## Family furniture

Root project files — Dockerfile, Docker Compose, Ansible deployments, Kubernetes manifests — were copied from previous human projects, already battle-tested, with no AI generation needed: "This is the family AK-47 vs something you 3D printed. Grandad's Fender vs something in Guitar Center."

They also tie into other systems (e.g. database/database-user provisioning also provisions connection secrets to the cluster; the repo only mounts an already-existing secret), so "there is nothing there for AI to use and nothing for it to do. It's a solved issue already so no chance for the AI to shine or fail spectacularly compiling postgres from scratch."

## The front end code dichotomy

Heavy churn in client-side code, especially the `client/` analytics directory. The analytics code must be all of: performance, clarity, modular, minimal, without dependencies — "JavaScript garbage all over the internet is none of these things. It failed. Horribly."

Author's (self-described "honest jerk") diagnosis: JS has an "over-representation of lower-skill developers", giving the LLM "plenty of bad material to absorb" (cf. "npm security issues", "leftpad"); unlike Go/Rust/C, "JavaScript itself does not enforce the same level of correctness. So incorrect code leaks out into the world." Tooling gap: "Botto would check for build errors when running Go, but in the JavaScript side there was not much else it could do. It was winging it more, and the human had to pick up the pieces." Hence churn and human ownership of `client/` — "the JavaScript code that goes out to all users, so it needs to be performant."

Counterpoint: "when the frontend just needed to make something look pretty, fucking eh, Codex is way better than I am. One shotting the client upgrade page was a welcome surprise. I didn't touch any CSS or other classes, it was glorious."

## Would I use AI again?

"In this sort of project in this manner? Yes, absolutely."

- Codex "is great"; setup was fast and "uses the same models I use on the browser". Models are "currently great for small throwaway tools or supporting software as well as isolated stand alone pieces of code", including isolated standalone pieces and even the graphs/analysis framework code for this analysis (though "I did need to bash them into shape").
- "As a research and typing automation tool, it is fantastic. But coding has such a small margin for error that it still needs someone who knows what they are doing. And when you add in a reasonably high minimum standard, no it just didn't cut it most of the time."
- Controls were required: "I would not be running this again without my isolated pipeline and process" — code never near a production database, never able to touch the desktop or other data. "An AI agent with that kind of access could blow up a database and instantly undo all the benefit it added." "I have zero regrets about building that pipeline. It stopped the work from becoming a loss and turned it into a gain."

### Outside the Agent

AI helped more with "research, analysis, documentation, debugging, and typing than with final production-ready code". Best use: dictating/articulating thoughts, generating basics where the output shape is already known, research — "not an extension of myself or a replacement of anyone else, but it's own thing with it's own benefits". For novel independent work — "Do something novel, independent, and sensible" without knowing the expected output — "Nope, still a way off… not viable in my experience." Value: "For $20 a month, right now, it is absolutely worth more than that… removes a lot of the mental energy needed for tedious work… As typing automation it's better than using a framework - such as an ORM - that mainly exists to save me typing in the first place."

### Why this analysis?

"Mostly because I wanted to know" — after months deep in the work, no real sense of how much the bot did versus the human; as a solo engineer the LLM is "a reliable deckhand right next to me" plus a creativity/product-idea sounding board, but "who is actually putting the code in and making it reality? Turns out it was mostly me." Also to counter the "sheer, unending stream of people screeching into the void about their productivity" (e.g. "Microsoft and Spotify talking about how their code is now mostly AI-generated, and yet it has never been a bigger pile of crap"): "How much did I actually get done with AI from start to finish in a crunch with a known end result? That's this analysis."

**Covers:** 03-the-non-quantifiable-metrics — rejected Codex PRs, over-engineering cases, reflection and would-use-AI-again verdict
