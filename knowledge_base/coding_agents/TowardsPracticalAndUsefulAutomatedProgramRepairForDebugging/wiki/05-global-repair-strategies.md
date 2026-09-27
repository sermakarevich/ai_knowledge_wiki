[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# REFERENCES — International Conference on Software Engineering (bibliography [1]–[47])
**In one sentence:** This chunk is the paper's bibliography entries [1]–[47] on automated program repair, fault localization, debugging, and related empirical studies, with no argumentative prose beyond the citation records and a footer line.
## Key points
- The chunk contains numbered bibliography entries [1] through [47], with entry [47] truncated mid-title ("Keep the Conversation Go-ing: Fixing 162 out of 337 bugs for $0.42 each using ChatGPT.").
- Publication years in the chunk range from 2008 ([18] Ko and Myers) to 2024 ([7] Eladawy et al.; [36] RepairTools 2024).
- Venues named include ICSE, ASE, ISSTA, FSE/ESEC-FSE, OOPSLA, TOSEM, TSE, Commun. ACM, CSUR, ICST, Quality Software, APR workshop, SEEDE/ASE, and arXiv preprints.
- APR approaches cited include template-based TBar [24], semantics/symbolic Angelix [26], GenProg [22], search-based anti-patterns [40], multi-hunk evolution [37], VarFix [44], context-aware patch generation [43], and bug-report-driven iFixR [20].
- Learning/LLM-based repair cited includes Getafix [2], CURE [14], DEAR [23], ChatGPT bug-fixing performance [39], Copiloting the Copilots [42], zero-shot repair [46], large pre-trained LM repair [45], fine-tuning study [10], code-LM impact [13], and patch prioritization with language models [16].
- Empirical/foundational entries include Defects4J [15], patch plausibility vs. correctness [32], overfitting in repair [38] and in semantics-based repair [21], test-suite efficiency [25], single-fault-fix prevalence [31], developer testing behavior [4] and test adoption [19], plus debugging UI work Code Bubbles [5], Whyline-style debugging [18], and reversible debugging [6].
- Author self-citations present are Reiss/Xin SEEDE [35], Quick Repair Facility [34], Quick Repair of Semantic Errors [33], alongside surveys/bibliographies E-APR mapping [1], APR survey [11], CACM APR overview [9], APR bibliography [28], and Living Review [29].
---
## Bibliographic block as given
> "REFERENCES                                                                                       International Conference on Software Engineering (ICSE). IEEE/ACM, 25–27."

| Ref | Authors (year) — verbatim title — venue as in chunk |
|---|---|
| [1] | Aldeida Aleti and Matias Martinez. 2021. E-APR: Mapping the effectiveness of automated program repair techniques. Empirical Software Engineering 26 (2021), 1–30. |
| [2] | Johannes Bader, Andrew Scott, Michael Pradel, and Satish Chandra. 2019. Getafix: Learning to fix bugs automatically. Proceedings of the ACM on Programming Languages 3, OOPSLA (2019), 1–27. |
| [3] | Rohan Bavishi, Hiroaki Yoshida, and Mukul R Prasad. 2019. Phoenix: Automated data-driven synthesis of repairs for static analysis violations. In Proceedings of the 27th ACM Joint Meeting on the Foundations of Software Engineering. 613–624. |
| [4] | Moritz Beller, Georgios Gousios, Annibale Panichella, and Andy Zaidman. 2015. When, how, and why developers (do not) test in their IDEs. In Proceedings of the 10th Joint Meeting on the Foundations of Software Engineering. 179–190. |
| [5] | Andrew Bragdon et al. 2010. Code bubbles: rethinking the user interface paradigm of integrated development environments. In Proceedings of the 32nd ACM/IEEE International Conference on Software Engineering-Volume 1. 455–464. |
| [6] | Tom Britton et al. 2013. Reversible debugging software. Judge Bus. School, Univ. Cambridge, Cambridge, UK, Tech. Rep 229 (2013). |
| [7] | Hadeel Eladawy, Claire Le Goues, and Yuriy Brun. 2024. Automated Program Repair, What Is It Good For? Not Absolutely Nothing!. In 2024 IEEE/ACM 46th International Conference on Software Engineering (ICSE). IEEE Computer Society, 868–868. |
| [8] | Xiang Gao et al. 2021. Beyond tests: Program vulnerability repair via crash constraint extraction. ACM Transactions on Software Engineering and Methodology (TOSEM) 30, 2 (2021), 1–27. |
| [9] | Claire Le Goues, Michael Pradel, and Abhik Roychoudhury. 2019. Automated program repair. Commun. ACM 62, 12 (2019), 56–65. |
| [10] | Kai Huang et al. 2023. An empirical study on fine-tuning large language models of code for automated program repair. In 2023 38th IEEE/ACM International Conference on Automated Software Engineering (ASE). IEEE, 1162–1174. |
| [11] | Kai Huang et al. 2023. A survey on automated program repair techniques. arXiv preprint arXiv:2303.18184 (2023). |
| [12] | Jiajun Jiang et al. 2018. Shaping program repair space with existing patches and similar code. In Proceedings of ACM 27th SIGSOFT International Symposium on Software Testing and Analysis (ISSTA). ACM, 298–309. |
| [13] | Nan Jiang, Kevin Liu, Thibaud Lutellier, and Lin Tan. 2023. Impact of code language models on automated program repair. arXiv preprint arXiv:2302.05020 (2023). |
| [14] | Nan Jiang, Thibaud Lutellier, and Lin Tan. 2021. CURE: Code-aware neural machine translation for automatic program repair. In Proceedings of IEEE/ACM 43rd International Conference on Software Engineering (ICSE). IEEE/ACM, 1161–1173. |
| [15] | René Just, Darioush Jalali, and Michael D Ernst. 2014. Defects4J: A database of existing faults to enable controlled testing studies for Java programs. In Proceedings of ACM 23rd SIGSOFT International Symposium on Software Testing and Analysis (ISSTA). ACM, 437–440. |
| [16] | Sungmin Kang and Shin Yoo. 2022. Language models can prioritize patches for practical program patching. In Proceedings of the Third International Workshop on Automated Program Repair. 8–15. |
| [17] | Dongsun Kim et al. 2013. Automatic patch generation learned from human-written patches. In Proceedings of the 35th International Conference on Software Engineering (ICSE). IEEE, 802–811. |
| [18] | Amy J Ko and Brad A Myers. 2008. Debugging reinvented: asking and answering why and why not questions about program behavior. In Proceedings of the 30th international conference on Software engineering. 301–310. |
| [19] | Pavneet Singh Kochhar et al. 2013. An empirical study of adoption of software testing in open source projects. In Proceedings of 13th International Conference on Quality Software. 103–112. |
| [20] | Anil Koyuncu et al. 2019. iFixR: Bug report driven program repair. In Proceedings of the 27th ACM Joint Meeting on the Foundations of Software Engineering. 314–325. |
| [21] | Xuan-Bach D Le et al. 2018. Overfitting in semantics-based automated program repair. In Proceedings of the 40th international conference on software engineering. 163–163. |
| [22] | Claire Le Goues et al. 2011. GenProg: A generic method for automatic software repair. IEEE Transactions on Software Engineering (TSE) 38, 1 (2011), 54–72. |
| [23] | Yi Li, Shaohua Wang, and Tien N Nguyen. 2022. DEAR: A novel deep learning-based approach for automated program repair. In Proceedings of IEEE/ACM 44th SE 2030 (chunk line truncates venue details). |
| [24] | Kui Liu et al. 2019. TBar: Revisiting template-based automated program repair. In Proceedings of ACM 28th SIGSOFT International Symposium on Software Testing and Analysis (ISSTA). ACM, 31–42. |
| [25] | Kui Liu et al. 2020. On the efficiency of test suite based program repair. In Proceedings of International Conference on Software Engineering. 615–627. |
| [26] | Sergey Mechtaev, Jooyong Yi, and Abhik Roychoudhury. 2016. Angelix: Scalable multiline program patch synthesis via symbolic analysis. In Proceedings of IEEE/ACM 38th International Conference on Software Engineering (ICSE). IEEE/ACM, 691–701. |
| [27] | Xiangxin Meng et al. 2022. Improving fault localization and program repair with deep semantic features and transferred knowledge. In Proceedings of the 44th International Conference on Software Engineering (ICSE). IEEE/ACM, 1169–1180. |
| [28] | Martin Monperrus. 2018. Automatic software repair: A bibliography. ACM Computing Surveys (CSUR) 51, 1 (2018), 1–24. |
| [29] | Martin Monperrus. 2018. The Living review on automated program repair. Technical Report hal-01956501. HAL/archives-ouvertes.fr. |
| [30] | Yannic Noller et al. 2022. Trust enhancement issues in program repair. In Proceedings of the 44th International Conference on Software Engineering. 2228–2240. |
| [31] | Alexandre Perez, Rui Abreu, and Marcelo d'Amorim. 2017. Prevalence of single-fault fixes and its impact on fault localization. In 2017 IEEE International Conference on Software Testing, Verification and Validation (ICST). IEEE, 12–22. |
| [32] | Zichao Qi et al. 2015. An analysis of patch plausibility and correctness for generate-and-validate patch generation systems. In Proceedings of ACM 24th SIGSOFT International Symposium on Software Testing and Analysis (ISSTA). ACM, 24–36. |
| [33] | Steven P Reiss, Xuan Wei, and Qi Xin. 2023. Quick Repair of Semantic Errors for Debugging. In 2023 IEEE/ACM International Workshop on Automated Program Repair (APR). IEEE, 9–10. |
| [34] | Steven P Reiss and Qi Xin. 2022. A Quick Repair Facility for Debugging. arXiv preprint arXiv:2202.05577 (2022). |
| [35] | Steven P Reiss, Qi Xin, and Jeff Huang. 2018. SEEDE: simultaneous execution and editing in a development environment. In Proceedings of 33rd IEEE/ACM International Conference on Automated Software Engineering. 270–281. |
| [36] | RepairTools 2024. Program Repair Tools. https://program-repair.org/tools.html |
| [37] | Seemanta Saha, Ripon k. Saha, and Mukul r. Prasad. 2019. Harnessing evolution for multi-hunk program repair. In Proceedings of IEEE/ACM 41st International Conference on Software Engineering (ICSE). IEEE/ACM, 13–24. |
| [38] | Edward K Smith et al. 2015. Is the cure worse than the disease? overfitting in automated program repair. In Proceedings of ACM 10th Joint Meeting on Foundations of Software Engineering (FSE). ACM, 532–543. |
| [39] | Dominik Sobania et al. 2023. An analysis of the automatic bug fixing performance of chatgpt. arXiv preprint arXiv:2301.08653 (2023). |
| [40] | Shin Hwei Tan et al. 2016. Anti-patterns in search-based program repair. In Proceedings of the 2016 24th ACM SIGSOFT International Symposium on Foundations of Software Engineering. 727–738. |
| [41] | Rijnard van Tonder and Claire Le Goues. 2018. Static automated program repair for heap properties. In Proceedings of the 40th International Conference on Software Engineering. 151–162. |
| [42] | Yuxiang Wei, Chunqiu Steven Xia, and Lingming Zhang. 2023. Copiloting the Copilots: Fusing Large Language Models with Completion Engines for Automated Program Repair. arXiv preprint arXiv:2309.00608 (2023). |
| [43] | Ming Wen et al. 2018. Context-aware patch generation for better automated program repair. In Proceedings of IEEE/ACM 40th International Conference on Software Engineering. 1–11. |
| [44] | Chu-Pan Wong et al. 2021. VarFix: Balancing edit expressiveness and search effectiveness in automated program repair. In Proceedings of ACM 29th Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE). ACM, 354–366. |
| [45] | Chunqiu Steven Xia, Yuxiang Wei, and Lingming Zhang. 2023. Automated program repair in the era of large pre-trained language models. In Proceedings of the 45th International Conference on Software Engineering (ICSE 2023). Association for Computing Machinery. |
| [46] | Chunqiu Steven Xia and Lingming Zhang. 2022. Less training, more repairing please: revisiting automated program repair via zero-shot learning. In Proceedings of the 30th ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering. 959–971. |
| [47] | Chunqiu Steven Xia and Lingming Zhang. 2023. Keep the Conversation Going: Fixing 162 out of 337 bugs for $0.42 each using ChatGPT (chunk truncates here; full venue/pages not present in chunk). |

## Footer line in chunk
> "SE 2030, November 2024, Puerto Galinàs (Brazil)                                                                           Qi Xin, Haojun Wu, Steven P. Reiss, and Jifeng Xuan"

Note: plan.md maps this chunk slug to page `05-global-repair-strategies.md` with Covers "Single-fault multi-location bugs, 8 partial-patch relationships, tailored global-repair strategies", but the chunk body supplied contains only the bibliography above and no global-repair discussion.

**Covers:** REFERENCES section, bibliography entries [1]–[47]
