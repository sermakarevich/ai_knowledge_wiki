> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# If You Click Play on This

**In one sentence:** Former Meta Staff engineer Evan (Hello Interview co-founder) argues system design prep feels overwhelming but becomes manageable by first understanding the interview format, refreshing six fundamentals and common components, then working backwards through 10 ordered practice problems using timed whiteboard attempts instead of passive watching.

## Key points

- Speaker credibility: Evan is a former Meta Staff engineer who conducted many hundreds of interviews and, via Hello Interview, has worked with hundreds of thousands of candidates.
- Core prep strategy has 4 steps in order: (1) understand what a system design interview actually is, (2) refresh fundamentals, (3) learn basic components present in almost every design, (4) work backwards from common problems to build deeper understanding.
- Method mirrors coding prep (LeetCode pattern): identify patterns across problems rather than memorizing random solutions; specific problem order is given later in the video.
- Interview format: whiteboard boxes-and-arrows design of a system like Ticketmaster or Uber, no code; the video covers the most common bucket — product and infra design problems.
- Recommended framework is fixed sequence: requirements (functional + non-functional) → core entities → APIs → simple high-level design → deep dives; evaluation covers problem solving, solution design, technical excellence, and communication over 35 minutes to an hour of talking.
- Six fundamentals cover 90+% of needs: storage, scalability, networking, latency/throughput/performance, fault tolerance and redundancy, CAP theorem.
- Components introduced: database (e.g. Postgres, MongoDB, Redis), cache (e.g. Redis), message queues (e.g. Kafka, RabbitMQ, SQS), load balancer, blob storage (e.g. S3), CDN / content delivery network (e.g. Cloudflare) as a global cache.
- Practice plan: work 10 problems in order starting with Bitly, then Dropbox, Ticketmaster, ending with Post Search; passively watch the first ~3, then for the rest use a timer plus online whiteboard, look up known unknowns via Google / ChatGPT, then watch the breakdown to catch unknown unknowns.

---

## Who is speaking and why

Evan introduces himself as a former Meta Staff engineer who has conducted "many hundreds of interviews" and is now co-founder of Hello Interview, described as "a platform that helps candidates just like you prepare for their upcoming interviews." Through that role he claims to have worked with "hundreds of thousands of candidates," giving him a view of "what works and what doesn't."

Verbatim framing:

- "system design can feel incredibly overwhelming, but it doesn't have to be."
- "The key, just like with leak code [LeetCode] for coding prep, is to work backwards from common problems."

## Prep roadmap

Ordered plan stated in the chunk:

1. Understand "what the hell a system design interview actually is."
2. Refresh fundamentals — "concepts that you likely learned back in college and just need a touch up."
3. Get familiar with "the basic components that are present in in almost every single system design."
4. "Start to work backwards from those common problems so that we can build a deeper understanding."

He promises to tell viewers "exactly which problems I would focus on and in what order a little bit later on in this video."

## What a system design interview really is

Textbook definition given: it "evaluates your ability to architect complex, scalable systems that solve real world problems." Practical version: "You come to a whiteboard. The interviewer asks you to design a system, something like Ticket Master or Uber, and you draw boxes explaining at a high level what services and interactions are necessary." Explicitly: "You're not writing code. It's typically just boxes and arrows."

Two heavily overlapping buckets covered:

| Type | Definition in chunk | Examples named |
|---|---|---|
| Product problems | Designing an app or website you use every day | Dropbox, Uber, Netflix |
| Infra / infrastructure problems | Non-user-facing systems / components | Rate limiter, message queue ("message cue"), data processing pipelines, ad-click aggregator |

## Framework to follow

Claim: "it's really, really, really important that you follow a framework. This keeps you focused and it makes sure that you're on time."

| Step | What to do | Details from chunk |
|---|---|---|
| 1. Requirements | Outline functional + non-functional requirements | Functional = features (e.g. user should be able to book a ticket); non-functional = quality (e.g. booking should be low latency, scale to N users); ensures you and interviewer agree on what is being designed |
| 2. Core entities | Outline entities the system persists | "Typically map directly to the tables in your database"; example: user, event, ticket; APIs will exchange these |
| 3. APIs | Outline basic APIs for functional requirements | "Nine times out of 10, these are probably going to be REST endpoints"; GraphQL or other only in unique cases |
| 4. High-level design | Whiteboard boxes and arrows, simple design first | Goal is to meet functional requirements (e.g. allow booking a ticket), not complex yet |
| 5. Deep dives | Enhance the design | Goal is to satisfy non-functional requirements: low latency, strong consistency, agreed scale numbers |

## How interviewers evaluate

"Every company is slightly different," but evaluation is "some permutation" of:

1. Problem solving — "most importantly your ability to recognize and prioritize the core challenges"; for Ticketmaster focus on booking flow, "not focused on authentication, for example."
2. Solution design — the high-level design; "Did you weigh trade-offs and did you arrive at something that meets those functional requirements?"
3. Technical excellence — shown in deep dives; expertise "in some, not all" areas; "Can you go deep? Talk about specific technologies. Talk about specific areas where things could break."
4. Communication — "Can you clearly explain complex technical concepts? You'll be talking for 35 minutes to an hour during the system design interview."

## Six fundamentals (90+ percent)

Claim: long online lists are overwhelming, but "knowing these six concepts here are going to get you 90 plus% of the way there."

1. **Storage fundamentals:** relational (normalized tables with relationships) vs. document stores (nested JSON-like structures) vs. key-value stores (simple key lookup); ACID (acid properties) for transactional systems vs. BASE (base principles) for distributed databases; choose by access patterns and consistency requirements from non-functional requirements.
2. **Scalability:** scaling compute via vertical scaling ("beefier machines, more CPU, more RAM") and horizontal scaling ("just add more machines"); scaling storage via partitioning and sharding across database instances plus distribution methods like "the famous consistent hashing algorithm" (separate channel video referenced).
3. **Networking:** of the OSI layers learned in college, "you only really need to know three": application layer (most important — REST vs. GraphQL vs. gRPC trade-offs, real-time via websockets or server-sent events e.g. chat app), transport layer (especially for infra interviews — TCP vs. UDP, request lifecycle), network layer (basic load balancing, maybe firewalls / access control lists, less likely unless specific interview type). A separate "networking essentials" video is referenced.
4. **Latency, throughput, and performance:** recall approximate latencies (memory access, disk reads, network calls); show throughput understanding and basic capacity-planning estimations during requirements; identify bottlenecks and fixes "in your distributed architecture," e.g. "adding a cache to lower latency" (article linked below video).
5. **Fault tolerance and redundancy:** "failures are inevitable in distributed systems"; discuss replication strategies and failure detection; add redundancy at servers, racks, maybe data centers to "recover from these failures gracefully."
6. **CAP theorem:** raised in non-functional requirements and upheld through the design; "consistency, availability, and partition tolerance. Your system can only have two of the three. Partition tolerance is a guarantee. And so your only decision is should my system prioritize availability or consistency?" A sub-10-minute CAP video is referenced.

## Basic components in almost every design

- **Database — "where your data lives when the power goes off":** Postgres (strict tables with clear rules), MongoDB (documents / JSON blobs), Redis / "Reddus" (fast key-value lookups). Warning: "don't get caught up in the old SQL versus NoSQL debate. Most modern databases can scale well and can maintain data integrity." Real question: "how does your app need to read and write data?" then pick what makes common operations "fast and simple."
- **Cache — "your system's short-term memory":** e.g. Redis; stores frequently accessed data to avoid hitting the database; "way faster" but challenge is freshness — decide "how long information stays valid" / eviction; makes repeated requests "lightning fast" but adds complexity.
- **Message queues — "texting instead of calling":** one service drops a message, another picks it up asynchronously when ready; examples Kafka, RabbitMQ, SQS ("Rabbit MQ, maybe SQS"); handles traffic spikes and survives a service crash; challenge is delivery semantics — "sometimes they get delivered once, sometimes potentially they get delivered multiple times" so strategies are needed.
- **Load balancer — "traffic control":** routes incoming requests across horizontally scaled servers "so that no single machine gets overwhelmed."
- **Blob storage:** database is for structured data (user accounts, product info), not large files; "trying to cram those things into your database is like forcing a square peg into a round hole" — bloats DB, slows queries, makes backups "a nightmare"; use e.g. S3 for unstructured media / large text at cheaper cost; rule: structured data in database, unstructured in blob storage.
- **CDN — "it's just a cache":** global distribution placing content closer to users; example Cloudflare ("Cloudfare"); stores copies of images, videos, static files often from blob storage; e.g. a user in India pulls from a local CDN server instead of America, making downloads faster.

## The 10 problems and how to practice them

Transition claim: "if you're thinking that everything that I just talked about was not foreign to you, then you are already ready to start working through the problems"; gaps can be closed via links below (videos / written resources), but "most of your learning is going to come from working through core problems."

- List: "just 10 problems here" covering "the overwhelming majority of concepts"; order starts "with Bitly, then Dropbox, Ticket Master, and then all the way around until you end with Post Search"; each introduces techniques/patterns that "continue to reappear in problems later on in this list."
- Practice method: for Bitly, Dropbox, "maybe even Ticket Master" passive video consumption is reasonable; "after those three, the key, and this is so so so so important, the key is to try it yourself."
- Cycle: open an online whiteboard, start a timer, work the problem; confusions found are "known unknowns" — search Google / "ChatGBT" to fill blanks; "then, and only then" watch the video / read the breakdown to find "unknown unknowns" ("things that you didn't even know you were missing"); "rinse and repeat" through all 10.
- Hello Interview specifics: "Stephan and I have written detailed breakdowns and recorded videos for each of these 10 problems, as well as over 15 others"; premium "guided practice" for each of 25 problems walks the delivery framework with inline feedback on whiteboard plus text (Ticketmaster free to everybody); closing advice: system design is also presentation, so "audibly" practice with friends / colleagues / peer mocks or professional mocks with interviewers from the target company (e.g. "an interviewer who's actively an interviewer at Meta").

**Covers:** Intro and prep strategy for system design interviews with Meta Staff Engineer (Hello Interview video).
