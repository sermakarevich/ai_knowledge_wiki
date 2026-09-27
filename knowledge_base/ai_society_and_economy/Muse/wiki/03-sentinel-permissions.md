> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Sentinel Permission Gate and User Control
**In one sentence:** A separate Sentinel agent checks what Muse wants to do online and only lets it through with approval, while the person stays in charge of access.
## Key points
- Sentinel is a separate agent that runs on the same machine as Muse but is kept apart at the system level.
- Nothing Muse does reaches the internet unless Sentinel approves it.
- Sentinel allows three outcomes: an action is allowed, blocked, or sent to the person for approval.
- Muse asks the person before sensitive actions such as sending an email or making a purchase.
- People can give read-only access, for example letting Muse read mail, or wider write access, for example letting it also send mail.
- Permissions can be narrowed to one task, service, transaction, or time period, and access can be changed or removed at any time.
- Meta executives said asking for approval too often can make people approve without thinking, so Muse asks for sensitive actions while lower-risk tasks already approved can go ahead.
- Muse shows a complete audit trail, meaning a full list of what it has done and what it plans to do.
---
## What Sentinel is
Sentinel is a separate agent that runs on the same machine as Muse. Muse is a personal Artificial Intelligence (AI) agent, meaning software that acts on a person's behalf. Sentinel is kept apart from Muse at the system level. Sentinel controls Muse's access to the internet and to connected services.
## How Sentinel approves actions
Muse can suggest an action, but Sentinel decides what happens next. Sentinel determines whether the action is allowed, blocked, or sent to the user for approval. Nothing Muse does reaches the internet unless Sentinel approves it. When needed, Sentinel asks the person for permission. A separate agent also monitors planned actions and in certain cases prompts Muse to seek authorization before carrying them out.
## Approval before sensitive actions
Muse checks with the person before sensitive actions like sending an email or making a purchase. For tasks that take more time, Muse keeps working after people close the app and comes back when it needs approval. Muse is designed to require approval for more sensitive actions while allowing previously authorized, lower-risk tasks to proceed.
## Read versus write access
People choose which apps Muse connects to and exactly how much access it gets. People can distinguish between read and write access. Read access means Muse can look, for example reading mail. Write access means Muse can act, for example sending mail on a person's behalf. People can set more granular, meaning more detailed, permissions within a service.
## Narrow and changeable permissions
Permissions can be narrowly scoped, meaning limited, to a particular task, service, transaction, or period of time. People can change access or disconnect a service whenever they want. People choose which apps it connects to and can revoke access at any time. Revoke means take away.
## Approval fatigue and audit trail
Meta executives said they were mindful that asking people to approve every small action can lead to them approving requests reflexively, meaning automatically without real thought, which can undermine safety. Muse shows people a complete audit trail of everything it has done and plans to do. Muse runs on its own dedicated Virtual Machine (VM), meaning a cloud-based emulation of a personal computer, contained so no one else's agent can reach it.
## Sentinel outcomes table
| Sentinel decision | What it means in plain language | Example from the sources |
|---|---|---|
| Allowed | Sentinel lets a previously approved lower-risk step go ahead | Continuing background work the person already approved |
| Blocked | Sentinel stops the action from reaching the internet | A planned action Sentinel judges not allowed |
| Sent for approval | Sentinel asks the person to decide | Before Muse sends an email or makes a purchase |
## Walkthrough: Sentinel and a dinner-party email
Take the dinner-party example Meta gives: Muse remembers friends' dietary restrictions and prepares invites. In Sentinel terms, Muse can suggest the invite text and plan the send. Sentinel then checks that plan against internet and service access. If sending mail needs explicit approval, Sentinel routes it to the person first. Nothing reaches the internet unless Sentinel approves it. Afterward the person can check the audit trail to see what Muse did and what it plans next. Lower-risk steps already approved can proceed without asking again.
## Walkthrough: Sentinel and selling a car or paying
For a car sale or a purchase, the stakes are higher because money and messages to strangers are involved. Meta says Muse can negotiate on the person's behalf, fill out forms, and check out with Link built by Stripe. Sentinel sits between Muse and the internet, so Muse suggests the payment or message while Sentinel decides whether it is allowed, blocked, or needs the person's approval. Meta says approval is required before sensitive actions such as sending an email or making a purchase. Credentials stay in secure storage that Muse can use without seeing, including passwords typed into the browser.
## Permission types table
| Permission idea | Plain meaning | Source wording |
|---|---|---|
| Which apps | Person picks connected services | People choose which apps Muse connects to |
| Read access | Muse can look but not act | Whether it reads mail |
| Write access | Muse can act on behalf of the person | Or can also send on their behalf |
| Narrow scope | Limit to one job, service, purchase, or time | Narrowly scoped to a particular task, service, transaction, or period of time |
| Change or remove | Person can adjust or cut access anytime | Change access, disconnect a service, revoke access at any time |
## Exact Sentinel words worth keeping
Meta says a separate Sentinel agent runs on that same machine, kept apart from Muse at the system level. Meta says nothing Muse does reaches the internet unless the Sentinel approves it, and it asks the person for permission when needed. Axios says Sentinel controls Muse's access to the internet and connected services, and that Muse can suggest an action, but Sentinel determines whether it is allowed, blocked, or sent to the user for approval. Reuters adds that a separate agent monitors planned actions and in certain cases prompts Muse to seek authorization.
## Sentinel lives on the same Sentinel-guarded machine
Sentinel runs on that same VM (Virtual Machine, an isolated computer running in the cloud) as Muse.
Same machine matters because checks happen close to where data and logins are stored.
Kept apart at the system level means Muse and Sentinel are separated inside that computer.
Meta presents this as a first-of-its-kind safety and security protection no other agent provides.
Reuters describes the same idea as a separate agent that monitors planned actions.
For the VM itself, see [[02-secure-vm-architecture|Secure VM Architecture]].
## Sentinel and connected app categories
Reuters says Muse can connect across email, calendar, payments, health, shopping, and the smart home.
Smart home here means internet-connected home devices such as lights or locks.
Sentinel controls Muse's access to those connected services and to the internet.
The person still decides which categories are connected at all.
Axios says permissions can be set with more detail within a single service.
That lets a person allow mail reading without allowing mail sending, for example.
## Sentinel walkthrough: honeymoon travel research
Reuters praises one tester case where Muse acted as the third participant on a three-week honeymoon in Indonesia.
The work included arranging travel plans and ground transport.
Ground transport means local cars, vans, or other travel on the ground.
In Sentinel terms, Muse could research options and prepare bookings in the background.
Sentinel would then check each outward step, allowing low-risk research and routing purchases or messages for approval.
Approval fatigue is the limit here: too many small prompts can make people approve without thought.
So Muse is designed to ask for sensitive steps while approved lower-risk work proceeds.
## Why Sentinel does not ask about everything
Axios reports executives were mindful that asking people to approve every small action can lead to approving reflexively, which can undermine safety. Reflexively here means clicking approve out of habit without real checking. The design answer in the sources is to require approval for more sensitive actions while letting previously authorized lower-risk tasks proceed. The audit trail is the backstop: Muse shows a complete list of everything it did and plans to do, so the person can review even steps that did not trigger a prompt.
**Covers:** 01-meta-official.md Built to be Private Safe and Secure bullets and How It Works approval passage; 02-axios.md Zoom in Sentinel and permissions passage; 03-reuters-syndicated.md app access revoke passage and separate-agent protection passage.
