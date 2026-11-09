---
name: flicker-recall
description: Retrieve and explain existing Flicker tickets, current document heads, history, and memory with provenance. Use when asked what exists, changed, or was decided and why; do not use to create a plan or mutate workflow state.
---

# flicker-recall

Answer "what exists, what changed, what did we decide" from the records, with a source on every claim. Labels and memory rules are in the companion `flicker-workflow` contract; load only the section a step names.

## Stage contract

- Use for questions about existing work. Planning new work is `/flicker-plan`.
- Authority: read only. Tickets, documents, and statuses stay as they are.
- A `historical` answer is shown and labeled; an `unknown` one is never reported as current.
- End with outcome `go` (answered) or `retry` (a read failed, with the error).

## Steps

1. **Search.** Search memory and tickets with targeted terms. Done when: you listed the searches you ran and their top hits.
2. **Read the current heads.** Read the current ticket fields and document heads behind the hits; read history only when the question is about change over time. Done when: every claim you will make points to a record you read.
3. **Label and reconcile.** Label each claim `current ticket`, `current document`, `historical event`, or `superseded event`. For each conflict, name both sources and versions, the differing claims, and why the current one wins or why it stays unconfirmed. Done when: no claim mixes two versions.
4. **Answer.** Return a short answer with provenance for each claim and the next targeted read when evidence is incomplete. Done when: every sentence of the answer cites a ticket, document version, or memory record.

## Required public commands

```bash
flicker memory search "<query>" --json
flicker memory expand ticket <id> --depth 1 --json
flicker ticket list --json
flicker ticket show <id> --json
flicker ticket document read <id> <kind> --json
flicker ticket document read <id> <kind> --history --json
```
