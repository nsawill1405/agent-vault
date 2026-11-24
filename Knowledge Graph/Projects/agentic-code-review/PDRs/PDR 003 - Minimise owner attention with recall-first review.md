---
title: "PDR 003: Minimise owner attention with recall-first review"
type: product-decision
date: "2026-09-30"
status: "Accepted"
decision_date: "2026-09-30"
tags:
  - hq
  - product-decision
source: "https://robbiepalmer.me/projects/agentic-code-review/pdrs/003-recall-first-agent-mediated-review"
author: Robbie Palmer
---

# PDR 003: Minimise owner attention with recall-first review

## Context

The reviewer originally treated acceptance rate and raw noise as promotion
constraints. That fits a workflow where every comment reaches a person. Here,
coding agents investigate most review findings before the owner intervenes.

A divergent scout may raise a higher number of false claims while still
finding a serious problem the authoring model missed. Investigating those
claims consumes money, elapsed time, and agent work. It can be a good trade
when it reduces the owner's review time or prevents later debugging and repair.

Correctness and downstream value are related but not identical. A wrong review
claim may prompt an independently useful improvement, while a technically
correct comment may create no useful action.

## Decision

Optimise review policy to minimise the owner's expected attention across the
life of a change. Use recall and incremental useful discovery as the main means
of doing that. Keep raw precision and rejection rate as diagnostics rather than
automatic promotion gates.

Count owner review and triage, interventions needed to unblock agents,
review-driven rework, and later work caused by escaped defects. Track
inference spend, latency, and agent investigation as constraints. Do not count
busywork as value merely because a review comment caused a patch.

Measure each scout's marginal useful contribution after reconciliation.
Duplicate findings do not add recall. Keep the cited finding's correctness
separate from its downstream effect: direct fix, independently useful
improvement, no material change, harmful churn, or unknown effect.

A precision loss is acceptable only when it lowers expected owner attention
within declared money, time, and safety limits. The final patch must still pass
the project's checks, and review findings must continue through the single
reconciled publication path.

## Consequences

The ensemble can retain genuinely different models instead of selecting only
the safest consensus comments. The product may spend more inference and agent
work to save human attention.

This policy can fail by flooding the owner, encouraging unsafe edits, delaying
delivery, or manufacturing changes that make noisy review appear productive.
Evaluation must inspect the resulting patch and record owner interventions,
not reward compliance or finding count.

## Evaluation

Reconsider the policy if marginal findings rarely survive adjudication,
agent-mediated triage increases total owner attention, or money, delay, or
safety crosses its declared limit. Compare scouts through controlled ablation
and keep harmful churn and escaped defects visible beside useful discovery.

## Migration note

This record preserves the product objective and promotion policy formerly
mixed into ADR 005. It keeps the original date and Accepted status. ADR 005 now
retains the technical record changes needed to measure correctness and
downstream utility separately. No product policy changed during migration.


## Links

- informed by adrs: [[ADR 001 - Stateful AI Code Review]]
- informed by adrs: [[ADR 002 - DuckDB for the AI Review Scorecard]]
- informed by adrs: [[ADR 004 - Use AACR-Bench as a Secondary Challenge Set]]
- project: [[Agentic Code Review]]
