> [[index|Wiki]] | [[summary|Summary]]

# Build-Time vs. Run-Time: Why Dev Tools Fail in Production — In Plain Language

## What is this about?

Imagine you hire an intern to help run your office. On day one, while you're standing right next to them, you might hand them a master key that opens every door — the supply closet, the server room, the CEO's office — because you're watching, and if they try to walk into the wrong room you can stop them. That's fine while you're supervising. But now imagine you leave that same intern alone at the front desk, dealing with the public, still holding that master key. Anyone who talks to them nicely enough — or tricks them cleverly enough — could get them to open any door in the building. That's the whole talk in one picture.

The "intern" here is an AI agent: a computer program that can read a request, decide what to do, and take actions on its own (as opposed to a plain chatbot that only replies with text). One of the main things agents do is call "tools" — small, pre-built actions someone has wired up for them, like "look up a customer" or "run this database search." MCP, which stands for Model Context Protocol, is simply a standard, plug-and-play way of connecting an agent to a set of these tools, a bit like a universal socket that lets any agent plug into any toolbox. This talk, given by two Google engineers who build a popular MCP toolbox for databases, is about a mistake they see teams make over and over: building a tool that's meant for a supervised developer to use while testing, and then accidentally shipping that same tool, unsupervised, straight into a live product used by real customers.

The core lesson is that a tool's safety depends entirely on who is using it and how much freedom it has. A flexible, "do-anything" tool is great in a lab with a human watching every step, and dangerous the moment no one is watching. The talk walks through what goes wrong when that mistake happens, and then shows how to fix it by taking freedom away from the agent, piece by piece, until it can only do one safe, narrow thing.

## Why does it matter?

In everyday terms: companies are increasingly letting AI agents act as customer-facing "employees" — answering questions, booking things, canceling orders, looking things up in a company database. If the tool you gave that AI employee is really a raw, unrestricted "do anything to the database" tool (the kind a developer uses while debugging), then a rude or clever customer could talk it into doing something disastrous — like deleting company records — the same way someone could sweet-talk that intern into opening the wrong door.

If this problem is solved properly, it means AI agents can be trusted with real customer interactions and real data, without a human standing over their shoulder for every single click. Get it wrong, and you get real damage: data leaked to people who shouldn't see it (like everyone's salary), or data destroyed outright. The talk even opens with a real demonstration of an agent being talked into deleting an entire database table because nobody had put any safety rails around the tool it was using.

## How does it work?

Here is the core idea as a step-by-step walkthrough, using the "keys to the office" analogy throughout.

1. **Start with the dangerous, all-purpose tool (the master key).** In its rawest form, a database tool gives the agent the actual login credentials, server address, and the ability to write and run any command it wants (in database terms, any SQL — the language used to ask a database questions or make it change data). This is exactly like handing someone a master key: powerful, but if the wrong person ends up holding it, they can open every door in the building.

2. **Lock the master key in a safe, out of the intern's hands (move connection details away from the agent).** The first fix is to stop letting the agent see the "master key" at all. The actual database address and password get stored separately, configured by a human ahead of time, and quietly plugged in behind the scenes. The agent never touches them directly — like the intern working from a front desk while the actual master keys live in a locked drawer only the building manager can open.

3. **Put up "keep out" signs on specific rooms (read-only limits, allowed areas, size caps).** Next, you restrict what can happen even with the doors that remain open: some doors can only be looked through, not walked into (read-only access — the agent can view data but not change it); certain rooms are off-limits entirely (limiting which parts of the database can be touched at all); and even in rooms the intern can enter, you cap how many boxes they're allowed to carry out at once (limiting how much data a single request can return). This shrinks the damage possible even if something goes wrong — engineers call this reducing the "blast radius," the size of the mess one bad action can cause.

4. **Give the intern a single labeled key instead of a master key (fixed, pre-written actions).** Instead of letting the agent write its own instructions from scratch (raw SQL), you pre-write the exact instruction ahead of time and just let the agent fill in a couple of blanks, the way a pre-approved form has one blank line for a date but the rest of the form is fixed and can't be altered. This also uses a technique called a "prepared statement," which checks that whatever the agent fills in is the right type of value (a date is really a date, not a hidden extra instruction), which is exactly what stops a classic hacking trick called SQL injection — smuggling commands inside what should be a harmless piece of text.

5. **Rename the key by its purpose, not by what it opens ("cancel my order" instead of "run this database command").** Rather than exposing database language at all, you give the agent business-friendly, single-purpose tools like "cancel order" or "look up flights," which only need a couple of everyday inputs. The agent no longer needs to know or think about databases at all — like giving the intern a key labeled "supply closet" instead of a key labeled "master."

6. **Take away the intern's ability to claim who they are (remove identity from the agent's control).** The riskiest remaining ingredient is often "whose account is this for?" If the agent gets to say "this is user #4521," a sneaky customer could try to trick it into saying someone else's number. The fix is to have the surrounding application check the customer's identity itself first (the way a badge reader checks your ID card, not something you get to tell the guard yourself), and hand that verified identity straight to the tool — the agent never even sees or controls it.

7. **End state: a single labeled key that only opens one drawer (a "zero trust" tool).** After all these steps, the tool the agent is left holding takes just one harmless input, like a date, and does exactly one thing, for exactly the verified person in front of it. Even if someone fully tricks the agent, the worst they can get it to do is that one narrow, safe action — nothing close to a master key anymore.

The talk calls this end state "zero trust": rather than trusting the agent's judgment to behave well, the surrounding system is designed so that misbehavior simply isn't possible, no matter how convincing the trick.

## Where can this be used?

- **Customer service chatbots** for banks, airlines, retailers, telecoms — anywhere an AI agent handles requests like "cancel my subscription" or "change my flight," this same "shrink the tool down to one safe action, tied to the verified user" pattern applies.
- **Internal IT and support agents**, like the "ticket triage" example in the talk, where an agent reads incoming tickets and looks things up in internal systems — a reminder that internal automation is not automatically safe just because it's "inside the company."
- **Any AI feature that touches a database, file system, or company API** — not just SQL databases; the same build-time-vs-runtime distinction applies to agents that read files, send emails, or hit external services, since the same three ingredients (private data, an untrusted request, and a way to send data back out) can cause a leak in any of those settings, not only databases.
- **Beyond AI entirely, this is a general lesson about giving less-supervised systems less power** — the same logic explains why, for example, you'd give a junior employee a company card with a $50 limit instead of full signing authority, or why building access badges are scoped to only the floors someone actually needs.

## Conclusions & takeaways

- The single sentence to remember a month from now: **a tool that's safe with a human watching is not automatically safe once you remove the human — shrink its powers before you do.**
- "Build-time" tools (flexible, powerful, meant for a supervised developer) and "runtime" tools (narrow, fixed, meant for an unsupervised agent facing real customers) are different things and should never be the same tool.
- Security should live in the tool and the surrounding system, not in hoping the AI "behaves" — because, as the speakers put it, an agent is still fairly easy to trick, no matter how advanced it seems.
- Two honest limitations of the talk worth flagging: (1) the live demo meant to show a *safe*, well-designed tool refusing to be tricked failed to load on video during the talk — the presenters only described it verbally from slides, so the audience never actually saw the "good" outcome happen live (only the earlier "bad" outcome, the accidental deletion, was shown as a real recorded failure); and (2) the specific mechanisms described (the "source" concept, bound and authenticated parameters, and so on) are specific to Google's own MCP Toolbox for Databases product — other tool platforms may implement the same general idea differently, or not offer all these safeguards out of the box.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| MCP (Model Context Protocol) | A shared, standard way to connect an AI agent to a set of tools — like a universal plug that works with many different sockets, instead of each agent needing its own custom wiring. |
| Agent | A computer program that can read a request and decide, on its own, which actions ("tools") to take to handle it — more autonomous than a chatbot that only replies with text. |
| Tool | A specific, pre-built action an agent is allowed to call, such as "look up a flight" or "cancel an order" — like a labeled key that opens exactly one door. |
| NL2SQL (Natural Language to SQL) | Letting the agent turn a plain-English question ("who bought coats and returned them?") directly into its own raw database command — powerful and flexible, but risky if unsupervised. |
| Confused deputy attack | Tricking a trusted helper (the agent) into misusing its own legitimate permissions to do something the person asking was never allowed to do themselves — like sweet-talking a security guard into opening a door for you using their own badge. |
| Lethal trifecta | The three ingredients that together cause a data leak: the agent has (1) access to private data, (2) exposure to untrusted instructions (e.g., hidden in a message it reads), and (3) a way to send information back out to someone. |
| Prepared statement / SQL injection | A "prepared statement" checks that each piece of information filled into a fixed instruction is the right, harmless type of value; "SQL injection" is the hacking trick of sneaking hidden extra commands inside what looks like ordinary text, which prepared statements block. |
| Bound parameter | A value (like a user's identity) that the surrounding application verifies and attaches to a request itself, so the agent never sees or controls that value at all. |
| Authenticated parameter | Similar idea, but here the tool is handed a signed, tamper-proof digital token proving who the user is, checks that the token is genuine, and reads the identity from it — rather than trusting a value the agent typed in. |
| Zero trust | A design philosophy where the system never assumes any part of it (including the AI agent) will behave correctly, so every request is independently checked and narrowed down, no matter how trustworthy that part seems. |
| JWT / OpenID token | A JWT (JSON Web Token) is a small, digitally signed piece of data proving "this really is user X" that can't be faked or edited without detection; OpenID is a common standard for issuing these identity tokens after someone logs in. |
| Blast radius | How much damage one bad or tricked action can cause — a small blast radius means even a successful trick only breaks one small, contained thing. |
