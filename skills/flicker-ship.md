---
name: flicker-ship
description: For projects tracked in Flicker Tickets. Autonomously take a selected Flicker ticket from pickup to merged — start, implement on a branch, open a PR, loop with the pluggable reviewer until clean, run tests, and auto-merge within safety rails (tests must be green; danger zones escalate to a human). Use when the user wants an agent to fully ship a ticket end to end.
---

# flicker-ship

Use the shared workflow contract in the `flicker-workflow` skill installed alongside this one, section `/flicker-ship`.

## Adapter behavior

- Resolve an explicit ticket id or pick the top `selected_for_dev` ticket.
- `flicker ticket start <id>`; implement only the `task_contract` on a feature branch.
- Run the test suite; it MUST pass before any merge (safety rail #1).
- Open a PR (author = the seat-holding account) stamped with the ticket id; write `implementation_notes`.
- Review loop: wait on the reviewer's status check, read its comments, fix actionable items, auto-resolve nitpicks, push; repeat UNTIL CLEAN. Circuit-breaker on no-progress/budget -> escalate.
- Danger zones (security-sensitive infrastructure / billing / DB migrations — define per repo) -> do NOT auto-merge; mark ready and escalate to a human (safety rail #2).
- Auto-merge ONLY when reviewer is clean + tests green + no danger-zone files. Then `flicker ticket complete` + add a release memory note.

## Required commands

```bash
flicker ticket list --json
flicker ticket show <id> --json
flicker ticket start <id> --json
gh pr create --title "<summary> (flicker #<id>)" --body "<links the ticket>"
gh pr view <n> --json reviews,comments,statusCheckRollup
gh pr merge <n> --squash
flicker ticket complete <id> --json
flicker memory add "<body>" --title "<title>" --json
```
