> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# AI primer

**In one sentence:** TypeSafe bets large-scale automation will be ~99% machine-to-machine, so instead of RLHF chatbots it trains decision models with RLCD (reinforcement learning for calibrated decisions) that return decisions plus calibrated probabilities rather than generated text.

## Key points

- Most AI products are built around model-to-person conversation, but TypeSafe bets large-scale automation will be closer to 99% machine-to-machine and 1% human interaction, so the machine interface matters more than the chat interface.
- Machine Native Intelligence means AI with software-like properties: structure, reliability, observability, testability, speed, consistency, and low cost.
- TypeSafe is not trying to build a model that does everything; it targets production systems where code needs a narrow decision it can inspect and act on.
- Pretrained language models branch into three post-training paths: RLHF (human feedback → chatbots), RLVR (verifiable rewards → reasoning models, strong at math but slower and more expensive), and TypeSafe's RLCD (calibrated decisions instead of generated text).
- RLHF was used to train InstructGPT and ChatGPT and was co-invented by Diogo Almeida, cofounder of TypeSafe.
- RLCD's output contract: the model does not generate text, it returns decisions and probabilities, and higher probability should correspond to a greater chance the answer is correct.
- Calibration is a group rate, not a per-answer guarantee: outcomes assigned 0.2 should occur ~20% of the time, 0.8 ~80%, and 1.0 100% of the time across many predictions (see Confidence for act-vs-escalate guidance).
- RLHF rewards what people prefer, which can produce sycophancy and confident-sounding hallucinations plus mode dropping (a milder version of GAN-style mode collapse where the generator repeats one fooling output), so human preference and machine trustworthiness are different optimization targets.

---

## Building prod, not God

TypeSafe is designed for production systems where code needs a narrow decision it can inspect and act on, shifting the design target from responses that feel good to read toward outputs that behave predictably inside software, given the expectation of ~99% machine-to-machine vs 1% human interaction.

Verbatim core bet:

> "We call this Machine Native Intelligence:"
>
> "AI with software-like properties such as structure, reliability, observability, testability, speed, consistency, and low cost."

Source links the [TypeSafe manifesto](https://typesafe.ai/manifesto).

## Three post-training approaches

Pretrained language models have been adapted in two major ways; TypeSafe adds a third (RLHF and RLVR shown for context; TypeSafe's path is RLCD):

| Approach | Full name | Effect |
|---|---|---|
| RLHF | Reinforcement learning from human feedback | Turned pretrained models into chatbots; trains models to produce responses people prefer (used for InstructGPT and ChatGPT; co-invented by Diogo Almeida). |
| RLVR | Reinforcement learning with verifiable rewards | Created reasoning models strong at tasks such as mathematics, but slower and more expensive. |
| RLCD | Reinforcement learning for calibrated decisions | Trains TypeSafe to return decisions and calibrated probabilities instead of generated text. |

## RLCD and calibrated decisions

RLCD optimizes for a different output contract:

- The model does not generate text.
- It returns decisions and probabilities.
- Higher probability should correspond to a greater chance that the answer is correct.

Calibration makes uncertainty usable by software. Across many predictions from a well-calibrated model:

- Outcomes assigned a probability of `0.2` should occur about 20% of the time.
- Outcomes assigned a probability of `0.8` should occur about 80% of the time.
- Outcomes assigned a probability of `1.0` should occur 100% of the time.

These rates describe groups of predictions, not a guarantee about any single answer. See Confidence for guidance on deciding when software should act or escalate.

## The problems with RLHF

RLHF teaches a model to say things that people prefer — good for chatbots, but it can also reward sycophancy and confident-sounding hallucinations. Preference optimization also causes **mode dropping**: the model learns to favor a particular style (e.g. instruction following) while reducing the probability of other possible outputs.

> "An output can be compelling to a person without being reliable enough for unattended automation. Human preference and machine trustworthiness are different optimization targets."

Mode dropping is a milder version of **mode collapse**: in the classic GAN (generative-adversarial-network) failure mode, a generator learns to produce the same kind of output repeatedly because that output keeps fooling the discriminator. RLHF remains a good fit for conversational models; TypeSafe's position is that production automation needs a different training objective centered on constrained decisions and calibrated uncertainty.

**Covers:** AI primer — why TypeSafe trains decision models with calibrated probabilities instead of generated text (source/topics/introduction_machine-learning-primer.md)
