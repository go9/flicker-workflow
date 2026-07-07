# Document & memory format

Everything the workflow persists — planning documents and memory events — is **markdown with optional YAML frontmatter**. That's the whole spec. It keeps documents human-readable in any tracker UI, diffable in git, and directly consumable by agents without a parser.

## Documents

One document per kind per ticket, versioned append-only (writing again creates a new version; the head is current truth, history is evidence). Body is plain markdown. When exporting or mirroring documents outside the tracker, add frontmatter so files are self-describing:

```markdown
---
type: Task Contract
title: Rate limiting — task contract
resource: https://flickercloud.com/tickets/123
tags: [api, security]
timestamp: 2026-07-06T00:00:00Z
---

# Task contract — rate limiting (#123)
…
```

`type` is the only required field; `title`, `description`, `resource`, `tags`, `timestamp` are the standardized optional ones. This is deliberately compatible with [Google's Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog) (OKF): an exported bundle of workflow documents is a valid OKF directory, so any OKF-aware tool can index it. We treat that as a nice property of the format, not a dependency — bundles are regenerable output, the tracker stays the source of truth.

### Type vocabulary

Document kinds map to Title Case `type` values: `Feature Brief`, `Plan Consensus`, `Task Contract`, `Design`, `Implementation Notes`, `Review`, `Regression`, `Test Verdict`, `Release`. Memory events use `Decision`, `Learning`, `Release Record`.

## Memory events

A memory event is a title + markdown body, append-only, timestamped, attributed. Same frontmatter convention when exported. The rules that make memory trustworthy:

- **Append, never rewrite.** A superseded decision gets a new event that names what it supersedes.
- **Cite sources.** Reference the ticket/PR/commit the event came from.
- **Current documents beat old events.** When they conflict, the document head wins; events are history.
