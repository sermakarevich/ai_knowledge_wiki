# Muse — Meta's Personal AI Agent

**Article:** [Introducing Muse: personal AI agent (Meta, Sept 2026)](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) — Meta Newsroom + Axios + Reuters coverage, Sept 8-9 2026

## Human Readable TL;DR

Muse is like a helper who lives in its own locked office in the cloud and runs errands for you. You tell it a goal in plain words, such as sell my car or plan my trip, and it fills forms and sends messages for you. It remembers little things you said once, keeps working even after you close the app, and knocks on your door for approval before sending anything or spending money. Meta launched it on September 8, 2026 as a first step toward everyday help for billions of people.

## TL;DR

Meta announced Muse on September 8, 2026 as a personal AI agent powered by Muse Spark. Each user gets a Muse Secure VM — an isolated cloud computer holding the agent, data, and logins in a separate space. A separate Sentinel agent guards internet access, allowing, blocking, or sending each planned action for human approval. Privacy today means no ads and a training opt-out, with a future Muse Confidential VM locked with a key only the user holds promised later in 2026.

---

## Problem & Motivation

Normal chat tools only answer questions and leave all the work to the person: sending emails, filling out forms, booking travel, lowering bills, tracking long goals. Meta says personal superintelligence — a very capable personal helper for goals and daily life — should take tasks off people's plates so they can focus on what matters, and Muse is presented as a first step toward that vision. It is built to act across apps, remember what matters, keep working in the background after the app is closed, and get better results with less effort — the examples given are selling a car for more, lowering a bill, or adjusting a training plan as life shifts. Reuters places Muse at the center of CEO Mark Zuckerberg's plan to offer personal help to the billions who use Meta services daily, while Axios links it to Zuckerberg's 6,500-word manifesto and to model work under chief AI officer Alexandr Wang.

---

## Main Original Ideas

1. **Secure VM per user** — Each person gets their own cloud computer where Muse lives with data and logins, kept separate so no other person's agent can reach it. It has a visible browser, hidden login storage, a full audit trail, and keeps working after the app is closed.
2. **Sentinel permission gate** — Sentinel is a separate guard agent on the same machine, kept apart at the system level. Nothing Muse does reaches the internet unless Sentinel approves it: it allows an action, blocks it, or sends it to the person for approval before sensitive steps like sending email or paying.
3. **Confidential VM (promised)** — A future version where the whole cloud computer is locked so not even Meta can see inside. Today's VM is private per person but still runs on Meta systems; the locked version is planned for later in 2026.
4. **Memory and proactivity** — Muse remembers details mentioned only once and helps without being asked. Examples are turning a saved Instagram recipe video into a grocery list and remembering friends' food limits before sending invites. A person can tell Muse to forget specific things at any time.
5. **Payments with protections** — Muse can pay with Link built by Stripe, which makes a one-time-use card for each buy so real card details stay hidden. Meta says Muse is the first AI agent covered by Link purchase protections for lost items, price drops, and returns. Shop Pay is coming soon as another way to pay.
6. **User control plus audit trail** — People choose which apps Muse connects to and how much access it gets, from read-only look to write access for acting. Permissions can narrow to one task, service, purchase, or time period, and can be changed or removed at any time. Muse shows a full audit trail of what it did and plans to do, and asks before sensitive sends or purchases.

---

## Key Findings

- Does work, not just answers: sends email, books travel, fills forms, and negotiates for the person — with better-result examples like selling a car for more or lowering a bill.
- Connects across email, calendar, payments, health, shopping, and smart home. People choose connected apps and can revoke access at any time.
- Runs on its own VM per person and keeps working after the app is closed, then returns when approval is needed. Sentinel guards every outward step — allowed, blocked, or sent for approval — though too many prompts risk approval fatigue (clicking approve without thinking).
- Talk to it in the Muse app or WhatsApp, with chat like a text thread. Users can name the agent and make an avatar.
- Powered by Muse Spark, described as Meta's most capable model for agent work, tied to Wang's latest models. Modeled on the open-source agent OpenClaw and known inside Meta under the codename Hatch.
- Platforms at launch: Apple iOS, Google Android, web at muse.ai, and WhatsApp. Meta AI glasses support is coming soon, not shipped now. US-only at launch, rolling out stateside first.
- Pricing: free tier for most needs, plus $20/month for heavier use and $100/month for power users. Wang says paid tiers help cover compute costs for background work.
- No ads inside Muse today, and chats are not shared with Meta ad systems. Meta is exploring future shop-related income while trying to earn beyond ads from $130B AI plans.
- Training choice: by default chats to Meta models can be used to improve models, but people can opt out. Muse can use passwords without seeing them, including passwords typed into its browser.
- Reuters internal-concerns findings: launched September 8, 2026 despite worries it mishandles sensitive data. Delayed in April 2026 to improve safety, reaching a minimum bar for safety, security, privacy, and model quality.
- Mixed tests: honeymoon-trip praise as a third participant in Indonesia, but also disconnects, sensitive uploads without permission, and a birthday-photo test that allegedly exposed private iCloud photos.
- Axios risk notes: an OpenClaw agent deleted Mac files after email access, Resy will delete accounts that use automated agents, and too many approval prompts can weaken safety.

---

## Suggestions & Future Directions

- Ship the Confidential VM, locked with a key only the user holds, later in 2026 so not even Meta can access data and chats.
- Add Meta AI glasses support, Shop Pay payments, and 1Password login support — all announced as coming soon.
- Answer the trust question: will ordinary users grant ever more access to personal data, and will Muse prove useful enough to justify the risk.
- Keep improving approval balance so Sentinel asks for sensitive steps without tiring people with too many small prompts.
- Learn from failures: disconnects, unapproved uploads, photo-exposure reports, and outside service rules like Resy.
- A NYT article was paywalled, so no claims from it are used and reviewing it remains future work.

---

## Authors & Institutions

- Meta: built and announced Muse in September 2026.
- Mark Zuckerberg, CEO: presented Muse as a key next step toward personal superintelligence for billions of users.
- Alexandr Wang, chief AI officer: led latest model work; said free tier fits most users and paid tiers cover compute costs.
- Vishal Shah, VP of AI products: said the April 2026 delay helped meet the minimum safety bar, and that mistakes can still happen.
- Summer Yue, Meta executive cited by Axios: shared an OpenClaw file-deletion case as a warning about agent risks.
- Press: Ina Fried / Axios (chat interface, Sentinel details, proactive design, glasses timing, pricing, trust risks); Katie Paul / Reuters (September 8 rollout, Hatch codename, OpenClaw model, app links, WhatsApp access, pricing, internal concerns).
- Sources used: Meta Newsroom announcement plus Axios and Reuters coverage from September 8–9, 2026.
