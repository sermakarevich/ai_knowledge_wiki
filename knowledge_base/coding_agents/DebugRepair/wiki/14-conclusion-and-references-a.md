> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Conclusion and References (Part A: [1]–[32])

**In one sentence:** This chunk contains no conclusion prose — only the first half of the bibliography (references [1]–[32]), spanning model/infrastructure sources, classic APR methods, and recent LLM-based APR work.

## Key points

- The chunk lists references [1]–[32] verbatim, with no conclusion, discussion, or open-science text present in the chunk body.
- References [1]–[3] are online sources: OpenAI Models docs (accessed 2026-01-20), SiliconFlow (accessed 2026-01-20), and tree-sitter (accessed 2026-03-13).
- References [4]–[11] cover recent LLM/agent-based APR work, including RepairAgent (2024), APRMCTS (2025), TSAPR (2025), and ContrastRepair (2025).
- References [12]–[25] cover classic and learning-based APR foundations: GenProg (2011), Defects4J (2014), Angelix (2016), Sequencer (2019), TBar (2019), and CURE/DLFix/DEAR/KNOD (2020–2023).
- References [26]–[32] cover benchmarks (QuixBugs 2017, SWE-bench 2023) and template/condition-based repair (Avatar 2019, Staged repair 2015, Astor 2016, RAP-Gen 2023).
- The chunk also carries journal page furniture ("J. ACM, Vol. 37, No. 4, Article 111", "111:26 Wu et al.", "111:27" running head) rather than paper content.
- Note: the planned page scope mentions a conclusion and open-science note, but neither appears in this chunk, so they are not summarised here.

---

## References [1]–[3]: models, infrastructure, parsing

Online sources cited:

| # | Citation |
|---|---|
| [1] | [n. d.]. Models \| OpenAI API. https://platform.openai.com/docs/models#gpt-3-5-turbo [Online; accessed 2026-01-20]. |
| [2] | [n. d.]. SiliconFlow – AI Infrastructure for LLMs & Multimodal Models. https://www.siliconflow.com/ [Online; accessed 2026-01-20]. |
| [3] | [n. d.]. tree-sitter/tree-sitter: An incremental parsing system for programming tools. https://github.com/tree-sitter/tree-sitter [Online; accessed 2026-03-13]. |

## References [4]–[11]: LLM-based and agent-based APR

| # | Citation |
|---|---|
| [4] | Islem Bouzenia, Premkumar Devanbu, and Michael Pradel. 2024. Repairagent: An autonomous, llm-based agent for program repair. arXiv preprint arXiv:2403.17134 (2024). |
| [5] | Mark Chen. 2021. Evaluating large language models trained on code. arXiv preprint arXiv:2107.03374 (2021). |
| [6] | Zimin Chen, Steve Kommrusch, Michele Tufano, Louis-Noël Pouchet, Denys Poshyvanyk, and Martin Monperrus. 2019. Sequencer: Sequence-to-sequence learning for end-to-end program repair. IEEE Transactions on Software Engineering 47, 9 (2019), 1943–1959. |
| [7] | Xiang Gao, Bo Wang, Gregory J Duck, Ruyi Ji, Yingfei Xiong, and Abhik Roychoudhury. 2021. Beyond tests: Program vulnerability repair via crash constraint extraction. ACM Transactions on Software Engineering and Methodology (TOSEM) 30, 2 (2021), 1–27. |
| [8] | Luca Gazzola, Daniela Micucci, and Leonardo Mariani. 2018. Automatic software repair: A survey. In Proceedings of the 40th International Conference on Software Engineering. 1219–1219. |
| [9] | Ali Ghanbari, Samuel Benton, and Lingming Zhang. 2019. Practical program repair via bytecode mutation. In Proceedings of the 28th ACM SIGSOFT International Symposium on Software Testing and Analysis. 19–30. |
| [10] | Haichuan Hu, Congqing He, Hao Zhang, Xiaochen Xie, and Quanjun Zhang. 2025. APRMCTS: Improving LLM-based Automated Program Repair with Iterative Tree Search. arXiv preprint arXiv:2507.01827 (2025). |
| [11] | Haichuan Hu, Ye Shang, Weifeng Sun, and Quanjun Zhang. 2025. TSAPR: A Tree Search Framework For Automated Program Repair. arXiv preprint arXiv:2507.01827 (2025). |

## References [12]–[25]: classic, template-based, and neural APR

| # | Citation |
|---|---|
| [12] | Jinru Hua, Mengshi Zhang, Kaiyuan Wang, and Sarfraz Khurshid. 2018. Sketchfix: a tool for automated program repair approach using lazy candidate generation. In Proceedings of the 2018 26th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering. 888–891. |
| [13] | Jiajun Jiang, Yingfei Xiong, Hongyu Zhang, Qing Gao, and Xiangqun Chen. 2018. Shaping program repair space with existing patches and similar code. In Proceedings of the 27th ACM SIGSOFT international symposium on software testing and analysis. 298–309. |
| [14] | Nan Jiang, Kevin Liu, Thibaud Lutellier, and Lin Tan. 2023. Impact of code language models on automated program repair. In 2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE). IEEE, 1430–1442. |
| [15] | Nan Jiang, Thibaud Lutellier, Yiling Lou, Lin Tan, Dan Goldwasser, and Xiangyu Zhang. 2023. Knod: Domain knowledge distilled tree decoder for automated program repair. In 2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE). IEEE, 1251–1263. |
| [16] | Nan Jiang, Thibaud Lutellier, and Lin Tan. 2021. Cure: Code-aware neural machine translation for automatic program repair. In 2021 IEEE/ACM 43rd International Conference on Software Engineering (ICSE). IEEE, 1161–1173. |
| [17] | Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik Narasimhan. 2023. Swe-bench: Can language models resolve real-world github issues? arXiv preprint arXiv:2310.06770 (2023). |
| [18] | René Just, Darioush Jalali, and Michael D Ernst. 2014. Defects4J: A database of existing faults to enable controlled testing studies for Java programs. In Proceedings of the 2014 international symposium on software testing and analysis. 437–440. |
| [19] | Jiaolong Kong, Xiaofei Xie, Mingfei Cheng, Shangqing Liu, Xiaoning Du, and Qi Guo. 2025. Contrastrepair: Enhancing conversation-based automated program repair via contrastive test case pairs. ACM Transactions on Software Engineering and Methodology 34, 8 (2025), 1–31. |
| [20] | Xuan-Bach D Le, Duc-Hiep Chu, David Lo, Claire Le Goues, and Willem Visser. 2017. S3: syntax-and semantic-guided repair synthesis via programming by examples. In Proceedings of the 2017 11th Joint Meeting on Foundations of Software Engineering. 593–604. |
| [21] | Xuan Bach D Le, David Lo, and Claire Le Goues. 2016. History driven program repair. In 2016 IEEE 23rd international conference on software analysis, evolution, and reengineering (SANER), Vol. 1. IEEE, 213–224. |
| [22] | Claire Le Goues, ThanhVu Nguyen, Stephanie Forrest, and Westley Weimer. 2011. Genprog: A generic method for automatic software repair. Ieee transactions on software engineering 38, 1 (2011), 54–72. |
| [23] | Claire Le Goues, Michael Pradel, and Abhik Roychoudhury. 2019. Automated program repair. Commun. ACM 62, 12 (2019), 56–65. |
| [24] | Yi Li, Shaohua Wang, and Tien N Nguyen. 2020. Dlfix: Context-based code transformation learning for automated program repair. In Proceedings of the ACM/IEEE 42nd international conference on software engineering. 602–614. |
| [25] | Yi Li, Shaohua Wang, and Tien N Nguyen. 2022. Dear: A novel deep learning-based approach for automated program repair. In Proceedings of the 44th international conference on software engineering. 511–523. |

## References [26]–[32]: benchmarks and synthesis-based repair

| # | Citation |
|---|---|
| [26] | Derrick Lin, James Koppel, Angela Chen, and Armando Solar-Lezama. 2017. QuixBugs: A multi-lingual program repair benchmark set based on the Quixey Challenge. In Proceedings Companion of the 2017 ACM SIGPLAN international conference on systems, programming, languages, and applications: software for humanity. 55–56. |
| [27] | Kui Liu, Anil Koyuncu, Dongsun Kim, and Tegawendé F Bissyandé. 2019. Avatar: Fixing semantic bugs with fix patterns of static analysis violations. In 2019 IEEE 26th International Conference on Software Analysis, Evolution and Reengineering (SANER). IEEE, 1–12. |
| [28] | Kui Liu, Anil Koyuncu, Dongsun Kim, and Tegawendé F Bissyandé. 2019. TBar: Revisiting template-based automated program repair. In Proceedings of the 28th ACM SIGSOFT international symposium on software testing and analysis. 31–42. |
| [29] | Fan Long and Martin Rinard. 2015. Staged program repair with condition synthesis. In Proceedings of the 2015 10th Joint Meeting on Foundations of Software Engineering. 166–178. |
| [30] | Matias Martinez and Martin Monperrus. 2016. Astor: A program repair library for java. In Proceedings of the 25th international symposium on software testing and analysis. 441–444. |
| [31] | Sergey Mechtaev, Jooyong Yi, and Abhik Roychoudhury. 2016. Angelix: Scalable multiline program patch synthesis via symbolic analysis. In Proceedings of the 38th international conference on software engineering. 691–701. |
| [32] | Weishi Wang, Yue Wang, Shafiq Joty, and Steven CH Hoi. 2023. Rap-gen: Retrieval-augmented patch generation with codet5 for automatic program repair. In Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering. 146–158. |

**Covers:** References [1]–[32] (first half of the bibliography); no conclusion or body prose present in this chunk.
