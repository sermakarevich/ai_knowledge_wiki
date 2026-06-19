# LLM Theory & Multimodal

Research on **core LLM theory, transformer architecture, reasoning mechanics, scaling properties, and multimodal models** (vision + audio + language).

## Papers

- [[AgenticWorldModeling/summary]] — Survey of 400+ works proposing L1–L3 capability levels (Predictor, Simulator, Evolver) for world models across four governing-law regimes; replaces generative metrics with decision-centric ASR/COD evaluation.
- [[AllElementaryFunctionsFromASingleOperator/summary]] — A single binary operator `eml(x,y)=exp(x)-ln(y)` generates all 36 standard math functions — continuous NAND universality.
- [[ASurveyOfLargeLanguageModels]] — Comprehensive encyclopedia of LLMs: pre-training, RLHF, prompting, emergent abilities, evaluation.
- [[FormalComparisonCoTLatentThought/summary]] — Formal proof that CoT enables PSPACE reasoning via sequential token positions while latent thought is bounded by NC; yields principled criteria for choosing between the two paradigms.
- [[HowEmotionShapesTheBehaviorOfLLMsAndAgents]] — E-STEER injects emotions via SAEs; positive valence +14.5% reasoning, dominance +28% agent success.
- [[HowTransformersLearnToPlanViaMultiTokenPrediction/summary]] — Multi-token prediction enables goal-first reverse reasoning; 87% on 3-SAT vs. 10% for NTP.
- [[LittleBookGenerativeAIFoundations/summary]] — Mathematical primer unifying 10 generative model families (VAE, DDPM, score-based diffusion, normalizing flows, GANs, EBMs) from first principles; step-by-step derivations with explicit cross-paradigm bridges (PCA→PPCA→VAE, energy gradients = score fields).
- [[LLMReasoningIsLatent/summary]] — "Reasoning" conflates visible CoT, latent state dynamics, and generic compute; dominant factor depends on task.
- [[LlmsGetLostInMultiTurnConversation]] — Multi-turn drops 39% vs. single-turn; degradation is unreliability, not reduced peak, triggers at 2 turns.
- [[LoopThinkGeneralize/summary]] — Recurrent-depth transformers overcome systematic generalization and depth-extrapolation failures via three-stage grokking; scaling inference-time iterations extends reasoning to chain lengths never seen during training.
- [[MechanisticAnalysisLoopedReasoning/summary]] — Looped transformers develop per-layer cyclic fixed points; each iteration recapitulates staged inference.
- [[MixtureOfDepthsAttention/summary]] — Single-softmax attention over both sequence tokens and depth-stream KVs from all preceding layers; combats Transformer information dilution with +1.76–2.11% downstream task gains at 97.3% FlashAttention-2 efficiency.
- [[NeuralComputers]] — Unified computation/memory/IO as video generation; strong PSNR but only 4% native arithmetic accuracy.
- [[PowerAndLimitationsOfAggregation]] — Characterizes when aggregating identical LLM outputs expands achievable outputs; three necessary mechanisms.
- [[RecurrentTransformer/summary]] — Layerwise recurrent KV memory boosts effective depth without extra parameters; RT 6-layer at 300M params outperforms 24-layer Transformer baseline; O(N log N) tiling cuts HBM traffic.
- [[ScientificTheoryOfDeepLearning/summary]] — Synthesis paper proposing "learning mechanics": five lines of evidence (solvable settings, limits, empirical laws, hyperparameters, universality) for an emerging physics-style theory of deep learning.
- [[StepsTowardArtificialIntelligence/summary]] — Minsky 1961 foundational survey: Search, Pattern-Recognition, Learning, Planning, Induction; credit assignment.
- [[TextResNet]] — Residual-style textual gradient routing; decouples local vs. upstream errors; +21 F1 over TextGrad.
- [[TextualEquilibriumPropagation]] — Local two-phase optimization (free + nudged) solves exploding/vanishing textual gradients.
- [[ThePriceReversalPhenomenon]] — In 22% of model comparisons, cheaper-listed API model costs more due to thinking-token variance.
- [[ThinkingWithVisualPrimitives/summary]] — Visual coordinates embedded directly into multimodal chain-of-thought close the "Reference Gap"; 7,056× image compression achieves SOTA on spatial reasoning and maze navigation benchmarks at 13B parameters.
- [[WhyWeThink]] — Survey of test-time compute & chain-of-thought: why extended thinking helps and may not be transparent.
