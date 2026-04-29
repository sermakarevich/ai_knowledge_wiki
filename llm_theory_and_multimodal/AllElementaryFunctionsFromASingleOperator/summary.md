# All Elementary Functions from a Single Operator

**Paper:** [All elementary functions from a single operator (Odrzywolek, 2025)](https://arxiv.org/abs/2603.21852v2)

## Human Readable TL;DR

In digital electronics, there's a single logic gate called NAND that can build any computer circuit -- every chip in your phone is ultimately made of copies of this one building block. Until now, nobody knew if a similar trick existed for the math on your calculator -- could one simple operation replace sin, cos, square root, logarithm, and everything else? This paper discovers that yes, a single operation called EML (which just does "raise e to the power of the first number, then subtract the logarithm of the second") combined with the number 1 can reconstruct every button on a scientific calculator. It's like finding out every recipe in a cookbook can be made from one ingredient.

## TL;DR

The paper identifies a single binary operator `eml(x, y) = exp(x) - ln(y)` which, paired with the constant `1`, is functionally complete for all standard elementary functions -- arithmetic, transcendentals, algebraic operations, and constants including pi and i. This is the continuous-math analog of the NAND gate's universality in Boolean logic. The uniform binary-tree structure of EML expressions is then exploited for gradient-based symbolic regression that can recover exact closed-form formulas from numerical data.

---

## Problem & Motivation

Boolean logic has the NAND gate -- a single two-input operation from which any logical circuit can be built. Continuous mathematics has had no comparable primitive: scientific calculators and programming languages ship dozens of distinct operations (exp, ln, sin, cos, sqrt, pow, ...) with well-known redundancies but no single generating element. This paper asks: can one binary operator and one constant reconstruct the entire scientific-calculator repertoire? Answering this question would reveal hidden structural simplicity in elementary mathematics and open new avenues for symbolic regression, analog computing, and interpretable AI.

---

## Main Original Ideas

1. **The EML operator.** The operator `eml(x, y) = exp(x) - ln(y)`, together with the constant `1`, is constructively shown to generate all 36 standard calculator primitives (arithmetic, transcendentals, algebraic functions, and constants). For example: `e^x = eml(x, 1)`, `ln(x) = eml(1, eml(eml(1, x), 1))`, `e = eml(1, 1)`.

2. **Systematic ablation methodology.** The author applies a "broken calculator" ablation strategy -- iteratively removing operations from a full 36-primitive basis and verifying that the remaining set can still reconstruct everything. This drives the reduction from 36 primitives down to a single operator, guided by hybrid numeric bootstrapping verified against the Schanuel conjecture.

3. **Uniform binary-tree grammar.** Every elementary expression collapses to a binary tree where each internal node is `eml` and each leaf is `1` or a variable, yielding the minimal context-free grammar `S -> 1 | eml(S, S)`. This is a direct continuous analog of NAND circuit topology.

4. **EML-based symbolic regression.** The uniform tree structure enables a "master formula" with trainable linear-combination weights at each node. Gradient-based optimization (Adam) can snap these weights to integers 0/1, recovering exact closed-form expressions from numerical data -- 100% success at depth 2, ~25% at depths 3--4.

5. **Related operator family.** Two cousins are identified: `edl(x, y) = exp(x) / ln(y)` (with constant `e`) and the argument-swapped variant `-eml(y, x) = ln(x) - exp(y)` (with constant `-inf`), showing EML is not unique but part of a family.

---

## Key Findings

| Primitive | EML complexity (K) | Notes |
|---|---|---|
| `e^x` | 3 | Simplest: `eml(x, 1)` |
| `e` | 3 | `eml(1, 1)` |
| `ln(x)` | 7 | Requires nesting |
| `0` | 7 | |
| `-1` | 15 | |
| `x * y` | 17 | Arithmetic is surprisingly complex |
| `x + y` | 19 | |
| `2` | 19 | |
| `pi` | >53 | Requires complex-domain intermediates |

- Functional completeness is **constructively proven**: all 36 calculator primitives are derivable from `{1, eml}`.
- Trigonometric functions require internal complex-domain computation (via Euler's formula and `i = exp(ln(-1) / 2)`), even when inputs and outputs are real.
- Direct exhaustive search yields shorter EML expressions than the prototype compiler, indicating room for optimization.
- Symbolic regression with EML master formulas recovers exact formulas with 100% success at tree depth 2; perturbed correct trees converge back to exact values even at depths 5--6, revealing robust basins of attraction.

---

## Suggestions & Future Directions

1. **Search for better operators** -- other EML-type operators may have more convenient asymptotics, fewer domain issues, or require different companion constants.
2. **Ternary universal operator** -- does a three-input operator exist that needs no distinguished constant at all?
3. **Univariate Sheffer activation function** -- could such an operator also serve as a neural-network activation function?
4. **Real-domain completeness** -- can a continuous Sheffer operator avoid complex intermediates entirely, or are they always necessary for trigonometric functions?
5. **Deeper symbolic regression** -- improving convergence of gradient-based EML recovery at tree depths beyond 4--5 for practical scientific-discovery applications.
6. **Analog computing** -- compiling expressions into uniform EML circuits as a building block for analog hardware.

---

## Authors & Institutions

Andrzej Odrzywolek -- Institute of Theoretical Physics, Jagiellonian University, Krakow, Poland.
