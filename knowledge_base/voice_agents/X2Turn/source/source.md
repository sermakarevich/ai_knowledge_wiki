# [2608.10878] X2-Turn: Frame-Synchronous Dual-Head Modeling for Joint Streaming ASR and Turn State Prediction
PDF: https://doi.org/10.48550/arxiv.2608.10878
Source: https://doi.org/10.48550/arxiv.2608.10878
Kind: article
Fetched: 2026-09-22T09:31:37.416425+00:00
Tool: urllib

[2608.10878] X2-Turn: Frame-Synchronous Dual-Head Modeling for Joint Streaming ASR and Turn State Prediction

Skip to main content

Search arXiv

      Press Enter to search · Advanced search

# Computer Science > Computation and Language

arXiv:2608.10878 (cs)

  [Submitted on 11 Aug 2026 (v1), last revised 8 Sep 2026 (this version, v3)]

# Title:X2-Turn: Frame-Synchronous Dual-Head Modeling for Joint Streaming ASR and Turn State Prediction

Authors:Kaiqi Fu, Rime Wen, Altman Lin, Shawn Qin, Roy Gan, Hao Wang, Qian Wang

View a PDF of the paper titled X2-Turn: Frame-Synchronous Dual-Head Modeling for Joint Streaming ASR and Turn State Prediction, by Kaiqi Fu and 6 other authors

View PDFHTML (experimental)

Abstract:Accurate and responsive turn-taking is essential for spoken dialogue systems, which must distinguish in real time between user interruptions, backchannels that should be ignored, and the completion of an utterance. Prior modular approaches typically optimize turn state prediction at the utterance or fixed-chunk level, creating a mismatch with the continuous turn state estimate, and often depend on an auxiliary ASR model, which limits responsiveness and increases overall system complexity. Therefore, we present X2-Turn, a frame-synchronous turn state prediction method via delayed-stream modeling. Specifically, building on the pretrained Voxtral Realtime model, we introduce a frame-synchronous turn state head that operates in parallel with the ASR head on shared streaming representations, jointly predicting ASR tokens and fine-grained turn states at the frame level. Experiments on bilingual EasyTurn and Full-Duplex-Bench demonstrate that the proposed method achieves an effective trade-off between turn state accuracy and decision latency.

Subjects:Computation and Language (cs.CL); Audio and Speech Processing (eess.AS)

Cite as:arXiv:2608.10878 [cs.CL]

(or arXiv:2608.10878v3 [cs.CL] for this version)

https://doi.org/10.48550/arXiv.2608.10878

Focus to learn more

                  arXiv-issued DOI via DataCite

## Submission history

 From: Kaiqi Fu [view email]

[v1]
        Tue, 11 Aug 2026 12:54:52 UTC (1,280 KB)

[v2]
        Wed, 19 Aug 2026 03:16:50 UTC (943 KB)

[v3]
        Tue, 8 Sep 2026 12:28:34 UTC (923 KB)

Full-text links:

## Access Paper:

View a PDF of the paper titled X2-Turn: Frame-Synchronous Dual-Head Modeling for Joint Streaming ASR and Turn State Prediction, by Kaiqi Fu and 6 other authors

View PDF

HTML (experimental)

TeX Source

view license

### Current browse context:

cs.CL

< prev  |  next >

new | recent | 2026-08

    Change to browse by:

cs

eess

eess.AS

### References & Citations

NASA ADS

Google Scholar

Semantic Scholar

export BibTeX citationLoading...

## BibTeX formatted citation

×

loading...

Data provided by:

### Bookmark

Bibliographic Tools

# Bibliographic and Citation Tools

Bibliographic Explorer Toggle

Bibliographic Explorer(What is the Explorer?)

Connected Papers Toggle

Connected Papers(What is Connected Papers?)

Litmaps Toggle

Litmaps(What is Litmaps?)

scite.ai Toggle

scite Smart Citations(What are Smart Citations?)

Code, Data, Media

# Code, Data and Media Associated with this Article

alphaXiv Toggle

alphaXiv(What is alphaXiv?)

Links to Code Toggle

CatalyzeX Code Finder for Papers(What is CatalyzeX?)

DagsHub Toggle

DagsHub(What is DagsHub?)

GotitPub Toggle

Gotit.pub(What is GotitPub?)

Huggingface Toggle

Hugging Face(What is Huggingface?)

ScienceCast Toggle

ScienceCast(What is ScienceCast?)

Demos

# Demos

Replicate Toggle

Replicate(What is Replicate?)

Spaces Toggle

Hugging Face Spaces(What is Spaces?)

Spaces Toggle

TXYZ.AI(What is TXYZ.AI?)

Related Papers

# Recommenders and Search Tools

Link to Influence Flower

Influence Flower(What are Influence Flowers?)

Core recommender toggle

CORE Recommender(What is CORE?)

Author

Venue

Institution

Topic

        About arXivLabs

# arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? Learn more about arXivLabs.

Which authors of this paper are endorsers? |
    Disable MathJax (What is MathJax?)
