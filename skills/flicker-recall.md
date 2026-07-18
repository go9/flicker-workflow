---
name: flicker-recall
description: Retrieve and explain existing Flicker tickets, current document heads, history, and memory with provenance. Use when asked what exists, changed, or was decided and why; do not use to create a plan or mutate workflow state.
---
<!-- Generated from orlando-umbrella/flicker@84c115fcc08c5c765955a58c37a99744830a5cc8 by scripts/publish-workflow-mirror.sh. Do not edit. -->

# flicker-recall

Follow the companion `flicker-workflow` contract, section `/flicker-recall`.

## Stage contract

- Search targeted tickets and memory, then read relevant current document heads; inspect history only when needed.
- Label evidence as current ticket, current document, historical event, or superseded event.
- Prefer current ticket fields and current heads. Expose contradictions or uncertainty instead of blending versions; for each conflict, name both source/version provenances, the differing claims, and why the current source wins or the claim remains unconfirmed.
- Return concise claims with ticket/document/version provenance and the next targeted read when evidence is incomplete.
- Do not create tickets, rewrite planning documents, select work, or change status.

## Required public commands

```bash
flicker memory search "<query>" --json
flicker ticket list --json
flicker ticket show <id> --json
flicker ticket document read <id> <kind> --json
flicker ticket document read <id> <kind> --history --json
```
