# PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing

**Paper:** [PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing (Song et al., 2025)](https://arxiv.org/abs/2604.05018)

## Human Readable TL;DR

Imagine you've done a bunch of science experiments and scribbled down your notes, but now you need to write the actual paper -- the polished, formatted document with proper references, charts, and all the academic bells and whistles. PaperOrchestra is like having a team of specialized AI assistants: one organizes your outline, another hunts down and cites relevant past research, another draws your charts, and a final one proofreads everything like a tough journal reviewer. The result is a near-publication-ready paper generated from your messy notes. In tests, its literature reviews were so thorough that human experts rated them competitive with human-written ones 43% of the time.

## TL;DR

PaperOrchestra is a multi-agent LLM framework from Google that transforms unstructured pre-writing materials (idea summaries, experimental logs) into submission-ready LaTeX manuscripts. It introduces specialized agents for outline generation, literature review with hybrid search, plot generation, section writing, and iterative peer-review-based refinement. Evaluated on PaperWritingBench (200 CVPR/ICLR 2025 papers), it achieves 84% simulated acceptance at CVPR and 81% at ICLR, with 88--99% win margins over baselines in literature review quality.

---

## Problem & Motivation

Existing AI research automation systems (AI Scientist, Cycle Researcher, OmniScientist) tightly couple their writing modules to internal experimental pipelines, making them unable to process arbitrary human-provided pre-writing materials as a standalone tool. These systems also produce superficial literature reviews with few citations (~9--14 vs. ~59 in human papers) and cannot generate conceptual diagrams. There is no standardized benchmark for evaluating automated AI paper writing in isolation. PaperOrchestra addresses all three gaps: standalone flexibility, deep literature synthesis, and a new benchmark.

---

## Main Original Ideas

1. **Multi-Agent Writing Pipeline** -- Five specialized agents (Outline, Plotting, Literature Review, Section Writing, Content Refinement) work in a coordinated pipeline, with plotting and literature review running in parallel. This decoupled design allows the system to accept arbitrary unstructured inputs rather than requiring outputs from a specific experimental loop.

2. **Hybrid Literature Discovery** -- The Literature Review Agent combines LLM-powered web search with Semantic Scholar API validation to authenticate papers, fetch metadata, enforce temporal cutoffs, and deduplicate. This produces ~46--48 citations per paper (vs. 9--14 from baselines), approaching human levels (~59).

3. **PaperBanana Visual Generation** -- A closed-loop plotting system where a VLM critic iteratively evaluates and revises generated images and captions, enabling both statistical plots and conceptual diagrams -- a capability absent from prior systems.

4. **Iterative Peer-Review Refinement** -- A Content Refinement Agent uses AgentReview to simulate peer review feedback, accepting revisions only when scores improve. This loop yielded +19--22% absolute gains in simulated acceptance rates.

5. **PaperWritingBench** -- The first standardized benchmark for AI paper writing, containing reverse-engineered pre-writing materials from 200 top-tier papers (100 CVPR 2025, 100 ICLR 2025), with sparse and dense idea variants to control input richness.

---

## Key Findings

| Metric | PaperOrchestra | AI Scientist-v2 | Single Agent | Human GT |
|--------|---------------|-----------------|--------------|----------|
| **CVPR Acceptance Rate** | **84%** | 71% | 62% | 86% |
| **ICLR Acceptance Rate** | **81%** | 72% | 63% | 94% |
| **Avg. Citations** | **45.7--48.0** | 9--14 | 9--14 | ~59 |
| **Lit Review Win vs. Baselines** | **88--99%** | -- | -- | upper bound |
| **Overall Quality Win vs. AI Sci-v2** | **39--86%** | -- | -- | -- |

- Human evaluators (11 AI researchers, 40 papers) confirmed automated metrics: PaperOrchestra won 50--68% on literature review quality and 14--38% on overall quality vs. AI baselines
- Against human ground truth, PaperOrchestra achieved 43% tie/win rate for literature synthesis
- Dense idea inputs improved overall paper quality (43--56% win rates) but literature review quality was robust regardless of input density
- The Content Refinement Agent was critical: 79--81% win rates over unrefined drafts, 0% losses
- Autonomous plot generation (PlotOn) achieved 51--66% tie/win rates against human-curated figures

---

## Suggestions & Future Directions

1. **Richer Input Modalities** -- Incorporate experimental code, raw data files, and other research artifacts beyond text summaries and logs to produce more grounded manuscripts.

2. **Interactive Writing Environments** -- Transition from fully autonomous generation to dynamic, interactive human-AI writing sessions that enable iterative collaboration rather than one-shot generation.

3. **Hallucination Safeguards** -- Despite the Semantic Scholar validation step, the authors emphasize that human researchers must retain full accountability for factual accuracy and originality; stronger verification pipelines are needed.

4. **Cross-Domain Generalization** -- The current benchmark and evaluation focus on AI/ML papers; extending to other scientific domains remains an open challenge.

5. **Ethical Positioning** -- The system is explicitly framed as an assistive tool, not a replacement for human authorship, with open questions about responsible deployment in academic publishing.

---

## Authors & Institutions

Yiwen Song (Google), Yale Song (Google), Tomas Pfister (Google), Jinsung Yoon (Google)
