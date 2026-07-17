---
name: flicker-release
description: Adversarially verify release readiness and perform only explicitly authorized merge/deploy actions for tested Flicker work. Use when asked for readiness, merge, deploy, publish, release notes, or rollback planning; do not use for rollback execution, coding, or full pickup-to-ship automation.
---
<!-- Generated from orlando-umbrella/flicker@84c115fcc08c5c765955a58c37a99744830a5cc8 by scripts/publish-workflow-mirror.sh. Do not edit. -->

# flicker-release

Follow the companion `flicker-workflow` contract, section `/flicker-release`.

## Stage contract

- Read current contract/evidence plus actual PR head, reviewer, CI, and diff.
- Try to refute readiness: stale head, uncovered criterion, scope drift, failing check, danger zone, data/migration risk, or absent rollback/post-deploy plan.
- Write `release` as `READY` or `NOT READY` with current head SHA, current-head review/CI/acceptance evidence, evidence versions, authority status, and risk. Separately label the exact gated merge/deploy command and the safe current action; without authority, never present the gated command as the action to run.
- Stop before merge/deploy/publish/upload unless authority is explicit in this turn. Danger zones always require human approval.
- When authorized, merge and verify the merge/deploy/post-deploy outcome as applicable; only then run `complete`.

## Required public commands

```bash
flicker ticket show <id> --json
flicker ticket document read <id> test_verdict --json
flicker ticket document read <id> regression --json
flicker ticket document read <id> review --json
flicker ticket document read <id> implementation_notes --json
gh pr view <n> --json headRefOid,reviews,comments,statusCheckRollup
flicker ticket document write <id> release --title "Release readiness" --body "<READY or NOT READY evidence>" --json
gh pr merge <n> --squash # explicit current-turn authority only
flicker ticket complete <id> --json
```
