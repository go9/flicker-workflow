# The Flicker Workflow

An agent-native development workflow: **plan → implement → test → release**, driven by tickets, versioned planning documents, and durable project memory — designed so AI coding agents can carry work end to end without losing the plot, and humans keep the gates that matter.

[Flicker](https://flickercloud.com) is the reference implementation: Flicker Tickets is the tracker, and the `flicker` CLI is the integration surface. But the workflow itself is a contract, not a product lock-in — see [Bring your own tracker](docs/bring-your-own-tracker.md).

## Quickstart

```bash
# 1. Install the flicker CLI and authenticate
flicker auth login <api-key>
flicker project use <your-project>

# 2. Install the workflow skills into your AI harness
#    (Claude Code, Codex/AGENTS.md, and Pi are auto-detected)
flicker skill install --workflow --global

# 3. Drive work through the stages
#    In your agent: /flicker-plan "add rate limiting to the API"
#    then /flicker-implement, /flicker-test, /flicker-release
```

That's the entire setup. The skills ship embedded in the CLI binary — no clone, no network, idempotent re-runs.

## The shape of it

| Stage | Skill | What it owns |
|---|---|---|
| **Plan** | `flicker-plan` | Search existing work first, shape scope, write `feature_brief` / `plan_consensus` / `task_contract`, select approved work for dev |
| **Implement** | `flicker-implement` | Feature branch in a dedicated worktree, code only the contract, open a PR, write `implementation_notes` |
| **Test** | `flicker-test` | Drive the PR-review loop with a pluggable AI reviewer, run regression, write a `test_verdict` |
| **Release** | `flicker-release` | Verify evidence, then merge **only with explicit human approval** (merge may deploy) |
| **Ship** | `flicker-ship` | The autonomous end-to-end loop, inside safety rails: tests must be green, danger zones escalate to a human |
| **Recall** | `flicker-recall` | Search tickets, current documents, and historical memory with provenance labels |

The full contract — canonical statuses, transitions, document kinds, the PR + review loop, and every stage procedure — is in [workflow.md](workflow.md).

## Why it works for agents

- **Tickets are the single source of truth.** Agents pick up only work that a human selected for development; status transitions are mandatory, so a watched in-progress list never lies.
- **Documents beat chat memory.** Plans, contracts, review verdicts, and release evidence are versioned documents attached to the ticket — the next agent (or the same agent after a context reset) reads current truth instead of reconstructing it.
- **Memory is append-only evidence.** Decisions and discoveries land in project memory, searchable later, never silently rewritten.
- **Approval gates are explicit.** No implementation before an approved contract; no merge/deploy without a human's explicit yes. Autonomy happens inside the rails, not instead of them.
- **Review is rented, not built.** Any PR-reviewing bot (PR-Agent, Claude Code Action, …) plugs in through GitHub itself — the workflow reads its comments with `gh`, so the reviewer is swappable.

## Repository layout

- [`workflow.md`](workflow.md) — the shared stage contract (the substance)
- [`skills/`](skills/) — readable mirror of the shipped skills. **The CLI is canonical**: `flicker skill install --workflow` installs exactly these, embedded in the binary you already have.
- [`docs/bring-your-own-tracker.md`](docs/bring-your-own-tracker.md) — fork the workflow, swap Flicker for your tracker
- [`docs/document-format.md`](docs/document-format.md) — the document/memory interchange format

## Not using Flicker?

The workflow's only integration surface is ~14 CLI commands (list/create/show tickets, transition statuses, read/write documents, search/add memory). Fork this repo, swap those commands for your tracker's equivalents, and everything else — the stages, the gates, the review loop — carries over unchanged. [Full guide](docs/bring-your-own-tracker.md).

## License

MIT — see [LICENSE](LICENSE).
