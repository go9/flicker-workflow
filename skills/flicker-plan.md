---
name: flicker-plan
description: For projects tracked in Flicker Tickets. Plan Flicker work by searching/adopting/creating tickets, writing planning documents, recording memory, and selecting approved work for development. Use when the user asks to plan, shape, ticket, scope, or prepare work in Flicker.
---

# flicker-plan

Use the shared workflow contract in the `flicker-workflow` skill installed alongside this one, section `/flicker-plan`.

## Adapter behavior

- Use the public `flicker` CLI only.
- Search existing tickets and memory before creating new tickets.
- Write `feature_brief`, `plan_consensus`, `task_contract`, and `design` when applicable.
- Ask for approval before running `flicker ticket select-for-dev <id>` unless approval is explicit.
- Keep the user-facing result concise: ticket id, documents written, open questions, and next command.

## Required commands

```bash
flicker ticket list --json
flicker memory search "<query>" --json
flicker ticket create "<title>" --body "<brief>" --json
flicker ticket document write <id> feature_brief --title "Feature brief" --body "<markdown>" --json
flicker ticket document write <id> plan_consensus --title "Plan consensus" --body "<markdown>" --json
flicker ticket document write <id> task_contract --title "Task contract" --body "<markdown>" --json
flicker ticket select-for-dev <id> --json
```
