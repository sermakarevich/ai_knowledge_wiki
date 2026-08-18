## Figure: agent-graph-starter-diagram.png

Source-provided alt text (used directly — sufficiently detailed, no vision-model call needed):

The starter agent graph: a task enters a Researcher node that gathers sources and writes notes,
which passes state `{task, notes}` down to a Writer node that turns notes into a draft, which
passes state `{task, notes, draft}` to a Reviewer node that scores the draft against the bar. A
solid conditional edge labelled "pass" routes to Ship; a dashed edge labelled "reject: loop back"
routes back to the Writer. Nodes are the specialists, edges are the routing, and state is the
object that grows as it flows.
