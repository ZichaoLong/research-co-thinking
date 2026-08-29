# Context budget for long documents

Long prose is an input-budget problem as well as a writing problem. The default
is **bounded retrieval**: discover the document's map, retrieve only the
smallest windows needed for the current inference, and retain structured cards
instead of repeatedly pasting the same paragraphs. This applies to Markdown,
LaTeX, notebooks exported to text, and long experiment logs.

## Trigger and budget

Enter long-document mode provisionally when a source is more than about 600
lines, more than about 30,000 characters, or has a deep/uncertain dependency
tree. These are routing heuristics, not context limits; the user can override
them. Estimate source size with a cheap metadata command, then reserve room for
the user's next turn, reasoning, and the requested output. Never spend the
whole available window on source ingestion.

Keep three separate budgets:

```text
source budget   — raw excerpts currently needed
model budget    — compact cards, definitions, claims, and decisions retained
output budget   — explanation, diff, paper section, or slides to produce
```

If one budget grows, compress or defer another. Do not solve pressure by
silently dropping a hypothesis, quantifier, caveat, failed result, or notation
binding.

## Retrieval levels

Use the lowest level that can answer the next question:

| Level | Retrieve | Use for |
| --- | --- | --- |
| `L0 locator` | path, size, date/hash, headings, links, frontmatter | orientation and source choice |
| `L1 section card` | section contract, first/last paragraphs, definitions/claims named in the map | decide what to read next |
| `L2 bounded window` | one heading subtree or explicit line range plus a small margin | explain or edit a local concept |
| `L3 dependency closure` | declarations and uses of the target symbol/term, adjacent assumptions and evidence | verify a claim or repair a cross-reference |
| `L4 sequential audit` | chunked pass over the whole source, with cards emitted between chunks | global audit when explicitly requested |

`L4` is not “load the entire file at once”. Process chunks in order, keep only
the cards and flagged locators in the working context, and make the aggregation
algorithm explicit.

## Default workflow

1. **Inventory.** Record path, byte/line count, heading spine, links, and
   source role. Use `scripts/extract_document_spine.py`; its JSON output omits
   formula bodies and the duplicate heading tree unless explicitly requested.
   Do not print the whole file merely to discover its headings.
2. **Choose a route.** Identify the current question and the one section or
   symbol that can change the next move. If several routes are plausible, ask
   for a branch decision rather than reading everything.
3. **Slice.** Use `scripts/slice_document.py` with a heading or line range (the
   default soft cap is 16,000 characters; lower it when the response also needs
   substantial reasoning/output).
   Include the parent heading and enough preceding/following lines to expose
   definitions, caveats, and transitions. Keep excerpts bounded by characters
   or lines; retrieve an exact formula separately if a cap cuts it.
4. **Card.** Convert the slice into a compact card:

   ```yaml
   source: docs/foo.md
   locator: "## 3.2, lines 410-468"
   purpose: "why this block exists"
   introduces: [O-selector, S-state]
   relies_on: [O-region]
   claims: [C-routing-bound]
   evidence_or_status: "definition / proposed / measured / open"
   unresolved: ["reset boundary not stated"]
   ```

5. **Verify locally.** For a consequential statement, retrieve its declaration,
   all nearby assumptions, and the exact supporting evidence. Search exact
   symbols/terms rather than rereading unrelated sections.
6. **Advance or stop.** Explain one concept, ask the focused check, and update
   the card/ledger. Do not fetch the next window until the check or branch is
   resolved.

## What to preserve when compressing

Preserve verbatim or with a precise locator:

- definitions, equations, domains, dimensions, index conventions, and state
  lifetime/reset rules;
- quantifiers, negations, exceptions, claim modality, and numerical values;
- experiment conditions, baseline, seed/configuration, and limitations;
- the author's raw intent when a working formulation is still tentative.

Compress or defer first:

- repeated motivation, historical chronology, routine prose, and already
  confirmed prerequisites;
- duplicate examples (keep one representative and link the rest);
- implementation or protocol detail not needed for the current question.

This is an ordering rule, not permission to delete information. Deferred detail
must remain reachable through a locator, ledger, appendix, or source link.

## Editing a long document

Make a section-local, reversible patch. Before changing it, retrieve the target
section and its immediate dependency cards; after changing it, re-read only the
changed section, its incoming/outgoing references, and affected symbol/claim
entries. A global consistency pass can be chunked by heading and summarized in
an audit ledger. Do not ask the model to regenerate a multi-thousand-line file
when a small diff suffices.

For a requested full rewrite, separate stages:

```text
spine + inventory → section contracts → local rewrites
→ cross-section dependency pass → cold-reader pass → render/compile check
```

The user may choose a different order; record the trade-off if a stage is
skipped.

## Session handoff under pressure

At the end of a window, save only what another session needs to continue:

```text
current question
confirmed cards/IDs
unread or stale sections
first unresolved dependency
source locators and next slice
```

Do not copy a long excerpt into the handoff unless it is a short canonical
definition. A hash or modification time can detect stale cards, but it cannot
prove semantic identity after a source edit; mark affected cards `revisit`.

## Limits

Heading and line tools are navigation aids. They do not understand arbitrary
LaTeX, Obsidian transclusion, diagrams, or mathematical equivalence. A bounded
excerpt can still omit a hidden dependency; report that uncertainty and fetch
the relevant closure before making a strong claim.
