# EvoOntology: A Self-Evolving Ontology Layer for Data Agents
Source: https://arxiv.org/pdf/2609.15779
Kind: pdf
Fetched: 2026-09-22T06:44:08.989384+00:00
Tool: pdftotext

                                                           EvoOntology: A Self-Evolving Ontology Layer for Data Agents

                                                                        Meiduo Chong1 , Shaolei Zhang1∗ , Ju Fan1 , Xiaoyong Du1
                                                                                           1
                                                                                             Renmin University of China
                                                                               zhongmeiduo210@ruc.edu.cn, zhangshaolei98@ruc.edu.cn




                                                                      Abstract                                           Heterogeneous Data Sources
                                                                                                                          CS
                                                                                                                                                                                          Heterogeneous Data Sources
                                                                                                                                                                                            CS




arXiv:2609.15779v1 [cs.AI] 14 Sep 2026
                                                                                                                          V                                                                 V
                                                                                                                Tables   CSV      Docs   Databases Charts   Logs              Tables       CSV              Docs       Databases Charts                    Logs
                                           Data agents aim to fulfill natural-language instructions over                                                                                                             Ontology Layer
                                           heterogeneous data, including tables, files, and databases.                                                                                 Node types
                                                                                                                                                                                        Terms
                                                                                                                                                                                                                                                              Self-Evolving
                                           However, data agents face a challenging agent–data gap: het-                                                                                 Mappings
                                                                                                                                                                                        Evidence
                                                                                                                                                                                        Constraints

                                           erogeneous data resides outside the agent, while the agent                                                                  Data
                                                                                                                                                                    interaction        Edge types
                                                                                                                                                                                        Semantic Relation
                                                                                                                                                                                        Structural References

                                           can access it (e.g., column names and file paths) only through                                                                                                                         Attribute
                                           generic tools. Existing approaches either let agents directly ex-                                                                                                    Diagnose
                                                                                                                                                                                                      Diagnose(Evaluate)
                                                                                                                                                                                                      (Trajectory)
                                                                                                                                                                                                                               (Content · Tool · Schema)

                                                                                                                                                                                                                                                                      Patch
                                                                                                                                                                                                                                                                   Refine
                                                                                                                                                                                                                                                                   (Candidate Update)

                                           plore raw data sources or inject manually constructed semantic                Data Agent                                               Ontology
                                                                                                                                                                                  interaction
                                                                                                                                                                                                                 Update
                                                                                                                                                                                                                 (Evolve)
                                                                                                                                                                                                                                 Evaluate
                                                                                                                                                                                                                            (Parent vs. Candidate)
                                                                                                                                                                                                                                                                  (Improve)




                                           layers into prompts. However, neither scales well to large het-                     Blind Data Exploration with High                                            Grounded Data Understanding
                                                                                                                               Semantic Uncertainty                 Data Agent                             with Self-Evolving Semantics
                                           erogeneous data sources nor adapts to different agent behav-
                                           iors. In this paper, we introduce EvoOntology, a self-evolving       (a) Data Agent w/o Ontology Layer                  (b) Data Agent with Self-Evolving Ontology Layer
                                           ontology layer for data agents. EvoOntology encapsulates the
                                           ontology as an MCP server comprising a schema layer, a con-         Figure 1: A self-evolving ontology layer helps data agents
                                           tent layer, and a tool layer, enabling agents to actively query     understand heterogeneous data.
                                           and interact with the ontology at runtime. To this end, we
                                           introduce a builder agent for autonomous ontology construc-
                                           tion and a self-evolution loop that continuously refines the        the agent can access the data only through generic tools such
                                           ontology through attribution-guided typed edits that are ac-
                                           cepted only after a backbone-conditional paired evaluation.
                                                                                                               as SQL interfaces and file readers. A fundamental challenge
                                           Experiments on three well-adopted data-agent benchmarks             is that neither the structure nor the content of these heteroge-
                                           with four LLM backbones demonstrate that EvoOntology con-           neous data sources is known a priori. As a result, the agent has
                                           sistently outperforms strong baselines and existing semantic-       to blindly explore the underlying data by repeatedly issuing
                                           layer approaches, effectively bridging the agent–data gap and       probing queries, guessing where the requested concepts are
                                           enabling more effective interaction with heterogeneous data.        located, and inspecting potentially irrelevant content. This
                                                                                                               mismatch creates a persistent agent–data gap. Bridging this
                                           Code — https://github.com/ruc-datalab/EvoOntology                   gap requires an intermediate ontology layer that explicitly
                                                                                                               represents domain concepts, grounds the concepts in the un-
                                                                  Introduction                                 derlying data, and enables agents to interact with data at the
                                         Data agents over heterogeneous data (Liu et al. 2026; Sahu            semantic level rather than the physical level.
                                         et al. 2025; Li et al. 2023; Hong et al. 2025; Zhang et al.              Existing approaches to agent–data interaction can be
                                         2023a) aim to solve natural-language tasks over both struc-           broadly divided into raw querying and semantic-layer-based
                                         tured data (e.g., tables and databases) and unstructured data         interaction. Raw-querying methods (Pourreza and Rafiei
                                         (e.g., documents and files). To accomplish such tasks, an             2023; Wang et al. 2025; Talaei et al. 2024) allow agents
                                         agent must continuously interact with heterogeneous data              to directly inspect schemas and issue exploratory queries
                                         sources to gather the information required for producing the          over the underlying data. While effective for small and rel-
                                         final answer. Recent advances in tool use for large language          atively simple data sources, they scale poorly to wide and
                                         models (LLMs) (Yao et al. 2022; Schick et al. 2023; Qin               heterogeneous data, where agents can easily become trapped
                                         et al. 2023; Patil et al. 2024) have enabled agents to directly       in repetitive and inefficient exploration. Semantic-layer ap-
                                         access and manipulate external data sources, providing the            proaches (Hitzler 2021; dbt Labs 2023; Feng et al. 2024;
                                         foundation for such data interactions.                                Chang and Fosler-Lussier 2023), in contrast, provide meta-
                                            However, direct interaction with heterogeneous data raises         data, including schemas, entities, metrics, and other domain
                                         a fundamental question: Can a data agent effectively under-           semantics, to guide the agent. However, incorporating the
                                         stand heterogeneous data? In real-world deployments, data             entire semantic layer into the agent context is impractical for
                                         resides outside the agent in the form of relational databases,        large data sources due to context-length limitations. More-
                                         semi-structured filings, and unstructured documents, while            over, existing semantic layers are typically predefined and
                                            ∗
                                                Corresponding author: Shaolei Zhang.
                                                                                                               maintained manually, making them costly to construct and
difficult to adapt to new data sources, tasks, and agents. These    supat and Liang 2015), and code-executing analysts that
limitations highlight the need for an effective and scalable        answer business-intelligence questions on CSV files (Sahu
ontology intermediate layer to bridge the agent–data gap.           et al. 2025; Guo et al. 2024). Pipeline-style variants orga-
    In this paper, we advance the intermediate layer between        nize these tool calls through decomposition, retrieval, and
agents and data from static semantic descriptions to an inter-      verification (Pourreza and Rafiei 2023; Wang et al. 2025;
active ontology layer that agents can flexibly access through       Talaei et al. 2024; Cao et al. 2024; Caferoğlu and Ulusoy
tools. Autonomously constructing such an ontology is in-            2024; Li et al. 2024b), improving standardized benchmarks
herently challenging because both data sources and agent            while leaving the underlying representation gap untouched.
behaviors are diverse and dynamic, requiring the ontology           This gap is amplified in heterogeneous settings, where a task
to adapt to both. To address this challenge, we introduce           may span databases, spreadsheets, and files with different
EvoOntology, a self-evolving ontology layer that continu-           naming conventions, schemas, and granularities. Ground-
ously adapts to the underlying data and the agents that use         ing discovered in one trajectory is typically discarded rather
it. As illustrated in Figure 1, the ontology consists of three      than retained for later tasks. EvoOntology instead amortizes
components: a schema layer, which defines object types and          schema discovery across the workload through an ontology
reference rules; a content layer, which stores domain knowl-        layer that preserves such grounding and evolves from agent
edge and data mappings; and a tool layer, which exposes             failures.
executable interfaces for agents to access and manipulate the          Semantic Layers. Ontology and semantic layers have
ontology. These components are encapsulated as a Model              long connected domain concepts with relational data, rang-
Context Protocol (MCP) server, enabling agents to actively          ing from OWL ontologies and metric layers (Hitzler 2021;
query and interact with the ontology rather than passively          dbt Labs 2023) to LLM-oriented semantic representations
consuming it as contextual metadata.                                and prompt-time metadata (Feng et al. 2024; Chang and
    Specifically, EvoOntology first employs a builder agent to      Fosler-Lussier 2023). Related work also uses LLMs to in-
construct an initial ontology by issuing probe queries over the     duce schema or metric descriptions (Zhang et al. 2023b; Nan
underlying data sources and grounding each ontology entry           et al. 2023) and feedback to refine prompts or retrievers (Zhou
in the observed data. EvoOntology then continuously refines         et al. 2022; Khattab et al. 2023; Asai et al. 2024). However,
the ontology based on agent interaction trajectories. Specifi-      existing layers are typically maintained as static prompt-
cally, it performs attribution analysis to identify deficiencies    time metadata. Whether manually authored or automatically
in the current ontology, proposes targeted refinements to its       induced, they are usually detached from downstream tra-
schema, content, or tools, and accepts each refinement only         jectories showing how agents use them. Full-context injec-
after it passes a paired evaluation on a held-out validation set.   tion scales poorly to large data sources, while coarse up-
Through this iterative self-evolution process, the ontology         dates provide little basis for identifying which semantic en-
continuously adapts to both heterogeneous data and agent            try affected a downstream decision. This makes targeted,
behaviors, progressively bridging the agent–data gap.               workload-driven maintenance difficult as tasks and agent be-
    In summary, our main contributions are as follows:              havior evolve. EvoOntology instead exposes the ontology
 • Interactive Ontology Layer. We propose the first au-             through an MCP server for selective runtime access and re-
    tonomous interactive ontology layer for data agents and         fines individual entries through typed, evidence-grounded
    encapsulate it as an MCP server, enabling agents to query       edits admitted by paired validation.
    and interact with heterogeneous data through tools.
 • Self-Evolving Ontology. We introduce a builder agent                                       Method
    for autonomous ontology construction and a self-evolving        To reduce manual semantic-layer authoring while adapt-
    framework that refines the ontology through attribution         ing the layer to agent behavior, we propose EvoOntology,
    analysis, targeted refinement, and paired evaluation.           an agent-first builder-and-evolver framework. EvoOntology
 • Strong Performance. Extensive experiments on three               maintains a versioned ontology state comprising content,
    well-adopted data-agent benchmarks with four LLM back-          schema, and tool layers. A builder agent constructs an
    bones demonstrate that EvoOntology consistently and             evidence-grounded initial state from the training workload
    substantially outperforms strong baselines and existing         and raw sources, while an evolution agent refines it from
    semantic-layer approaches.                                      historical trajectories. The design is agent-first in that the
                                                                    ontology is built around the workload, accessed through the
                                                                    agent’s tool interface, and adapted from its execution history.
                      Related Work
Data Agents on Heterogeneous Data. Deploying LLMs                   Agent-First Ontology-Layer Architecture
as data agents is an important step toward automated analyt-        EvoOntology represents the ontology state at evolution round
ics. Existing approaches fall into two families: raw querying       t as Lt = (St , Γt , Rt ), comprising a Content Layer St , a
and semantic-layer-based interaction. Raw-querying agents           Schema Layer Γt , and a Tool Layer Rt . The three compo-
equip LLMs with schema-reading, query-executing, and file-          nents separate semantic knowledge, its object model, and its
inspecting tools, exemplified by text-to-SQL agents that gen-       runtime exposure. This separation allows the deployed agent
erate queries over relational databases (Li et al. 2023; Yu         to retrieve only the semantics relevant to the current step and
et al. 2018; Li et al. 2024a), table-QA agents that reason          allows the evolution agent to update a bounded part of the
over spreadsheets and web tables (Chen et al. 2020; Pa-             ontology state.
             User Query                                     RESULT                                           Extract Candidate Concepts from Workload Queries                                                                                                Diagnose and Attribute Failures from History Trajectory
                                                                                          Builder
                                                    • Cost rose 12% last month.           Agent
             Why did cost rise                                                                                          Why did cost rise last month?                                    Cost            Time
                                                    • Top drivers: Inflation (+7pp), FX                                                                                                                                                                       History Trajectory                                                                                            Attribute
             last month?
                                                     (+3pp), Volume (+2pp).                                             What drove profit change over                                  Revenue           Cost            Profit         Time         Q1 Why did cost rise last month?                                    Evolution Agent                                    Content Level
                                                                                                                        time?                                                                                                                                                                                                                                          Missing term “Channel”
                                                                                                                                                                                                                                                     Q2 What drove margin decline?
                                                                                                                        How did revenue change month                                   Revenue           Time                                                                                                                                                                Tools Level
                                                                                                                        by month?                                                                                                                           Cost by channel last quarter                                                                                        Add tool
                                                                                                                                                                                                                                                     Q3
                                                                                                                                                                                                                                                            Missing mapping for channel                                                                                       “FX Convert”

                                                                                                                                                                                                                                                            Cost in constant currency                                        Analyse                                        Schema Level
                                                                                                                                                                                                                                                    Q4                                                                                                                      No schema-level issue
                                       Data Agent                                         Builder             Ground Candidate Concepts in Heterogeneous Data                                                                                               Constraint conflict (currency)
                                                                                          Agent                                                                                                                                                                                                                                                                                  identified

       Data Execution Tools                                                                                            Tables              CSV                  Docs         Databases                    Charts                  Logs
                                                           Ontology Interaction Tools
                                                                                                                                           C
                                                                                                                                           S
                        ...                                                                                                                V                                                                                                                                                 Patch the Parent Ontology
                                                                                                                                                                                                                                                               Ontology v1                                                                 Candidate Ontology
   Execute   Execute                                           browse     resolve         Cost Table                                                                          Metric Definition                                 Revenue
    SQL      Python                                                                                                                                                                                                                                                Tool Layer                                                                        Tool Layer
                                                                                                               month_id cost_type cost_amount                                     Cost:                                         Records
                                                                                           fact_cost                                                                              Sum of cost amounts
                                                                                           month_id             Jan-24    Labor     1,234,567
                                                                                           cost_type            Jan-24   Freight     234,987
                                                                                                                                                                                  Revenue:                                            ...
                                                                                                                                                                                  Net revenue from completed orders                                                                                                                                                                          Tool 3:
                                                                                           cost_amount          Feb-24    Labor     1,310,000                                     Profit:                                             ...               Tool 1:                                  Tool 2:                          Tool 1:                       Tool 2:
                                                                                                                                                                                                                                                                                                                                                                                               FX
                                                                                           currency                                                                               Revenue    Operating Cost                                             browse                                   resolve                          browse                        resolve
                                                                                                                  …         …          …                                                                                                                                                                                                                                                     Convert
      Data Interaction                         Ontology interaction                                                                                                               …



                                                                                                                                                                                                                                               Schema                                                                         Schema
                                      Ontology layer                                                                                                                                                                                           Layer
                                                                                                                                                                                                                                                                             Content Layer
                                                                                                                                                                                                                                                                                                                              Layer
                                                                                                                                                                                                                                                                                                                                                          Content Layer
                                                                                                          Construct and Expose the Grounded Ontology Layer                                                                                                                       Profit                                                                            Profit
                        Node types                                                                                                                     Tool Layer                                                                               Term                                                                            Term
                        Terms                                                                                                                                                                                                                                 Cost               Revenue             Time                                     Cost               Revenue              Time         Channel

                                                                                                                                                                      Tool 2: resolve
                        Mappings                                                                         Tool 1: browse
                                                                                                                                                                      • Retrieve complete semantics                                                         fact_.cost           fact_rev           dim_date
                                                                                                         • Find relevant terms                                                                                                                  Mapping                                                                        Mapping      fact_.cost        fact_rev          dim_date       dim_channel
                        Evidence
                                                                                                                                                                                                                                                            total_cost         net_revenue            date
                                                                                                                                                                      • Terms IDs → Mappings, Relations, Constraints, and                                                                                                                   total_cost        net_revenue         date         channel_name
                                                                                                         • Query → Ranked Terms
                                                                                                                                                                        Evidence
                        Constraints                                                                                                                                                                                                                                            GAAP revenue
                                                                                                                                                                                                                                                Evidence      Cost catalog                                                     Evidence       Cost        GAAP revenue          Date table     Currency basis
                                                                                           Schema Layer                                                          Content Layer                                                                                                 definition
                                                                                                                                                                                                                                                                                                     Date table sample
                                                                                                                                                                                                                                                                                                                                              catalog     definition            sample         = Constant USD
                       Edge types
                                                                                                                                                   derivation                                                                                                Profit =         Revenue excludes       Time grain =                            Profit =              Revenue excludes          Time grain =
                       Semantic Relation                                                                                  Constraint by                                  Profit                                                                Constraint    Revenue - cost   cancelled orders         Month                  Constraint     Revenue - cost        cancelled orders            Month

                       Structural References                                                     Term                                                           derivation
                                                                                                 (Semantic Concept)                                                                    association
                                                                                                                                            Cost                       Revenue                          Time                          ...                       Candidate
                                                                                                                                                        association
                                                                                                                                                                                                                                                                Ontology
                                                                                                                                                                                                                                                                                   Evaluate and Gate the Candidate
                                                                                                    Mapping                                                                                                                                                                                                                              Accept
                                                                                                 (Exact Fields)                           fact_.cost                    fact_rev                     dim_date         Constraint by   ...                                                                                           (Candidate Ontology
                                                                                                                                                                      net_revenue                                                                                                                                                    → Ontology v2.0)
                        Heterogeneous Data Sources                                                                                        total_cost                                                   date

                                                                                                Evidence
                 CS                                                                             (Data Observations)                   Cost catalog                    GAAP revenue                   Date table sample                ...
                                                                                                                                                                      definition                     (10K rows)
                 V                                                                                  Constraint                                                                                                                                                                                    Evaluate
                                                                                                                                                                                                                                                                                                                                           Reject
                                                                                                                                                                                                                                                                                                                                 (Roll back to Ontology v1.0)
                                                                                                                                                                                                                                                                                                                                                                            New Evolution Loop
                                                                                                                               Profit = Revenue - cost                Revenue excludes           Tim e grain = M onth                 ...        Data Agent                                  (parent vs. candidate)
   Tables         CSV         Docs      Databases      Charts           Logs                        (Business Rules)                                                  cancelled orders




Figure 2: Overview of EvoOntology. It comprises a typed content graph, its object schema, and a runtime tool interface. The
builder constructs an evidence-grounded initial state, while the evolution agent refines it from historical interaction trajectories.


   Content Layer. The Content Layer St is a typed se-                                                                                                                                    mantics relevant to the agent, while executable probes verify
mantic graph with four node families and two edge families.                                                                                                                              their grounding in the underlying data.
The node families comprise Terms, Mappings, Constraints,                                                                                                                                    Workload-Guided Probing. Given a training work-
and Evidence. Terms represent domain concepts, Mappings                                                                                                                                  load W and raw sources D, the builder proposes C =
ground them to fields and linking paths, Constraints govern                                                                                                                              propose(W) from recurrent entities, metrics, operations, and
their valid use, and Evidence supports their semantic claims.                                                                                                                            analytical conditions. For each candidate c ∈ C, it issues
The edge families comprise Semantic Relations and Struc-                                                                                                                                 probe(c, D) to identify candidate fields and linking paths
tural References. Semantic Relations connect Terms through                                                                                                                               and to inspect their types, values, and semantic consistency.
association, hierarchy, composition, equivalence, or deriva-                                                                                                                                Evidence-Grounded Commitment. Only candidates
tion. Structural References link Terms to Mappings and at-                                                                                                                               supported by their probe results are committed to the ini-
tach Constraints and Evidence to the objects they govern                                                                                                                                 tial Content Layer:
or support. Figure 2 illustrates these components through a
financial-analysis example.                                                                                                                                                                                                     C + = {c ∈ C | verify(probe(c, D)) = 1} ,
                                                                                                                                                                                                                                                                                                                                                                                                            (1)
   Schema Layer. The Schema Layer Γt defines the fields                                                                                                                                                                         S0 = construct C + , D; Γ0 .
                                                                                                                                                                                                                                                           
of the four node families, the admissible Semantic Relation
types, and the permitted reference patterns. Schema updates                                                                                                                              Here, verify(·) checks the declared type, filter, and value-
can therefore extend the ontology’s representational capacity                                                                                                                            distribution requirements. Verified candidates are instanti-
without changing its instantiated content.                                                                                                                                               ated under Γ0 , with their supporting records retained as Ev-
   Tool Layer. The Tool Layer Rt exposes the ontology                                                                                                                                    idence. Together with the default Tool Layer R0 , they form
through two MCP tools and a session manifest. The func-                                                                                                                                  the initial state L0 = (S0 , Γ0 , R0 ).
tion fbrowse (q, k, n) retrieves the top-n semantic matches for
query q and kind k, while fresolve (I, c) returns the requested                                                                                                                          Trajectory-Grounded Ontology Evolution
records and their linked objects. The manifest provides com-
                                                                                                                                                                                         Data grounding alone does not ensure that an ontology suits
pact source and usage information at session initialization.
                                                                                                                                                                                         a particular agent. EvoOntology therefore uses historical tra-
It is the only ontology content placed in the prompt, while
                                                                                                                                                                                         jectories as behavioral evidence. Successful executions re-
detailed records are retrieved on demand.
                                                                                                                                                                                         veal effective semantic structures and access patterns, while
                                                                                                                                                                                         unsuccessful ones expose missing, misleading, or poorly ex-
Evidence-Grounded Ontology Initialization                                                                                                                                                posed components.
Manually defining domain concepts, field mappings, linking                                                                                                                                  Trajectory Attribution. Given historical trajectories Tt
paths, and semantic constraints for each data source requires                                                                                                                            and the current state Lt , the evolution agent extracts recur-
substantial expert effort. The builder agent constructs an ini-                                                                                                                          rent signatures Σt = analyze(Tt , Lt ). Each signature sum-
tial ontology from the training workload and raw sources                                                                                                                                 marizes an interaction pattern, the ontology objects involved,
without observing gold answers. The workload identifies se-                                                                                                                              and its observed outcomes. The agent assigns the signature
to Content, Tool, or Schema through α : Σt → {C, T, S}             evaluation protocol (Li et al. 2023; Sahu et al. 2025; Liu
and states the expected behavioral effect of an update.            et al. 2026).
   Localized Intervention. For an attributed signature σ,             Baselines. We compare EvoOntology against two base-
the agent proposes L′t = patch(Lt , σ, α(σ)). Each candidate       lines under the same ReAct scaffold and backbone. Baseline
modifies one level only. Content interventions add, remove,        runs ReAct without any ontology layer, so the agent must re-
or revise instantiated semantic objects in St . Tool interven-     discover the schema and the domain vocabulary at every task.
tions modify existing tools or add and remove tools in Rt          Baseline + SL prepends the builder-agent’s semantic layer
according to observed agent behavior. Schema interventions         into the agent’s context as a static prompt fragment (Cao
revise the object model in Γt . Multiple dependent Content         et al. 2024; Caferoğlu and Ulusoy 2024; Li et al. 2024b;
objects may be updated together when they implement the            Chang and Fosler-Lussier 2023).
same hypothesis.                                                      Reciprocal Two-Fold Evaluation. We treat ontology
   Backbone-Conditional Paired Validation. For back-               construction and evolution as training-time workload adap-
bone m, let ϕ(L, V; m) denote the score of ontology state L        tation, following held-out optimization protocols in prompt
on validation set V. The candidate and its parent are evaluated    and agent adaptation (Zhou et al. 2022; Yang et al. 2024;
on the same V with identical decoding and interaction bud-         Xu, Wen, and Li 2026). Each benchmark is divided into two
gets. The candidate is retained only when its improvement          disjoint folds, A and B. In the A → B run, 70% of A is used
reaches margin τ :                                                 for ontology construction, trajectory analysis, and candidate
              ′                                                   generation, and the remaining 30% for paired validation. The
               Lt , ϕ(L′t , V; m) − ϕ(Lt , V; m) ≥ τ,              selected ontology is frozen before testing on B. We then re-
    Lt+1 =                                                  (2)
               Lt , otherwise.                                     verse the folds and report

The single-level difference isolates the attributed hypothesis                            ScoreA→B + ScoreB→A
                                                                               Score =                               .
while limiting regressions on the validation set. Rejected can-                                       2
didates are not deployed, and their signatures, interventions,     This reciprocal design follows two-fold split-and-swap eval-
and evaluation outcomes are logged to avoid repeated inef-         uation (Dietterich 1998; Wang et al. 2026). All methods use
fective updates. All backbones evolve independently from           the same fold assignment and deployment configuration. The
the same initial state L0 , allowing accepted updates to reflect   same adaptation fold is used for ontology construction and
backbone-specific interaction patterns.                            updating across all relevant conditions. The held-out fold is
                                                                   accessed only for final evaluation after the ontology has been
                       Experiments                                 frozen, and its answers and evaluator feedback are never used
Benchmarks                                                         for ontology construction, evolution, or candidate selection.
We evaluate EvoOntology on three data-agent benchmarks             Main Results
with heterogeneous modalities and answer formats. All eval-        Capability on Multi-Source Data Research. Table 1
uations follow each benchmark’s official evaluation protocol.      reports DDR-Bench results across six LLM backbones.
  Deep Data Research (DDR-Bench) (Liu et al. 2026)                 EvoOntology improves Trajectory-Wise accuracy on all six
evaluates open-ended data research across heterogeneous            backbones, with an average gain of +17.8 points over Base-
sources. We evaluate on the 10-K scenario, and re-                 line. The improvement ranges from +4.8 on Qwen3.5-Flash
port Message-Wise accuracy on per-turn interpretation,             to +26.7 on GPT-5.5, indicating that the ontology remains
Trajectory-Wise accuracy on full-history synthesis.                effective across backbones with substantially different base-
  InsightBench (Sahu et al. 2025) is a business-analytics          line capabilities. In contrast, Baseline + SL, which injects the
benchmark of business-intelligence flags, each paired with a       semantic layer into the context as a static prompt, does not
CSV dataset and a ground-truth insight that an analyst should      consistently improve over the un-mediated agent and even
surface. We report the Insight and Summary scores.                 drops by −15.0 points on Claude-Sonnet-5. The gap be-
  BIRD (Li et al. 2023) is a text-to-SQL benchmark on              tween Baseline + SL and EvoOntology stems from how the
natural-language questions across real-world databases, eval-      layer is used: a static prompt fragment competes with the
uated under the official Oracle Knowledge setting. Follow-up       agent’s other instructions and cannot be pruned per turn,
benchmarks such as Spider (Yu et al. 2018; Lei et al. 2025)        whereas EvoOntology exposes the same content through
extend the setting to multi-schema and enterprise workflows.       MCP tools that the agent actively queries, retrieving only
The primary metric is Execution Accuracy EX and the sec-           the terms and mappings relevant to the current step. We ad-
ondary is Valid Efficiency Score VES.                              ditionally compare against ReAct + Memory (Shinn et al.
                                                                   2023; Wang et al. 2023; Madaan et al. 2023), which stores
Experimental Setup                                                 past trajectories as retrievable episodes. As shown in Table 2,
Backbones. We evaluate EvoOntology on six LLM back-                memory-based persistence lifts Trajectory-Wise from 69.5 to
bones: GPT-5.5, GPT-5.6-sol, Claude-Sonnet-5, Claude-              75.8 but remains 13.7 points below EvoOntology, because
Opus-4.8, DeepSeek-V4-Flash, and Qwen3.5-Flash. For each           episodic memory only replays what has been done and does
backbone, all conditions use the same ReAct (Yao et al. 2022)      not expose typed, composable structure.
scaffold, raw-data tools, decoding configuration, and inter-          Capability on Insight Mining. Table 3 reports Insight-
action budget. Scoring follows each benchmark’s standard           Bench results across six backbones. EvoOntology improves
                                     Msg-Wise      Traj-Wise       Overall                Method                 Traj-Wise (%, ↑)            ∆
 Method          Backbone
                                      (%, ↑)        (%, ↑)         (%, ↑)
                                                                                          Baseline (ReAct)              69.5                –
                 Claude-Sonnet-4.5     77.6          60.6           69.1                  ReAct + Memory                75.8              +6.3
                 DeepSeek-V3.2         60.1          38.2           49.2                  EvoOntology                   89.5              +20.0
                 GLM-4.6               60.3          36.0           48.2
 Reported        GPT-5.2               44.9          41.1           43.0        Table 2: Comparison against a memory-based persistence
 ReAct           GPT-5-mini            46.8          37.1           42.0
                                                                                baseline on DDR-Bench, averaged across the four backbones.
                 Kimi-K2               51.1          30.8           40.1
                 GPT-5.1               37.1          44.3           40.7
                                                                                “ReAct + Memory” stores past trajectories as retrievable
                 Gemini-3-Flash        44.8          21.2           33.0
                                                                                episodes and injects the top-k into the prompt.
                 GPT-5.5               60.6          64.2           62.4
                 GPT-5.6-sol           64.0          68.5           66.3                                               Insight     Summary        Overall
 Baseline                                                                        Method          Backbone
                 Claude-Sonnet-5       74.3          72.5           73.4                                               (%, ↑)       (%, ↑)        (%, ↑)
 (ReAct
                 Claude-Opus-4.8       74.0          73.0           73.5         Pandas Agent    GPT-4o                 54.0          40.0          47.0
 w/o Ontology)
                 DeepSeek-V4-Flash     26.2          30.3           28.2         AgentPoirot     GPT-3.5-turbo          50.0          31.0          40.5
                 Qwen3.5-Flash         16.4          14.3           15.4         AgentPoirot     GPT-4-turbo            56.0          35.0          45.5
                 GPT-5.5           58.4 (−2.2) 63.9 (−0.3) 61.2 (−1.2)           AgentPoirot     Llama-3-70B            52.0          33.0          42.5
                 GPT-5.6-sol       62.5 (−1.5) 65.5 (−3.0) 64.0 (−2.3)           AgentPoirot     GPT-4o                 60.0          44.0          52.0
 Baseline + SL
                 Claude-Sonnet-5   65.6 (−8.7) 57.5 (−15.0) 61.5 (−11.9)                         GPT-5.5                52.9          47.6          50.3
 (ReAct +
                 Claude-Opus-4.8   65.9 (−8.1) 71.4 (−1.6) 68.6 (−4.9)                           GPT-5.6-sol            51.6          49.4          50.5
 Semantic Layer)                                                                 Baseline
                 DeepSeek-V4-Flash 28.8 (+2.6) 31.7 (+1.4) 30.2 (+2.0)                           Claude-Sonnet-5        53.3          51.3          52.3
                 Qwen3.5-Flash     14.8 (−1.6) 13.3 (−1.0) 14.1 (−1.3)           (ReAct
                                                                                                 Claude-Opus-4.8        54.9          49.9          52.4
                                                                                 w/o Ontology)
                 GPT-5.5           74.0 (+13.4)   90.9 (+26.7)   82.5 (+20.1)                    DeepSeek-V4-Flash      45.0          34.6          39.8
                 GPT-5.6-sol       78.2 (+14.2)   93.5 (+25.0)   85.9 (+19.6)                    Qwen3.5-Flash          37.5          26.2          31.9
                 Claude-Sonnet-5    78.4 (+4.1)    81.3 (+8.8)    79.9 (+6.5)                    GPT-5.5           53.4 (+0.5) 48.6 (+1.0) 51.0 (+0.8)
 EvoOntology
                 Claude-Opus-4.8    78.0 (+4.0)   92.3 (+19.3)   85.2 (+11.7)                    GPT-5.6-sol       51.3 (−0.3) 50.8 (+1.4) 51.1 (+0.6)
                 DeepSeek-V4-Flash 37.5 (+11.4)   52.3 (+22.0)   44.9 (+16.7)    Baseline + SL
                                                                                                 Claude-Sonnet-5   53.5 (+0.2) 48.0 (−3.3) 50.8 (−1.6)
                 Qwen3.5-Flash      21.1 (+4.7)    19.1 (+4.8)    20.1 (+4.8)    (ReAct +
                                                                                                 Claude-Opus-4.8   55.8 (+0.9) 50.5 (+0.6) 53.2 (+0.8)
                                                                                 Semantic Layer)
                                                                                                 DeepSeek-V4-Flash 47.0 (+2.0) 36.5 (+1.9) 41.8 (+2.0)
Table 1: Main results on the DDR-Bench 10-K scenario.                                            Qwen3.5-Flash     39.0 (+1.5) 25.2 (−1.0) 32.1 (+0.2)
Parentheses report the gain over the Baseline result.                                            GPT-5.5             53.4 (+0.5)   48.6 (+1.0)   51.0 (+0.8)
                                                                                                 GPT-5.6-sol         53.2 (+1.6)   50.9 (+1.5)   52.1 (+1.6)
                                                                                                 Claude-Sonnet-5     54.4 (+1.1)   51.5 (+0.2)   53.0 (+0.7)
                                                                                 EvoOntology
                                                                                                 Claude-Opus-4.8     55.8 (+0.9)   50.5 (+0.6)   53.2 (+0.8)
Overall performance on every backbone, with a mean gain                                          DeepSeek-V4-Flash   49.2 (+4.2)   42.6 (+8.0)   45.9 (+6.1)
of 1.9 points and the largest improvement on DeepSeek-V4-                                        Qwen3.5-Flash       39.3 (+1.8)   27.6 (+1.4)   33.4 (+1.6)
Flash (+6.1). The gains are smaller than DDR-Bench be-
cause Insight is graded on short reference-style findings and                   Table 3: Main results on InsightBench. Parentheses report
saturates once the answer aligns with the reference. Base-                      the gain over the corresponding Baseline result.
line + SL recovers most of the Insight gain on InsightBench,
but drops by −3.3 on Claude-Sonnet-5 Summary, whereas
EvoOntology improves both Insight and Summary on all four                       Effect of Ontology Layer
backbones by exposing the same content through queryable
                                                                                To separate the contribution of the builder-constructed on-
tools instead of a static prompt.
                                                                                tology from the additional gain brought by self-evolution, we
   Capability on Data Retrieval. Table 4 reports BIRD re-                       compare three settings: Baseline, Initial, and Evolved. Base-
sults across six backbones under Oracle Knowledge. EvoOn-                       line uses no ontology layer, Initial uses the ontology con-
tology improves both EX and VES for every backbone, with                        structed by the builder agent before evolution, and Evolved
average gains of 7.4 and 8.6 points. The consistent gains                       uses the final ontology after self-evolution. Figure 3 reports
across both metrics indicate that the ontology improves query                   the performance of each backbone under the three settings.
correctness as well as execution efficiency. Baseline + SL                      To summarize the overall trend, we average the primary-
shows a mixed pattern: EX drops by up to −5.6 (GPT-5.5)                         metric scores across the four backbones for each benchmark
while VES rises across all backbones, indicating that a static                  and setting and compare the resulting means.
semantic layer improves SQL well-formedness but distracts                          The initial ontology establishes a strong improvement over
from producing correct queries. Once the same content is                        the no-ontology baseline, while self-evolution consistently
exposed through MCP tools that the agent actively queries                       extends this gain across all three benchmarks. On DDR-
and refined by the evolution loop, EvoOntology recovers the                     Bench, the mean Trajectory-Wise score increases by 12.3
EX gains and yields a stable per-backbone improvement over                      percentage points from Baseline to Initial, followed by a
both baselines and prior text-to-SQL systems (Pourreza and                      further improvement of 7.7 percentage points from Initial
Rafiei 2023; Wang et al. 2025; Talaei et al. 2024).                             to Evolved. On InsightBench, the mean Insight score first
                                                                                                                                                                                                 Baseline                       Initial                   Evolved
   Method                 Backbone            EX (%, ↑)      VES (%, ↑)
                                                                                                  100
                                                                                                                               DDR-Bench (10-K)                                                  60
                                                                                                                                                                                                                         InsightBench                                                                                   BIRD
                                                                                                                                              93.5
   GPT-4                  GPT-4                  46.4            –                                     90
                                                                                                                               90.9
                                                                                                                                                                       87.9
                                                                                                                                                                           92.3
                                                                                                                                                                                                 58
                                                                                                                                                                                                                                                                                          80                                                        78.3

                                                                                                                                          82.9                                                                                                                                                                                                  73.2
                                                                                                                                                                                                                                                                                                                                      71.8




                                                                                                                                                                                                                                                                        Overall EX (%)
                                                                                                                                                             81.3                                                                                                                                                       70.7
   DIN-SQL                GPT-4                  50.7           58.8

                                                                            Traj-Wise (%)
                                                                                                       80             78.2                               78.2                                    56                                                        55.755.8                       70              68.9      68.2



                                                                                                                                                                                   Insight (%)
                                                                                                                                                                                                                                                                                                                                  67.4       67.5
                                                                                                                                                                    73.0                                                                               54.9                                           66.1
                                                                                                                                                     72.5                                                                                   54.254.4                                                             63.5
   DAIL-SQL               GPT-4                  54.8           56.1                                   70                              68.5                                                      54           53.453.4                  53.3
                                                                                                                                                                                                                                                                                                   61.5                        61.9
                                                                                                                   64.2                                                                                   52.9               52.8
                                                                                                                                                                                                                                 53.2
                                                                                                                                                                                                                                                                                          60
                                                                                                       60                                                                                        52                      51.6
   TA-SQL                 GPT-4                  56.2            –                                                                                                                                                                                                                        50
                                                                                                       50                                                                                        50
   MAC-SQL                GPT-4                  57.6           58.8                                   40                                                                                        48                                                                                       40
                                                                                                                                      l        5                                                                     ol       t-5                                                                             ol       t-5
   MCS-SQL                GPT-4                  63.4            –                                              GPT-5
                                                                                                                      .5        .6-so    nnet-     us-4.8                                                  .5
                                                                                                                                                                                                      GPT-5 GPT-5.6-s e-Sonne e-Opus-4
                                                                                                                                                                                                                                       .8                                                           .5
                                                                                                                                                                                                                                                                                               GPT-5 GPT-5.6-s e-Sonne e-Opus-4
                                                                                                                                                                                                                                                                                                                                .8
                                                                                                                           GPT-5 laude-So laude-Op                                                                      d        d                                                                               d        d
                                                                                                                                 C         C                                                                      Clau      Clau                                                                           Clau      Clau
   CHESS                  GPT-4o                 65.0           62.8

                          GPT-5.5                61.5           63.4           Figure 3: Primary metric on the three benchmarks under three
                          GPT-5.6-sol            63.5           65.6           conditions: Baseline , Initial, and Evolved (EvoOntology).
   Baseline               Claude-Sonnet-5        61.9           63.7
   (ReAct w/o Ontology)   Claude-Opus-4.8        67.5           69.6                                                                                                GPT-5.5                      GPT-5.6-sol                    Claude-Sonnet-5                       Claude-Opus-4.8
                          DeepSeek-V4-Flash      33.1           36.4                                                       DDR-Bench (10-K)                                                                              InsightBench                                                     80
                                                                                                                                                                                                                                                                                                                        BIRD
                                                                                                  95
                          Qwen3.5-Flash          46.5           47.9                                                                                                                            56                                                                                        78




                                                                            Trajectory-Wise (%)
                                                                                                  90                                                                                                                                                                                      76


                                                                                                                                                                                                                                                                         Overall EX (%)
                                                                                                                                                                                                55                                                                                        74

                                                                                                                                                                                  Insight (%)
                          GPT-5.5             55.9 (−5.6)    67.7 (+4.3)                          85                                                                                            54
                                                                                                                                                                                                                                                                                          72
                                                                                                                                                                                                                                                                                          70
                          GPT-5.6-sol         63.0 (−0.5)    68.9 (+3.3)                          80                                                                                            53                                                                                        68
   Baseline + SL                                                                                                                                                                                                                                                                          66
                          Claude-Sonnet-5     60.8 (−1.1)    65.8 (+2.1)                          75                                                                                            52                                                                                        64
   (ReAct +                                                                                                 0              1             2           3          4          5                          0                  1                   2                   3                             0             1             2             3             4
                          Claude-Opus-4.8     66.2 (−1.3)    75.0 (+5.4)                                                              Evolution round                                                                    Evolution round                                                                         Evolution round
   Semantic Layer)
                          DeepSeek-V4-Flash   36.3 (+3.2)    37.2 (+0.7)
                          Qwen3.5-Flash       48.0 (+1.5)    51.9 (+4.0)       Figure 4: Primary metric across accepted evolution rounds
                          GPT-5.5              68.9 (+7.4)    71.1 (+7.7)
                                                                               on the three benchmarks: Traj-Wise on DDR-Bench, Insight
                          GPT-5.6-sol          70.7 (+7.2)    73.0 (+7.4)      on InsightBench, and EX on BIRD.
                          Claude-Sonnet-5      71.8 (+9.9)   74.1 (+10.4)
   EvoOntology
                          Claude-Opus-4.8     78.3 (+10.8)   80.5 (+10.9)
                          DeepSeek-V4-Flash    39.4 (+6.4)    44.1 (+7.6)      Opus-4.8 reaching 92.3 after four. Notably, the trajectories
                          Qwen3.5-Flash        49.1 (+2.5)    55.2 (+7.3)      flatten by the last two rounds, which is consistent with the
                                                                               failure signatures becoming rarer once the ontology covers
Table 4: Main results on BIRD under Oracle Knowledge.                          the recurrent cross-filing concepts. The results show that the
VES is reported on a 0–100 scale. Parentheses report the                       gains reported in Table 1 are the outcome of a converging
gain over the corresponding Baseline result.                                   refinement and not a single fortunate patch, which validates
                                                                               the design of the four-step evolution loop.

increases by 0.8 points and then gains another 0.2 points                      Ablation Study on Evolution Loop
through evolution. On BIRD, the mean EX score improves
                                                                               The relative contribution of the four steps in the evolution
by 5.1 percentage points with the initial ontology and by a
                                                                               loop (diagnose, attribute, patch, gate) is assessed by dis-
further 3.7 percentage points after evolution. These results
                                                                               abling each step in turn and comparing the resulting final
show that the builder-constructed ontology provides an effec-
                                                                               Evolved score on DDR-Bench, averaged across the four back-
tive starting point, whereas the self-evolution loop is essen-
                                                                               bones.The disabled variant of each step is: w/o Diagnose
tial for realizing the full performance gain and consistently
                                                                               skips the failure-trace clustering step and asks the evolution
improves the ontology beyond its initial state.
                                                                               agent to propose an edit from a random sample of recent
                                                                               traces; w/o Attribution drops the level tag and lets the agent
                             Analyses                                          commit an edit at any level without stating a hypothesis; w/o
To better understand the source and behavior of EvoOntol-                      Patch stage replaces the typed, hypothesis-conditioned edit
ogy’s advantage, we conduct a series of in-depth analyses.                     with a free-form ontology rewrite that the evolution agent
Unless otherwise stated, all analyses in this section are con-                 produces directly from the diagnosis; w/o Gate accepts ev-
ducted on DDR-Bench across the four backbones (GPT-5.5,                        ery candidate patch. As shown in Table 5, removing the gate
GPT-5.6-sol, Claude-Sonnet-5, Claude-Opus-4.8).                                causes the largest drop (−11.2 Traj-Wise), because unfiltered
                                                                               candidates admit regressions that the next round cannot al-
Effect of Iterative Evolution                                                  ways undo. Removing the attribution step drops by −6.3,
To evaluate whether the observed gain accumulates through                      because without a level tag the loop tends to make content
many small edits and does not collapse into a single round,                    edits when the failure is a manifest problem, and vice versa.
we plot the deployed agent’s primary score across the se-                      Removing the diagnose step drops by −4.8, and replacing
quence of accepted evolution rounds on DDR-Bench. Each                         the typed patch with a free-form rewrite drops by −1.7. The
round corresponds to one candidate that passed the paired                      results show that the gate and attribution are the two load-
gate, and the parent line traces the score of the ontology ver-                bearing pieces, which validates the design of an evolution
sion that would remain if no more rounds were run. As shown                    loop that is more selective than iterative.
in Figure 4, all four backbones improve monotonically from                        Three-Level Evolution. Beyond removing individual
Initial through the accepted rounds, with GPT-5.6-sol reach-                   steps, we further evaluate whether the three editable levels
ing 93.5 Traj-Wise after five accepted rounds and Claude-                      (Content / Tool / Schema) are jointly required by restricting
     Variant                      Traj-Wise (%, ↑)    ∆                          Variant                                     Traj-Wise (%, ↑)                                                   ∆
     Full loop                         89.5            –                         Full EvoOntology                                                                  89.5                       –
       w/o Gate                        78.3          −11.2                         w/o Mappings                                                                    76.1                     −13.4
       w/o Attribution                 83.2          −6.3                          w/o Evidence                                                                    80.8                     −8.7
       w/o Diagnose                    84.7          −4.8                          w/o Constraints                                                                 86.0                     −3.5
       w/o Patch (free-form)           87.8          −1.7                          w/o Relations                                                                   87.4                     −2.1

Table 5: Ablation on the four steps of the evolution loop,        Table 7: Ablation on the five object families of the ontology
averaged across four backbones.                                   content layer on DDR-Bench, averaged across four back-
                                                                  bones. Terms cannot be masked in isolation and are omitted.
     Variant                      Traj-Wise (%, ↑)     ∆
                                                                                                                    1.0                                                                                        95
     Baseline                           69.5           –                                                                                                              GPT-5.5    90.9   82.4    71.8   78.9
                                                                         GPT-5.5 1.00     0.61     0.58    0.56     0.9                                                                                        90




                                                                                                                                        Store fitted on backbone
       Content-only evolution           78.2         +8.7

                                                                                                                                                                                                                Performance (%)
                                                                                                                    0.8                                            GPT-5.6-sol   80.6   93.5    70.2   77.5    85


                                                                                                                      Jaccard overlap
       Tool-only evolution              82.7         +13.2            GPT-5.6-sol 0.61    1.00     0.60    0.62
                                                                                                                    0.7                                                                                        80
       Schema-only evolution            73.1         +3.6                                                                                                            Sonnet-5    73.1   76.8    81.3   82.1
                                                                  Claude-Sonnet-5 0.58    0.60     1.00    0.55
     Full three-level evolution         89.5         +20.0                                                          0.6                                                                                        75
                                                                                                                                                                     Opus-4.8    75.4   78.9    75.6   92.3
                                                                  Claude-Opus-4.8 0.56    0.62     0.55    1.00     0.5                                                                                        70

Table 6: Ablation on the three editable levels of the evolution                                                                                                                 5.5     -sol  t-5    4.8
                                                                                  5.5     -sol    t-5
                                                                              GPT- GPT-5.6 e-Sonne e-Opus-
                                                                                                           4.8      0.4                                                     GPT- GPT-5.6 Sonne Opus-
                                                                                            d       d
loop on DDR-Bench, averaged across four backbones.                                     Clau    Clau                                                                              Agent backbone (deployment)

                                                                  (a) Pairwise Jaccard overlap of                                           (b) Cross-backbone transfer of
                                                                  accepted Term identifiers be-                                             the evolved store: each row is fit-
the evolution loop to a single level at a time and comparing      tween the evolved stores of the                                           ted on one backbone and served
against the full three-level variant on DDR-Bench, averaged       four backbones.                                                           to every backbone (columns).
across the four backbones. As shown in Table 6, Tool-only
evolution recovers the largest single-level gain (+13.2 over      Figure 5: Generalization of the evolved ontology store across
Baseline), consistent with the manifest reshaping being the       backbones on DDR-Bench.
dominant lever surfaced by the attribution analysis in Fig-
ure 7. Content-only and Schema-only evolution contribute
+8.7 and +3.6 respectively, but none reaches the +20.0 of         do (0.61). The accepted edits also differ across backbones.
the full three-level loop. The results indicate that the three    For example, Claude-Opus-4.8 retains more detailed man-
levels are complementary and not substitutable, which val-        ifest variants than Claude-Sonnet-5, while GPT-5.5 intro-
idates the design of an evolution loop that ranges over all       duces short SQL fragment libraries under Evidence that do
three editable levels.                                            not appear in the Claude-Opus-4.8 ontology. However, iden-
                                                                  tifier overlap alone cannot determine semantic equivalence,
Ablation Study on Ontology Structure                              since different identifiers may encode similar concepts. We
We mask each removable object family from the final Evolved       further evaluate cross-backbone transfer by applying each
ontology on DDR-Bench and report the average performance          evolved store to all four backbones and measuring Traj-Wise
across four backbones. As shown in Table 7, masking Map-          performance on DDR-Bench. As shown in Figure 5b, the
pings causes the largest drop (−13.4 Traj-Wise), which is         diagonal is uniformly the highest entry of its column, and
consistent with the role of Mappings as the only object that      every off-diagonal drops by at least 6.6 points relative to the
grounds a Term to concrete columns and join paths. Masking        same-backbone store; the average column drop from diag-
Evidence drops by −8.7, because without a probe query the         onal to off-diagonal ranges from −6.6 (Sonnet-5) to −10.9
agent cannot verify a candidate SQL fragment against the          (GPT-5.5). These results show that different backbones pro-
underlying value distribution. Masking Constraints and Re-        duce different evolved ontology stores from the same initial-
lations produces smaller drops (−3.5 and −2.1), and Terms         ization. The cross-backbone transfer results further indicate
cannot be masked in isolation as every other family refer-        that backbone-specific evolution is beneficial.
ences them. These findings identify Mappings and Evidence
as the two load-bearing families, which validates our deci-                                                       Conclusion
sion to require every committed entry to be anchored in a         In this paper, we introduce EvoOntology, an interactive ontol-
probe query and not a natural-language description alone.         ogy layer that is automatically constructed and self-evolving
                                                                  for data agents. EvoOntology encapsulates the ontology as an
Divergence across Backbones                                       MCP server that the agent actively queries at runtime, and re-
We investigate whether different backbones converge to sim-       fines it through attribution-guided typed edits admitted only
ilar ontologies or develop distinct ones by comparing the         after a backbone-conditional paired evaluation gate. Exper-
pairwise Jaccard overlap of their accepted Term-identifier        iments on benchmarks and six LLM backbones, EvoOntol-
sets on DDR-Bench. As shown in Figure 5a, no pair ex-             ogy consistently outperforms both ReAct baselines and tradi-
ceeds 0.62 overlap, and the two Claude backbones share            tional semantic-layer baselines, offering an effective solution
less with each other (0.55) than the two GPT backbones            for helping data agents understand heterogeneous data.
                         References                                 Li, J.; Hui, B.; Qu, G.; Li, B.; Yang, J.; Li, B.; Wang, B.; Qin,
Asai, A.; Wu, Z.; Wang, Y.; Sil, A.; and Hajishirzi, H. 2024.       B.; Cao, R.; Geng, R.; et al. 2023. Can llm already serve as
Self-rag: Learning to retrieve, generate, and critique through      a database interface. A big bench for large-scale database
self-reflection. In International conference on learning rep-       grounded text-to-SQLs, 2305.
resentations, volume 2024, 9112–9141.                               Li, Z.; Wang, X.; Zhao, J.; Yang, S.; Du, G.; Hu, X.; Zhang,
Caferoğlu, H. A.; and Ulusoy, Ö. 2024. E-SQL: Direct                B.; Ye, Y.; Li, Z.; Zhao, R.; and Mao, H. 2024b. PET-SQL:
Schema Linking via Question Enrichment in Text-to-SQL.              A Prompt-Enhanced Two-Round Refinement of Text-to-SQL
arXiv:2409.16751.                                                   with Cross-consistency. arXiv:2403.09732.
Cao, Z.; Zheng, Y.; Fan, Z.; Zhang, X.; Chen, W.; and Bai,          Liu, W.; Yu, P.; Orini, M.; Du, Y.; and He, Y. 2026. Hunt In-
X. 2024. RSL-SQL: Robust Schema Linking in Text-to-SQL              stead of Wait: Evaluating Deep Data Research on Large Lan-
Generation. arXiv:2411.00073.                                       guage Models. Accepted at the 43rd International Conference
Chang, S.; and Fosler-Lussier, E. 2023. How to Prompt               on Machine Learning (ICML 2026), arXiv:2602.02039.
LLMs for Text-to-SQL: A Study in Zero-shot, Single-                 Madaan, A.; Tandon, N.; Gupta, P.; Hallinan, S.; Gao, L.;
domain, and Cross-domain Settings. arXiv:2305.11853.                Wiegreffe, S.; Alon, U.; Dziri, N.; Prabhumoye, S.; Yang,
Chen, W.; Wang, H.; Chen, J.; Zhang, Y.; Wang, H.; Li, S.;          Y.; et al. 2023. Self-refine: Iterative refinement with self-
Zhou, X.; and Wang, W. Y. 2020. TabFact: A Large-scale              feedback. Advances in neural information processing sys-
Dataset for Table-based Fact Verification. In 8th Interna-          tems, 36: 46534–46594.
tional Conference on Learning Representations, ICLR 2020,           Nan, L.; Zhao, Y.; Zou, W.; Ri, N.; Tae, J.; Zhang, E.; Cohan,
Addis Ababa, Ethiopia, April 26-30, 2020. OpenReview.net.           A.; and Radev, D. 2023. Enhancing text-to-SQL capabil-
dbt Labs. 2023. The Semantic Layer for Modern Data Teams.           ities of large language models: A study on prompt design
https://www.getdbt.com/product/semantic-layer. Accessed             strategies. In Findings of the Association for Computational
2025-11-01.                                                         Linguistics: EMNLP 2023, 14935–14956.
Dietterich, T. G. 1998. Approximate statistical tests for com-      Pasupat, P.; and Liang, P. 2015. Compositional semantic
paring supervised classification learning algorithms. Neural        parsing on semi-structured tables. In Proceedings of the 53rd
computation, 10(7): 1895–1923.                                      Annual Meeting of the Association for Computational Lin-
Feng, S.; Shi, W.; Bai, Y.; Balachandran, V.; He, T.; and           guistics and the 7th International Joint Conference on Nat-
Tsvetkov, Y. 2024. Knowledge card: Filling LLMs’ knowl-             ural Language Processing (Volume 1: Long Papers), 1470–
edge gaps with plug-in specialized language models. In Inter-       1480.
national Conference on Learning Representations, volume             Patil, S. G.; Zhang, T.; Wang, X.; and Gonzalez, J. E. 2024.
2024, 16097–16121.                                                  Gorilla: Large language model connected with massive apis.
Guo, S.; Deng, C.; Wen, Y.; Chen, H.; Chang, Y.; and Wang,          Advances in Neural Information Processing Systems, 37:
J. 2024. DS-Agent: Automated Data Science by Empowering             126544–126565.
Large Language Models with Case-Based Reasoning. In Pro-            Pourreza, M.; and Rafiei, D. 2023. Din-sql: Decomposed in-
ceedings of the 41st International Conference on Machine            context learning of text-to-sql with self-correction. Advances
Learning, volume 235 of Proceedings of Machine Learning             in neural information processing systems, 36: 36339–36348.
Research, 16813–16848. PMLR.                                        Qin, Y.; Liang, S.; Ye, Y.; Zhu, K.; Yan, L.; Lu, Y.; Lin, Y.;
Hitzler, P. 2021. A Review of the Semantic Web Field.               Cong, X.; Tang, X.; Qian, B.; et al. 2023. Toolllm: Facil-
Communications of the ACM, 64(2): 76–83.                            itating large language models to master 16000+ real-world
Hong, S.; Lin, Y.; Liu, B.; Liu, B.; Wu, B.; Zhang, C.; Li, D.;     apis. In The twelfth international conference on learning
Chen, J.; Zhang, J.; Wang, J.; et al. 2025. Data interpreter:       representations.
An llm agent for data science. In Findings of the Association       Sahu, G.; Puri, A.; Rodriguez, J. A.; Abaskohi, A.; Chegini,
for Computational Linguistics: ACL 2025, 19796–19821.               M.; Drouin, A.; Taslakian, P.; Zantedeschi, V.; Lacoste, A.;
Khattab, O.; Singhvi, A.; Maheshwari, P.; Zhang, Z.; San-           Vazquez, D.; Chapados, N.; Pal, C.; Rajeswar, S.; and Laradji,
thanam, K.; Vardhamanan, S.; Haq, S.; Sharma, A.; Joshi,            I. 2025. InsightBench: Evaluating Business Analytics Agents
T. T.; Moazam, H.; Miller, H.; Zaharia, M.; and Potts, C.           Through Multi-Step Insight Generation. In Yue, Y.; Garg, A.;
2023. DSPy: Compiling Declarative Language Model Calls              Peng, N.; Sha, F.; and Yu, R., eds., International Conference
into Self-Improving Pipelines. arXiv:2310.03714.                    on Learning Representations, volume 2025, 4683–4715.
Lei, F.; Chen, J.; Ye, Y.; Cao, R.; Shin, D.; Su, H.; Suo, Z.;      Schick, T.; Dwivedi-Yu, J.; Dessì, R.; Raileanu, R.; Lomeli,
Gao, H.; Hu, W.; Yin, P.; et al. 2025. Spider 2.0: Evalu-           M.; Hambro, E.; Zettlemoyer, L.; Cancedda, N.; and Scialom,
ating language models on real-world enterprise text-to-sql          T. 2023. Toolformer: Language models can teach themselves
workflows. In International Conference on Learning Repre-           to use tools. Advances in neural information processing
sentations, volume 2025, 28691–28735.                               systems, 36: 68539–68551.
Li, H.; Zhang, J.; Liu, H.; Fan, J.; Zhang, X.; Zhu, J.; Wei, R.;   Shinn, N.; Cassano, F.; Gopinath, A.; Narasimhan, K.; and
Pan, H.; Li, C.; and Chen, H. 2024a. Codes: Towards building        Yao, S. 2023. Reflexion: Language agents with verbal re-
open-source language models for text-to-sql. Proceedings of         inforcement learning. Advances in neural information pro-
the ACM on Management of Data, 2(3): 1–28.                          cessing systems, 36: 8634–8652.
Talaei, S.; Pourreza, M.; Chang, Y.-C.; Mirhoseini, A.; and
Saberi, A. 2024. CHESS: Contextual Harnessing for Efficient
SQL Synthesis. arXiv:2405.16755.
Wang, B.; Ren, C.; Yang, J.; Liang, X.; Bai, J.; Chai, L.;
Yan, Z.; Zhang, Q.-W.; Yin, D.; Sun, X.; and Li, Z. 2025.
MAC-SQL: A Multi-Agent Collaborative Framework for
Text-to-SQL. In Rambow, O.; Wanner, L.; Apidianaki, M.;
Al-Khalifa, H.; Eugenio, B. D.; and Schockaert, S., eds., Pro-
ceedings of the 31st International Conference on Computa-
tional Linguistics, 540–557. Abu Dhabi, UAE: Association
for Computational Linguistics.
Wang, G.; Xie, Y.; Jiang, Y.; Mandlekar, A.; Xiao, C.;
Zhu, Y.; Fan, L.; and Anandkumar, A. 2023. Voyager: An
Open-Ended Embodied Agent with Large Language Models.
arXiv:2305.16291.
Wang, Y.; Chen, Y.; Goyal, A.; and Sundaram, H. 2026.
CausalDetox: Causal Head Selection and Intervention for
Language Model Detoxification. In Findings of the Asso-
ciation for Computational Linguistics: ACL 2026, 11893–
11914.
Xu, T.; Wen, H.; and Li, M. 2026. Adapting the interface,
not the model: Runtime harness adaptation for deterministic
llm agents. arXiv preprint arXiv:2605.22166.
Yang, C.; Wang, X.; Lu, Y.; Liu, H.; Le, Q. V.; Zhou, D.;
and Chen, X. 2024. Large language models as optimizers.
In International Conference on Learning Representations,
volume 2024, 12028–12068.
Yao, S.; Zhao, J.; Yu, D.; Shafran, I.; Narasimhan, K. R.; and
Cao, Y. 2022. React: Synergizing reasoning and acting in
language models. In NeurIPS 2022 Foundation Models for
Decision Making Workshop.
Yu, T.; Zhang, R.; Yang, K.; Yasunaga, M.; Wang, D.; Li, Z.;
Ma, J.; Li, I.; Yao, Q.; Roman, S.; et al. 2018. Spider: A large-
scale human-labeled dataset for complex and cross-domain
semantic parsing and text-to-sql task. In Proceedings of the
2018 conference on empirical methods in natural language
processing, 3911–3921.
Zhang, W.; Shen, Y.; Tan, Z.; Hou, G.; Lu, W.; and Zhuang, Y.
2023a. Data-Copilot: Bridging Billions of Data and Humans
with Autonomous Workflow. arXiv:2306.07209.
Zhang, X.; Yang, Y.; Lasseigne, B.; and Yao, X. 2023b.
Schema-Aware Multi-Task Learning for Complex Text-to-
SQL. arXiv:2305.09994.
Zhou, Y.; Muresanu, A. I.; Han, Z.; Paster, K.; Pitis, S.; Chan,
H.; and Ba, J. 2022. Large language models are human-level
prompt engineers. In The eleventh international conference
on learning representations.
                                                                                            100
                    160                                                                                                                  Metric                       Baseline                  Initial       Evolved
                                                                                            95
                    140                                                                                                                  Input tokens / turn (K)                3.2                  4.1           4.6
                                                                                            90
                    120


Number of objects
                                                                                                                                         Output tokens / turn (K)               0.4                  0.4           0.4


                                                                                              Performance (%)
                    100                                                                     85                                           Turns / task                          14.6                 11.2           8.4
                     80                                                                     80                                           Total tokens / task (K)               52.6                 50.4          42.0
                     60                                                                     75                                           Traj-Wise (%, ↑)                      69.5                 81.8          89.5
                     40                                                                     70
                                                                 Terms        Constraints
                     20                                          Mappings     Evidence      65                    Table 8: Cost of the ontology layer on DDR-Bench, averaged
                                                                 Relations    Traj-Wise
                      0                                                                     60                    across the four-backbone analysis subset.
                             R0         R1     R2           R3           R4          R5
                          (Initial)
                                               Evolution round                                                                                                                          70
                                                                                                                                    14
                                                                                                                                                                                        60   57%
   Figure 6: Growth of the Content Layer across accepted evo-                                                                       12               11



                                                                                                                # accepted rounds
                                                                                                                                                                                        50


                                                                                                                                                                      % of total gain
   lution rounds on DDR-Bench under GPT-5.6-sol. The curves                                                                         10
                                                                                                                                     8                                                  40                  34%
   report the four node families and instantiated Semantic Re-                                                                              6
                                                                                                                                     6                                                  30
   lations. The right axis reports Trajectory-Wise performance.
                                                                                                                                     4                         3                        20
                                                                                                                                                                                        10                               9%
                                                                                                                                     2
                                                                                                                                     0                                                   0
                      Content-Layer Growth across Evolution                                                                                Tool    Content   Schema                          Tool          Content   Schema
                                     Rounds                                                                       Figure 7: Distribution of the accepted evolution gain across
                                                                                                                  Content, Tool, and Schema edits on DDR-Bench, aggregated
   To examine whether iterative evolution causes uncontrolled                                                     over the four-backbone analysis subset.
   expansion of the ontology content, we track its instantiated el-
   ements across the accepted evolution rounds on DDR-Bench,
   using GPT-5.6-sol as a representative backbone. The tracked                                                                              Attribution across Editable Levels
   elements comprise the four node families, Terms, Mappings,
   Constraints, and Evidence, together with instantiated Seman-                                                   We next examine how the accepted evolution gain is dis-
   tic Relations.As shown in Figure 6, most content growth oc-                                                    tributed across the three editable levels. Each accepted round
   curs in the first three rounds. The number of Terms increases                                                  is grouped by its attribution tag, and the paired-evaluation
   from 61 in the Initial ontology to 80 after five accepted                                                      improvement contributed by each group is aggregated across
   rounds, while the per-round growth of every tracked element                                                    the four backbones. As shown in Figure 7, Tool-level edits
   falls below 5% after round three. The content-size curves                                                      account for 57% of the cumulative gain across six accepted
   then flatten together with Trajectory-Wise performance. Con-                                                   rounds. These edits mainly improve how existing ontology
   tent expansion is therefore concentrated in the early rounds,                                                  content is exposed through the manifest and MCP tools.
   when the evolution loop addresses recurrent semantic gaps,                                                     Content-level edits contribute 34% across eleven accepted
   and stabilizes once these gaps have been covered.                                                              rounds by adding or refining Terms, Mappings, Constraints,
                                                                                                                  Evidence, and Semantic Relations identified from interac-
                                                                                                                  tion trajectories. Schema-level edits contribute the remaining
                                                                                                                  9% across three accepted rounds by changing the represen-
                                      Cost of the Ontology Layer                                                  tational structure of the ontology. Content edits are more
                                                                                                                  frequent, while Tool edits contribute the largest share of the
   The ontology layer introduces a compact manifest into the                                                      accumulated gain. Schema edits are less common but address
   agent’s initial context and retrieves detailed semantic records                                                limitations that cannot be resolved by modifying instantiated
   through MCP tools. We measure its computational cost us-                                                       content alone. This distribution is consistent with the three
   ing the average input and output tokens per turn, the number                                                   levels serving distinct and complementary roles during evo-
   of turns per task, and the resulting total tokens per task on                                                  lution.
   DDR-Bench.Table 8 shows that the Initial ontology increases
   average input tokens per turn from 3.2K to 4.1K because                                                                               Case Study: Evolution of Card-Legality
   of the manifest and retrieved semantics. At the same time,
   the average trajectory shortens from 14.6 to 11.2 turns, re-                                                                                       Semantics
   ducing the total cost from 52.6K to 50.4K tokens per task.                                                     Figure 8 presents a representative text-to-SQL case in which
   The Evolved ontology further reduces the trajectory to 8.4                                                     the agent must identify cards that are banned in a target game
   turns and the total cost to 42.0K tokens, which is approxi-                                                    format. The case illustrates how a localized Content-level
   mately 20% below the Baseline. Over the same comparison,                                                       update extends the ontology without rewriting its existing
   Trajectory-Wise performance rises from 69.5 to 89.5.The                                                        Tool or Schema layers.
   ontology layer therefore adds modest per-turn context while                                                       Initial state. The Initial ontology L0 contains the Terms
   reducing repeated schema discovery over the full trajectory.                                                   Card and Legality, together with an association between
   Evolution strengthens this effect by improving how the agent                                                   them. The Card Term is grounded to Cards.uuid, while
   discovers and grounds relevant semantics.                                                                      the Legality Term is grounded to legalities.uuid,
                                      Initial Ontology L0                                                                                             Evolved Ontology Lt
                                               Tool Layer                                                                                                              Tool Layer
             Tool 1: browse                             Tool 2: resolve                                                      Tool 1: browse                                           Tool 2: resolve

             • Find relevant terms                      • Retrieve complete semantics                                        • Find relevant terms                                    • Retrieve complete semantics
             • Query → Ranked Terms                     • Term IDs → Mappings, Relations, Constraints, and Evidence          • Query → Ranked Terms                                   • Term IDs → Mappings, Relations, Constraints, and Evidence




      Schema Layer                                   Content Layer                                                    Schema Layer                                                  Content Layer
                                                                                                                                                                      association                         association
                                                     association                                                                                                                                                          Legality
         Term                           Card                              Legality                           ...         Term                           Card                         Legality
                                                                                                                                                                                                                        Status Code                ...
                                                                                                                                                                                                                 Constrained
                                                                                                                                                                                                                     by
                                                                      legalities.uuid                                                                                               legalities.uuid
         Mapping                      Cards.u                         legalities.format                      ...         Mapping                      Cards.u                       legalities.format                     legalities.status        ...
                                      uid                             legalities.status                                                               uid                           legalities.status




         Evidence                     cards schema                   legalities schema                       ...         Evidence                     cards schema                    legalities schema                        legalities.status   ...
                                                                                                                                                                                                                                 distribution

                                                                                                             ...
                                                                                                                                                       To identify banned cards, use: legalities.status='Banned’ with                              ...
        Constraint                                     No legality rule                                                 Constraint                     legalities.format=<target format>




        Semantic Relation             Has mapping            Constraints by                   Evidence supports        Semantic Relation                Has mapping                       Constraints by                         Evidence supports




Figure 8: Evolution of the ontology for a card-legality task. The Initial state contains general Card and Legality semantics but
no explicit interpretation of legality status. The accepted patch adds a Legality Status Code Term, its Mapping and Evidence,
and a Constraint that relates the status value to the requested format. Red dashed boxes mark the added or refined objects.


legalities.format, and legalities.status.
Schema observations for the two tables are retained as Ev-
idence.Although these objects allow the agent to locate the
relevant table, the ontology does not explain how the values
of legalities.status should be interpreted. It also
does not make explicit that legality status is defined relative
to a particular game format. The agent must therefore redis-
cover these semantics from raw values during execution.
   Attributed limitation. The evolution agent attributes this
limitation to the Content Layer. The existing browse and
resolve tools can already retrieve the relevant objects, and
the Schema Layer can represent the required knowledge. The
missing component is a reusable semantic description of the
status field and its applicability condition.
   Localized intervention. The Candidate adds a new
Term, Legality Status Code, and grounds it to
legalities.status. An Evidence object records
the observed distribution of the status values. A Con-
straint then states that identifying banned cards re-
quires both legalities.status = ’Banned’ and
legalities.format = target_format. The ex-
isting Card and Legality objects remain unchanged, and the
Candidate introduces no Tool- or Schema-level modifica-
tion.After passing paired validation, the Candidate becomes
part of the Evolved ontology Lt .
   Effect on agent interaction. With the Evolved ontology,
browse can surface Legality Status Code for queries involv-
ing banned or legal cards. The agent can then use resolve
to obtain the physical Mapping, the supporting Evidence,
and the format-dependent Constraint. Native SQL execution
remains responsible for applying the filter and verifying the
returned records.The case shows that evolution can correct
a specific semantic gap by adding a small connected set of
objects. The ontology retains its existing structure and inter-
face while providing the agent with the missing interpretation
required for the task.

