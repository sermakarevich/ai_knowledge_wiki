> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Experimental Setup: Datasets, Retrieval Tuning, and Evaluation Criteria
**In one sentence:** The evaluation uses 39 competency questions (20 from four Onto-DESIDE modules, 19 from an internal Bosch ontology) created by removing classes and referencing properties, with retrieval fixed to text-embedding-ada-002 (pipe separator, with comments, Mw 0.63) and LLMs o1-preview and GPT-5, assessed by structural, functional (CQ verification plus refined superfluous-element count), and human Correctness/Completeness ratings.
## Key points
- Dataset covers two settings jointly evaluated: four Onto-DESIDE ontology-network modules (circular-economy interoperability, 20 CQs) and an internal Bosch manufacturing ontology (19 CQs).
- CQs were created by selecting random classes C, removing each class c plus properties whose domain/range references c, iteratively adding subclasses and their referencing properties, then writing one CQ per removed class/properties asking what it was intended to represent.
- Input ontologies were converted to Turtle with compact prefixes; token counts use the GPT-4o tokeniser, with EU-project part 1 largest at 75,000 tokens / 2920 axioms / 405 classes+properties and part 4 smallest at 6,000 tokens / 228 axioms / 54 classes+properties.
- Retrieval tuning compared 3 OpenAI embedding models (text-embedding-3-small, text-embedding-3-large, text-embedding-ada-002) × separator (| vs newline) × comments in/out on 5 held-out CQs, judged manually by two cross-checking ontology engineers with P@3 and P@20.
- Best retrieval was text-embedding-ada-002 with pipe-separated axioms plus comments (Mprod 0.23, Mw 0.63 where Mw = 0.7·P3 + 0.3·P20), selected for the main experiment; both Mw and Mprod = P3·P20 agreed per model.
- Extender LLMs are o1-preview (best in prior work [16]) and GPT-5 (latest OpenAI model); no other families were tested, and the prompt (general template + retriever elements + CQ placeholder + formalism directive) was iteratively refined on a disjoint dev set to remove typical axiom errors.
- Expressivity differs by setting by design: EU-project requests OWL restrictions in generated fragments, industry disallows OWL restrictions and requires only SHACL shapes, so the two settings are not comparable on OWL expressivity.
- Evaluation is multidimensional: OOPS! + Pellet + RDFLib syntax check (structural), CQ verification via writable SPARQL plus superfluous-element count where only named classes/properties absent from the query AND unconnected by subClassOf/subPropertyOf count (functional), and six-engineer Likert survey on Correctness (fragment alone) and Completeness (fragment + input ontology, effort to make usable).
---
## Dataset creation
**Covers:** Section 4 opening through dataset-creation procedure

> "In this section, we describe the experimental setup, including the dataset we created, parameter tuning for the retrieval and the extender module, and the evaluation criteria."

Procedure as stated:
1. "Select a random set of classes C from the ontology."
2. "For each class c, remove c and add to the set P all properties whose domain or range restrictions references c."
3. "Iteratively expand the removal process by adding c all subclasses of each removed class to C, and include in P any properties that reference these subclasses. This step is repeated iteratively until no additional subclasses are found."
4. "Finally, construct a set of CQs associated with C and P. Each CQ is formulated by asking what each corresponding class with its properties, were intended to represent or accomplish within the original ontology."

> "This procedure yields a set of CQs that systematically probe the missing ontology components, enabling an effective evaluation of the OntoExtend framework."

Settings: "four modules of the Onto-DESIDE ontology network, treated jointly as one setting (20 CQs), and an internal Bosch ontology (19 CQs)" — "Onto-DESIDE addresses circular economy data interoperability, whereas the Bosch setting follows a more manufacturing industrial profile."

## Dataset statistics
**Covers:** Dataset statistics paragraph and Table 2

- "The EU-project parts have 20 CQs in total, while the Industry ontology comprises 19 CQs."
- "Detailed counts of tokens, the sum of classes and properties, and axiom counts for each subset are provided in the GitHub repository."
- "The input ontologies were converted to Turtle with compact prefix declarations to reduce size."
- "Token counts are measured using the GPT-4o tokeniser (https://platform.openai.com/tokenizer), see Table 2."

Table 2. Token counts of input ontologies after conversion to Turtle.

| Ontology fragment | Size (tokens) | Axioms | Classes+Properties |
|---|---|---:|---:|
| EU-project — part 1 | 75 000 | 2920 | 405 |
| EU-project — part 2 | 22 000 | 958 | 242 |
| EU-project — part 3 | 25 000 | 1172 | 270 |
| EU-project — part 4 | 6 000 | 228 | 54 |
| Industry use case | 22 000 | 979 | 134 |

## Parameter and configuration tuning — best retrieval configuration
**Covers:** Retrieval tuning paragraphs and Table 3

- Tuning ran "on a separate subset to find out the best embedding model and parameter configuration to test on the main experiment, along with the best prompt to minimise the common mistakes by LLMs in ontology generation."
- Compared "three OpenAI embedding models: text-embedding-3-small, text-embedding-3-large, and text-embedding-ada-002 under four different styles of formulating ontology elements as a raw text", varying "the delimiter used to separate consecutive elements, comparing the use of a pipe character (|) with the use of a newline character (\n)" and whether comments are included.
- Judged manually "on five CQs not present in the test data", computing "precision at 3 and 20 (focusing on top-3 retrieved for answer quality in case of creating a small ontology subset, but still monitoring top-20 to have an estimate of recall)", with "two ontology engineers cross cross-checking each other's work".
- Primary metric: "Mw = 0.7 P3 + 0.3 P20 which emphasises the quality of the very top-ranked results (those most likely to be consumed by the LLM in Ontology Extender) while still rewarding configurations that retrieve more relevant items in the top 20"; additional check "Mprod = P3 · P20, which penalises configurations that perform well at only one cutoff. Both metrics agreed on the same best configuration per model."
- Result: "Across all 12 configurations, the best overall result came from text-embedding-ada-002 with pipe-separated element axioms and comments included. On this basis, we selected that as the embedding model for the main experiment."

Table 3. Embedding model comparison results (top configurations shown).

| Embedding model | Separator, Comments | Mprod | Mw |
|---|---|---:|---:|
| text-embedding-3-small | Newline, with Comments | 0.22 | 0.62 |
| text-embedding-3-large | Newline, without Comments | 0.20 | 0.54 |
| text-embedding-ada-002 | Pipe, with Comments | 0.23 | 0.63 |

## Best prompt and LLM extender
**Covers:** LLM selection and prompt-development paragraphs

- "For the LLMs, we selected o1-preview, reported as the best-performing model in previous work [16], and GPT-5, the latest LLM from OpenAI. We did not select other models or families because previous studies reported lower performance relative to o1-preview for what concerns ontology generation tasks [16]."
- "Prompt development followed the same tuning procedure used for retrieval": fixed retrieval, then "evaluated several prompt variants on a small development set of CQs (disjoint from the main evaluation set)"; baseline "modelled closely on the prompt used in previous work [16] and was augmented with an explicit list of observed pitfalls"; refined iteratively with "two ontology engineers inspect[ing] generated axioms for recurrent problems".
- "The final prompt comprises (i) a general template that specifies the task and required output format, (ii) a section into which the Ontology Retriever's elements are inserted, (iii) a placeholder for the given CQ, and (iv) a directive that indicates the expected modelling formalism."
- "The framework populates all components automatically, while the style directive may be supplied by the user to constrain output style."
- Formalism split: "in the EU-Project, this section requested OWL restrictions for creating restrictions in the generated ontologies; in the industry use case, we disallowed OWL restrictions and required only SHACL shapes. Consequently, the two use cases should not be interpreted as testing the same level of OWL expressivity. The EU-project setting evaluates OWL-style fragment generation, whereas the industry setting evaluates extension under a SHACL-oriented engineering profile."
- "The final prompt template is available on the Github repository."

## Evaluation criteria (Section 4.1)
**Covers:** Section 4.1 through Correctness/Completeness Likert definitions

- "Building on previous studies in LLM-assisted knowledge engineering [16], we adopt a multidimensional evaluation setup that combines structural and functional metrics along with human evaluation."
- Structural: "We employ the Ontology Pitfall Scanner (OOPS!) [23] for reporting on pitfalls, Pellet reasoner and syntax checking through the RDFLib Python library."
- Functional — CQ verification [2]: "evaluates whether a given CQ is actually represented in the ontology by attempting to formulate a SPARQL query that retrieves an answer for that CQ. If no such SPARQL query can be written to obtain an answer, the CQ is considered not modelled in the ontology."
- Functional — superfluous elements (modified from Lippolis et al. [16]): "a superfluous element is a named class or property that: 1) is not mentioned in the verification SPARQL used to in CQ verification, and 2) is not connected to any component appearing in that query by a subClassOf or subPropertyOf relation"; hierarchical relatives are not superfluous, "while genuinely disconnected named classes and object properties are flagged as superfluous."
- Survey: "six ontology engineers from both academia and industry", criteria "adapted from Monka et al. [19]"; "Correctness measures the syntactic and semantic quality of the generated fragment in isolation, and Completeness measures the sufficiency of the generated fragment after it has been combined with the input ontology; it captures the amount of effort required by an ontology engineer to make the fragment usable." Ratings on "a five-point Likert scale".
- Correctness scale: 1 = "generation failure, for example because the output exceeded token limits"; 2 = "syntactically erroneous fragment, such as one containing issues in the generated code"; 3 = "syntactically correct but semantically incorrect, for instance due to an inappropriate taxonomy"; 4 = "both syntactically and semantically correct, but does not fully satisfy the intent of the competency question (CQ)"; 5 = "syntactically and semantically correct and fully aligned with the intended meaning of the CQ."
- Completeness scale: 1 = "not useful and would require complete manual reworking"; 2 = "significant changes are needed, corresponding roughly to 25–40% of the fragment requiring modification"; 3 = "moderate changes, with approximately 11–25% of the fragment needing revision"; 4 = "only minor changes are required, typically affecting around 1–10% of the fragment"; 5 = "in combination with the input ontology, is complete and correct."

**Covers:** Experimental setup — datasets, retrieval/embedding tuning, and evaluation criteria (plan.md chunk 03-in-this-section-we-describe-the; source Section 4 through Section 4.1; chunk tail previews Section 5 / 5.1 Structural Evaluation without body).
