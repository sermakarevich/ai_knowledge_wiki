> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Smart Home Assistant Demo

**In one sentence:** The smart home demo evaluates every user request against a long list of questions — many speculative — in one parallel call and pairs TypeSafe with an LLM that splits compound requests and handles conversational fallback, so deterministic commands stay fast and cheap while open-ended chat still works.

## Key points

- The chief pattern demonstrated is speculative fan-out: each user request is evaluated against a long list of questions, including many that end up irrelevant for most requests.
- The worked request is "Turn off all of the lights in the house", for which code only needs four answers: request category (smarthome command), domain (whole house), device type (lights), and action on the lights (turn off).
- The lights-action question is speculative — written assuming a lights command and asked before knowing the request is one — so all questions evaluate in parallel and code filters out irrelevant results after the fact, handling a wide variety of requests with a single question set.
- The wrong way is sequential API calls (ask category, then domain/device only once it's known to be a smarthome command, then action only once lights are known): it minimizes question count but ends up much slower and more expensive than one upfront batched call.
- A Noul question detects whether the request asks for more than one distinct action; if true, an LLM splits it into atomic commands that TypeSafe evaluates individually.
- When TypeSafe determines the query is general information or conversation, the system falls back to a conversational LLM for a freeform response — deterministic behavior stays fast and cost-efficient while the LLM adds flexibility, and the initial TypeSafe response is so fast it adds negligible latency.
- The demo is a Vite/React single-page app using the TypeSafe API; full source will be available on GitHub at release, with local run instructions and a code-to-demo-part overview in its README.
- A demo video is embedded on the page ("Check it out in action").

---

## Check it out in action

The page embeds a demo video of the smart home assistant.

## How it works

### Speculative fan-out

> "Turn off all of the lights in the house"

This simple request needs only: "What category of request is this?" (smarthome command), "What domain is this request targeting?" (whole house), "What type of device is this request targeting?" (lights), "What action should be taken on the lights?" (turn off).

> "Notice that the last question is written with the assumption that the user is issuing a command to lights, and we ask it before we know what the user is actually requesting. This is what we call a 'speculative question' - we ask it before we even know if it's relevant, allowing us to evaluate all questions in parallel and rely on code to filter out the irrelevant results after the fact. This is a key pattern for building systems that can handle a wide variety of user requests with a single set of questions."

#### The wrong way: sequential API calls

Separating questions into multiple calls — category first, then domain/device only once it's a smarthome command, then action only once lights are targeted — optimizes for a minimum number of questions but is much slower and more expensive than batching everything into one upfront call.

### TypeSafe and LLM pairing

- **Splitting a compound user request:** a Noul identifies multi-action requests; when true, an LLM splits the request into atomic commands, each evaluated by TypeSafe individually.
- **Falling back to a conversational LLM:** general-information or conversational queries get a freeform LLM response, so known deterministic behavior stays fast and cost-efficient while generative flexibility remains available; the initial TypeSafe response adds negligible latency compared to the LLM response.

## Run it yourself

A simple Vite/React single-page app using the TypeSafe API to evaluate user requests. Full source code will be available on GitHub at release; its README includes local run instructions and an overview of which source bits drive which demo parts.

**Covers:** https://docs.typesafe.ai/demos/smart-home
