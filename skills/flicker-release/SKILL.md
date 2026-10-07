---
name: flicker-release
description: Adversarially verify release readiness and perform only explicitly authorized merge/deploy actions for tested Flicker work. Use when asked for readiness, merge, deploy, publish, release notes, or rollback planning; do not use for rollback execution, coding, or full pickup-to-ship automation.
---

# flicker-release

Follow the companion `flicker-workflow` contract, section `/flicker-release`.

## Stage contract

- Begin by searching memory for this work and REPORT what came back, including "nothing relevant" — a stage that silently found nothing is indistinguishable from one that never looked. Treat `historical` hits as prior decisions (read them, never present them as current) and `unknown` as unresolvable, never as current.
- Before finishing, write a memory note IF you learned something that would change a future decision — a root cause, a rejected approach and why, a constraint found the hard way, a false claim corrected. Do not write status updates or restatements of the diff; noise is what makes a memory system worthless.
- Read current contract/evidence plus actual PR head, reviewer, CI, and diff. Accept a Flicker ticket `review` document as reviewer evidence in place of a PR-Agent comment only when its `Head SHA` exactly matches the PR `headRefOid` and its verdict is `CLEAN`; missing or mismatched evidence is stale and blocks readiness. Any new commit requires a fresh `/flicker-review`; unresolved `FINDINGS` block readiness.
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
