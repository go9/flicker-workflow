---
name: flicker-triage
description: Turn a project's open end-user suggestion inbox into grouped reports linked to existing or new tickets, plus written reporter-facing rejections. Use when asked to triage an inbox, suggestions, feedback, or incoming bug reports; do not use to scope an accepted ticket, retrieve history, or change code.
---

# flicker-triage

Follow the companion `flicker-workflow` contract, section `/flicker-triage`.

## Stage contract

- Read one project's open inbox and page it to the agreed batch size. Treat `summary` and `enrichment.candidates` as cheap cloud hints to verify, never as decisions already made.
- Group the batch by underlying cause, not by wording. Many reports legitimately share one ticket id.
- Search existing work before minting anything, including `in_progress` and recently completed tickets. A new report of a known problem links to that ticket; a rival ticket splits the notification cohort and the evidence.
- Accept each grouped report against one ticket id. Create a ticket only when no existing ticket covers the group; a created ticket enters `backlog` for `/flicker-plan` to scope.
- Reject only what will not be worked, with a reason the reporter reads: name their specific report, say what happens instead, stay kind. Boilerplate is a defect.
- Rank accepted groups on evidence you actually have — report count, severity, blast radius, source spread. Public vote counts are the intended priority signal once the public board ships; do not assume that field exists yet.
- Record each confirmed diagnosis in memory with provenance so the next pass starts from the answer instead of the raw text.
- Deep reasoning runs locally on the operator's own subscription. Mutate suggestion state and create tickets only; never edit code, push, deploy, merge, or move ticket status.

## Required public commands

```bash
curl -s "$FLICKER_API/api/v1/projects/<project>/suggestions?status=open&limit=50" -H "Authorization: Bearer $FLICKER_TOKEN"
flicker ticket list --json
flicker memory search "<report keywords>" --json
flicker ticket show <id> --json
flicker ticket create "<title>" --body "<grouped reports and evidence>" --json
curl -s -X PATCH "$FLICKER_API/api/v1/suggestions/<id>" -H "Authorization: Bearer $FLICKER_TOKEN" -d action=accept -d ticket_id=<id>
curl -s -X PATCH "$FLICKER_API/api/v1/suggestions/<id>" -H "Authorization: Bearer $FLICKER_TOKEN" --data-urlencode action=reject --data-urlencode "rejection_reason=<reason written for the reporter>"
flicker memory write "<confirmed diagnosis with suggestion ids>" --ticket <id> --json
```
