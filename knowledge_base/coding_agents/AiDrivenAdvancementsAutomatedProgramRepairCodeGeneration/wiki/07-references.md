> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# References
**In one sentence:** This section is the survey's bibliography, listing references [1]–[27] spanning code LLMs, pre-trained code models, LLM-based debugging and program repair, fuzzing, and alignment methods.
## Key points
- The bibliography contains 27 numbered entries, from [1] Phind-CodeLlama (Phind Technical Report, 2023) through [27] Zhong et al., "Debug like a Human" (2024).
- Code-model entries include Phind-CodeLlama [1], StarCoder 2 and The Stack v2 (Lozhko et al., 2024) [2], Mixtral of Experts (Jiang et al., 2024) [3], DeepSeek-Coder (Guo et al., 2024) [7], and Magicoder with OSS-Instruct (Wei et al., 2024) [22].
- Pre-training representations are covered by GraphCodeBERT with data flow (Guo et al., ICLR 2021) [6], SPT-Code sequence-to-sequence pre-training (Niu et al., 2024) [14], and CodeT5 identifier-aware encoder-decoder (Wang et al., EMNLP 2021) [21].
- APR and debugging entries include LLM-based multi-agent synergy (Lee et al., 2024) [8], DEAR deep-learning APR (Li et al., 2024) [9], ProveNFix temporal property-guided repair (Song et al., ICSE 2024) [18 in text order; listed as [19]), and program repair by fuzzing over patch and input space (Zhang et al., ISSTA 2024) [25 in text order; listed as [25]).
- Evaluation and alignment entries include OpenAI's code-LLM evaluation report (2021) [15], evaluating debugging capability of LLMs (Tian et al., 2024) [20], ZEPHYR direct distillation of LM alignment (Tunstall et al., 2024) [4], WizardLM complex-instruction following (Xu et al., 2024) [24], and Smaug DPO-Positive preference optimisation (Pal et al., 2024) [34 in text order; listed as [16]).
- Fuzzing, testing, and security entries include LLM-guided protocol fuzzing (Meng et al., NDSS 2024) [12], evolutionary testing for program repair (Ruan et al., ISSTA 2024) [17], timing side-channel mitigation via APR (Ruan et al., ICSE 2024) [18], and greybox fuzzing for concurrency testing (Wolff et al., CCS 2024) [23].
- The chunk carries the survey footer "Vol. 1, No. 1, Article. Publication date: November 2024" and the running head "A Comprehensive Survey of AI-Driven Advancements and Techniques in Automated Program Repair and Code Generation" with page number 19.
---
## Code LLMs and instruction/alignment models
**Covers:** References [1]–[5], [15]–[16], [22], [24], [26]

| # | Verbatim citation as in chunk |
|---|---|
| [1] | "2023. Phind-CodeLlama. Phind Technical Report (2023). https://www.phind.com/blog/code-llama-beats-gpt4" |
| [2] | "Anton Lozhko et al. 2024. StarCoder 2 and The Stack v2: The Next Generation. arXiv preprint (2024). https://arxiv.org/abs/2402.19173" |
| [3] | "Albert Q. Jiang et al. 2024. Mixtral of Experts. arXiv preprint (2024). https://arxiv.org/abs/2401.04088" |
| [4] | "Lewis Tunstall et al. 2024. ZEPHYR: DIRECT DISTILLATION OF LM ALIGNMENT. arXiv preprint (2024). https://arxiv.org/pdf/2310.16944" |
| [5] | "Lucy Gao. 2024. TabbyML. Online. https://github.com/TabbyML/tabby" |
| [15] | "OpenAI. 2021. Evaluating Large Language Models Trained on Code. OpenAI Technical Report (2021). https://openai.com/research/evaluating-large-language-models" |
| [16] | "Arka Pal, Deep Karkhanis, Samuel Dooley, Manley Roberts, Siddartha Naidu, and Colin White. 2024. Smaug: Fixing Failure Modes of Preference Optimisation with DPO-Positive. arXiv preprint (2024). https://arxiv.org/pdf/2402.13228" |
| [22] | "Yuxiang Wei, Zhe Wang, Jiawei Liu, Yifeng Ding, and Lingming Zhang. 2024. Magicoder: Empowering Code Generation with OSS-Instruct. arXiv preprint (2024). https://arxiv.org/abs/2312.02120" |
| [24] | "Can Xu1, Qingfeng Sun, Kai Zheng, Xiubo Geng, Pu Zhao, Jiazhan Feng, Chongyang Tao, Qingwei Lin, and Daxin Jiang. 2024. WizardLM: Empowering Large Language Models to Follow Complex Instructions. arXiv preprint (2024). https://arxiv.org/abs/2304.12244" |
| [26] | "Tianyu Zheng, Ge Zhang, Tianhao Shen, Xueling Liu, Bill Yuchen Lin, Jie Fu, Wenhu Chen, and Xiang Yue. 2024. OpenCodeInterpreter: Integrating Code Generation with Execution and Refinement. arXiv preprint (2024). https://arxiv.org/abs/2402.14658" |

## Pre-trained code representations
**Covers:** References [6]–[7], [14], [21]

| # | Verbatim citation as in chunk |
|---|---|
| [6] | "Daya Guo, Shuo Ren, Shuai Lu, Long Zhou, Junjie Huang, Daxin Jiang, Shuming Shi, Huanbo Luan, and Ming Zhou. 2021. GraphCodeBERT: Pre-training Code Representations with Data Flow. In International Conference on Learning Representations (ICLR). https://arxiv.org/abs/2009.08366" |
| [7] | "Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao Zhang, Guanting Chen, Xiao Bi, Y. Wu, Y.K. Li, Fuli Luo, Yingfei Xiong, and Wenfeng Liang. 2024. Deepseek-coder. arXiv preprint (2024). https://arxiv.org/abs/2401.14196" |
| [14] | "Changan Niu, Chuanyi Li, Vincent Ng, Jidong Ge, Liguo Huang, and Bin Luo. 2024. SPT-Code: Sequence-to-Sequence Pre-Training for Learning Source Code Representations. arXiv preprint (2024). https://arxiv.org/abs/2201.01549" |
| [21] | "Yue Wang, Weishi Wang, Shafiq Joty, and Steven C.H. Hoi. 2021. CodeT5: Identifier-aware Unified Pre-trained Encoder-Decoder Models for Code Understanding and Generation. In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing (EMNLP). https://arxiv.org/abs/2109.00859" |

## Debugging, repair, fault localization, and repository understanding
**Covers:** References [8]–[11], [13], [17]–[20], [25], [27]

| # | Verbatim citation as in chunk |
|---|---|
| [8] | "Cheryl Lee, Chunqiu Steven Xia, Jen tse Huang, Zhouruixin Zhu, Lingming Zhang, and Michael R. Lyu. 2024. A Unified Debugging Approach via LLM-Based Multi-Agent Synergy. arXiv preprint (2024). https://arxiv.org/pdf/2404.17153" |
| [9] | "Yi Li, Shaohua Wang, and Tien N. Nguyen. 2024. DEAR: A Novel Deep Learning-based Approach for Automated Program Repair. arXiv preprint (2024). https://dl.acm.org/doi/pdf/10.1145/3510003.3510177" |
| [10] | "Michael R. Lyu, Baishakhi Ray, Abhik Roychoudhury, Shin Hwei Tan, and Patanamon Thongtanunam. 2024. Automatic Programming: Large Language Models and Beyond. arXiv preprint (2024). https://arxiv.org/pdf/2405.02213" |
| [11] | "Yingwei Ma, Qingping Yang, Rongyu Cao, Binhua Li, Fei Huang, and Yongbin Li. 2024. How to Understand Whole Software Repository? arXiv preprint (2024). https://arxiv.org/pdf/2406.01422" |
| [13] | "Xiangxin Meng, Xu Wang, Hongyu Zhang, Hailong Sun, and Xudong Liu. 2024. Improving fault localization and program repair with deep semantic features and transferred knowledge. arXiv preprint (2024). https://dl.acm.org/doi/abs/10.1145/3510003.3510147" |
| [17] | "Haifeng Ruan, Hoang Lam Nguyen, Ridwan Shariffdeen, Yannic Noller, and Abhik Roychoudhury. 2024. Evolutionary Testing for Program Repair. In International Symposium on Software Testing and Analysis (ISSTA). https://abhikrc.com/pdf/ICST24.pdf" |
| [18] | "Haifeng Ruan, Yannic Noller, Saeid Tizpaz-Niari, Sudipta Chattopadhyay, and Abhik Roychoudhury. 2024. Timing Side-Channel Mitigation via Automated Program Repair. 2024 International Conference on Software Engineering (ICSE) (2024). https://dl.acm.org/doi/pdf/10.1145/3678169" |
| [19] | "Yahui Song, Xiang Gao, Wenhua Li, Wei-Ngan Chin, and Abhik Roychoudhury. 2024. ProveNFix: Temporal Property-Guided Program Repair. In International Conference on Software Engineering (ICSE). https://dl.acm.org/doi/pdf/10.1145/3643737" |
| [20] | "Runchu Tian, Yining Ye, Yujia Qin, Xin Cong, Yankai Lin, Yinxu Pan, Yesai Wu, Haotian Hui, Weichuan Liu, Zhiyuan Liu, and Maosong Sun. 2024. Evaluating Debugging Capability of Large Language Models. arXiv preprint (2024). https://arxiv.org/pdf/2401.04621" |
| [25] | "Yuntong Zhang, Ridwan Shariffdeen, Gregory J. Duck, Jiaqi Tan, and Abhik Roychoudhury. 2024. Program Repair by Fuzzing over Patch and Input Space. In International Symposium on Software Testing and Analysis (ISSTA). https: //arxiv.org/pdf/2308.00666" |
| [27] | "Li Zhong, Zilong Wang, and Jingbo Shang. 2024. Debug like a Human. In Proceedings of the 2024 ACM Conference on Computer and Communications Security (CCS). https://arxiv.org/pdf/2402.16906" |

## Fuzzing and concurrency testing
**Covers:** References [12], [23]

| # | Verbatim citation as in chunk |
|---|---|
| [12] | "Ruijie Meng, Martin Mirchev, Marcel Bohme, and Abhik Roychoudhury. 2024. Large Language Model guided Protocol Fuzzing. arXiv preprint (2024). https://abhikrc.com/pdf/NDSS24.pdf" |
| [23] | "Dylan Wolff, Zheng Shi, Gregory J. Duck, Umang Mathur, and Abhik Roychoudhury. 2024. Greybox Fuzzing for Concurrency Testing. In Proceedings of the 2024 ACM Conference on Computer and Communications Security (CCS). https://dl.acm.org/doi/pdf/10.1145/3620665.3640389" |

**Covers:** References [1]–[27] of the survey bibliography (chunk 07/7)
