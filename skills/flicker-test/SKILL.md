---
name: flicker-test
description: Independently review and test implemented Flicker work, map acceptance to evidence, and issue PASS or REQUEST CHANGES. Use when asked to validate, regress, review, or test a ticket; do not use for initial coding or merge/release.
---

# flicker-test

Follow the companion `flicker-workflow` contract, section `/flicker-test`.

## Stage contract

- Begin by searching memory for this work and REPORT what came back, including "nothing relevant" — a stage that silently found nothing is indistinguishable from one that never looked. Treat `historical` hits as prior decisions (read them, never present them as current) and `unknown` as unresolvable, never as current.
- Before finishing, write a memory note IF you learned something that would change a future decision — a root cause, a rejected approach and why, a constraint found the hard way, a false claim corrected. Do not write status updates or restatements of the diff; noise is what makes a memory system worthless.
- Read the current contract, implementation evidence, actual diff, PR, and head SHA; do not trust a handoff summary alone.
- Re-run an original failure first for bug fixes. Every behavioral change gets relevant changed-area regression; risk only adds checks.
- Map every acceptance id to a separately labeled expected proof and actual command/manual result, including explicit missing-proof entries, negative paths, and UI states when applicable. Green aggregate tests cannot hide an uncovered acceptance id.
- Require reviewer evidence for the current head. Accept a Flicker ticket `review` document with `Head SHA` equal to the PR's `headRefOid`; its verdict must be `CLEAN` to pass. A missing document or mismatched SHA is missing/stale evidence: stop and request `/flicker-review`. A `FINDINGS` verdict requires resolution and a new review after the fix commit. This is reviewer evidence in place of a PR-Agent comment; never infer freshness from document recency.
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
