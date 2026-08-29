# Pilot — reader-aware reconstruction (read-only sources)

This pilot exercises the skill on two source files. It does not edit either
source, rename symbols, or assert that the mathematical argument is correct.
The line numbers are locators in the source as inspected on 2026-08-29; rerun
the spine extractor if the files change.

## Inputs and roles

| Artifact | Role used in the pilot |
| --- | --- |
| `ObsidianVault/20-tide-decentralized-neural-network/adaptive-routing-prefill-lower-bound.md` | authoritative mathematical draft plus Tide-facing interpretation |
| `llm/fractal-latcarf/docs/experiment-semantics-and-naming.md` | target experiment semantics/interface specification; it explicitly says v0 and historical runs may not implement all targets |

The existing documents already contain valuable guardrails (definition-before-
use, claim boundaries, proof status, placement tables, and a reading entry).
The pilot therefore treats them as semantic sources and repairs the reader
route around them, rather than using their full prose as a style exemplar.

## One-page shared orientation

### Mathematical lower-bound thread

**Question.** Under what precise conditions does an adaptive routing chain rule
out a work-efficient, sublinear-depth exact prefill?

**Current answer in the source.** Not every cross-token recurrence is
sequential: XOR and affine transitions can be scan-composed (section 1,
lines 62–128). The claimed lower bound instead targets a sufficiently large
routing state space, exact treatment of arbitrary black-box transitions, and a
work budget that does not enumerate the state space (overview line 38; theorem
6.1, lines 577–606).

**What is still conditional.** The theorem's assumptions, the oracle embedding
of a concrete selector, and the mapping from query depth to a particular runtime
all need to remain explicit. The source itself lists structured escape cases
and non-claims in sections 10–11.

### Experiment-semantics thread

**Question.** What is the stable semantic contract between a base Transformer
block and a stateful, graph-routed `GraphBranch`, independent of a particular
implementation?

**Current answer in the source.** The contract exposes one hidden entering and
one hidden leaving the branch, with four placement choices; internal roles
(`AggregatePort`, receiver, selector, state, `EmitPolicy`) and execution order
are defined separately (sections 1–2, lines 15–490).

**What is still conditional.** The document labels complex-topology defaults as
pending review and warns that v0/reference and historical experiments may not
cover the target interfaces (lines 1–11). Those statuses must not be flattened
into implementation facts.

## Three reader routes

| Reader | Route | Deliberately deferred |
| --- | --- | --- |
| `self-now` | phenomenon → XOR/affine counterexamples → exact adaptive-address question → query model → one lemma → theorem → concrete selector obligation | full asymptotic preliminaries until used |
| `senior-architect` | decision (“which routing promises can prefill support?”) → constraint (address discovery/work) → architecture choices → evidence and cost → structured escape conditions → requested next experiment | line-by-line proof and node internals (speaker notes/appendix) |
| `math-peer` | typed state space/transition → query round/transcript/exactness/work → fresh-address lemmas → theorem → quantifier boundary → graph embedding | implementation history unless it changes a hypothesis |
| `broad-mixed` | tiny pointer-chasing trace → why XOR is different → one picture of the query model → bounded takeaway → optional formal appendix | most notation and acronym inventory |

The routes select the same canonical nodes; they differ only in order, depth,
and what is kept in notes or an appendix.

## Concept dependency map

```text
cross-token influence (motivation)
 ├─> prefix XOR / affine scan (counterexamples)
 └─> adaptive address discovery (precise question)
      ├─> routing state space Ω, length L, oracle family F
      ├─> query / round / transcript / exactness / work / depth
      │    └─> fresh-address lemmas
      │          └─> exact adaptive-routing lower bound
      │                ├─> work-efficient prefill corollary
      │                ├─> layered-graph embedding
      │                └─> Tide design constraints + escape conditions

+base block boundary (architecture)
 └─> GraphBranch input/output + placement
      └─> AggregatePort / receiver / selector / state / EmitPolicy
            ├─> one-step execution order
            ├─> single-layer instance
            └─> HB-Lattice / wavefront instance
                  └─> experiment protocol and implementation checks
```

The first branch is a mathematical argument; the second is a semantic/runtime
contract. A slide or section should say when it moves from one branch to the
other.

## Sample symbol and term ledger

| Name | Local type/scope | First source use | Status to preserve |
| --- | --- | --- | --- |
| `L` | positive chain length / token-axis index bound | lower-bound overview and definitions 2–4 | confirmed in the draft; check each theorem quantifier |
| `q_t` | routing state/address at step `t` | XOR/affine examples and routing-chain definitions | overloaded risk: state versus address; qualify in each scope |
| `F_t` | transition/oracle at step `t` | routing oracle definitions | formal object, not automatically a runtime kernel |
| `R_A` | adaptive query-round depth of algorithm `A` | definitions 4.7 and theorem 6.1 | claim quantity; distinguish from wall-clock latency |
| `x_{ell,t}` | hidden entering base block `ell`, token `t` | experiment document section 1.1 | implementation/model interface symbol |
| `h_in_{j,t}` | GraphBranch input hidden at site `j`, token `t` | experiment document section 1.1/1.3 | placement-dependent; do not conflate with `x_{ell,t}` |
| `Delta_G_{j,t}` | GraphBranch residual relative to common input | experiment document section 1.3 | boundary output, not an internal message |
| `state` | persistent value with declared lifetime/update | experiment document sections 2.1/2.6 | requires profile/reset scope |
| `frontier` | project-local term with more than one possible graph/schedule meaning | lower-bound notes around line 27 and later sections | `revisit` until one canonical scope is chosen |

## Semantic-preserving rewrite sample

The following is a proposed replacement for the *route* of the lower-bound
overview, not an in-place edit. It preserves the source's qualifications and
leaves theorem details for later sections.

> **What this page can and cannot show.** We study a routing chain of length
> `L` in which the address needed at step `t+1` is revealed only after the
> transition at step `t` is answered. We ask whether an algorithm can process
> every allowed transition exactly, use work close to the realized route, and
> still finish in `o(L)` adaptive rounds.
>
> Cross-token dependence alone is not enough for a negative result. Prefix XOR
> and affine recurrences have a composable operation, so a parallel scan can
> evaluate all prefixes. The target obstruction is narrower: arbitrary
> black-box address-dependent transitions without a promised scan or bulk-
> composition law.
>
> We therefore proceed in four checkpoints: (1) define the state space and
> oracle family, (2) define a parallel query round, exactness, work, and depth,
> (3) prove that a fresh unseen address prevents more than one reliably new
> route step per round under the stated budget, and (4) map the abstract result
> to a layered graph while listing structured cases that escape the bound.

This version introduces only the concepts needed for the next inference and
keeps “runtime” as a later mapping rather than an unstated consequence.

## Audit findings (candidate findings, not semantic verdicts)

| ID | Severity | Observation | Reversible repair to consider |
| --- | --- | --- | --- |
| P-01 | major | The lower-bound overview uses `routing state space`, `adaptive depth`, `work-efficient`, and `chunk prefill` before their formal definitions in sections 2–4. | Keep the short overview, add a four-line local glossary/bridge, and defer the formal symbols to section 2. |
| P-02 | major | Mathematical motivation, Tide architecture consequences, and runtime-performance caveats are interleaved (for example overview lines 40–60 and graph embedding lines 812–816). | Label the lane in each subsection; move runtime caveats to a clearly linked realization subsection. |
| P-03 | major | The experiment document is both a target semantic specification and a map of current/historical implementation status. | Add a visible status badge per section or split the target contract from the implementation review ledger. |
| P-04 | medium | `state`, `node`, `frontier`, `t`, and `v` have explicitly different meanings in nearby contexts; the source warns about this, but a cold reader still has to retain several axes at once. | Add a compact type/scope table at each lane boundary and use qualified names in the mainline. |
| P-05 | medium | Deep heading trees (up to level 5 in the mathematical foundations family) make the route hard to reconstruct outside Obsidian navigation. | Add a one-page map and section contracts; do not flatten definitions or change numbering without author approval. |
| P-06 | review-needed | A regex/spine scan can flag candidate forward uses and undefined symbols but cannot decide whether a displayed formula's notation is semantically bound. | Run the helper scripts for triage, then perform a human symbol/claim ledger pass. |

## Smallest next move

Create a project-local ledger for just the lower-bound overview and the
GraphBranch boundary (roughly 15–25 nodes), then ask the author to confirm the
two overloaded terms `state` and `frontier`. Once those are confirmed, derive a
10-minute senior-architect deck and a math-peer proof route from the same IDs.
