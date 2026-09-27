> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# So, you've looked into AI phone

**In one sentence:** Because the number of AI phone-caller platforms is overwhelming, this video compares seven platforms — Vappy, Retail, Synflow, Bland, 11 Labs, Voice Flow, and Vogent — across sound, speed, cost, and integrations so the viewer knows which one fits them best.

## Key points

- The comparison covers seven platforms — Vappy, Retail, Synflow, Bland, 11 Labs, Voice Flow, and Vogent — in four categories: sound, speed, cost, and integrations.
- Sound depends most on the AI speech model chosen; the presenter's poll of a free school community found the top three providers in use were 11 Labs, Cartisia, and Rhyme.
- Vapy, Retail, Sinflow, and Voice Flow use existing speech providers, while Vappy/Bappy also has its own provider alongside Bland, 11 Labs, and Vogent; Vapy's own phone-trained voices are rated best-sounding but limited to a few American-accent voices.
- Speed was tested with 10 real phone calls per platform over Twilio using GPT-4o, default settings, the same system prompt and transcriber, the same 11 Labs voice where supported, and default custom voices elsewhere.
- Average response latency ranked: Retail AI 1.79s, Synflow 1.88s, Vappy 1.91s, Bland AI 2.5s, 11 Labs 2.6s, Voice Flow 2.7s, and Vogent 3.6s.
- Standard cost per minute ranked: Voice Flow 8 cents (plus required $60/month subscription), Bland and Vogent 9 cents, Vapy, Retail, and 11 Labs 12 cents, and Synflow 13 cents, before enterprise/volume discounts or model changes.
- Integrations differ by native SMS (Retail, Vapy, Bland; only Retail supports two-way SMS), calendar booking (Retail, Vapy, Sinflow, Voice Flow support Cal.com or Google Calendar), and CRM (Vappy, Synflow, Bland support Go High Level; Sinflow and Bland support HubSpot or Salesforce; 11 Labs supports only API calls built from scratch).
- Technically, Vapy is the most developer-centric platform with custom LLMs and broad LLM/speech/transcriber provider support, while Synflow is the most agency-focused with white-labeling and native workflow automations and mostly hidden model settings.

---

## Intro: which platform should you choose

The chunk opens on choice overload: *"So, you've looked into AI phone callers and have discovered an overwhelming number of platforms and you're not quite sure which one should you choose. Which one sounds the best, which one is the quickest, which one is the cheapest, and which one has the most integrations."* The promised payoff is: *"by the end of this video, you'll know exactly which platform is best for you."* The presenter identifies himself as Brendan Jawat, based in Melbourne, Australia, running the agency Inflate AI for over 2 years helping businesses integrate AI voice agents, and notes all test calls and data are linked in a CSV file below, plus a free school community (over 15,000 members) and his new simulation/evaluations software Reliable.

## Sound: speech models matter most

The presenter states the most significant sound factor is the AI speech model chosen, since many platforms assemble agents from multiple external providers — e.g. multiple compared platforms support 11 Lab Speech, distinct from the 11 Labs conversational-agents platform. He demos 11 Labs, Cartisia, and Rhyme default voices on the same real-estate script (Emily from Inflate Real Estate Services, 123 Main Street, John Smith / first-home-buyer walkthrough booking) and asks viewers to comment which sounded best, warning that each provider offers many voices/accents of varying quality so extensive voice testing is essential. Pitfalls of a bad voice are quality and speed: for casual phone calls a more monotone voice feels more realistic than movie-trailer/ebook-style expressive voices, partly controllable via voice temperature (expressiveness), though best to pick a voice that sounds right by default; speaking speed in words per minute should be neither too fast nor painfully slow. Standouts with custom models: Vapy's own uploaded voices, trained specifically for phone calls versus audiobook/marketing-recorded voices like 11 Labs', sound "pretty awesome" but offer only a few American-accent choices; 11 Labs, Bland, and Vogent custom voices all sounded quite similar to the first models showcased, with per-platform recordings in the linked spreadsheet.

| Platform | Speech source per chunk table |
|---|---|
| Vapy | Existing providers |
| Retail | Existing providers |
| Sinflow | Existing providers |
| Voice Flow | Existing providers |
| Bappy / Vappy | Own provider (alongside existing-provider support) |
| Bland | Own custom voice |
| 11 Labs | Own custom voice |
| Vogent ("Virgin"/"Vent" in transcript) | Own custom voice |

## Speed: latency test setup and results

Speed/latency is framed as second only to sound for call realism, since slow AI causes frustration. Most platforms default to similar LLMs — GPT-4o (cited as a good overall model and used for the whole comparison), Google Gemini, Anthropic Claude, and xAI Grok — which drive response speed/intelligence more than any other single setting. Test controls: GPT-4o everywhere, same 11 Labs voice where supported (default custom voices where not), real phone calls via a Twilio number each, default settings including transcriber model, same system prompt, 10 test calls per platform.

| Rank | Platform | Avg. response latency |
|---|---|---|
| 1 | Retail AI | 1.79 seconds |
| 2 | Synflow ("Syninflow") | 1.88 seconds |
| 3 | Vappy | 1.91 seconds |
| 4 | Bland AI | 2.5 seconds |
| 5 | 11 Labs | 2.6 seconds |
| 6 | Voice Flow | 2.7 seconds |
| 7 | Vogent ("Vogen") | 3.6 seconds |

The top three are described as "incredibly close," with settings tweaks able to make any agent quicker; Bland is "quite a jump up from Vappy."

## Cost: per-minute pricing

Every platform charges per minute the agent speaks over the phone, plus some require a platform subscription. Ordered by standard-rate cost per minute with default model settings:

| Rank | Platform | Cost per minute |
|---|---|---|
| 1 | Voice Flow | 8 cents + $60/month subscription required |
| 2 | Bland | 9 cents |
| 2 | Vogent | 9 cents |
| 4 | Vapy | 12 cents |
| 4 | Retail | 12 cents |
| 4 | 11 Labs | 12 cents |
| 7 | Synflow | 13 cents |

Costs are "very similar" overall, changeable via AI-model and other settings, and reducible via enterprise plans and larger call volumes; only standard rates are compared, and call volume determines how much per-minute cost dominates.

## Integrations: SMS, calendar, CRM, and technical flexibility

All platforms support API calls (direct CRM requests or automation via Make.com / n8n), but native integrations save agency rebuild time. SMS: Retail, Vapy, and Bland have native SMS sending (confirmations, links); only Retail supports two-way SMS, i.e. converting voice agents into SMS text agents without other platforms. Calendar (one of the most requested): Retail, Vapy, Sinflow, and Voice Flow have pre-created Cal.com or Google Calendar booking/availability functions. CRM: Vappy, Synflow, and Bland natively integrate Go High Level; Sinflow and Bland support HubSpot or Salesforce; 11 Labs allows only API calls, so those CRM links must be built from scratch. Technical split: developer-centric versus agency-centric — Vapy is most developer-centric (custom LLMs, support for almost all LLM/speech/transcriber providers, every option exposed); Synflow is the opposite, agency-focused (built-in white-labeling and native workflow automations, model settings largely hidden) — neither inherently bad, depending on technical expertise and whether the goal is hosting for businesses, app integration, or handover.

**Covers:** Chunk 01-so-you-ve-looked-into-ai-phone (video intro plus four-category framing: sound, speed, cost, integrations)
