> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Introduction: From Autocomplete to Thought Partners
**In one sentence:** Writing needs shifting personal cognitive support, but existing tools split between proactive-but-shallow autocomplete and rich-but-reactive prompt-based tools, so the paper proposes proactive thought partners that take initiative to offer customizable higher-level cognitive help during writing.

## Key points
- Writing is a dynamic cognitive process after Flower & Hayes 1981, shifting moment to moment between ideation, wording, and revision, so support needs vary by person and by moment.
- Existing proactive writing help focuses on local text production such as autocomplete and next-phrase suggestions (Bhat et al. 2023; Buschek et al. 2021; Jakesch et al. 2023; Chen et al. 2019 on pauses as intervention moments).
- Higher-level cognitive work such as ideation, reflection, and revision has largely relied on reactive interfaces where users must prompt, click buttons, or use menus (Gero et al. 2022; Reza et al. 2023; Zhang et al. 2025a).
- Figure 1 maps intelligent writing assistants on two dimensions -- initiative (reactive vs proactive) and level of support (textual vs cognitive) -- placing proactive thought partners in the proactive-plus-cognitive quadrant.
- The paper contributes 3 things: the proactive thought partners concept, a customizable technology probe after Hutchinson et al. 2003, and empirical insights plus design implications from deployment.
- The probe lets users create partners by configuring roles (what kind of cognitive support) and proactivity/timing (when to intervene), with suggestions users can dismiss, use as inspiration, or apply to the document.
- The probe was deployed with 16 participants for one week as a diary study followed by semi-structured interviews, finding prospective planning in setup, use for idea generation and self-monitoring, and preference for lightweight visuals plus non-directive framing.

---
## The cognitive nature of writing
Writing involves diverse cognitive activities, from ideation to revision. A writer may shift within minutes between developing ideas, selecting prose, and evaluating text against broader narrative goals. At one moment an example that concretizes an abstract claim helps; at another, an alternative perspective or a plan for the next section helps.

Needs also differ across writers. Some want help developing and evaluating their own ideas, others want information-seeking help such as outside-domain evidence. The paper argues an ideal assistant should therefore support this shifting and personal cognitive work by offering the right kind of help at the right moment.

## The gap: proactive-textual vs reactive-cognitive
Local text production is relatively structured and predictable: surrounding text signals likely continuations, and observable events such as pauses give natural intervention moments (Chen et al. 2019). Prior work used such signals for proactive local textual assistance, including autocomplete and next-phrase suggestions (Bhat et al. 2023; Buschek et al. 2021; Jakesch et al. 2023).

Higher-level activities such as ideation, reflection, and revision depend more on writer preferences and evolving context (Flower and Hayes 1981). Support for them has largely stayed reactive, responding only after explicit user requests through prompts, buttons, or menus (Gero et al. 2022; Reza et al. 2023; Zhang et al. 2025a). The gap is therefore: proactive support exists but stays shallow and textual, while cognitive support exists but stays reactive.

## Proactive thought partners concept + Fig 1
The paper names the missing quadrant proactive thought partners: AI agents that proactively offer customizable, higher-level cognitive support during writing without requiring explicit prompting.

Figure 1 makes this explicit with a two-dimension design space. One axis is initiative, from reactive user-invoked support to proactive system-initiated support. The other axis is level of support, from textual assistance to higher-level cognitive assistance. Proactive thought partners sit in the proactive and cognitive quadrant.

The concept is instantiated in a technology probe (Hutchinson et al. 2003) where customization is both an interaction mechanism and an inquiry instrument. Users define each partner's role (type of cognitive support needed) and timing conditions (when it should intervene). As users write, relevant partners take initiative at appropriate moments to offer suggestions.

## Contributions and study overview
The work claims 3 contributions. First, the proactive thought partners design concept for assistants that proactively provide higher-level and personal cognitive support through customizable AI partners. Second, the technology probe that lets writers create such partners by configuring roles and proactivity, enabling study of customizable proactive cognitive support in situated practice. Third, empirical insights and design implications from real use, articulating a design space around customization, timing, engagement, and representation.

For evidence, the probe was deployed with 16 participants in a one-week diary study followed by semi-structured interviews. Previewed findings: participants treated configuration as prospective planning, translating anticipated needs into roles and timing; during writing they often ignored interventions to preserve flow, while engaged suggestions supported idea generation and self-monitoring; lightweight visual representations and non-directive rhetorical framing made proactive support feel less intrusive.

**Covers:** Abstract, Section 1 (Introduction), Figure 1 design space
