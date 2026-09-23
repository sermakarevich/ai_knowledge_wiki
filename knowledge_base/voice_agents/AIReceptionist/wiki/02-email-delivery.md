[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Email delivery
**In one sentence:** Email delivery is enabled via a top-level `email` section with SMTP or Resend senders and `on_message` / `on_call_end` / `on_booking` triggers, sitting alongside multi-language support, retention sweeps, multi-business routing, per-minute costing, calendar booking, and SIP transfer overrides.
## Key points
- Email is configured in a top-level `email` section with `from: "receptionist@acmedental.com"` and a `sender` of type `smtp` (host `smtp.gmail.com`, port 587, `use_tls: true`, `${SMTP_USERNAME}` / `${SMTP_PASSWORD}`) or `resend`.
- Two email triggers are shown in the chunk: `triggers.on_message: true` (email when `take_message` fires) and `triggers.on_call_end: false` (email a summary after every call), plus optional `email.triggers.on_booking: true` to email staff whenever a calendar booking lands.
- `gpt-realtime-2.1` auto-detects the caller's language and continues in it when whitelisted (`primary: "en"`, `allowed: ["en", "es", "fr"]`), otherwise politely redirects in `primary`.
- Retention is configured as `recordings_days: 90`, `transcripts_days: 90`, `messages_days: 0` (0 = keep forever), swept on a schedule via `python -m receptionist.retention sweep` (or `--dry-run` preview), and the sweeper never touches `.failures/` directories.
- One agent process serves multiple businesses: each inbound number maps via SIP dispatch-rule metadata `{"agentName": "receptionist", "metadata": "{\"config\": \"my-business\"}"}` to `config/businesses/my-business.yaml`.
- Realtime is authenticated with a standard `sk-...` OpenAI API key and billed per audio minute at an estimated ~$0.20-0.30/minute (e.g. 10 calls/day x 2 min ≈ ~$5/day / ~$150/month; 30 x 2 min ≈ ~$15/day / ~$450/month; 60 x 1.5 min ≈ ~$22/day / ~$660/month), with no AIReceptionist platform fee or markup.
- Google Calendar booking adds `check_availability(preferred_date, preferred_time)` (up to 3 slots near the requested time) and `book_appointment(caller_name, callback_number, proposed_start_iso, notes?, caller_email?)` tools, with the agent reading the proposed time back for a "yes", tagging events UNVERIFIED, and adding `caller_email` as an OPTIONAL Google attendee that does not affect organizer free/busy on decline.
---
## Email delivery
Enable the top-level `email` section when using an email channel or `on_call_end` trigger:

```yaml
email:
  from: "receptionist@acmedental.com"
  sender:
    type: "smtp"   # or "resend"
    smtp:
      host: "smtp.gmail.com"
      port: 587
      username: ${SMTP_USERNAME}
      password: ${SMTP_PASSWORD}
      use_tls: true
  triggers:
    on_message: true    # email when take_message fires
    on_call_end: false  # email a summary after every call
```

## Multi-language
```yaml
languages:
  primary: "en"
  allowed: ["en", "es", "fr"]
```

`gpt-realtime-2.1` auto-detects the caller's language. If the caller speaks one of the allowed languages, the agent responds in that language for the rest of the call. If the caller speaks an un-whitelisted language, the agent politely redirects in `primary`.

## Retention
```yaml
retention:
  recordings_days: 90
  transcripts_days: 90
  messages_days: 0       # 0 = keep forever
```

Run on a schedule (cron / Windows Task Scheduler):

```bash
python -m receptionist.retention sweep


# or preview
python -m receptionist.retention sweep --dry-run
```

The sweeper never touches `.failures/` directories.

## Multi-Business Setup
One running agent can serve multiple businesses. Each inbound phone number maps to a business config via the agent metadata on its SIP dispatch rule:

```json
{
  "agentName": "receptionist",
  "metadata": "{\"config\": \"my-business\"}"
}
```

This loads `config/businesses/my-business.yaml`. Add as many business configs as you need -- one agent process handles them all.

## Cost
You authenticate Realtime with a standard OpenAI API key (`sk-...`) and pay OpenAI Platform usage directly, metered per audio minute. (A ChatGPT/Codex OAuth subscription path previously powered Realtime, but OpenAI's 2026-06-03 Realtime Beta sunset disabled OAuth for Realtime — an API key is now required.) There is no AIReceptionist platform fee or markup.

**Estimated cost:** ~$0.20-0.30 per minute of conversation.

| Business type | Calls/day | Avg duration | Daily cost | Monthly cost |
|---|---|---|---|---|
| Small office | 10 | 2 min | ~$5 | ~$150 |
| Dental practice | 30 | 2 min | ~$15 | ~$450 |
| Busy front desk | 60 | 1.5 min | ~$22 | ~$660 |

> "Compare that to a SaaS AI receptionist at $300-500/month that sounds worse and gives you zero control. At higher call volumes the per-minute model costs more, but you get dramatically better quality and full ownership of the system. For most small-to-medium businesses, the cost is comparable or lower -- and the experience for your callers is not even close."

## Appointment booking (Google Calendar)
Each business can optionally enable Google Calendar integration for in-call booking:

```yaml
calendar:
  enabled: true
  calendar_id: "primary"
  auth:
    type: "service_account"  # or "oauth"
    service_account_file: "./secrets/<business>/google-calendar-sa.json"
  appointment_duration_minutes: 30
  buffer_minutes: 15
  buffer_placement: "after"
  booking_window_days: 30
  earliest_booking_hours_ahead: 2
```

When enabled, the agent gets two new tools:
- **`check_availability(preferred_date, preferred_time)`** — queries the calendar and returns up to 3 slots near the requested time
- **`book_appointment(caller_name, callback_number, proposed_start_iso, notes?, caller_email?)`** — books one of the offered slots. When `caller_email` is provided, the caller is added as an OPTIONAL Google attendee and Google sends them the standard `.ics` invite. Optional attendees don't impact the organizer's free/busy if they decline.

The agent always says the proposed time back to the caller and waits for "yes" before booking. Events are tagged UNVERIFIED so staff know the caller's identity wasn't verified.

See `documentation/google-calendar-setup.md` for step-by-step setup of both auth paths (service account for Workspace, OAuth for any account).

Optional: set `email.triggers.on_booking: true` to email staff whenever a booking lands (uses the existing email channel).

## SIP transfer URI (Asterisk + non-standard PBX)
By default, transfer-to-DID uses `tel:{number}`, which works for Twilio, Telnyx, and most BYOC SIP trunks that translate tel-URIs to SIP. If your trunk is **Asterisk classic `sip.conf`** (chan_sip, not pjsip), it rejects tel-URIs — you'll see transfers fail. Add a `sip:` block to your business config to override the URI scheme:

```yaml
sip:
  transfer_uri_template: "sip:{number}"          # local DID lookup on Asterisk
  # transfer_uri_template: "sip:{number}@asterisk.local"  # remote PBX
```

The default (`tel:{number}`) is preserved for everyone else; the field is only needed when your trunk doesn't accept tel-URIs.

Credit to @trinicomcom (issue #6) for surfacing this.

---

## Alternatives This Replaces
This project is a direct, self-hosted, open-source alternative to:

- **Bland AI** -- AI phone calls API. Cascaded pipeline, closed source, per-minute pricing with platform markup.
- **Vapi** -- Voice AI platform. Another middleman between you and the model. Vendor lock-in.
- **Retell AI** -- Conversational voice AI. Same cascaded architecture, same latency problems.
- **Smith.ai** -- Virtual receptionist service. Expensive, limited customization, your data on their servers.
- **Ruby Receptionist** -- Live + AI receptionist. Premium pricing for a service you can run yourself.

> "If you are evaluating any of these, try this first. It is free to deploy, and the voice quality speaks for itself."

---

## License
**AGPL-3.0**

This project is licensed under the [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0.html).

> "This means: you can use it, modify it, self-host it, and deploy it for your business with no restrictions. But if you run a modified version of this code as a hosted service (i.e., you let other people interact with it over a network), you must release your modifications under the same license."

> "**Why AGPL and not MIT?** Because this license specifically prevents companies from taking this code, wrapping it in a SaaS product, and charging people a monthly fee without giving anything back. The whole point of this project is that you should not have to pay rent on software you can run yourself. AGPL ensures it stays that way."

---

## Support the Project
> "If this saved you from a $300/month SaaS subscription, consider buying me a coffee."

**BTC:** `bc1q573f3x6zlsh06lcfetpmrquw5jr5e26ahu4syn`

**ETH:** `0x5d48560C58b65dc7FeECa2F452c2Df817d1d61CC`

**Covers:** chunk 02-email-delivery (email delivery config with smtp/resend sender and on_message/on_call_end triggers; multi-language; retention sweep; multi-business setup; cost; appointment booking / Google Calendar with on_booking trigger; SIP transfer URI; alternatives; license; support the project)
