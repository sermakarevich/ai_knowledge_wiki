A Generalized Software Architecture for Swarm
Agentic AI: Decentralized Coordination for
Task-Agnostic Multi-Agent Systems
Mingyu Kang
Dublin, California, USA
amg.kang@email.com
Abstract—The proliferation of large language models and
autonomous reasoning agents has catalyzed a paradigm shift
from monolithic AI systems toward distributed, multi-agent
collectives capable of addressing open-ended computational prob-
lems. However, prevailing multi-agent frameworks frequently rely
on hierarchical orchestrators or centralized coordinators, which
introduce single points of failure, scalability bottlenecks, and rigid
task-specific assumptions that limit generalizability. This paper
proposes a generalized, task-agnostic software architecture for
swarm agentic AI in which heterogeneous autonomous agents
collaborate through fully decentralized coordination mechanisms
to complete complex, abstract goals. The proposed framework
integrates three principal subsystems: (i) a Dynamic Task Decom-
position and Allocation layer that recursively partitions abstract
goals into executable sub-tasks and distributes them across the
swarm using a capability-aware, load-sensitive bidding protocol;
(ii) a Decentralized State Synchronization layer that employs
gossip-based dissemination and conflict-free replicated data types
to maintain a coherent shared context, prevent redundant com-
putation, and track task progression without reliance on a central
node; and (iii) a Scalability and Fault Tolerance layer that enables
agents to join, scale, or depart from the network dynamically
while preserving operational continuity through state replication
and adaptive role reassignment. By decoupling the coordination
substrate from the underlying task semantics, the architecture
supports a broad class of cooperative problem-solving scenarios
without modification to its core protocols. The paper articulates
the conceptual foundations of the system, identifies the formal
properties required for convergence and consistency, and outlines
a modular implementation pathway. The contribution is intended
to serve as a reference design for future research on resilient,
large-scale agentic AI ecosystems.
Index Terms—Agentic AI, decentralized multi-agent systems,
swarm intelligence, task decomposition, distributed consensus,
fault tolerance, software architecture.
I. INTRODUCTION
A. Background and Motivation
Recent advances in foundation models and autonomous
reasoning have positioned artificial intelligence agents as first-
class computational entities capable of perceiving context,
planning, invoking tools, and producing goal-directed behavior
over extended time horizons. As the complexity of target
tasks grows—spanning domains such as scientific discovery,
software synthesis, knowledge curation, and large-scale data
analysis—the limitations of single-agent systems become in-
creasingly apparent. Bounded context windows, constrained
reasoning depth, and the inherent serialization of single-
agent execution motivate the transition toward multi-agent
configurations in which several agents operate concurrently
and cooperatively.
While multi-agent frameworks have demonstrated promis-
ing results, the majority of contemporary implementations
adopt a centralized or hierarchical control topology. In such
designs, a designated orchestrator agent decomposes the user
goal, assigns sub-tasks to worker agents, and aggregates
the resulting outputs. Although conceptually straightforward,
this pattern reproduces the architectural deficiencies that dis-
tributed systems research has long sought to mitigate: the
orchestrator constitutes a single point of failure, becomes
a throughput bottleneck under increasing swarm size, and
typically encodes task-specific assumptions that impair gen-
eralization across problem domains.
Swarm intelligence, by contrast, offers a complementary
design philosophy in which global behavior emerges from
local interactions among autonomous, peer-level participants.
When applied to agentic AI, this philosophy suggests an
architecture in which no agent holds privileged coordination
authority, and in which collective problem-solving capacity
is a function of protocol design rather than central control.
Realizing this vision in software, however, requires careful
treatment of three intertwined concerns: how abstract goals are
decomposed and distributed, how shared state is synchronized
in the absence of a central authority, and how the system
remains operational under churn and partial failure.
B. Problem Statement
Despite growing interest in agentic AI, there is currently
no widely adopted reference architecture that simultaneously
satisfies the following requirements: (1) task-agnosticism, in
which the coordination substrate is independent of the se-
mantics of any particular problem domain; (2) decentraliza-
tion, in which coordination, state management, and decision-
making are distributed across all participating agents; and (3)
operational resilience, in which the system tolerates dynamic
membership changes, agent failures, and network partitions
without compromising progress on active tasks. Addressing
these requirements jointly—rather than in isolation—remains
an open architectural problem.

C. Scope and Contributions
This paper is concerned exclusively with the software-
level architecture of swarm agentic AI systems. Considera-
tions related to physical hardware, embodied robotics, sensor
fusion, and actuation in physical environments are deliberately
excluded. The scope is restricted to the design of the coordi-
nation substrate, the inter-agent communication and consensus
protocols, and the network dynamics that govern collective
behavior. Within this scope, the paper makes the following
contributions:
1) It introduces a generalized, task-agnostic software ar-
chitecture for swarm agentic AI in which coordination
concerns are cleanly separated from task semantics,
enabling reuse across heterogeneous problem domains.
2) It formulates a Dynamic Task Decomposition and Allo-
cation mechanism in which abstract goals are recursively
partitioned into sub-tasks and assigned to agents via
a capability-aware, load-sensitive protocol that operates
without a central scheduler.
3) It specifies a Decentralized State Synchronization layer
based on gossip dissemination and conflict-free repli-
cated data types, allowing agents to share context, dedu-
plicate effort, and track task progression with bounded
staleness guarantees.
4) It articulates a Scalability and Fault Tolerance model
that supports dynamic agent join, scale, and departure
events, ensuring operational continuity through state
replication, redundant assignment, and adaptive role
reassignment.
5) It identifies the structural invariants and protocol proper-
ties that future implementations must preserve in order
to retain the architecture’s generality and resilience.
D. Conceptual Framework
The proposed architecture conceptualizes a swarm as a
dynamic graph of autonomous agents, each exposing a de-
clared capability profile and maintaining a local view of shared
task state. Three logical planes structure the design. The task
plane governs the lifecycle of goals and sub-tasks, including
decomposition, advertisement, bidding, execution, and result
integration. The state plane maintains the eventually consistent
shared context that enables agents to reason about ongoing
work, completed sub-tasks, and outstanding dependencies. The
membership plane tracks the evolving composition of the
swarm and reallocates responsibilities in response to join,
departure, and failure events. The three planes interact through
well-defined interfaces but operate independently, allowing
each to evolve without disrupting the others.
A central design commitment is the strict separation be-
tween the coordination substrate, which is task-agnostic,
and the agent reasoning logic, which may be specialized
to particular domains or tool ecosystems. This separation
is intended to enable the same swarm framework to host
agents engaged in disparate cooperative activities—such as
collaborative research, code synthesis, or document analysis—
without modification to its underlying protocols.
E. Organization of the Paper
The remainder of this paper is organized as follows. Sec-
tion II surveys related work on multi-agent systems, swarm
intelligence, and distributed coordination protocols. Section III
formalizes the system model, including agent abstractions, task
representations, and assumed network conditions. Section IV
presents the methodology and Section V elaborates the system
architecture in detail. Section VI analyzes the architecture’s
properties, including scalability characteristics, consistency
guarantees, and failure-mode behavior. Section VII discusses
limitations and open challenges. Section VIII concludes the
paper and outlines directions for future work.
II. RELATED WORK
A. Multi-Agent LLM Frameworks
Contemporary multi-agent frameworks for large language
models, such as those exemplified by orchestrator–worker
patterns and role-based collaboration paradigms, have estab-
lished the practical viability of agent collectives for complex
reasoning tasks. These systems, however, generally rely on a
designated planning agent or static role hierarchy that mediates
inter-agent communication. While effective at modest scale,
such designs concentrate coordination authority in a single
component and tightly couple control flow to task-specific
prompt engineering.
B. Classical Multi-Agent Systems
The multi-agent systems (MAS) literature has long stud-
ied coordination mechanisms in the absence of central con-
trol. The Contract Net Protocol, originally proposed for dis-
tributed problem solving, established the announce–bid–award
paradigm that underlies many modern allocation schemes.
Belief–desire–intention (BDI) architectures and joint-intention
theory provided formal grounding for cooperative behavior.
The present work draws conceptually on these foundations
while adapting them to the operational characteristics of LLM-
based reasoning agents, whose capabilities are probabilistic,
context-dependent, and dynamically self-describable.
C. Swarm Intelligence and Stigmergy
Swarm intelligence research, including ant colony optimiza-
tion, particle swarm optimization, and stigmergic coordination,
has demonstrated that complex global behavior can emerge
from simple local interactions among large populations of ho-
mogeneous agents. While agentic AI introduces heterogeneity
and richer per-agent reasoning, the design principles of swarm
systems—locality of interaction, redundancy, and emergent
global properties—inform the architectural decisions presented
in this paper.
D. Distributed Systems Foundations
The proposed architecture builds upon well-established re-
sults from distributed systems research. Gossip (epidemic)
protocols provide probabilistic dissemination guarantees with
bounded message overhead. Conflict-free replicated data types
(CRDTs) enable eventually consistent shared state without

coordination. Consensus protocols such as Raft and Paxos
offer strong agreement guarantees when required for critical
commitment points. Distributed hash tables (DHTs), exempli-
fied by Kademlia and Chord, provide scalable peer discovery
and routing. The novelty of the present contribution lies not
in any individual primitive, but in their composition into a
coherent coordination substrate suited to the unique demands
of agentic AI.
III. SYSTEM MODEL AND ASSUMPTIONS
A. Agent Abstraction
Let A = {a1, a2, . . . , an} denote the set of agents currently
participating in the swarm. Each agent ai is characterized by
the tuple
ai = ⟨idi, Ci, Li, Si, κi⟩,
(1)
where idi is a globally unique identifier, Ci is the agent’s
capability profile, Li ∈[0, 1] is its current normalized load,
Si is its local state replica, and κi ∈[0, 1] is a reputation score
derived from the historical quality of its contributions.
The capability profile Ci is a structured descriptor express-
ing the classes of sub-tasks the agent can execute, together
with parametric attributes such as supported tool integrations,
modality, and estimated competence. Capabilities are self-
declared but verifiable: contributions are evaluated by peer
agents, and persistent misrepresentation degrades κi, reducing
the agent’s likelihood of future awards.
B. Task Representation
A goal G submitted to the swarm is represented as an
abstract task descriptor that does not presuppose a particular
decomposition. During execution, G is dynamically expanded
into a directed acyclic graph (DAG) T = (V, E), where each
vertex t ∈V is a sub-task and each edge (tj, tk) ∈E encodes
a dependency in which tk requires the output of tj. Each sub-
task is described by
t = ⟨idt, ρt, δt, πt, σt⟩,
(2)
where ρt is the required capability descriptor, δt is the set of
dependency identifiers, πt specifies the acceptance predicate
(the conditions under which a result is considered valid).
C. Network Model
The swarm is assumed to operate over an asynchronous,
partially synchronous network in which messages may be de-
layed, reordered, or dropped, but are not arbitrarily corrupted
(a non-Byzantine failure model is adopted in the baseline;
Byzantine extensions are discussed in Section VII). Agents are
connected via a structured peer-to-peer overlay that supports
logarithmic-cost lookup and neighborhood maintenance. The
membership of A is dynamic: agents may join or depart at any
time, and failures are modeled as silent departures detected
through heartbeat timeouts.
IV. METHODOLOGY
A. Design Principles
The methodology underpinning the architecture is governed
by five principles, each motivated by the limitations of cen-
tralized agent frameworks identified in Section II:
1) Locality of decision. No agent requires a global view of
the swarm to make valid local progress. Decisions are
made on partial, possibly stale, but eventually consistent
state.
2) Protocol–semantics separation. The coordination pro-
tocols operate uniformly over opaque task descriptors.
Domain semantics reside exclusively within agent rea-
soning modules.
3) Redundancy by default. Critical state is replicated and
critical sub-tasks may be assigned redundantly. Single-
instance components are avoided wherever feasible.
4) Graceful
degradation.
The
architecture
maintains
progress, possibly at reduced throughput, under partial
failure, partition, or sudden membership change.
5) Composable primitives. Each subsystem is built from
standard distributed-systems primitives whose properties
are well understood, enabling formal reasoning about
composite behavior.
B. Coordination Substrate Overview
The methodology realizes the three planes introduced in
Section I-D as follows. The task plane is implemented through
a Contract Net-inspired allocation protocol enriched with ca-
pability scoring and load awareness. The state plane is imple-
mented through a gossip-based dissemination layer supporting
CRDT-encoded shared structures, with optional escalation
to lightweight consensus for irreversible commitments. The
membership plane is implemented through a structured peer-
to-peer overlay augmented by a SWIM-style failure detector.
The remainder of this section formalizes each subsystem.
C. Dynamic Task Decomposition and Allocation
1) Recursive Decomposition: When a goal G is admitted
to the swarm, it is initially held by an arbitrary agent ai
designated as its temporary root holder—an assignment that
confers no special authority beyond responsibility for initiating
decomposition. The root holder applies a domain-appropriate
decomposition function D : G 7→{t1, . . . , tm} implemented
within its reasoning module. The resulting sub-tasks, together
with their dependency edges, are inserted into the shared task
DAG and propagated through the state plane.
Decomposition is recursive: any sub-task t may itself be
further decomposed by the agent to which it is eventually
assigned, producing a hierarchy of refinements. This permits
the swarm to begin work on tractable sub-tasks while more
abstract sub-tasks are still being broken down, supporting
pipelined progress.

2) Capability-Aware Bidding: For each sub-task t entering
status PENDING, the holder publishes a task announcement
to the overlay neighborhood relevant to ρt, exploiting the
structured topology to direct announcements toward agents
whose capability profiles are likely matches. Eligible agents
respond with bids of the form
bi,t = ⟨idi, ui,t, ei,t⟩,
(3)
where ui,t is the agent’s self-estimated utility for executing
t and ei,t is its estimated time-to-completion. Utility is com-
puted as
ui,t = α · cap(Ci, ρt) + β · (1 −Li) + γ · κi,
(4)
where cap(·, ·) is a capability-match score in [0, 1], and α, β, γ
are tunable weights satisfying α + β + γ = 1. The functional
form of cap(·, ·) is task-agnostic at the protocol level: it
operates on opaque descriptors interpreted by agent reasoning
modules.
3) Award and Conflict Resolution: After a bounded bidding
window, the holder selects the highest-utility bidder. To avoid
pathological concentration of work and to mitigate adversarial
bidding, the protocol incorporates a tempered selection rule:
with probability 1 −ϵ, the highest-utility bidder is selected;
with probability ϵ, selection is performed by softmax sampling
over the top-k bids. Ties and conflicting concurrent awards
are resolved using deterministic agent identifiers, ensuring
that even in the presence of message reordering, the swarm
converges to a unique assignment for each sub-task.
For sub-tasks marked critical (e.g., those on which many
downstream tasks depend), redundant assignment is permitted:
the top-r bidders execute the sub-task in parallel, and results
are reconciled by the acceptance predicate πt. This trades
computational cost for resilience and is configurable on a per-
task basis.
D. Decentralized State Synchronization
1) Shared State Schema: The shared state S maintained
across the swarm comprises three principal structures:
• The task DAG T, encoding sub-tasks, dependencies, and
statuses.
• The result store R, mapping completed sub-task identi-
fiers to their outputs.
• The membership view M, listing currently known agents
and their capability profiles.
Each structure is encoded as a CRDT chosen for its operational
characteristics: T employs an OR-Set for vertex membership
combined with a last-writer-wins register for status fields; R
uses a grow-only map (G-Map) since results, once written,
are immutable; M uses a delta-state CRDT to bound metadata
overhead under churn.
2) Gossip Dissemination: State updates are propagated via
an anti-entropy gossip protocol. At each gossip interval τ, an
agent selects a fixed-fan-out subset of overlay neighbors and
exchanges CRDT delta states. Under standard assumptions,
gossip dissemination converges in O(log n) rounds with high
probability, providing bounded staleness without central co-
ordination. Each agent maintains a vector clock that is used
to detect concurrent updates and to bound the age of locally
observed state, enabling agents to defer decisions when their
view is detected to be unacceptably stale.
3) Avoiding Redundant Work: The combination of CRDT-
encoded task statuses and timely gossip dissemination is the
primary mechanism by which redundant work is avoided. Be-
fore initiating execution, an agent verifies that σt is ASSIGNED
to itself in its local replica and that no concurrent assignment
has been observed within a synchronization window. When
concurrent assignments are detected—which may occur tran-
siently under partition—the deterministic conflict-resolution
rule of Section IV-C ensures that, post-merge, a single agent
retains responsibility, while the others release their claims.
4) Selective Strong Consistency: Most coordination oper-
ates under eventual consistency, which is sufficient for the
bulk of task progression. However, certain transitions—most
notably the marking of a goal as completed and the release of
dependent downstream computations—benefit from stronger
guarantees. For these commitment points, the architecture
invokes a lightweight Raft-style consensus among a small quo-
rum of agents drawn from the relevant overlay neighborhood.
The consensus group is ephemeral, formed on demand, and
dissolved after the commitment is recorded in T.
E. Scalability and Fault Tolerance
1) Membership Dynamics: Agent join, departure, and fail-
ure are handled by the membership plane. A joining agent
contacts a small set of bootstrap peers, retrieves the current
membership view via gossip, and announces its capability
profile. A departing agent issues a graceful-leave message,
allowing its outstanding assignments to be released cleanly.
Failures are detected by a SWIM-style protocol in which
agents periodically probe random peers; suspected failures are
gossiped to the swarm and confirmed through indirect probes
before being committed to M.
2) Reassignment under Failure: When an agent ai fails or
departs while holding assignments, its outstanding sub-tasks
must be reassigned. The swarm identifies orphaned sub-tasks
by inspecting the task DAG for entries whose assignee is
no longer in the membership view. Each orphan is returned
to the bidding pool with its status reset to PENDING, and
the allocation protocol of Section IV-C is reinvoked. To
bound the reassignment latency, a bounded number of shadow
agents may be designated at award time as standby executors;
should the primary assignee fail, a shadow agent assumes the
assignment without a fresh bidding round.
3) Elastic Scaling: The architecture supports elastic scaling
in two senses. First, the swarm may grow without protocol
modification: the structured overlay accommodates new agents
at logarithmic routing cost, and the gossip and CRDT layers
scale gracefully with n. Second, individual agents may scale
their internal computational resources without disrupting the
swarm, since capability profiles and load reports are contin-

uously updated through gossip and consumed by the bidding
protocol on the next cycle.
V. SYSTEM ARCHITECTURE
A. Layered Architecture
The software architecture is organized into five layers,
ordered from network substrate to agent reasoning:
1) Transport Layer. Handles authenticated, encrypted point-
to-point messaging between agents over the underlying
transport (e.g., QUIC or TLS-secured TCP). Provides
ordered delivery within a single connection and connec-
tion multiplexing.
2) Overlay Layer. Implements the structured peer-to-peer
topology, providing peer discovery, routing, and neigh-
borhood maintenance. Exposes primitives for unicast,
multicast within a neighborhood, and capability-targeted
dissemination.
3) State Synchronization Layer. Hosts the CRDT-encoded
shared structures and the gossip dissemination engine,
as elaborated in Section IV-D.
4) Coordination Layer. Implements the task allocation pro-
tocol, the membership and failure-detection protocols,
and the on-demand consensus subsystem. Exposes high-
level operations for goal submission, sub-task announce-
ment, bidding, award, and result publication.
5) Agent Reasoning Layer. Encapsulates the domain-
specific reasoning logic of each agent, including its
decomposition function, capability evaluation, execution
behavior, and acceptance-predicate verification. Com-
municates exclusively through interfaces exposed by the
coordination layer.
The strict layering ensures that domain semantics never leak
into the lower layers, preserving task-agnosticism. Conversely,
the upper reasoning layer remains insulated from the network
substrate, allowing reasoning modules to be developed and
replaced independently.
B. Internal Agent Components
Within each agent, the runtime decomposes into the fol-
lowing components: a coordination client maintaining local
CRDT replicas and gossip state; a bidding engine computing
utilities and submitting bids; a task executor dispatching
accepted assignments to the reasoning layer; a state observer
continuously monitoring the local replica of T, R, and M
to detect actionable events; and a health monitor maintaining
heartbeats and producing load reports.
C. Goal Lifecycle
A complete goal lifecycle proceeds as follows. A user
or external system submits goal G to any agent ai, which
becomes the root holder. The agent invokes its decompo-
sition function, producing initial sub-tasks that are inserted
into T and gossiped through the state plane. Eligible agents
observe the new sub-tasks via their state observers and submit
bids; the holder of each sub-task awards it to the selected
bidder. Awarded agents execute their sub-tasks, recursively
decomposing as needed, and upon completion publish results
into R and update σt to COMPLETED. Downstream sub-tasks
whose dependencies are satisfied transition from PENDING to
BIDDING. The cycle continues until the root sub-task of G
reaches COMPLETED, at which point an on-demand consensus
quorum confirms goal completion and the result is delivered
to the original submitter.
D. Architectural Invariants
For correctness, the architecture maintains the following
invariants:
• Eventual assignment uniqueness. For every sub-task t, in
the absence of further membership changes affecting t,
the swarm converges to a state in which exactly one non-
failed agent holds the assignment.
• Result immutability. Once a sub-task transitions to COM-
PLETED with a value in R, that value is not subsequently
overwritten by the protocol.
• Dependency safety. A sub-task does not enter EXECUT-
ING unless all its dependencies are observed as COM-
PLETED in the local replica.
• Membership convergence. The membership view M con-
verges to reflect the true set of live agents within bounded
gossip latency under stable membership.
These invariants are preserved by the composition of the
underlying primitives—CRDT semantics for state, determin-
istic conflict resolution for assignments, and consensus for
commitment points—and constitute the formal contract that
the architecture offers to higher-level reasoning modules.
VI. ANALYSIS
A. Scalability Characteristics
The scalability of the architecture is governed by the cost
of its dominant operations. Peer lookup and routing in the
structured overlay incur O(log n) message complexity. Gossip
dissemination converges in O(log n) rounds with constant
per-round message overhead per agent, yielding O(n log n)
aggregate messages per dissemination cycle. CRDT merge
operations are O(|∆|) in the size of the delta state, which
is bounded by recent activity rather than total state size.
Allocation overhead per sub-task is O(k) in the number
of solicited bidders, which is configurable and independent
of n. The composition therefore admits sub-linear per-agent
overhead with respect to swarm size, supporting growth into
the thousands of agents under realistic message budgets.
B. Consistency Guarantees
The architecture provides eventual consistency for routine
state, with bounded staleness determined by the gossip pe-
riod τ and fan-out. Critical commitments—goal completion
and certain irreversible state transitions—are protected by
lightweight consensus, providing linearizability at those points.
This layered consistency model matches the operational profile
of agentic workloads, in which most progress is monotonic
and tolerant of brief inconsistency, while a small number of
decisions warrant stronger guarantees.

C. Fault-Tolerance Properties
Under non-Byzantine failure assumptions, the architecture
tolerates the simultaneous failure of any minority of agents in
the consensus quorum and any number of agents in the broader
swarm, provided the overlay remains connected. Orphaned
sub-tasks are reassigned within a bounded latency determined
by failure-detection timeouts and the duration of a fresh
bidding round, or instantaneously for sub-tasks protected by
shadow agents. Network partitions are handled by allowing
each partition to make local progress on independent sub-
tasks; upon healing, CRDT merges reconcile divergent states,
and any conflicting assignments are resolved deterministically.
D. Generality
Because the coordination substrate operates on opaque
task descriptors and capability profiles, the same architec-
ture supports a broad range of cooperative workloads—
collaborative research, distributed code synthesis, document
analysis, knowledge graph construction—without modifica-
tion. Specialization is achieved exclusively through the agent
reasoning layer, satisfying the task-agnosticism requirement
stated in Section I-B.
VII. DISCUSSION
A. Limitations
Several limitations attend the present architectural proposal.
First, the baseline assumes non-Byzantine failures; extend-
ing the architecture to tolerate Byzantine agents—particularly
relevant in open swarms admitting untrusted participants—
requires Byzantine fault-tolerant consensus and verifiable com-
putation, both of which incur substantial overhead. Second,
the utility function in Eq. 4 assumes that capability matching
can be reduced to a scalar score; richer multi-dimensional
matching may be required for highly heterogeneous swarms.
Third, the architecture as described does not address economic
incentives for participation in open agent markets, which is an
important direction for future work.
B. Open Challenges
Several challenges remain open. The decomposition func-
tion D is left to the agent reasoning layer, and the quality of
decomposition strongly affects swarm efficiency; principled,
learning-based decomposition strategies warrant investigation.
The interaction between gossip parameters, CRDT delta sizes,
and bidding latencies admits optimization that has not been
characterized in this paper. Empirical validation through large-
scale simulation, including realistic latency and failure models,
is required to substantiate the analytical claims of Section VI.
C. Implementation Pathway
A reference implementation following the architecture
would profitably build upon mature open-source components:
an existing structured overlay library for the overlay layer, a
CRDT library for the state layer, and a Raft implementation for
the on-demand consensus subsystem. The novel components
requiring implementation are the coordination layer and the
agent reasoning interfaces. This modular approach reduces
engineering risk and enables incremental validation.
VIII. CONCLUSION
This paper has proposed a generalized, task-agnostic soft-
ware architecture for swarm agentic AI in which heteroge-
neous autonomous agents collaborate through fully decentral-
ized coordination mechanisms. By organizing the system into
task, state, and membership planes, and by composing well-
understood distributed-systems primitives—structured peer-to-
peer overlays, gossip dissemination, conflict-free replicated
data types, and on-demand lightweight consensus—the archi-
tecture addresses the joint requirements of task-agnosticism,
decentralization, and operational resilience that contemporary
multi-agent frameworks satisfy only partially. Dynamic task
decomposition and capability-aware bidding distribute work
across the swarm without central scheduling; CRDT-based
state synchronization with gossip dissemination maintains a
coherent shared context with bounded staleness; and SWIM-
style failure detection combined with adaptive reassignment
preserves operational continuity under churn and partial fail-
ure. The strict separation between the coordination substrate
and the agent reasoning layer enables the same framework to
host disparate cooperative workloads without protocol modi-
fication.
Future work will pursue empirical validation through large-
scale simulation, characterize the parameter space of gossip
and bidding configurations, extend the architecture to Byzan-
tine failure models, and investigate learning-based decompo-
sition strategies. The contribution presented here is intended
as a reference design upon which such investigations can be
grounded, advancing the development of resilient, large-scale
agentic AI ecosystems.
REFERENCES
[1] R. G. Smith, “The contract net protocol: High-level communication and
control in a distributed problem solver,” IEEE Trans. Comput., vol. C-29,
no. 12, pp. 1104–1113, 1980.
[2] A. S. Rao and M. P. Georgeff, “BDI agents: From theory to practice,”
in Proc. 1st Int. Conf. Multi-Agent Systems, 1995, pp. 312–319.
[3] M. Dorigo, M. Birattari, and T. St¨utzle, “Ant colony optimization,” IEEE
Comput. Intell. Mag., vol. 1, no. 4, pp. 28–39, 2006.
[4] A. Demers et al., “Epidemic algorithms for replicated database mainte-
nance,” in Proc. 6th ACM Symp. Principles of Distributed Computing,
1987, pp. 1–12.
[5] M. Shapiro, N. Preguic¸a, C. Baquero, and M. Zawirski, “Conflict-free
replicated data types,” in Proc. Symp. Self-Stabilizing Systems, 2011, pp.
386–400.
[6] D. Ongaro and J. Ousterhout, “In search of an understandable consensus
algorithm,” in Proc. USENIX Annu. Tech. Conf., 2014, pp. 305–319.
[7] L. Lamport, “The part-time parliament,” ACM Trans. Comput. Syst., vol.
16, no. 2, pp. 133–169, 1998.
[8] P. Maymounkov and D. Mazi`eres, “Kademlia: A peer-to-peer informa-
tion system based on the XOR metric,” in Proc. Int. Workshop Peer-to-
Peer Systems, 2002, pp. 53–65.
[9] I. Stoica et al., “Chord: A scalable peer-to-peer lookup service for
internet applications,” in Proc. ACM SIGCOMM, 2001, pp. 149–160.
[10] A. Das, I. Gupta, and A. Motivala, “SWIM: Scalable weakly-consistent
infection-style process group membership protocol,” in Proc. Int. Conf.
Dependable Systems and Networks, 2002, pp. 303–312.
[11] M. Wooldridge, An Introduction to MultiAgent Systems, 2nd ed. Chich-
ester, U.K.: Wiley, 2009.

[12] P. R. Cohen and H. J. Levesque, “Intention is choice with commitment,”
Artif. Intell., vol. 42, no. 2–3, pp. 213–261, 1990.
