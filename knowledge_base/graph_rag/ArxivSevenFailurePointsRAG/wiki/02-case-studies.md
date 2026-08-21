> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Case Studies

**In one sentence:** Three RAG systems — a running literature-review tool, a running university tutor, and a BioASQ biomedical experiment — are described to ground the paper's catalogue of RAG failure points in real implementations across research, education, and biomedical domains.

## Key points

- The three case studies deliberately span different scales: Cognitive Reviewer handles arbitrary-sized PDF collections, AI Tutor works over a fixed unit of 38 learning resources (videos, HTML, PDFs), and BioASQ is a large-scale experiment over 4,017 open-access biomedical documents.
- Cognitive Reviewer is the only case study that performs the Index process at run time (documents are uploaded by the user per session), which removes the possibility of development-time quality control and forces a robust data-processing pipeline.
- Two of the three case studies (Cognitive Reviewer and AI Tutor) are running systems in active use at Deakin University, which is why their scripts and data cannot be made public for confidentiality reasons, unlike BioASQ.
- AI Tutor was built in three months (August–November 2023) specifically to pilot in one unit of ~200 students starting 30 October 2023, making it a deployment-constrained, real-education use case rather than a benchmark.
- AI Tutor's only case study with a query rewriter uses chat history as context to resolve ambiguous follow-up requests such as "Explain this concept further," showing why rewriters matter in conversational RAG settings.
- AI Tutor and BioASQ both index heterogeneous content (videos and HTML in the former, scientific PDFs in the latter), and AI Tutor transcribes videos with the Whisper deep-learning model before chunking them.
- BioASQ is the only case study with pre-existing labelled question–answer pairs, which enables automated evaluation of generated answers with OpenAI's OpenEvals — something the other two, user-facing systems, cannot do at development time.
- In the BioASQ evaluation, 1,000 questions were generated against the indexed documents, 40 generated answers were manually inspected, and every answer OpenEvals flagged as incorrect was reviewed, revealing that the automated evaluator is more pessimistic than human raters in this domain (with the caveat that BioASQ is domain-specific and the human reviewers were not experts).
- The paper's failure-point catalogue (Section 5) is derived directly from these three case studies, and case studies marked with an asterisk in Table 1 are the running systems.

---

## Overview of the three case studies

Reproduced from Table 1 of the paper:

| Case Study | Domain | Doc Types | Dataset Size | RAG Stages | Sample Questions |
|---|---|---|---|---|---|
| Cognitive Reviewer* | Research | PDFs | (Any size) | Chunker, Rewriter, Retriever, Reader | What are the key points covered in this paper? |
| AI Tutor* | Education | Videos, HTML, PDF | 38 | Chunker, Rewriter, Retriever, Reader | What were the topics covered in week 6? |
| BioASQ | Biomedical | Scientific PDFs | 4017 | Chunker, Retriever, Reader | Define pseudotumor cerebri. How is it treated? |

\* Cases marked with a `*` are running systems currently in use.

## Cognitive Reviewer

Cognitive Reviewer is a RAG system designed to support researchers in analysing scientific documents. The workflow is:

1. The researcher specifies a research question or objective.
2. They upload a collection of related research papers.
3. All documents are ranked in accordance with the stated objective, for the researcher to manually review.
4. The researcher can also ask questions directly against all of the uploaded documents.

- **Domain / users:** Research; currently used by PhD students at Deakin University to support their literature reviews.
- **Deployment status:** A running system (marked `*` in Table 1), in active use.
- **RAG stages:** Chunker, Rewriter, Retriever, Reader (Table 1).
- **Dataset / document types:** PDFs, of any size (user-supplied collections at run time).
- **Operational characteristic:** It performs the Index process at run time rather than at deployment, because documents arrive from users per session. This means it relies on a robust data-processing pipeline to handle uploaded documents — there is no quality control possible at development time. It also uses a ranking algorithm to sort the uploaded documents by relevance to the stated objective.

## AI Tutor

The AI Tutor is a RAG system where students ask questions about a university unit and the answers are sourced from the unit's learning content. Students can verify answers by accessing the list of sources that the answer came from.

- **Domain / users:** Education; built for a pilot in a Deakin University unit with ~200 students (commenced 30 October 2023).
- **Development window:** Built between August 2023 and November 2023 for that pilot; the paper reports lessons learned during implementation and promises follow-up findings when the pilot concludes.
- **Deployment status:** A running system (marked `*` in Table 1).
- **Integration / content:** Integrated into Deakin's learning management system, indexing all unit content including PDF documents, videos, and text documents (38 resources in Table 1).
- **Video handling:** As part of the Index process, videos are transcribed with the deep-learning model Whisper before being chunked.
- **RAG stages:** Chunker, Rewriter, Retriever, Reader (Table 1) — one of the two case studies with a rewriter.
- **Conversational context:** Implemented as a chat interface where previous dialogue between the user and the AI Tutor is used as context for each question. The rewriter considers this context and rewrites the query to resolve ambiguous requests such as "Explain this concept further."
- **Sample question (Table 1):** "What were the topics covered in week 6?"

## Biomedical Question and Answer

The previous two case studies focused on documents with smaller content sizes. To explore issues at a larger scale, a RAG system was built on the BioASQ dataset, which comprises questions, links to documents, and answers (with answer types of yes/no, text summarisation, factoid, or list). The dataset was prepared by biomedical experts and contains domain-specific question-and-answer pairs.

- **Domain / users:** Biomedical; an empirical/experimental RAG system rather than a deployed product for end users.
- **Data:** 4,017 open-access scientific PDFs were downloaded from the BioASQ dataset, alongside 1,000 questions (Table 1 lists the dataset size as 4017).
- **RAG stages:** Chunker, Retriever, Reader (Table 1) — notably **without** a Rewriter, unlike the two user-facing case studies.
- **Procedure:** All documents were indexed and the 1,000 questions asked against the RAG system; the generated answers were then evaluated using the OpenEvals technique implemented by OpenAI.
- **Evaluation method and findings:** 40 issues were manually inspected, and all issues that OpenEvals flagged as inaccurate were also reviewed. The automated evaluation was found to be more pessimistic than a human rater in this domain. A stated threat to validity: BioASQ is a domain-specific dataset and the human reviewers were not experts — the LLM may know more than a non-expert.
- **Reproducibility:** All scripts, data, and examples of each failure point for the BioASQ case study are available online (figshare: fbf7805b5f20d7f7e356). The other two case studies (Cognitive Reviewer and AI Tutor) are excluded from publication due to confidentiality concerns.

**Covers:** Section 4 (Case Studies), Table 1
