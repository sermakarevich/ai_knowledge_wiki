[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview: Abstract and Introduction (in-IDE HAX)
**In one sentence:** This systematic literature review of 90 studies defines in-IDE Human-AI Experience (HAX) and organizes findings into Impact, Design, and Quality dimensions, reporting productivity gains alongside verification overhead, over-reliance, and code-quality risks.
## Key points
- Reviews 90 relevant studies (from 257 identified) via a PRISMA-guided SLR combining database search, backward snowballing, and expert-informed additions, extending an earlier non-systematic survey of 36 papers (Sergeyuk et al., 2024).
- Frames in-IDE HAX as the shift from HCI to HAX where AI acts as an active collaborator rather than just a tool, focused on what happens where code is written, inspected, or tested rather than AI in software engineering broadly.
- Cites industry adoption pressure: 76% of respondents are using or planning to use AI tools (Stack Overflow, 2024), and more than 50% note reduced search time, faster coding, quicker repetitive tasks, and higher productivity (JetBrains, 2024).
- Impact dimension (74/90 studies): AI-assisted coding enhances productivity, especially among experienced users, but increases verification time and raises over-reliance concerns.
- Design dimension (28/90 studies): covers autocompletion, conversational, and emerging hybrid systems; prompt structure plus interface properties — context awareness, transparency/explanations, and user control — shape experience.
- Quality dimension (19/90 studies): evaluates correctness, maintainability, and security of generated code, often calling for improved validation and diagnostic support.
- Claims to be, to the best of the authors' knowledge, the first systematic review of in-IDE HAX, positioned as a foundational reference for cumulative and reproducible progress rather than a follow-up.
- Future agenda: larger and longer evaluations, stronger audit/verification assets, broader SDLC coverage (requirements, testing, deployment), longitudinal and comparative designs, and adaptive assistance under user control; gaps include non-users/stopped-users, educational contexts, AI governance, and proactivity.
---
## Abstract
**Covers:** title block, authors, arXiv identifier, abstract paragraph

- Paper: "Human-AI Experience in Integrated Development Environments: A Systematic Literature Review" by Agnia Sergeyuk, Ilya Zakharov, Ekaterina Koshchenko (JetBrains Research) and Maliheh Izadi (Delft University of Technology).
- Identifier: arXiv:2503.06195v3 [cs.SE] 15 Jan 2026. Received/Accepted dates listed as "date".
- Verbatim framing: "The integration of Artificial Intelligence (AI) into Integrated Development Environments (IDEs) is reshaping software development, fundamentally altering how developers interact with their tools."
- Verbatim gap: "Despite rapid adoption, research on in-IDE HAX remains fragmented, which highlights the need for a unified overview of current practices, challenges, and opportunities."
- Three aspects verbatim: "Impact, Design, and Quality of AI-based systems inside IDEs."
- Abstract's Impact summary: "AI-assisted coding enhances developer productivity but also introduces challenges, such as verification overhead and over-reliance."
- Abstract's Design summary: "effective interfaces surface context, provide explanations and transparency of suggestion, and support user control."
- Abstract's Quality summary: "risks in correctness, maintainability, and security."
- Abstract's agenda verbatim: "larger and longer evaluations, stronger audit and verification assets, broader coverage across the software life cycle, and adaptive assistance under user control."

## Keywords and classification
**Covers:** keywords, MSC lines (p. 2)

| Field | Value (verbatim) |
|---|---|
| Keywords | Human-Computer Interaction · Artificial Intelligence · Integrated Development Environment · Programming · User Studies · User Experience |
| Mathematics Subject Classification (2020) | 68N01 · 68T01 · 68U35 |

## 1 Introduction
**Covers:** Section 1, pp. 2–4 (up to start of Section 2 METHOD)

### Motivation and adoption context
- Productivity/quality/workflow promise cited with Ziegler et al., 2022 and Izadi et al., 2024.
- 76% using or planning AI tools (Stack Overflow, 2024); >50% report benefits (JetBrains, 2024): reduced time searching for information, faster coding and development, quicker completion of repetitive tasks, overall productivity increase.
- HCI-to-HAX shift: traditionally HCI studied how users interact with software and tools; with AI in workflows the focus shifts to Human-AI Experience because "AI acts as an active collaborator rather than just a tool."
- Example of reliance given: "Cursor" (chunk renders as "Coursor1" with footnote "Cursor: The AI Code Editor https://www.cursor.com/").

### Relation to prior reviews and the authors' earlier survey
- General LLM-for-SE reviews (He et al., 2025; Zhou et al., 2025a; Hou et al., 2024; Durrani et al., 2024) summarize model capabilities, task coverage, and evaluation techniques but "do not analyze the interaction experience inside developer workspaces, where the software development lifecycle takes place."
- Earlier survey (Sergeyuk et al., 2024): initial exploration with 36 papers, no systematic protocol; present study extends scope and rigor with formal SLR under PRISMA (Moher et al., 2010), 90 papers via database search plus backward snowballing plus expert-informed additions.
- Beyond dataset expansion, adds analysis of study context, empirical methods, and proposed future directions; organized along Design, Impact, and Quality.

### Protocol, goals, and scope
- "Using our protocol, we identified 257 studies and thoroughly reviewed 90 that were relevant to in-IDE HAX."
- Goals verbatim: "(a) identify common themes and patterns in the literature, (b) merge the current state of knowledge regarding in-IDE HAX, and (c) identify critical gaps that can guide future research efforts."
- Scope: "how the presence of an AI assistance changes what happens in the very place where code is written, inspected, or tested, rather than how AI helps in software engineering broadly."

### Research-activity focus and gaps (as previewed in introduction)
- Focus: professional software development settings, code implementation stage of the SDLC, often with GitHub Copilot as primary example.
- Limited attention: requirements, testing, deployment; educational contexts; non-users or people who stopped using AI assistance.

### Dimension findings preview (exact counts)
| Dimension | Count | Introduction's summary |
|---|---|---|
| Impact | 74/90 | Productivity improvements, especially among experienced users; increased verification time; over-reliance concerns |
| Design | 28/90 | Autocompletion and conversational systems, some hybrid; prompt structure and interface properties (context awareness, transparency, user control) matter |
| Quality | 19/90 | Correctness, maintainability, security evaluated; calls for improved validation and diagnostic support |

### Future directions preview
- Topics: productivity factors, audit mechanisms for AI-generated code, design of AI assistance; emphasis on personalization and transparency; growing interest in long-term adoption.
- Methods: larger-scale evaluations, comparative research across user groups and contexts, longitudinal studies; underexplored: AI governance, user control, proactivity.
- Summary call: broaden contexts, add longitudinal designs, refine methods; cover underrepresented SDLC stages and diverse user groups.

### Stated contributions
- Comprehensive synthesis of 90 studies by research goals, methods, and findings, revealing themes, contexts, and trends.
- Characterization of three dimensions: (a) Impact — effects on workflows, productivity, experience; (b) Design — integration of AI assistance into IDEs; (c) Quality — security, comprehensibility, adequacy of AI-generated code.
- Identification of future opportunities from proposed future work, e.g. AI governance, user control, proactivity.

**Covers:** manuscript title/abstract (p. 1) through end of Section 1 Introduction (pp. 2–4); Section 2 METHOD begins but is not included in this chunk.
