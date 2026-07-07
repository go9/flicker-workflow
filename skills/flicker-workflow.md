---
name: flicker-workflow
description: The shared Flicker agent workflow contract — canonical ticket statuses, transitions, document kinds, and the plan/implement/test/release/ship/recall stage procedures. The flicker-plan, flicker-implement, flicker-test, flicker-release, flicker-ship, and flicker-recall skills all follow this contract. Read the relevant section when running any of those stages.
---

# Flicker Agent Workflow Core

This is the shared contract for all Flicker agent workflow skills. The stage skills (flicker-plan, flicker-implement, flicker-test, flicker-release, flicker-ship, flicker-recall) stay thin: they call into this workflow and use the public `flicker` CLI/API only.

## Requirements

- The `flicker` CLI must be installed and authenticated (`flicker auth login <key>`).
- A default project must be set with `flicker project use <slug>` or supplied with `--project <slug>`.
- Skills must use canonical ticket statuses only:
  - `backlog`
  - `selected_for_dev`
  - `in_progress`
  - `done`
- Skills must use canonical transitions only:
  - `select-for-dev`
  - `start`
  - `complete`
  - `reopen`
  - `defer`

> Status note: `in_progress` covers the whole active loop — coding, the PR, and the review rounds. A ticket leaves `in_progress` for `done` only when its PR merges (see "PR + review loop"). Do not invent non-canonical statuses — keep the review loop inside `in_progress`.

## Public CLI surface

Use these public commands as the integration boundary:

```bash
flicker ticket list --json
flicker ticket tree --json
flicker ticket show <id> --json
flicker ticket create "<title>" --body "<markdown>" [--parent <id>] --json
flicker ticket select-for-dev <id> --json
flicker ticket start <id> --json
flicker ticket complete <id> --json
flicker ticket reopen <id> --json
flicker ticket defer <id> --json
flicker ticket document read <id> <kind> [--history] --json
flicker ticket document write <id> <kind> --title "<title>" --body "<markdown>" --json
flicker ticket checkout [project] --out .flicker/tickets
flicker ticket push .flicker/tickets/<ticket>.md
flicker memory search "<query>" --json
flicker memory add "<body>" --title "<title>" --json
```

GitHub coordination uses the `gh` CLI (PRs and review state live on GitHub, not in Flicker):

```bash
gh pr create --title "<title> (flicker #<id>)" --body "<body, links the ticket>"
gh pr view <n> --json reviews,comments,statusCheckRollup
gh pr merge <n> --squash   # ONLY with explicit approval — merge may deploy
```

Document kinds:

- `feature_brief`
- `plan_consensus`
- `task_contract`
- `design`
- `implementation_notes`
- `review`
- `regression`
- `test_verdict`
- `release`

## Hard rules for all workflows

1. Do not silently invent work outside the active ticket/contract.
2. If substantive new work is discovered, create a child ticket or record a memory note; do not bury it in prose only.
3. Treat current ticket fields and current document heads as current truth.
4. Treat events and older document versions as historical evidence.
5. Never push to the default branch, deploy, publish, merge, upload, or release without explicit user approval in the current turn.
6. Prefer local narrow tests first. Record commands and outcomes in documents/events.
7. Use `--json` when a skill needs machine-readable output.
8. If a CLI command returns HTTP 409/conflict, stop and ask the user whether to re-pull/rebase local edits.
9. If no project context is configured, ask for a project slug or instruct the user to run `flicker project use <slug>`.
10. Code changes ship as **pull requests**, never direct commits to the default branch. Pushing a *feature* branch is safe (it does not deploy); only a merge to the default branch deploys. Chunky PRs are fine, but a PR must exist.
11. **Review is rented, not built.** A pluggable PR reviewer (e.g. self-hosted PR-Agent, or the Claude Code GitHub Action) reviews each PR. Never build a bespoke review engine. The agent coordinates with the reviewer *through GitHub* (reads its PR comments via `gh`), not via a direct integration.

## PR + review loop

The pipeline maps onto the canonical statuses like this:

```
backlog (tag: v1/v2/...) → selected_for_dev → in_progress ──────────────┐
                                              (code → PR → review rounds) │
                                                                          ▼
                                                          merge PR (with approval)
                                                                          ▼
                                                                        done
won't-do = defer the ticket + tag `won't-do` + close the PR unmerged
```

Coordination model (the agent never talks to the reviewer directly — **GitHub is the bus**):

1. The implementing agent opens a PR stamped with the ticket id; the ticket stays `in_progress`.
2. The pluggable reviewer reviews the PR automatically on open and on every push. It is async — wait for it to post on the **current head SHA** before reading.
3. The agent reads the review via `gh pr view <n> --json reviews,comments`, triages (act on real issues, skip nitpicks), fixes, pushes. The reviewer re-reviews the delta. Loop — but **cap at ~2-3 rounds**, then escalate to a human (AI-reviewer ↔ agent can ping-pong forever).
4. **The merge is the gate to `done`, and it requires explicit human approval** (merge = prod deploy on auto-deploy repos). An AI reviewer's "looks good" is necessary, not sufficient.
5. On approval, merge the PR, then `flicker ticket complete <id>`.

Keep the reviewer pluggable: the workflow assumes *some* reviewer is installed on the repo, but never depends on a specific vendor's API.

## Tags and parked work

Backlog is not a dumping ground. Use tags to carry intent the status can't:

- **Timing tags** `v1` / `v2` / `v3` ... = roughly when we intend to do it. `backlog` = not now; the tag says when.
- **`won't-do`** = abandoned (a tag, not a dead status lane). Close the PR unmerged and `flicker ticket defer`.
- Status carries *where in the pipeline*; tags carry *when / disposition*.

> Interim until first-class tags ship: prefix the title with `[v2]` etc. Replace prefixes with real tags once available.

## `/flicker-plan`

Purpose: convert an idea/bug/request into ticketed, selected work.

Procedure:

1. Clarify the request only if needed to identify scope, project, appetite, or acceptance.
2. Search existing work and memory:
   ```bash
   flicker ticket list --json
   flicker memory search "<request terms>" --json
   ```
3. If an appropriate ticket exists, adopt it. Otherwise create one:
   ```bash
   flicker ticket create "<title>" --body "<feature brief>" --json
   ```
4. Write current documents:
   - `feature_brief` for problem, users, non-goals, risks.
   - `plan_consensus` for selected approach and rejected alternatives.
   - `task_contract` for exact implementation acceptance criteria.
   - `design` when UI/UX is in scope.
5. Record durable context with `flicker memory add` when useful.
6. Ask for approval before selecting work for dev if the user has not clearly approved it.
7. When approved, run:
   ```bash
   flicker ticket select-for-dev <id>
   ```

Output: ticket id, document kinds written, open questions, and recommended next command (`/flicker-implement <id>`).

## `/flicker-implement`

Purpose: implement approved selected work, on a branch, behind a PR.

Procedure:

1. Resolve the ticket. If omitted, list `selected_for_dev` tickets and choose the best match.
2. Read current truth:
   ```bash
   flicker ticket show <id> --json
   flicker ticket document read <id> task_contract --json
   flicker ticket document read <id> plan_consensus --json
   flicker ticket document read <id> design --json
   ```
3. If the ticket is `selected_for_dev`, run `flicker ticket start <id>` (moves it to `in_progress`).
4. Create a dedicated worktree off the default branch and do all work inside it: `git worktree add ../<repo>-<ticket> -b <branch>` (own working dir + own branch). A branch alone does not isolate the working tree — a concurrent session's checkout in the same clone can silently discard uncommitted edits. Solo single-session work MAY stay in the main clone, but any time more than one agent may touch the same repo the worktree is mandatory. Implement only the contract. Keep changes small and scoped. **Never commit to the default branch.**
5. Run narrow validation locally.
6. Push the **feature branch** (this does NOT deploy) and open a PR: `gh pr create --title "<summary> (flicker #<id>)" --body "<links the ticket + summary>"`. Chunky is fine; a PR must exist. The ticket stays `in_progress` through the PR + review loop.
7. Write `implementation_notes` with changed files, commands run, behavior changes, the **PR URL**, and intentionally-not-done.
8. Add memory notes for durable decisions or discoveries.
9. Do not mark complete; hand off to `/flicker-test`, which drives the PR review loop.

Output: branch name, PR URL, changed files, tests run, implementation notes document id/version, residual risks, recommended next command (`/flicker-test <id>`).

## `/flicker-test`

Purpose: drive the PR review loop and validate an implemented ticket.

Procedure:

1. Read `task_contract`, `implementation_notes`, and the PR.
2. Let the pluggable reviewer review the PR. Wait for it to post on the current head SHA, then read it:
   ```bash
   gh pr view <n> --json reviews,comments,statusCheckRollup
   ```
3. Triage the reviewer's comments (act on real issues, skip nitpicks), fix, push; the reviewer re-reviews the delta. Loop, but **cap at ~2-3 rounds**, then escalate to a human.
4. Also run appropriate local/regression checks against the change (and, where available, the ticket's preview env).
5. If substantive defects are found, create child tickets and keep the parent `in_progress`.
6. Write documents:
   - `review`
   - `regression`
   - `test_verdict`
7. On PASS, the ticket is **ready to merge** — but do NOT merge or complete here. Merge is the release gate (`/flicker-release`).
8. On fail, do not advance. Record findings with `flicker memory add` and report the blockers.

Output: PASS / REQUEST CHANGES verdict, reviewer rounds run, commands + evidence, child tickets created, PR URL, recommended next command (`/flicker-release <id>` on PASS).

## `/flicker-release`

Purpose: verify release readiness and, on explicit approval, merge (which may deploy) and complete the ticket.

Procedure:

1. Read ticket, `test_verdict`, `regression`, `review`, and `implementation_notes`.
2. Confirm the PR is green (reviewer satisfied + CI checks passing) and the acceptance criteria are met.
3. Check release notes, migrations, rollback notes, and deployment risk.
4. Write a `release` document with readiness, commands checked, and approval gates.
5. **Stop and require explicit user approval before merging** — on auto-deploy repos, merge = prod deploy.
6. On approval:
   ```bash
   gh pr merge <n> --squash
   flicker ticket complete <id>
   ```
7. If the work is abandoned instead: close the PR unmerged, `flicker ticket defer <id>`, and tag `won't-do`.

Output: release readiness verdict, required approvals, and exact next safe command(s).

## `/flicker-ship`

Purpose: autonomously take a `selected_for_dev` ticket all the way to merged, in one agent run. This is the combined `implement` + `test` + `release` loop with auto-merge, for agents the user spawns to clear the queue.

Procedure:

1. Resolve the ticket (arg) or pick the top `selected_for_dev` ticket (`flicker ticket list --json`).
2. Read current truth: `flicker ticket show <id> --json`, `task_contract`, `plan_consensus`, `design`.
3. `flicker ticket start <id>` (→ `in_progress`).
4. Create a dedicated worktree off the default branch and work inside it: `git worktree add ../<repo>-<ticket> -b <branch>` (own working dir + own branch). Spawned ship-agents commonly run concurrently in the same repo, so the worktree is mandatory here. Implement ONLY the `task_contract`. Keep it scoped. **Never commit to the default branch.**
5. SAFETY RAIL #1 — run the test suite locally; it MUST pass. If it can't be made green, stop, write `implementation_notes`, and escalate. Never open a mergeable PR with red tests.
6. Push the feature branch; open a PR (author = the seat-holding account) stamped with the ticket id. Write `implementation_notes` (PR URL included).
7. Review loop (until clean):
   - Wait on the reviewer's status check for the current head SHA (`gh pr view <n> --json statusCheckRollup` until the reviewer's checks complete).
   - Read inline comments (`gh pr view <n> --json comments`; `gh api repos/<owner>/<repo>/pulls/<n>/comments`).
   - Fix actionable items; auto-resolve nitpicks; push. The reviewer re-reviews the delta. Repeat UNTIL CLEAN (0 actionable).
   - CIRCUIT-BREAKER: stop and escalate (leave the PR open, comment the blocker) if there is no progress (same issues recur / actionable count stops dropping) or a token/time budget is exhausted. "Until clean" with a brake, not infinite.
8. SAFETY RAIL #2 — danger zones: if the change touches security-sensitive infrastructure, billing/money paths, or DB migrations (define the exact list per repo), DO NOT auto-merge. Mark the PR ready, comment, and escalate to a human.
9. Auto-merge ONLY when: reviewer clean (0 actionable) AND tests green AND no danger-zone files. Then `gh pr merge <n> --squash` (this may deploy).
10. `flicker ticket complete <id>` (→ `done`). Add a release memory note.

Output: ticket id, PR URL, rounds run, merged-or-escalated, deploy status, final ticket status.

Notes:
- On auto-deploy repos, merge = prod deploy; the safety rails (tests green, danger-zone exclusion) are the substitute for a human merge gate.

## `/flicker-recall`

Purpose: search tickets, current documents, and historical memory.

Procedure:

1. Run targeted searches:
   ```bash
   flicker memory search "<query>" --json
   flicker ticket list --json
   ```
2. Label results by source class:
   - current ticket
   - current document
   - historical event
   - superseded event
3. Prefer current ticket fields and current document heads when they conflict with historical events.
4. Summarize with provenance and uncertainty.

Output: concise answer with source labels and ticket/document references.
