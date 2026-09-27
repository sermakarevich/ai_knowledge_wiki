# Robots Need More Than VLAs & World Models

**Paper:** [Robots Need More Than VLAs & World Models (Karcini et al., 2025)](https://paper.motoniq.ai/paper.pdf)

## Human Readable TL;DR

Imagine you want to teach a robot to help around the house. Right now, the main approach is to collect thousands of videos of a robot doing tasks and train it to copy those actions -- but this is expensive and slow. The world is already full of useful information: videos of people cooking, sensors that track how humans move, simulations, and even robot failures. The problem is that none of this raw data tells a robot exactly what motor commands to use. The authors say we need new tools that can automatically translate messy human behavior into robot-usable instructions -- like a translator between how humans move and how robots should act. Without these translation tools, no matter how big the robot's "brain" gets, it will keep hitting the same wall.

## TL;DR

This position paper argues that the core bottleneck in generalist robotics is not policy capacity (model size or demonstration count), but the absence of mechanisms that convert unstructured physical experience -- human motion, internet video, simulation, wearable sensing -- into grounded robot supervision. The authors identify four missing architectural components: a physical data engine for embodied autolabelling, task-preserving cross-embodiment retargeting, physics-grounded world models for consequence prediction, and task-conditioned reward grounding enabling self-improving deployment loops. The paper surveys over 100 recent works in VLAs, cross-embodiment datasets, latent-action learning, world models, and reward modelling to motivate a research agenda aimed at world-scale physical supervision rather than robot-native data scaling alone.

---

## Problem & Motivation

The dominant paradigm in generalist robotics frames capability as a policy-scaling problem: collect more robot demonstrations, train larger Vision-Language-Action (VLA) models, and expect generalization to follow. Recent systems such as RT-2, π0, OpenVLA, and NVIDIA GR00T N1 have achieved impressive results under this paradigm. However, the authors argue this framing is fundamentally incomplete because it depends entirely on supervision that has already been expressed in the coordinate system of robot learning -- observations paired with robot actions, manually specified success conditions, explicit task labels, and curated reward functions.

The central bottleneck is not a shortage of physical data. Human motion, internet video, factory workflows, wearable sensor streams, simulation rollouts, and robot failure traces collectively represent enormous reservoirs of information about task structure, object affordances, contact dynamics, temporal progress, and failure recovery. But none of this data arrives with the specific labels robot learning requires: embodiment-specific action sequences, contact annotations, task phase boundaries, reward signals, and success/failure indicators. The gap between "abundant physical experience" and "usable robot supervision" is the grounding problem the paper targets.

The paper distinguishes three existing directions that each partially address this gap but fail to close it: (1) robot-native supervision (demonstrations, teleoperation, Open X-Embodiment scale datasets) which works but cannot scale to world-scale physical experience; (2) learning from weakly grounded physical observations (latent-action methods like LAPA and UniVLA, representation learners like R3M and VIP, video-based reward models like PROGRESSOR and ReWiND) which expand data sources but relocate rather than eliminate the grounding problem; and (3) generating physical experience through simulation, MimicGen-style data augmentation, and learned world models, which promise counterfactual experience but only when the generated futures preserve the physical variables that determine control success.

---

## Main Original Ideas

1. **Physical Data Engine and Embodied Autolabelling** -- A system that ingests heterogeneous, asynchronous streams of physical experience -- video frames, motion-capture, tactile readings, proprioception, language captions -- and automatically infers a latent sequence of physically grounded events (object states, contact labels, task phases, latent actions, rewards, and success/failure outcomes). The engine formalizes this as an inference model qθ(z, A | x) that jointly solves temporal alignment, event segmentation, contact inference, phase recognition, latent-action discovery, and reward grounding. Unlike ordinary video labeling, embodied autolabelling must recover labels that are physically grounded and control-relevant, not merely semantic.

2. **Task-Preserving Retargeting across Embodiments** -- Rather than copying human joint trajectories (pose-matching), this component maps latent physical actions inferred from human or wearable demonstrations into executable robot actions that preserve the task-relevant physical effect on the world (drawer displacement, object pose change, contact state). Retargeting is formalized as finding an embodiment-conditioned executable action such that the task-relevant state transition produced by the robot approximates the transition observed in the human demonstration. The paper identifies a hierarchy from pose preservation → contact preservation → object-state preservation → full intent/skill preservation, and argues generalist robotics requires progress up this hierarchy.

3. **Physics-Grounded World Models for Consequence Prediction** -- Rather than generic video generators that produce visually plausible futures, robotics requires predictive models that estimate what physically changes under candidate actions -- object permanence, contact forces, geometric constraints, material response, stability, and failure modes. The authors formalize this as consequence prediction sζ+1 ~ pω(· | sζ, aζ, embodiment, g), where predictions must be task-conditioned. The paper surveys physics-structured models, JEPA-style predictive architectures, and 3D Gaussian Splatting coupled dynamics, arguing that hybrid approaches combining 3D scene representations, object-centric structure, and physics-inspired constraints are the most promising direction.

4. **Self-Improving Deployment Loops with Task-Conditioned Reward Grounding** -- Every robot deployment rollout should become structured supervision rather than a pass/fail record. This requires task-conditioned reward models that interpret physical states relative to a goal: rη(sζ, g, ϕζ), where reward is a function of inferred physical state, task goal, and current task phase. Successful rollouts contribute robust completion examples; failures provide information about which contact was missed or which subgoal was not achieved; human corrections provide high-value supervision. The deployment loop feeds back into the physical data engine, creating a closed-loop compounding improvement system.

5. **Taxonomy of Weak Physical Supervision** -- The paper articulates a four-category taxonomy of signals that passive video can provide: (1) visual representations for perception (R3M, VIP, MVP, VC-1); (2) latent action codes describing physical transitions (LAPA, UniVLA); (3) task-progress and reward signals from temporal order (PROGRESSOR, Adapt2Reward, ReWiND, TimeRewarder, SARM); and (4) behavioral priors about object affordances, contact, and temporal task structure. The key insight is that all four categories relocate rather than eliminate the grounding problem.

6. **Uncertainty Quantification for World Models** -- The paper identifies calibrated uncertainty as a critical and underexplored property for robot world models. Without it, hallucinated predictions lead to poor control choices that push the world model further from its training distribution, creating compounding errors. The authors survey early work (Mei et al. 2025, Li et al. 2025, Ward et al. 2026) and identify this as a key growth area as world models become more integrated into autonomy stacks.

---

## Key Findings

- MimicGen generates 50,000+ demonstrations from fewer than 200 seed demos across 18 tasks, demonstrating simulation-based synthesis can dramatically scale robot experience -- but open question remains whether generated trajectories preserve contact and failure-mode details needed for real control
- RoboCasa365 reports 365 everyday tasks, 2,500 kitchen scenes, and 2,000+ hours of robot interaction data -- yet still requires manually specified task definitions and success conditions
- OpenVLA trains a 7B-parameter VLA on ~970,000 real-world demos from Open X-Embodiment; SpatialVLA is trained on ~1.1M real robot episodes; RDT-1B pretrains on 1M+ multi-robot episodes -- all still require robot-native action labels
- V-JEPA 2 combines internet-scale video with a small amount of robot interaction data and reports zero-shot robot control capabilities -- one of the clearest links between JEPA-style world models and embodied control
- Policies trained in 3D Gaussian Splatting simulators (SOUS VIDE, SINGER) transfer zero-shot to real-world drone navigation; ContactGaussianWM reports real-time MPC from a physics-grounded Gaussian rigid-body world model
- DreamerV3 shows a single world-model algorithm with fixed hyperparameters solves a wide range of control tasks; DayDreamer shows Dreamer-style world models can be learned directly on physical robots
- No existing system fully closes all four missing components simultaneously; the closest examples (LAPA, UniVLA, GR00T N1, V-JEPA 2) address one or two components but leave grounding gaps in the others
- The grounding gap is asymmetric: the world contains far more physical behavioral data than current pipelines can use; the limiting factor is absence of grounding mechanisms, not shortage of compute or model capacity

---

## Suggestions & Future Directions

1. **Build physical data engines as standalone systems** -- develop inference models that jointly solve temporal alignment, event segmentation, object-state estimation, contact inference, task phase recognition, latent-action discovery, and reward grounding from heterogeneous, partially supervised episode sources
2. **Develop task-preserving retargeting beyond pose-matching** -- create systems that preserve contact events, object-state transitions, and task intent across the morphological diversity between human hands, parallel-jaw grippers, dexterous hands, mobile manipulators, quadrupeds, and humanoids
3. **Design world models evaluated by control utility, not visual fidelity** -- shift evaluation criteria from visual realism to whether predicted futures preserve the physical consequences (contact, geometry, force, stability) that determine task success
4. **Develop calibrated uncertainty quantification for world models** -- extend early work to make world models aware of when they are operating outside their training distribution, enabling uncertainty-gated planning and failure detection
5. **Close the self-improving deployment loop** -- build systems where deployment failures are automatically routed to the correct component (policy, reward model, world model, or retargeting) via component-level credit assignment
6. **Use wearable and embodied sensing as a labeling instrument** -- treat motion-capture or sensorimotor suit demonstrations as sources of physically structured supervision to train perception models, reward models, retargeting systems, and robot policies simultaneously
7. **Integrate human-centric data for human-aware and collaborative robot policies** -- leverage human motion and wearable data to build natural, human-compliant, and collaborative behavioral models
8. **Shift evaluation benchmarks for generalist robotics** -- move beyond measuring whether a larger policy solves more tasks toward measuring whether a system can convert weaker sources of physical experience into useful supervision
9. **Develop hybrid world model architectures** -- combine 3D scene representations, object-centric structure, physics-inspired inductive biases (Lagrangian/Hamiltonian mechanics, differentiable contact), and data-driven residual dynamics

---

## Authors & Institutions

Elis Karcini (Motoniq.ai), Faisal Mehrban (Motoniq.ai), Arash Ajoundani (Istituto Italiano di Tecnologia), Nguyen Pham (Motoniq.ai), César Cadena (ETH Zurich), Marco Hutter (ETH Zurich), Mac Schwager (Stanford University, Motoniq.ai), Jan Peters (Technical University of Darmstadt), Haitham Bou-Ammar (UCL Centre for AI)
