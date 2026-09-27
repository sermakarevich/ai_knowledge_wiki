> [[index|Wiki]] | [[summary|Summary]]

# Muse — In Plain Language

## What is this about?

Think of Muse as a helper you text, who then goes and does the errand for you.

Meta announced Muse on September 8, 2026, as a personal AI agent.
An agent here means software that acts on your behalf, not just answers questions.

You talk to it like messaging another person, in a dedicated Muse app or in WhatsApp.
You can name your agent and create an avatar for it.

You tell it what needs to get done in normal language, and it takes action.
Examples from Meta are sending an email, booking travel, opening a browser, filling out forms, and negotiating for you.

Reuters reports it can autonomously send emails, sell a car, and book travel.
Reuters also reports it was modeled on an open-source agent called OpenClaw and was known inside Meta under the codename Hatch.

Meta says it is powered by Muse Spark, its most capable model to date, built for real-world agent work.
Axios reports it is built on the latest generation of models developed under chief AI officer Alexandr Wang.

Meta says it remembers what matters to you, so it can suggest things without being asked.
A favorite example: you once save a recipe video on Instagram, and later Muse turns it into a grocery list.

Meta says it was built for billions of people worldwide with no learning curve.
No learning curve means no technical training is needed, it works right away.

## Why does it matter?

Most chatbots are like a librarian: they answer, then you do the work.

Muse tries to be more like an assistant with keys to your office: you share a goal once, it makes a plan, coordinates time and resources, and keeps advancing the work on its own.

That matters for long jobs that take many small steps over days.
Meta says Muse keeps working after you close the app, then comes back when something changes or needs approval, like before sending an email or making a purchase.

It also tries to be proactive instead of waiting for orders.
Meta gives examples such as suggesting a dinner-party menu, remembering friends' dietary restrictions before sending invites, lowering a bill, or adjusting an exercise plan when work or travel changes.

Meta calls this a first step toward personal superintelligence.
Axios quotes Wang calling Muse an early but big step that helps people accomplish goals, pursue passions, and build things they otherwise would not build.

Reuters connects it to CEO Mark Zuckerberg's plan to offer personal superintelligence to billions of daily Meta users.
At the same time, Reuters reports it rolled out despite internal concerns about how it handles sensitive personal data.

## How does it work?

Imagine three parts: your private office, your security guard, and your to-do list.

1. Your private office in the cloud.

Meta says each person gets their own dedicated computer in the cloud, called Muse Secure VM.
Think of it as a private office computer in the cloud, just for you and your agent.

Meta says it is contained, so no other person's agent can reach it.
That is where Muse lives, and where your data and logins for connected services are stored.

It has its own built-in browser that you can see.
Muse can open that browser, fill out sale forms, and negotiate on your behalf.

Passwords you type into that browser go into secure storage.
Meta says Muse can use them without seeing them, and has no visibility into your passwords or payment methods.

Reuters describes the same idea as a cloud-based emulation of a personal computer that lets Muse keep working in the background even when you are not actively using it.

2. Your security guard who checks every errand.

Sentinel is a separate agent that runs on that same cloud computer, kept apart from Muse at the system level.
Think of Sentinel as a security guard who checks every errand before the helper leaves the office.

Meta says nothing Muse does reaches the internet unless Sentinel approves it.
Axios explains it this way: Muse can suggest an action, but Sentinel decides whether it is allowed, blocked, or sent to you for approval.

Allowed means a previously approved lower-risk step goes ahead.
Blocked means Sentinel stops it from reaching the internet.
Sent for approval means you decide first, for example before Muse sends an email or makes a purchase.

You stay in charge of access.
You choose which apps Muse connects to and exactly how much access it gets.
You can change access or disconnect a service whenever you want.

You can give read access, which means Muse can look but not act, like reading mail.
Or write access, which means Muse can act for you, like also sending mail.
Permissions can be narrowed to one task, service, purchase, or time period.

Meta executives said asking for approval too often can backfire, because people start clicking approve without thinking.
So the design asks for sensitive steps, while approved lower-risk work proceeds.

3. Your to-do list you can audit.

Meta says Muse shows a complete audit trail of everything it has done and plans to do.
Think of it as a full receipt and upcoming to-do list in one place.

## Where can this be used?

Reuters reports Muse is designed to connect across email, calendar, payments, health, shopping, and the smart home.
Smart home means internet-connected home devices such as lights or locks.

You pick which categories are connected at all.
Axios adds permissions can be set in more detail within a single service, like allowing mail reading without allowing mail sending.

Concrete uses named in the sources:

- Email and calendar help: draft, plan, and send messages, with approval before sending.
- Selling a car for more: Muse builds a plan, opens its browser, fills out forms, negotiates, and asks before final messages or payment.
- Travel booking: arrange plans and local ground transport, meaning cars or vans on the ground. One tester praised Muse as a third participant on a three-week honeymoon in Indonesia.
- Lowering a bill: handle paperwork or negotiation to reduce what you pay.
- Training plan: adjust an exercise schedule when life shifts.
- Dinner party: turn a saved recipe video into a grocery list, suggest a menu, remember dietary restrictions before sending invites.

For paying, Meta says Muse can check out with Link built by Stripe.
Meta says it is the first AI agent covered by Link's purchase protections, which include free coverage for damaged or lost items, price drops, no-fee returns, and a return guarantee on eligible purchases.

Meta says it is rolling out in the US on iOS, Android, and muse.ai, with support for AI glasses coming soon.
Meta lists Shop Pay as another way to pay coming soon, and 1Password login support coming soon.

## Conclusions & takeaways

- Muse is a shift from answering to doing: you describe the goal, it plans and acts across apps.
- Each person gets an isolated cloud computer, so work continues in the background after the app is closed.
- Logins go into secure storage Muse can use without seeing.
- A separate Sentinel guard controls internet access, with allow, block, or ask-you outcomes.
- You control connections, choose read or write access, narrow permissions, and can revoke access anytime.
- Approval is required before sensitive actions, while approved low-risk steps proceed, and everything is listed in an audit trail.
- Stated direction is proactive personal superintelligence for billions, paired with reported internal concerns about sensitive data handling.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Agent | Software that does errands for you, not just answers, like sending mail or booking travel |
| VM / Secure VM | Your private office computer in the cloud, one per person, where Muse, data, and logins live |
| Sentinel | A security guard on that same cloud computer who checks every outward errand and allows, blocks, or asks you |
| Audit trail | A full receipt and to-do list: everything Muse did plus everything it plans to do |
| Confidential VM | A promised locked version of that office where the whole computer is locked with a key only you hold |
| Read access | Muse can look but not act, for example reading mail |
| Write access | Muse can act for you, for example also sending mail on your behalf |
| Narrow scope | Limiting permission to one job, service, purchase, or time period |
| Muse Spark | The AI model Meta says powers Muse, built for real-world agent work |
| Purchase protections | Link by Stripe coverage for eligible buys: damaged or lost items, price drops, no-fee returns, return guarantee |
