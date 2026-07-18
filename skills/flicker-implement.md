---
name: flicker-implement
description: Implement an approved Flicker task contract with baseline, worktree, scoped code, tests, PR, and implementation evidence. Use when asked to code or continue a selected/in-progress ticket; do not use for planning, independent verdicts, or release.
---
<!-- Generated from orlando-umbrella/flicker@84c115fcc08c5c765955a58c37a99744830a5cc8 by scripts/publish-workflow-mirror.sh. Do not edit. -->

# flicker-implement

Follow the companion `flicker-workflow` contract, section `/flicker-implement`.

## Stage contract

- Read all current planning heads and stop on stale or contradictory scope.
- Verify selected/in-progress status, intended base/head, dedicated worktree when concurrency is possible, and a relevant green baseline. Record the exact pre-edit baseline command, exit code, output, and whether any failure is confirmed pre-existing; stop rather than silently coding over an unexplained red baseline.
- Keep one named writer per worktree. For bugs, reproduce the original failure first or record why reproduction is impossible.
- Deliver a vertical/tracer slice that leaves the system working; avoid drive-by refactors and default-branch writes.
- Run changed-area regression tests plus additive risk checks. Push/open a PR only when the approved run authorizes remote collaboration.
- Write complete `implementation_notes`: contract version, one-writer/worktree, exact baseline result, changed files, tests added/updated, every command with exit/output, base/head, PR, criterion coverage, decisions, residual risks, and intentionally not done. Never fabricate a run, result, file, or SHA.
- Never complete or merge; hand off to `flicker-test`.

## Required public commands

```bash
flicker ticket show <id> --json
flicker ticket document read <id> task_contract --json
flicker ticket document read <id> plan_consensus --json
flicker ticket start <id> --json
gh pr create --title "<summary> (flicker #<id>)" --body "<ticket, scope, evidence>"
flicker ticket document write <id> implementation_notes --title "Implementation notes" --body "<evidence>" --json
```
