---
title: "ADR 009: Python as the primary language"
type: decision
date: "2026-09-12"
status: "Accepted"
tags:
  - hq
  - decision
source: "https://robbiepalmer.me/projects/agent-first-writing/adrs/009-primary-language-python"
author: Robbie Palmer
---

# ADR 009: Python as the primary language

## Context

The platform's TypeScript default fits interactive applications, but this
editor trains and evaluates language models with PyTorch and Hugging Face.
Those libraries and the existing evaluation pipeline are Python-native.

## Decision

Override the platform's primary-language slot with Python. This activates the
Python layer for validation and test-case defaults without changing the
platform choice for other projects.

## Consequences

The project follows Python tooling by default. Browser interfaces may still
use TypeScript as a supplemental language and record it directly.


## Links

- project: [[Agent-first Writing Editor]]
