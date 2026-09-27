> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# StreamTN: A Low-Latency Streaming Chinese Text Normalization Model for Streaming TTS in Dialogue Systems — In Plain Language

## What is this about?

StreamTN is a small, specialized AI model that cleans up Chinese text
so a voice assistant can read it aloud correctly — and it does this
live, while the chatbot is still typing its answer.

The problem it solves is called *text normalization*. Chatbot replies
are full of shortcuts humans read easily but speech software cannot:
numbers, dates, times, phone numbers, money amounts, units like "kg",
and trickier things like chemical formulas (H2O) or math equations.
The same digits sound completely different depending on context —
"2024" can be a year, part of a phone number, or a quantity — and
guessing wrong means the voice says something silly or fails outright.

Existing fixes fall short. Hand-written rules are controllable but need
enormous manual effort and break on anything new. Asking a big general
chatbot to clean up text with clever instructions works, but it has to
wait for the whole reply, adds noticeable delay, and sometimes invents
words. StreamTN is a different answer: a lightweight model built on
Qwen3-0.6B that is trained specifically for this one cleanup job and
works incrementally, a few words behind the chatbot.

The authors also built a new test collection for this task: about
95,800 training examples and 1,262 carefully checked test examples
across 14 categories, including the scientific formulas and equations
that older test sets mostly ignored.

## Why does it matter?

In a modern voice assistant, three parts run in a chain: the chatbot
thinks of a reply, the normalizer rewrites it into speakable words,
and the speech synthesizer speaks it. The first and last parts already
work in streaming fashion — words flow through as they are ready.
The middle part was the bottleneck: old-style normalizers waited for
the full reply before starting.

That waiting is what users feel as dead air before the assistant starts
talking. For a real conversation, the first sound should come within a
few hundred milliseconds, not after the whole answer is finished.

StreamTN matters because it removes that bottleneck without giving up
quality. At its standard setting it matches the accuracy of the best
non-streaming neural model while starting to speak after only about
213 milliseconds of its own compute. It also generalizes better than
rule lists, because it learned patterns from data instead of relying
on hand-written cases, and it hallucinates less than a general chatbot
asked to do the job on the side.

## How does it work?

Picture two conveyor belts running side by side inside the model.

Belt one carries the raw chatbot text as it arrives, word by word.
Belt two carries the cleaned-up text produced so far, slightly behind.
At each step the model looks at both belts together — what raw words
have arrived plus what it has already cleaned — and writes the next
cleaned word. When the chatbot finishes, the raw belt is padded with
blanks and the model keeps writing until it signals it is done.

The key control is a single number called the *delay* (d): how many
raw words the model waits for before writing its first cleaned word.
A delay of 4 (the recommended setting) means it peeks at 4 raw words,
then starts writing. A delay of 1 starts almost immediately but often
guesses wrong (score ~0.70); a delay of 16 is much more accurate
(~0.92) but makes the user wait ~750 ms. Four is the sweet spot:
score ~0.894 at ~213 ms.

Training teaches exactly this skill. Instead of showing the model whole
sentences, the training objective only lets it see the partial input
it would have at each step — the same limited view it gets in real
use — and grades it only on the cleaned words. This is done with
full retraining of all the model's weights (not a cheap adapter:
a LoRA-only version collapsed to ~0.63), and no fancy instruction
prompt is needed — adding one slightly hurt the score.

The test collection was built to match real chatbot output. Everyday
questions came from DuReader (Baidu Search and Zhidao), filtered for
tricky expressions; scientific examples were drafted by a larger
model and hand-reviewed; the correct cleaned versions were produced
under written pronunciation guidelines and every test answer was
checked by a person.

## Where can this be used?

- **Voice assistants and phone bots.** The direct target: any Chinese
spoken dialogue system where the chatbot's reply must be spoken with
minimal pause between thinking and talking.
- **Car, home, and customer-service speech pipelines.** Any setup with
a chatbot feeding a streaming speech synthesizer benefits from a
drop-in streaming cleanup step that does not hold up the first sound.
- **Reading scientific and technical content aloud.** Tutoring apps,
lab assistants, and accessibility readers that encounter formulas and
equations — the hardest cases in the tests — get a model explicitly
trained and measured on them.
- **Replacing rule maintenance.** Teams currently maintaining large
hand-written rule sets for numbers, dates, and units can replace or
supplement them with a learned model that handles unseen phrasing
more gracefully.
- **Research on real-time speech chains.** The public benchmark (14
categories with accuracy and delay measurements) gives other teams a
standard way to compare streaming normalizers under realistic timing.

## Conclusions & takeaways

- StreamTN shows the middle of the speech chain can stream too: with a
4-word delay it matches a strong non-streaming model (~0.894 vs ~0.894)
while starting output after ~213 ms of its own compute.
- Delay is a smooth, predictable knob: more waiting means better
accuracy (0.70 → 0.92 from delay 1 to 16) at the cost of slower first
sound (75 ms → 756 ms). A fully non-streaming version scores highest
(~0.964) but cannot start until the whole reply arrives.
- The job needs real training, not shortcuts: full retraining beats
lightweight adapters by a wide margin, and no system prompt is needed.
- Easy cases are nearly solved (units 0.977, money 0.975, time 0.967;
most everyday number types above 0.95), while complex math equations
(0.750) and chemical formulas (0.791) remain the clear frontier —
long, oddly structured, and hard to spell out character by character.
- Bottom line: for Chinese streaming voice dialogue, a small dedicated
streaming cleaner beats big generic models and brittle rule lists on
the combination of speed, accuracy, and robustness.

## Jargon decoder

| Term | Plain meaning |
|---|---|
| Text normalization (TN) | Rewriting shortcuts like "2024" or "kg" into the full words a speech engine should say. |
| Non-standard word (NSW) | Any written shortcut whose pronunciation depends on context (dates, amounts, formulas). |
| Cascaded spoken dialogue system | A voice assistant built as a chain: understand speech → chatbot replies → speak reply. |
| TTS (text-to-speech) | The module that turns cleaned text into audible voice. |
| Dual-track architecture | StreamTN's design: one track reads incoming raw words, a delayed second track writes cleaned words. |
| Delay parameter (d) | How many raw words the model waits for before writing its first cleaned word; the speed-vs-accuracy knob. |
| First-packet delay (FPD) | How long until the first cleaned word is ready — the pause the user actually notices. |
| Micro-F1 / Micro-Precision | Accuracy scores counted character by character across all test examples; higher is better. |
| LoRA fine-tuning | A cheap training shortcut that adjusts only a small add-on; too weak for this task. |
| Autoregressive decoding | Writing output one word at a time, each new word building on the words already written. |
