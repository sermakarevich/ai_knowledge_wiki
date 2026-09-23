> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Robot Demonstration and Closed-Loop Validation
**In one sentence:** A self-contained edge system couples the neuromorphic AVSR pipeline on Raspberry Pi + AKD1000 to a uFactory xArm 6 arm, dispatching recognised voice commands to physical action in real time with ~5× lower energy per inference than the strongest CPU baseline and >100× lower than a laptop GPU.
## Key points
- A uFactory xArm 6 robotic arm is connected directly to the Pi, closing the loop from voice command to physical action.
- Video and audio are captured, processed through the neuromorphic pipeline, and recognised commands are dispatched to the arm in real time.
- The complete system is self-contained, edge-deployable, and runs entirely on commodity embedded hardware augmented by the AKD1000.
- The chunk contains the fragment "command accuracy and 1.5% WER" and separately states a task-specific industrial-command corpus "reaches 98.6%".
- On the deployment platform the system sustains real-time throughput at approximately 5× less energy per inference than the strongest CPU baseline, identified as the SNN-converted model running on the Akida software backend.
- The same deployment point uses over 100× less energy per inference than a laptop GPU on the video-only model.
- The authors state this is, to the best of their knowledge, the first end-to-end multimodal AVSR system demonstrated on neuromorphic hardware of this class.
- The remaining gap to unconstrained SOTA accuracy is attributed to the chip's deliberate architectural simplicity, with sparsity-aware fine-tuning named as the concrete path to close the video-only vs audio-video deployment gap.
---
## Closed-loop robot system
The chunk opens mid-sentence with "by a standard USB keyboard. A uFactory xArm 6 robotic arm is connected directly to the Pi, closing the loop from voice command to physical action."

Verbatim pipeline description:

> "Video and audio are captured, processed through the neuromorphic pipeline, and the recognised commands are dispatched to the arm in real time."

Verbatim system claim:

> "The complete system is self-contained, edge-deployable and runs entirely on commodity embedded hardware augmented by the AKD1000."

No table, participant count, command vocabulary size, or latency value is present in this chunk fragment.

## Deployment efficiency and novelty claim
Exact claims as written in the chunk:

- Fragment: "command accuracy and 1.5% WER."
- "On the deployment platform it sustains real-time throughput at approximately 5× less energy per inference than the strongest CPU baseline (the SNN-converted model running on the Akida software backend) and over 100× less than a laptop GPU on the video-only model."
- "To the best of our knowledge, this is the first end-to-end multimodal AVSR system demonstrated on neuromorphic hardware of this class."
- "The remaining gap to unconstrained SOTA accuracy is consistent with the chip's deliberate architectural simplicity, and Appendix A identifies a concrete path, sparsity-aware fine-tuning, to further close the gap between the video-only and audio-video deployment points."
- Conclusion fragment also present in this chunk: "On a task-specific industrial-command corpus it reaches 98.6%".

## Truncated Discussion / Conclusion / Appendix material in this chunk
This chunk physically also contains the opening lines of Section IX "DISCUSSION AND LIMITATIONS", Section X "CONCLUSION", and "APPENDIX A WHY THE AUDIO-VIDEO MODEL IS SLOWER ON THE AKD1000" (image-encoder 75 NPs / 1 sequence vs 348 NPs / 9 sequences; `akida.Model.map()` binary search over `cnp_max_filters`; l2-only regularisation). Full treatment belongs to page `10-limitations-future-work-appendices.md`; only the robot-demo and deployment sentences above are summarised here per the plan mapping.

**Covers:** Interactive xArm 6 robot demonstration and closed-loop validation
