---
name: flicker-recall
description: For projects tracked in Flicker Tickets. Recall Flicker tickets, current documents, and project memory with source labels. Use when the user asks what was decided, what tickets exist, why something changed, or to search Flicker memory.
---

# flicker-recall

Use the shared workflow contract in the `flicker-workflow` skill installed alongside this one, section `/flicker-recall`.

## Adapter behavior

- Search Flicker memory and current ticket list.
- Label every answer as current ticket, current document, historical event, or superseded event when available.
- Prefer current ticket fields and current document heads over historical events when they conflict.
- If evidence is incomplete, say so and suggest the next search or ticket/document to inspect.

## Required commands

```bash
flicker memory search "<query>" --json
flicker ticket list --json
flicker ticket show <id> --json
flicker ticket document read <id> <kind> --json
flicker ticket document read <id> <kind> --history --json
```
