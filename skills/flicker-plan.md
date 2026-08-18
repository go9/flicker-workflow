---
name: flicker-plan
description: Shape a request into approved Flicker planning documents and selection-ready scope. Use when asked to research, clarify, scope, plan, ticket, or define acceptance; do not use for implementing an approved contract or only recalling prior decisions.
---

# flicker-plan

Follow the companion `flicker-workflow` contract, section `/flicker-plan`.

## Stage contract

- START by checking agent-config freshness: `flicker harness sync --check` (exit 0 fresh, exit 1 stale, writes nothing). REPORT the result either way, including "fresh" and including a legitimate skip (no project bound here, or no config assigned to it) — a check that speaks up only when unhappy is indistinguishable from one that never ran. NEVER block the stage on it; stale config is a finding, not a gate. Planning a project on stale instructions is planning against the wrong constraints. Use `flicker harness doctor` when `--check` is clean but the config still looks wrong, or when the plan itself touches agent config.
- Search current tickets, document heads, memory, repository evidence, prior art, and authoritative upstream sources before asking discoverable questions. Report what repository and upstream evidence was inspected; never imply research that was not performed.
- Memory hits carry a temporal state: read `historical` ones as prior decisions and never present them as current, and never present `unknown` as current. Use `flicker memory expand` when a hit mentions something it does not explain — the decision that caused X is often one link away and shares no vocabulary with the query.
- Write a memory note when planning surfaces something that would change a FUTURE decision (a rejected approach and why, a constraint found the hard way, a false claim corrected). Not status updates, and not a restatement of the brief.
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
