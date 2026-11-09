---
name: flicker-test
description: Independently test implemented Flicker work, map each acceptance row to evidence, and issue PASS or REQUEST CHANGES. Use when asked to validate, regress, or test a ticket; do not use for initial coding or merge/release.
---

# flicker-test

Check the builder's work yourself and decide `PASS` or `REQUEST CHANGES` for one head SHA. Templates, outcomes, and gates are in the companion `flicker-workflow` contract; load only the section a step names.

## Stage contract

- Use after `/flicker-implement` opened a PR. Code fixes go back to `/flicker-implement`; merges go to `/flicker-release`.
- Authority: run tests and write `regression` and `test_verdict`. The `review` document belongs to the reviewer (`/flicker-review` or a PR reviewer), so read it and leave it as written.
- The builder's notes are claims. Every verdict rests on commands you ran and files you read.
- End with one outcome; the verdict is the evidence for it.

## Steps

1. **Search memory.** Search memory for the ticket and report the result (see *Memory*). Done when: your report states what came back.
2. **Read the evidence and the diff yourself.** Read the current `task_contract`, `implementation_notes`, the PR, its head SHA, and the full diff. Done when: you know the head SHA from `gh pr view`, and each claim in the notes is marked confirmed, contradicted, or not checked.
3. **Re-run the original failure.** For a bug fix, run the reproduction on the head SHA. Done when: the command and its passing output are recorded.
4. **Prove each acceptance row.** Run each row's verification, including negative paths and, for UI, the rendered route and its states. Done when: every acceptance id maps to an expected proof and an actual result, or to an explicit missing-proof entry.
5. **Check the tests themselves.** Compare changed test files against the base. Done when: no existing assertion was weakened, skipped, or deleted without an acceptance row that requires it; any that was is a blocker.
6. **Check reviewer evidence.** Find a `review` document or PR review for the current head SHA (see *Review and danger-zone gates*). Done when: it exists with `Verdict: CLEAN`; a missing or stale review, or `FINDINGS`, is a blocker that asks for `/flicker-review` at this head.
7. **Write the verdict.** Write `regression` and `test_verdict` from the templates. Keep in-scope blockers on this ticket. Done when: the verdict is exactly `PASS` or `REQUEST CHANGES` with the head SHA, and the next command is `/flicker-release <id>` or the blocker list.

## Required public commands

```bash
flicker memory search "<ticket keywords>" --json
flicker ticket show <id> --json
flicker ticket document read <id> task_contract --json
flicker ticket document read <id> implementation_notes --json
flicker ticket document read <id> review --json
gh pr view <n> --json headRefOid,reviews,comments,statusCheckRollup
gh pr diff <n>
flicker ticket document write <id> regression --title "Regression" --body "<criterion map>" --json
flicker ticket document write <id> test_verdict --title "Test verdict" --body "<PASS or REQUEST CHANGES>" --json
```
