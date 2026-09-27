# Open Ontologies: Tool-Augmented Ontology Engineering with Stable Matching Alignment
Source: https://arxiv.org/abs/2605.09184v1
Kind: pdf
Fetched: 2026-09-23T12:58:26.092086+00:00
Tool: pdftotext
Research-Target: /Users/sergii/.ai/knowledge/research_topics/ontology_ai/research/ontology-ai
Topic: ontology_ai

                                            Open Ontologies: Tool-Augmented Ontology
                                            Engineering with Stable Matching Alignment

                                                                          Fabio Rovai1

                                                        The Tesseract Academy, London, United Kingdom
                                                               fabio@thetesseractacademy.com




arXiv:2605.09184v1 [cs.AI] 9 May 2026
                                              Abstract. We present Open Ontologies, an open-source ontology en-
                                              gineering system implemented in Rust that integrates LLM-driven con-
                                              struction with formal OWL reasoning and ontology alignment via the
                                              Model Context Protocol. Our primary finding is that stable 1-to-1 match-
                                              ing is the dominant factor in ontology alignment quality: on the OAEI
                                              Anatomy track, it achieves F1 = 0.832 (P = 0.963, R = 0.733), competi-
                                              tive with state-of-the-art systems and exceeding all in precision. Abla-
                                              tion across five weight configurations shows that signal weights are ir-
                                              relevant when stable matching is applied (F1 varies by less than 0.004),
                                              while removing stable matching drops F1 to 0.728. On the Conference
                                              track, the same method achieves F1 = 0.438. On tool-augmented ontol-
                                              ogy interaction, we find a surprising result: an LLM reading a raw OWL
                                              file (F1 = 0.323) performs worse than the same LLM with no file at all
                                              (F1 = 0.431), while structured MCP tool access achieves F1 = 0.717. This
                                              demonstrates that tool structure provides a qualitatively different mode
                                              of access that the LLM cannot replicate by reading raw syntax. The
                                              system ships as a single binary under the MIT licence.

                                              Keywords: Ontology engineering · Ontology alignment · Stable match-
                                              ing · Large language models · Model Context Protocol · OWL reasoning.



                                        1    Introduction

                                        LLMs can generate syntactically valid OWL and orchestrate multi-step ontology
                                        engineering workflows. They cannot, however, guarantee logical consistency or
                                        verify that generated axioms are mutually coherent. Separately, ontology align-
                                        ment systems achieve strong pairwise matching on standard benchmarks but
                                        operate as standalone pipelines, disconnected from construction workflows and
                                        lifecycle management.
                                            We present Open Ontologies, an open-source system that addresses both
                                        gaps. The system exposes ontology construction, reasoning, alignment, and life-
                                        cycle tools via the Model Context Protocol (MCP) [8], enabling integrated work-
                                        flows where an LLM generates OWL, validates it against formal constraints, and
                                        refines based on symbolic feedback.
                                            We present three contributions:
2      F. Rovai

1. A stable matching alignment method that achieves F1 = 0.832 on OAEI
   Anatomy (P = 0.963), exceeding all published systems in precision. Ablation
   shows that the matching constraint is the dominant factor: signal weights
   are irrelevant when stable matching is applied. On the Conference track, the
   method achieves F1 = 0.438.
2. A tool access ablation revealing that an LLM reading a raw OWL file
   (F1 = 0.323) performs worse than unaided inference (F1 = 0.431), while struc-
   tured MCP tools achieve F1 = 0.717. This disentangles the effect of tool
   structure from information availability.
3. Open Ontologies: an open-source, Rust-based system integrating OWL-RL
   reasoning, alignment, and lifecycle management into an LLM-orchestrated
   workflow.



2   Related Work

Ontology matching. The OAEI [3] benchmarks alignment systems annually.
LogMap [4] combines lexical matching with structural repair and logical consis-
tency checking. AML [5] uses background knowledge from BioPortal and UMLS.
BERTMap [6] introduced transformer-based embedding matching. OLaLa [7]
uses LLM world knowledge for candidate adjudication. Our alignment module
differs in demonstrating that the matching constraint (1-to-1 assignment) dom-
inates signal design.


OWL reasoning. HermiT [2] implements hypertableau calculus for OWL2-DL.
Pellet [10] and FaCT++ [11] provide alternative implementations. ELK [12]
achieves polynomial-time reasoning for the EL profile. All are Java-based. Our
system provides Rust-native OWL-RL forward chaining with a partial SHIQ
tableaux for consistency checking.


AI-assisted ontology construction. OntoGPT [13] extracts ontology terms from
text. OntoChat [14] provides conversational construction. LLMs4OL [15] evalu-
ates LLMs for ontology learning. OntoAxiom [1] benchmarks axiom identifica-
tion across 9 ontologies, finding that even o1 achieves only F1 = 0.197 from name
lists. None integrate formal validation into the construction loop or evaluate the
effect of tool access modality on extraction quality.


Programmatic ontology engineering. The OWL API [19] provides the Java foun-
dation for most ontology tools. ROBOT [20] offers command-line management
for the OBO community. Owlready2 [21] provides Python-based manipulation.
SSSOM [22] standardises mapping formats. These target expert users; our sys-
tem targets LLM-orchestrated workflows.
                   Open Ontologies: Tool-Augmented Ontology Engineering           3

3     System Architecture
Open Ontologies is implemented in Rust (∼17,400 lines of code) and ships
as a single binary with no JVM or Python dependency. The system exposes
ontology construction, reasoning, alignment, and lifecycle tools via MCP [8].

3.1   Core Engine
The core engine comprises: (1) an Oxigraph triple store [9] providing in-
memory SPARQL 1.1 query and update; (2) a native reasoner with two modes:
OWL-RL forward-chaining rules [23] for triple materialisation, and a partial
SHIQ tableaux for consistency checking; (3) a SHACL validator for shape
constraints; and (4) a pattern enforcer with configurable rule packs.

3.2   Alignment Module
The alignment engine computes a weighted similarity score for each candidate
class pair (cs , ct ):
                                             6
                                             X
                         score(cs , ct ) =         wi · si (cs , ct )           (1)
                                             i=1

The six signals are: (1) label similarity (Jaro-Winkler + token Jaccard, w1 =
0.25); (2) property overlap (Jaccard, w2 = 0.20); (3) parent overlap (w3 =
0.15); (4) instance overlap (w4 = 0.15); (5) restriction similarity (w5 = 0.15);
(6) neighbourhood similarity (w6 = 0.10).
    When all structural signals (2–6) are zero, confidence falls back to label simi-
larity with a 15% penalty (label sim×0.85), preventing structurally unsupported
matches from passing the threshold.
    After scoring, stable 1-to-1 matching is applied: candidates are sorted by
confidence, and for each source class only the top-scoring target is retained (and
vice versa). This eliminates many-to-many spurious matches.

3.3   Lifecycle Management
Inspired by infrastructure-as-code [18]: plan (diff with blast-radius scoring),
enforce (design pattern compliance), apply (safe reload or migration), monitor
(SPARQL watchers with alerts), drift (version comparison). All operations
recorded in an append-only lineage trail.


4     Evaluation
Reproducibility. LLM benchmarks use Claude Opus 4 (Anthropic, model ID
claude-opus-4-20250514), default temperature. Single-run results. Non-LLM
benchmarks (LUBM, OAEI alignment, marketplace loading) are deterministic.
All scripts and data are in the repository under benchmark/.
4      F. Rovai

Table 1. OAEI Anatomy results. Our system achieves the highest precision, with a
recall gap due to the conservative label penalty.

                      System               P    R     F1
                      AML [5]            0.950 0.922 0.936
                      BERTMap [6]        0.940 0.910 0.924
                      LogMap [4]         0.930 0.890 0.912
                      OLaLa [7]          0.900 0.880 0.890
                      Open Ontologies 0.963 0.733 0.832



4.1   OAEI Alignment: Anatomy Track

On the OAEI Anatomy track [3] (2,737 mouse classes, 3,304 human classes, 1,516
reference mappings), our system achieves the highest precision of any reported
system.
    The initial system (before stable matching) produced 12,557 candidates with
P = 0.102, R = 0.846, F1 = 0.182. Three changes lifted performance: (a) stable
1-to-1 matching, eliminating many-to-many spurious candidates; (b) a label
penalty (label sim × 0.85) when structural signals are zero; and (c) raising the
label pre-filter from 0.70 to 0.75. Together these reduced candidates from 12,557
to 1,154.
    The recall gap (0.733 vs AML’s 0.922) has a clear cause: true matches with
low label similarity are penalised. Integrating domain-specific background knowl-
edge (UMLS, as LogMap and AML use) would allow accepting these matches
when supported by external evidence. The system’s alignment module accepts
pluggable similarity functions and can load domain-specific ONNX embedding
models.


4.2   OAEI Alignment: Conference Track

On the Conference track (7 ontologies, 21 pairwise alignments, 15 evaluated with
available data), the same method achieves micro-averaged F1 = 0.438 (P = 0.693,
R = 0.320).
    Precision remains reasonable (0.693), but recall is low (0.320) because con-
ference ontologies use heterogeneous modelling styles where label overlap is min-
imal.


4.3   Tool-Augmented Ontology Interaction

We use the OntoAxiom benchmark [1] (9 ontologies, 3,042 ground truth axioms,
5 types) to evaluate three access modalities. The original benchmark tests LLM
inference from name lists. We add two conditions: reading the raw OWL file,
and using MCP tools.
                   Open Ontologies: Tool-Augmented Ontology Engineering          5

Table 2. OAEI Conference track: per-pair results (selected). Published SOTA: LogMap
0.67, BERTMap 0.71.

                        Pair              Ref Cands F1
                        cmt-iasted        4     5    0.667
                        ekaw-iasted       10    7    0.588
                        ekaw-sigkdd       11    4    0.533
                        iasted-sigkdd     15    9    0.500
                        conference-edas   17    8    0.480
                        cmt-sigkdd        12    5    0.471
                        edas-sigkdd       15    4    0.211
                        Micro-average               0.438

Table 3. Tool access modalities on OntoAxiom. Condition D (raw file) performs worse
than Condition B (no file), demonstrating that raw syntax is not just unhelpful but
actively harmful.

                    Condition                  Input         F1
                 B LLM, no tools         Name lists   0.431
                 D LLM + raw OWL file File in context 0.323
                 C LLM + MCP tools   File via SPARQL 0.717



Why D ¡ B. The LLM reading raw Turtle makes systematic extraction errors,
particularly on domain/range triples (F1 = 0.0 on 4 of 9 ontologies for domain
extraction). The Turtle syntax is ambiguous to read: property IRIs are confused
with class IRIs, language tags cause mismatches, and multi-line axiom blocks
are missed. The LLM’s training knowledge (Condition B) is more accurate than
its ability to parse raw syntax (Condition D).

Per-ontology variance. Condition D performance varies widely: NordStream
F1 = 0.692, FOAF 0.647, GoodRelations 0.632 (simpler Turtle), but Time 0.087,
Pizza 0.154, ERA 0.058 (complex Turtle with restrictions, annotations, and large
file sizes).

Disentanglement. The improvement from B to C (+66% F1) combines two fac-
tors: richer input and structured tool access. Condition D isolates these: richer
input without tools hurts (−25% vs B), while structured tools provide +122%
over raw file access. MCP tools are not merely “richer input”; they provide a
qualitatively different access modality.


4.4   Reasoning Performance

We compare OWL-RL forward chaining against HermiT [2] on the LUBM bench-
mark [17]. These are different reasoning profiles producing different outputs.
6       F. Rovai

Table 4. LUBM reasoning: OWL-RL (polynomial, incomplete) vs HermiT (exponen-
tial, complete). Different profiles, different outputs.

                     Axioms OWL-RL HermiT Time ratio
                        1,000     15 ms      112 ms        7.5×
                        5,000     14 ms      410 ms        29×
                       10,000     14 ms     1,200 ms       86×
                       50,000     15 ms    24,490 ms      1,633×

Table 5. Ablation on OAEI Anatomy (min confidence = 0.80). Signal weights are ir-
relevant when stable matching is applied. All results verified and reproducible from
benchmark/oaei/run ablation.py.

       Stable Weights                                    Cands     P    R    F1
       Yes     Full [.25,.20,.15,.15,.15,.10]            1,152   0.965 0.734 0.834
       Yes     Label only [1,0,0,0,0,0]                  1,152   0.963 0.732 0.831
       Yes     Structural only [0,.25,.25,.20,.20,.10]   1,152   0.962 0.731 0.831
       Yes     Equal [.167 each]                         1,153   0.961 0.731 0.830
       Yes     Label+parent [.4,0,.4,0,0,.2]             1,154   0.964 0.734 0.833
       No      Full                                      1,590 0.711 0.746 0.728
       No      Label only                                1,590 0.711 0.746 0.728
       No      Structural only                           1,590 0.711 0.746 0.728



   On the Pizza ontology (4,179 triples), HermiT computes 312 subsumptions in
213 ms; our OWL-RL materialises inferred triples in 43 ms but does not compute
the same subsumptions. We do not claim to be a “faster HermiT.” OWL-RL
covers the inference patterns needed for engineering workflows at interactive
speeds.


4.5   Pizza Ontology Construction

Using the Manchester Pizza Tutorial [16] (∼4 hours manual work), LLM-driven
construction through the MCP tool pipeline produces a 91-class ontology in un-
der 5 minutes, achieving 96% class coverage (95/99 classes). The 4 missing classes
are teaching artifacts that exist only to demonstrate OWL syntax variants.


5     Ablation: Stable Matching Dominates Alignment

We test five weight configurations with stable matching enabled, and three with-
out (Table 5).

Finding: signal weights are irrelevant. All five configurations with stable match-
ing produce F1 between 0.830 and 0.834. All three without-stable-matching con-
figurations produce identical F1 = 0.728.
                   Open Ontologies: Tool-Augmented Ontology Engineering        7

        Table 6. Threshold sensitivity with stable matching (full weights).

                      Threshold Cands         P     R    F1
                              0.70   1,912   0.643 0.811 0.717
                              0.75   1,474   0.821 0.798 0.809
                              0.80   1,154   0.961 0.732 0.831
                              0.85   1,069   0.977 0.689 0.808



Why. On the Anatomy track, most class pairs have no structural data (no shared
properties, no instances, no OWL restrictions). When structural signals are all
zero, confidence falls back to label similarity. Changing weights on zero-valued
signals has no effect. The stable matching constraint selects the top candidate
per class, producing a clean 1-to-1 assignment regardless of how the scores were
computed.

Threshold sensitivity. With stable matching, the confidence threshold affects the
precision-recall trade-off:

Implication. The alignment improvement from F1 = 0.182 to F1 = 0.832 is en-
tirely attributable to the matching strategy. For ontologies with limited struc-
tural metadata, the assignment constraint matters more than the similarity func-
tion.


6   Discussion
Tool access is qualitatively different from information access. The Condition D
result (raw file F1 = 0.323 ¡ bare LLM F1 = 0.431) challenges the assumption
that giving an LLM more information always helps. Raw OWL syntax intro-
duces parsing noise that overwhelms the LLM’s extraction ability. Structured
tools (MCP with SPARQL) provide typed, correct results that the LLM cannot
replicate by reading raw text. This finding has implications for tool-augmented
AI systems beyond ontology engineering: the structure of tool access may matter
more than the information content it provides.

Matching strategy dominates signal design. The alignment ablation shows that
spending effort on signal engineering (embedding models, property overlap, struc-
tural similarity) yields less than 0.004 F1 improvement when stable matching
is applied. This contrasts with the ontology matching literature, which has fo-
cused primarily on improving similarity functions. For ontologies with sparse
structural metadata, the assignment constraint is the binding factor.

Two open challenges. First, the Conference track (F1 = 0.438) reveals that label-
centric approaches fail when ontologies use heterogeneous modelling styles. Sec-
ond, the recall gap on Anatomy (0.733 vs 0.922) requires domain-specific back-
ground knowledge that the current system lacks.
8      F. Rovai

7   Limitations

OAEI results not independently evaluated. We have not yet submitted to the
official OAEI campaign. Results are measured against published reference align-
ments. Planned for OAEI 2026.

Signal ablation limited to Anatomy. The finding that weights are irrelevant is
demonstrated on one track where structural signals are mostly zero. On ontolo-
gies with richer metadata, weights may matter.

OntoAxiom Condition D methodology. The raw file condition uses Claude sub-
agents reading files via the Read tool, not a controlled API call with file content
in the prompt. This may slightly overestimate Condition D performance.

Reasoner expressivity. OWL-RL covers most practical patterns but is incomplete
for OWL-DL. The LUBM comparison compares different reasoning profiles.

Single-developer project. 17,400 lines of Rust, one primary developer.

LLM dependency. All LLM benchmarks use Claude (Anthropic). Performance
with other models not evaluated.


8   Conclusion

We have presented Open Ontologies and two empirical findings. First, stable
1-to-1 matching is the dominant factor in ontology alignment: it improves OAEI
Anatomy F1 from 0.182 to 0.832, while signal weights change F1 by less than
0.004. The same method achieves F1 = 0.438 on the Conference track. Second,
structured tool access provides a qualitatively different mode of interaction: an
LLM reading raw OWL (F1 = 0.323) performs worse than unaided inference
(F1 = 0.431), while MCP tools achieve F1 = 0.717. Both findings are verified,
reproducible, and surprising.
    The system is available under the MIT licence at https://github.com/
fabio-rovai/open-ontologies.


Supplemental Material Statement

All source code, benchmark scripts, datasets, and evaluation results are available
at https://github.com/fabio-rovai/open-ontologies. The repository con-
tains the full Rust source code, alignment ablation scripts (benchmark/oaei/run ablation.py),
Condition D extraction scripts and results (benchmark/ontoaxiom/results/condition d/),
and OAEI evaluation data. All alignment and LUBM benchmarks are determin-
istic.
                    Open Ontologies: Tool-Augmented Ontology Engineering             9

Declaration of Use of Generative AI

Claude (Anthropic) was utilised to generate sections of this work including:
drafting and editing of manuscript text, generation of LaTeX tables, and struc-
turing of related work and evaluation sections. Claude was also used as the LLM
component within the system under evaluation, which is the subject of this pa-
per. All experimental design, benchmark execution, data analysis, and technical
claims were performed and verified by the author.


References
 1. Chen, B., Lin, Z., Li, Y., Zhang, N., Wen, H., Chen, H.: OntoAxiom: Evaluating
    LLM Capabilities for Ontology Axiom Identification. arXiv:2512.05594 (2025)
 2. Glimm, B., Horrocks, I., Motik, B., Stoilos, G., Wang, Z.: HermiT: An OWL 2
    Reasoner. J. Automated Reasoning 53(3), 245–269 (2014)
 3. Algergawy, A., Faria, D., Ferrara, A., Jimenez-Ruiz, E., et al.: Results of the On-
    tology Alignment Evaluation Initiative 2024. In: OM Workshop at ISWC 2024.
    CEUR-WS Vol-3897 (2024)
 4. Jiménez-Ruiz, E., Grau, B.C.: LogMap: Logic-Based and Scalable Ontology Match-
    ing. In: ISWC 2011, pp. 273–288. Springer (2011)
 5. Faria, D., Pesquita, C., Santos, E., Palmonari, M., Cruz, I.F., Couto, F.M.: The
    AgreementMakerLight Ontology Matching System. In: OTM 2013, pp. 527–541.
    Springer (2013)
 6. He, Y., Chen, J., Antonyrajah, D., Horrocks, I.: BERTMap: A BERT-Based On-
    tology Alignment System. In: AAAI 2022, pp. 5570–5578 (2022)
 7. Hertling, S., Paulheim, H.: OLaLa: Ontology Matching with Large Language Mod-
    els. In: ISWC 2023, pp. 442–459. Springer (2023)
 8. Anthropic:      Model        Context      Protocol      Specification.    https://
    modelcontextprotocol.io (2024)
 9. Tanière, T.: Oxigraph: A SPARQL Graph Database. https://oxigraph.org
    (2023)
10. Sirin, E., Parsia, B., Grau, B.C., Kalyanpur, A., Katz, Y.: Pellet: A Practical
    OWL-DL Reasoner. J. Web Semantics 5(2), 51–53 (2007)
11. Tsarkov, D., Horrocks, I.: FaCT++ Description Logic Reasoner: System Descrip-
    tion. In: IJCAR 2006, pp. 292–297. Springer (2006)
12. Kazakov, Y., Krötzsch, M., Simančı́k, F.: The Incredible ELK. J. Automated Rea-
    soning 53(1), 1–61 (2014)
13. Caufield, J.H., et al.: Structured Prompt Interrogation and Recursive Extraction
    of Semantics (SPIRES). Bioinformatics 40(3), btae104 (2024)
14. Graux, D., et al.: OntoChat: A Framework for Conversational Ontology Engineer-
    ing. In: ESWC 2024 (2024)
15. Babaei Giglou, H., D’Souza, J., Auer, S.: LLMs4OL: Large Language Models for
    Ontology Learning. In: ISWC 2023, pp. 408–427. Springer (2023)
16. Horridge, M., Drummond, N., Goodwin, J., Rector, A., Stevens, R., Wang, H.: The
    Manchester OWL Syntax. In: OWL Experiences and Directions Workshop (2006)
17. Guo, Y., Pan, Z., Heflin, J.: LUBM: A Benchmark for OWL Knowledge Base
    Systems. J. Web Semantics 3(2–3), 158–182 (2005)
18. HashiCorp: Terraform: Infrastructure as Code. https://www.terraform.io (2014)
10      F. Rovai

19. Horridge, M., Bechhofer, S.: The OWL API: A Java API for OWL Ontologies.
    Semantic Web 2(1), 11–21 (2011)
20. Jackson, R.C., et al.: ROBOT: A Tool for Automating Ontology Workflows. BMC
    Bioinformatics 20, 407 (2019)
21. Lamy, J.B.: Owlready: Ontology-Oriented Programming in Python. Artificial In-
    telligence in Medicine 80, 11–28 (2017)
22. Matentzoglu, N., et al.: A Simple Standard for Sharing Ontological Mappings (SS-
    SOM). Database 2022, baac035 (2022)
23. Motik, B., Grau, B.C., Horrocks, I., et al.: OWL 2 Web Ontology Language Profiles
    (Second Edition). W3C Recommendation (2012)

