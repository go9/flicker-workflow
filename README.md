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

That's the entire setup. This repository is the editable canonical source; released CLI binaries vendor pinned copies so installation needs no clone or network access.

## The shape of it

| Stage | Skill | What it owns |
|---|---|---|
| **Plan** | `flicker-plan` | Check whether it already exists, shape the smallest useful scope, write `feature_brief` / `plan_consensus` / `task_contract`, ask the owner late and little, select approved work |
| **Implement** | `flicker-implement` | Dedicated worktree, failing test first (proved by reverting the fix), code only the contract, open a PR, write `implementation_notes` |
| **Test** | `flicker-test` | Re-check the builder's claims, map every acceptance row to evidence, check the current-head review, write a `test_verdict` |
| **Review** | `flicker-review` | From a session that did not write the diff: review correctness and spec, write a SHA-bound `review` with `Verdict: CLEAN` or `FINDINGS` |
| **Release** | `flicker-release` | Verify evidence, then merge **only with explicit human approval** (merge may deploy) |
| **Ship** | `flicker-ship` | The autonomous end-to-end loop, inside safety rails: tests must be green, danger zones escalate to a human |
| **Recall** | `flicker-recall` | Search tickets, current documents, and historical memory with provenance labels |
| **Triage** | `flicker-triage` | Group end-user suggestions, link accepted reports to tickets, and write reporter-facing rejections |
| **Health watchdog** | `flicker-health-watchdog` | Read live Flicker infrastructure state and report evidence without mutation |

Each stage skill is a short numbered procedure in which every step ends on a "Done when" test, written so cheap models can follow it. The shared contract (statuses, transitions, document templates, the five outcomes, asking rules, review and danger-zone gates) is in [workflow.md](workflow.md); stage steps reference its sections by name.

## Why it works for agents

- **Tickets are the single source of truth.** Agents pick up only work that a human selected for development; status transitions are mandatory, so a watched in-progress list never lies.
- **Documents beat chat memory.** Plans, contracts, review verdicts, and release evidence are versioned documents attached to the ticket — the next agent (or the same agent after a context reset) reads current truth instead of reconstructing it.
- **Memory is append-only evidence.** Decisions and discoveries land in project memory, searchable later, never silently rewritten.
- **Approval gates are explicit.** No implementation before an approved contract; no merge/deploy without a human's explicit yes. Autonomy happens inside the rails, not instead of them.
- **Review is SHA-bound and swappable.** A review counts only as a `review` ticket document for the head SHA it names, written by a session that did not write the diff; a PR bot's comments are its input. Reviews check correctness and the spec (missing, unrequested, and wrong work) separately.
- **Claims need tool results.** Every stage ends with one of five outcomes (`go`, `already done`, `rejected`, `needs a person`, `retry`) and reports only what a command result showed.

## Repository layout

- [`skills/`](skills/) — editable canonical workflow contract and skills, each in `<name>/SKILL.md` form for public import. Flat `skills/<name>.md` files remain compatibility copies for existing raw-path consumers.
- [`workflow.md`](workflow.md) — readable projection of the shared contract.
- Released Flicker CLI binaries vendor an immutable public commit from this repository for offline `flicker skill install --workflow`.
- [`docs/bring-your-own-tracker.md`](docs/bring-your-own-tracker.md) — fork the workflow, swap Flicker for your tracker
- [`docs/document-format.md`](docs/document-format.md) — the document/memory interchange format

## Validate

```bash
python3 test/skill_contract_test.py
```

This checks skill inventory, frontmatter, public-safe paths, editable-source provenance, and health/triage separation.

## Not using Flicker?

The workflow's only integration surface is ~14 CLI commands (list/create/show tickets, transition statuses, read/write documents, search/add memory). Fork this repo, swap those commands for your tracker's equivalents, and everything else — the stages, the gates, the review loop — carries over unchanged. [Full guide](docs/bring-your-own-tracker.md).

## License

MIT — see [LICENSE](LICENSE).
