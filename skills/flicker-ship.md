---
name: flicker-ship
description: Take one approved Flicker ticket through implementation, testing, release gates, and authorized normal-path merge in one run. Use only for an explicit end-to-end ship request; do not use for vague ship language, planning, or danger-zone auto-merge.
---
<!-- Generated from orlando-umbrella/flicker@84c115fcc08c5c765955a58c37a99744830a5cc8 by scripts/publish-workflow-mirror.sh. Do not edit. -->

# flicker-ship

Follow the companion `flicker-workflow` contract, section `/flicker-ship`.

## Stage contract

- Confirm a named/selected ticket and scoped current-turn end-to-end authority; ambiguous requests require clarification.
- Execute every implement, test, and release evidence contract without shortcuts. Explicitly record the dedicated worktree and its one writer in the ship handoff.
- Require changed-area regression, current-head clean review, green CI, acceptance mapping, rollback/post-deploy notes, and no unresolved findings.
- Circuit-break on red tests, missing/stale reviewer, non-decreasing findings, budget exhaustion, contradiction, or ambiguity; leave durable safe handoff evidence.
- Never auto-merge a danger-zone change. Only the explicitly authorized non-danger path may merge; verify the outcome before `complete`.

## Required public commands

```bash
flicker ticket show <id> --json
flicker ticket start <id> --json
gh pr create --title "<summary> (flicker #<id>)" --body "<ticket, scope, evidence>"
gh pr view <n> --json headRefOid,reviews,comments,statusCheckRollup
gh pr merge <n> --squash # only within explicit scoped authority and outside danger zones
flicker ticket complete <id> --json
flicker memory add "<release evidence>" --title "Release note" --json
```
