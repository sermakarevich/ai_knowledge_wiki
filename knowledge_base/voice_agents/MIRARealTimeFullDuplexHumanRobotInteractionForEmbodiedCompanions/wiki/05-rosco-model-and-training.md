> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# ROSCO Model and Training

**In one sentence:** ROSCO-DiT is a prefix-conditioned diffusion transformer that generates target motion chunks from preceding motion context and causal audio features, trained with rich-motion reconstruction plus kinematic, rollout, and contrastive audio objectives.

## Key points

- Streaming generation conditions on preceding motion prefix `Pi` and causal audio features, with cached rich-motion history providing the prefix for subsequent updates.
- The backbone consists of eight stacked Prefix-DiT blocks, each applying causal motion self-attention, causal audio cross-attention, and a feed-forward network.
- Motion and prefix audio sequences are processed by a shared causal audio encoder, and each motion token can access only same-or-earlier audio tokens.
- Motion sequence is projected to d = 256 dimensions with sinusoidal temporal position embeddings; each block uses 4 attention heads, a 1024-dimensional feed-forward layer, and dropout of 0.1.
- Diffusion timestep τ is embedded and injected via AdaLN, with separate shift, scale, and residual gates (g1, g2, g3) for self-attention, cross-attention, and feed-forward branches.
- Only denormalized joint qpos qt are retained for downstream robot execution; auxiliary geometric components are used for training and reconstruction.
- Training combines rich-motion reconstruction, kinematic consistency with FK and collision clearance, two-step autoregressive rollout, and a margin-based contrastive audio loss.
- Streaming inference uses overlapping windows: each call predicts 50 frames but commits only the first 15, reusing the latest 10 committed frames as prefix context at 30 fps.

---

## Figure 3a — Streaming generation

ROSCO-DiT predicts a clean motion window conditioned on the preceding motion context and causal audio features. The cached rich-motion history provides the prefix for subsequent updates.

**Covers:** Figure 3a; Sections 4.2–4.3

## Motion representation

Joint qpos and local-body positions are normalized using statistics computed over the training split, with the same statistics reused during inference. Joint velocities are computed from the unnormalized trajectories and scaled by the joint-position standard deviation. The auxiliary geometric components are used for training and reconstruction, while:

> "only the denormalized joint qpos qt are retained for downstream robot execution."

**Covers:** Section 4.1 motion representation

## Figure 3b / Section 4.2 — ROSCO-DiT: Prefix-Conditioned Diffusion Transformer

ROSCO employs a prefix-conditioned Diffusion Transformer, termed ROSCO-DiT, to generate each target motion chunk conditioned on preceding motion and temporally aligned audio. Notation from the chunk:

| Symbol | Meaning |
|---|---|
| `Xi ∈ RK×Dm` | target rich-motion chunk |
| `Pi ∈ RC×Dm` | preceding motion prefix |
| `Ai ∈ RK×Da` | audio features aligned with target chunk |
| `Aprev_i ∈ RC×Da` | audio features aligned with prefix |
| `τ` | diffusion timestep |

Forward diffusion (Eq. 4):

> "X̃iτ = √ᾱτ Xi + √(1 − ᾱτ) ϵ, ϵ ∼ N(0, I)."

Denoising prediction (Eq. 5):

> "X̂i = fθ(X̃iτ, Pi, Ai, Aprev_i, τ)"

Architectural details (verbatim/mechanistic):

- Noisy target tokens and clean prefix tokens are concatenated along the temporal dimension and marked with a binary type indicator distinguishing prefix from target frames.
- Projected to d = 256 dimensions and augmented with sinusoidal temporal position embeddings.
- Prefix and target audio processed by a shared causal audio encoder, producing Eprev_i and Ei.
- Each block applies causally masked self-attention over motion tokens, then causal audio cross-attention (each motion token sees only same-or-earlier audio tokens), then a feed-forward network.
- Eight transformer blocks with four attention heads, 1024-dimensional feed-forward layer, dropout 0.1.
- Output head removes the prefix portion and predicts only the denoised target chunk X̂i.
- Diffusion timestep τ embedded and injected through adaptive LayerNorm (AdaLN); separate modulation parameters for self-attention, audio cross-attention, and feed-forward branches, including shift, scale, and residual gates g1, g2, g3.
- A modulation MLP conditioned on τ generates the AdaLN shifts and scales together with residual gates g1, g2, and g3.

**Covers:** Figure 3b; Section 4.2

## Figure 3c / Section 4.3 — Joint training objectives and contrastive loss

Matched and shuffled audio conditions share the same noisy motion, motion prefix, and diffusion timestep. The matched prediction is supervised by rich-motion reconstruction including kinematic consistency and collision constraints, while a margin-based audio loss contrasts matched and shuffled conditions through reconstruction loss and joint-qpos prediction separation.

Rich-motion objective (Eq. 6):

> "Lrich = λx MSE(X̂, X) + λq MSE(q̂, q) + λ∆q MSE(∆q̂, ∆q) + λp MSE(p̂local, plocal) + λR MSE(R̂6D, R6D) + λkin Lkin"

where λx weights full rich-motion reconstruction and λq, λ∆q, λp, λR, λkin weight joint qpos, joint velocities, local-body positions, local link rotations, and kinematic constraints.

Kinematic / collision constraints (Eq. 7): predictions are mapped to Cartesian positions via forward kinematics FK(q̂t), with output pFK_t = FK(q̂t):

> "Lkin = λFK-pos MSE(pFK, plocal) + λcol (1/T) Σt [mcol − Clearance(q̂t)]+"

where Clearance(q̂t) is the minimum pairwise clearance between collision proxies; the first term enforces Cartesian consistency and the second penalizes potential self-collisions below minimum clearance.

Autoregressive rollout (Eq. 8): to mitigate exposure bias, a two-step rollout detaches the first predicted chunk, recomputes joint velocities from predicted qpos, retains the latest C frames to form the next prefix Pi+1, and supervises the next chunk with the same rich-motion objective:

> "Lrollout = Lrich(X̂′, X′)"

Contrastive audio conditioning (Eq. 9): negative conditions are built by cyclically shuffling current and prefix audio across each batch; L+_rich and L−_rich are reconstruction losses under matched and shuffled audio; q̂+ and q̂− are predicted joint qpos under matched and shuffled audio:

> "Laudio = sg(L+_rich) + [maudio − L−_rich]+ + λsep [msep − mean|q̂+ − q̂−|]+"

where maudio encourages matched audio to yield lower reconstruction loss than mismatched audio, msep encourages minimum prediction difference in joint-qpos space, and sg(·) stop-gradient prevents optimizing the matched loss through this comparison.

Complete objective (Eq. 10):

> "L = λrich Lrich + λroll Lrollout + λaudio Laudio."

**Covers:** Figure 3c; Section 4.3

## Figure 4 (included in chunk) — Overlapping-window streaming inference

Predict-more-than-commit streaming inference: 50-frame prediction / 15-frame commitment / 10-frame prefix / 30 fps. Each call predicts 50 frames but commits only the first 15; the next call advances by 15 frames, reuses the latest 10 committed frames as prefix context, and predicts an overlapping future horizon. Verbatim: "Only committed rich frames enter the next prefix; joint-angle slices are sent to the controller."

**Covers:** Figure 4 streaming inference (present in chunk body)
