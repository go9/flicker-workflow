---
name: flicker-implement
description: Implement an approved Flicker task contract with baseline, worktree, scoped code, tests, PR, and implementation evidence. Use when asked to code or continue a selected/in-progress ticket; do not use for planning, independent verdicts, or release.
---

# flicker-implement

Follow the companion `flicker-workflow` contract, section `/flicker-implement`.

## Stage contract

- START by checking agent-config freshness: `flicker harness sync --check` (exit 0 fresh, exit 1 stale, writes nothing). REPORT the result either way, including "fresh" and including a legitimate skip (no project bound here, or no config assigned to it). NEVER block the stage on it; say what is stale, offer `flicker harness sync`, and carry on. Use `flicker harness doctor` when the work adds or changes agent config, or when `--check` is clean but the config still looks wrong — `--check` compares against the last sync, `doctor` compares against the bytes on disk.
- Begin by searching memory for this work and REPORT what came back, including "nothing relevant" — a stage that silently found nothing is indistinguishable from one that never looked. Treat `historical` hits as prior decisions (read them, never present them as current) and `unknown` as unresolvable, never as current.
- Before finishing, write a memory note IF you learned something that would change a future decision — a root cause, a rejected approach and why, a constraint found the hard way, a false claim corrected. Do not write status updates or restatements of the diff; noise is what makes a memory system worthless.
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
