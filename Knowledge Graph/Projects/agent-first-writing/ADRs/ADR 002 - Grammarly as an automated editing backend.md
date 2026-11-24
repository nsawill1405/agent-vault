---
title: "ADR 002: Grammarly as an automated editing backend"
type: decision
date: "2026-09-04"
status: "Rejected"
tags:
  - hq
  - decision
source: "https://robbiepalmer.me/projects/agent-first-writing/adrs/002-grammarly-as-an-automated-backend"
author: Robbie Palmer
---

# Context

Grammarly is the practical baseline for the final editorial pass. Its product
also demonstrates useful levels of intervention, including local findings,
sentence suggestions, passage rewrites, and the option to ignore a change.

The agentic publishing workflow needs programmatic suggestions, source spans,
replacements, reasons, confidence, and edit outcomes. Grammarly's documented
Writing Score and Analytics APIs do not expose that editing interface. We
cannot use its private product as reproducible architecture.

# Decision

Reject Grammarly as an automated backend or runtime dependency for the editor.

Continue to use it as a manual quality baseline. Capture its suggestions for
evaluation only where doing so is legitimate. Use published research and public
descriptions as prior work, not as instructions for reproducing the private
implementation.

# Consequences

The editor needs its own suggestion contract, orchestration, and record of edit
decisions. It cannot promise parity with closed behavior or call that behavior
through an appropriate API.

Manual Grammarly use can still reveal missed failure classes. It does not form
an automated stage and must not become an unrecorded source of training data.
A browser-assisted handoff may reduce the manual round trip without turning
Grammarly into a backend. [[ADR 007 - Playwright-assisted Grammarly handoff|ADR 007]]
defines that narrower experiment.


## Links

- project: [[Agent-first Writing Editor]]
