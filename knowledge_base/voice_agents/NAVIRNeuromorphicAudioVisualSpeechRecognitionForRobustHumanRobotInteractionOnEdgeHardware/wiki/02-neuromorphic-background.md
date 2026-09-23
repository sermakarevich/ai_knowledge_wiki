> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Neuromorphic Background: SNN Architectures and the AKD1000
**In one sentence:** SNNs replace energy-intensive MAC operations with sparse event-driven accumulate operations, and a lineage from surrogate-gradient training through residual and spike-driven transformers to prior AKD1000 deployments motivates NAVIR's strictly convolutional, spike-encoder- and firing-rate-driven design for the AKD1000.
## Key points
- SNNs use event-driven binary computation to replace dense multiply-accumulate (MAC) operations with sparse synaptic accumulate (AC) operations, cutting power consumption in principle.
- Wu et al.'s spatio-temporal backpropagation framework unrolled leaky integrate-and-fire dynamics across time and approximated the non-differentiable spike function with a smooth surrogate, making direct deep SNN training feasible.
- SEW-ResNet and MS-ResNet applied residual connections inside spiking networks, with membrane-shortcut designs guaranteeing strictly binary spike communication for efficient hardware deployment.
- Spikformer introduced spiking self-attention with binary query, key and value tensors, and the Spike-driven Transformer redesigned attention as a mask-and-add operation reducing all components to sparse addition.
- Prior audio-visual SNN work (S-CMRL cross-modal complementary attention with semantic-alignment loss, Tucker-fusion transformer coupling binary spike sequences with floating-point representations, DVS lip events as cross-modal attention cues) still grapples with keeping the full network spike-driven.
- The AKD1000 imposes a stricter regime supporting only sequential convolutional inference via the MetaTF/CNN2SNN toolchain, precluding recurrence and attention, so NAVIR builds on convolutional SNNs with spike encoder design and firing-rate control as the primary accuracy/energy levers.
- Prior AKD1000 results: Lunghi et al. report 0.63–1.38 mJ per frame at 0.66–1.41 ms latency for 4-bit-quantized CNNs on EuroSAT with a 911 mW idle floor; Chemnitz and Ermis report 99.5% lower energy and 76.7% lower latency vs an NVIDIA GTX 1080 on a GXNOR MNIST classifier; Lenz and McLelland cut total energy to less than a quarter via a two-stage AkidaNet/YOLOv5 pipeline.
---
## A. Neuromorphic architectures for spiking neural networks
Hardware context in the chunk names Intel Loihi, IBM TrueNorth and BrainScaleS as maturing neuromorphic processors accelerating hardware-compatible SNN architecture development.

| Architecture / method | Mechanism stated in chunk |
|---|---|
| Spatio-temporal backpropagation (Wu et al. [3]) | Unrolls leaky integrate-and-fire dynamics across time; smooth surrogate for non-differentiable spike function |
| SEW-ResNet [4], MS-ResNet [5] | Residual connections within spiking networks; membrane-shortcut designs guarantee strictly binary spike communication |
| Spikformer [6] | Spiking self-attention with binary query, key and value tensors |
| Spike-driven Transformer [7] | Attention redesigned as mask-and-add operation, reducing all components to sparse addition |
| S-CMRL (He et al. [9]) | Cross-modal complementary attention with semantic-alignment loss |
| Tucker-fusion transformer (Li et al. [10]) | Couples binary spike sequences with floating-point representations |
| Liu et al. [11] | Human-inspired approach using dynamic-vision-sensor lip events as cues for cross-modal attention |

Verbatim motivation: "SNNs, by virtue of their event-driven binary computation, can in principle replace energy-intensive multiply-accumulate (MAC) operations with sparse synaptic accumulate (AC) operations, achieving substantial reductions in power consumption."

Design conclusion stated in chunk: "The AKD1000 imposes a stricter regime, since it supports only sequential convolutional inference, precluding recurrence and attention. We therefore build on the convolutional SNN literature and treat spike encoder design and firing-rate control as the primary levers for accuracy and energy."

## B. Applications of the BrainChip AKD1000
The chunk describes the AKD1000 as "a first-generation digital neuromorphic system-on-chip whose architecture supports the conversion of pre-trained CNNs into SNN-compatible models via the MetaTF/CNN2SNN toolchain."

| Study | Numbers / setup stated in chunk |
|---|---|
| Lunghi et al. [12], EuroSAT, space-applications context | 0.63–1.38 mJ per frame at 0.66–1.41 ms latency for 4-bit-quantized CNNs; 911 mW idle floor dominating the runtime budget on resource-constrained platforms |
| Chemnitz and Ermis [13] vs NVIDIA GTX 1080 | 99.5% lower energy and 76.7% lower latency on GXNOR MNIST classifier; energy advantage maintained but latency margin shrinking on YOLOv2 detector |
| Lenz and McLelland [14], maritime ship detection in satellite imagery | Two-stage AkidaNet/YOLOv5 pipeline reducing total energy to less than a quarter |

System context fragment in this chunk: the compiled SNNs connect to a host platform (Raspberry Pi 5) via PCIe, "with total system draw in the 350–430 mWh band over a five-minute inference session," and multi-stream temporally structured AVSR "has not previously been demonstrated at the system level" despite interest in sensor-level event detection and gesture recognition.

**Covers:** Section II.A–II.B (Neuromorphic architectures for SNNs; Applications of the BrainChip AKD1000), plus introductory system-draw/contributions fragment captured in this chunk
