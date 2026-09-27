> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# CWE Classification of Copilot-Generated Weaknesses
**In one sentence:** Two authors manually mapped scanner warnings to CWE IDs (Cohen's Kappa 0.82, with a security expert breaking ties) and found 628 CWE instances of 43 types in 200 snippets, led by CWE-330 (18.15%), with 233 instances belonging to eight MITRE 2023 Top-25 CWEs.
## Key points
- Manual CWE mapping was done independently by two authors over ten days with Cohen's Kappa of 0.82 (above 0.8, high agreement); disagreements were discussed and resolved with a third author acting as security expert.
- 200 code snippets with security weaknesses contained 628 CWE occurrences across 43 CWE types, showing varied weaknesses when using Copilot and other code generation tools.
- CWE-330 (Use of Insufficiently Random Values) dominates at 114 occurrences (18.15%), followed by CWE-94 Code Injection 62 (9.87%), CWE-79 Cross-site Scripting 60 (9.55%), and CWE-78 OS Command Injection 39 (6.21%).
- 233 of the 628 weaknesses map to eight CWEs on the MITRE 2023 CWE Top-25 list (used as baseline since snippets are mainly from 2022–2023), including high-ranking CWE-79 and CWE-78.
- CWE patterns differ by language: Python weaknesses center on data processing and system calls (e.g., CWE-78 OS Command Injection, CWE-427 Uncontrolled Search Path Element), while JavaScript centers on dynamic code generation and web issues (e.g., CWE-94 Code Injection, CWE-79 Cross-site Scripting).
- CWE patterns differ by application domain and by language within a domain: Python's worst domain is Utility Tool versus JavaScript's Web Applications; within Web Applications, JavaScript's top CWE is CWE-79 (XSS) while Python's is CWE-89 (SQL Injection).
- Low-frequency CWEs (many under 1%) show weakness types track the specific scenarios where developers use generation tools, so vigilance and caution remain necessary when programming.
---
## Manual CWE mapping method
**Covers:** chunk "in conjunction with relevant descriptions from": CWE classification details with descriptions and examples.

- Mapping was done "in conjunction with relevant descriptions from the CWE, to perform manual correspondences."
- "Initially, two authors independently matched each description of the security issue with a CWE ID within a period of ten days."
- "Cohen's Kappa coefficient [9] was 0.82, which was higher than 0.8 and indicated a high level of agreement between the two authors."
- "In case of disagreement, a discussion was initiated between the two authors, and one other author (a security expert) was then involved to provide his assessment."
- "We provided correspondences between the warning prompt messages and CWEs in our online replication package [21]."

## Statistical analysis and Top-25 baseline
- "In the final stage, we performed a statistical analysis of CWE weaknesses in 200 code snippets that contained security weaknesses."
- "Additionally, we analyzed the distribution of different CWEs across different application domains of the code snippets."
- Snippets were "mainly generated in 2022 and 2023"; baseline chosen is "MITRE 2023 CWE Top-25 list [45]".
- "We compared the CWEs obtained in RQ2 with the 2023 CWE Top 25."

## Table 5: Distribution of CWEs (628 total, 43 types)

| CWE-ID | Name | Frequency | Percentage |
|---|---|---:|---:|
| CWE-330 | Use of Insufficiently Random Values | 114 | 18.15% |
| CWE-94 | Improper Control of Generation of Code ('Code Injection') | 62 | 9.87% |
| CWE-79 | Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') | 60 | 9.55% |
| CWE-78 | Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') | 39 | 6.21% |
| CWE-427 | Uncontrolled Search Path Element | 35 | 5.57% |
| CWE-457 | Use of Uninitialized Variable | 30 | 4.78% |
| CWE-22 | Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') | 29 | 4.62% |
| CWE-772 | Missing Release of Resource after Effective Lifetime | 29 | 4.62% |
| CWE-89 | Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') | 27 | 4.30% |
| CWE-259 | Use of Hard-coded Password | 16 | 2.55% |
| CWE-685 | Function Call with Incorrect Number of Arguments | 14 | 2.23% |
| CWE-284 | Improper Access Control | 13 | 2.07% |
| CWE-312 | Cleartext Storage of Sensitive Information | 12 | 1.91% |
| CWE-390 | Detection of Error Condition Without Action | 11 | 1.75% |
| CWE-456 | Missing Initialization of Variable | 11 | 1.75% |
| CWE-607 | Use of Wrong Operator in String Comparison | 11 | 1.75% |
| CWE-770 | Allocation of Resources Without Limits or Throttling | 11 | 1.75% |
| CWE-20 | Improper Input Validation | 8 | 1.27% |
| CWE-665 | Improper Initialization | 8 | 1.27% |
| CWE-117 | Improper Output Neutralization for Logs | 7 | 1.11% |
| CWE-400 | Uncontrolled Resource Consumption | 7 | 1.11% |
| CWE-561 | Dead Code | 7 | 1.11% |
| CWE-732 | Incorrect Permission Assignment for Critical Resource | 6 | 0.96% |
| CWE-798 | Use of Hard-coded Credentials | 6 | 0.96% |
| CWE-215 | Information Exposure Through Debug Information | 5 | 0.80% |
| CWE-290 | Authentication Bypass by Spoofing | 5 | 0.80% |
| CWE-295 | Improper Certificate Validation | 5 | 0.80% |
| CWE-209 | Information Exposure Through an Error Message | 4 | 0.64% |
| CWE-252 | Unchecked Return Value | 4 | 0.64% |
| CWE-571 | Expression is Always True | 4 | 0.64% |
| CWE-605 | Multiple Binds to the Same Port | 4 | 0.64% |
| CWE-200 | Information Exposure | 3 | 0.48% |
| CWE-327 | Use of a Broken or Risky Cryptographic Algorithm | 3 | 0.48% |
| CWE-367 | Time-of-check Time-of-use Race Condition | 3 | 0.48% |
| CWE-563 | Assignment of a Fixed Address to a Pointer | 3 | 0.48% |
| CWE-116 | Improper Encoding or Escaping of Output | 2 | 0.32% |
| CWE-480 | Use of Incorrect Operator | 2 | 0.32% |
| CWE-502 | Deserialization of Untrusted Data | 2 | 0.32% |
| CWE-601 | URL Redirection to Untrusted Site ('Open Redirect') | 2 | 0.32% |
| CWE-208 | Observable Timing Discrepancy | 1 | 0.16% |
| CWE-570 | Expression is Always False | 1 | 0.16% |
| CWE-628 | Function Not Implemented Correctly | 1 | 0.16% |
| CWE-682 | Incorrect Calculation | 1 | 0.16% |
| 43 Types | Total | 628 | — |

Note on chunk inconsistency: the narrative text states "CWE-117: Improper Output Neutralization for Logs only occurred twice", but Table 5 as given in the chunk lists CWE-117 with frequency 7 (1.11%); both values are reproduced as they appear in the chunk.

## Results narrative (verbatim claims)
- "In total, we found 628 CWEs in 200 code snippets with security weaknesses."
- "These security weaknesses were related to 43 CWE types, indicating that developers face a variety of security weaknesses when using Copilot and other code generation tools."
- "CWE-330: Use of Insufficiently Random Values is the most frequently occurring CWE, as it represents 18.15% of the security weaknesses, followed by CWE-94: Code Injection, CWE-79: Cross-site Scripting, and CWE-78: OS Command Injection."
- "It is worth noting that 233 security weaknesses in the code snippet correspond to these eight CWEs, which belong to the Top-25 CWE list, indicating that the CWE Top-25 weaknesses are also prevalent in the code generated by Copilot and other tools."
- "At the same time, we can see that CWE-79: Cross-site Scripting and CWE-78: OS Command Injection are among the most frequently occurring security weaknesses in our results and rank high on the Top-25 CWE list."
- "This indicates that the types of security weaknesses are closely related to the specific scenarios in which developers use code generation tools, emphasizing the importance of maintaining vigilance and caution when programming."

## Language and domain distribution
- "Table 6 presents the top 5 CWEs that appear in Python and JavaScript code snippets." (Table 6 body itself is not in this chunk beyond its title line.)
- "CWEs in Python are mainly related to data processing and system calls, such as CWE-78: OS Command Injection and CWE-427: Uncontrolled Search Path Element."
- "In contrast, CWEs in JavaScript are primarily associated with dynamic code generation problems and security issues in Web development, such as CWE-94: Code Injection and CWE-79: Cross-site Scripting."
- "Furthermore, Figure 14 and Figure 15 show the distribution of CWEs across different application domains."
- "In Python, the application domain with the most CWEs is Utility Tool, while in JavaScript, Web Applications have the most CWEs."
- "In the Web Application category, CWE-79: Cross-site Scripting is the most frequent in JavaScript code snippets, while CWE-89: SQL Injection is the most present in Python code snippets."
