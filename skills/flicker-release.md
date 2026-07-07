---
name: flicker-release
description: For projects tracked in Flicker Tickets. Prepare release readiness for completed Flicker tickets by verifying evidence, writing release documents, and stopping before merge/deploy/publish unless explicitly approved. Use when the user asks to release, ship, merge, deploy, or prepare release notes for Flicker-ticketed work.
---

# flicker-release

Use the shared workflow contract in the `flicker-workflow` skill installed alongside this one, section `/flicker-release`.

## Adapter behavior

- Read current ticket state and evidence documents.
- Verify `test_verdict`, `regression`, `review`, and `implementation_notes` exist.
- Confirm the PR is green (reviewer satisfied + CI passing) and acceptance criteria are met.
- Write a `release` document with readiness, risks, rollback notes, and approval gates.
- Stop before merge/deploy/publish/upload unless explicitly approved in the current turn (merge = prod deploy on auto-deploy repos).
- On approval, merge the PR (`gh pr merge`) then `flicker ticket complete <id>`. Abandoned work: close the PR unmerged, `flicker ticket defer <id>`, tag `won't-do`.

## Required commands

```bash
flicker ticket show <id> --json
flicker ticket document read <id> test_verdict --json
flicker ticket document read <id> regression --json
flicker ticket document read <id> review --json
flicker ticket document read <id> implementation_notes --json
flicker ticket document write <id> release --title "Release readiness" --body "<markdown>" --json
gh pr merge <n> --squash   # only with explicit approval — merge may deploy
flicker ticket complete <id> --json
flicker memory add "<body>" --title "Release note" --json
```
