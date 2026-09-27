# 4 Weeks of Vibecoding: What I Built, What I Learned, and… | Pokharna Talks
PDF: https://pokharnatalks.com/blog/4-weeks-of-vibecoding-what-i-built-what-i-learned-and-whats-next (no local source.pdf; use Source URL)
Source: https://pokharnatalks.com/blog/4-weeks-of-vibecoding-what-i-built-what-i-learned-and-whats-next
Kind: article
Fetched: 2026-09-25T05:46:18.325792+00:00
Tool: urllib
Topic: coding_agents

4 Weeks of Vibecoding: What I Built, What I Learned, and… | Pokharna Talks

Skip to main content

I didn’t know how to set up a GitHub repo four weeks ago.

I am not exaggerating. On February 12, 2026, a client and a dear friend forced me to take a Claude Code plan, and my wife set it up for me because I genuinely did not know how. I had never used a terminal to push codes. I had never written a commit message. I had spent a decade building coliving companies, advising 70+ operators across 14 countries, and running a 36,000-subscriber newsletter, but I had never shipped a single line of code in my life.

Today is March 12. Exactly one month later. I have 197 commits across multiple live projects. And I have shipped more product in these four weeks than most funded startups ship in a quarter.

## Vibecoding Is Not Coding. It Is the Wrong Word.

I was intimidated by the term for months. “Vibecoding” sounds like something developers do when they are in a flow state. It sounds technical. It sounds like you need to understand syntax, languages, and frameworks.

You don’t.

Vibecoding, at least the way I do it, is this: if you have a vision, if you know what you need to build, if you understand the problem deeply enough, you can just get it done. You do not write code. You write the details of how you want things to be done and what exactly you want them to do. The AI coding tools just execute.

I do not know JavaScript. I do not know TypeScript. I do not know what Prisma is or why Next.js has an “App Router.” But I know what a coliving operator needs from a marketplace. I know what SEO architecture looks like for a B2B platform. I know the exact fields a property listing needs, the permissions an admin panel requires, and the user journey from discovery to booking.

Image

## What I Actually Built in 4 Weeks

Let me be specific. I am not talking about toy projects or landing pages. Here is what went live:

BookMyColiving.com: A full two-sided coliving marketplace with three distinct user roles (tenant, operator, and admin), each with their own portal. The platform has property listings with moderation workflows, a messaging system, reviews, lead management, CSV exports, and over 2,500 SEO-optimized pages across city pages, keyword pages, community-type pages, and locality pages. Three stakeholders interacting with each other through a single platform. Built on Next.js, TypeScript, Prisma, and PostgreSQL, and deployed on Vercel.

EverythingColiving.com platform rebuild: The entire everythingcoliving.com website was rebuilt. Not a redesign. A rethink. We went from 170+ pages to a planned 300+ pages, added 15 interactive tools for coliving operators (ROI calculator, readiness index, pricing optimizer, vacancy cost calculator, house rules generator, and more), and launched a vendor directory, an operator directory, a coliving markets section, and a free templates library. All built through AI-assisted development.

JumboTiger inthe making: A complete PRD for the JumboTiger custom property management software website, written specifically as a Claude Code execution document. Sections covering site architecture, module deep dives, design system, technical specs, and content strategy. Written so precisely that a developer or an AI can pick it up and build it without asking a single clarifying question.

PokharnaTalks.com: My personal blog and portfolio website, rebuilt from the ground up. This was actually one of the first things I built to get comfortable with the tools. The site has a full blog engine and an About page that doubles as an interactive portfolio filterable by region and company type showcasing every coliving operator, proptech brand, and real estate company I have worked with over the last decade. The About page alone has more depth than most startup pitch decks, and it was important to me because this portion is where I practice what I preach. If I am advising coliving operators to document their story and build their personal brand, my house better be in order. This blog post you are reading right now lives on that site.

## The Process: Speaking Products Into Existence

Here is the part that will sound strange to anyone who has managed software projects before.

I recorded most of my product requirements by speaking into my voice memo app.

I would think through what I wanted while walking, driving, or between calls. I would speak it out: the user flow, the data model, the edge cases, and the things I hated about existing solutions. Then I would use AI to transcribe the recording, structure it into a specification, and feed that specification to Claude Code for execution.

Writing PRDs is one of the most significant tasks for product managers. I can now speak in PRD. I can articulate what I want verbally, convert it into structured requirements using AI, and have those requirements executed, sometimes within the same day.

The deliverable has changed. It used to be a Jira ticket that sat in a backlog for weeks. Now it is a detailed prompt that becomes a live feature within hours.

## The Hard Part Is Not Building. The Hard Part Is Quality.

This is where I need to be honest, because the narrative around vibecoding is dangerously incomplete.

Building the first version of BookMyColiving was fast. Getting it to production quality was not.

After the initial build, I ran QA across the admin panel, operator portal, and public web app. I found 21 bugs. Buttons that did not disable after submission. Fields with no validation. Share links pointing to localhost instead of the production URL. Deactivated content is still showing on the frontend. Low-contrast text that was unreadable. Draft prices reset to zero on save.

These are not exotic bugs. These are the boring, unglamorous bugs that make or break a product. And AI did not catch them on its own. I had to test, find them, document them precisely, and then write prompts for Claude Code to fix each one.

Then I did something that I would recommend every vibecoder do: I hired an independent development team to conduct a technical review of the codebase.

Their findings were humbling.

Backend logic was living directly inside route handlers with no service layer. There was no caching strategy. No async processing. Database indexing was not intentional. File handling within the Next.js runtime would not scale. The admin and operator dashboards were basic CRUD interfaces, not operational tools.

In short: the AI built what I asked it to build. But I did not know to ask for architectural best practices because I am not a software architect. The product worked. But it was not built to scale.

So I went back to Claude Code with a master refactoring prompt. I made architectural decisions: keep the monolith but add proper service layers, use Vercel KV for caching instead of Redis, keep Vercel Blob for file handling but add async processing. Phase by phase, the codebase improved. When I sent it back to the development team, their response was; and I am paraphrasing; “this is much better; 80% of the work is done.”

The lesson: vibecoding gives you speed. It does not give you architecture wisdom. You still need human experts to audit what the AI builds. Anyone who tells you otherwise is selling you something.

## The Cost Equation Has Fundamentally Changed

Let me put numbers to this.

What I built in the last four weeks, a two-sided marketplace, a full platform rebuild, 15 interactive tools, 2,500+ SEO pages, multiple client deliverables — would have cost me a minimum of $50,000 if I had hired a development agency. Realistically, closer to $80,000-$100,000. And it would have taken three to six months with constant back-and-forth, scope creep, and misaligned expectations.

My actual cost: approximately $500 in AI subscriptions over four weeks. Plus my time. Plus a few hundred dollars for an independent technical review.

That is not a marginal improvement. That is a category shift. And it has massive implications for bootstrapped founders, solo operators, and anyone building in a niche vertical where the budget for custom software simply did not exist before.

I could never have justified spending $50,000 to build BookMyColiving as an experiment. But I could justify four weeks of intense work and $500 to see if the idea had legs. That changes the calculus for every operator I advise.

## What Vibecoding Cannot Do

I want to be balanced here because the hype is real and it is misleading.

Vibecoding cannot replace product thinking. The AI did not decide which 15 tools to build for coliving operators. I did because I have spent a decade in the industry, and I know what operators struggle with. The AI did not decide that BookMyColiving should have community-type filtering or that the SEO architecture should be built around city + keyword combinations. That came from understanding the market.

Vibecoding cannot replace user research. I still need to talk to operators, understand their workflows, and figure out what problems are worth solving. The AI executes. It does not strategize.

Vibecoding cannot replace distribution. This is the part that most people have not realised yet. There will be a massive wave of AI-built products in the next 12 months. Most of them will die because nobody uses them. Building is no longer the bottleneck. Finding users, building distribution channels, and creating content that attracts the right audience, that is the bottleneck now. Marketing is more important than ever, not less.

And vibecoding cannot replace taste. Knowing what to build is harder than building it. Critical thinking, creative thinking, product-first thinking, and user-first thinking; these are the skills that will matter most in the next decade. The companies that win will not be the ones with the best AI tools. They will be the ones with the best understanding of their users.

## Documentation Is Your Moat

One unexpected benefit of vibecoding: it forces you to document everything.

Every prompt I wrote is a specification. Every PRD is a product decision captured in writing. Every QA sheet is an audit trail. Every refactoring prompt is an architectural decision with reasoning attached.

When I eventually hand off any of these projects to a development team or hire engineers they will inherit a fully documented product. Not a codebase with tribal knowledge locked in someone’s head. A codebase with written intent behind every major decision.

The more you document, the more you write, the more original your thinking is, the better the outputs will be. This is true for AI-assisted development, and it is true for building anything.

## What’s Next

I am not stopping.

The immediate plan is to continue building traffic and a user base for BookMyColiving. The platform is live. The SEO pages are indexed. Now I need operators to list and tenants to discover. That is a marketing and distribution challenge, not a product challenge.

For Everything Coliving, I want to keep expanding the tools, the directories, and the content. The platform rebuild after the Google algorithm penalty is already showing results, 2X growth in impressions in the last 28 days. The foundation is solid. Now it is about compounding.

For JumboTiger, the PRD is ready. Execution is next.

And personally, I want to keep experimenting. I will fail at some things. I will get better at others. I will keep learning, unlearning, and relearning. That is the only way this works.

## The Real Takeaway

This is not a story about AI tools. This is a story about intent.

There are a hundred reasons you can give yourself for not starting. You do not know how to code. You do not know how to set up a repository. You do not understand the technology. All valid reasons. All irrelevant now.

The only thing that matters is: do you know what you want to build, and are you willing to put in the work to describe it precisely enough for it to get built?

Being technical or non-technical is no longer the dividing line. The dividing line is between people who have clarity on what needs to exist and people who do not.

I am a zero-technical ex-founder turned freelancer turned entrepreneur again. I have spent 11 years in coliving, and I could not write a for loop. And in four weeks, I shipped more product than I did in the previous two years combined.

If that does not tell you something about where we are headed, I do not know what will.

Start. The tools are ready. The question is whether you are.

Tags:Ai CodingAi DevelopmentAi for FoundersAi Tools 2026Bootstrapped FounderBuilding with AiClaude AiClaude CodeColiving TechDigital NomadFounder JourneyIndie HackerNo-codeNon-technical FounderPrdProduct ManagementPrompt EngineeringProptechShipping ProductSoftware DevelopmentSolopreneurStartup ToolsVibecodingVibecoding ExperienceZero to One

Share:

Mayank Pokharna

Entrepreneur, coliving expert, and digital nomad. Co-founded SimplyGuest ($1M ARR) and Artof.Co; now buildsEverything Coliving,JumboTigerandAICabinet. Consulted 60+ coliving operators across15+ countries.

Read full bio →Get in touch

### Want to get fluent in AI without learning it all yourself?

AICabinet is my private 1:1 advisory for founders and CXOs — turning a fast-moving field into clear decisions and working systems.

Explore AICabinet

### Get the next one in your inbox.

I write about building things, chasing curiosity, and the coliving industry — one email every Tuesday. 1M+ reads.

Subscribe

Your email goes to Substack. Unsubscribe any time.Privacy.

## Related Posts

The 101st City

### The 101st City

An anonymous email. 4,200 beds across 11 cities. An operator nobody has ever heard of. Two dead engineers. And a USB drive in an empty coliving room that changes everything. A fictional thriller set in the world I know best — where the real danger is not the market, but…

Mar 27, 2026

### Does customer service create a formidable sales channel?

In the last few years, customer service and customer experience have changed to the core. If you ask the top management today in any internet company what is the top priority of the business, the answer would be "Customer Experience" by a long margin.

Oct 3, 2021

### Basics of Digital Marketing – Social Media Marketing, SEO, Google Adwords

I started learning about digital marketing while I was still in college. There was  so much to read on the web that I generally got confused as to what should I read and what not. Hence, now as I have gone through the basics of digital marketing and have applied…

Feb 14, 2017
