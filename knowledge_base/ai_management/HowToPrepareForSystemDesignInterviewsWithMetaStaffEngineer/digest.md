> [[index|Wiki]] | [[summary|Summary]]

# How to Prepare for System Design Interviews w/ Meta Staff Engineer — Digest

## 1. [[wiki/01-if-you-click-play-on-this|If You Click Play on This]]

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

## The argument in five moves

1. System design prep feels overwhelming, but like LeetCode for coding, it becomes manageable by working backwards from common problems to learn recurring patterns instead of memorizing solutions.
2. First understand what the interview really is: a timed whiteboard boxes-and-arrows exercise judged on problem solving, solution design, technical excellence, and communication, run through a fixed framework from requirements to deep dives.
3. Refresh the six fundamentals — storage, scalability, networking, latency/throughput/performance, fault tolerance, and CAP — which cover 90+% of what interviews demand.
4. Learn the reusable components present in almost every design — database, cache, message queue, load balancer, blob storage, and CDN — and how to choose between them by access patterns and trade-offs.
5. Work the 10 ordered problems from Bitly to Post Search with active timed whiteboard attempts, filling known unknowns via search/AI and catching unknown unknowns from expert breakdowns, then rehearse delivery aloud through peer or professional mocks.
