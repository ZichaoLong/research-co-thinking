# Research Co-Thinking

`research-co-thinking` is a reader-aware Codex skill for jointly developing
mathematics, computer-science, neural-network, and LLM research ideas. It is
designed for the case where the author needs to understand every load-bearing
detail before asking the work to become a paper, specification, personal note,
or presentation.

The skill keeps a shared research model and derives audience-specific views
from it. Its default interaction is incremental: capture the author's raw
intent, identify the earliest missing dependency, explain one small concept,
check understanding, and only then advance. It does not treat polished prose
as evidence of understanding.

Version 0.2 adds bounded retrieval for long sources: the agent inventories a
spine, slices only the relevant section or line window, and keeps compact cards
and locators instead of repeatedly carrying a whole document in context.

## Contents

- `SKILL.md` — routing, invariants, and invocation contract;
- `references/` — reader calibration, co-thinking protocol, research-model
  schema, long-document context budgeting, document/slide modes, NN/LLM
  exposition, state, and quality gates;
- `scripts/` — read-only spine extraction, bounded document slicing, and ledger
  checks;
- `pilot/` — a small, non-destructive exercise on TIDE/fractal-latcarf source
  material and a ledger fixture.

## Local use

This repository is intentionally kept separate from the author's research
documents. To make it available as an automatically discovered Codex skill,
copy or symlink the repository directory to a local Codex skill directory after
reviewing it. In current Codex documentation, a user-level location is
`~/.agents/skills/` (a repository-level `.agents/skills/` also works):

```bash
mkdir -p ~/.agents/skills
ln -s /path/to/research-co-thinking ~/.agents/skills/research-co-thinking
```

Some older/local installations use `$CODEX_HOME/skills` or `~/.codex/skills`;
use the skill root reported by that installation. Explicit invocation remains
`$research-co-thinking` because implicit invocation is disabled here.

The repository itself does not require network services or third-party runtime
packages. The helper scripts use the Python standard library. They report
bookkeeping and navigation issues; they cannot prove a theorem or semantic
equivalence.

## Provenance and scope

The design was informed by public mathematical-authoring, paper-planning,
dependency-audit, and diagnostic-teaching projects. Their prose and code are
not copied here, and none is a runtime dependency. The `pilot/` report names
only project-local source paths and does not modify those files.
