# CQ4OE: A benchmark for assessing LLM-assisted ontology generation from competency questions
Source: https://arxiv.org/abs/2609.26029v1
Kind: pdf
Fetched: 2026-09-23T12:58:01.799840+00:00
Tool: pdftotext
Research-Target: /Users/sergii/.ai/knowledge/research_topics/ontology_ai/research/ontology-ai
Topic: ontology_ai

                                         CQ4OE: A benchmark for assessing LLM-assisted
                                          ontology generation from competency questions

                                           Jiayi Li1[0009−0001−9475−8159] , Ziyuan Wang1[0009−0000−6228−4713] , Daniel
                                          Garijo1[0000−0003−0454−7145] , and María Poveda-Villalón1[0000−0003−3587−0367]

                                                  Ontology Engineering Group, Universidad Politécnica de Madrid
                                                   {li.jiayi,ziyuan.wang,daniel.garijo,m.poveda}@upm.es




arXiv:2609.26029v1 [cs.AI] 22 Sep 2026
                                               Abstract. Ontology generation from Competency Questions (CQs) is a
                                               central yet labor-intensive phase of Ontology Engineering. While large
                                               language models (LLMs) offer promising automation capabilities, current
                                               evaluations remain fragmented. Task formulations are heterogeneous, gold
                                               standards often lack fine-grained CQ provenance, metrics conflate lexical
                                               overlap with structural and logical adequacy, and reference ontologies
                                               are not always explicitly designed around the evaluation CQs. Here, we
                                               address these limitations with CQ4OE, a benchmark for the systematic
                                               and reproducible evaluation of LLM-based ontology generation from
                                               CQs. For each ontology in the benchmark, we build a CQ-driven gold
                                               OWL ontology with explicit provenance linking each CQ to the classes,
                                               properties, and axioms required to answer it. From this resource, we
                                               define two complementary evaluation tasks. CQ2Term supports term-
                                               level evaluation of CQ-specific class and property prediction over 99 CQs,
                                               and CQ2Onto supports ontology-level evaluation over 118 CQs, including
                                               hierarchy, property modeling, and axiom-level structure. We demonstrate
                                               CQ4OE with experiments using nine LLMs under zero-shot, iterative,
                                               and multi-agent generation strategies, showing that LLMs recover explicit
                                               vocabulary terms more reliably than creating ontologies, particularly in
                                               property modeling, hierarchy construction, and axiom generation.

                                               Keywords: Ontology Generation· LLMs· Benchmark Evaluation.


                                         1   Introduction

                                         Ontology Engineering (OE) refers to the systematic process of developing machine-
                                         interpretable formal knowledge representations of a domain [49]. Despite well-
                                         established methodologies such as Linked Open Terms [42], eXtreme Design
                                         Methodology [5], and SAMOD [39], OE remains a challenging activity that
                                         requires substantial expertise and iterative cycles of requirement analysis, con-
                                         ceptual modeling, implementation, and evaluation [51,17]. Within these method-
                                         ologies, conceptualization is a central stage where domain requirements are
                                         transformed into an explicit conceptual model [6]. Competency questions (CQs)
                                         are commonly used to express these requirements in natural language, specifying
                                         the questions that the ontology should answer [2]. The conceptualization step
2         J. Li et al.

models CQs as classes, properties, relations, and constraints [45], shaping the
structure and expressiveness of the resulting ontology [42,17].
    Recent advances in Large Language Models (LLMs) have motivated their
adoption across ontology engineering tasks, from CQ generation [36,32,45] and
ontology conceptualization [8,23] to the encoding of conceptual models into formal
ontology languages [11,34]. Across these tasks, LLMs have been used to suggest
candidate terms, identify domain relationships, refine ontology fragments, and
support modeling decisions that traditionally require substantial expertise.
    However, the evaluation landscape is heterogeneous, with different studies
adopting different task formulations, input/output specifications, and evaluation
criteria [25]. This heterogeneity introduces three specific challenges. First, task
formulations are frequently incompatible across studies. For example, evaluated
tasks range from concept extraction and ontology completion to full OWL
generation from documents or CQs [25,17], with each adopting different inputs,
outputs, and modeling depths. Since these tasks differ fundamentally in input,
output, and modeling depth, direct comparison is challenging. Second, previous
analyses have shown that reference ontologies are often not finely aligned with
their CQs [16]. In particular, they rarely specify which classes, properties, or
axioms are required by each CQ, making it unclear whether a generated ontology
satisfies the CQ requirements. Third, existing metrics, often based on lexical or
coarse structural overlap, do not adequately assess property modeling, logical
constraints, or reasoning behavior, leaving errors such as wrong domain/range
assignments, missing axioms, or flawed hierarchies undetected. Together, these
limitations make it difficult to compare LLM-based ontology generation systems
under a shared, requirement-driven evaluation protocol.
    To address these issues, we present CQ4OE, a benchmark for the systematic
and reproducible evaluation of LLM-based ontology generation from CQs. Our
work makes four contributions:

    – Gold standards aligned with the CQs for two evaluation tasks.
      CQ4OE includes two complementary evaluation tasks. CQ2Term supports
      term-level evaluation with CQ-to-term provenance over 99 CQs, and CQ2Onto
      supports ontology-level evaluation with fine-grained CQ-to-axiom provenance
      over 118 CQs from six ontologies.
    – A multi-task evaluation framework. We introduce metrics for term
      recovery, property characteristics, domain/range triples, TBox axioms, and
      hierarchy closure, to assess whether a model can generate ontologies that are
      both structurally and logically sound beyond surface vocabulary.
    – An automated explainable reporting pipeline. We release an open-
      source pipeline that aligns candidate outputs with the gold standards, com-
      putes all proposed metrics, and produces detailed evaluation reports that
      trace matched and missing terms, axioms, CQ coverage, and reasoning-aware
      hierarchy recovery for each generated ontology.
    – A baseline evaluation against CQ4OE. We compare nine LLMs, using
      three generation strategies (zero-shot term prediction for CQ2Term and
      zero-shot, iterative, and multi-agent [27] for CQ2Onto).
                                                                   CQ4OE          3

2     Related Work
Large language models (LLMs) have been applied to ontology conceptualiza-
tion and generation, including ontology completion [45], vocabulary term sug-
gestion [52], relation classification [3,20], and generation from user stories or
CQs [38,48,8,40]. Several recent approaches directly produce ontologies from CQs.
Lippolis et al. [30,31] compare prompting strategies through pitfall detection,
CQ coverage, and expert assessment. MASEO [26] generates OWL ontologies
from CQs with provenance links but releases no reusable evaluation resource.
These efforts remain difficult to compare because they use different CQ sets,
reference ontologies, and metrics [17,25], and prior analysis [16,26] shows that
structural overlap with full reference ontologies is an unfair proxy for requirement
satisfaction, since these ontologies may contain knowledge beyond the input CQs.
    Several evaluation resources exist but target different tasks. OAEI [13] evalu-
ates ontology matching, and BioASQ [53] evaluates biomedical question answer-
ing, neither targeting ontology construction from CQs. OntoAxiom [4] identifies
missing axioms within existing vocabularies instead of constructing complete
ontologies. CORAL [15] provides ontological requirements and CQs but does
not map each CQ to the terms or axioms required to answer it. Alharbi et
al. [1] classify CQ-generation settings, focusing on CQ quality rather than the
ontologies generated from them. Plu et al. [41] evaluate LLM-generated ontologies
through human references and qualitative assessment, but their evaluation is
not CQ-driven. Beyond ontology engineering, general LLM benchmarks such as
HELM [28] and HumanEval [7] evaluate broad capabilities, including reasoning
and code synthesis, beyond ontology construction.
    None of these resources provides a reusable benchmark for evaluating ontolo-
gies within a CQ-aligned requirement scope. CQ4OE addresses this gap with
shared CQs, CQ-aligned gold standards, and metrics that assess requirement sat-
isfaction across term recovery, property characteristics, domain/range relations,
TBox axioms, and hierarchy closure.

3     CQ4OE Benchmark Dataset Construction
CQ4OE is a benchmark for evaluating LLM-based ontology generation from CQs
through two CQ-aligned evaluation tasks: CQ2Term assesses whether a system
predicts the classes and properties required by each selected CQ. In contrast,
CQ2Onto assesses whether a generated ontology captures the terms, property
semantics, domain/range relations, axioms, and hierarchies needed to answer
the selected CQs. For each source ontology and selected CQ set, we construct
two task-specific gold standards. CQ2Term records explicit terms per CQ, while
CQ2Onto records CQ-relevant terms and required axioms with CQ provenance.

3.1   Source ontologies
We select source ontologies based on three criteria. They must have established
use in OE practice, publicly documented requirements with associated CQs, and
4           J. Li et al.

open licenses that allow redistribution and modification. From the candidates
satisfying these criteria, we select six ontologies spanning three size tiers based on
the number of published CQs. The small tier contains Wine [35] and the African
Wildlife Ontology (AWO) [22]. The medium tier contains the Open Digital Rights
Language (ODRL) [21] and SAREF4WATR [12]. The large tier contains the
Video Game Ontology (VGO) [15,37] and the Software Ontology (SWO) [33].
The selected ontologies vary in hierarchical structure, from the nearly flat ODRL
(depth 1) to the deeply nested SWO (depth 15), with AWO and VGO remaining
shallow but wide. This diversity lets CQ4OE assess LLM performance across
different structural complexities. Table 1 reports key statistics for each ontology.

Table 1: Benchmark dataset statistics. Src., Ret., and New⋆ are original, retained, and added CQs.
CQ2O and CQ2T are CQs in each gold standard. C, OP, DP, and Ax are classes, object properties,
data properties, and OWL axioms. Depth is the longest SubClassOf or SubPropertyOf chain and
Width is the maximum number of terms at any hierarchy level. Source counts include imports, and
CQ2Onto counts refer to CQ-aligned sub-ontologies. In CQ2Term, P combines OP and DP.

                                (a) CQ counts and source ontology statistics.


                                      CQs                                            Source
    Ontology          Src.   Ret.   New⋆      CQ2O    CQ2T        C    OP       DP        Ax     Depth    Width
    Wine                7      4          1      5         5     77     13       1        744         3       7
    AWO                14      7          0      7         7     31      5       0         93         2      21
    ODRL               35     13          6     19        19     30     49       4        416         1      22
    SAREF4WATR         43     21          0     21        20     72     40      22        445         5      19
    VGO                68     30          1     31        22     37     33       6        189         2      20
    SWO                88     35          0     35        26   1971    161       5       8087        15     679
    Total             255    110          8    118        99


                             (b) CQ2Term and CQ2Onto gold standard statistics.


                                     CQ2Term                      CQ2Onto
                  Ontology           C          P    C    OP   DP     Ax     Depth        Width
                  Wine               11         5    17    8     1    68             2           4
                  AWO                 7         1     9    5     0    25             1           5
                  ODRL               13        26    15   28     0    60             1           9
                  SAREF4WATR         15        20    20   14    11    43             3           8
                  VGO                 7        14    25   33     5    77             1          12
                  SWO                20        18    31   18     5    80             1           7




3.2     Annotation methodology

To ensure a fair evaluation, the benchmark must assess the knowledge required
by the CQs, not the broader domain content of full reference ontologies. Without
CQ alignment, a generated ontology could be penalized for omitting out-of-
scope content or rewarded for reproducing domain knowledge beyond the stated
CQ requirements. Figure 1 illustrates the four-phase workflow for constructing
CQ-aligned gold standards. Table 1 reports the resulting CQ counts per stage.
   Phase 1: Core term selection. For each source ontology, we identify core
terms (classes and properties that define the domain scope) through a two-step
process combining automatic ranking with manual verification. First, we rank
                                                                  CQ4OE         5

named classes and properties by in- and out-degree, taking highly connected nodes
as initial candidates. Then, we validate these candidates with owl2diagram1 and
inspect them against the official published requirements provided with the source
ontologies. Terms are retained if they are highly connected, visually central, and
domain-relevant. The resulting set Tcore defines the conceptual backbone the gold
standards must cover.
      Phase 2: CQ filtering and term annotation. From the 255 published CQs
across the six source ontologies, we remove those requiring external knowledge,
unanswerable from the source ontology, or targeting instance-level rather than
TBox-level knowledge. This filtering ensures fair evaluation, since every retained
CQ has an answer grounded in the source TBox without requiring content that
the gold ontology cannot express. This leaves 110 retained CQs. For each retained
cq i , we annotate three required term sets, illustrated using the AWO CQ “Which
plants eat animals?” as a running example. Ei (explicit) contains direct surface
matches, such as Plant, Animal, and eats. Ii (implicit) contains synonymous or
equivalent phrases, such as Carnivore for “predators” in the AWO CQ “Which
animals are the predators of these animals?”. Ri (derived ) contains terms not
mentioned in a CQ but required for its formalization, including answer-side
concepts, such as CarnivorousPlant for the running example.
      Phase 3: CQ augmentation. We then check whether all core terms in
Tcore are covered by at least one retained CQ. Uncovered terms are addressed by
manually authoring additional CQs (marked ⋆ in Table 1). This augmentation is
conservative. Only 8 CQs (3.1% of the original 255) are added across all domains,
yielding 118 CQs in total.
      Phase 4: Gold standard construction. With the final CQ set fixed,
CQ2Term records CQ-to-term provenance over explicit class and property terms.
For CQ2Term, we retain only CQs with at least one explicit class or property
term (Ei ̸= ∅), since the task evaluates explicit term recovery. This excludes 19
inference-heavy CQs from SAREF4WATR, VGO, and SWO, leaving 99 CQs.
For the running example, CQ2Term records Plant, Animal, and eats with
CQ-to-term provenance. For CQ2Onto, the annotated terms (Ei ∪ Ii ∪ Ri ) are
used to extract CQ-relevant TBox fragments from the source ontology. An
extracted TBox axiom is linked to cq i only if its removal would make cq i
unanswerable, so the linked axioms form a sufficient set for answering each
CQ. For the running example, CQ2Onto additionally includes the derived class
CarnivorousPlant, together with the axioms CarnivorousPlant ⊑ Plant and
CarnivorousPlant ⊑ ∃eats.Animal recorded with CQ-to-axiom provenance.
The resulting gold standards cover 99 CQs for CQ2Term and 118 CQs for
CQ2Onto.
      Throughout construction, each annotation decision follows a triple-review,
adjudication-based protocol. An annotator with an OE background produces the
initial labeling of every candidate item (core terms, CQs, CQ-to-term provenance,
CQ-to-axiom provenance), and two expert reviewers then inspect each item in
full to verify completeness and correctness. An item is finalized only when all
1
    https://github.com/jatoledo/owl2diagram
6           J. Li et al.

three reach agreement, with disagreements resolved through discussion. Most
items reached agreement on first pass, with 101 of the 118 CQs (85.6%) accepted
without change. The 17 revised items concentrated in the more complex ontologies
(10 in SWO, 3 in VGO, 2 in ODRL, 2 in SAREF4WATR, none in Wine or AWO),
indicating that disagreements track ontology complexity rather than random
variation.

                                                                        annotator reviewer1 reviewer2



                                                                             ↓ All agree ↓

                                                                                                                                     Phase 4:
                                                                                                             Insert
                                                                         Phase 2:                           new CQs                CQ2Onto gold
                                                                CQ filtering & annotation
       Source Dataset                                                                                                     Explicit, implicit, derived terms

                                           Phase 1:                out-of-scope removed                    Phase 3:               TBox axioms
                          Ontology
      Source ontologies              Core terms selection                                               CQ augmentation
                                                                  explicit / implicit / derived                             CQ-axioms provenance
                                                                                                                                   Step 3:
       Published CQs

                                                                                                                                 CQ2Term gold
                                                   missing core terms
                                                                                                                                 Explicit terms
                                     CQ Source
                                                                                                                               CQ-term provenance




Fig. 1: Overview of the CQ4OE annotation workflow. The triple-review, adjudication-based protocol
applies to all candidate items across all phases, including core terms, retained CQs, term annotations,
augmented CQs, CQ-to-term and CQ-to-axiom provenance links.




3.3      CQ2Term and CQ2Onto gold standards

CQ2Term is the term-level task. ForSeach cq i , the required explicit term set
is TiCQ2Term = Ei , with TCQ2Term = i TiCQ2Term . CQ2Term records the links
between each cq i and its explicit terms in TiCQ2Term following the annotation
protocol in Section 3.2.
     CQ2Onto is the ontology-level task that preserves Osrc as the domain reference
ontology. For each cq i , the CQ-relevant term set is TiCQ2Onto = Ei ∪ Ii ∪ Ri , and
OiCQ2Onto is extracted from Osrc using TiCQ2Onto as in Section 3.2. The required TBox
axioms Ai are a curated subset of (OiCQ2Onto )TBox , obtained by first extracting all
TBox axioms involving the terms in TiCQ2Onto and then retaining an axiom only
if its removal would make cq i unanswerable, so that Ai forms a sufficient axiom
set for answering cq i . CQ2Onto records these CQ-to-axiom links as provenance
following the same annotation protocol.


4     Benchmark Evaluation Methodology

We evaluate LLM outputs against the CQ-aligned gold standards described in
Section 3. The evaluation is organized around two principles. First, generated
terms and gold-standard terms must be aligned before comparison, since models
may use different labels for the same intended class or property. Second, ontology
quality must be assessed at multiple modeling depths, beyond lexical overlap
alone. Section 4.1 describes the term alignment procedure, and Sections 4.2
and 4.3 define the metrics for CQ2Term and CQ2Onto.
                                                                      CQ4OE          7

4.1   Term alignment aggregation and selection

Generated ontologies can use labels that differ from the gold standard while de-
noting the same class or property (e.g., hasPart vs. containsComponent), so we
align the gold and predicted terms before computing the CQ2Term and CQ2Onto
metrics. From seven candidate similarity methods, we excluded WordNet-based
synonym matching [50] due to poor coverage of domain terms and information-
content similarity [47,29] as it requires a shared taxonomy. The final pipeline uses
five methods. Hard matching applies exact string equality. Sequence matching
uses Python difflib.SequenceMatcher2 . Levenshtein [24] and Jaro–Winkler
similarity are computed with the textdistance library3 . Embedding-based se-
mantic similarity uses embeddinggemma served via Ollama4 . Standalone Precision
(P), Recall (R), and F1 are reported per method, using thresholds of 1.0 for hard
matching, 0.8 [14] for lexical similarities, and 0.6 [46] for semantic similarity.
Because the methods exhibit complementary failure modes, with exact and lexi-
cal matching missing paraphrases, while semantic matching can introduce false
positives on short labels, the final metrics use an aggregated alignment defined
below.
    Let Tg and Tp denote the gold-standard and predicted term sets. Alignment
is performed between terms of the same type. For each candidate pair (tg , tp ),
where tg ∈ Tg and tp ∈ Tp , each of the five similarity methods produces a score
sm (tg , tp ) ∈ [0, 1]. We aggregate the four non-hard methods using the mean of
the three highest scores, with hard matching as an exact-match override:
                          (
                           1,                              if shard (tg , tp ) = 1,
             s(tg , tp ) = 1 P
                            3                  s (t ,
                               m∈Top3 (tg ,tp ) m g p t ), otherwise,

where Top3 (tg , tp ) denotes the three non-hard methods with the highest scores
for (tg , tp ). This aggregation mechanism prevents any single method with a lower
score from vetoing a reasonable matching result.
    A candidate pair passes thresholding if its score reaches the type-specific
threshold τ . We selected τC = 0.6 for classes and τP = 0.7 for properties by
inspecting correct and spurious alignments at {0.5, 0.6, 0.7} on a held-out subset.
The higher property threshold reduces false matches on short formulaic labels
(e.g., has_, is_ prefixes), where spurious matches concentrate around 0.6–0.65.
Pairs passing thresholding are ranked by decreasing aggregated score, with hard
matches prioritized, and selected greedily to obtain a one-to-one alignment: (tg , tp )
is kept only if both terms are still unmatched. The same procedure is applied
per standalone method using its own score, enabling comparable per-method
P/R/F1 . The accepted pairs form the final alignment set α = αC ∪ αP , where
αC contains accepted class pairs and αP contains accepted property pairs. Since
α is a set of one-to-one pairs, we use it in both directions to translate between
2
  https://docs.python.org/3.8/library/difflib.html
3
  https://github.com/life4/textdistance
4
  https://ollama.com/library/embeddinggemma
8        J. Li et al.

gold and predicted vocabularies. This alignment provides the correspondence
layer used by all downstream metrics.
    Table 2 gives an overview of the metrics reported for each evaluation target.
The following sections define these metrics in detail.

Table 2: Overview of reported metrics in CQ4OE. AC scores use only structures whose named
terms align under the alignment set α, G denotes global scores, computed over the full gold and
predicted sets. Per-method reports standalone P/R/F1 for the five similarity methods. Diag.
denotes standalone embedding-cosine diagnostics. CQ reports at-least-one, mean, and full coverage
over terms (t), axiom-level matches (a), or closure-recovered axioms (c).
    Evaluation tasks             Per-method Diag. P/R/F1 (AC) P/R/F1 (G) CQ cov.
    Class & property (CQ2Term)        ✓         —           —               ✓           t
    Class & property (CQ2Onto)        ✓         —           —               ✓           —
    Property characteristics          —         —           ✓               ✓           —
    Triple                            —         ✓           ✓               ✓           —
    Axiom-level                       —         ✓           ✓               ✓           a
    Hierarchy closure                 —         —           —               ✓           c



4.2    CQ2Term Evaluation
CQ2Term is the term-level task in CQ4OE. It evaluates the explicit term sets
TiCQ2Term defined in Section 3. The LLM prediction for each CQ is denoted by
T̂iCQ2Term . For aggregate reporting, let TgCQ2Term and TpCQ2Term
                                                          S       denote the combined
gold and predicted CQ2Term term sets: TgCQ2Term = i TiCQ2Term and TpCQ2Term =
S CQ2Term
   i T̂i      . The final alignment α = αC ∪ αP from Section 4.1 is applied
separately for classes and properties.

Term-level metrics. The CQ2Term metrics are computed globally over the
combined gold term set TgCQ2Term and the predicted term set TpCQ2Term . Let α
be the final one-to-one alignment between TgCQ2Term and TpCQ2Term , where |α| is
the number of accepted matched pairs. We define true positives (TP), false
positives (FP), and false negatives (FN) as TP = |α|, FP = |TpCQ2Term | − |α|, and
FN = |TgCQ2Term | − |α|. Precision P = TP/(TP + FP), Recall R = TP/(TP + FN),
and F1 = 2P R/(P + R) are then computed. We set F1 = 0 when P + R = 0.
These metrics are reported per standalone similarity method and for the final
aggregated alignment.

CQ-conditioned coverage. CQ-conditioned coverage checks whether recovered
terms appear under the correct CQ: a gold term for cq i counts as covered only if α
aligns it to a term predicted for cq i . Let covi be the proportion of required explicit
terms covered for cq i , and N the number of retained CQs. At-least-one coverage
(A1) measures the share of CQs with at least one required term recovered, mean
coverage (MC) averages covi across CQs, and full coverage (FC) gives the share
of CQsP  whose required terms are all recovered, with A1 = |{i : covi > 0}|/N ,
MC = i covi /N , and FC = |{i : covi = 1}|/N .
    The two views thus capture complementary failure modes, since a model may
recover the required vocabulary without attaching each term to the CQ that
requires it, leaving individual CQs unanswered despite high overall scores.
                                                                   CQ4OE          9

4.3   CQ2Onto Evaluation

CQ2Onto evaluates LLM-generated ontologies against the ontology-level gold
standard defined in Section 3.3 using five evaluation targets: term recovery,
property characteristics, domain/range triples, TBox axioms, and hierarchy
closure. For property characteristics, domain/range triples, and TBox axioms,
we report a global view over the full gold and predicted element sets, and an
alignment-conditioned (AC) view restricted to elements whose named terms align
under αC and αP . Term recovery is reported only globally, since term recovery
itself evaluates how well α recovers gold terms. An AC view here would only
evaluate α in terms that have already been aligned. Hierarchy closure is reported
as a single set-based metric over inferred subsumptions translated through α.


Ontology-level metrics. Term recovery compares predicted and gold class
and property vocabularies using both the final alignment αC ∪ αP and the
five standalone similarity methods. Property characteristics compare OWL
property characteristic axioms (functional, symmetric, etc.) between aligned
property pairs. Domain/range triples assess graph structure by treating
domain and range axioms as triples (s, p, o). Properties are compared through αP ,
class-valued domains and ranges through αC , and datatype ranges by normalized
string equality. Triples involving complex anonymous OWL expressions are
excluded here and evaluated at the axiom level. TBox axioms compare structural
decompositions of TBox axioms, recursively translating named terms through
αC and αP and matching datatypes, cardinalities, intersections, unions, and
restrictions strictly. Hierarchy closure uses HermiT to compare inferred class
and property subsumption closures of the gold and predicted ontologies (with the
predicted closure translated to gold vocabulary through α), capturing hierarchy
relations that may be entailed rather than explicitly asserted. For domain/range
triples and TBox axioms, we additionally report an embedding-cosine diagnostic
over normalized textual serializations, which does not affect strict P/R/F1 .
    For term recovery and the non-closure structural targets, P/R/F1 follow
Section 4.2. For each target and view, TP counts one-to-one matched pairs that
are strictly equivalent, unmatched predicted elements count as FP, unmatched
gold elements count as FN, and matched but non-equivalent pairs count as both
FP and FN.
    For hierarchy closure, let Cl g be the gold closure and Cl gp the predicted
closure translated to the gold vocabulary through α. We define TP = |Cl g ∩ Cl gp |,
FN = |Cl g | − TP, and FP = |Cl gp | − TP + U , where U counts predicted closure
pairs that cannot be translated through the alignment and are therefore counted
as additional FP. P, R, and F1 are computed as above.


CQ-conditioned coverage. We report CQ coverage in CQ2Onto in two forms:
axiom-level coverage and closure-recovered coverage. As in CQ2Term, both
are summarized using At-least-one coverage (A1), Mean Coverage (MC), and
Full Coverage (FC). Here, coverage is computed over required TBox axioms
10        J. Li et al.

rather than explicit terms. Let Ai denote the set of TBox axioms required
to answer cq i , as defined in Section 3.3. For axiom-level coverage, covaxiom      i      =
#axiom-level matches in Ai
            |Ai |          denotes   the   fraction  of axioms    in A  i that  are  strictly
matched by the axiom-level evaluation defined in Section 4.3. Closure-recovered
coverage checks whether hierarchy-related gold axioms missed by axiom-level
matching can be recovered through HermiT reasoning. Only missed hierarchy-
related axioms are eligible for closure recovery. They are counted only if they
can be decomposed into atomic Subclass or Subproperty pairs, including Equiv-
alentClasses axioms whose IntersectionOf or UnionOf operands yield such pairs
and all extracted pairs appear in Cl gp . Closure-recovered axioms are counted
only among axioms not already matched by the axiom-level evaluation. The
CQ coverage after adding closure-recovered axioms to the axiom-level matches
is covclosure
       i      = #axiom-level matches in Ai +#closure-recovered
                                            |Ai |
                                                               axioms in Ai
                                                                            . Closure recov-
ery is restricted to gold axioms that are hierarchy-related and that decompose into
atomic Subclass or Subproperty pairs. Other axioms are scored only by matching
at the axiom-level.


Evaluation report. The CQ4OE pipeline generates a Markdown report per-run
that aggregates all metrics from Sections 4.2 and 4.3, organized by evaluation
target. Each report includes standalone scores for the five similarity methods, the
final one-to-one term alignment, TP/FN/FP, and CQ-level traces for matched,
closure-recovered, and missed axioms, together with CSV exports of term align-
ments and per-axiom traces. Each closure-recovered axiom is tagged as directly
asserted, chain-inferred, or complex-inferred. For chain-inferred cases, a breadth-
first search reconstructs the shortest path through the predicted hierarchy, pro-
viding a human-readable explanation of the recovery. Sample reports for all runs
are available in the project repository.6


5      Experimental Setup and Results

We evaluate CQ2Term on 99 CQs and CQ2Onto on 118 CQs across six ontologies,
providing reference baselines from nine LLMs, DeepSeek V4-Pro, V4-Flash,
V3.2 [10,9]; Qwen3.6 Plus, Flash, 35B-A3B, 27B [44]; and Gemma 4 31B-IT,
26B-A4B-IT [18]. Models are accessed via OpenRouter5 with temperature 0 and
a 16,384 token output limit. All setups reuse the prompting set from the MASEO
Generation Agent [27] so that performance differences reflect the models and
strategies rather than prompt design. For CQ2Term, it outputs the required
classes and properties per CQ. For CQ2Onto, each model generates a full ontology
under three strategies. Zero-shot feeds the full CQ set in one pass, iterative
feeds CQs sequentially, and multi-agent refines the initial ontology with RDFLib,
HermiT [19], and OOPS! [43] for up to three iterations with backtracking. In
total, CQ2Term yields 54 runs, and CQ2Onto produces 162 ontologies, providing
5
     https://openrouter.ai
                                                                  CQ4OE        11

reference baselines for future methods. All results and reports are available in
the project repository.6


5.1    Results

CQ2Term reports global F1 over the combined gold and predicted term sets and
CQ-conditioned coverage, in which a term counts only when recovered under
the CQ that requires it. Global term F1 ranges from 59.1% (DeepSeek V3.2) to
66.5% (DeepSeek V4-Pro), with five models leading on at least one domain. Class
recovery exceeds property recovery (67.1% vs 55.2%), and precision-recall gaps
indicate over-generation (overall 56.1% vs 71.5%; properties 47.9% vs 69.3%).
Among standalone methods, hard matching is conservative (51.7% on classes,
30.0% on properties) while semantic similarity reaches 73.9% and 63.3%; the
33.3-point property gap supports the multi-method aggregation in CQ4OE.
Figure 2(a) shows global term F1 for each (model, domain) pair: performance
varies more by domain than by model, ranging from 48.0% on Wine to 90.5% on
AWO. Figure 2(b) reports CQ-conditioned coverage, averaging 89.2% at-least-
one, 54.8% mean, and only 23.5% full. Water reaches 70.6% global F1 but 0%
full coverage for every model, and Wine reaches 100% at-least-one but 0% full
coverage. These contrasts show that strong global vocabulary recovery does not
imply CQ-level completeness; by tying every recovered term to the CQ that
requires it, CQ4OE exposes requirement-localization errors that global scores
hide.
    CQ2Onto extends term recovery to the full ontology structure across the five
evaluation targets of Section 4.3, under three generation strategies. DeepSeek
V4-Pro achieves the highest class-label F1 at 66.5%, and Gemma-4 31B-IT leads
on property triple recovery at 41.2%. Mean structural F1 across the 18 (domain,
strategy) settings ranges from 26.7% for Gemma-4 26B-A4B-IT to 33.7% for
DeepSeek V3.2, with five models leading on at least one domain. At the CQ
level, DeepSeek V4-Flash leads on Axiom-Mean and Closure-Mean at 23.7%
and 24.8%. No single model dominates every dimension, a heterogeneity that
only the multi-target design of CQ4OE makes visible. Performance drops steeply
from vocabulary to structure, with class F1 averaging 59.7% and property F1
31.8%. The AC view is consistently higher than the global view, with Triple-
AC 36.4% vs Triple-G 12.4% and Axiom-AC 35.3% vs Axiom-G 15.0% (AWO
excluded from triple aggregation because its gold range is a complex anonymous
OWL expression). Closure F1 averages only 16.7%, indicating shallow predicted
hierarchies. Models identify relevant entities better than they assemble them into
globally correct structures, a distinction that the two-view design of CQ4OE
makes explicit and that single-score benchmarks cannot capture.
    Figure 3(a) summarizes the structural metrics by (domain, strategy). Domain
variation dominates strategy variation. The three strategies yield comparable
structural F1 within 3 percentage points but shape the hierarchy differently.
Iterative prompting produces the densest SubClassOf graphs at 8.6 closure pairs
6
    https://github.com/oeg-upm/cq4oe-benchmark
12      J. Li et al.

on average against 4.9 for zero-shot and 4.7 for multi-agent. Multi-agent generation
instead improves the axioms themselves. Using OOPS! and HermiT to repair
pitfalls without adding new chains, it raises CQ-level axiom coverage (Axioms-
Mean) from 18.3% under zero-shot to 24.2%, with the gain concentrated in
AWO (26.0% → 37.6%) and ODRL (23.3% → 32.3%). Each domain exposes a
different facet of the benchmark. AWO is the easiest case at class F1 87.6% and
closure F1 52.2%. Wine produces the strongest axiom-level scores in Axiom-AC
54.0%, Axiom-G 23.7%, and VGO and ODRL show large AC-to-Global drops in
triples, from 70.0% to 25.8% and from 59.7% to 19.1%, isolating the unaligned
vocabulary as their dominant error. Water displays the sharpest split between
recognition and structure, reaching class F1 ≈ 65% but Triple-G ≤ 3.5% and
Axiom-G ≤ 6%. Figure 3(b) reports CQ-conditioned coverage before and after
closure rescue. Axioms@1 averages 63.0%, Axioms-Mean 20.2%, and Axioms-Full
only 2.1%. Closure rescue raises Closure-Mean to 21.6%, an average gain of 1.4
points shown as ∆ in the same panel, but leaves Closure-Full unchanged. The
gain concentrates in the domains with the densest predicted hierarchies, where
AWO rises from 30.5% to 37.1% and Wine from 19.8% to 21.3%, and there is
no measurable improvement on ODRL, Water, VGO, or SWO, whose predicted
hierarchies collapse to flat edges. CQ4OE thus pinpoints both the failure type,
recognition against structure, and the domain factor, predicted hierarchy density
against collapse, driving each result.
    Three recurrent LLM limitations emerge from these views, all traceable
through the CQ4OE reports. First, models rarely generate sufficient SubClassOf
or SubPropertyOf chains. In VGO and SWO, predicted ontologies produce only
0.6 and 0.7 closure pairs against gold 12 and 8, leaving HermiT with almost no
hierarchy to reason with. In Water, predicted hierarchies recover flat leaf-to-top
edges (e.g., Sensor ⊑ Asset) and miss the chain WaterMeter ⊑ Meter ⊑ Sensor
⊑ Device, explaining the high class F1 but near-zero closure coverage. Second,
property modeling is unstable, with labels paraphrased or aliased much more
often than classes, depressing property F1 to nearly half of class F1 . Third, CQ
completeness remains low, with models recovering some axioms required by a CQ
but rarely all of them, leaving Axiom-Full near 2%. Each failure mode corresponds
to a distinct evaluation target in CQ4OE and would remain invisible under a
single aggregate score.


6    Discussion

Impact and contribution. CQ4OE addresses a gap in the evaluation of
LLM-based ontology generation. Existing evaluations often reuse full reference
ontologies as undifferentiated gold standards, even when they contain knowledge
unrelated to the evaluated CQs. This makes it difficult to determine whether
a generated ontology satisfies the stated requirements or merely overlaps with
general domain knowledge. CQ4OE introduces CQ-aligned gold standards in
which terms and TBox axioms are explicitly linked to the CQs that require them,
with provenance preserved at the level of each individual class, property and
                                                                                                                                                                         CQ4OE                    13

                                              CQ2Term Global Combined F1 across Models and Domains
                                                           Small                             Medium                                 Large

                              DS-V4-Pro          56.2              100.0              48.9              65.8                 69.2              58.6
                                                                                                                                                                    100
                             DS-V4-Flash         64.5                88.9             43.2              71.8                 64.2              52.5
                                                                                                                                                                    90
                                DS-V3.2          51.3                80.0             43.2              66.7                 60.7              52.8




                                                                                                                                                                          Combined F1 Score (%)
                                                                                                                                                                    80
                              Qwen-Plus          41.0                94.1             46.0              74.7                 65.4              51.5



               LLM Model
                             Qwen-Flash          42.4                87.5             51.2              69.2                 57.1              51.5                 70

                              Qwen-35B           38.9                87.5             57.8              75.0                 63.0              49.5
                                                                                                                                                                    60
                              Qwen-27B           45.7                82.4             50.0              69.1                 59.3              53.6
                                                                                                                                                                    50
                             Gemma-31B           54.5              100.0              54.8              66.7                 67.9              51.9

                             Gemma-26B           37.5                94.1             46.7              76.3                 60.4              52.4                 40

                                                Wine               AWO               ODRL               Water                VGO               SWO
                                                                                   Benchmark Domain

                                                     (a) Overall term F1 by model and domain.
                                                           CQ2Term CQ-conditioned Coverage by Domain
                                                                                   At-least-one           Mean               Full

                                      100.0                  100.0
                             100                                     96.5                                                       95.0
                                                                            92.1                         92.2                                         90.6


                              80
                                                                                                                                       69.1




              Coverage (%)
                              60                                                    57.3                        55.8


                                              42.8                                                                                                           42.7
                                                                                                                                              39.9
                              40

                                                                                           22.0
                              20
                                                                                                                                                                    8.5

                                                     0.0                                          0.6                  0.0
                               0
                                           Wine                    AWO                ODRL                 Water                    VGO                  SWO
                                                                                     Benchmark Domain

                                           (b) CQ-conditioned coverage averaged over 9 LLMs.

Fig. 2: CQ2Term results across six benchmark domains. (a) Overall term F1 for each model and
domain pair, computed by pooling class and property matches before calculating precision, recall,
and F1 . (b) CQ-conditioned coverage averaged over nine LLMs, reporting at-least-one, mean, and
full coverage for each domain.

axiom. To our knowledge, no existing benchmark for ontology generation provides
this level of CQ-to-axiom provenance.
    This requirement-driven design advances evaluation along two complementary
fronts. First, CQ2Term targets the conceptualization capability of an LLM by
measuring whether a model can recognize and organize the explicit classes and
properties expressed in the CQs, which capture the most immediate semantic
content of the requirements. Conceptualization is the foundation of any down-
stream ontology, since vocabulary selection determines all subsequent modeling
decisions. By isolating this capability, CQ2Term reduces the manual effort that
ontology engineers would otherwise spend enumerating candidate terms, and
offers practitioners a transparent basis for selecting the model best suited to their
domain rather than relying on a single aggregate ranking. Second, CQ2Onto
evaluates the ability of a model to understand and reason over CQ requirements
beyond recognizing their surface vocabulary. It assesses whether the model can
14       J. Li et al.

                                                                             CQ2Onto Structural Performance by Domain and Strategy
                                                                                                                                                                              100
                                                  WINE | zero-shot          62.5         38.6        48.0          19.5         54.2        27.7      16.5

                                                   WINE | iterative         64.2         18.0        23.1           5.8         55.7        22.2      22.3

                                                WINE | multi-agent          57.8         24.4        55.3          15.8         52.0        21.2      14.7

                                                   AWO | zero-shot          87.8         32.8        N/A           N/A          23.4        15.8      52.3                    80
                                                    AWO | iterative         91.5         26.1        N/A           N/A          22.0        14.5      66.3




              Domain and Generation Strategy
                                                 AWO | multi-agent          83.4         45.3        N/A           N/A          32.8        21.8      37.9

                                                  ODRL | zero-shot          61.4         30.4        65.8          26.6         33.7        15.8      13.8




                                                                                                                                                                                       Mean F1 Score (%)
                                                                            50.5         22.6        46.7          11.3         16.9         5.3       1.6                    60
                                                   ODRL | iterative
                                                ODRL | multi-agent          67.6         28.3        66.7          19.5         36.9        13.5      13.9

                                                   Water | zero-shot        69.5         36.0         3.6           1.4         12.4         6.0      21.4

                                                    Water | iterative       61.4         38.6         8.9           3.4         10.0         4.5      10.7
                                                                                                                                                                              40
                                                 Water | multi-agent        64.0         27.8         1.9           0.6         11.9         4.3      21.3

                                                   VGO | zero-shot          45.5         37.4        75.7          28.8         44.5        16.1       0.0

                                                    VGO | iterative         43.0         36.8        67.4          25.1         41.7        14.7       1.4

                                                 VGO | multi-agent          41.0         31.2        66.8          23.6         29.9        11.9       0.0                    20

                                                   SWO | zero-shot          32.4         33.8         3.4           1.1         52.0        17.6       2.0

                                                    SWO | iterative         49.7         33.3         8.6           2.5         59.8        21.5       1.9

                                                 SWO | multi-agent          42.2         30.4         4.8           1.1         45.1        14.7       2.0
                                                                                                                                                                              0
                                                                           Class       Property   Triple-AC      Triple-G   Axiom-AC Axiom-G         Closure
                                                                                                            Evaluation Metric

                                                                                     (a) Structural performance (F1 ).
                                                                                   CQ2Onto CQ-conditioned Coverage by Domain                                     Gain
                                                                                      Axioms                                Closure
                                                                                                                                                      100
                                                  WINE | zero-shot        97.8         21.3         0.0           97.8        22.8         0.0                      +1.5

                                                                          97.8         18.9         0.0           97.8        20.7         0.0                      +1.8
                                                                                                                                                                                   7
                                                   WINE | iterative
                                                WINE | multi-agent        91.1         19.2         0.0           91.1        20.4         0.0                      +1.2

                                                  AWO | zero-shot         96.8         26.0         0.0          100.0        33.0         0.0        80            +7.0           6
                                                   AWO | iterative        100.0        28.0         0.0          100.0        35.2         0.0                      +7.2




               Domain and generation strategy
                                                AWO | multi-agent         96.8         37.6         0.0           96.8        43.3         0.0                      +5.7
                                                                                                                                                                                   5
                                                 ODRL | zero-shot         50.0         23.3         6.2           50.0        23.3         6.2                          0.0

                                                                          37.7         10.4         0.6           37.7        10.4         0.6
                                                                                                                                                      60                0.0
                                                  ODRL | iterative


                                                                                                                                                             Coverage
                                                ODRL | multi-agent        70.4         32.3         6.2           70.4        32.3         6.2                          0.0        4
                                                                                                                                                                                       Δ
                                                  Water | zero-shot       17.4          4.5         0.5           17.4         4.5         0.5                          0.0

                                                   Water | iterative      23.3          4.6         0.0           23.3         4.6         0.0                          0.0
                                                                                                                                                      40                           3
                                                Water | multi-agent       15.9          5.5         1.6           15.9         5.5         1.6                          0.0

                                                   VGO | zero-shot        42.7         19.2         6.5           42.7        19.2         6.5                          0.0

                                                                          44.4         21.0         7.6           44.4        21.0         7.6                          0.0
                                                                                                                                                                                   2
                                                    VGO | iterative
                                                 VGO | multi-agent        44.5         22.2         7.9           44.5        22.2         7.9        20                0.0

                                                   SWO | zero-shot        55.2         15.7         0.0           55.2        15.7         0.0                          0.0        1
                                                    SWO | iterative       77.5         26.7         0.0           77.5        26.7         0.0                          0.0

                                                 SWO | multi-agent        74.0         28.2         1.3           74.0        28.2         1.3                          0.0
                                                                                                                                                      0                            0
                                                                        Axioms@1 Axioms-Mean Axioms-Full       Closure@1 Closure-Mean Closure-Full                      Δ
                                                                                                  CQ coverage metric

                                                                                  (b) CQ-conditioned coverage and gain.
Fig. 3: CQ2Onto results across six benchmark domains, with each (domain, strategy) cell averaged
over nine LLMs in both panels. (a) Structural F1 across seven evaluation metrics (AWO Triple cells
shown as N/A because the gold range is a complex anonymous OWL expression). (b) CQ-conditioned
coverage before and after closure rescue, where ∆ shows the gain in Mean coverage from closure
rescue (Closure-Mean − Axioms-Mean).


move beyond the explicit terms of each CQ to recover the implicit and derived
terms that the answer also requires, and whether it can express them as a coherent
ontology including property characteristics, property triples, TBox axioms, and
hierarchical structure under reasoner-derived closure. This goes beyond lexical
fluency, requiring the structural and inferential commitments that make a CQ
formally answerable.
   The transition from natural-language requirements to formal OWL repre-
sentations remains a central bottleneck in ontology engineering [31,32], which
makes this resource particularly relevant to the Semantic Web community. By
making the CQ-to-term and CQ-to-axiom provenance explicit, CQ4OE enables a
                                                                   CQ4OE         15

transparent evaluation of LLM-generated ontologies, distinguishing failures that
arise from missing vocabulary, unstable property modeling, shallow hierarchy gen-
eration, or incomplete coverage of the local CQs. The CQ4OE pipeline produces
per-run Markdown reports and CSV alignment exports that trace each metric
back to specific gold and predicted axioms, making evaluation results traceable
at the level of individual CQs and axioms, instead of only aggregate scores.
By enabling transparent, requirement-driven comparison of ontology generation
approaches, CQ4OE can benefit not only ontology engineers but the broader
Semantic Web community, as LLM-assisted ontology engineering matures and
the need for fair, reproducible evaluation grows.

Reusability and reproducibility. CQ4OE is designed for reuse across domains,
models, prompting strategies, ontology repair pipelines, and human-in-the-loop
workflows. The repository organizes CQ2Term and CQ2Onto as two parallel
directories, each with gold standards, predictions, evaluation scripts, intermediate
results, and aggregated reports. To benchmark a new LLM, users add their
generated ontologies to the predictions folder and run a single script that extracts
atomic axioms, executes the five evaluation steps, and produces the aggregated
report. To evaluate a single capability, users can apply CQ2Term for term-level
recovery or reuse the CQ2Onto layers for ontology-level evaluation independently.
To extend the benchmark, users simply need to add a new domain following
the four-phase annotation methodology of Section 3.2 under the same triple-
review, adjudication-based protocol. Each metric has a persistent W3ID identifier
and a Turtle definition in the metric catalogue, supporting integration into
other evaluation pipelines. A public leaderboard7 with submission guidelines is
maintained in the project repository to facilitate comparison of new methods.

Limitations. Several limitations of the current evaluation deserve attention. The
most consequential is that all ontology-level metrics depend on term alignment, so
errors at this layer propagate into downstream scores. Our combined hard, lexical,
and semantic procedure with one-to-one selection handles lexical variation and
reduces many-to-many score inflation, but it can still fail on short property labels
or on semantically close yet non-equivalent terms. The thresholds τC and τP
in Section 4.1 were selected through empirical inspection, informed by previous
studies [14,46], and are applied uniformly across all six heterogeneous ontologies
without per-domain tuning. The pipeline first performs a dry run that exports
the complete alignment traces before any scoring. After applying the thresholds,
manual inspection in all six domains confirmed that most automatic alignments
agreed with expert judgment, although borderline cases remain. The thresholds
are configurable, and users can inspect and, where necessary, manually correct
alignments in the intermediate CSV files before re-running the evaluation.
    A second limitation is methodological. The closure rescue mechanism evalu-
ates only those hierarchy-related axioms that can be decomposed into atomic
SubClassOf or SubPropertyOf relations, including EquivalentClasses with Intersec-
tionOf or UnionOf. Consequently, complex expressions whose semantics cannot be
7
    https://w3id.org/cq4oe/leaderboard
16     J. Li et al.

represented by such atomic relations are excluded from quantitative evaluation,
since assigning partial credit to individual sub-expressions within a complex
axiom remains an open problem. We leave richer handling of such cases to future
work.
    A third concern is data contamination, since the source ontologies and some
of their published CQs are public and may appear in pre-training data. Three
observations qualify its impact. First, mean structural F1 remains low at 26.7%
to 33.7% across models, suggesting that prior exposure to ontology vocabulary
alone does not translate into structurally correct ontology generation. Second,
the CQ-to-term and CQ-to-axiom provenance is manually curated through the
triple-review protocol of Section 3.2, introducing an additional manually curated
annotation layer that is unlikely to have appeared in pre-training data. Third, the
methodology is portable. Private or post-cutoff ontologies can be added through
the documented annotation protocol, future versions of the benchmark plan will
include several such ontologies to support evaluations with contamination control.



7    Conclusion

We presented CQ4OE, a benchmark for evaluating LLM-based ontology gen-
eration from competency questions. CQ4OE links each CQ to the terms and
TBox axioms required to answer it through two complementary evaluation tasks,
CQ2Term and CQ2Onto. The CQ4OE pipeline automatically generates Mark-
down reports and CSV alignment exports that trace every metric back to specific
gold and predicted axioms, enabling a detailed diagnosis of why a generated
ontology does not satisfy individual CQs. Experiments with nine LLMs across
six ontologies show that models recover explicit vocabulary more reliably than
ontology structure, with performance varying more across domains than across
models or generation strategies. Reasoning-based closure provides only limited
recovery when the underlying hierarchy is missing. These findings highlight the
need for provenance-aware, multi-dimensional evaluation of LLM-generated on-
tologies. We believe CQ4OE will provide a common evaluation basis for future
research on LLM-assisted ontology engineering. Future work will extend CQ4OE
with additional domains, further refine alignment and evaluation metrics, and
incorporate private or post-cutoff ontologies to support contamination-controlled
evaluations.



Acknowledgments.

This work was supported by the grant “SOEL: Supporting Ontology Engi-
neering with Large Language Models” (PID2023-152703NA-I00) funded by
MCIN/AEI/10.13039/501100011033 and by “ERDF/UE”.
                                                                      CQ4OE         17

Resource Availability Statement
CQ4OE is openly available under Apache 2.0 at https://github.com/oeg-upm/
cq4oe-benchmark, archived on Zenodo (https://doi.org/10.5281/zenodo.20080309)
and HuggingFace (https://doi.org/10.57967/hf/8712). The repository contains
the CQ2Term and CQ2Onto gold standards for all six ontologies, the evalua-
tion pipeline, and the run-level reports underlying the results. Persistent metric
identifiers are defined at https://w3id.org/cq4oe/metrics.


Declaration of use of Generative AI
All the ideas presented in this manuscript are original from the authors. During
the preparation of this work, the authors used Claude (Anthropic) to improve
the clarity, grammar, and readability of the manuscript. After using this tool, the
authors reviewed and edited the content as needed and take full responsibility
for the content of the publication.


References
 1. Alharbi, R., de Berardinis, J., Grasso, F., Payne, T.R., Tamma, V.: Characteristics
    and desiderata for competency question benchmarks. In: ISWC 2024 Special Session
    on Harmonising Generative AI and Semantic Web Technologies (2024), https:
    //ceur-ws.org/Vol-3953/
 2. Antia, M.J., Keet, C.M.: Automating the generation of competency questions for on-
    tologies with agocqs. In: Iberoamerican Knowledge Graphs and Semantic Web Con-
    ference. pp. 213–227. Springer (2023). https://doi.org/10.1007/978-3-031-47745-4_
    16
 3. Babaei Giglou, H., D’Souza, J., Auer, S.: LLMs4OL: Large language models for
    ontology learning. In: International Semantic Web Conference. pp. 408–427. Springer
    (2023). https://doi.org/10.1007/978-3-031-47240-4_22
 4. Bakker, R.M., Di Scala, D.L., de Boer, M.H., Raaijmakers, S.A.: Ontology learning
    with LLMs: A benchmark study on axiom identification (2025). https://doi.org/10.
    48550/arXiv.2512.05594
 5. Blomqvist, E., Hammar, K., Presutti, V.: Engineering ontologies with patterns –
    the extreme design methodology. In: Ontology Engineering with Ontology Design
    Patterns, Studies on the Semantic Web, vol. 25, pp. 23–50. IOS Press (2016).
    https://doi.org/10.3233/978-1-61499-676-7-23
 6. Chávez-Feria, S., García-Castro, R., Poveda-Villalón, M.: Chowlk: from uml-based
    ontology conceptualizations to owl. In: European Semantic Web Conference. pp.
    338–352. Springer (2022). https://doi.org/10.1007/978-3-031-06981-9_20
 7. Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H.P.D.O., Kaplan, J., Edwards,
    H., Burda, Y., Joseph, N., Brockman, G., et al.: Evaluating large language models
    trained on code. arXiv preprint arXiv:2107.03374 (2021). https://doi.org/10.48550/
    arXiv.2107.03374
 8. Coutinho, M.L.: Leveraging llms in text-based ontology-driven conceptual modeling.
    In: Proceedings of the Joint Ontology Workshops (JOWO) (2024), https://ceur-ws.
    org/Vol-3882/
18      J. Li et al.

 9. DeepSeek-AI: DeepSeek-V3 technical report (2024), https://arxiv.org/abs/2412.
    19437
10. DeepSeek-AI: DeepSeek-V4 Technical Report. https://huggingface.co/deepseek-ai/
    DeepSeek-V4-Pro/blob/main/DeepSeek_V4.pdf (2026), preview release, April 2026
11. Doumanas, D., Soularidis, A., Kotis, K., Vouros, G.: Integrating llms in the
    engineering of a sar ontology. In: IFIP International Conference on Artificial
    Intelligence Applications and Innovations. pp. 360–374. Springer (2024). https:
    //doi.org/10.1007/978-3-031-63223-5_27
12. ETSI: SmartM2M; Extension to SAREF; Part 9: Water Domain (SAREF4WATR).
    ETSI TS 103 410-9 V1.1.2 (2020), https://saref.etsi.org/saref4watr/v1.1.1/
13. Euzenat, J., Meilicke, C., Stuckenschmidt, H., Shvaiko, P., Trojahn, C.: The ontology
    alignment evaluation initiative. Journal on Data Semantics XV pp. 158–192 (2011).
    https://doi.org/10.1007/978-3-642-22630-4_6
14. Fathallah, N., Das, A., De Giorgis, S., Poltronieri, A., Haase, P., Kovriguina,
    L., Simperl, E., Meroño-Peñuela, A., Staab, S., Algergawy, A.: Extended NeOn-
    GPT: Advancing LLM-Powered Ontology Learning Through Ontology Reuse and
    Automated Verification. Semantic Web Journal (2026). https://doi.org/10.1177/
    22104968261453138
15. Fernández-Izquierdo, A., Poveda-Villalón, M., García-Castro, R.: CORAL: a cor-
    pus of ontological requirements annotated with lexico-syntactic patterns. In: The
    Semantic Web: 16th International Conference, ESWC 2019. pp. 443–458. Springer
    (2019). https://doi.org/10.1007/978-3-030-21348-0_29
16. Fernández-Izquierdo, A., Poveda-Villalón, M., García-Castro, R.: Analysing on-
    tological requirements: a journey from requirements to code and back. In: XIX
    Conferencia de la Asociación Española para la Inteligencia Artificial (CAEPIA
    20/21). pp. 122–127. Málaga, Spain (Sep 2021), https://oa.upm.es/83630/
17. Garijo, D., Poveda-Villalón, M., Amador-Domínguez, E., Wang, Z., García-Castro,
    R., Corcho, O.: Llms for ontology engineering: A landscape of tasks and bench-
    marking challenges. In: ISWC 2024 Special Session on Harmonising Generative AI
    and Semantic Web Technologies (2024), https://ceur-ws.org/Vol-3953/
18. Gemma Team, Google DeepMind: Gemma 4. https://ai.google.dev/gemma/docs/
    core/model_card_4 (2026)
19. Glimm, B., Horrocks, I., Motik, B., Stoilos, G., Wang, Z.: HermiT: an OWL 2
    reasoner. Journal of Automated Reasoning 53(3), 245–269 (2014). https://doi.org/
    10.1007/s10817-014-9305-1
20. Goyal, P.K., Singh, S., Tiwary, U.S.: silp_nlp at LLMs4OL 2024 tasks a, b, and c:
    Ontology learning through prompts with llms. In: Open Conference Proceedings.
    vol. 4, pp. 31–38 (2024). https://doi.org/10.52825/ocp.v4i.2485
21. Iannella, R., Villata, S.: ODRL information model 2.2. W3C Recommendation
    (2018), https://www.w3.org/TR/odrl-model/
22. Keet, C.M.: The African Wildlife Ontology tutorial ontologies. Journal of Biomedical
    Semantics 11(1), 4 (2020). https://doi.org/10.1186/s13326-020-00224-y
23. Kholmska, G., Kenda, K., Rozanec, J.: Enhancing ontology engineering with LLMs:
    From search to active learning extensions. In: Proceedings of Data Mining and
    Data Warehouses – SiKDD 2024 (2024). https://doi.org/10.70314/is.2024.sikdd.28
24. Levenshtein, V.I.: Binary codes capable of correcting deletions, insertions, and
    reversals. Soviet Physics Doklady 10(8), 707–710 (1966)
25. Li, J., Garijo, D., Poveda-Villalón, M.: Large language models for ontology engineer-
    ing: a systematic literature review. Semantic Web Journal 17(4), 22104968261465514
    (2026). https://doi.org/10.1177/22104968261465514
                                                                         CQ4OE          19

26. Li, J., Wang, Z., Garijo, D., Poveda-Villalón, M.: MASEO: A multi-agent system
    for explainable ontology generation. In: Proceedings of the 1st Workshop on LLM-
    driven Knowledge Graph and Ontology Engineering (LLM4KGOE 2026), co-located
    with the 23rd European Semantic Web Conference (ESWC 2026). CEUR Workshop
    Proceedings, CEUR-WS.org, Dubrovnik, Croatia (May 2026), https://oa.upm.es/
    97387/
27. Li, J., Wang, Z., Garijo, D., Poveda-Villalón, M.: oeg-upm/maseo: V1.1 — MASEO:
    Multi Agent System for Explainable Ontology generation (mar 2026). https://doi.
    org/10.5281/zenodo.19052003, https://doi.org/10.5281/zenodo.19052003
28. Liang, P., Bommasani, R., Lee, T., Tsipras, D., Soylu, D., Yasunaga, M., Zhang,
    Y., Narayanan, D., Wu, Y., Kumar, A., et al.: Holistic evaluation of language
    models. Transactions on Machine Learning Research 2023-August (2023). https:
    //doi.org/10.48550/arXiv.2211.09110
29. Lin, D.: An information-theoretic definition of similarity. In: Proceedings of the
    Fifteenth International Conference on Machine Learning (ICML 1998). pp. 296–304.
    Morgan Kaufmann (1998)
30. Lippolis, A.S., Saeedizade, M.J., Keskisärkkä, R., Gangemi, A., Blomqvist, E., Nuz-
    zolese, A.G.: Assessing the capability of large language models for domain-specific
    ontology generation. In: Proceedings of the Second Workshop on Evaluation of Lan-
    guage Models in Knowledge Engineering (ELMKE). CEUR Workshop Proceedings,
    vol. 3977 (2025), https://ceur-ws.org/Vol-3977/elmke-2.pdf
31. Lippolis, A.S., Saeedizade, M.J., Keskisärkkä, R., Zuppiroli, S., Ceriani, M.,
    Gangemi, A., Blomqvist, E., Nuzzolese, A.G.: Ontology generation using large
    language models. In: European Semantic Web Conference. pp. 321–341. Springer
    (2025). https://doi.org/10.1007/978-3-031-94575-5_18
32. Mahlaza, Z., Keet, C.M., Chahinian, N., Haydar, B.: On the feasibility of LLM-
    based automated generation and filtering of competency questions for ontologies. In:
    Proceedings of the 5th Conference on Language, Data and Knowledge. pp. 136–146.
    Unior Press, Naples, Italy (Sep 2025), https://aclanthology.org/2025.ldk-1.15/
33. Malone, J., Brown, A., Lister, A.L., Ison, J., Hull, D., Parkinson, H., Stevens, R.:
    The Software Ontology (SWO): a resource for reproducibility in biomedical data
    analysis, curation and digital preservation. Journal of Biomedical Semantics 5(25),
    1–13 (2014). https://doi.org/10.1186/2041-1480-5-25
34. Masa, P., Meditskos, G., Kintzios, S., Vrochidis, S., Kompatsiaris, I.: Ontology-
    based modelling and reasoning for forest fire emergencies in resilient societies. In:
    Proceedings of the 12th Hellenic Conference on Artificial Intelligence. pp. 1–9 (2022).
    https://doi.org/10.1145/3549737.3549765
35. Noy, N.F., McGuinness, D.L., Hayes, P., Welty, C.: Wine ontology. W3C
    OWL Web Ontology Language Guide (2004), https://www.w3.org/TR/2004/
    REC-owl-guide-20040210/wine.rdf
36. Pan, X., Ossenbruggen, J.v., de Boer, V., Huang, Z.: A rag approach for generating
    competency questions in ontology engineering. In: Research Conference on Metadata
    and Semantics Research. pp. 70–81. Springer (2024). https://doi.org/10.1007/
    978-3-031-81974-2_6
37. Parkkila, J., Radulovic, F., Garijo, D., Poveda-Villalón, M., Ikonen, J., Porras, J.,
    Gómez-Pérez, A.: An ontology for videogame interoperability. Multimedia tools and
    applications 76(4), 4981–5000 (2017). https://doi.org/10.1007/s11042-016-3552-6
38. Perera, O., Liu, J.: Exploring large language models for ontology learning. Issues in
    Information Systems 25, 299–310 (2024). https://doi.org/10.48009/4_iis_2024_124
39. Peroni, S.: SAMOD: an agile methodology for the development of ontologies (11
    2016). https://doi.org/10.6084/m9.figshare.3189769.v4
20      J. Li et al.

40. Pisu, A., Pompianu, L., Salatino, A., Osborne, F., Riboni, D., Motta, E., Refor-
    giato Recupero, D., et al.: Leveraging language models for generating ontologies
    of research topics. In: CEUR WORKSHOP PROCEEDINGS. vol. 3747, p. 11.
    CEUR-WS (2024), https://ceur-ws.org/Vol-3747/
41. Plu, J., Escobar, O.M., Trouillez, E., Gapin, A., Troncy, R.: A comprehensive
    benchmark for evaluating llm-generated ontologies. In: ISWC 2024 Special Session
    on Harmonising Generative AI and Semantic Web Technologies (2024), https:
    //ceur-ws.org/Vol-3953/
42. Poveda-Villalón, M., Fernández-Izquierdo, A., Fernández-López, M., García-Castro,
    R.: Lot: An industrial oriented ontology engineering framework. Engineering Ap-
    plications of Artificial Intelligence 111, 104755 (2022). https://doi.org/10.1016/j.
    engappai.2022.104755
43. Poveda-Villalón, M., Gómez-Pérez, A., Suárez-Figueroa, M.C.: Oops! (ontology
    pitfall scanner!): An on-line tool for ontology evaluation. Int. J. Semantic Web Inf.
    Syst. 10(2), 7–34 (2014). https://doi.org/10.4018/ijswis.2014040102
44. Qwen Team: Qwen3.6. https://qwen.ai/blog?id=qwen3.6 (2026), alibaba Group
45. Rebboud, Y., Lisena, P., Tailhardat, L., Troncy, R.: Benchmarking llm-based
    ontology conceptualization: A proposal. In: ISWC 2024 Special Session on Harmon-
    ising Generative AI and Semantic Web Technologies (2024), https://ceur-ws.org/
    Vol-3953/
46. Rebboud, Y., Tailhardat, L., Lisena, P., Troncy, R.: Can LLMs Generate Compe-
    tency Questions? In: The Semantic Web: ESWC 2024 Satellite Events. pp. 71–80.
    Springer (2025). https://doi.org/10.1007/978-3-031-78952-6_7
47. Resnik, P.: Disambiguating noun groupings with respect to wordnet senses. In:
    Third Workshop on Very Large Corpora (1995). https://doi.org/10.48550/arXiv.
    cmp-lg/9511007
48. Saeedizade, M.J., Blomqvist, E.: Navigating ontology development with large
    language models. In: European Semantic Web Conference. pp. 143–161. Springer
    (2024). https://doi.org/10.1007/978-3-031-60626-7_8
49. Salamon, J.S., Barcellos, M.P.: Towards a framework for continuous ontology
    engineering. In: ONTOBRAS. pp. 158–165 (2022), https://ceur-ws.org/Vol-3324/
50. Sedding, J., Kazakov, D.: Wordnet-based text document clustering. In: Proceedings
    of the 3rd workshop on RObust Methods in Analysis of Natural Language Data
    (ROMAND 2004). pp. 104–113 (2004), https://aclanthology.org/W04-2405/
51. Stadlhofer, B., Salhofer, P., Durlacher, A.: An overview of ontology engineering
    methodologies in the context of public administration. In: Proceedings of the Seventh
    International Conference on Advances in Semantic Processing (SEMAPRO). pp. 36–
    42 (2013), http://personales.upv.es/thinkmind/dl/conferences/semapro/semapro_
    2013/semapro_2013_2_30_50039.pdf
52. Toro, S., Anagnostopoulos, A.V., Bello, S.M., Blumberg, K., Cameron, R., Car-
    mody, L., Diehl, A.D., Dooley, D.M., Duncan, W.D., Fey, P., et al.: Dynamic
    retrieval augmented generation of ontologies using artificial intelligence (DRAGON-
    AI). Journal of Biomedical Semantics 15(1), 19 (2024). https://doi.org/10.1186/
    s13326-024-00320-3
53. Tsatsaronis, G., Balikas, G., Malakasiotis, P., Partalas, I., Zschunke, M., Alvers,
    M.R., Weissenborn, D., Krithara, A., Petridis, S., Polychronopoulos, D., et al.: An
    overview of the BIOASQ large-scale biomedical semantic indexing and question
    answering competition. BMC Bioinformatics 16, 1–28 (2015). https://doi.org/10.
    1186/s12859-015-0564-6

