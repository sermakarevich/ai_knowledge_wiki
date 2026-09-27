---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: 4 Weeks of Vibecoding: What I Built, What I Learned, and… | Pokharna Talks

Answer from memory before opening any answer.

### Q1. What was the author's technical starting point on February 12, 2026, and where did he stand one month later?

> [!tip]- Answer
> On February 12, 2026 he could not set up a GitHub repo, had never used a terminal to push code, and had never written a commit message — his wife set up his Claude Code plan for him. By March 12 he had 197 commits across multiple live projects and claims to have shipped more product than most funded startups ship in a quarter. See [[wiki/01-vibecoding-definition-and-built-projects|Vibecoding Is Not Coding. It Is the Wrong Word.]].

### Q2. How does the author define vibecoding, and why does he call it the wrong word?

> [!tip]- Answer
> He defines it as: "if you have a vision, if you know what you need to build, if you understand the problem deeply enough, you can just get it done" — you write the details of what you want done, and AI coding tools execute. The word misleads because it sounds like developers in flow state needing syntax, languages, and frameworks, whereas he knows no JavaScript, TypeScript, Prisma, or Next.js App Router and relies on domain knowledge instead. See [[wiki/01-vibecoding-definition-and-built-projects|Vibecoding Is Not Coding. It Is the Wrong Word.]].

### Q3. What four projects shipped in the four weeks, and what did the two largest ones include?

> [!tip]- Answer
> The four were BookMyColiving.com (full two-sided marketplace), the EverythingColiving.com rebuild, the JumboTiger PRD, and the PokharnaTalks.com blog/portfolio rebuild. BookMyColiving has 3 role-based portals (tenant, operator, admin) with listings moderation, messaging, reviews, lead management, CSV exports, and 2,500+ SEO pages on Next.js/TypeScript/Prisma/PostgreSQL/Vercel; the EverythingColiving rebuild grows 170+ pages to a planned 300+ with 15 interactive operator tools plus vendor, operator, and markets directories. See [[wiki/01-vibecoding-definition-and-built-projects|Vibecoding Is Not Coding. It Is the Wrong Word.]].

### Q4. What is the author's "speaking products into existence" process, and how did the deliverable change?

> [!tip]- Answer
> He thinks through user flows, data models, edge cases, and dislikes of existing solutions while walking, driving, or between calls, speaks requirements into a voice memo app, has AI transcribe and structure them into a specification, and feeds it to Claude Code. The deliverable changed from a Jira ticket sitting in a backlog for weeks to a detailed prompt that becomes a live feature within hours. See [[wiki/01-vibecoding-definition-and-built-projects|Vibecoding Is Not Coding. It Is the Wrong Word.]].

### Q5. What is the article's core takeaway, and what dividing line replaces technical vs. non-technical?

> [!tip]- Answer
> The takeaway is explicit: "This is not a story about AI tools. This is a story about intent" — the only thing that matters is knowing what you want to build and describing it precisely enough for it to get built. The old dividing line of technical vs. non-technical is replaced by clarity vs. lack of clarity on what needs to exist, with excuses like not knowing how to code declared "all valid" but "all irrelevant now." See [[wiki/02-lessons-limits-and-takeaway|The Real Takeaway]].

### Q6. How does the author describe himself in the closing, and what is the article's final line?

> [!tip]- Answer
> He calls himself a zero-technical ex-founder turned freelancer turned entrepreneur again with 11 years in coliving who "could not write a for loop," and claims he shipped more product in four weeks than in the previous two years combined. The article closes with the call to action: "Start. The tools are ready. The question is whether you are." See [[wiki/02-lessons-limits-and-takeaway|The Real Takeaway]].

### Q7. (evaluation) A non-technical domain expert wants to copy this approach and ship a production marketplace in a month with no engineering review. Should you endorse that plan as stated, and what should you recommend instead?

> [!tip]- Answer
> No — the article proves that precise domain specification can produce volume fast, but it reports shipped features and commit counts, not reliability, security, or maintainability evidence for a production marketplace. Recommend adopting the spec-first voice-memo-to-PR D discipline while adding engineering review of the AI-generated stack (auth, permissions, data handling) before launch, so intent stays the driver without mistaking output volume for production readiness. See [[wiki/02-lessons-limits-and-takeaway|The Real Takeaway]].
