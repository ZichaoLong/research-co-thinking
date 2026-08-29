# Shared research model

The canonical research model is a small, typed graph that records what the
author means, what is only a proposal, and what is supported. It is the source
from which notes, papers, specifications, and slides are rendered. A document
may choose a different order or level of detail, but it must not silently
change the graph.

## Node kinds

Use the smallest kind that captures the role. A node can link to another node;
do not encode a relation merely in a paragraph when the relation affects a
later decision.

| Kind | Purpose | Minimum fields |
| --- | --- | --- |
| `question` | A question the work is trying to answer | wording, scope, status |
| `motivation` | Observation, need, or failure that makes the question useful | observation, source |
| `object` | Mathematical, conceptual, or engineering entity | name, type, domain/scope |
| `symbol` | A notation bound to one object in one scope | glyph, object, declaration |
| `assumption` | Condition under which a claim or design is intended | statement, scope |
| `mechanism` | Proposed or implemented transformation | inputs, outputs, steps |
| `alternative` | A materially different candidate interpretation/design | options, trade-off |
| `claim` | Statement whose strength and support can be assessed | statement, modality |
| `evidence` | Proof, derivation, trace, benchmark, citation, or observation | artifact, conditions |
| `decision` | Author-approved choice or explicit deferral | options, rationale |
| `risk` | A way the model or output can fail | trigger, consequence |
| `term` | Project-local name or imported technical term | canonical meaning, aliases |
| `artifact` | A source file, result table, implementation, or output view | path/locator, role |

`claim` is intentionally separate from `evidence`: a benchmark can support an
engineering claim under its measured conditions, but it does not by itself
support a universal theorem. `decision` is also separate from `claim`: choosing
an interface does not imply that it is optimal.

## Edges and fields

Prefer explicit, directed relations. Common edge types are:

| Edge | Reading |
| --- | --- |
| `motivates` | observation/question gives a reason for a node |
| `defines` / `uses` | a definition introduces, or a passage relies on, an object/term |
| `depends_on` | the target cannot be understood or derived before the source |
| `specializes` / `instantiates` | a general interface is given a concrete case |
| `implements` | code/runtime realizes a semantic mechanism |
| `supports` | evidence supports a bounded claim |
| `qualifies` | evidence or assumption limits a claim |
| `contradicts` | observation or result conflicts with a claim |
| `offers` / `selects` / `defers` | alternative is considered and a decision records the outcome |
| `supersedes` | a new definition or decision replaces an old one, with a reason |
| `appears_in` | node is rendered in a document, section, slide, or appendix |

Every node should carry a stable `id`, a human-readable `label`, a `kind`, and
one of the following statuses:

```yaml
status: draft        # captured but not yet checked
# or: proposed, confirmed, supported, bounded, disputed, rejected,
#     superseded, open, blocked
```

Use `scope` to say where the node is valid (`project`, `model-family`,
`implementation`, `experiment`, `section`, or a named configuration). Use
`impact: low|medium|high` for the cost of changing it. High-impact nodes
include public definitions, interfaces, theorem hypotheses, and quantities
used in several artifacts.

Claims should additionally record their modality and boundary:

```yaml
modality: definition | invariant | theorem | proposition | conjecture |
          design-intent | implementation-observation | empirical-result |
          interpretation
boundary: "under assumptions A and measured protocol P"
evidence_ids: [E-004]
```

Do not upgrade `design-intent`, `interpretation`, or `empirical-result` to a
theorem by changing prose alone. If the author's wording is ambiguous, keep a
`raw_text` field and create a tentative working formulation rather than
overwriting it.

## Symbols and terms

A symbol ledger entry binds a glyph to one object and scope:

```yaml
- id: S-x-l-t
  glyph: "x_{ell,t}"
  object_id: O-hidden-input
  scope: "base block ell, token t"
  declared_in: "doc.md#1.2"
  first_use: "doc.md#1.2"
  aliases: []
  status: confirmed
```

The same glyph in a different scope needs a different entry and an explicit
relationship. Do not resolve collisions by silently renaming the author's
notation. A term ledger should distinguish canonical names from aliases and
record whether an alias is deprecated. For every unfamiliar imported term,
link a local term card; an expansion of an acronym is not a definition of the
project's object.

## Evidence and provenance

An evidence entry states what was actually observed and under which conditions:

```yaml
- id: E-run-17
  kind: benchmark | proof | derivation | trace | citation | inspection
  artifact_id: A-run-17
  supports: [C-throughput]
  conditions: "commit abc; batch 4; sequence 4096; CUDA ..."
  result: "..."
  limitations: "..."
  reproducibility: recorded | partial | unknown
  status: draft | checked | failed
```

Record negative, failed, and missing evidence. A citation is provenance for a
statement in the cited source, not automatic evidence that the current system
has the same property. A proof obligation may be an open evidence node until
it is discharged.

## Canonical model and output views

Maintain one semantic identity across views:

```text
raw idea / source artifacts
          ↓ capture + typing
canonical model (nodes, edges, ledgers, decisions)
          ├─ self-now / self-cold note
          ├─ explanatory guide or formal specification
          ├─ paper / theorem-proof / experiment protocol
          └─ audience-specific slide deck + speaker notes
```

Each output view declares a `view_id`, selected node IDs, audience, purpose,
and omission policy. Omission is not deletion: an omitted proof or caveat must
remain reachable in a note, appendix, or ledger. When a view needs a stronger
claim than the model supports, stop at the boundary and ask for evidence or a
weaker formulation.

## Minimal model update

For an exploratory turn, do not build a complete knowledge graph. Add only:

1. the current question and the earliest blocking relation;
2. the one or two objects/terms needed for the next inference;
3. the user's correction or confirmation;
4. one consequence, test, or decision edge.

At handoff, list node IDs or stable labels changed in the turn. This makes a
later reload possible without replaying the entire chat.

## Change impact

When a node changes, traverse outgoing `depends_on`, `uses`, `supports`, and
`appears_in` edges. Report affected artifacts in descending impact. Separate:

- **semantic change** — definition, quantifier, interface, result, or status;
- **expository change** — order, example, diagram, or wording;
- **rendering change** — Markdown/LaTeX/PPTX formatting.

Only the first category requires author confirmation by default. Expository
repairs still need a reversible diff when they may alter emphasis or imply a
stronger result.

