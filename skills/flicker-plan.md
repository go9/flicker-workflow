---
name: flicker-plan
description: Shape a request into approved Flicker planning documents and selection-ready scope. Use when asked to research, clarify, scope, plan, ticket, or define acceptance; do not use for implementing an approved contract or only recalling prior decisions.
---
<!-- Generated from orlando-umbrella/flicker@84c115fcc08c5c765955a58c37a99744830a5cc8 by scripts/publish-workflow-mirror.sh. Do not edit. -->

# flicker-plan

Follow the companion `flicker-workflow` contract, section `/flicker-plan`.

## Stage contract

- Search current tickets, document heads, memory, repository evidence, prior art, and authoritative upstream sources before asking discoverable questions. Report what repository and upstream evidence was inspected; never imply research that was not performed.
- Ask only consequential unresolved decisions; present choices, consequences, and a recommendation. Prefer a structured question UI when available.
- Write the required `feature_brief`, `plan_consensus`, `task_contract`, and applicable `design` body contracts.
- Report target purpose, callers/dependents, contracts/invariants, nearby tests/gaps, risk, prior-art source plus `adopt | adapt | compose | reference | build` disposition, explicit non-goals, behavior-to-verification pairs, negative paths, and end-to-end evidence.
- Planning remains non-writing. When feasibility requires executable code, propose an explicitly approved child spike ticket that enters `/flicker-implement` with normal worktree and evidence rules.
- Vertically slice broad work. Do not select until scope is mapped, material questions are resolved, evidence is defined, and approval is explicit.

## Required public commands

```bash
flicker ticket list --json
flicker memory search "<query>" --json
flicker ticket show <id> --json
flicker ticket document read <id> <kind> --json
flicker ticket create "<title>" --body "<brief>" --json
flicker ticket document write <id> <kind> --title "<title>" --body "<contract markdown>" --json
flicker ticket select-for-dev <id> --json
```
