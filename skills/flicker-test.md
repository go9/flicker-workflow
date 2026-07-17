---
name: flicker-test
description: Independently review and test implemented Flicker work, map acceptance to evidence, and issue PASS or REQUEST CHANGES. Use when asked to validate, regress, review, or test a ticket; do not use for initial coding or merge/release.
---
<!-- Generated from orlando-umbrella/flicker@84c115fcc08c5c765955a58c37a99744830a5cc8 by scripts/publish-workflow-mirror.sh. Do not edit. -->

# flicker-test

Follow the companion `flicker-workflow` contract, section `/flicker-test`.

## Stage contract

- Read the current contract, implementation evidence, actual diff, PR, and head SHA; do not trust a handoff summary alone.
- Re-run an original failure first for bug fixes. Every behavioral change gets relevant changed-area regression; risk only adds checks.
- Map every acceptance id to a separately labeled expected proof and actual command/manual result, including explicit missing-proof entries, negative paths, and UI states when applicable. Green aggregate tests cannot hide an uncovered acceptance id.
- Require reviewer evidence for the current head. Bound waits/rounds and stop on missing reviewer, stale review, or no progress.
- Keep in-scope blockers on this ticket; create children only for out-of-scope independent follow-up.
- Write `review`, `regression`, and an exact `PASS` or `REQUEST CHANGES` `test_verdict`. Never merge or complete here.

## Required public commands

```bash
flicker ticket show <id> --json
flicker ticket document read <id> task_contract --json
flicker ticket document read <id> implementation_notes --json
gh pr view <n> --json headRefOid,reviews,comments,statusCheckRollup
flicker ticket document write <id> review --title "Review" --body "<evidence>" --json
flicker ticket document write <id> regression --title "Regression" --body "<criterion map>" --json
flicker ticket document write <id> test_verdict --title "Test verdict" --body "<PASS or REQUEST CHANGES>" --json
```
