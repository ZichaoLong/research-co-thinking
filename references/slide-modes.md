# Slide modes

Slides are a view of the shared research model, not a second source of truth.
Before outlining a deck, fill a situation card:

```yaml
audience: self-now | self-cold | senior-architect | math-peer | broad-mixed
purpose: understand | decide | teach | report | solicit-critique
duration_minutes: 15
requested_outcome: "approve the next ablation"
prior_knowledge: "..."
medium: markdown-outline | pptx | beamer | speaker-notes
```

If duration or requested outcome is unknown, make a provisional assumption and
ask only the question that would change the deck spine. Default to a Markdown
outline with explicit speaker notes, then render to PPTX when an editable deck
is wanted; use Beamer when equations and reproducible source are the priority.
Do not maintain independent facts in a `.pptx` file.

## The slide contract

Every slide has one load-bearing takeaway, one relation to the preceding slide,
and a declared audience action. Store it in notes or an outline table:

| Field | Meaning |
| --- | --- |
| `slide_id` | stable identifier for later edits |
| `question` | question this slide answers |
| `takeaway` | one sentence the audience should retain |
| `visual` | diagram, equation, table, or example; name its source nodes |
| `spoken_bridge` | why this follows and what to watch for |
| `assumptions` | prerequisites not shown on the slide |
| `status` | draft / checked / evidence-backed |
| `appendix_link` | where omitted detail can be recovered |

Use at most one new notation family per slide unless the comparison itself is
the point. Put definitions next to first use; if a symbol is only needed in an
appendix, do not introduce it in the main deck. A slide may be visually sparse
while its speaker notes carry a precise qualification.

## Audience-specific spines

These are starting routes, not stereotypes. Calibrate after the first question
or rehearsal.

### `self-now` and `self-cold`

For the author, optimize for re-entry and a next decision:

```text
why this thread exists → current model/map → changed assumptions
→ key mechanism with one worked trace → open branch/risk → next action
```

`self-cold` needs a short rejected-alternatives slide and source/commit
provenance; `self-now` can collapse already-confirmed prerequisites into notes.

### `senior-architect`

Lead with the decision and system constraint, then show the smallest mechanism
that makes the trade-off credible:

```text
decision requested → workload/constraint → architecture boundary
→ cost/benefit and evidence → failure modes → options and recommendation
```

For a technically broad, experienced leader, avoid unexplained project-local
names and avoid pretending a benchmark proves a general law. Keep derivations,
kernel details, and full notation in speaker notes or an appendix. State what
would change the recommendation.

### `math-peer`

Make the formal object and status visible while connecting it to the
implementation:

```text
question → definitions/types → proposition or invariant
→ proof/derivation or exact algorithm → implementation correspondence
→ empirical check and boundary
```

Do not replace quantifiers with diagrams. Label a proof sketch, conjecture,
heuristic, and measured result differently. Include a notation appendix only
after the main dependency route is clear.

### `broad-mixed`

Start from a concrete phenomenon, not a stack of acronyms:

```text
observed example → intuitive obstacle → tiny running example
→ one formal anchor → proposed mechanism → evidence/boundary
→ takeaway and invitation
```

Define only the terms needed for the next move and keep a visible two-line
glossary. Offer optional deep-dive slides rather than front-loading every
component.

## Timing and density

Budget time by decisions, not by a fixed slide count. Mark slides as
`must-understand`, `supporting`, or `appendix`; if rehearsal exceeds the budget,
remove supporting slides before compressing a must-understand bridge. A slide
that introduces a term, equation, and architecture simultaneously usually
needs to be split or preceded by a worked example.

Use progressive disclosure within a slide: phenomenon/diagram first, labels
second, equation or caveat third. Animation is optional; the static sequence of
states must remain interpretable when exported to PDF.

## Speaker notes and appendices

Speaker notes should contain:

- the spoken bridge from the previous slide;
- one local explanation for a likely unfamiliar term;
- the exact qualification or evidence condition;
- a check/question to ask the audience when the decision depends on it.

An appendix can hold full proofs, ablation tables, symbol ledgers, runtime
traces, and alternative designs. Link each appendix slide to the main claim it
supports; an appendix is not permission to omit a necessary mainline
assumption.

## Rendering and semantic QA

Treat Markdown, PPTX, Beamer, and PDF as render targets. Before rendering,
validate slide IDs, source-node links, symbol declarations, and claim/evidence
status. After rendering, inspect overflow, equation legibility, figure labels,
font fallback, and whether notes/appendix links survived. A visually polished
deck can still fail the shared-model check if it changes a quantifier or turns a
design option into a result.

