# Quality gates

Quality means that a reader can follow the intended route, recover the exact
semantics, and tell what is supported. It is not synonymous with grammatical
polish or a low word count. Run the lightest gates that fit the requested
artifact; a personal scratch note need not pass a journal-style citation audit.

## Gate A — route and spine

- The first screen states purpose, audience, and current answer/unknown.
- Headings form a route, not only a taxonomy; each section contract names its
  question and next dependency.
- A paragraph that changes lane (motivation, semantics, realization, evidence)
  has a bridge or a split.
- Every abbreviation and project-local term is explained at first load-bearing
  use or linked to a term card.
- The mainline does not require reading an appendix or a later section first.

Severity: `blocker` when the next inference is impossible; `major` when a
reader can proceed only by guessing; `minor` for navigation friction.

## Gate B — notation and dependency order

- Every symbol has a declaration, type/domain, scope, and first-use locator.
- A symbol is not used with a new meaning without a qualified scope or an
  explicit decision.
- Definitions and assumptions precede claims and derivations that use them.
- Forward references are either removed or accompanied by a short bridge and a
  reason for retaining them.
- Index sets, dimensions, state lifetime/reset, and evaluation order are stated
  where they affect the result.

Automated scans can find candidate undeclared glyphs or heading order, but they
cannot parse arbitrary LaTeX semantics. Treat a scan as triage, not a proof.

## Gate C — claims and evidence

- Each consequential claim is labeled as definition, theorem/proposition,
  conjecture, design intent, implementation observation, empirical result, or
  interpretation.
- A claim has an explicit scope and boundary; universal words such as “always”
  and “guarantees” are justified.
- Evidence states artifact, conditions, comparison, and limitations.
- Failed or negative results remain visible when they change the conclusion.
- A citation is checked for what it actually establishes, not merely attached
  to a related keyword.

## Gate D — cross-view identity

Compare the canonical model with every derived view:

| Check | Question |
| --- | --- |
| notation | Are glyphs, dimensions, and names bound identically? |
| modality | Did a slide/paper turn an option or observation into a fact? |
| scope | Are model-family, implementation, and run scopes preserved? |
| omission | Can omitted proof/caveat be reached through notes/appendix/ledger? |
| provenance | Does each figure/table/result point to a source artifact? |

## Gate E — cold-reader and author check

Perform two distinct passes:

1. **Cold-reader pass:** without the drafting chat, write one sentence for the
   purpose, each section's question, the central mechanism, and the strongest
   supported result. Record the first point at which a guess was required.
2. **Author check:** ask the user one focused boundary or application question
   about the earliest doubtful concept. A fluent “yes” is weaker evidence than
   a correction, paraphrase, or application.

If the reader says “局部都懂但整体不懂”, repair the earliest missing relation
or route before editing sentences. If the reader says “太基础”, compress only
the confirmed prerequisite and keep its link available.

## Gate F — rendering and reproducibility

For code/experiments, verify the protocol and configuration independently of
the prose. For slides/PDF, inspect overflow, equation legibility, labels,
font fallback, and notes/appendix links. For Markdown/Obsidian, check relative
links and heading anchors in the target vault. Record tool/version and known
limitations; never report “validated” when only a regex or visual glance ran.

## Suggested audit report

```yaml
artifact: docs/foo.md
gates: [route, notation, claims, cross-view, cold-reader]
findings:
  - id: F-003
    severity: major
    location: "# 2.1 paragraph 3"
    type: forward-dependency
    observation: "selector is used before its candidate set is defined"
    repair: "insert a two-sentence bridge or move definition"
    semantic_risk: low
status: needs-author-check
```

An audit produces findings and a reversible repair plan before making broad
changes. It should identify uncertainty rather than hide it under smoother
prose.

