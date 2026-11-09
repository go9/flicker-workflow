---
name: flicker-review
description: Review the current branch diff on two axes, correctness and spec, and record a SHA-bound review verdict on its Flicker ticket. Use before test, ship, or release when reviewer evidence is needed; do not use to fix the code, review your own diff, or merge.
---

# flicker-review

Review one branch's diff and write a `review` document that is valid only for its head SHA. Templates and gates are in the companion `flicker-workflow` contract; load only the section a step names.

## Stage contract

- Use when a ticket's PR needs reviewer evidence. Fixes go back to `/flicker-implement`; verdicts to `/flicker-test`.
- You must not be the author. Run in a session that did not write or edit this diff: a fresh agent session or thread, or a person. If you wrote any of it in this session, end with outcome `needs a person`.
- Authority: read the code and write the `review` document. Code, branches, merges, and deploys stay as they are.
- End with outcome `go` (`CLEAN`), `rejected` (`FINDINGS`, each finding its remedy), `needs a person`, or `retry`.

## Steps

1. **Load the reviewer setting.** Read the repository's root `AGENTS.md` and find its reviewer provider, model, and reasoning setting; review with exactly those. Done when: you quoted the setting. If it is missing or incomplete, stop with: `No reviewer configured: add the reviewer provider, model, and reasoning to this repository's AGENTS.md.`
2. **Fix the range.** Require an attached Flicker ticket and a checked-out branch. Set `head` from `git rev-parse HEAD` and `base` from the ticket's or PR's target branch, verified to resolve. Done when: both are full SHAs and `git diff <merge-base>...<head>` is not empty.
3. **Read the contract.** Read the ticket's current `task_contract`. Done when: you can list its acceptance ids and its out-of-scope list, or you noted that it has none.
4. **Review correctness.** Read the whole diff and the code around it. Look for bugs, regressions, security or data-loss risk, danger-zone paths, weakened or deleted tests, and missing tests. Done when: each finding has a severity and `file:line`.
5. **Review the spec.** Compare the diff with the contract: work the contract asked for that is missing, work nobody asked for, and work that looks done but is wrong. Done when: each finding quotes the acceptance row or contract line it is about.
6. **Rate the risk.** Write one line: `Risk: one-way door | two-way door; blast radius: <one word>`. A danger-zone touch or a one-way door is a finding that needs a person, however sound the code. Done when: the line is written.
7. **Write the verdict.** Write the `review` document in the format below. `CLEAN` only when neither axis has an actionable finding. Done when: the write returned a document version, and your report gives that version and the head SHA.

The `review` document:

```text
Head SHA: <full sha>
Base: <ref> (<full sha>)
Reviewer: <provider/model/reasoning, or the person>
Verdict: CLEAN | FINDINGS
Risk: <one-way door | two-way door>; blast radius: <word>

## Correctness
- <severity> <file:line>: <finding>   (or: None)

## Spec
- missing | unrequested | wrong: <finding> ("<quoted contract line>")   (or: None)
```

Any new commit makes this review stale; a new head needs a new review. Long test suites are the tester's job.

## Required public commands

```bash
git rev-parse HEAD
git merge-base <base> HEAD
git diff <merge-base>...HEAD
flicker ticket document read <id> task_contract --json
flicker ticket document write <id> review --title "Review <short sha>" --body "<review document>" --json
```
