---
title: "Bounded Context"
type: idea
description: "An explicit boundary within which one domain model and its language have a consistent meaning."
source_url: "https://martinfowler.com/bliki/BoundedContext.html"
tags:
  - hq
  - idea
source: "https://robbiepalmer.me/ideas/bounded-context"
author: Robbie Palmer
---

# Bounded Context

A bounded context defines where a domain model applies. Inside the boundary, terms, rules, and
assumptions should have one consistent meaning. Outside it, another model may use the same words
differently.

The boundary makes disagreement manageable. "Customer" can mean the person receiving an order in
one context and the account responsible for payment in another. Neither definition needs to become
universal. A context map records how the models relate and where translation belongs.

Bounded contexts are part of [[Domain-Driven Design|Domain-Driven Design]]. They do not have to
match microservices, databases, or teams one for one. Those boundaries often align because
[[Conway's Law|Conway's Law]] pulls architecture towards communication paths, but treating the
org chart as the model skips the domain work.

[[Ontology Engineering|Ontology Engineering]] can define concepts within a context and map
them to concepts elsewhere. The mapping should preserve differences instead of forcing every
context into one vocabulary.

## Questions it prompts

* Where does the meaning of an important term change?
* Which rules must remain consistent together?
* What must be translated when information crosses the boundary?
* Does the team that owns the model have authority to change and operate it?


## Links

- related ideas: [[Domain-Driven Design]]
- related ideas: [[Data Mesh]]
- related ideas: [[Ontology Engineering]]
- related ideas: [[Conway's Law]]
