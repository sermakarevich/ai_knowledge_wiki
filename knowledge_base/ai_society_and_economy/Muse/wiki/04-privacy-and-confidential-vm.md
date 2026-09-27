> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Privacy and Confidential VM
**In one sentence:** Muse is built to keep personal chats away from ads and let people opt out of training today, with a future locked computer version that even Meta cannot open.
## Key points
- Each person gets their own dedicated VM (Virtual Machine, an isolated computer running in the cloud) that other agents cannot reach, and this is where chats, data, and connected service details are stored.
- Muse does not share a person's conversations or VM data with Meta ad systems, and there is no advertising inside Muse today.
- By default Meta can use queries made to its AI (Artificial Intelligence, computer software that can learn and do tasks) models, but people can turn this off and opt out of training Meta models on their interactions.
- Muse remembers important details so it can help without being told twice, but a person can tell it to "forget" specific things it has learned at any time.
- Muse has no visibility into passwords or payment methods because those go into secure storage that it can use without seeing them, including passwords typed into its browser.
- Payment today can use Link built by Stripe with one-time-use cards that hide real card details, while Shop Pay and 1Password login support are still to come.
- Muse Confidential VM, a promised future version where the whole VM is locked with a key only the person holds so not even Meta can access the data, is planned for later this year, before the end of the year.
---
## Private computer today
Each Muse agent runs on its own dedicated computer in the cloud. Meta says this space is private to each person even though it runs on Meta infrastructure. No other person's agent can reach it. The data and login details for any connected service are stored securely there. A person chooses which apps Muse connects to and how much access it gets, and can change access or disconnect a service at any time.
## No ads and training choice
Shipped now: Muse does not share a person's conversations or the data in their VM with Meta ad systems. There is no advertising inside Muse. People can opt out of their interactions being used to train Meta AI models. Press reporting adds important detail: by default queries made to one of Meta models are able to be used by the company, so a person must use the option to turn that off.
## Memory and forget
Shipped now: Muse remembers what matters to a person so it can make suggestions without being asked and act on details mentioned only once. A person stays in control of this memory and can always tell Muse to "forget" specific things it has learned.
## Payments privacy
Shipped now: Muse can checkout with Link built by Stripe. Link creates a one-time-use card for each purchase so the real card details stay hidden. Meta says Muse is the first AI agent covered by Link purchase protections for damaged or lost items, price drops, no-fee returns, and a return guarantee on qualifying purchases. Still to come: Shop Pay as another way to pay, along with 1Password support so Muse can use logins a person already has.
## Confidential VM — promised, not yet shipped
Promised for later this year, before the end of the year: Muse Confidential VM. In this future version the whole VM, including a person's data and conversations with Muse, is encrypted with a key only that person holds, so not even Meta can access it. Press reporting describes the same plan as a confidential version where Meta cannot see what is taking place inside the user's virtual workspace. This has not shipped yet.
## Shipped now versus promised later table
| Area | Shipped now | Promised later |
|---|---|---|
| Personal space | Dedicated cloud computer per person, no other agent can reach it | Confidential VM locked with a key only the person holds |
| Ads | No advertising inside Muse, no sharing of chats or VM data with ad systems | Commerce opportunities are being explored, per Axios, which could bring future revenue |
| Model training | Person can opt out of training, but default allows use unless turned off | No new training promise in sources beyond the existing opt-out |
| Memory | Remembers details and acts on things mentioned once, plus forget on request | No change described in sources |
| Logins and payments | Hidden-credential storage, Link one-time-use cards, Link purchase protections | Shop Pay payments and 1Password login support |
## Walkthrough: turning off training use
Axios reports that by default queries made to one of Meta models are able to be used by the company, but there is an option to turn that off. Meta separately says people can opt out of their interactions being used to train Meta AI models. In plain steps: the person starts with the default setting, finds the training choice, and turns it off. Reuters confirms the same opt-out fact. The sources do not describe the exact buttons or screens, so this page does not invent them. The key privacy point is that protection here requires action by the person.
## Walkthrough: dinner-party memory with privacy controls
Meta says Muse can turn a saved Instagram recipe video into a grocery list, suggest a dinner-party menu, and remember friends' dietary restrictions before sending invites. From a privacy view, that helpful memory lives inside the person's own VM, which other agents cannot reach. If the person no longer wants a detail remembered, they can tell Muse to forget that specific thing. If they no longer want an app connected, they can change access or disconnect the service at any time. Reuters likewise says people choose connected apps and can revoke, meaning take away, access.
## What each usable source says about privacy
| Source | Privacy detail it provides |
|---|---|
| Meta official announcement | No sharing with ad systems, training opt-out, forget command, hidden credentials, future Confidential VM with user-held key |
| Axios press report | More privacy options than prior AI products, VM private to each person on Meta infrastructure, default training use with off switch, confidential version before end of year |
| Reuters wire report | Opt-out of training use, encrypted version planned later this year, revoke access anytime, safety stakes rise when real app data is connected |
| NYT (New York Times, a United States newspaper) note | No privacy claims used, because direct retrieval was blocked and the note says to skip it |
## Hidden logins walkthrough: car sale and bill lowering
Meta says Muse gets better results with less effort, with examples such as selling a car for more and lowering a bill.
Both jobs may need logins, forms, and messages to strangers.
Meta says Muse has no visibility into passwords or payment methods.
Credentials go into secure storage that Muse can use without seeing.
That includes passwords a person types into the browser themselves.
The audit trail then shows what Muse did and plans to do, and sensitive sends need approval.
## Training opt-out in plain words
Model training here means using people's chats to improve future AI (Artificial Intelligence) models.
Meta says people can opt out, meaning choose not to take part, in training use.
Axios adds the default detail: queries to Meta models can be used unless the person turns that option off.
Reuters confirms users can opt out of having interactions used to train Meta models.
The sources do not describe the exact settings screen, so this page does not invent steps.
For approval checks on sensitive actions, see [[03-sentinel-permissions|Sentinel Permissions]].
## Confidential VM timing from two sources
Meta says it will introduce Muse Confidential VM later this year.
Axios says Meta is aiming to release that confidential version before the end of the year.
Reuters likewise says an encrypted version is planned later this year.
All three point to the same promise: the whole VM, including data and chats, locked with a key only the person holds.
Not even Meta could access it in that future design.
Today's VM is private per person but still runs on Meta infrastructure.
Axios frames this as more privacy options than with prior AI products, as suggested in Zuckerberg's manifesto.
Reuters notes safety stakes rise once the agent touches real data across email, calendar, payments, health, shopping, and the smart home.
Smart home here means internet-connected home devices.
People can also change access or disconnect a service whenever they want.
Revoke means take away access completely.
## Exact words worth keeping
Meta says Muse does not share a person's conversations or the data in their VM with Meta ad systems. Meta says people can always tell Muse to forget specific things it has learned. Meta says the future Confidential VM is encrypted with a key only the person holds, so not even Meta can access it. Axios says the virtual machine is designed to be private to each person, although it runs on Meta infrastructure. Axios says Meta is also working on a confidential version where Meta cannot see what is taking place inside the user's virtual workspace.
**Covers:** 01-meta-official.md Built to be Private Safe and Secure plus payments paragraph; 02-axios.md Between the lines privacy options and confidential version timing; 03-reuters-syndicated.md opt-out of training and encrypted version planned later this year
