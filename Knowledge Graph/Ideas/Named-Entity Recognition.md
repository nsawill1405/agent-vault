---
title: "Named-Entity Recognition"
type: idea
description: "NER finds spans of text that name entities and assigns them types such as people, organisations, products, or identifiers."
source_url: "https://en.wikipedia.org/wiki/Named-entity_recognition"
tags:
  - hq
  - idea
source: "https://robbiepalmer.me/ideas/ner"
author: Robbie Palmer
---

# Named-Entity Recognition

Named-entity recognition, or NER, finds mentions of entities in text and assigns each mention a
type. A general model may recognise people, organisations, and places. A domain model might instead
need shipment numbers, carriers, ingredients, medical conditions, or account identifiers.

NER is an [[NLP|NLP]] task, but its labels come from the problem being solved. The same text
can need different boundaries and types in different systems. "New York Times" may be one
organisation mention in a news index, while another task may care about the place name inside it.
[[Ontology Engineering|Ontology Engineering]] makes those categories and distinctions
explicit.

Recognition does not establish identity. Finding two mentions of "Starbucks" does not prove that
they refer to the same company or branch. Entity resolution handles that later question. In
[[Intelligent Document Processing|Intelligent Document Processing]], NER can turn recognised
text into candidate fields before validation and review.

## Questions it prompts

* Which entity types affect a real product decision?
* How should overlapping, nested, or ambiguous mentions be labelled?
* Does evaluation score exact text boundaries as well as the entity type?
* Which rules, dictionaries, or checks should complement the model?


## Links

- related ideas: [[NLP]]
- related ideas: [[Intelligent Document Processing]]
- related ideas: [[Ontology Engineering]]
