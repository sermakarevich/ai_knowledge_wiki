# Compiling Agentic Workflows into LLM Weights: Near-Frontier Quality at Two Orders of Magnitude Less Cost

**Paper:** [Compiling Agentic Workflows into LLM Weights (Dennis et al., 2026)](https://arxiv.org/abs/2605.22502)

## Human Readable TL;DR

Imagine you have a customer service script that a manager (the "orchestrator") reads out loud to a new employee (the AI model) before every single customer call -- that's how most AI agent systems work today, and it's expensive and slow. This paper asks: what if instead of reading the script every time, you just trained the employee until they internalized it? The result is an employee that needs no manager on the call, works 100--400x cheaper, and still handles 87--98% of situations as well as the best frontier systems. You can even retrain them with an updated script in about 30--50 minutes if the procedure changes.

## TL;DR

This paper empirically challenges three assumed barriers to compiling agentic workflows directly into LLM weights ("subterranean agents") instead of relying on external orchestration frameworks. Across travel booking, Zoom support, and insurance claims tasks, 8B fine-tuned models achieve 87--98% of frontier in-context quality while costing 128--462x less per conversation and requiring only 30--50 minutes to recompile when procedures change. The core insight is: persistent procedural structure belongs in the weights, transient conversational state belongs in the prompt.

---

## Problem & Motivation

External agent orchestration frameworks (LangGraph, CrewAI, Google ADK, etc.) dominate with 290k+ combined GitHub stars, yet they inject instructions and routing decisions into the LLM every turn -- a costly, failure-prone pattern for procedural tasks. The alternative of embedding the full procedure in a frontier model's system prompt works well qualitatively but burns context window, locks you into expensive frontier APIs, and exposes proprietary logic to third-party providers. Compiling procedures directly into model weights ("weight compilation") was proven feasible by prior academic work (SimpleTOD, FireAct, WorkflowLLM), yet developer adoption remains negligible. This paper identifies and empirically dismantles the three perceived reasons why.

---

## Main Original Ideas

1. **Subterranean Agent Architecture** -- The orchestrator is used only at training time to generate synthetic conversations from a procedure flowchart. At inference, the fine-tuned model receives a minimal system prompt with no injected procedure -- it self-orchestrates from internalized weights. This eliminates runtime routing logic entirely.

2. **Compilation Pipeline** -- A four-step process: (1) define the procedure as a directed flowchart, (2) generate synthetic conversations by traversing all valid paths using a frontier model, (3) full-parameter fine-tune a small open-source LLM on those conversations, (4) deploy without any orchestration layer. LoRA was found insufficient; full-parameter fine-tuning is required.

3. **Persistent vs. Transient Information Split** -- The key architectural principle: procedural structure that must persist across all conversations is compiled into weights, while transient state (the current user's details, conversation history) stays in the prompt. This is the theoretical justification for why compilation outperforms orchestration on procedural tasks.

4. **Structural Advantages of Compilation** -- Compiled models avoid three structural costs imposed by orchestration: fragmented reasoning (each LLM call processes only one node's context), routing failures (classifier errors misdirect conversation flow), and constrained conversational style (node prompts restrict natural responses). These advantages explain why a 3B compiled model can outperform a 3B orchestrated model and stay competitive with a 70x-larger frontier orchestrator.

5. **Cost Scaling with Procedure Complexity** -- The cost advantage of compilation *grows* with procedure complexity because compiled models use a constant-size minimal prompt regardless of flowchart size. A 14-node procedure saves ~2x tokens; a 55-node procedure saves ~7x. Combined with ~65x per-token savings from self-hosting, this yields 128--462x total cost reduction.

---

## Key Findings

| Metric | 8B Compiled vs. In-Context Baseline | 8B Compiled vs. LangGraph Orchestrator |
|--------|-------------------------------------|----------------------------------------|
| Quality range | 87--98% across all domains | Competitive or better |
| Cost per conversation | 128--462x cheaper | 77--249x cheaper |
| Latency (Insurance) | -- | 2.8x faster (43.2s vs. 120.8s) |
| Failure rate (Travel) | -- | 5.5% vs. 24.0% |
| Failure rate (Insurance) | -- | 9.0% vs. 17.0% |
| Recompile cycle | 30--50 min (8x H200) | 3--4 hr (single A100) |
| Compilation break-even | 500 conversations | -- |

- The 3B compiled model beats the **same 3B base model with orchestration** on 4/5 quality metrics (p < 0.001), isolating compilation itself as the performance driver -- not model size.
- Scaling from 3B to 8B closes the graceful handling and naturalness gap with frontier models from ~82% to 92--97%.
- The 8B compiled model **leads** the LangGraph orchestrator on Naturalness (Zoom, p < 0.001) and Graceful Handling + Naturalness + Consistency (Insurance, p < 0.001).
- Compiled models develop a natural "one-question-per-turn" style that produces cleaner audit trails.
- Results confirmed by independent GPT-4.1 judge, ruling out Claude self-preference bias.
- One-time compilation cost: $50--80, breaking even vs. in-context baseline within 500 conversations.

---

## Suggestions & Future Directions

1. **Larger model scales** -- Testing 14B+ parameter models was not done; larger compiled models may close the remaining quality gap entirely.
2. **Broader domain coverage** -- All three domains are customer service / support workflows; extension to coding agents, research tasks, or multi-modal workflows is open.
3. **LoRA vs. full fine-tuning** -- The paper confirms full-parameter fine-tuning is needed (LoRA insufficient), but the boundary conditions and potential improvements to parameter-efficient methods warrant further investigation.
4. **Dynamic procedure updates** -- The current pipeline requires full recompilation on any procedure change; online or incremental fine-tuning methods could shrink the recompile cycle further.
5. **Multi-procedure models** -- Compiling multiple distinct procedures into a single model (with task routing by the model itself) is a natural extension not yet explored.
6. **Proprietary procedure protection** -- The paper identifies IP protection as a benefit of self-hosting but does not formally study adversarial extraction; this is an open security question.

---

## Authors & Institutions

Simon Dennis (i14, University of Melbourne), Rivaan Patil (i14), Kevin Shabahang (i14), Hao Guo (i14)
