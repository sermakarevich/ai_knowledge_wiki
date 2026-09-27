[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Conclusion and References
**In one sentence:** This chunk is the paper's bibliography tail (references [24]–[61] plus the ICSE '24 venue line), listing the LLM-based, learning-based, and classic APR works cited by PracRepair.
## Key points
- Xia and Zhang [24] revisit APR via zero-shot learning (ESEC/FSE 2022, pages 959–971) under the title "Less training, more repairing please".
- Xia and Zhang [25] report conversation-based repair fixing "162 out of 337 bugs for $0.42 each using chatgpt" (ISSTA 2024, pages 819–831).
- Bouzenia, Devanbu, and Pradel [26] present "Repairagent: An autonomous, llm-based agent for program repair" (ICSE '25, pages 2188–2200).
- Yin et al. [27] present "Thinkrepair: Self-directed automated program repair" (ISSTA 2024, pages 1274–1286).
- Zhang et al. [28] propose improving LLM-based repair "via repair ingredients search" (2025 preprint).
- Huang et al. [29] survey "Evolving paradigms in automated program repair: Taxonomy, challenges, and opportunities" (ACM Comput. Surv., 57(2), October 2024).
- Kolak et al. [30] study "Patch generation with language models: Feasibility and scaling behavior" (Deep Learning for Code Workshop, 2022).
- The tail [44]–[61] spans classic and neural repair baselines cited by the paper, from GenProg [46] and SemFix [49] through SequenceR-style NMT repair [57], DLFix [59], and execution-based backpropagation [60] to the ICSE '23 LLM impact study [61].
---
## LLM-based APR references ([24]–[31])
**Covers:** References [24]–[31]

| # | Citation (verbatim details) |
|---|---|
| [24] | Chunqiu Steven Xia and Lingming Zhang. "Less training, more repairing please: revisiting automated program repair via zero-shot learning." In Proceedings of the 30th ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering, ESEC/FSE 2022, page 959–971, New York, NY, USA, 2022. Association for Computing Machinery. |
| [25] | Chunqiu Steven Xia and Lingming Zhang. "Automated program repair via conversation: Fixing 162 out of 337 bugs for $0.42 each using chatgpt." In Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis, ISSTA 2024, page 819–831, New York, NY, USA, 2024. Association for Computing Machinery. |
| [26] | Islem Bouzenia, Premkumar Devanbu, and Michael Pradel. "Repairagent: An autonomous, llm-based agent for program repair." In Proceedings of the IEEE/ACM 47th International Conference on Software Engineering, ICSE '25, page 2188–2200. IEEE Press, 2025. |
| [27] | Xin Yin, Chao Ni, Shaohua Wang, Zhenhao Li, Limin Zeng, and Xiaohu Yang. "Thinkrepair: Self-directed automated program repair." In Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis, ISSTA 2024, page 1274–1286, New York, NY, USA, 2024. Association for Computing Machinery. |
| [28] | Jiayi Zhang, Kai Huang, Jian Zhang, Yang Liu, and Chunyang Chen. "Repair ingredients are all you need: Improving large language model-based program repair via repair ingredients search, 2025." |
| [29] | Kai Huang, Zhengzi Xu, Su Yang, Hongyu Sun, Xuejun Li, Zheng Yan, and Yuqing Zhang. "Evolving paradigms in automated program repair: Taxonomy, challenges, and opportunities." ACM Comput. Surv., 57(2), October 2024. |
| [30] | Sophia D Kolak, Ruben Martins, Claire Le Goues, and Vincent Josua Hellendoorn. "Patch generation with language models: Feasibility and scaling behavior." In Deep Learning for Code Workshop, 2022. |
| [31] | Julian Aron Prenner, Hlib Babii, and Romain Robbes. "Can openai's codex fix bugs?: An evaluation on quixbugs." In 2022 IEEE/ACM International Workshop on Automated Program Repair (APR), pages 69–75, 2022. |

## Tooling, models, and methodological references ([32]–[45])
**Covers:** References [32]–[45]

| # | Citation (verbatim details) |
|---|---|
| [32] | joernio. "Joern: The bug hunter's workbench." https://github.com/joernio/joern, 2024. Accessed: 2026-03-06. |
| [33] | Fabian Yamaguchi, Nico Golde, Daniel Arp, and Konrad Rieck. "Modeling and discovering vulnerabilities with code property graphs." In 2014 IEEE Symposium on Security and Privacy, pages 590–604, 2014. |
| [34] | Raffi Khatchadourian, Yiming Tang, Mehdi Bagherzadeh, and Syed Ahmed. "Safe automated refactoring for intelligent parallelization of java 8 streams." In 2019 IEEE/ACM 41st International Conference on Software Engineering (ICSE), pages 619–630, 2019. |
| [35] | Oracle. "Package java.lang.instrument. Java Platform, Standard Edition API Specification." Accessed: 2026-03-06. |
| [36] | Romain Lenglet. "Asm: a code manipulation tool to implement adaptable systems." Adaptable and extensible..., 2002. |
| [37] | Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. "ReAct: Synergizing reasoning and acting in language models." In International Conference on Learning Representations (ICLR), 2023. |
| [38] | Anonymous Authors. "Artifact: Source code, prompts, datasets, and experimental results for this paper." https://doi.org/10.5281/zenodo.19336422, 2026. Anonymous research artifact. |
| [39] | OpenAI. "gpt-3.5-turbo-0125." https://developers.openai.com/api/docs/models#gpt-3-5-turbo, September 2023. Accessed: 2025-09-29. |
| [40] | OpenAI. "Gpt-4o-2024-05-13: Openai's next-generation language model." https://developers.openai.com/api/docs/models#gpt-4-turbo-and-gpt-4, September 2023. Accessed: 2025-09-29. |
| [41] | Fabrizio Gilardi, Meysam Alizadeh, and Maël Kubli. "Chatgpt outperforms crowd workers for text-annotation tasks." Proceedings of the National Academy of Sciences, 120(30):e2305016120, 2023. |
| [42] | OpenAI. "GPT-4." https://developers.openai.com/api/docs/models/gpt-4, 2023. OpenAI API documentation. |
| [43] | Ollama. "Meta Llama 3: The Most Capable Openly Available LLM to Date." https://ollama.com/library/llama3, 2024. |
| [44] | DeepSeek AI. "DeepSeek Coder: Let the Code Write Itself." https://github.com/deepseek-ai/DeepSeek-Coder, 2023. GitHub repository. |
| [45] | Chunqiu Steven Xia, Yuxiang Wei, and Lingming Zhang. "Automated program repair in the era of large pre-trained language models, 2023." |

## Classic, data-driven, and neural repair references ([46]–[61])
**Covers:** References [46]–[61] plus the ICSE '24 venue line

| # | Citation (verbatim details) |
|---|---|
| Venue line | "Conference on Software Engineering, ICSE '24, New York, NY, USA, 2024. Association for Computing Machinery." |
| [46] | Claire Le Goues, ThanhVu Nguyen, Stephanie Forrest, and Westley Weimer. "Genprog: A generic method for automatic software repair." IEEE Transactions on Software Engineering, 38(1):54–72, 2012. |
| [47] | Dongsun Kim, Jaechang Nam, Jaewoo Song, and Sunghun Kim. "Automatic patch generation learned from human-written patches." In Proceedings of the 2013 International Conference on Software Engineering, ICSE '13, page 802–811. IEEE Press, 2013. |
| [48] | Rohan Bavishi, Hiroaki Yoshida, and Mukul R. Prasad. "Phoenix: automated data-driven synthesis of repairs for static analysis violations." In Proceedings of the 2019 27th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering, ESEC/FSE 2019, page 613–624, New York, NY, USA, 2019. Association for Computing Machinery. |
| [49] | Hoang Duong Thien Nguyen, Dawei Qi, Abhik Roychoudhury, and Satish Chandra. "Semfix: program repair via semantic analysis." In Proceedings of the 2013 International Conference on Software Engineering, ICSE '13, page 772–781. IEEE Press, 2013. |
| [50] | Xusheng Xiao, Sihan Li, Tao Xie, and Nikolai Tillmann. "Characteristic studies of loop problems for structural test generation via symbolic execution." In Proceedings of the 28th IEEE/ACM International Conference on Automated Software Engineering, ASE '13, page 246–256. IEEE Press, 2013. |
| [51] | Yu Liu, Sergey Mechtaev, Pavle Subotić, and Abhik Roychoudhury. "Program repair guided by datalog-defined static analysis." In Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering, ESEC/FSE 2023, page 1216–1228, New York, NY, USA, 2023. Association for Computing Machinery. |
| [52] | Alexandru Marginean, Johannes Bader, Satish Chandra, Mark Harman, Yue Jia, Ke Mao, Alexander Mols, and Andrew Scott. "Sapfix: Automated end-to-end repair at scale." In 2019 IEEE/ACM 41st International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP), pages 269–278, 2019. |
| [53] | Rahul Gupta, Aditya Kanade, and Shirish Shevade. "Deep reinforcement learning for syntactic error repair in student programs." In Proceedings of the Thirty-Third AAAI Conference on Artificial Intelligence and Thirty-First Innovative Applications of Artificial Intelligence Conference and Ninth AAAI Symposium on Educational Advances in Artificial Intelligence, AAAI'19/IAAI'19/EAAI'19. AAAI Press, 2019. |
| [54] | Daniel Tarlow, Subhodeep Moitra, Andrew Rice, Zimin Chen, Pierre-Antoine Manzagol, Charles Sutton, and Edward Aftandilian. "Learning to fix build errors with graph2diff neural networks." In Proceedings of the IEEE/ACM 42nd International Conference on Software Engineering Workshops, ICSEW'20, page 19–20, New York, NY, USA, 2020. Association for Computing Machinery. |
| [55] | Fan Long and Martin Rinard. "Automatic patch generation by learning correct code." In Proceedings of the 43rd Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL '16, page 298–312, New York, NY, USA, 2016. Association for Computing Machinery. |
| [56] | Rahul Gupta, Soham Pal, Aditya Kanade, and Shirish Shevade. "Deepfix: fixing common c language errors by deep learning." In Proceedings of the Thirty-First AAAI Conference on Artificial Intelligence, AAAI'17, page 1345–1351. AAAI Press, 2017. |
| [57] | Michele Tufano, Jevgenija Pantiuchina, Cody Watson, Gabriele Bavota, and Denys Poshyvanyk. "On learning meaningful code changes via neural machine translation." In Proceedings of the 41st International Conference on Software Engineering, ICSE '19, page 25–36. IEEE Press, 2019. |
| [58] | Qihao Zhu, Zeyu Sun, Yuan-an Xiao, Wenjie Zhang, Kang Yuan, Yingfei Xiong, and Lu Zhang. "A syntax-guided edit decoder for neural program repair." In Proceedings of the 29th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering, ESEC/FSE 2021, page 341–353, New York, NY, USA, 2021. Association for Computing Machinery. |
| [59] | Yi Li, Shaohua Wang, and Tien N. Nguyen. "Dlfix: context-based code transformation learning for automated program repair." In Proceedings of the ACM/IEEE 42nd International Conference on Software Engineering, ICSE '20, page 602–614, New York, NY, USA, 2020. Association for Computing Machinery. |
| [60] | He Ye, Matias Martinez, and Martin Monperrus. "Neural program repair with execution-based backpropagation." In Proceedings of the 44th International Conference on Software Engineering, ICSE '22, page 1506–1518, New York, NY, USA, 2022. Association for Computing Machinery. |
| [61] | Nan Jiang, Kevin Liu, Thibaud Lutellier, and Lin Tan. "Impact of code language models on automated program repair." In Proceedings of the 45th International Conference on Software Engineering, ICSE '23, page 1430–1442. IEEE Press, 2023. |
