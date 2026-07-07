# Bring your own tracker

The workflow is a contract; Flicker is its reference implementation. Every stage skill talks to the tracker through a small set of CLI commands and nothing else — no private APIs, no webhooks, no database access. Swap those commands and the whole workflow (stages, statuses, documents, gates, review loop) carries over.

## The seam: ~14 commands

This is the complete integration surface, as used throughout [workflow.md](../workflow.md):

| Capability | Flicker command |
|---|---|
| List work | `flicker ticket list --json` |
| Ticket detail | `flicker ticket show <id> --json` |
| Create work | `flicker ticket create "<title>" --body "<md>" [--parent <id>] --json` |
| Transition: approve for dev | `flicker ticket select-for-dev <id>` |
| Transition: start | `flicker ticket start <id>` |
| Transition: finish | `flicker ticket complete <id>` |
| Transition: reopen / park | `flicker ticket reopen <id>` / `flicker ticket defer <id>` |
| Read a planning document | `flicker ticket document read <id> <kind> --json` |
| Write a planning document | `flicker ticket document write <id> <kind> --title "…" --body "<md>" --json` |
| Search durable memory | `flicker memory search "<query>" --json` |
| Record durable memory | `flicker memory add "<body>" --title "…" --json` |

Plus `gh` for the PR/review loop — which is tracker-independent already.

## What your replacement must provide

1. **Four statuses** (or a mapping onto yours): `backlog`, `selected_for_dev`, `in_progress`, `done`. The load-bearing one is `selected_for_dev` — the explicit human "yes, build this" gate agents pick up from.
2. **Versioned documents per work item** for the nine kinds (`feature_brief`, `plan_consensus`, `task_contract`, `design`, `implementation_notes`, `review`, `regression`, `test_verdict`, `release`). Any mechanism works: wiki pages, issue comments with markers, files in a directory keyed by issue number. Append-only beats editable.
3. **Searchable, append-only memory.** A labeled issue, a JSONL file, a notes tool with an API — anything an agent can search and append to but not silently rewrite.

## Example mapping: GitHub Issues

| Workflow verb | `gh` equivalent |
|---|---|
| `ticket list` | `gh issue list --json number,title,labels,state` |
| `ticket show` | `gh issue view <n> --json body,labels,comments` |
| `ticket create` | `gh issue create --title … --body …` |
| `select-for-dev` / `start` / `complete` | labels (`status:selected`, `status:in-progress`) + `gh issue close` |
| `document read/write` | delimited, marker-bounded sections in issue comments, or `docs/tickets/<n>/<kind>.md` in-repo |
| `memory search/add` | a pinned `memory` issue with appended comments, or JSONL in-repo + `grep` |

Linear, Jira, and friends map the same way through their CLIs/APIs; the statuses and document kinds are the invariant, the transport is yours.

## How to fork

1. Fork this repo.
2. Rewrite the **Required commands** blocks in each skill under [`skills/`](../skills/) and the command examples in [workflow.md](../workflow.md) to your tracker's equivalents. Everything outside those blocks — adapter behavior, hard rules, gates — stays.
3. Install the skills into your harness by hand (each file in `skills/` is a complete skill document: Claude Code reads `.claude/skills/<name>/SKILL.md`, Codex reads `AGENTS.md`, Pi reads `.pi/skills/<name>.md`).
4. Keep the hard rules. Especially: no implementation before an approved contract, and no merge/deploy without explicit human approval. They are the point.

## What not to fork away

The gates are the workflow. If your fork drops "agents only pick up `selected_for_dev` work" or "merge requires a human," what remains is an autocomplete with a ticket habit — you'll get speed and lose trust. Swap the tracker, keep the discipline.
