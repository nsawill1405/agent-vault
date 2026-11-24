---
title: "ADR 006: Knowledge graph context with bounded authority"
type: decision
date: "2026-09-04"
status: "Proposed"
tags:
  - hq
  - decision
source: "https://robbiepalmer.me/projects/agent-first-writing/adrs/006-knowledge-graph-context-with-bounded-authority"
author: Robbie Palmer
---

# Context

Generic writing tools see the draft but not the project's source decisions.
They cannot reliably tell which architecture decision supports a claim, which
terms the author uses elsewhere, or which evidence may be stale.

The Personal Knowledge Graph already connects projects, architecture
decisions, technologies, and public artifacts. That context can improve
editing. [[PDR 000 - Keep authors in control of editing and publication|PDR 000]]
keeps factual judgment and publication authority with the author, so retrieval
must remain a source of context rather than authority.

# Decision

Use the knowledge graph to supply editorial context. The editor may retrieve the
project a draft describes, linked architecture decisions, established
terminology, and claims that need fresh evidence.

Return proposed public artifacts and structured edit history to the graph.
Label the retrieved source and revision, surface missing or stale evidence, and
stop when no source decision supports a claim. The review workflow enforces the
author-control policy from PDR 000.

# Consequences

Suggestions can cite the project's own decisions and preserve local terms
instead of applying generic style blindly. The structured edit history can also
improve later evaluation.

Graph context can contain gaps or stale claims. The editor must present retrieved
material as context, keep factual verification separate, and fail safely when
the graph contains no source decision.


## Links

- implements product decisions: [[PDR 000 - Keep authors in control of editing and publication]]
- project: [[Agent-first Writing Editor]]
