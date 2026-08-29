# Exposition for neural-network and LLM research

Neural-network documents often become hard to read because one name is used for
an abstract function, a parameterized model, a runtime component, and an
experiment. Keep those layers separate before choosing prose or diagrams.

## Four layers that must not be conflated

| Layer | Question | Typical artifact | Safe claim form |
| --- | --- | --- | --- |
| architecture | what components and connections are designed? | block/graph diagram, interface contract | “the proposed architecture has …” |
| model semantics | what function/state transition is defined? | equations, types, invariants | “for input/state … the model computes …” |
| realization/engine | how is it implemented and scheduled? | code, kernel, memory/communication plan | “implementation X realizes … under …” |
| experiment | what was actually run and measured? | config, trace, table, checkpoint | “run R measured …” |

An architecture diagram does not establish a mathematical property; a reference
implementation does not establish that every implementation has the property;
one run does not establish a model-wide guarantee. Link claims across layers
explicitly (`implements`, `instantiates`, `supports`, `qualifies`).

## Type boundary table

Use a type-and-scope table early in a document. The following distinctions are
especially useful for routing, stateful modules, and LLM systems:

| Term | Declare as | Do not silently treat as |
| --- | --- | --- |
| token | input symbol/ID at position (t) | hidden vector, event, or node |
| position/index | element of an index set | a token's identity or execution time |
| hidden/representation | vector in a stated space | probability, message, or persistent state |
| value/message | data sent across a declared edge/interface | a node or an address |
| node/module | parameterized computation with inputs/outputs | one activation or one event |
| event/execution step | occurrence in a schedule with time/order | a static graph vertex |
| state | persistent data with lifetime and update rule | a transient hidden or cache line |
| address/key | element used to select storage or a receiver | semantic content or graph node itself |
| selector/router | function producing a choice/set and its domain | the selected computation |
| support/reached set | candidates with an actual message/input | active/committed set unless defined |
| frontier | a defined cut/ready set in one graph or schedule | a universal notion of context length |
| model | mathematical/parameterized mapping plus state semantics | serving engine or checkpoint directory |
| engine/runtime | scheduler, kernels, memory, communication, device policy | the abstract function |
| experiment | fixed run/configuration and measurements | a general theorem or architecture definition |

The project may intentionally use a different meaning, but then add a local
term card and scope it. If a word such as “frontier”, “state”, or “node” has two
legitimate meanings, use qualified names (`routing-frontier`,
`execution-frontier`) until the author chooses an identity.

## A useful semantic ladder

For each new mechanism, write the smallest complete ladder:

```text
design intent
→ abstract object and input/output types
→ transition/order and state lifetime
→ implementation correspondence
→ predicted consequence or proof obligation
→ experiment and measurement protocol
→ observed result and boundary
```

Do not jump from a motivation such as “reduce communication” to a named
architecture. State which quantity is reduced, relative to which baseline, and
what correctness or quality is preserved. If an item is still an option, use
conditional language and create a `decision` node only after confirmation.

## Routing and graph modules

For a graph-routed module, introduce these objects in dependency order:

1. static topology (vertices/ports/edges and allowed messages);
2. per-token/per-step input and state domains;
3. reached candidates (what received a message);
4. selector score and active/commit policy;
5. node computation and emitted message;
6. external boundary/residual merge;
7. schedule and runtime realization.

A compact execution trace is often clearer than a second taxonomy:

```text
input hidden → fixed edge delivery → aggregate
→ selector read/choice → state update (if any)
→ active node compute → emit → next step/output
```

Mark which arrows are semantic requirements and which are one implementation's
ordering. For lower bounds or impossibility arguments, state the oracle/query
model, exactness requirement, work budget, and allowed algebraic structure;
“adaptive routing” alone is too broad to support a conclusion.

## Transformer and LLM interfaces

When discussing a base Transformer or LLM, state the boundary at which the new
module attaches. A reader should be able to answer:

- which hidden enters and leaves the module;
- whether attention/MLP sees the modified value;
- whether the module has token-local or cross-token state;
- when state is read, proposed, committed, and reset;
- whether training-only paths (for example balance losses) affect inference;
- what prefill/decode schedule and cache assumptions apply.

Use a placement table or one worked token trace before discussing performance.
Do not infer runtime parallelism from a dataflow drawing without declaring the
schedule and address-dependency model.

## Adapting difficult existing project documents

Treat existing TIDE/GraphBranch, mathematical-foundations, and fractal-latcarf
documents as semantic sources to classify, not as prose to imitate wholesale.
Extract:

1. a one-page map of research question, main objects, and strategic branches;
2. a glossary separating standard terms from project-local terms;
3. an interface/type ledger (for example placement, port, receiver, state,
   selector, emit policy);
4. a claim/evidence/status ledger;
5. a chronology or experiment ledger kept outside the conceptual mainline.

When rewriting, preserve formulas and names first, then repair the reader route:
split a paragraph that changes semantic lanes, insert the smallest missing
bridge, and move protocol/history details to linked sections. Explicitly label
which statements describe target semantics and which describe the current
implementation or an unverified default.

## Exposition checks specific to NN/LLM work

Before presenting a result, ask:

- Is the object a function, a state machine, a graph, a kernel, or a run?
- Are dimensions, index ranges, batch/token axes, and reset boundaries stated?
- Does “can”, “typically”, “is”, or “guarantees” match the evidence status?
- Could a reader reproduce the claimed comparison from the protocol?
- Does the diagram show static edges and dynamic choices differently?
- Is a new acronym earning its cost, and is its first use locally explained?

If any answer is unknown, record an open obligation instead of filling the gap
with confident-sounding prose.

