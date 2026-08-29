# State and ledgers

The state directory is project-local and optional. It lets a later session
resume the model instead of rereading thousands of lines or trusting a chat
summary. Keep it beside the project or in a user-approved working directory;
do not put unpublished material in a shared/external service by default.

## Layout

```text
.research-co-thinking/
├── profile.yaml             # stable reader/background preferences
├── session.yaml             # current goal and last handoff
├── concepts.yaml            # terms, objects, relations, knowledge state
├── symbols.yaml             # glyph/type/scope/declaration ledger
├── claims.yaml              # claim modality, boundary, support
├── evidence.yaml            # proofs, runs, traces, citations, limitations
├── source-map.yaml           # source artifacts and authoritative roles
├── decisions.yaml           # accepted, rejected, and deferred branches
├── impact.yaml               # optional reverse/dependency index
└── handoffs/                 # dated, short human-readable checkpoints
```

JSON is also acceptable when tooling or version control makes it safer. YAML
examples in this reference are illustrative schemas, not a demand to convert
an existing repository. Keep entries small and link to source locators rather
than copying whole documents.

## Stable profile versus session context

`profile.yaml` stores only durable preferences that improve explanations:

```yaml
reader:
  known: [probability, functional-analysis, transformer-basics]
  likely_known: [standard-optimization]
  domain_gaps: [project-local-routing-terms]
  notation_tolerance: dense
  preferred_representation: equation-plus-running-example
  evidence_expectation: proof-and-reproducible-run
  language: zh
```

Do not record sensitive personality judgements or infer permanent mastery.
`session.yaml` is short-lived and task-specific:

```yaml
session_id: 2026-08-29-routing
mode: co-think
goal: "decide whether the selector assumption is needed"
source_of_truth: [claims.yaml, concepts.yaml, "docs/foo.md"]
confirmed: [C-route-boundary, D-selector-scope]
tentative: [T-frontier-meaning]
blocked_by: [E-selector-proof]
introduced_terms: [pointer-chasing]
next_move: "compare oracle and affine-scan cases"
last_updated: 2026-08-29T12:00:00+08:00
```

At session start, read `session.yaml`, unresolved/high-impact ledger entries,
and the source map. Read the full source only when a linked node is stale or a
local proof/implementation detail is needed.

## Ledger invariants

Use stable IDs and append history rather than rewriting provenance. At minimum:

- every `symbol` has a nonempty declaration locator and one scope;
- every `claim` has a modality, boundary (or explicit `none`), and status;
- every `supported`/`bounded` claim names at least one evidence or qualifying
  assumption;
- every evidence item names an artifact and its conditions/limitations;
- every decision records the options considered and whether it is reversible;
- aliases point to a canonical term and are not silently treated as synonyms;
- links to source files remain relative where possible and are checked for
  existence before a handoff is marked reproducible.

The basic checker can report violations, but it cannot establish mathematical
truth, semantic equivalence, or whether a proof really follows. Human review
is required for those questions.

## Source roles

Classify each source artifact with one role:

```yaml
- id: A-foundations
  path: ../ObsidianVault/20-tide-decentralized-neural-network/tide-mathematical-foundations.md
  role: authoritative-semantics | explanatory-example | implementation |
        experiment-record | historical-motivation | process-log | output-view
  authority: canonical | provisional | historical
  last_checked: 2026-08-29
```

If two sources disagree, preserve both, create a conflict/risk node, and ask
which one becomes canonical. Do not resolve the conflict by whichever file was
read last.

## Handoff format

A handoff should be short enough to scan in under a minute:

```markdown
## Handoff — <date>
- Goal:
- Confirmed (IDs):
- Still open / blocked (IDs):
- New terms and knowledge states:
- Sources inspected:
- Semantic changes made:
- Next smallest move:
- Questions for the author:
```

If no semantic change occurred, say so. A polished paragraph without a model or
decision update is not a complete handoff.

## Cross-session and branch safety

When a new session proposes a change, compare its node IDs and source hashes (if
available) with the last handoff. If a source changed underneath the ledger,
mark dependent entries `revisit` rather than assuming the old interpretation
still holds. For parallel branches, use namespaced decision IDs and merge only
after checking contradictory assumptions.

