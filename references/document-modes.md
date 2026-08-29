# Document modes

Choose a document mode before drafting a long passage. The mode is a contract
with a reader, not a permanent label on the source. A single project can keep a
private context note, a formal specification, and a paper that point to the
same canonical nodes.

## Mode table

| Mode | Reader's job | Required spine | Keep visible |
| --- | --- | --- | --- |
| `personal-notes` | resume thinking and choose the next move | question → current model → open branches → next action | raw intent, uncertainty, rejected paths |
| `self-context-reload` | recover a cold project after time away | why → one-page map → what changed → definitions → unresolved obligations | dates/versions, source map, decision history |
| `explanatory-guide` | learn one idea and use it on a small case | phenomenon → minimal example → definition → consequence → boundary → optional depth | prerequisite bridges, glossary, checks |
| `formal-spec` | implement or review an unambiguous contract | scope/types → inputs/outputs → state/order → invariants → errors → examples | domains, quantifiers, version and non-goals |
| `proof` | verify a mathematical statement | definitions → assumptions → statement → proof → corollaries/counterexamples | dependency order and proof status |
| `paper` | assess novelty, validity, and relevance | problem/gap → method → analysis → evidence → limits/related work | claim modality, comparison protocol, reproducibility |
| `protocol` | reproduce an experiment or operation | objective → variables → procedure → measurements → stopping/analysis rules | exact configuration, seeds, failure handling |
| `ledger` | audit state rather than read a narrative | entry schema → status → owner/source → next check | unknowns and stale entries |

If the user says “帮我写一篇文档” without specifying a mode, ask what the
reader must be able to do afterward. For the author's own understanding,
default to `personal-notes` or `self-context-reload`, not `paper`.

## Contracts by mode

### Personal notes and cold reload

Personal notes are allowed to be provisional and densely linked, but each block
must answer “why is this here?” Keep two columns or labels where useful:
`raw-intent` (the author's words) and `working-formulation` (Codex's current
interpretation). Mark open choices instead of smoothing them away.

A cold-reload page should fit a short first screen containing:

```text
one-sentence aim
current best answer (or explicit “not known”)
map of 3–7 major objects/sections
what changed since the previous checkpoint
next decision and blocked obligations
```

Only then reopen detailed derivations. Link each major object to its first
definition and source artifact. A historical log can be retained, but it does
not replace the current model.

### Explanatory guide

Use progressive disclosure. A section should introduce no more than the
objects needed for its next inference. Place a small running example before a
general abstraction when the audience is mixed; place a formal anchor next to
the intuition rather than many pages later. End a section with a bounded
takeaway and a boundary/non-example. Use a term card for imported vocabulary;
do not make the reader infer whether a project-local name is standard.

### Formal specification and proof

Declare sets, spaces, types, domains, index conventions, state lifetime, and
evaluation order before using them. State whether an item is a definition,
invariant, theorem, implementation requirement, or recommendation. For a proof,
separate intuition from the formal proof and name every lemma used. If a proof
uses a result from another file, link the exact statement and assumptions;
“as usual” is not a dependency declaration.

### Paper

The paper is an argument, not a chronological dump of the research process.
Select a claim spine:

```text
problem and stakes → precise gap → contribution (with modality)
→ method/object → analysis or design rationale → evidence
→ limitations, scope, and what is not shown
```

A contribution list must map one-to-one to claims in the body and evidence in
figures, tables, proofs, or citations. Preserve failed experiments and caveats
when they change interpretation. Keep implementation details that affect
reproducibility; move merely navigational detail to an appendix or linked
artifact.

### Protocol and ledger

A protocol fixes variables before results are inspected: data split, model
configuration, seed policy, metrics, baseline, budget, and stopping rule.
The ledger records whether each item is planned, running, checked, failed, or
stale. Neither document should claim significance or causality without a
predeclared comparison and an explicit limitation.

## Layered page pattern

For long material, use layers rather than one undifferentiated page:

1. **Orientation:** purpose, audience, prerequisites, map, and one-sentence
   answer.
2. **Mainline:** the minimum definitions and steps needed to follow the central
   argument.
3. **Deepening:** derivations, alternatives, implementation details, and
   counterexamples, each linked to the mainline node it expands.
4. **Audit layer:** symbol/term table, claim-evidence ledger, open questions,
   source map, and change history.

The first three layers can be rendered for a reader; the audit layer keeps the
author and future collaborators honest. Do not hide an essential assumption in
the audit layer.

## Section contract

Before writing a nontrivial section, record a compact contract:

```yaml
section_id: sec-routing-bound
mode: explanatory-guide
reader: self-now
purpose: "understand why the lower bound does not cover affine scans"
prerequisites: [term-pointer-chasing, object-transition]
introduces: [object-oracle, claim-bound]
answers: "what exact dependency is being ruled out?"
not_claiming: "all cross-token recurrence is sequential"
evidence: [E-proof-02]
next_section: sec-query-model
```

If `introduces` contains more than the reader can use before the next check,
split the section or add a deliberate bridge. A heading hierarchy is not a
dependency map; make both available when a page is long.

## Revision procedure

For a rewrite, first extract the existing spine and semantic inventory. Label
each proposed move as `move`, `bridge`, `split`, `merge`, `delete`, or
`wording-only`. Show any change to a quantifier, symbol binding, claim
modality, numerical value, or caveat as a semantic diff requiring confirmation.
After the rewrite, perform a cold-reader pass from the first heading without
using the drafting conversation.

