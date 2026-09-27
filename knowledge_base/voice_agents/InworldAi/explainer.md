> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# api-evangelist/inworld-ai — In Plain Language

## What is this about?

This repository is not software you install or run.

It is an independent, third-party profile of Inworld AI's public
voice-AI platform, maintained by API Evangelist. Think of it as a
librarian's index card: it does not serve the meal, it tells you
what is on the menu and where to order.

The "menu" here is Inworld AI, a company offering real-time voice
infrastructure — technology that lets computers listen and speak
like people do.

The profile catalogs five related services behind one API surface
and one billing relationship:

- Text-to-speech: turns written words into spoken voice.
- Voices: creates and manages custom voices.
- Speech-to-text: turns spoken words into written text.
- Realtime: the full live loop — listen, think, and speak back.
- Chat completions: question-answering through an LLM Router
  that speaks OpenAI- and Anthropic-compatible dialects.

The repo itself holds only text and machine-readable descriptions
of those services, assembled from material any member of the public
could reach with a browser and no login.

## Why does it matter?

Choosing a voice provider means answering hard questions: how good
do the voices sound, can I clone a voice, will it keep up with a
live conversation, what happens to my users' voice data, and how
much rewriting will my existing code need?

This profile gathers those answers in one place, in a standard
format that both people and automated tools can read.

It also matters because it is honest about its standpoint. It says
plainly: this is not Inworld's own API, just an outside observer's
notes. The recorded position is Consuming with third-party access,
so you know you are reading a customer's-eye view, not a sales pitch.

Finally, it grades what it found. An independent Tier-1 Consuming
review scores how complete and machine-readable the public paperwork
is — a useful shortcut before you dive into the full documentation.

## How does it work?

The profile works in three layers: collect, organize, and judge.

First, it collects public facts about Inworld's text-to-speech,
voice, speech-to-text, realtime, and chat-completion services —
models, endpoints, features, docs links, and pricing signals.

Second, it organizes those facts as structured files. A catalog file
declares each of the five services with its name, description, and
links. Each service points at a per-service OpenAPI description plus
shared extras: an AsyncAPI file for live connections, a JSON Schema
file for data shapes, and a JSON-LD file for data meanings.

Third, it records how every file was made and what the reviewer
thought. A provenance manifest labels each artifact as harvested
(fetched from the provider as-is), derived (split or generated from
another file, such as path-subset OpenAPIs or collections), or
unknown (no authorship record). Then the review weighs strengths —
one base URL and bill, drop-in OpenAI and Anthropic compatibility,
cloning with lip-sync alignment, open-source and on-premise speech
options, public indexes — against weaknesses such as reconstructed
specs and a narratively documented realtime protocol.

## Where can this be used?

This kind of profile helps wherever someone must evaluate or connect
to voice AI without writing code first.

A product team can shortlist Inworld for a voice agent, a talking
game character or avatar, a language-learning app, an AI companion,
or a phone assistant reached through a telephony integration.

A developer can see at a glance that one surface covers speech
output, speech input, live conversation, and access to outside
language models — so code already written for popular standards
can switch over with little rewriting.

An organization with strict privacy needs can spot the signals that
matter: zero-data-retention and on-premise options for regulated
workloads, plus word-level timing and phoneme detail for lip-synced
characters.

And an automated assistant or catalog tool can read the structured
files directly to answer "what can this API do?" without scraping
web pages.

## Conclusions & takeaways

The big picture is simple: an outside observer's structured guide
to a live voice-AI platform, not a replacement for it.

It does not run anything itself. It points at Inworld's services,
describes them in standard formats, shows its derivation chain,
and grades how complete and machine-readable the public surface is.

Its strengths are unity and openness: five capabilities behind one
surface and bill, familiar compatibility doorways, cloning plus
design with alignment detail, and openly published indexes.

Its limits are equally clear: the specs are partly reconstructed
rather than provider-published, the realtime live protocol is told
as a story rather than a machine-readable contract, and some
housekeeping pages are hard to find.

Use it as a starting map, then confirm the live details in Inworld's
own docs before you build or buy.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| API surface | The public doorways programs use to talk to a company's service. |
| Third-party profile | Notes about a product written by an outsider, not the company itself. |
| Text-to-speech (TTS) | Technology that reads written text out loud in a natural voice. |
| Speech-to-text (STT) | Technology that listens to speech and writes down the words. |
| Realtime / speech-to-speech | A live loop that listens, thinks, and speaks back with little delay. |
| LLM Router | A switchboard that forwards your question to one of many AI models. |
| Voice cloning | Making a computer voice that sounds like a specific real person. |
| OpenAPI / AsyncAPI | Standard instruction manuals: one for simple requests, one for live streams. |
| Provenance | A record of where each file came from and how it was made. |
| Tier-1 Consuming review | An outsider's top-grade verdict, written from a customer's viewpoint. |
