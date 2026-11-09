---
name: flicker-release
description: Adversarially verify release readiness of tested Flicker work and merge or deploy only with explicit authority. Use when asked for readiness, merge, deploy, publish, release notes, or rollback planning; do not use for rollback execution, coding, or full pickup-to-ship automation.
---

# flicker-release

Try to prove the work is not ready; merge only when that fails and authority is explicit. Templates, outcomes, and gates are in the companion `flicker-workflow` contract; load only the section a step names.

## Stage contract

- Use after `/flicker-test` wrote `PASS`. Coding goes to `/flicker-implement`; a full pickup-to-merge run is `/flicker-ship`.
- Authority: write `release`. Merge, deploy, publish, and upload only with explicit authority in the current turn. Danger zones and one-way doors always need a person's approval.
- Unknowns fail closed: missing or stale evidence is `NOT READY`.
- End with one outcome: `go` (merged and done), `needs a person` (approval), `rejected` (a blocker, with its remedy), or `retry`.

## Steps

1. **Search memory.** Search memory for the ticket and report the result (see *Memory*). Done when: your report states what came back.
2. **Read the current state.** Read the ticket, `task_contract`, `implementation_notes`, `review`, `regression`, `test_verdict`, the PR head SHA, its CI checks, and its diff. Done when: every document's head SHA has been compared with the PR's `headRefOid`.
3. **Try to refute readiness.** Look for a stale head, an uncovered acceptance row, a missing command result, scope drift, a failing check, a danger zone, a migration or data risk, and a missing rollback or post-deploy plan. Done when: each item is marked clear or named as a blocker.
4. **Write the release document.** Write `release` as `READY` or `NOT READY` from the template, with the gated command and the safe current action labeled separately. Done when: the document write returned a version.
5. **Merge only with authority.** Merge only when the current turn grants it and no danger zone needs a person. Done when: `gh pr view` shows the PR merged, or the stage ends with outcome `needs a person` naming the approval needed.
6. **Verify, then complete.** After a merge, check the merge commit and any deploy or post-deploy result that applies; then run `flicker ticket complete`. Done when: a fresh `flicker ticket show` reads `done`.
7. **Retro on a sample.** When the PR number ends in 0, or the work needed more than one fix round, write a short retro: each mechanical mistake becomes a proposed check, each judgment mistake a proposed review rule, filed as one `backlog` ticket. Done when: the retro ticket id is in your report, or the report says no retro was due.

## Required public commands

```bash
flicker memory search "<ticket keywords>" --json
flicker ticket show <id> --json
flicker ticket document read <id> test_verdict --json
flicker ticket document read <id> regression --json
flicker ticket document read <id> review --json
flicker ticket document read <id> implementation_notes --json
gh pr view <n> --json headRefOid,state,mergeCommit,reviews,comments,statusCheckRollup
flicker ticket document write <id> release --title "Release readiness" --body "<READY or NOT READY evidence>" --json
gh pr merge <n> --squash # explicit current-turn authority only
flicker ticket complete <id> --json
flicker ticket create "Retro: <PR>" --body "<mistakes, proposed checks and review rules>" --json
```
