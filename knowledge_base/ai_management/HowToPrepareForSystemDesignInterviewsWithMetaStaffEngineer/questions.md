---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: How to Prepare for System Design Interviews w/ Meta Staff Engineer

### Q1. What are the four steps of the system design prep roadmap, in order, and what pattern do they mirror from coding prep?
> [!tip]- Answer
> The four steps are (1) understand what a system design interview actually is, (2) refresh fundamentals, (3) learn the basic components present in almost every design, and (4) work backwards from common problems to build deeper understanding. Like LeetCode prep for coding, the method is to identify recurring patterns across problems rather than memorizing random solutions. See [[wiki/01-if-you-click-play-on-this|If You Click Play on This]].

### Q2. What does a system design interview actually look like, and what fixed framework should you follow?
> [!tip]- Answer
> You come to a whiteboard and design a system like Ticketmaster or Uber with boxes and arrows, writing no code, covering product problems (Dropbox, Uber, Netflix) and infra problems (rate limiter, message queue, pipelines). Follow the fixed sequence: requirements (functional plus non-functional) → core entities → APIs → simple high-level design → deep dives. The framework keeps you focused and on time across 35 minutes to an hour of talking. See [[wiki/01-if-you-click-play-on-this|If You Click Play on This]].

### Q3. What are the four dimensions interviewers evaluate, and what does each one test?
> [!tip]- Answer
> Interviewers evaluate problem solving (recognizing and prioritizing core challenges, e.g. the Ticketmaster booking flow over authentication), solution design (weighing trade-offs to meet functional requirements), technical excellence (going deep on specific technologies and failure modes in deep dives), and communication (clearly explaining complex concepts while talking for 35 minutes to an hour). Every company uses some permutation of these four. See [[wiki/01-if-you-click-play-on-this|If You Click Play on This]].

### Q4. What are the six fundamentals that cover 90+% of system design interviews, and what does each one cover?
> [!tip]- Answer
> The six are storage (relational vs. document vs. key-value, ACID vs. BASE chosen by access patterns), scalability (vertical vs. horizontal compute, partitioning/sharding with consistent hashing), and networking (application, transport, and network layers of OSI). The remaining three are latency/throughput/performance (approximate latencies, capacity estimation, bottleneck fixes like caching), fault tolerance and redundancy (replication, failure detection, multi-server/rack/data-center redundancy), and CAP theorem (partition tolerance is guaranteed, so choose availability or consistency). See [[wiki/01-if-you-click-play-on-this|If You Click Play on This]].

### Q5. What are the six reusable components in almost every design, and how do you choose between them?
> [!tip]- Answer
> The six are database (Postgres, MongoDB, Redis — "where your data lives when the power goes off"), cache as short-term memory with eviction trade-offs, message queues for async "texting instead of calling" with delivery-semantics trade-offs, load balancer for traffic control across scaled servers, blob storage like S3 for unstructured files, and CDN as a global cache like Cloudflare. Skip the SQL-vs-NoSQL debate and pick by asking how the app reads and writes data, choosing whatever makes common operations fast and simple. See [[wiki/01-if-you-click-play-on-this|If You Click Play on This]].

### Q6. How should you practice the 10 ordered problems, and what are known unknowns vs. unknown unknowns?
> [!tip]- Answer
> Work the 10 problems in order from Bitly through Dropbox and Ticketmaster to Post Search, since each introduces patterns that reappear later; passively watching is fine for the first ~3, but after that open an online whiteboard, start a timer, and attempt each problem yourself. Confusions you notice are known unknowns to fill via Google or ChatGPT, and only then watch the expert breakdown to catch unknown unknowns you didn't know you were missing. Finish by practicing delivery aloud through peer or professional mocks with interviewers from your target company. See [[wiki/01-if-you-click-play-on-this|If You Click Play on This]].

### Q7. Is Evan's "work backwards from 10 ordered problems" plan the right prep strategy for a candidate whose fundamentals are shaky?
> [!tip]- Answer
> Judge it against the video's own sequencing: the plan explicitly starts with interview format, six fundamentals, and components before any problems, and says most learning comes from problems only once "everything I just talked about was not foreign to you." Recommend a shaky candidate spend extra cycles on fundamentals and components via the linked resources first, then enter the problem cycle at Bitly with timed attempts rather than passive watching. Skipping straight to problem 10 or pure video-watching would invert the strategy the video argues for. See [[wiki/01-if-you-click-play-on-this|If You Click Play on This]].
