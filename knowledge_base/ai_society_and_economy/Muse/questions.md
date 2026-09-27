---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Muse

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. When was Muse announced and what distinguishes it from a chatbot that only answers questions?
> [!tip]- Answer
> Meta announced Muse on September 8, 2026 as a personal agent that does work across apps rather than only answering. Examples include sending email, booking travel, filling forms, and negotiating on a person's behalf. See [[wiki/01-announcement-and-capabilities|Announcement and Capabilities]].

### Q2. What is Muse Secure VM and what three things does it store?
> [!tip]- Answer
> Muse Secure VM is a dedicated per-person cloud computer that is contained so no other agent can reach it. It stores the Muse agent, the person's data, and credentials for connected services. See [[wiki/02-secure-vm-architecture|Secure VM Architecture]].

### Q3. How does Sentinel control Muse's internet access and what are its three possible outcomes?
> [!tip]- Answer
> Sentinel is a separate agent on the same machine, kept apart at the system level, and nothing Muse does reaches the internet unless Sentinel approves it. Sentinel allows an action, blocks it, or sends it to the person for approval. Sensitive actions such as sending email or making a purchase require approval. See [[wiki/03-sentinel-permissions|Sentinel Permissions]].

### Q4. What are Muse's launch availability and pricing tiers by exact price?
> [!tip]- Answer
> At launch Muse is US-only on iOS, Android, muse.ai, and WhatsApp, with AI glasses support coming soon. It has a free tier for most needs plus $20 per month and $100 per month plans for heavier use and power users to cover compute costs. See [[wiki/05-pricing-and-availability|Pricing and Availability]].

### Q5. Why does the default training setting matter for privacy, and what does the promised Confidential VM add?
> [!tip]- Answer
> By default Meta can use queries to its models for training unless the person turns the opt-out on, so privacy requires action. Today chats are kept out of ad systems and memory can be erased with forget, but the VM still runs on Meta infrastructure. The promised Confidential VM later this year would encrypt the whole VM with a user-held key so not even Meta can access it. See [[wiki/04-privacy-and-confidential-vm|Privacy and Confidential VM]].

### Q6. Why does Muse not ask for approval on every action, and what breaks if approval gates are removed or overused?
> [!tip]- Answer
> Muse requires approval for sensitive actions while letting approved lower-risk tasks proceed, because asking too often causes reflexive approval without thought and weakens safety. Without gates, Muse could send messages, pay, or upload sensitive data without permission, as seen in test reports of unapproved uploads. The audit trail of everything done and planned is the backstop for review. See [[wiki/03-sentinel-permissions|Sentinel Permissions]].

### Q7. A freelancer wants Muse to read invoices by email, negotiate a lower vendor bill, and pay if savings exceed $200. How should access and approvals be scoped?
> [!tip]- Answer
> Give read-only email access first, then narrow write scope to that vendor, transaction, and time period, with Link one-time-use cards hiding real card details. Sentinel allows low-risk research to proceed but routes the negotiation message and payment for explicit approval before reaching the internet. Afterwards check the audit trail to verify what was done. See [[wiki/02-secure-vm-architecture|Secure VM Architecture]].

### Q8. Was launching Muse on September 8 despite internal data-mismanagement concerns and mixed tests justified by the minimum-bar claim?
> [!tip]- Answer
> Reuters reports Meta delayed from April to cross the threshold for safety, security, privacy, and performance, yet testers still reported disconnects, unapproved uploads, and an alleged iCloud photo exposure. Shah says it is impossible to promise zero mistakes while claiming every part aims to be as safe and private as possible. The evaluation turns on whether honeymoon-planning usefulness outweighs ongoing risks of approval fatigue and ever-wider data access. See [[wiki/06-press-critique|Press Critique]].
