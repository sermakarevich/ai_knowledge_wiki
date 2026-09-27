> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Muse Secure VM Architecture
**In one sentence:** Meta says Muse runs on Muse Secure VM, a dedicated per-person cloud computer that holds the agent, the person's data, and their service credentials in an isolated space.
## Key points
- Meta says each person gets their own dedicated computer in the cloud that runs their Muse agent.
- Meta says each cloud computer is contained, so no other person's agent can reach it.
- Meta says the VM (Virtual Machine, an isolated computer running in the cloud) stores the agent, the person's data, and credentials for connected services.
- Meta says the VM includes its own built-in browser that the user can see.
- Meta says credentials go into secure storage that Muse can use without seeing, including passwords the person types into the browser.
- Meta says Muse shows a complete audit trail of everything it has done and plans to do.
- Meta says Muse keeps working after the person closes the app and returns when something changes or needs approval.
- Reuters reports that each Muse agent runs on its own VM (Virtual Machine, an isolated computer running in the cloud), which lets it keep working in the background.
---
## What the Secure VM is
Meta says Muse runs on Muse Secure VM, a dedicated VM (Virtual Machine, an isolated computer running in the cloud). Meta describes it as a personal agent needing a new kind of secure computer, and says it built one for everyone.
## One VM per person, kept separate
Meta says Muse runs on its own dedicated computer in the cloud, contained so no one else's agent can reach it. Axios similarly reports that the VM (Virtual Machine, an isolated computer running in the cloud) is designed to be private to each person, although it runs on Meta's infrastructure. Reuters reports that each Muse agent runs on its own virtual machine, described as a cloud-based emulation of a personal computer.
## What lives inside the VM
Meta says that is where Muse lives and where the data and credentials for any service a person connects are securely stored. Meta says the VM houses both the agent and a person's data. Meta says people choose which apps Muse connects to and exactly how much access it gets, and can change access or disconnect a service whenever they want.
## Built-in browser the user can see
Axios reports that the Muse agent runs on a dedicated virtual machine in Meta's cloud, using a built-in browser that is visible to the user. Meta says Muse can open a browser, fill out forms, and negotiate on the person's behalf.
## Credential storage Muse cannot see into
Meta says Muse has no visibility into people's passwords or payment methods. Meta says any credentials a person shares go into secure storage, so Muse can use them without seeing them, including passwords a person types into the browser themselves.
## Audit trail and approval checks
Meta says Muse checks with the person before sensitive actions like sending an email or making a purchase. Meta says Muse shows people a complete audit trail of everything it has done and plans to do. Reuters similarly reports that among the protections is a separate agent that monitors planned actions and in certain cases prompts Muse to seek authorization before carrying them out.
## Works after the app is closed
Meta says that for tasks that take more time, Muse keeps working after people close the app, and comes back when something changes or when it needs approval, like before it sends an email or makes a purchase. Reuters reports that the VM (Virtual Machine, an isolated computer running in the cloud) enables Muse to keep carrying out requests in the background even when a person is not actively using it.
## Walkthrough: how an email task moves through the VM
In simple steps using only what the sources say: the person connects an email app and chooses how much access Muse gets. Muse lives inside that person's own cloud computer with the stored data and login details. Muse drafts or plans the email work in the background, even after the app is closed. Before anything sensitive such as sending the email, Muse checks back for approval. The person can later review the complete audit trail, which is a full list of what Muse did and plans to do. A separate Sentinel agent on the same machine also checks planned actions, as described in [[03-sentinel-permissions|Sentinel Permissions]].
## Walkthrough: selling a car without exposing logins
Meta gives selling a car for more as an example of better results with less effort. Inside the VM pattern, Muse can open its visible browser, fill out sale forms, and negotiate on the person's behalf. Passwords the person types into that browser go into secure storage that Muse can use without seeing. Link built by Stripe handles checkout with a one-time-use card so real card details stay hidden. Meta says Muse shows the audit trail and asks before sensitive steps such as sending messages or paying. Shop Pay and 1Password login support are described by Meta as coming soon, not shipped now.
## What each usable source says about the VM
| Source | VM detail it provides |
|---|---|
| Meta official announcement | Dedicated Secure VM per person, contained isolation, houses agent plus data, secure credential storage, audit trail, background work |
| Axios press report | Dedicated virtual machine in Meta cloud, built-in browser visible to user, VM designed to be private to each person although on Meta infrastructure |
| Reuters wire report | Each agent on its own virtual machine defined as cloud emulation of a personal computer, background work continues, separate monitoring agent |
| NYT (New York Times, a United States newspaper) note | No VM claims used, because direct retrieval was blocked by paywall controls |
## Exact words worth keeping
Meta says Muse runs on its own dedicated computer in the cloud, contained so no one else's agent can reach it. Meta says that is where Muse lives and where the data and credentials for any service a person connects are securely stored. Meta says Muse has no visibility into people's passwords or payment methods. Axios says the agent runs on a dedicated virtual machine in Meta cloud, using a built-in browser that is visible to the user. Reuters calls the VM a cloud-based emulation of a personal computer that keeps carrying out requests in the background.
## Why a new kind of secure computer
Meta says personal agents need a new kind of secure computer, so it built one for everyone.
The reason in the sources is that Muse holds real logins, money details, and daily app data.
A normal chatbot only answers, so it does not need to store those secrets.
Muse must act across apps, keep working in the background, and remember personal details.
That is why Meta gives each person a contained cloud computer instead of a shared chat window.
Axios adds that the product was long in development under chief AI officer Alexandr Wang.
## Person stays in control of connections
Meta says each person stays in control of their Muse and decides how much access it gets.
People choose which apps Muse connects to and exactly how much access it gets.
For email, people choose what Muse can do, whether it reads mail or can also send for them.
People can change access or disconnect a service whenever they want.
Reuters confirms people choose connected apps and can revoke, meaning take away, access anytime.
Axios adds permissions can be narrowed to one task, service, transaction, or time period.
## Deep links to safety design
Meta points to two longer explainers for readers who want more.
One is How We Built Safety Into Muse, hosted at security.muse.ai.
The other is How We Designed Muse, hosted at introducing.muse.ai.
These links are listed in the official announcement Takeaways section.
They are not summarized in the usable sources, so this page makes no claims about their contents.
For approval logic inside the VM, see [[03-sentinel-permissions|Sentinel Permissions]].
For ad separation, training choice, and the locked future VM, see [[04-privacy-and-confidential-vm|Privacy and Confidential VM]].
## Shipped now versus promised later for the VM
| Timing | Status from the sources |
|---|---|
| Shipped now | Own cloud computer per person, isolated storage, hidden-credential use, visible browser, audit trail, background work after app is closed |
| Promised later this year | Muse Confidential VM, where the whole VM including data and chats is locked with a key only the person holds so not even Meta can access it |
| Still to come without a date in sources | Shop Pay payments and 1Password login support inside the same VM workflow |
| Source with no VM claims | NYT note, skipped because direct retrieval was blocked and no claims are used |
**Covers:** source 01 Built to be Private Safe and Secure bullets 1, 3, 4 plus How It Works background-work passage; source 02 dedicated VM plus visible browser plus private-to-each-person passage; source 03 own-VM background-work passage plus separate-agent authorization passage.
