---
name: flicker-health-watchdog
description: Audit live Flicker infrastructure and hosted-project health using current platform state, deploys, logs, and documented probes. Use for an on-demand or scheduled health sweep; do not use for suggestion inbox triage, code changes, restarts, deploys, or destructive remediation.
---

# flicker-health-watchdog

Use Flicker as primary infrastructure authority. Read live state; report evidence. Do not mutate infrastructure or ticket state unless user separately authorizes that action.

This skill is distinct from `flicker-triage`: health watchdog inspects infrastructure; triage groups end-user suggestions and mutates suggestion disposition.

## 1. Resolve scope

Confirm organization/project and requested breadth:

- one app, database, or environment
- one Flicker project
- platform/control-plane components
- all projects visible to current credential

Use current Flicker API/CLI state before repository docs or memory. Read project instructions only for documented health endpoints and safe app-specific probes.

## 2. Gather smallest useful live evidence

Start narrow:

```bash
flicker current
flicker app list
flicker database list
```

Then inspect only degraded or in-scope resources with available commands such as:

```bash
flicker app logs <app>
flicker app env <app>
flicker app exec <app> -- <documented-read-only-probe>
flicker config <app>
```

Use documented HTTP health endpoints when they prove user-visible service. Use `gh` only for repository CI/release evidence that Flicker does not own. Use external telemetry only as enrichment; it cannot override contradictory live platform state.

Never expose secret values. `app env` provenance is safe; `printenv` is not a health-report surface.

## 3. Classify evidence

For each resource report one status:

- **green** — current live evidence proves expected service
- **yellow** — degraded, stale, flaky, or partly unknown
- **red** — current failure, outage, failed deploy, or repeated user-affecting error
- **unknown** — evidence unavailable or insufficient

Prefer strongest evidence first: functional probe, runtime/deploy state, then logs. A passing CI run does not prove a deployed app is healthy. A quiet log slice does not prove uptime.

## 4. Preserve platform invariants

- Never hand-set `DATABASE_URL`; same-project dependency wiring owns it.
- Distinguish internal and public database connection strings.
- Treat environment inheritance and managed injection as separate provenance.
- Do not use legacy hosts as evidence for current Kubernetes-cell placement.
- Do not restart, deploy, migrate, scale, edit secrets, or execute write probes in watchdog mode.

## 5. Output

Return compact table:

| Resource | Status | Strongest evidence | Risk | Next safe action |
|---|---|---|---|---|

Call out missing proof. If issue deserves tracked work, recommend `/flicker-plan`; do not create or transition ticket during read-only watchdog run unless user explicitly requested ticket mutation.

## Verification checklist

- Current credential and scope confirmed.
- Live Flicker state checked.
- Every status cites concrete evidence.
- Unknowns remain unknown.
- No secrets printed.
- No mutation command executed.
- Suggestion inbox untouched.
