> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# RQ3 Findings: Distinct Preferences in Refactoring Types
**In one sentence:** StarCoder2 favors frequent, syntactic rule-based refactorings (e.g., Rename Method, Extract Method, annotation changes) while developers favor dependency-heavy, structural refactorings (e.g., Move Method, Change Attribute Access Modifier), with complementary strengths in smell reduction and metric improvement.
## Key points
- StarCoder2 performs Rename Method and Extract Method at higher frequency than developers, refactorings detectable by following syntactic rules, while developers more frequently perform Move Method and Change Attribute Access Modifier, which require dependency checks and propagate larger code changes.
- On code-smell reduction (p-value < 0.05, all large Cliff's Delta), StarCoder2 wins 9 of 11 significant refactoring types, including Remove Method Annotation (δ = 0.9619), Modify Class Annotation (δ = 0.9589), Move And Rename Method (δ = 0.9394), Add Method Annotation (δ = 0.9117), and Rename Class (δ = 0.5871).
- Developers win only 2 of the 11 significant smell-reduction types, both attribute-level: Move Attribute (δ = 0.7832) and Change Attribute Type (δ = 0.7796), which require deeper context and data-dependency understanding.
- On code-metric improvement, StarCoder2 wins 3 of 5 significant types — Add Class Annotation (δ = 0.8517), Change Return Type (δ = 0.8032), Rename Class (δ = 0.6123) — while developers win Encapsulate Attribute (δ = 0.6798) and Change Attribute Access Modifier (δ = 0.7215).
- Access-control refactorings (Change Method Access Modifier, Encapsulate Attribute) are unique to StarCoder2, applied in a rule-based manner to visibility/encapsulation; developers instead handle Extract Method, Inline Variable, Extract Superclass, and Pull Up Method, requiring class-hierarchy and modularity reasoning.
- Class-level work diverges: StarCoder2 applies simpler Change Type Declaration Kind and Add Class Modifier, developers apply Extract Superclass and Pull Up Method; package/file movement diverges as StarCoder2 doing Move Package versus developers doing granular Move Source Folder.
- The chunk's stated conclusion is complementarity: "StarCoder2 excels in automated, syntactic refactoring types, while developers focus on more complex, structural changes," so a combined LLM-plus-developer approach "could potentially offer the most comprehensive strategy for code refactoring."
---
## Distribution of refactoring types (Figure 6)
**Covers:** Section 3.3.3, Findings opening (Figure 6 distribution)

Figure 6 shows the distribution of all refactoring types StarCoder2 performs. Per the chunk text:

> "StarCoder2 demonstrates a higher frequency of certain refactorings which can be detected by following syntactic rules, such as Rename Method and Extract Method, compared to developers. Conversely, developers more frequently perform refactorings that require more checks on dependencies and cause a larger impact on code change propagation, such as Move Method and Change Attribute Access Modifier."

## Code-smell reduction by refactoring type (Table 5)
**Covers:** Section 3.3.3, Table 5 (p-value < 0.05)

Table 5 compares refactoring types performed by either StarCoder2 or developers that significantly reduce code smells more than the other:

| Refactoring Type | Better Reduction | Cliff's Delta (δ) | Interpretation |
|---|---|---|---|
| Remove Class Annotation | LLM | 0.6969 | Large |
| Move Class | LLM | 0.6060 | Large |
| Add Method Annotation | LLM | 0.9117 | Large |
| Remove Method Annotation | LLM | 0.9619 | Large |
| Rename Class | LLM | 0.5871 | Large |
| Move Attribute | Developer | 0.7832 | Large |
| Modify Class Annotation | LLM | 0.9589 | Large |
| Add Class Annotation | LLM | 0.8539 | Large |
| Move And Rename Method | LLM | 0.9394 | Large |
| Change Attribute Type | Developer | 0.7796 | Large |
| Move And Rename Class | LLM | 0.5048 | Large |

Chunk text on Table 5:

> "The data shows that StarCoder2 performs significantly better in reducing code smells for refactoring types such as Remove Class Annotation, Remove Method Annotation, and Rename Class. The Cliff's Delta (δ) values for these types indicate a large effect size. StarCoder2 is particularly effective at eliminating annotations and renaming classes in ways that reduce code smells more efficiently than human developers."

> "This is evidenced by the large effect size for Move Attribute and Change Attribute Type. The developers perform better at the attribute level which involves data dependencies; these refactorings often require a deeper understanding of the code's context and architecture. Developers tend to engage in more types of refactoring that involve dependency checks and have a greater impact on the code, demonstrating superior performance in managing complex structural changes."

## Code-metric improvement by refactoring type (Table 6)
**Covers:** Section 3.3.3, Table 6

| Refactoring Type | Better Improvement | Cliff's Delta (δ) | Interpretation |
|---|---|---|---|
| Rename Class | LLM | 0.6123 | Large |
| Add Class Annotation | LLM | 0.8517 | Large |
| Encapsulate Attribute | Developer | 0.6798 | Large |
| Change Return Type | LLM | 0.8032 | Large |
| Change Attribute Access Modifier | Developer | 0.7215 | Large |

## Categorized refactoring patterns (unique focuses)
**Covers:** Section 3.3.3, categorized refactoring focuses

- Access control refactorings, "which are changes to access modifiers and encapsulation of attributes, are unique to StarCoder2, which frequently modifies access levels and encapsulates attributes, addressing visibility and encapsulation issues in a rule-based manner. For instance, StarCoder2 performs refactorings like Change Method Access Modifier and Encapsulate Attribute, focusing on improving data hiding and access control."
- "Developers handle more complex method and attribute refactorings such as Extract Method and Inline Variable, which involve restructuring code for better modularity and readability. These types of refactorings require a deeper understanding of code context."
- "Class-level refactorings also show divergence, with StarCoder2 applying simpler changes like Change Type Declaration Kind and Add Class Modifier, while developers performed more intricate refactorings like Extract Superclass and Pull Up Method, requiring a deeper understanding of class hierarchies."
- "Additionally, package and file movement refactorings are handled differently: StarCoder2 focuses on high-level tasks such as Move Package, while developers engage in more granular changes such as Move Source Folder."
- "The full details of all refactorings unique to StarCoder2 and unique to developers are included in the replication package."

## Summary of Results (verbatim)
**Covers:** Section 3.3.3, Summary of Results box

> "StarCoder2 excels in automated, syntactic refactoring types, while developers focus on more complex, structural changes, demonstrating complementary strengths between the two approaches. A combined approach leveraging both LLMs and developers could potentially offer the most comprehensive strategy for code refactoring."

**Covers:** Section 3.3.3 (RQ3 findings: distinct LLM/developer refactoring preferences)
