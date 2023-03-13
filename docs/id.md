# Slot: id
_A unique identifier for a thing._


URI: [schema:identifier](http://schema.org/identifier)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[NamedThing](NamedThing.md) | A generic grouping for any identifiable entity
[UseCase](UseCase.md) | Represents a use case for Bridge2AI standards
[DataStandardOrTool](DataStandardOrTool.md) | Represents a standard or tool in the Bridge2AI Standards Registry
[DataStandard](DataStandard.md) | Represents a general purpose standard in the Bridge2AI Standards Registry
[BiomedicalStandard](BiomedicalStandard.md) | Represents a standard in the Bridge2AI Standards Registry with particular app...
[Registry](Registry.md) | Represents a resource in the Bridge2AI Standards Registry serving to curate a...
[OntologyOrVocabulary](OntologyOrVocabulary.md) | A set of concepts and categories, potentially defined or accompanied by their...
[ModelRepository](ModelRepository.md) | Represents a resource in the Bridge2AI Standards Registry serving to curate a...
[ReferenceDataOrDataset](ReferenceDataOrDataset.md) | Represents a resource in the Bridge2AI Standards Registry serving as a standa...
[SoftwareOrTool](SoftwareOrTool.md) | Represents a piece of software or computational tool in the Bridge2AI Standar...
[ReferenceImplementation](ReferenceImplementation.md) | Represents an implementation of one or more standards or tools in the Bridge2...
[TrainingProgram](TrainingProgram.md) | Represents a training program for skills and experience related to standards ...
[DataTopic](DataTopic.md) | Represents a general data topic for Bridge2AI data or the tools/standards app...
[Organization](Organization.md) | Represents a group or organization related to or responsible for one or more ...
[DataSubstrate](DataSubstrate.md) | Represents a data substrate for Bridge2AI data






## Properties

* Range: [Uriorcurie](Uriorcurie.md)
* Required: True








## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/bridge2ai/standards-schema-all




## LinkML Source

<details>
```yaml
name: id
description: A unique identifier for a thing.
from_schema: https://w3id.org/bridge2ai/standards-schema-all
rank: 1000
slot_uri: schema:identifier
identifier: true
alias: id
domain_of:
- NamedThing
range: uriorcurie
required: true

```
</details>