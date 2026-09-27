> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# How to Prepare for System Design Interviews w/ Meta Staff Engineer — In Plain Language

## What is this about?

This is a preparation guide for system design interviews, explained by Evan,
a former Staff Engineer at Meta (a very senior engineer title) who has run
hundreds of interviews and now teaches candidates through Hello Interview.

The main message is simple: system design prep feels overwhelming, but it
does not have to be. Just like programmers use LeetCode (a popular site with
practice coding puzzles) to prepare for coding interviews, you can prepare
for design interviews by working backwards from a short list of common
practice problems.

The guide gives you a 4-step plan in order:

1. Understand what a system design interview actually is.
2. Refresh the basic fundamentals (ideas you likely met in college).
3. Learn the handful of building blocks that appear in almost every design.
4. Practice about 10 common problems, in a specific order, so patterns repeat.

A system design interview is not writing code. You go to a whiteboard
(a shared drawing board, often virtual), the interviewer names a product
like Ticketmaster (ticket sales) or Uber (ride hailing), and you draw boxes
and arrows showing which parts the system needs and how they talk to each other.

## Why does it matter?

System design interviews decide many senior engineering hires, and candidates
often fail not because they lack knowledge but because they have no plan.

This guide matters because it:

- Removes the overwhelm. Instead of endless article lists, you focus on
  6 fundamentals, 6 building blocks, and 10 problems.
- Teaches you the grading rules. Interviewers score problem solving
  (did you find the hard part?), solution design (does it work?),
  technical depth (can you go deep somewhere?), and communication
  (can you explain clearly for 35–60 minutes?).
- Gives you a fixed framework (a step-by-step script) so you stay on track
  and finish on time instead of rambling.
- Shows how to practice actively. Watching videos feels productive but does
  not build skill. Timed whiteboard attempts do.
- Comes from someone who sat on the other side of the table hundreds of times.

## How does it work?

Think of it like learning to cook: first learn the kitchen rules, then the
basic ingredients, then cook a short menu of dishes from easy to hard.

**Step 1 — Learn the interview script.** Every answer follows the same order:

1. Requirements: what must the system do (features) and how well
   (speed, size, reliability)? Agree on this with the interviewer first.
2. Core entities: what things must be saved, e.g. user, event, ticket?
   These usually become tables in the database.
3. APIs: how do parts talk to each other? Usually simple REST endpoints
   (standard web addresses an app calls, like POST /bookings).
4. High-level design: draw a simple boxes-and-arrows sketch that covers
   the main features. Keep it simple first.
5. Deep dives: improve the sketch to hit the quality goals — faster,
   bigger, more reliable. This is where you show depth.

**Step 2 — Refresh 6 fundamentals.** These cover more than 90% of interviews:
storage, scaling, networking, speed math, failure handling, and CAP trade-offs.

**Step 3 — Learn 6 reusable building blocks:** the database (permanent
storage), the cache (fast short-term memory), the message queue (async
texting between services), the load balancer (traffic controller), blob
storage (cheap home for big files), and the CDN (worldwide copies near users).

**Step 4 — Work 10 problems in order.** Start with Bitly (a link shortener),
then Dropbox (file storage), then Ticketmaster, and finish with Post Search
(searching posts). Watch the first ~3 passively. After that: open a timer,
try each one on a whiteboard yourself, Google what confused you, and only
then watch the expert answer to catch what you did not even know was missing.
Repeat for all 10, then rehearse out loud with friends or mock interviews.

## Where can this be used?

- Preparing for product design questions: design Dropbox, Uber, Netflix,
  Ticketmaster, or a link shortener like Bitly.
- Preparing for infra (infrastructure, meaning behind-the-scenes) questions:
  design a rate limiter (a guard against too many requests), a message queue,
  or a data pipeline (a chain of steps that moves and processes data).
- Interviews at Meta and other large tech companies with the same whiteboard
  format and grading style.
- On the job: sketching a new feature, choosing storage, adding a cache,
  or explaining trade-offs to teammates uses the same steps.
- Study groups and mock interviews: the fixed script and timed-attempt method
  work well with a partner.

## Conclusions & takeaways

- Do not memorize solutions. Learn the repeating patterns across problems.
- Follow the framework every time: requirements, entities, APIs,
  simple design, then deep dives.
- Aim simple first, then improve. Find the core hard part (for Ticketmaster
  it is booking, not login) and spend your time there.
- Know a little about everything and a lot about something. Depth in one or
  two areas beats shallow talk everywhere.
- Practice out loud under a timer. System design is a talk, not just a drawing.
- If a topic feels familiar, start solving. Most learning comes from the
  10 problems, not from re-reading theory.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| System design interview | A test where you sketch how a big app would work, with boxes and arrows, no code. |
| Functional vs non-functional requirements | What the system does (book a ticket) vs how well it does it (fast, for millions). |
| High-level design | A simple first sketch of the parts and how they connect. |
| Deep dive | Going into detail on one hard part, e.g. making booking fast and correct. |
| Scalability (vertical vs horizontal) | Handling more load by buying a bigger machine vs adding more machines. |
| Latency vs throughput | How slow one request is vs how many requests you finish per second. |
| Cache (e.g. Redis) | Fast short-term memory that saves repeated trips to the database. |
| Load balancer | A traffic controller that spreads requests so no server gets crushed. |
| Message queue (e.g. Kafka) | Like texting instead of calling: services leave messages others read later. |
| Blob storage (e.g. S3) | Cheap storage for big unstructured files like photos and videos. |
| CDN (content delivery network) | Copies of files stored around the world so users download from nearby. |
| CAP theorem | When parts of the system disconnect, you must pick speed of access or data correctness. |
