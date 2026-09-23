> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# rusty4444/hermes-voice-ha-integration — In Plain Language

## What is this about?

This project connects two things that are each useful alone but much more useful together: Hermes Agent and Home Assistant.

Home Assistant is the program that already controls your house — your lights, switches, scenes, thermostats, and media players.
Hermes Agent is a smart assistant that can reason, answer questions, and use tools to get things done.

This integration is the bridge between them. It lets you talk to Hermes in plain English — by text or by voice —
and have it understand your home and actually change things in it.

You can ask "Is the kitchen light on?" and get a real answer based on the live state of your house.
You can say "Turn off everything except the living room lamp" and Hermes will do it.

The project comes in three pieces that work as a team:

- A Home Assistant add-in that teaches Home Assistant how to talk to Hermes.
- A set of home-control tools that teach Hermes how to read and control the house.
- A set of voice tools that add listening, speaking, and wake-word detection.

Think of it as giving your house a brain (Hermes), ears and a mouth (the voice tools),
and hands (the Home Assistant connection).

## Why does it matter?

Most smart homes today have a frustrating split.

On one side, Home Assistant knows everything about your house but is awkward to talk to.
On the other side, chat assistants are easy to talk to but know nothing about your home and cannot flip a single switch.

This project closes that gap. The assistant stops guessing and starts seeing:
which lights exist, which are on, what scenes are available, what just changed.

It also works in both directions, which is the part people miss.
Hermes can reach into Home Assistant to read and control devices,
and Home Assistant can reach out to Hermes as its conversation
brain — for example through the Assist voice/chat feature —
plus show Hermes health as simple status sensors on a dashboard.

Safety matters here too. Letting an assistant flip switches
in your home is powerful but risky, so the project includes
guardrails: blocked device types, an optional allow-list of
what Hermes may touch, and a log file recording every action.

Finally, it respects choice about privacy. You can run the whole
thing with cloud services for convenience, or swap in local,
offline pieces so your voice never leaves your house.

## How does it work?

Imagine the flow as a short chain with five links:

1. You speak or type a request, such as "Dim the living room lights."
2. Hermes Agent receives it and figures out what you mean.
3. Hermes picks the right home-control tool — for example,
   search for the right light, check its current state,
   then call the service that changes it.
4. Home Assistant carries out the action on the real device.
5. Hermes replies, optionally out loud through a speaker.

Under the hood, the three bundle pieces each handle one job:

- The Home Assistant side adds setup screens, action buttons,
  health sensors ("is Hermes connected?"), a small dashboard bar,
  and a WebSocket channel that carries voice events back and forth.
- The Hermes home-control tools (eight of them) cover searching devices,
  reading one device's state, calling a service, getting a compact
  summary of the whole home, discovering available services,
  and handy shortcuts like "control lights plus a scene,"
  "turn off everything except these," or "run several commands at once."
- The Hermes voice tools (six of them) cover checking the voice setup,
  turning always-listening mode on and off, speaking a reply,
  listening once and writing down what was heard,
  and building a voice-friendly prompt that includes home context.

Setup follows four everyday steps: install Hermes, create a
Home Assistant access token (a long password Hermes uses to log in),
install the two Hermes plugins and enter the house address and token,
then test with a safe question like "Search my lights."

The newest release (v0.0.14) focuses on reliability: safer handling
of simple built-in requests, cleaner recovery when the connection
drops, and a fix so settings reload correctly on recent
Home Assistant versions.

## Where can this be used?

Anywhere someone already runs Home Assistant and wants a more
natural way to live with it:

- Hands-free control in the kitchen, workshop, or garage — "turn off everything except the porch light"
  beats hunting for your phone with messy hands.
- Quick status checks from the couch or bed — "is the kitchen light still on?" or "give me a summary of the house."
- A family-friendly dashboard with a small action bar
  and health sensors, so everyone can see whether the assistant is up.
- Voice-first rooms where a wake word starts listening,
  the assistant thinks, and a speaker answers back.
- Tinkerer setups where one command runs many actions at once,
  such as an evening routine that dims lights, sets a scene,
  and turns off everything unneeded.
- Privacy-conscious homes that choose fully local pieces —
  a local assistant model, offline speech tools, and an open
  wake-word engine — so nothing is sent to the cloud.

What it is not: a replacement for Home Assistant itself,
or a magic fix for bad Wi-Fi, missing microphones, or speakers
Home Assistant cannot reach. It makes a working smart home
easier to talk to; it does not wire the house for you.

## Conclusions & takeaways

The big idea is simple: the assistant should see the house, not just chat about it.
Once Hermes can search devices, read live states, and call services safely,
plain English becomes a genuine remote control.

The second idea is direction: most add-ons only let the assistant
reach into the home. This one also lets the home reach the assistant,
so Home Assistant can use Hermes as its brain and report
on its health like any other device.

The third idea is caution by design. Blocked controls,
allow-lists, and an audit log mean you decide how much power
the assistant gets — wide open for experiments, tightly fenced
for a family home.

If you remember three sentences, remember these: it turns everyday language into safe home control;
it works by text today and by voice when you add the voice piece; and local-only operation is possible,
but you must pick the local options deliberately because the defaults favor ease.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Hermes Agent | The smart assistant program that understands language and uses tools. |
| Home Assistant | The popular program that monitors and controls smart-home devices. |
| HACS | The community app store that makes installing Home Assistant add-ins easy. |
| Entity | One single thing Home Assistant tracks, like "kitchen light" or "thermostat." |
| Service call | An instruction like "turn on" or "set brightness" sent to a device. |
| Scene | A saved mood — a preset combination of lights and settings recalled at once. |
| Wake word | A trigger phrase (like "hey house") that tells the system to start listening. |
| STT / TTS | Speech-to-text (hearing you) and text-to-speech (talking back to you). |
| WebSocket | An always-open phone line between two programs for instant back-and-forth updates. |
| Long-Lived Access Token | A long password Hermes shows Home Assistant to prove it is allowed in. |
