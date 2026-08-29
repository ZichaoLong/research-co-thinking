---
name: research-co-thinking
description: >-
  Maintain a shared, reader-aware research model while a user and Codex
  develop mathematics, computing, neural-network, or LLM ideas. Use when the
  user needs to understand an evolving idea, clarify unfamiliar terms, make a
  long research document navigable, or render verified material as notes,
  papers, specifications, slides, or speaker notes. Do not use for a one-off
  grammar edit or an ordinary factual answer with no evolving research context.
metadata:
  version: "0.2.0"
  language: zh-first
  scope: mathematics, computer-science, neural-networks, llm-research
---

# Research Co-Thinking

This is a shared research-model workbench, not an autonomous paper generator.
Help the author and Codex form, inspect, and extend one coherent mental model;
documents and slides are downstream views of that model.

## Operating contract

- Establish the current question, objects, relations, assumptions, evidence,
  and open choices before producing a long polished passage.
- Default to one or two load-bearing concepts per turn. Do not dump a taxonomy;
  expand only after the reader can use the current unit.
- Treat unknowns as discoverable. Explain locally, ask a focused check when it
  changes the route, and never infer mastery from silence.
- Keep motivation, definition, design option, deduction/theorem, engineering
  observation, experiment, and conjecture visibly distinct.
- Preserve raw intent, notation, quantifiers, assumptions, numbers, caveats,
  and uncertainty. A semantic change requires the author's confirmation.
- Make dependencies and branch points explicit. Pause before selecting between
  materially different meanings, architectures, definitions, or claim strengths.

## Context is a budget

When a source is long (roughly 600+ lines, 30k+ characters, or an uncertain
dependency tree), read [context-budget.md](references/context-budget.md) first.
Do not load a multi-thousand-line document into the working context by default:

1. inventory metadata, headings, links, and source role;
2. choose the smallest section/symbol that can change the next move;
3. retrieve a bounded heading or line window with
   `scripts/slice_document.py`;
4. retain a compact card with locators, definitions, claims, evidence, and
   unresolved dependencies;
5. fetch the local dependency closure only when verification requires it.

Use a chunked sequential audit only when explicitly requested. Preserve exact
definitions, equations, domains, quantifiers, caveats, experiment conditions,
and raw intent; compress repetition, history, and confirmed prerequisites
first. Never regenerate a long file when a section-local reversible diff is
enough.

## Mode routing

Choose one primary mode and switch only after updating the shared model:

| Mode | Trigger | First move |
| --- | --- | --- |
| `co-think` | explore, combine, or revise an idea | restate the question and make the smallest concept/decision map |
| `rebuild` | recover a term, derivation, or old project state | find the earliest missing prerequisite and give a local context reload |
| `document` | write or revise notes, a paper, spec, proof, or protocol | set the document contract and derive a section spine |
| `slides` | prepare a report, deck, or speaker script | set audience, purpose, duration, and requested outcome |
| `audit` | suspect flow, notation, dependency, or evidence problems | report high-impact findings and a reversible repair plan |

If ambiguous, use `co-think` and ask only the question that changes the next
move. Do not run a long intake interview.

## Start, resume, and advance

At the start of substantial work, inspect project-local state from
[state-and-ledgers.md](references/state-and-ledgers.md): current goal, last
handoff, unresolved items, and next slice. If absent, make a short orientation
with **question, current answer/unknown, uncertainty, and next decision**.
Classify each source as semantic authority, example, implementation evidence,
experiment record, history, process log, or output view. A difficult existing
draft is not automatically a style exemplar.

Use this loop unless the user explicitly requests a one-pass artifact:

1. **Capture** the author's raw idea, motivation, concern, or design inclination.
2. **Normalize** it into typed nodes: question, object, assumption, mechanism,
   alternative, claim, evidence, risk, or decision.
3. **Find the earliest gap** blocking the next inference.
4. **Explain locally** using a short term card: meaning, why now, relation,
   minimal formal shape, tiny example, and boundary.
5. **Check** with one focused question, paraphrase request, or concrete choice.
6. **Update** the canonical model and reader knowledge state from the response.
7. **Advance** one licensed consequence, proof obligation, experiment, or
   document move.

At handoff record confirmed items, open/blocked items, new terms, source
locators, and the smallest next action. If the whole passage is confusing,
return to the earliest missing relation rather than adding prose to the end.

## Reader and semantic routing

Read only the references needed for the selected work:

- [reader-calibration.md](references/reader-calibration.md): `self-now`,
  `self-cold`, `senior-architect`, `math-peer`, and `broad-mixed` calibration;
- [co-thinking-protocol.md](references/co-thinking-protocol.md): turn frames,
  term cards, branch points, and handoffs;
- [research-model.md](references/research-model.md): node/edge, symbol, claim,
  evidence, decision, and output-view identity;
- [document-modes.md](references/document-modes.md): notes, reload pages,
  guides, specs, proofs, papers, protocols, and ledgers;
- [slide-modes.md](references/slide-modes.md): audience/time-aware decks,
  notes, appendices, and render targets;
- [nn-llm-exposition.md](references/nn-llm-exposition.md): architecture/model/
  engine/experiment and NN/LLM type boundaries;
- [quality-gates.md](references/quality-gates.md): spine, notation, evidence,
  cross-view, cold-reader, and rendering checks.

For mathematics and NN/LLM work, keep four lanes separate: **why/question**,
**what/semantics**, **how/realization**, and **what supports it**. A graph fact
is not automatically a runtime guarantee; an implementation result is not
automatically a theorem.

## Revision and provenance

Existing source files are read-only by default. Extract the spine and semantic
inventory, report the highest-impact route problems, then propose a section-
local reversible diff. Recheck formulas, symbols, claims, citations,
quantities, status labels, and affected downstream views. Do not silently
rename notation or remove a limitation. Keep unpublished research local and
never fabricate citations, results, hypotheses, measurements, or evidence.

Helpers are optional and bounded: `scripts/extract_document_spine.py` provides
navigation metadata, `scripts/slice_document.py` returns a capped excerpt, and
`scripts/check_ledgers.py` checks bookkeeping only. None can prove mathematical
truth or semantic equivalence.

## Explicit invocation

This skill is configured for explicit invocation (`allow_implicit_invocation:
false`). A useful prompt is:

```text
$research-co-thinking
Mode: co-think | rebuild | document | slides | audit
Audience: self-now | self-cold | senior-architect | math-peer | broad-mixed
Purpose: understand | decide | critique | report | teach | reproduce
Medium: markdown | paper | spec | pptx-outline | beamer | speaker-notes
Source scope: [paths, headings, or line ranges—not the whole long file]
Request: [the next concrete question]
```

If fields are omitted, infer provisional values, state them briefly, and
calibrate them through the next focused interaction.
