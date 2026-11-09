---
name: flicker-plan
description: Shape a request into approved Flicker planning documents and selection-ready scope. Use when asked to research, clarify, scope, plan, ticket, or define acceptance; do not use for implementing an approved contract or only recalling prior decisions.
---

# flicker-plan

Turn a request into one ticket (or a few thin ones) with a contract a cheap model can build and another agent can check. Templates, outcomes, and the asking rules are in the companion `flicker-workflow` contract; load only the section a step names.

## Stage contract

- Use for research, scoping, ticketing, and acceptance. Approved contracts go to `/flicker-implement`; questions about past decisions go to `/flicker-recall`.
- Authority: create and update tickets and planning documents. Code, branches, and `start` belong to later stages. When feasibility needs real code, propose an approved child spike ticket that runs through `/flicker-implement`.
- Ask the person late and little: only decisions they own, one per question, so "yes" accepts your recommendation.
- End with one outcome: `go` (selected), `already done`, `rejected`, `needs a person`, or `retry`.

## Steps

1. **Check freshness and memory.** Run `flicker harness sync --check` and search memory for the request (see *Agent config freshness* and *Memory*). Done when: your report states both results, including "fresh" and "nothing relevant".
2. **Check whether it already exists.** Search tickets (including `in_progress` and recently done), memory, and the code for the requested behavior. Done when: you named the matching ticket or code, or wrote "no match" with the searches you ran. A match that already delivers the behavior ends the stage with outcome `already done`.
3. **Adopt or create the ticket.** Reuse a matching ticket; create one only when none fits. Read every current planning document head before writing. Done when: one ticket id owns the work and you have read its current heads.
4. **Gather evidence.** Read the repository instructions, the affected code, its callers, its contracts, and its nearby tests; read authoritative external sources when they matter. Done when: `plan_consensus` can cite what you read and at which commit, and anything you did not inspect is listed as not inspected.
5. **Find the smallest useful outcome.** Cut the request to the thinnest slice that delivers value end to end. Broad work becomes vertical child tickets with `blocked by` edges, the first one the thinnest risk-reducing slice. Done when: every in-scope outcome maps to one ticket and the out-of-scope list is written.
6. **Write the documents.** Write `feature_brief`, `plan_consensus`, `task_contract`, and `design` when required, from the templates in *Planning document contracts*. Done when: each acceptance row has an id, one behavior, a verification, an expected result, and a negative case where one applies.
7. **Resolve decisions late.** List the decisions a person owns that remain. Ask them per *Asking a person*, one at a time. Done when: `Open questions` is empty, or the stage ends with outcome `needs a person` naming the first question.
8. **Select.** With all scope mapped, no material open question, acceptance defined, and explicit approval, run `select-for-dev`. Done when: the ticket reads `selected_for_dev` in a fresh `flicker ticket show`.

Report: the ticket id, document versions, what you read, the outcome, and `/flicker-implement <id>` when selected.

## Required public commands

```bash
flicker harness sync --check
flicker ticket list --json
flicker memory search "<query>" --json
flicker ticket show <id> --json
flicker ticket document read <id> <kind> --json
flicker ticket create "<title>" --body "<brief>" --json
flicker ticket document write <id> <kind> --title "<title>" --body "<contract markdown>" --json
flicker memory write "<learning>" --ticket <id> --json
flicker ticket select-for-dev <id> --json
```
