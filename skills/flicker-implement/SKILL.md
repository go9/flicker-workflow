---
name: flicker-implement
description: Implement an approved Flicker task contract test-first, with baseline, worktree, scoped code, tests, PR, and implementation evidence. Use when asked to code or continue a selected/in-progress ticket; do not use for planning, independent verdicts, or release.
---

# flicker-implement

Build exactly what the approved `task_contract` asks, test-first, and leave evidence another agent can check. Templates, outcomes, and gates are in the companion `flicker-workflow` contract; load only the section a step names.

## Stage contract

- Use for a `selected_for_dev` or `in_progress` ticket with an approved `task_contract`. Planning goes to `/flicker-plan`; verdicts to `/flicker-test`.
- Authority: write code in your own worktree and feature branch; push and open a PR when the run authorizes remote collaboration. Merging and `complete` belong to `/flicker-release`.
- You are the one writer of your worktree.
- End with a builder status (`done`, `done with concerns`, `blocked`, `needs context`) and one outcome.

## Steps

1. **Check freshness and memory.** Run `flicker harness sync --check` and search memory for the ticket (see *Agent config freshness* and *Memory*). Done when: your report states both results.
2. **Read the contract.** Read the ticket and the current `task_contract`, `plan_consensus`, `feature_brief`, and `design` heads. Done when: you can state the goal, the acceptance ids, and the out-of-scope list; contradictory or stale documents end the stage with outcome `needs a person`.
3. **Set up the worktree and baseline.** Create a dedicated worktree and feature branch from a verified base SHA. Run the changed-area tests before any edit. Run `flicker ticket start` if the ticket is `selected_for_dev`. Done when: you recorded the base SHA, the baseline command, its exit code, and any pre-existing failure; an unexplained red baseline ends the stage with outcome `retry` or `needs a person`.
4. **Write the failing test first.** For each acceptance row, write the test at the contract's seam and run it. For a bug, follow the *Debugging loop* below. A row whose proof is a document, a manual protocol, or a pure refactor uses the alternative proof the contract names for it (the rendered page, the protocol's recorded result, the existing tests passing unchanged); write it as "no red test: <proof>". Done when: each new test fails for the expected reason and its command and output are saved as the red proof, and every other row names its alternative proof; a row with neither ends the stage with status `needs context`.
5. **Make it pass.** Write the smallest code that turns the tests green, inside the contract's scope. Leave existing assertions unchanged. Done when: the new tests and the changed-area tests pass, and every changed file serves an acceptance row.
6. **Prove the test catches the bug.** For a bug fix: commit the fix and its test. Take the fix out: `git checkout <base-sha> -- <changed fix files>`, and delete each fix file the base does not have. Run the new test and see it fail. Put the fix back: `git checkout HEAD -- <all fix files>`, and see it pass. Done when: the revert proof is recorded, `git status --porcelain` prints nothing, and `git diff HEAD` is empty; a test that passes without the fix is rewritten.
7. **Run the risk checks.** Run the format, compile, and lint steps the repository's CI runs, plus the checks the risk class adds. Done when: each command and exit code is recorded and all are green, or a red one is reported with its output.
8. **Open the PR.** If remote collaboration is authorized, push the feature branch and open a ticket-stamped PR whose body carries the scope, the evidence, and the risk line. Done when: `gh pr view` returns the PR's `headRefOid` and it matches your local HEAD.
9. **Write the notes and hand off.** Write `implementation_notes` from the template and write a memory note if you learned something. Done when: the document write returned a version and your report starts with a builder status and ends with `/flicker-test <id>`.

### Debugging loop

1. Build one fast, deterministic command that fails on this bug and runs unattended. Do this before forming theories.
2. Shrink the reproduction until every remaining part matters.
3. Write three to five ranked hypotheses, each with what it predicts you will see.
4. Probe the top hypothesis. Tag any temporary debug output with one prefix (`DBG-<ticket>`) so one grep removes it.
5. Fix the root cause in the shared function, not in one caller. The failing command becomes the regression test.

If no test seam can reach the bug, record "no test seam" as a finding in `implementation_notes` and say what seam would.

### When skipping the test looks tempting

| The thought | The reply |
|---|---|
| "Too simple to test." | Simple code breaks too, and the test takes a minute. Write it. |
| "I'll add tests after." | A test written after the code passes on its first run and proves nothing. Write it first and watch it fail. |
| "I checked it by hand." | A manual check leaves nothing to re-run. Turn it into a command. |
| "This existing test is wrong." | Changing it is a scope decision. Leave it, and record the conflict with the acceptance row it contradicts. |
| "It is only a refactor." | Then the existing tests pass unchanged. That is the proof; run them. |
| "It is hard to test." | Name the seam you would need, and record "no test seam" as a finding. |

## Required public commands

```bash
flicker harness sync --check
flicker memory search "<ticket keywords>" --json
flicker ticket show <id> --json
flicker ticket document read <id> task_contract --json
flicker ticket document read <id> plan_consensus --json
flicker ticket start <id> --json
gh pr create --title "<summary> (flicker #<id>)" --body "<scope, evidence, risk line>"
gh pr view <n> --json headRefOid
flicker ticket document write <id> implementation_notes --title "Implementation notes" --body "<evidence>" --json
flicker memory write "<learning>" --ticket <id> --json
```
