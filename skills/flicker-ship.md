---
name: flicker-ship
description: Take one approved Flicker ticket through implementation, testing, release gates, and authorized normal-path merge in one run. Use only for an explicit end-to-end ship request; do not use for vague ship language, planning, or danger-zone auto-merge.
---

# flicker-ship

Run implement, test, and release back to back for one named ticket, with every stage's evidence and every stop intact. Templates, outcomes, and gates are in the companion `flicker-workflow` contract; load only the section a step names.

## Stage contract

- Use only when the person names one ticket and asks for the whole path in this turn. Anything vaguer is `/flicker-plan` or a question.
- Authority: the named ticket's normal-path merge. Danger zones and one-way doors stop for a person.
- You are the author, so you never review your own work and never write the `review` document.
- Load `flicker-implement`, `flicker-test`, and `flicker-release` and run their steps in full. A shortcut in one stage voids the run.
- Nobody watches an autonomous run, so its report carries the evidence: the head SHA, each stage's outcome, and every command result it relies on.

## Steps

1. **Confirm authority.** Confirm the request names one ticket and grants end-to-end authority in this turn. Done when: the ticket id and the authority sentence are quoted in your report; an ambiguous request ends with outcome `needs a person`.
2. **Implement.** Run every `/flicker-implement` step. Done when: its step 9 is done and your status is `done` or `done with concerns`.
3. **Get a separate review, then test.** Have a reviewer that did not write the diff run `flicker-review` at the current head: a fresh agent session or thread you start for it, or a person. Fix its findings and get a new review at the new head. Then run every `/flicker-test` step. Done when: a `review` by that reviewer reads `Verdict: CLEAN` at the current head SHA and `test_verdict` is `PASS` there; with no separate reviewer available, the run ends with outcome `needs a person`.
4. **Release.** Run every `/flicker-release` step. A danger zone stops here with outcome `needs a person`. Done when: the PR is merged and the ticket reads `done`, or the stop is recorded.
5. **Stop on the circuit breakers.** Stop on red tests, a missing or stale review, a finding count that does not drop after 2 to 3 rounds, an exhausted budget, a contradiction, or a danger zone. Done when: the ticket and PR are left safe and your report names the outcome and the next command.

## Required public commands

```bash
flicker harness sync --check
flicker ticket show <id> --json
flicker ticket start <id> --json
gh pr create --title "<summary> (flicker #<id>)" --body "<scope, evidence, risk line>"
gh pr view <n> --json headRefOid,state,reviews,comments,statusCheckRollup
gh pr merge <n> --squash # only within explicit scoped authority and outside danger zones
flicker ticket complete <id> --json
flicker memory write "<release learning>" --ticket <id> --json
```
