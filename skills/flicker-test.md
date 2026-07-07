---
name: flicker-test
description: For projects tracked in Flicker Tickets. Review and validate Flicker ticket implementation by reading contracts and notes, running checks, writing review/regression/test verdict documents, creating child tickets for findings, and completing only passing work.
---

# flicker-test

Use the shared workflow contract in the `flicker-workflow` skill installed alongside this one, section `/flicker-test`.

## Adapter behavior

- Read `task_contract`, `implementation_notes`, and the PR first.
- Drive the PR review loop: let the pluggable reviewer review, read its comments via `gh`, triage + fix + push; cap at ~2-3 rounds, then escalate. Review is rented, not built.
- Run the narrowest meaningful local/regression checks (and the ticket's preview env where available).
- Write `review`, `regression`, and `test_verdict` documents.
- Create child tickets for substantive follow-up work instead of hiding findings in prose.
- Do NOT complete or merge here — merge is the release gate. On PASS, hand to `/flicker-release`.
- If checks fail, leave the ticket in progress and report blockers.

## Required commands

```bash
flicker ticket show <id> --json
flicker ticket document read <id> task_contract --json
flicker ticket document read <id> implementation_notes --json
gh pr view <n> --json reviews,comments,statusCheckRollup
flicker ticket document write <id> review --title "Review" --body "<markdown>" --json
flicker ticket document write <id> regression --title "Regression" --body "<markdown>" --json
flicker ticket document write <id> test_verdict --title "Test verdict" --body "<markdown>" --json
flicker ticket create "<finding>" --parent <id> --body "<details>" --json
```
