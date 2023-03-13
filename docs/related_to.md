# Slot: related_to
_A relationship that is asserted between two named things._


URI: [https://w3id.org/bridge2ai/standards-schema-all/:related_to](https://w3id.org/bridge2ai/standards-schema-all/:related_to)




## Inheritance

* **related_to**
    * [concerns_data_topic](concerns_data_topic.md)
    * [has_relevant_organization](has_relevant_organization.md)
    * [subclass_of](subclass_of.md)





## Applicable Classes

| Name | Description |
| --- | --- |
[NamedThing](NamedThing.md) | A generic grouping for any identifiable entity
[Organization](Organization.md) | Represents a group or organization related to or responsible for one or more ...
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
[DataSubstrate](DataSubstrate.md) | Represents a data substrate for Bridge2AI data






## Properties

* Range: [NamedThing](NamedThing.md)
* Multivalued: True








## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/bridge2ai/standards-schema-all




## LinkML Source

<details>
```yaml
name: related_to
description: A relationship that is asserted between two named things.
from_schema: https://w3id.org/bridge2ai/standards-schema-all
rank: 1000
domain: NamedThing
multivalued: true
inherited: true
alias: related_to
domain_of:
- NamedThing
- Organization
symmetric: true
range: NamedThing

```
</details>