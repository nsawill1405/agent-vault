---
title: "ADR 000: Vale for deterministic prose checks"
type: decision
date: "2026-09-04"
status: "Accepted"
tech_stack:
  - "Vale"
tags:
  - hq
  - decision
source: "https://robbiepalmer.me/projects/agent-first-writing/adrs/000-vale-for-deterministic-prose-checks"
author: Robbie Palmer
---

# Context

Agent-written drafts repeat a known set of tiring patterns. They over-explain
simple points, repeat conclusions, flatten the author's voice, and use stock
phrases. These defects often survive grammar checks because the prose is
technically correct.

Many of the patterns are precise enough to detect without a model. A fast rule
can point to the exact text and explain what failed. It can also run before a
human spends time reviewing the draft.

# Decision

Run Vale against changed prose in the Personal Knowledge Graph. Keep repository-specific
rules for recurring faults in agent-written text and report each finding at its
source location.

Vale is the accepted first layer of the editor. Deterministic rules should own
problems they can identify reliably. Model-based review should not replace a
working rule with a slower and less predictable judgment.

# Consequences

Writers get fast, exact feedback before editorial review, and the same checks
can guard later revisions. The rules make known style expectations executable.

Vale cannot restructure an argument, compare dependent edits, or decide whether
a technically sound passage is worth reading. Those failures need evaluation
and wider context before the project adds a model.


## Links

- project: [[Agent-first Writing Editor]]
