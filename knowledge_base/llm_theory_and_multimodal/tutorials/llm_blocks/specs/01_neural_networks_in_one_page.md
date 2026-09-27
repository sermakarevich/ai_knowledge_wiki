# Task: chapter 01 — neural networks in one page (neurons, matmul, activations, loss, gradient descent)

Read `specs/COMMON.md`, `index.md`, `00_setup.md` (cwd `/Users/sergii/.ai/knowledge/research_topics/llm_theory_and_multimodal/tutorials/llm_blocks`).

## Code — `src/llm_blocks/ch01_neural_networks.py`
- `Linear` (from scratch: `W x + b`), `MLP2` (Linear→activation→Linear) — compare to `torch.nn.Linear`/`torch.nn.Sequential` in tests.
- Activations implemented as pure functions: `relu`, `gelu` (tanh approximation and exact via `torch.erf`), `silu`, `swiglu(x, W_gate, W_up)`; tests against `torch.nn.functional`.
- `train_toy(cfg)`: fit the 2-D "two moons" dataset (`sklearn.datasets.make_moons`, 500 points) with `MLP2` and plain SGD written by hand (`p -= lr * p.grad`), 300 steps; return loss history and decision boundary grid.
- `plots`: `01_activations.png` (ReLU, GELU, SiLU and their derivatives, 2 panels), `01_loss_surface.png` (a 2-parameter linear-regression loss surface as contour + the gradient-descent path for lr 0.02/0.1/0.5 showing convergence vs oscillation), `01_moons_training.png` (3 panels: decision boundary at step 0 / 50 / 300 with points), `01_loss_curve.png` (train loss vs step, log-y, annotated "plateau" and "steep phase"), `01_matmul_picture.png` (a schematic of `x (1×4) · W (4×3)` as coloured blocks, drawn with matplotlib patches, with the arithmetic of one output cell written next to it).
- `demo`: prints parameter counts and final accuracy quoted in the chapter.

## Chapter — `01_neural_networks_in_one_page.md`
What a neuron computes (weighted sum + non-linearity, the "dimmer switch" analogy); why matrix multiplication *is* a layer (picture); why non-linearity is required (show that two Linear layers collapse into one — a 4-line proof and a sentence); activation functions used in LLMs (ReLU → GELU → SiLU → SwiGLU gating — explain "gate" as a volume knob computed from the input; mention Qwen uses SwiGLU); the loss as "how wrong", cross-entropy in one sentence (details in ch. 02/08); gradients and gradient descent (ball rolling downhill, learning rate as step size — the loss-surface figure); backpropagation in one paragraph (chain rule, `loss.backward()` does it for you); mini-batches and noise; the moons demo end to end with real numbers; how an LLM is "just" this at scale (Qwen3.8-27B: 27 billion of these weights, ~64 layers) — bridge to the next chapters; Troubleshooting (loss NaN → lr too big; dead ReLUs; forgetting `zero_grad`); Exercises (change lr, swap activation, add a layer, plot gradients norms).

## Scope limits
No transformers imports in this chapter. No `index.md` edits.
