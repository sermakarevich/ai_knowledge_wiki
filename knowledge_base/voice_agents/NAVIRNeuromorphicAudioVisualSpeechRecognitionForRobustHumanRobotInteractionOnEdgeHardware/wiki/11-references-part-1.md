> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# References Part 1: Energy, SNN, and Hardware References
**In one sentence:** This page catalogs bibliography entries [2]–[30] cited by the NAVIR paper, spanning computing-energy motivation, SNN training and architectures, neuromorphic hardware studies, and audio-visual speech datasets.
## Key points
- [2] M. Horowitz, "1.1 Computing's energy problem (and what we can do about it)," 2014 IEEE ISSCC Digest of Technical Papers, pp. 10–14, 2014.
- [3]–[5] cover SNN training foundations: spatio-temporal backpropagation (Wu et al., Front. Neurosci., vol. 12, 2017), deep residual learning in SNNs (Fang et al., NeurIPS 2021), and advancing SNNs toward deep residual learning (Hu et al., IEEE TNNLS, vol. 36, pp. 2353–2367, 2021).
- [6]–[8] cover SNN transformer and forecasting variants: Spikformer (Zhou et al., ICLR 2023), spike-driven transformer (Yao et al., NeurIPS 2023), and time-series forecasting with SNNs (Lv et al., ICML 2024).
- [9]–[11] cover audio-visual SNN fusion work: semantic-alignment and cross-modal residual learning (He et al., 2025, arXiv:2502.12488), spiking Tucker fusion transformer (Li et al., IEEE TIP, vol. 33, pp. 4840–4852, 2024), and human-inspired AVSR computing (Liu et al., IEEE Trans. Computers, vol. 74, pp. 2950–2961, 2025).
- [12]–[17] cover neuromorphic energy/hardware evidence: SNN energy-efficiency for space (Lunghi et al., Astrodynamics, vol. 9, pp. 909–932, 2025), Akida vs. NVIDIA GPU comparison (Chemnitz and Ermis, 2025), low-power ship detection (Lenz and McLelland, 2024, arXiv:2406.11319), onboard processing with COTS SoCs and neuromorphic co-processors (Benoot et al., SPAICE2024, pp. 416–419), braking-intent few-shot transfer (Lutes et al., J. Neural Eng., vol. 22, 2024), and Akida on-edge medical imaging training (Bråtman and Dow, 2023).
- [18]–[24] cover audio-visual speech corpora: GRID audio-visual corpus (Cooke et al., JASA, vol. 120, pp. 2421–2424, 2006, PMID: 17139705), Lip Reading in the Wild (Chung and Zisserman, ACCV 2016), deep AVSR (Afouras et al., IEEE TPAMI, vol. 44, pp. 8717–8727, 2018), LRS3-TED (Afouras et al., 2018, arXiv:1809.00496), TCD-TIMIT (Harte and Gillen, IEEE Trans. Multimedia, vol. 17, pp. 603–615, 2015), looking-to-listen cocktail party (Ephrat et al., ACM TOG, vol. 37, pp. 1–11, 2018), and ASPIRE noisy AV enhancement corpus (Gogate et al., 2020).
- [25]–[30] as visible in the chunk cover event-based lip-reading (Tan et al., CVPR 2022, pp. 20062–20071), Heidelberg spiking datasets (Cramer et al., IEEE TNNLS, vol. 33, pp. 2744–2757, 2019), Speech Commands dataset (Warden, 2018, arXiv:1804.03209), LipNet sentence-level lipreading (Assael et al., 2016, arXiv:1611.01599), lip reading sentences in the wild (Chung et al., CVPR 2017, pp. 3444–3453), and LCANet cascaded attention-CTC lipreading (Xu et al., FG 2018, pp. 548–555).
---
## Cited references [2]–[11]
| No. | Citation as printed in chunk |
|---|---|
| [2] | M. Horowitz, "1.1 Computing's energy problem (and what we can do about it)," 2014 IEEE International Solid-State Circuits Conference Digest of Technical Papers (ISSCC), pp. 10–14, 2014. |
| [3] | Y. Wu, L. Deng, G. Li, J. Zhu, and L. Shi, "Spatio-Temporal Backpropagation for Training High-Performance Spiking Neural Networks," Frontiers in Neuroscience, vol. 12, 2017. |
| [4] | W. Fang, Z. Yu, Y. Chen, T. Huang, T. Masquelier, and Y. Tian, "Deep Residual Learning in Spiking Neural Networks," in Neural Information Processing Systems, 2021. |
| [5] | Y. Hu, L. Deng, Y. Wu, M. Yao, and G. Li, "Advancing Spiking Neural Networks Toward Deep Residual Learning," IEEE Transactions on Neural Networks and Learning Systems, vol. 36, pp. 2353–2367, 2021. |
| [6] | Z. Zhou et al., "Spikformer: When spiking neural network meets transformer," in The Eleventh International Conference on Learning Representations, 2023. |
| [7] | M. Yao et al., "Spike-driven transformer," in Thirty-seventh Conference on Neural Information Processing Systems, 2023. |
| [8] | C. Lv, Y. Wang, D. Han, X. Zheng, X. Huang, and D. Li, "Efficient and Effective Time-Series Forecasting with Spiking Neural Networks," in International Conference on Machine Learning, 2024. |
| [9] | X. He, D. Zhao, Y. Dong, G. Shen, X. Yang, and Y. Zeng, Enhancing audio-visual spiking neural networks through semantic-alignment and cross-modal residual learning, 2025. arXiv: 2502.12488 [cs.CV]. |
| [10] | W. Li, P. Wang, R. Xiong, and X. Fan, "Spiking Tucker Fusion Transformer for Audio-Visual Zero-Shot Learning," IEEE Transactions on Image Processing, vol. 33, pp. 4840–4852, 2024. |
| [11] | Q. Liu, J. Wang, Y. Wang, X. Yang, G. Pan, and H. Li, "Human-Inspired Computing for Robust and Efficient Audio-Visual Speech Recognition," IEEE Transactions on Computers, vol. 74, pp. 2950–2961, 2025. |
**Covers:** bibliography entries [2]–[11] on paper p. 11, left column
## Cited references [12]–[17]
| No. | Citation as printed in chunk |
|---|---|
| [12] | P. Lunghi, S. Silvestrini, D. Dold, G. Meoni, A. Hadjiivanov, and D. Izzo, "Energy efficiency analysis of Spiking Neural Networks for space applications," Astrodynamics, vol. 9, pp. 909–932, 2025. |
| [13] | C. Chemnitz and M. Ermis, Comparison of Akida Neuromorphic Processor and NVIDIA Graphics Processor Unit for Spiking Neural Networks. 2025. |
| [14] | G. Lenz and D. McLelland, Low-power ship detection in satellite images using neuromorphic hardware, 2024. arXiv: 2406.11319 [cs.CV]. |
| [15] | W. Benoot, N. Destrycker, and A. De Brabanter, "Development of a robust onboard data processing unit using commercial off-the-shelf system-on-chips and neuromorphic co-processors," presented at the Proceedings of SPAICE2024: The First Joint European Space Agency / IAA Conference on AI in and for Space, Oct. 1, 2024, pp. 416–419. |
| [16] | N. Lutes, V. Sriram, S. Nadendla, and K. Krishnamurthy, "Few-shot transfer learning for individualized braking intent detection on neuromorphic hardware," Journal of Neural Engineering, vol. 22, 2024. |
| [17] | E. Bråtman and L. Dow, Neuromorphic Medical Image Analysis at the Edge: On-Edge Training with the Akida Brainchip. 2023. |
**Covers:** bibliography entries [12]–[17] on paper p. 11, spanning both columns
## Cited references [18]–[30] (as visible)
| No. | Citation as printed in chunk |
|---|---|
| [18] | M. Cooke, J. Barker, S. Cunningham, and X. Shao, "An audio-visual corpus for speech perception and automatic speech recognition," The Journal of the Acoustical Society of America, vol. 120, pp. 2421–2424, 5 Pt 1 Nov. 2006. PMID: 17139705. |
| [19] | J. S. Chung and A. Zisserman, "Lip Reading in the Wild," in Asian Conference on Computer Vision, 2016. |
| [20] | T. Afouras, J. S. Chung, A. W. Senior, O. Vinyals, and A. Zisserman, "Deep Audio-Visual Speech Recognition," IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 44, pp. 8717–8727, 2018. |
| [21] | T. Afouras, J. S. Chung, and A. Zisserman, Lrs3-ted: A large-scale dataset for visual speech recognition, 2018. arXiv: 1809.00496 [cs.CV]. |
| [22] | N. Harte and E. Gillen, "TCD-TIMIT: An Audio-Visual Corpus of Continuous Speech," IEEE Transactions on Multimedia, vol. 17, pp. 603–615, 2015. |
| [23] | A. Ephrat et al., "Looking to listen at the cocktail party," ACM Transactions on Graphics (TOG), vol. 37, pp. 1–11, 2018. |
| [24] | M. Gogate, K. Dashtipour, A. Adeel, and A. Hussain, "ASPIRE - Real noisy audio-visual speech enhancement corpus," 2020. |
| [25] | G. Tan, Y. Wang, H. Han, Y. Cao, F. Wu, and Z. Zha, "Multi-grained Spatio-Temporal Features Perceived Network for Event-based Lip-Reading," 2022 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 20062–20071, 2022. |
| [26] | B. Cramer, Y. Stradmann, J. Schemmel, and F. Zenke, "The Heidelberg Spiking Data Sets for the Systematic Evaluation of Spiking Neural Networks," IEEE Transactions on Neural Networks and Learning Systems, vol. 33, pp. 2744–2757, 2019. |
| [27] | P. Warden, Speech commands: A dataset for limited-vocabulary speech recognition, 2018. arXiv: 1804.03209 [cs.CL]. |
| [28] | Y. M. Assael, B. Shillingford, S. Whiteson, and N. de Freitas, Lipnet: End-to-end sentence-level lipreading, 2016. arXiv: 1611.01599 [cs.LG]. |
| [29] | J. S. Chung, A. W. Senior, O. Vinyals, and A. Zisserman, "Lip Reading Sentences in the Wild," 2017 IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pp. 3444–3453, 2016. |
| [30] | K. Xu, D. Li, N. Cassimatis, and X. Wang, "LCANet: End-to-End Lipreading with Cascaded Attention-CTC," 2018 13th IEEE International Conference on Automatic Face & Gesture Recognition (FG 2018), pp. 548–555, 2018. |
**Covers:** bibliography entries [18]–[30] on paper p. 11, right column through chunk end
