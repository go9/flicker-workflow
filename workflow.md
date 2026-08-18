---
name: flicker-workflow
description: Shared contract for the seven Flicker lifecycle skills. Load it only when a Flicker stage skill needs canonical statuses, evidence templates, safety gates, or stage procedures.
---

# Flicker Agent Workflow Core

**Contract version: 1.1.** Breaking changes are changes to statuses, transitions, document kinds, or release authority.

This file is the **single editable workflow source**. `packages/flicker-agent/skills/*/SKILL.md` are the editable stage adapters. `npm run sync` projects both into `cli/skill/workflow/`; never hand-edit that generated directory. Pi, Claude Code, Codex, and the CLI bundle must all install this behavior.

## Invariants

- Use the public `flicker` CLI/API for durable workflow state. Use `gh` only for PR/review state.
- Durable truth is the current Flicker ticket plus current document heads. Events and older versions are historical evidence. Runtime journals and agent transcripts are not another tracker.
- Statuses are exactly `backlog`, `selected_for_dev`, `in_progress`, and `done`.
- Transitions are exactly `select-for-dev`, `start`, `complete`, `reopen`, and `defer`.
- `in_progress` covers code, PR, review, and release readiness. Only a merged PR may precede `complete`.
- Document kinds are exactly `feature_brief`, `plan_consensus`, `task_contract`, `design`, `implementation_notes`, `review`, `regression`, `test_verdict`, and `release`.
- Do not invent work beyond the current task contract. Keep in-scope defects on the ticket; create a child only for genuinely out-of-scope, independently valuable follow-up.
- Never commit or push to the default branch. Code changes use a feature branch and PR.
- Never merge, deploy, publish, upload, or release without explicit authority in the current turn. A named `/flicker-ship <id>` request grants only that ticket's normal-path merge authority; ambiguous ship requests require confirmation, and danger zones always stop for a human.
- A feature-branch push/PR is allowed only when the approved run includes remote collaboration; otherwise stop after local evidence.
- On HTTP 409, stop, re-read current truth, and ask before replacing concurrent edits.
- Prefer narrow local checks first. Every behavioral change gets relevant changed-area regression coverage; risk adds breadth but never removes that baseline.

## Public commands

```bash
flicker ticket list --json
flicker ticket tree --json
flicker ticket show <id> --json
flicker ticket create "<title>" --body "<markdown>" [--parent <id>] --json
flicker ticket select-for-dev <id> --json
flicker ticket start <id> --json
flicker ticket complete <id> --json
flicker ticket reopen <id> --json
flicker ticket defer <id> --json
flicker ticket document read <id> <kind> [--history] --json
flicker ticket document write <id> <kind> --title "<title>" --body "<markdown>" --json
flicker memory search "<query>" --json
flicker memory search "<query>" --current-only --json  # drop superseded answers
flicker memory expand ticket <id> --depth 1 --json     # what a record connects to
flicker memory write "<learning>" --ticket <id> --json
flicker memory add "<body>" --title "<title>" --json    # legacy alias of write
gh pr create --title "<summary> (flicker #<id>)" --body "<ticket, scope, evidence>"
gh pr view <n> --json headRefOid,reviews,comments,statusCheckRollup
gh pr merge <n> --squash # explicit current-turn authority only
```

If project context is absent, ask for a slug or recommend `flicker project use <slug>`. Use `--json` for machine reads.

## Behavior profiles and orchestration

Profiles describe behavior, not mandatory agents: **Minimalist** limits scope; **Scout** gathers read-only evidence; **Strategist** resolves consequential ambiguity; **Implementer** writes narrowly; **Critic** attacks high-risk assumptions; **Verifier** maps criteria to evidence; **Gatekeeper** refutes release readiness; **Archivist** records durable results.

- One writer owns a worktree. Parallelize read-only research, review, or validation; parallel writers require disjoint worktrees and an explicit integration order.
- Use a dedicated worktree whenever another session or agent may touch the repository. Create it from a verified base ref without switching/resetting the shared checkout. A branch alone is not filesystem isolation.
- Parent/user authority remains singular. Agents may advise or implement approved choices; they must escalate unapproved product, public API, scope, licensing, data-loss, or release decisions.
- Bound waits and loops. Reviewer polls are 30–60 seconds apart, at most about 10 minutes per push. Stop after 2–3 rounds, repeated findings, non-decreasing actionable count, missing reviewer, or exhausted time/token budget.

### Project profiles and UI preferences

An optional project/user profile conforming to the Flicker Agent Profile schema may supply component, branching, visual-QA, and release preferences. It is a default, not durable workflow truth: explicit ticket documents override project preferences, which override organization defaults. Do not hardcode one team's stack into the generic skills. Missing preferences trigger a question only when they change scope or acceptance.

For UI/product changes, the `design` document and acceptance matrix must cover visible improvement, relevant loading/empty/error/focus/responsive states, accessibility, component strategy, and reuse boundaries. Verify the rendered surface; technical completion alone cannot satisfy visible acceptance.

## Planning document contracts

Use these headings; omit only a heading that is explicitly marked optional.

### `feature_brief`

- `Problem and current behavior`
- `Affected users`
- `Smallest useful outcome`
- `In scope`
- `Non-goals and reasons`
- `Appetite and constraints`
- `Assumptions and risks`
- `Success signals`
- `References`

Every in-scope outcome maps to a `task_contract` acceptance item or a child ticket. Keep implementation choices out of the brief.

### `plan_consensus`

- `Selected approach`
- `Repository evidence`
- `Prior art` with candidate/source/version when relevant and disposition `adopt | adapt | compose | reference | build`
- `Impact and risk`: target purpose, callers/dependents, contracts/invariants, nearby tests/gaps, `low | medium | high`, mitigation
- `Decisions and assumptions`
- `Rejected alternatives`
- `Open questions` (material unresolved questions block selection)
- `Spike result` when used

Inspect code, tickets, and authoritative docs before asking answerable questions. If two material interpretations remain, present each consequence and a recommendation, then ask one decision at a time. Prefer a structured choice UI when the host supports it; portable text must include the same choices and recommendation.

Planning itself is non-writing research and contract preparation. A proposed spike records one question, a fixed timebox, evidence needed, exclusions, and no production-code assumption. If executable code is genuinely required, first create and obtain approval for a child ticket with an explicit spike contract; that child enters `/flicker-implement` and follows the normal worktree, one-writer, baseline, changed-files, command, and evidence rules. Retain its result, evidence, untested gaps, recommendation, and plan impact in the parent `plan_consensus`; discard experimental code only through the approved child-ticket disposition.

### `task_contract`

- `Goal`
- `Scope and non-goals`
- `Affected surfaces and invariants`
- `Implementation sequence` (only when multiple working increments are needed)
- `Acceptance matrix`
- `Test strategy and fixtures`
- `Compatibility, rollback, and risk`
- `Intentionally not done`

Each acceptance row contains: stable id, observable behavior, verification command or named real-user/manual protocol, expected result, risk, and a negative/error case when applicable. Cover the main path, material failure modes, regression surface, and at least one end-to-end proof where applicable. UI evidence may be a route plus screenshots/browser steps; do not replace visible acceptance with an implementation detail.

### `design` (required for consequential UI/product or public-interface work)

Record options, selected interface/component strategy, misuse/compatibility risks, visible states (loading/empty/error/focus/responsive as applicable), accessibility, before/after acceptance, and reuse boundaries.

## Delivery evidence contracts

### `implementation_notes`

Record ticket/contract version; one-writer owner; branch/worktree; base SHA and head SHA; changed files; tests added/updated; every command with exit code and concise output; behavior delivered; criterion coverage; decisions; PR URL (when opened); residual risks; and intentionally-not-done work. Record the exact pre-edit baseline command, exit code, and failure output, and whether a red baseline is confirmed pre-existing; do not silently implement over an unexplained red baseline. For a bug, record the original failing command/output or why honest reproduction was impossible.

### `review`, `regression`, and `test_verdict`

`review` records reviewer identity/source, reviewed head SHA, rounds, actionable findings and dispositions. `regression` maps every acceptance id to its expected proof and actual command/manual result, including an explicit missing-proof entry and real-surface evidence. Aggregate green tests never substitute for a missing acceptance row. `test_verdict` is exactly `PASS` or `REQUEST CHANGES`, names the head SHA, blockers, residual risks, and evidence document versions. A stale-head review cannot pass.

### `release`

Record head SHA, acceptance coverage, current-head reviewer and CI state, migration/data/danger-zone analysis, rollback plan, post-deploy checks, explicit authority status, and remaining risk. Record both the exact gated merge/deploy command and a separately labeled safe current action; without current-turn authority, the gated command is evidence only and must not be presented as the action to run. Missing or stale evidence produces `NOT READY`, never an inferred pass.

## Memory: read before deciding, write on learning

Memory is not documentation you file at the end. It is the reason the same
conclusions do not get re-derived every session, and it only works if both
halves happen.

### Read gate (every stage)

Begin each stage by searching memory for the work at hand, and REPORT WHAT
CAME BACK — including "nothing relevant", which is a real answer and must be
stated rather than skipped. A stage that silently found nothing is
indistinguishable from a stage that never looked.

Results carry a temporal state. A `historical` hit is still worth reading —
it is what was decided before, and its replacement is named — but never
present it as current. Never present `unknown` as current either: it means the
record was superseded and the replacement could not be read.

Use `expand` when a hit mentions something it does not explain. That is the
whole reason edges exist: the decision that caused X is often one link away
and shares no vocabulary with your query.

### Write trigger (on learning, not on schedule)

Write a memory note when you learn something that would CHANGE A FUTURE
DECISION:

- a root cause, especially a non-obvious one
- an approach that was tried and rejected, and why
- a constraint discovered the hard way
- a claim in the docs or a ticket that turned out to be false

Do NOT write: status updates, restatements of the diff, "started work on X",
or anything the ticket already says. Noise is the failure mode that kills a
memory system — the read gate starts returning garbage and agents learn to
skip it. If you would not want to read it in six months, do not write it.

### Supersession over deletion

When a new learning contradicts an old one, do not delete or edit the old
note. Close the old ticket by supersession (`flicker ticket close <id>
--disposition superseded --superseded-by <new>`) so the wrong answer stays
visible with its correction attached. "We tried that and it failed" is exactly
the thing worth keeping.

## Agent config freshness (stage start)

A project's agent config — skills, MCP specs, rules — lives in the Flicker library and reaches a working copy only when `flicker harness sync` writes it there. So a checkout can be running last month's instructions while the library has moved on, and nothing inside a session ever says so: the skills load, they are simply the wrong ones.

`/flicker-plan`, `/flicker-implement`, and `/flicker-ship` therefore START by checking freshness:

```bash
flicker harness sync --check   # exit 0 fresh, exit 1 stale, writes nothing
flicker harness doctor         # deeper: reads the DISK, not the intent
```

Rules:

- **Report the result, including "fresh".** A check that speaks up only when it is unhappy is indistinguishable from one that never ran.
- **Never hard-fail a human's stage on it.** Stale config is a finding to surface, not a gate. Name what is stale, offer `flicker harness sync`, and continue the stage.
- **Name the legitimate skips instead of hiding them.** No project bound to this directory, and no agent config assigned to the project, are both normal — say which one happened rather than reporting nothing.
- **Reach for `doctor` when `--check` is clean but the config still looks wrong**, and whenever the work itself adds or changes agent config. `--check` compares against what the last sync recorded; `doctor` compares against the bytes on disk, so it is the one that catches a skill file that was edited or emptied, an MCP server with no harness registration, a project-only entry assigned org-wide, and a description index over budget. Drift and scope findings exit 1; prerequisite and budget findings are warnings and exit 0.

## Review and danger-zone gates

The PR stays `in_progress`. Use the repository's pluggable reviewer through GitHub rather than creating a bespoke review engine. A reviewer response counts only when it covers the **current head SHA** (`headRefOid`). If no reviewer check exists after the first push, stop immediately. Otherwise use the bounded wait and progress circuit breaker above.

Risk is additive:

- all behavioral changes: relevant changed-area tests and contract evidence;
- medium risk: integration/real-surface checks and independent review;
- high risk: Critic review plus applicable full-suite, security, performance, migration, preview, rollback, or post-deploy checks.

Danger zones include repository-defined paths plus security/auth/permissions, billing/money, destructive data operations, DB migrations, deployment/data-plane core, concurrency, and broad UI system/theme changes. They always require human merge authority and a rollback/post-deploy plan. A preview failure blocks only when preview is the only meaningful acceptance surface; otherwise record and escalate it.

Parked work remains inside the same lifecycle: leave future work in `backlog` with timing/intent tags. For abandoned active work, close the PR unmerged and use `defer`; do not invent a status or mark an unmerged ticket done.

## `/flicker-plan`

**Use for:** shaping, scoping, researching, ticketing, or preparing work. **Not for:** executing an already-approved contract or merely recalling prior decisions.

**Stage start:** run `flicker harness sync --check` and report the result, per *Agent config freshness*. Planning a project on stale instructions is planning against the wrong constraints. Never block the stage on it.

1. Run Minimalist; identify the smallest useful outcome and appetite.
2. Search tickets and memory. Adopt a matching ticket or create one.
3. Read the ticket and all current planning heads before overwriting any document.
4. Scout repository instructions, git/worktree state, affected helpers/callers/tests, installed dependencies, and authoritative external sources when material.
5. Resolve only consequential ambiguity. Record prior-art disposition and impact/risk.
6. If one coherent contract is impossible, create vertically valuable child tickets; the first is the thinnest end-to-end risk-reducing slice. Do not create horizontal layer tickets.
7. Write `feature_brief`, `plan_consensus`, `task_contract`, and `design` when required using the contracts above.
8. Selection readiness requires: all scope mapped, no material open question, acceptance evidence defined, external assumptions evidenced or explicitly blocked, and user approval. Then run `select-for-dev`.

Output ticket id, document versions, repository and upstream evidence, target purpose, callers/dependents, contracts/invariants, nearby tests/gaps, prior-art source and disposition, non-goals, resolved/open decisions with recommendation, behavior-to-verification acceptance, risk, and `/flicker-implement <id>`. If evidence was not inspected, say so instead of inventing it.

## `/flicker-implement`

**Use for:** coding an approved `selected_for_dev` or `in_progress` ticket. **Not for:** planning, independent acceptance review, or release.

**Stage start:** run `flicker harness sync --check` and report the result, per *Agent config freshness*. Never block the stage on it.

1. Read ticket plus current `feature_brief`, `plan_consensus`, `task_contract`, and `design`. Stop on contradictions or staleness.
2. Verify approved status, intended branch/worktree, clean scope, base SHA, and a relevant green baseline. If selected, run `start`.
3. Scout the affected surface. For bugs, run the original failing reproduction before editing unless impossible and recorded.
4. Use one writer. Implement a tracer/vertical slice and keep the system working after each meaningful increment. Avoid drive-by refactors and dependencies.
5. Run changed-area tests, then additive risk checks. Do not weaken worktree/default-branch/release safety.
6. If remote collaboration is authorized, push the feature branch and open a ticket-stamped PR. Never push the default branch.
7. Write the complete `implementation_notes` contract. Do not mark done; hand off to `/flicker-test`.

Output one-writer owner, branch/worktree, exact baseline command/result (including pre-existing failure status), base/head SHA, changed files, tests added/updated, every command and exit code, PR (if any), residual risk, intentionally-not-done work, and next safe action. Never fabricate a command run or SHA.

## `/flicker-test`

**Use for:** independent review, regression, acceptance mapping, or a terminal verdict on implemented work. **Not for:** initial implementation or merging.

1. Read the current task contract, implementation notes, actual diff, and PR head; do not trust the implementation summary alone.
2. Verify scope and each acceptance row. Re-run the original failure first for bug fixes, then changed-area regression and additive risk checks.
3. Seek real-surface behavioral proof where feasible. For UI, inspect the rendered route and applicable visible/accessibility states.
4. Drive the current-head reviewer loop with bounded waits and progress circuit breakers. Keep in-scope blockers on this ticket; ticket only true follow-ups.
5. Write `review`, `regression`, and terminal `test_verdict` using the evidence contracts.
6. On `PASS`, stop ready for `/flicker-release`. On `REQUEST CHANGES`, leave `in_progress`, record exact blockers and next command.

## `/flicker-release`

**Use for:** adversarial release-readiness review and an explicitly authorized merge/deploy. **Not for:** coding or a full autonomous pickup-to-merge run.

1. Read current ticket, contract, implementation, review, regression, verdict, actual PR head, reviewer, and CI.
2. Try to refute readiness: stale head, uncovered criterion, missing command result, scope drift, danger zone, migration/data risk, absent rollback/post-deploy plan, or failing CI.
3. Write `release` as `READY` or `NOT READY` with exact evidence and next command.
4. Stop unless merge/deploy/publish authority is explicit in the current turn. Danger zones require human approval even in ship mode.
5. When authorized, merge; verify merge/deploy/post-deploy outcome as applicable; only then run `complete`.

## `/flicker-ship`

**Use for:** an explicit request to take one named/selected ticket through implement, test, release, and normal-path merge in one run. **Not for:** vague “ship” language, planning, danger-zone auto-merge, or bypassing evidence.

**Stage start:** run `flicker harness sync --check` and report the result, per *Agent config freshness*. An autonomous run is exactly where nobody is watching the instructions it is following. Never block the run on it.

1. Confirm the request grants scoped current-turn end-to-end authority for this ticket; otherwise ask. Read current truth and run all `/flicker-implement`, `/flicker-test`, and `/flicker-release` contracts.
2. Use a dedicated worktree and one writer. Require changed-area regression, complete evidence, current-head clean review, green CI, and no unresolved findings.
3. Stop on red tests, missing reviewer, stale evidence, no progress, exhausted budget, ambiguity, or a danger zone. Leave the PR/ticket safe and report the next command.
4. Only the explicitly authorized, non-danger-zone path may merge. Verify post-merge outcome, then run `complete` and record release memory.

## `/flicker-recall`

**Use for:** finding or explaining existing tickets, current documents, decisions, and memory. **Not for:** creating a plan or changing ticket state.

1. Search memory and tickets with targeted terms; read relevant current heads and history only when needed.
2. Label claims `current ticket`, `current document`, `historical event`, or `superseded event`.
3. Prefer current fields/heads; expose contradictions, uncertainty, and missing evidence rather than blending versions.
4. For every contradiction, name both sources and versions/timestamps when available, quote or summarize the conflicting claims, and state why the current source wins or why the claim remains unconfirmed.
5. Return a concise answer with ticket/document/version provenance and the next targeted read if evidence is incomplete.

## `/flicker-health-watchdog`

**Use for:** read-only audits of live Flicker infrastructure and hosted-project health. **Not for:** suggestion inbox triage, code changes, restarts, deploys, secret changes, scaling, or destructive remediation.

1. Confirm organization/project/resource scope and current credential.
2. Read current Flicker resource, deploy, log, config-provenance, and documented functional-probe evidence. External telemetry and repository CI are enrichment only.
3. Label each resource `green`, `yellow`, `red`, or `unknown`; cite strongest live evidence and never infer health from quiet logs or green CI alone.
4. Preserve platform invariants: no manual `DATABASE_URL`, no secret values, no legacy-host assumptions, and no write probes.
5. Return resource, status, evidence, risk, and next safe action. Recommend `/flicker-plan` for tracked work; mutate no ticket unless separately authorized.

This stage and `/flicker-triage` are intentionally distinct: watchdog reads infrastructure; triage mutates suggestion disposition.

## `/flicker-triage`

**Use for:** turning a project's open end-user suggestions into grouped reports linked to tickets, plus written rejections. **Not for:** scoping an accepted ticket, retrieving history, or changing code.

1. Resolve the project, then read the open inbox with `GET /api/v1/projects/<project>/suggestions?status=open`. Page backwards with `before_id` until the inbox is exhausted or the agreed batch size is reached. Reporter identity is deliberately absent from this list; do not try to reconstruct it.
2. Read `summary` and `enrichment.candidates` as cheap cloud hints. A candidate is `{"type": "ticket" | "suggestion", "id": N, "confidence": 0.0-1.0, "reason": "..."}` and links nothing by itself; confirm or discard each one against the real ticket or suggestion before acting on it. Absent enrichment is normal, not an error.
3. Group the batch into clusters that share one underlying cause. Wording similarity is not a cluster; a shared cause is.
4. Before minting any ticket, search existing work with `flicker ticket list`, `flicker memory search`, and `flicker ticket show` on every plausible hit, explicitly including `in_progress` and recently completed tickets. A new report of a known problem links to that ticket; a rival ticket splits the notification cohort and the evidence.
5. Accept every report in a cluster against one ticket id: `PATCH /api/v1/suggestions/<id>` with `action=accept` and `ticket_id=<id>`. Accept is valid only from `open`, the ticket must belong to the same project, and it writes a linked event on the ticket. Create a ticket first only when no existing ticket covers the cluster; the created ticket enters `backlog` and is scoped by `/flicker-plan`, not here.
6. Reject only what will not be worked: `action=reject` with a `rejection_reason` written for the person who sent the report. Name their specific report, say what happens instead, and stay kind. Reused boilerplate is a defect, not a shortcut.
7. Rank accepted clusters on evidence in hand — report count, severity, blast radius, spread across sources. Public vote counts are the intended priority signal once the public board ships; treat that as forward-looking and never depend on the field today.
8. Record each confirmed diagnosis in memory with provenance — suggestion ids, the linked ticket, what was actually checked — so the next pass starts from the answer rather than the raw text.

Deep reasoning runs locally on the operator's own subscription; the cloud does only cheap enrichment. This stage mutates suggestion state and creates tickets. It never edits code, pushes, deploys, merges, or moves a ticket through delivery statuses.
