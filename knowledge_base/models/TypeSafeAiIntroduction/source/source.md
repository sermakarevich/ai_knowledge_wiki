# Introduction - TypeSafe AI
PDF: https://docs.typesafe.ai/introduction
Source: https://docs.typesafe.ai/introduction
Kind: article
Fetched: 2026-09-16T19:39:08.134460+00:00
Tool: urllib

Introduction - TypeSafe AI

## Documentation Index

Fetch the complete documentation index at:/llms.txt

Use this file to discover all available pages before exploring further.

Skip to main content

Large language models (LLMs) are designed to produce text for humans to read. When you need a model to make a judgment that your code will consume, that creates a mismatch: you are coercing a text-generation system into outputting structured decisions, then parsing the results back into something your code can depend on.Jev is TypeSafe’s flagship model and the first System One model. System One models are built to make fast, structured decisions that software can use directly. Jev evaluates typed questions against a state and returns structured results directly. No text generation, no parsing. You get typed values and probability distributions that your code can branch on, sort by, and route with.

##

​

TypeSafe primitives

TypeSafe exposes three AI primitives. Similar to software primitives, our AI primitives are modular, composable, structured, reliable, and fast. Each asks a different type of question and returns a different type of answer.

Question typeGoalReturns

ChoiceChoose an option from a listchoice, probabilities, confidence

ScoreScore the state on a rubricscore, probabilities, confidence

NoulIs this statement true?noul (0–1)

All three question types can be mixed in a single API call. Every question is evaluated in parallel and in isolation against the same state in one go. Adding questions barely changes the response time. Each question is evaluated independently, so adding more questions does not create context-rot.

##

​

Atomic questions, composed in code

System One models work best when each question asks one specific, well-scoped thing. Think of each question as a gut-check determination: the kind of judgment a highly knowledgeable person could make in a few seconds given the right context.If the question you want to ask would require extended reasoning or weighs multiple independent factors, decompose it. Ask each factor as a separate question, then combine the results with logic in your code. This keeps each individual evaluation reliable and gives you full control over how dimensions are weighted.For example, instead of “rate this startup pitch,” ask separately about market size, technical feasibility, and differentiation. Combine the scores with your own formula. When priorities shift, change a coefficient in your code rather than rewriting a prompt.

##

​

Next steps

Quick Start — Everything you need to get started immediately.

AI Primer — Why TypeSafe trains models for calibrated decisions instead of generated text.

Primitives (Questions) — How to define questions, choose between Choice, Score, and Noul, and ask several at once.

Confidence — How TypeSafe reports certainty, and how to use it architecturally.

Patterns — Common patterns for building systems with TypeSafe.

Was this page helpful?

YesNo

Assistant

Responses are generated using AI and may contain mistakes.
