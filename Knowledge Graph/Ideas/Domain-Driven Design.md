---
title: "Domain-Driven Design"
type: idea
description: "Model software around the language, rules, and boundaries of the problem domain."
source_url: "https://www.domainlanguage.com/ddd/"
tags:
  - hq
  - idea
source: "https://robbiepalmer.me/ideas/domain-driven-design"
author: Robbie Palmer
---

# Domain-Driven Design

Domain-Driven Design treats the domain model as a product of sustained collaboration between domain
experts and software builders. The model lives in code and language, not in a diagram handed over
before development begins.

Its most useful move is admitting that one universal model is often worse than several explicit
ones. A term can mean different things in different [[Bounded Context|bounded contexts]]. A
context map then describes how those models meet and where translation belongs.

I care less about reproducing every named tactical pattern than about keeping language honest. If
the team, interface, database, and user all use the same word for different concepts, the design is
already accumulating ambiguity.

## Questions it prompts

* What language do the people doing the work already use?
* Where does the meaning of a term change?
* Which rules belong together and which should stay behind a translation boundary?


## Links

- related ideas: [[Bounded Context]]
- related ideas: [[Data Mesh]]
- related ideas: [[EventStorming]]
