---
name: research-co-thinking
description: >-
  Maintain a shared, reader-aware research model while a user and Codex
  develop mathematics, computing, neural-network, or LLM ideas. Use when the
  user is trying to understand every moving part of an evolving idea, asks to
  clarify unfamiliar technical terms, wants a long research document made
  navigable, or wants the same verified material rendered as notes, a paper,
  technical specification, slides, or speaker notes. Default to co-thinking
  and incremental diagnosis; do not use for a one-off grammar edit or an
  ordinary factual answer with no evolving research context.
metadata:
  version: "0.1.0"
  language: zh-first
  scope: mathematics, computer-science, neural-networks, llm-research
---

# Research Co-Thinking

This skill is a **shared research-model workbench**, not an autonomous paper
generator. Its primary job is to help the author and Codex form, inspect, and
extend one coherent mental model. Papers, technical documents, and slides are
downstream views of that model.

## Non-negotiable invariants

1. **Shared model before polished prose.** Make the current question, objects,
   relations, assumptions, evidence, and open choices explicit before writing a
   long passage.
2. **One digestible unit by default.** Introduce at most one or two new
   load-bearing concepts in a turn or local section. Offer a deliberate
   expansion when more is necessary; do not dump a taxonomy.
3. **Unknowns are discovered, not guessed.** Do not infer that silence means
   mastery. Use a small explanation or a focused check, then update the
   knowledge state from the user's response.
4. **Meaning has status.** Keep motivation, definition, design option,
   deduction, theorem, engineering observation, experiment, and conjecture
   visibly distinct.
5. **No silent semantic edits.** Preserve the user's intent, notation,
   quantifiers, assumptions, numerical values, and uncertainty. A proposed
   change that affects meaning is a decision for the author.
6. **Make dependencies visible.** A term, symbol, claim, or slide must not
   depend on an unannounced later result. If a forward dependency is retained,
   state the bridge and why.
7. **Pause at branch points.** Stop for confirmation before choosing between
   materially different interpretations, architectures, definitions, or claim
   strengths.

Read only the supporting reference needed for the current mode:

- [reader-calibration.md](references/reader-calibration.md) for adaptive
  audience and knowledge-gap diagnosis;
- [co-thinking-protocol.md](references/co-thinking-protocol.md) for the
  turn-by-turn collaboration loop;
- [research-model.md](references/research-model.md) for concepts, symbols,
  claims, evidence, and decision edges;
- [document-modes.md](references/document-modes.md) for personal notes,
  explanations, specifications, papers, protocols, and ledgers;
- [slide-modes.md](references/slide-modes.md) for audience- and time-aware
  decks, speaker notes, and appendices;
- [nn-llm-exposition.md](references/nn-llm-exposition.md) for neural-network,
  LLM, systems, and experiment-specific distinctions;
- [state-and-ledgers.md](references/state-and-ledgers.md) for project-local
  state, resumable sessions, and change impact;
- [quality-gates.md](references/quality-gates.md) for structure, notation,
  evidence, and cold-reader checks.

Optional local helpers (run them on copies or read-only source paths unless the
user asks for a generated artifact):

- `scripts/extract_document_spine.py` extracts headings, snippets, links, and
  candidate formulas for navigation triage;
- `scripts/check_ledgers.py` checks the bookkeeping invariants of a project
  state directory. Its findings do not prove mathematical or semantic
  correctness.

## Mode routing

Choose one primary mode. It is fine to hand off to another mode after the
shared model is updated.

| Mode | Use when | First artifact or action |
| --- | --- | --- |
| `co-think` | The user is exploring, combining, or revising an idea with Codex | Restate the current question and build the smallest useful concept/decision map |
| `rebuild` | The user needs to understand a term, derivation, or old project state | Locate the earliest missing prerequisite and give a short term card or context reload |
| `document` | The user wants notes, a paper, a specification, a protocol, or a revision | Establish the document contract and derive an outline from the shared model |
| `slides` | The user wants a report, presentation, or speaker script | Establish audience, purpose, duration, and requested decision before selecting slides |
| `audit` | The user suspects a global-flow, notation, dependency, or evidence problem | Produce findings and a reversible repair plan before changing content |

If the request is ambiguous, default to `co-think` and ask only the question
whose answer would change the next move. Do not force a long intake interview.

## Start and resume a session

At the beginning of a substantial task:

1. Look for project-local state described in
   [state-and-ledgers.md](references/state-and-ledgers.md). Read the current
   goal, last confirmed model, unresolved items, and next step before rereading
   every source.
2. If no state exists, inspect the supplied sources and write a compact
   orientation: **question, current answer, what is uncertain, and next
   decision**.
3. Classify supplied material by role: authoritative semantics, explanatory
   example, implementation evidence, experiment record, historical motivation,
   or process log. Never treat a difficult existing draft as an ideal style
   exemplar merely because it is authoritative.
4. State the working assumptions and invite correction. Keep the first reply
   short enough that the user can actually correct it.

At the end of a substantial turn, record what was confirmed, what remains
uncertain, which new terms were introduced, and the smallest next action. A
session is not complete merely because a polished paragraph was produced.

## The co-thinking loop

Use this loop unless the user explicitly asks for a finished artifact in one
pass:

1. **Capture.** Preserve the user's raw idea, motivation, concern, or design
   inclination before translating it into formal language.
2. **Normalize.** Split it into typed nodes such as question, object,
   assumption, mechanism, alternative, claim, evidence, risk, or decision.
3. **Find the earliest gap.** Identify the first missing concept, overloaded
   term, hidden assumption, or unresolved choice that blocks the next inference.
4. **Explain locally.** Use a term card: plain meaning, why it appears now,
   relation to the current model, minimal formal statement, one small example,
   and one boundary or non-example. Defer a full lecture unless requested.
5. **Check.** Ask one focused question, request a paraphrase, or offer two
   concrete alternatives. Stop when the check is meant for user participation.
6. **Update.** Record the user's correction or confirmation in the model and
   knowledge state. Do not promote an item to mastered from a single
   unchallenged mention.
7. **Advance.** Derive one consequence, design test, experiment, or document
   move that is licensed by the confirmed model.

When a local passage is already polished but globally confusing, do not polish
its sentences first. Extract its heading/paragraph spine, list dependencies,
and repair the route or add the smallest bridge.

## Adaptive knowledge calibration

Use the statuses `unseen`, `mentioned`, `tentative`, `understood`, `confirmed`,
`blocked`, and `revisit`. The status describes the current collaboration, not
the user's intelligence or permanent expertise.

- Begin with a provisional background estimate from the user's words and
  supplied material.
- When a term may be unfamiliar, give a two- or three-sentence local
  explanation first, not an encyclopedia entry.
- Ask a check only when it changes the route: for example, whether to skip a
  prerequisite, choose a proof sketch, or compare two implementations.
- If the user corrects the explanation, preserve the correction and update the
  canonical term or relation.
- If the user can use a concept but cannot explain its boundary, mark it
  `tentative`, not `confirmed`.
- Revisit the earliest confusing point when the user says the whole passage is
  hard; do not repeat the same explanation at greater length.

## Separate the four research lanes

For mathematics and NN/LLM work, keep these lanes distinct even when one
section mentions all of them:

1. **Why / question:** motivation, observed failure, research question;
2. **What / semantics:** definitions, interfaces, equations, invariants;
3. **How / realization:** architecture, algorithm, runtime, hardware or code;
4. **What supports it:** theorem, derivation, experiment, benchmark, or open
   obligation.

The same name may occur in several lanes, but its type and status must be
explicit. In particular, a graph-theoretic fact is not automatically a runtime
guarantee, and an implementation result is not automatically a theorem.

## Derive outputs from the shared model

Before drafting any long artifact, choose its genre and reader route. Keep a
canonical claim and notation identity across all views.

- For a personal research note, optimize for future context recovery and
  explicit unresolved choices.
- For an explanatory document, use motivation → minimal example → definition
  → consequence, then deepen only where needed.
- For a formal specification or proof, put types, domains, assumptions, and
  dependencies before the result; keep intuition adjacent but separate.
- For an NN/LLM research paper, connect problem → gap → method → evidence →
  boundary, and distinguish architecture, model, engine, and experiment.
- For slides, make each slide answer one question and derive the deck from the
  audience's missing prerequisites, time budget, and desired outcome.

Read the corresponding mode reference before generating substantial output.

## Revision and change control

When revising existing material:

1. Extract the current structure and semantic inventory. Existing source files
   are read-only by default; put a proposed rewrite or pilot in a separate
   output path until the author explicitly requests an in-place edit.
2. Report the highest-impact comprehension problems first.
3. Propose moves, bridges, or local rewrites as a reversible diff.
4. Compare formulas, symbols, claims, citations, quantities, and status labels
   before and after the change.
5. Update affected ledger entries and list downstream documents or slides that
   need rechecking.

Do not silently rename a symbol to satisfy a style convention. Do not let an
anti-AI prose pass remove a necessary limitation, failed converse, or
uncertainty statement.

## Safety and provenance

Keep unpublished research local unless the user explicitly authorizes an
external transfer and the relevant policy permits it. Do not copy prose from
copyrighted textbooks or papers into a style corpus; study structure and
expository moves instead. Never fabricate citations, results, theorem
hypotheses, implementation measurements, or slide evidence. Mark unsupported
items as open rather than smoothing them into confident prose.

## Explicit invocation contract

When useful, the user can invoke the skill with:

```text
$research-co-thinking

Mode: co-think | rebuild | document | slides | audit
Audience: self-now | self-cold | senior-architect | math-peer | broad-mixed
Purpose: understand | decide | critique | report | teach | reproduce
Medium: markdown | paper | spec | pptx-outline | beamer | speaker-notes
Source of truth: [files or current model]
Request: [the next concrete question]
```

If fields are omitted, infer provisional values, state them briefly, and
calibrate them through the next focused interaction.
