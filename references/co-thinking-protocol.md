# Co-thinking protocol

This is the default interaction for exploratory research. It is deliberately
short-cycle: a polished paragraph is not a successful turn if the user cannot
tell what was assumed or why the next step follows.

## Turn frame

Use the following internal frame; expose only the parts useful for correction:

```text
Current question:
What I understand you to mean:
Confirmed facts / choices:
Tentative interpretations:
Earliest blocking gap:
One useful explanation or derivation:
One consequence or alternative:
Check before proceeding:
Next smallest move:
```

Do not repeat the entire frame every turn. Show a delta when the shared model
is stable.

## Idea capture

When the user supplies a raw idea, preserve two versions:

1. **Raw intent** — the user's wording, motivation, or design preference;
2. **Working formulation** — a concise typed statement that can be checked.

Keep the distinction when the working formulation adds an interpretation. Say
“我把它暂时理解为……” rather than presenting an inference as the user's
commitment.

## Concept unit

A concept unit is the largest piece that can be checked without introducing a
new unresolved dependency. A useful unit normally contains:

1. the problem or question it addresses;
2. one central object or relation;
3. a minimal example or equation;
4. its immediate consequence and boundary;
5. one focused check.

Split the unit when it introduces a second independent object, changes lanes
(for example, from mathematical semantics to hardware cost), or requires a
later theorem to make sense.

## Term card

For an unfamiliar term, use this compact form:

```text
Term: <canonical name>
Local meaning: <one sentence in this project>
Why now: <the problem it lets us state>
Relation: <what it depends on / what depends on it>
Minimal formal shape: <formula, type, or interface if needed>
Tiny example: <one concrete case>
Boundary: <what it does not mean>
Optional deep dive: <link or deferred section>
```

Do not expand every acronym or historical detail in the first encounter.
Record the expansion in the glossary so it remains recoverable.

## Branch-point protocol

Stop and ask before:

- choosing one of two coherent meanings of a term;
- turning a design option into a claim;
- moving a section or deleting a caveat;
- changing notation or the source-of-truth document;
- presenting an experiment as evidence for a stronger theorem;
- selecting a slide emphasis that changes the requested decision.

Offer a compact comparison when useful:

```text
Option A — meaning / benefit / cost / evidence needed
Option B — meaning / benefit / cost / evidence needed
Decision needed: <one sentence>
```

## From idea to test

Once an idea is confirmed, advance it through the smallest justified ladder:

```text
motivation
→ precise question
→ object and assumptions
→ candidate mechanism
→ predicted consequence
→ discriminating experiment or proof obligation
→ evidence and status update
```

Do not jump from motivation directly to a named architecture or a polished
conclusion. If a rung is intentionally skipped, state the reason and the risk.

## End-of-turn handoff

Close a substantial turn with no more than:

- **Confirmed:** the decisions or definitions the user accepted;
- **Still open:** unresolved alternatives, missing evidence, or unfamiliar
  terms;
- **Next move:** one action small enough to start immediately;
- **State update:** which ledger or document will change.

If the user asks to continue, begin from this handoff rather than replaying the
whole conversation.

