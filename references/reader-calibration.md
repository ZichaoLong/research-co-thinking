# Reader calibration

Reader calibration is an iterative working hypothesis, not a personality
label. Keep a stable background card and a per-artifact situation card.

## Two cards

### Background card

Record only information that changes an explanation:

| Field | Example |
| --- | --- |
| `known` | linear algebra, probability, transformer blocks |
| `likely_known` | standard graph algorithms, basic optimization |
| `domain_gap` | this project's event-DAG terminology |
| `notation_tolerance` | light / standard / dense |
| `preferred_representation` | equations, dataflow diagram, running example |
| `evidence_expectation` | theorem, benchmark, implementation trace |

Do not infer a permanent level from a title, age, or one successful answer.

### Situation card

Record what this particular artifact must accomplish:

```yaml
audience: senior-architect
purpose: decide-next-experiment
medium: slides
duration_minutes: 20
must_leave_with:
  - the design constraint
  - the strongest evidence
  - the unresolved risk
```

The situation card can override the background card. A mathematically trained
reader may still need a short explanation of a new LLM systems term; a senior
architect may want a one-page decision brief rather than a proof.

## Initial audience archetypes

Use these only as starting points. Edit them after the first check.

### `self-now`

Assume strong project ownership but do not assume that every newly imported
term is familiar. Start with the current question, what changed since the last
session, and the smallest unresolved decision. Prefer precise detail over
ceremonial exposition.

### `self-cold`

Treat the reader as the same author after context decay. Restore the reason for
the project, the current mainline, the rejected alternatives, and the source
map before reopening technical details. Highlight changes and open obligations.

### `senior-architect`

Assume broad technical literacy and limited patience for project-local names.
Lead with constraints, architecture, trade-offs, evidence, risk, and the
decision requested. Put derivations and implementation minutiae in an
appendix or speaker notes. Never replace a precise claim with an appeal to
authority or a slogan.

### `math-peer`

Assume strong mathematical maturity, but do not assume familiarity with the
specific NN/LLM implementation. State types, domains, quantifiers,
assumptions, theorem status, and the correspondence between formal objects and
the implementation. A proof sketch is not a proof; an experiment is not a
universal result.

### `broad-mixed`

Assume heterogeneous preparation. Begin with a concrete phenomenon or small
example, introduce only the notation needed for the next inference, and keep a
visible glossary. Use a diagram or running example, then give one formal
anchor and a bounded takeaway. Offer an advanced appendix rather than
front-loading it.

## The calibration loop

For each unfamiliar or potentially overloaded term:

1. Give its local meaning in one sentence.
2. Explain why it is needed at this point.
3. Relate it to an already established object.
4. Give one small example or counterexample.
5. Ask one discriminating check only if the answer changes the route.

Useful checks include:

- “Should I treat `SCC` here as a graph-theoretic object, a runtime macro
  node, or both?”
- “Do you want the proof of this bound, or only the implication for the
  experiment?”
- “Can we skip the standard Transformer definition and focus on the new
  placement interface?”

Evidence for a knowledge-state update is stronger in this order:

1. the user corrects or rephrases the concept;
2. the user applies it to a new case;
3. the user answers a focused boundary question;
4. the user merely does not object.

Do not treat item 4 as mastery.

## Adaptation signals

After each unit, update the route from observable signals:

| Signal | Action |
| --- | --- |
| User asks what a term means | add a local term card; mark it `revisit` until used |
| User corrects the model | preserve the correction; re-check dependent edges |
| User says “整体不懂” | return to the earliest missing relation, not the last sentence |
| User says “太基础” | compress that prerequisite and spend budget on the unresolved edge |
| User asks “为什么现在讲这个” | expose the section's motivation and dependency edge |
| User asks for a report | switch situation card; do not discard the canonical model |

The skill should become more concise about confirmed prerequisites while keeping
their definitions available through links or a glossary.

## Language and naming

Follow the user's current working language; for this profile, default to
Chinese prose. At the first load-bearing use of an imported term, give a short
Chinese local meaning and the English canonical term in parentheses when that
helps search or disambiguation. Do not stack a translation, acronym, historical
name, and taxonomy in the same sentence. Preserve project names and notation,
and ask before standardizing a disputed Chinese translation.
