---
name: flicker-implement
description: For projects tracked in Flicker Tickets. Implement selected Flicker tickets by reading current contracts, moving selected work to in_progress, coding narrowly, writing implementation notes, and recording durable memory. Use when the user asks to implement a Flicker ticket or continue selected work.
---

# flicker-implement

Use the shared workflow contract in the `flicker-workflow` skill installed alongside this one, section `/flicker-implement`.

## Adapter behavior

- Resolve an explicit ticket id or choose from `selected_for_dev` tickets.
- Read current document heads before editing code.
- Run `flicker ticket start <id>` when the ticket is `selected_for_dev`.
- Implement only the `task_contract` scope on a **feature branch** (never the default branch).
- Push the feature branch (safe, no deploy) and open a **PR** stamped with the ticket id; the ticket stays `in_progress`.
- Write `implementation_notes` (include the PR URL) before handing off to testing.
- Do not mark the ticket complete; `/flicker-test` drives the PR review loop, `/flicker-release` merges.
- Do not push to the default branch / deploy / merge without explicit current-turn approval.

## Required commands

```bash
flicker ticket list --json
flicker ticket show <id> --json
flicker ticket document read <id> task_contract --json
flicker ticket document read <id> plan_consensus --json
flicker ticket start <id> --json
gh pr create --title "<summary> (flicker #<id>)" --body "<links the ticket>"
flicker ticket document write <id> implementation_notes --title "Implementation notes" --body "<markdown incl. PR URL>" --json
flicker memory add "<body>" --title "<title>" --json
```
