# Large Language Models for Ontology Engineering: A Systematic Literature Review | www.semantic-web-journal.net
Source: https://www.semantic-web-journal.net/content/large-language-models-ontology-engineering-systematic-literature-review
Kind: article
Fetched: 2026-09-23T13:00:14.292716+00:00
Tool: urllib
PDF: https://www.semantic-web-journal.net/content/large-language-models-ontology-engineering-systematic-literature-review (no local source.pdf archived; see Source)
Research-Target: /Users/sergii/.ai/knowledge/research_topics/ontology_ai/research/ontology-ai
Topic: ontology_ai

Large Language Models for Ontology Engineering: A Systematic Literature Review | www.semantic-web-journal.net

Skip to main content area

Semantic Web – Interoperability, Usability, Applicability an IOS Press Journal

## Search form

## Main menu

About

Calls

Blog

Issues

Under Review

Reviewed

For Authors

For Reviewers

Scientometrics

FAQ

## Login

Username or e-mail *

Password *

Create new account

Request new password

## Editorial Board

Editor-in-Chief

Cogan Shimizu

Eva Blomqvist

Editorial Board

Mehwish Alam

Claudia d’Amato

Stefano Borgo

Boyan Brodaric

Philipp Cimiano

Michael Cochez

Oscar Corcho

Bernardo Cuenca-Grau

Elena Demidova

Jerome Euzenat

Sebastián Ferrada

Mark Gahegan

Aldo Gangemi

Dagmar Gromann

Armin Haller

Pascal Hitzler

Aidan Hogan

Katja Hose

Eero Hyvönen

Krzysztof Janowicz

Sabrina Kirrane

Agnieszka Lawrynowicz

Maria Maleshkova

Raghava Mutharaju

Axel Polleres

Guilin Qi

Marta Sabou

Harald Sack

Angelo Salatino

Christoph Schlieder

Stefan Schlobach

Cogan Shimizu

Blerina Spahiu

Sanju Tiwari

Jouni Tuominen

GQ Zhang

Rui Zhu

Former/Founding Editors-in-Chief

Krzysztof Janowicz

Pascal Hitzler

Editorial Assistants

Michael McCain

## Syndicate

# Large Language Models for Ontology Engineering: A Systematic Literature Review

Submitted by Jiayi Li on 04/30/2025 - 18:40

### Tracking #: 3864-5078

A new version of this paper is available

Authors: 

Jiayi Li

Maria Poveda

Daniel Garijo

Responsible editor: 

Guilin Qi

Submission type: 

Survey Article

Abstract: 

Ontology engineering (OE) is a complex task in knowledge representation that relies heavily on domain experts to accurately define concepts and precise relationships in a domain of interest, as well as to maintain logical consistency throughout the resultant ontology. Recent advancements in Large Language Models (LLMs) have created new opportunities to automate and enhance various stages of ontology development. This paper presents a systematic literature review on the use of LLMs in OE, focusing on their roles in core development activities, input-output characteristics, evaluation methods, and application domains. We analyze 30 different papers to identify common tasks where LLMs have been applied, such as ontology requirements specification, implementation, publication, and maintenance. Our findings indicate that LLMs serve primarily as ontology engineers, domain experts, and evaluators, using models such as GPT, LLaMA, and T5 to process heterogeneous inputs (such as OWL ontologies, text, competency questions, etc.) to generate task-specific outputs (such as examples, axioms, documentation, etc.). Our review also observed a lack of homogenization in task definitions, dataset selection, evaluation metrics, and experimental workflows. At the same time, some papers do not release complete evaluation protocols or code, making their results hard to reproduce and their methods insufficiently transparent. Therefore, the development of standardized benchmarks and hybrid workflows that integrate LLM automation with human expertise will become an important challenge for future research.

Full PDF Version: 

swj3864.pdf

Revised Version:

Large Language Models for Ontology Engineering: A Systematic Literature Review

Tags: 

Reviewed

Long-term Stable Link to Resources: 

https://github.com/oeg-upm/llm4oe-slr

Decision/Status: 

Major Revision

Solicited Reviews:

Click to Expand/Collapse

Review #1

Anonymous submitted on 12/Jun/2025

Suggestion:

Minor Revision

Review Comment:

This paper provides a comprehensive review of the application of large language models (LLMs) in ontology engineering (OE). It examines various stages of ontology development—such as requirements specification, implementation, publication, and maintenance—by analyzing 30 studies.

Strengths:

S1. This paper aligns well with the journal's theme and serves as a comprehensive and valuable review for readers interested in OE.

S2. The paper offers valuable insights into how LLMs can automate aspects of OE while also pointing out the limitations in current studies. The authors effectively frame the need for standardized benchmarks and hybrid workflows that integrate human expertise, setting the stage for future advancements.

Weaknesses and areas for improvement:

W1. Although the authors organize the content using a question-answer-summary format, the overall structure still feels scattered, making the main findings unclear. I believe that part of the reason is that there are still few studies on the application of large language models in the field of OE, and the specific research tasks are quite dispersed, resulting in less commonality among studies. So, this shortcoming is not an issue with this paper itself, but rather a result of the existing literature in this field.

W2. In my view, some parts of Section 4.1 and Section 4.2.1 are essentially redundant, as the activity at which an LLM is involved already indicates its role.

W3. Moreover, I think that the title of Section 4.2 does not align with its content. The title is "How do LLM-based approaches support different ontology development activities?" However, the section primarily analyzes the roles of LLMs, their inputs and outputs, model versions, etc., rather than technically summarizing and answering "how to do" from an implementation perspective. If possible, I suggest that the authors add a technical perspective summary. I believe that the lack of technical content is the biggest shortcoming of this paper.

W4. Presentation could be further improved. For example, the rectangles in Figure 2 can be flattened slightly to make the layout more compact.

Review #2

 By Tianxing Wu submitted on 21/Oct/2025

Suggestion:

Major Revision

Review Comment:

The topic of this paper, LLMs for Ontology Engineering, is a timely and important subject within the fields of Artificial Intelligence and the Semantic Web. The authors clearly identify the gaps in existing research within the Introduction. They explicitly list four research objectives, mapping them to four Research Questions (RQs), which form the core structure of the entire results section. Crucially, the paper does not merely list the 30 included publications; instead, it extracts 41 distinct studies and provides a synthesized analysis of these data points structured around the RQs. The logical structure and overall presentation in the current manuscript are generally clear. The authors also provide relatively rich and well-organized data files via GitHub and Zenodo, though a clarifying README file is missing. Overall, this paper is suitable as an introductory text for practitioners in Semantic Web. However, before it meets the requirements for publication, I have several concerns and recommendations, detailed below:

1. The paper mentions that this work is an extension of an earlier overview article (Garijo et al. 2024). It is essential that the authors clearly and explicitly articulate the unique, novel contributions of the current manuscript. This clarification must go beyond a simple increase in the number of papers and should include a clear statement of the substantive new analyses and new insights gained in this extended work.

2. In a high-profile area like LLMs and the Semantic Web, filtering the initial 11,985 retrieved results from 2018 to 2024 down to only 30 core papers (which appear to be predominantly from 2023 to 2024 based on the materials provided) seems a comparatively low number. This may be a consequence of the search terms (MR Terms) being restricted to "Language Model," "LM," and "LLM*." While these terms cover the general concepts, this strategy likely missed relevant work conducted between 2018 and 2021 (before "LLM" became common usage) that used specific models (e.g., BERT, T5) for ontology engineering but did not explicitly use "LM" or "LLM" in the abstract or keywords. The authors should discuss this potential limitation.

3. While the paper demonstrates critical thought in the Evaluation (RQ3) and Discussion (Section 5), there is a problem of excessive description in certain parts. For example, Section 4.4 (RQ4: Application Domains) largely constitutes a list of which papers were applied in which fields (healthcare, cultural heritage, finance, etc.). It lacks a deeper analysis of why these domains are hot spots (e.g., due to data availability, clear commercial needs, or the maturity of existing ontologies). Furthermore, there is no analysis of the commonalities or differences in the tasks addressed across these various domains. Similarly, Section 4.2.4 (RQ2.e: Role of the Human) is very brief. The finding that only four studies explicitly involve human participants is a significant observation, yet the paper's analysis of this crucial point could be much more profound.

4. The paper suffers from noticeable redundancy. Each subsection of Section 4 (Results) concludes with a detailed Summary section. While these summaries are well-written, they cause Section 5 (Discussion) to feel repetitive. Many of the core arguments presented in the Discussion have already been thoroughly emphasized in the Section 4 summaries. I recommend that the authors reorganize the relevant sections to convey their interpretive insights.

5. For a systematic review of this length and depth, the overall visual presentation is insufficient. In particular, the paper is missing a comprehensive taxonomic framework diagram. Such a visualization is crucial for helping the reader gain a clear, "at-a-glance" understanding of how the authors have organized and categorized the entire research field.

Log in or register to post comments

16243 reads

## Reviewed Articles

All accepted articles

All reviewed articles

Accepted articles by views

Accepted survey articles

Accepted tools/system papers

Accepted Dataset descriptions

## Authors & Reviewers

Submission Types

Submission Guidelines

Open and Transparent Reviews

## Links

SWJ at IOS Press

SWJ online issues at IOS Press

SWJ Scientometrics Portal

SWJ at Twitter

SWJ at DBLP

Job Postings

Book series 'Studies on the Semantic Web'

## Recent blog posts

Special Issue on Semantic Materials Science and Engineering (SMSE)

Off To New Adventures

Special Issue on Bridging Machine Learning and Knowledge Representation

Special Issue on Geospatial Knowledge Graphs

Special issue on Large Language Models, Generative AI and Knowledge Graphs

2024 Journal Impact Metrics

Special issue on the Semantic Web and Ontology Design for Cultural Heritage

Special Issue on the Pedagogy and Praxis of Knowledge Graphs and the Semantic Web

Special issue on Knowledge Graph Construction

Taking My Leave

More

## Accepted Articles

Pre-prints of accepted articles

Disclaimer | Privacy Policy| SWJ is Published by IOS Press, Copyright 2025
