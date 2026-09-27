> PDF location: https://www.linkedin.com/posts/arpitbhayani_if-you-are-letting-ai-agents-write-large-activity-7497869801172791296-s0mf (no source.pdf fetched; see Source field below)
# If you are letting AI agents write large chunks of your codebase, here is something I would recommend - decide your tradeoff per file / module. | Arpit Bhayani
Source: https://www.linkedin.com/posts/arpitbhayani_if-you-are-letting-ai-agents-write-large-activity-7497869801172791296-s0mf
Kind: article
Fetched: 2026-09-24T04:59:52.610770+00:00
Tool: urllib
Topic: coding_agents

If you are letting AI agents write large chunks of your codebase, here is something I would recommend - decide your tradeoff per file / module. | Arpit Bhayani

## LinkedIn respects your privacy

LinkedIn and 3rd parties use essential and non-essential cookies to provide, secure, analyze and improve our Services, and to show you relevant ads (including professional and job ads) on and off LinkedIn. Learn more in our Cookie Policy.

Select Accept to consent or Reject to decline non-essential cookies for this use. You can update your choices at any time in your settings.

                Accept

                Reject

              Agree & Join LinkedIn

      By clicking Continue to join or sign in, you agree to LinkedIn’s User Agreement, Privacy Policy, and Cookie Policy.

      Skip to main content

#  Codebase Tradeoff: Speed vs Understanding with AI-Generated Code

This title was summarized by AI from the post below.

              Arpit Bhayani
            Arpit Bhayani is an Influencer

      1mo

                      Report this post

If you are letting AI agents write large chunks of your codebase, here is something I would recommend - decide your tradeoff per file / module.

You cannot get both. Ship faster with AI-generated code, and deeply understand the codebase you are shipping. Trying to have both everywhere just means you get neither properly.

I recommend - sort modules within a codebase into two buckets before you hand anything to an agent.

Bucket one is code where being fast matters more than knowing every line. Think one-off scripts, internal tooling, throwaway prototypes. Let the agent own these fully. Do not waste your "attention" re-deriving understanding you will never need again.

Bucket two is code where a failure is expensive or hard to reverse. Think auth, payments, anything touching data integrity. For this bucket, treat the agent's output as a first draft. Read the diff line by line, trace how it touches the rest of the system, and make the agent explain its own reasoning before you merge.

If you pick one side for everything, you are smart enough to figure out what you would be losing out on. I would not repeat and restate the obvious :)

So spend the time you saved on shipping fast by reading deeply, but only where it counts. That is the whole tradeoff.

Hope this helps.

                    1,258

                41 Comments

      Like

      Comment

              Share

Copy

LinkedIn

Facebook

X

                    Kareem Hesham

      3w

                      Report this comment

This distinction between internal tooling and core logic is a practical way to manage cognitive load. It’s easy to fall into the trap of trying to audit every line of a script, but that often leads to diminishing returns compared to focusing deeply on critical paths like auth or data integrity.

      Like

      Reply

                1 Reaction

                    Arjun Joshi

      4w

                      Report this comment

Will certainly add a few more factors when categorizing modules into buckets, but 100% agree with the core ask
Don’t apply the same level of human attention to every line of AI-generated code. Decide deliberately where human understanding is an engineering requirement and where it isn’t.

      Like

      Reply

                1 Reaction

                    Trilochanprasad B Hilli

      4w

                      Report this comment

While reading core code remains essential, we can scale safely by building agent friendly repos. Enforcing pre and post run documentation alongside automated testing establishes the hard guardrails needed to ship reliable AI generated code.

      Like

      Reply

                  2 Reactions

                3 Reactions

                See more comments

        To view or add a comment, sign in

##  More Relevant Posts

              Anurag Upadhyay

      3w

                      Report this post

If you’re getting bored while Claude is doing its thing, go read some important code or think through the plan. It’s way better than sitting around and having to fix expensive mistakes later.

TBH, I feel like Claude is making all of us a little weaker as engineers. If we stop thinking deeply and just let AI do everything, I’m worried it could have some pretty disastrous consequences down the road. ⚠️ :')

              Arpit Bhayani
            Arpit Bhayani is an Influencer

      1mo

If you are letting AI agents write large chunks of your codebase, here is something I would recommend - decide your tradeoff per file / module.

You cannot get both. Ship faster with AI-generated code, and deeply understand the codebase you are shipping. Trying to have both everywhere just means you get neither properly.

I recommend - sort modules within a codebase into two buckets before you hand anything to an agent.

Bucket one is code where being fast matters more than knowing every line. Think one-off scripts, internal tooling, throwaway prototypes. Let the agent own these fully. Do not waste your "attention" re-deriving understanding you will never need again.

Bucket two is code where a failure is expensive or hard to reverse. Think auth, payments, anything touching data integrity. For this bucket, treat the agent's output as a first draft. Read the diff line by line, trace how it touches the rest of the system, and make the agent explain its own reasoning before you merge.

If you pick one side for everything, you are smart enough to figure out what you would be losing out on. I would not repeat and restate the obvious :)

So spend the time you saved on shipping fast by reading deeply, but only where it counts. That is the whole tradeoff.

Hope this helps.

                    3

      Like

      Comment

              Share

Copy

LinkedIn

Facebook

X

        To view or add a comment, sign in

              Anshul Sahni

      4w

                      Report this post

The best approach for building applications, overtime the size of Bucket 1, can reduce since as it becomes more mature and you are able to write good instructions for agents

              Arpit Bhayani
            Arpit Bhayani is an Influencer

      1mo

If you are letting AI agents write large chunks of your codebase, here is something I would recommend - decide your tradeoff per file / module.

You cannot get both. Ship faster with AI-generated code, and deeply understand the codebase you are shipping. Trying to have both everywhere just means you get neither properly.

I recommend - sort modules within a codebase into two buckets before you hand anything to an agent.

Bucket one is code where being fast matters more than knowing every line. Think one-off scripts, internal tooling, throwaway prototypes. Let the agent own these fully. Do not waste your "attention" re-deriving understanding you will never need again.

Bucket two is code where a failure is expensive or hard to reverse. Think auth, payments, anything touching data integrity. For this bucket, treat the agent's output as a first draft. Read the diff line by line, trace how it touches the rest of the system, and make the agent explain its own reasoning before you merge.

If you pick one side for everything, you are smart enough to figure out what you would be losing out on. I would not repeat and restate the obvious :)

So spend the time you saved on shipping fast by reading deeply, but only where it counts. That is the whole tradeoff.

Hope this helps.

      Like

      Comment

              Share

Copy

LinkedIn

Facebook

X

        To view or add a comment, sign in

              Saba M.

      1mo

                      Report this post

One config line stands between my AI feature and a bill I could not pay.

AI_DAILY_TOKEN_CAP = 2,000,000.

That is the total every user of my product can burn in a day, combined. There is a second cap, 25,000 per request. Both are hard stops. When they hit, Otto stops answering and I get an angry email instead of an invoice with a number I cannot cover.

I did not build those on day one. I built them the night I understood what an unbounded loop plus a metered API plus a stranger on the internet actually adds up to.

The thing nobody warns you about when you ship software without a coding background is that AI does not fail like a bug fails. A bug breaks and you notice. A runaway AI call succeeds, repeatedly, correctly, expensively, all night, and the first sign is the billing page.

Three things I would tell anyone shipping an AI feature alone.

1. Put the global cap in before the feature works, not after. If you wait until it works you will ship it, because it works.

2. Cap per request as well as per day. The day cap protects your company. The request cap protects you from one user with a loop.

3. Keep the model behind one variable you can change. Not because you picked wrong, but because the price moves and the quality moves, and you do not want to be rewriting anything at 2am to escape either one.

None of this is clever. All of it is the difference between a bad week and a closed company.

What is the cheapest safeguard you have ever been glad you built?

                    1

      Like

      Comment

              Share

Copy

LinkedIn

Facebook

X

        To view or add a comment, sign in

              Isaac Sundar

      3w

                      Report this post

𝗧𝗵𝗲 𝗯𝗲𝘀𝘁 𝗼𝘂𝘁𝗽𝘂𝘁 𝗼𝘂𝗿 𝗔𝗜 𝗮𝗴𝗲𝗻𝘁 𝗽𝗿𝗼𝗱𝘂𝗰𝗲𝘀 𝗶𝘀𝗻'𝘁 𝗮𝗻 𝗮𝗻𝘀𝘄𝗲𝗿. 𝗜𝘁'𝘀 𝘁𝗵𝗲 𝗮𝗻𝘀𝘄𝗲𝗿 𝗶𝘁 𝗰𝗼𝘂𝗹𝗱𝗻'𝘁 𝗳𝗶𝗻𝗱.

Two years ago, I set out to solve this for developers building on Amazon's Selling Partner API. Leading the architecture and development of an agentic chatbot for answering complex API integration queries, grounded entirely in our documentation, built on one rule: never guess.

Here's the part our team is most proud of: when it can't find a confident answer, it doesn't make one up. It flags the gap.

Normally, gaps surface the slow way. A developer gets stuck, files a ticket, it gets escalated, and weeks pass before anyone notices. By then, others have likely hit the same wall and just worked around it. Our agent lets us catch these gaps the moment they happen, in real time, at a scale manual review never could.

We built a pipeline that groups similar gaps together into a clear, prioritized list, and our team closes them before they ever become a ticket.

The result is a flywheel: every "I don't know" makes the next answer better, for everyone who asks after.

This is what I think AI agents built on custom knowledge bases should do: actively find the gaps in your own knowledge, and close the loop before it becomes someone else's problem.

View C2PA information

                    5

                1 Comment

      Like

      Comment

              Share

Copy

LinkedIn

Facebook

X

        To view or add a comment, sign in

              Raghunath Boreddy

      2w

                      Report this post

Why Transaction Management Quietly Decides Whether Your Spring AI App Is Production-Ready

We talk a lot about prompts, embeddings, and RAG pipelines in Spring AI. We talk far less about what happens when an LLM call succeeds but the database write after it fails — or vice versa.

That's where Spring's transaction management becomes the unsung hero of reliable AI applications.

Here's why it matters more than most teams realize:

AI workflows aren't single operations — they're chains.
A typical Spring AI flow might: call an LLM → parse the response → update a vector store → write results to a relational DB → trigger a downstream event. If any step fails midway, you need the whole chain to fail cleanly, not leave orphaned or inconsistent data.

@Transactional isn't just for CRUD apps anymore.
When you're persisting conversation history, tool-call results, or embeddings alongside business data, partial commits can silently corrupt your AI system's "memory" — and debugging that days later is painful.

Retries need transactional boundaries:
LLM calls are inherently flaky — timeouts, rate limits, model errors. Wrapping the surrounding data operations in well-scoped transactions (with correct propagation and isolation levels) means a retry doesn't duplicate writes or leave dangling state.

Non-transactional AI calls + transactional persistence = design decision.
LLM/API calls shouldn't sit inside a DB transaction (you don't want to hold locks during a slow network call). Spring AI apps need thoughtful separation: do the AI call, then transactionally persist the outcome — often via the Saga or Outbox pattern for true consistency across services.

Skipping this = subtle, expensive bugs.
Stale embeddings, duplicated chat messages, half-updated audit trails — none of these throw obvious errors. They just make your AI system quietly untrustworthy.

The takeaway: Spring AI gives you the building blocks for intelligent applications, but Spring's mature transaction management is what makes those applications dependable at scale.

Are you handling transactional boundaries around your AI calls today, or is this an area your team is still figuring out?

#SpringBoot#SpringAI#SoftwareArchitecture#TransactionManagement#BackendEngineering#AIEngineering

                    1

      Like

      Comment

              Share

Copy

LinkedIn

Facebook

X

        To view or add a comment, sign in

              John Aspinall ✱

      1w

                      Report this post

I asked DeepSeek V4.1 Flash to write code.

It refused.

Told me my architecture was flawed.
⤷ Then it fixed it.

Not kidding here.

On September 10, DeepSeek dropped V4.1 Flash. A smaller model. Beats their flagship V4 Pro so decisively they're killing it .

I spent 72 hours testing.
Three moments stopped me cold.

1. I asked for a data script. It gave me code + a warning:
"Your field names are ambiguous. Three interpretations below. Confirm first."

2. I gave it a prompt with a logical trap.
It didn't fall for it. Called out the flaw directly.

3. It refused a task.
Reason: "This will leak data. I don't recommend it."

Old AI: "You say it, I do it."
New AI: "I understand. I judge. I refuse."

552B parameters.
8B active reading.
16B generating.

Native vision. Built in. Not bolted on.

So ask yourself:

Do you want your AI obedient or intelligent?

If it refuses your instruction, is that "broken" or "trustworthy"?

                    15

                7 Comments

      Like

      Comment

              Share

Copy

LinkedIn

Facebook

X

        To view or add a comment, sign in

              Augment

                12,498 followers

      2w

                      Report this post

You ask the assistant for a small feature. Ninety seconds later you have four hundred lines that look completely reasonable, and you have no idea whether any of it is true.

If the project has tests, you find out in two minutes. If it doesn't, you find out in a store review three weeks later, written in caps.

That's really the whole AI story so far. The tool doesn't improve your codebase, it just runs at whatever quality the codebase already had. Typed, tested and consistent? Every feature gets noticeably cheaper. No tests, no docs, three different opinions about how to name a file? Congratulations, you can now produce technical debt at machine speed.

So the useful question isn't which assistant to buy. It's what in your project would push back if the code were wrong.

CI that blocks the merge pushes back. A test on your sync logic pushes back, and sync is worth testing precisely because it fails politely. No crash, no alert. Just a user whose data quietly isn't there.

A written API contract pushes back too. The model can't guess an endpoint that lives only in someone's head. Neither can the developer who joins in March.

A linter pushes back without getting tired, and without anyone taking it personally. Which is more than you can say for review comments.
And a one-page note on why you chose the thing objects six months later, when everyone has forgotten and the answer would otherwise be "no idea, git blame says it was you".

Once those exist, the AI part is almost boring. Generated code goes through the same tests and the same review as anything typed by hand. AI review sits on top of human review. Translations and release notes come out of the model as drafts and get approved by a person.

Boring is the point. The interesting part was always going to be the guardrails.

                    8

                1 Comment

      Like

      Comment

              Share

Copy

LinkedIn

Facebook

X

        To view or add a comment, sign in

              Thiago Marinho

      5d

                      Report this post

What is Jev? Structured AI decisions for software

Jev is TypeSafe's System One model for structured software decisions. Learn its typed primitives through a safe customer refund triage example in production.

https://lnkd.in/dB347-PH

                    1

      Like

      Comment

              Share

Copy

LinkedIn

Facebook

X

        To view or add a comment, sign in

              Matthew Turley

      2w

                      Report this post

How much does it cost to run an AI coding agent?

After routing my whole pipeline through a local proxy for about six months, roughly 1,500 tasks, I finally priced it. About $27 per shipped task at API rates.

That surprised me, because a task that ships on the first try prices out around $5.50. The gap is not the work that succeeds. It is the work that fails and keeps retrying.

Priced at API rates, about $3,200 of one month went to tasks that retried themselves into the ground and got canceled anyway. One task retried more than a hundred times before I killed it, roughly $940, and it produced nothing.

Here is what I did about it. I stopped budgeting per day and started pricing per run. Every run gets an expected cost, and the actual is checked against it. A run coming in around 1.2x expected is usually just a cold cache. A run at 3x or more is almost always a retry loop on a failure that was never going to resolve, so it gets capped and killed instead of bleeding out. That one change turned the invisible retry tail into something I catch the same hour it starts, not at the end of the month.

I run on a flat-rate plan, so I never actually paid the $3,200, and I never saw a bill. These are what the runs would cost at provider list prices. That is exactly why it stayed invisible so long. Flat rate hides the waste until you price each run.

The proxy that does this has run my pipeline for six months. It is free and local at relayplane.com. If you run agents, where do you draw the line to auto-kill a run, 3x, 5x? I am still tuning mine.

                    1

                3 Comments

      Like

      Comment

              Share

Copy

LinkedIn

Facebook

X

        To view or add a comment, sign in

              John Young

      1w

                      Report this post

The fix for a bad AI coding agent day is not a second subscription. It is a repo where swapping the agent underneath is a config flip, not a migration.

Plan for two triggers, not one. The obvious one is the red status page: Anthropic logged "Elevated errors for multiple models" on 2026-09-03, four surfaces down together. The one that actually costs you a sprint is quieter. The model keeps answering, the answers get worse, and nobody declares anything. A routing bug ran for a month before the postmortem opened, because internal evals kept scoring isolated recoveries as fine and missed the pattern.

The blast radius of a vendor incident is the vendor, not the model. Research across public status pages found any two Anthropic services fail together on the same day more than 80% of the time. Cross-provider, no such correlation shows up. A second vendor doesn't buy you uptime. It buys you an uncorrelated failure schedule.

Most of your harness will not survive the swap. Hooks, permissions, subagents, MCP client config: four vendors, four schemas, no shared field. The one piece that does port cleanly, the instruction file, is also the layer doing the least work. Research found context files don't generally improve task success while raising inference cost over 20%.

Port the cheap layer because it's cheap. Rebuild the expensive layer before the incident, not during it. Put your real guarantees, tests passing, secrets blocked, outside any vendor's reach entirely, where no config flag can turn them off.

Question: What's actually locked to one vendor in your setup right now, and would you find out during an outage or before one?

                    1

                1 Comment

      Like

      Comment

              Share

Copy

LinkedIn

Facebook

X

        To view or add a comment, sign in

            293,971 followers

                    3000+ Posts

                    179 Articles

            View Profile
          Connect

##  More from this author

###  How Much Are People Willing to Bet on You?

            Arpit Bhayani

      9mo

###  How to Get Leadership to Say Yes to Your Project

            Arpit Bhayani

      10mo

###  Don’t Let Your Best Ideas Die in Silence

            Arpit Bhayani

      10mo

##  Explore related topics

How to Use AI Agents to Optimize Code

How to Stay Proficient in Complex Codebases

Tips for AI-Assisted Programming

How to Boost Productivity With Developer Agents

How to Overcome AI-Driven Coding Challenges

How AI Agents Are Changing Software Development

Tips for Balancing Speed and Quality in AI Coding

How to Maintain Code Quality in AI Development

How to Use AI Instead of Traditional Coding Skills

Using Asynchronous AI Agents in Software Development

                Show more

                Show less

##  Explore content categories

Career

Productivity

Finance

Soft Skills & Emotional Intelligence

Project Management

Education

Technology

Leadership

Ecommerce

User Experience

                Show more

                Show less

##  Sign in to view more content

Create your free account or sign in to continue your search

          Email or phone

          Password

Show

Forgot password?
          Sign in

Sign in with Email

                      or

                    New to LinkedIn? Join now

      By clicking Continue to join or sign in, you agree to LinkedIn’s User Agreement, Privacy Policy, and Cookie Policy.
