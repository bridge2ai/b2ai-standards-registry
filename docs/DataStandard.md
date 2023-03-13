# Class: DataStandard
_Represents a general purpose standard in the Bridge2AI Standards Registry._




URI: [https://w3id.org/bridge2ai/standards-schema-all/:DataStandard](https://w3id.org/bridge2ai/standards-schema-all/:DataStandard)



```mermaid
 classDiagram
    class DataStandard
      DataStandardOrTool <|-- DataStandard
      
      DataStandard : collection
        DataStandard <.. StandardsCollectionTag : collection
      DataStandard : concerns_data_topic
        DataStandard <.. DataTopic : concerns_data_topic
      DataStandard : description
        DataStandard <.. string : description
      DataStandard : formal_specification
        DataStandard <.. uriorcurie : formal_specification
      DataStandard : has_relevant_organization
        DataStandard <.. Organization : has_relevant_organization
      DataStandard : id
        DataStandard <.. uriorcurie : id
      DataStandard : is_open
        DataStandard <.. boolean : is_open
      DataStandard : name
        DataStandard <.. string : name
      DataStandard : publication
        DataStandard <.. uriorcurie : publication
      DataStandard : purpose_detail
        DataStandard <.. string : purpose_detail
      DataStandard : related_to
        DataStandard <.. NamedThing : related_to
      DataStandard : requires_registration
        DataStandard <.. boolean : requires_registration
      DataStandard : subclass_of
        DataStandard <.. NamedThing : subclass_of
      DataStandard : url
        DataStandard <.. uriorcurie : url
      

      DataStandard <|-- BiomedicalStandard
      
      DataStandard : collection
        DataStandard <.. StandardsCollectionTag : collection
      DataStandard : concerns_data_topic
        DataStandard <.. DataTopic : concerns_data_topic
      DataStandard : description
        DataStandard <.. string : description
      DataStandard : formal_specification
        DataStandard <.. uriorcurie : formal_specification
      DataStandard : has_relevant_organization
        DataStandard <.. Organization : has_relevant_organization
      DataStandard : id
        DataStandard <.. uriorcurie : id
      DataStandard : is_open
        DataStandard <.. boolean : is_open
      DataStandard : name
        DataStandard <.. string : name
      DataStandard : publication
        DataStandard <.. uriorcurie : publication
      DataStandard : purpose_detail
        DataStandard <.. string : purpose_detail
      DataStandard : related_to
        DataStandard <.. NamedThing : related_to
      DataStandard : requires_registration
        DataStandard <.. boolean : requires_registration
      DataStandard : subclass_of
        DataStandard <.. NamedThing : subclass_of
      DataStandard : url
        DataStandard <.. uriorcurie : url
      
```





## Inheritance
* [NamedThing](NamedThing.md)
    * [DataStandardOrTool](DataStandardOrTool.md)
        * **DataStandard**
            * [BiomedicalStandard](BiomedicalStandard.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [collection](collection.md) | 0..* <br/> [StandardsCollectionTag](StandardsCollectionTag.md) | Tags for specific sets of standards | [DataStandardOrTool](DataStandardOrTool.md) |
| [concerns_data_topic](concerns_data_topic.md) | 0..* <br/> [DataTopic](DataTopic.md) | Subject standard is generally applied in the context of object data topic | [DataStandardOrTool](DataStandardOrTool.md) |
| [has_relevant_organization](has_relevant_organization.md) | 0..* <br/> [Organization](Organization.md) | Subject standard is managed or otherwise guided buy the object organization(s... | [DataStandardOrTool](DataStandardOrTool.md) |
| [purpose_detail](purpose_detail.md) | 0..1 <br/> [String](String.md) | Text description of the standard or tool | [DataStandardOrTool](DataStandardOrTool.md) |
| [is_open](is_open.md) | 0..1 <br/> [Boolean](Boolean.md) | Is the standard or tool FAIR and available free of cost? | [DataStandardOrTool](DataStandardOrTool.md) |
| [requires_registration](requires_registration.md) | 0..1 <br/> [Boolean](Boolean.md) | Does usage of the standard or tool require registrion of a user or group with... | [DataStandardOrTool](DataStandardOrTool.md) |
| [url](url.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | URL for basic documentation of the standard or tool | [DataStandardOrTool](DataStandardOrTool.md) |
| [publication](publication.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | Relevant publication for the standard or tool | [DataStandardOrTool](DataStandardOrTool.md) |
| [formal_specification](formal_specification.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | Relevant code repository or other location for a formal specification of the ... | [DataStandardOrTool](DataStandardOrTool.md) |
| [id](id.md) | 1..1 <br/> [Uriorcurie](Uriorcurie.md) | A unique identifier for a thing | [NamedThing](NamedThing.md) |
| [name](name.md) | 0..1 <br/> [String](String.md) | A human-readable name for a thing | [NamedThing](NamedThing.md) |
| [description](description.md) | 0..1 <br/> [String](String.md) | A human-readable description for a thing | [NamedThing](NamedThing.md) |
| [subclass_of](subclass_of.md) | 0..* <br/> [NamedThing](NamedThing.md) | Holds between two classes where the domain class is a specialization of the r... | [NamedThing](NamedThing.md) |
| [related_to](related_to.md) | 0..* <br/> [NamedThing](NamedThing.md) | A relationship that is asserted between two named things | [NamedThing](NamedThing.md) |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/bridge2ai/standards-schema-all





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/bridge2ai/standards-schema-all/:DataStandard |
| native | https://w3id.org/bridge2ai/standards-schema-all/:DataStandard |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: DataStandard
description: Represents a general purpose standard in the Bridge2AI Standards Registry.
from_schema: https://w3id.org/bridge2ai/standards-schema-all
rank: 1000
is_a: DataStandardOrTool

```
</details>

### Induced

<details>
```yaml
name: DataStandard
description: Represents a general purpose standard in the Bridge2AI Standards Registry.
from_schema: https://w3id.org/bridge2ai/standards-schema-all
rank: 1000
is_a: DataStandardOrTool
attributes:
  collection:
    name: collection
    description: Tags for specific sets of standards.
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    is_a: node property
    domain: NamedThing
    multivalued: true
    alias: collection
    owner: DataStandard
    domain_of:
    - DataStandardOrTool
    range: StandardsCollectionTag
  concerns_data_topic:
    name: concerns_data_topic
    description: Subject standard is generally applied in the context of object data
      topic.
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    is_a: related_to
    domain: DataStandardOrTool
    multivalued: true
    inherited: true
    alias: concerns_data_topic
    owner: DataStandard
    domain_of:
    - DataStandardOrTool
    range: DataTopic
  has_relevant_organization:
    name: has_relevant_organization
    description: Subject standard is managed or otherwise guided buy the object organization(s).
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    is_a: related_to
    domain: DataStandardOrTool
    multivalued: true
    inherited: true
    alias: has_relevant_organization
    owner: DataStandard
    domain_of:
    - DataStandardOrTool
    range: Organization
  purpose_detail:
    name: purpose_detail
    description: Text description of the standard or tool.
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    is_a: node property
    domain: NamedThing
    alias: purpose_detail
    owner: DataStandard
    domain_of:
    - DataStandardOrTool
    range: string
  is_open:
    name: is_open
    description: Is the standard or tool FAIR and available free of cost?
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    is_a: node property
    domain: NamedThing
    alias: is_open
    owner: DataStandard
    domain_of:
    - DataStandardOrTool
    range: boolean
  requires_registration:
    name: requires_registration
    description: Does usage of the standard or tool require registrion of a user or
      group with some organization or managerial body?
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    is_a: node property
    domain: NamedThing
    alias: requires_registration
    owner: DataStandard
    domain_of:
    - DataStandardOrTool
    range: boolean
  url:
    name: url
    description: URL for basic documentation of the standard or tool.
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    is_a: node property
    domain: NamedThing
    alias: url
    owner: DataStandard
    domain_of:
    - DataStandardOrTool
    - Organization
    range: uriorcurie
  publication:
    name: publication
    description: Relevant publication for the standard or tool. Prefer a DOI or PUBMED.
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    is_a: node property
    domain: NamedThing
    alias: publication
    owner: DataStandard
    domain_of:
    - DataStandardOrTool
    range: uriorcurie
  formal_specification:
    name: formal_specification
    description: Relevant code repository or other location for a formal specification
      of the standard or tool. Often a URL, particularly to a Git repository.
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    is_a: node property
    domain: NamedThing
    alias: formal_specification
    owner: DataStandard
    domain_of:
    - DataStandardOrTool
    range: uriorcurie
  id:
    name: id
    description: A unique identifier for a thing.
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    slot_uri: schema:identifier
    identifier: true
    alias: id
    owner: DataStandard
    domain_of:
    - NamedThing
    range: uriorcurie
    required: true
  name:
    name: name
    description: A human-readable name for a thing.
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    slot_uri: schema:name
    alias: name
    owner: DataStandard
    domain_of:
    - NamedThing
    range: string
  description:
    name: description
    description: A human-readable description for a thing.
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    slot_uri: schema:description
    alias: description
    owner: DataStandard
    domain_of:
    - NamedThing
    range: string
  subclass_of:
    name: subclass_of
    description: Holds between two classes where the domain class is a specialization
      of the range class.
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    exact_mappings:
    - rdfs:subClassOf
    - MESH:isa
    narrow_mappings:
    - rdfs:subPropertyOf
    rank: 1000
    is_a: related_to
    domain: NamedThing
    multivalued: true
    inherited: true
    alias: subclass_of
    owner: DataStandard
    domain_of:
    - NamedThing
    range: NamedThing
  related_to:
    name: related_to
    description: A relationship that is asserted between two named things.
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    domain: NamedThing
    multivalued: true
    inherited: true
    alias: related_to
    owner: DataStandard
    domain_of:
    - NamedThing
    - Organization
    symmetric: true
    range: NamedThing

```
</details>