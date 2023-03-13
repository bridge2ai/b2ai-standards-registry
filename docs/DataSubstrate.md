# Class: DataSubstrate
_Represents a data substrate for Bridge2AI data. This may be a high-level data structure or a specific implementation of that structure. Interpret as "data, in this form or format", as compared to DataStandard, which refers to the set of rules defining a standard. For example, data in TSV format is represented as a DataSubstrate but the concept of TSV format is a DataStandard._




URI: [https://w3id.org/bridge2ai/standards-schema-all/:DataSubstrate](https://w3id.org/bridge2ai/standards-schema-all/:DataSubstrate)



```mermaid
 classDiagram
    class DataSubstrate
      NamedThing <|-- DataSubstrate
      
      DataSubstrate : description
        DataSubstrate <.. string : description
      DataSubstrate : edam_id
        DataSubstrate <.. edam_identifier : edam_id
      DataSubstrate : file_extensions
        DataSubstrate <.. string : file_extensions
      DataSubstrate : id
        DataSubstrate <.. uriorcurie : id
      DataSubstrate : limitations
        DataSubstrate <.. string : limitations
      DataSubstrate : mesh_id
        DataSubstrate <.. mesh_identifier : mesh_id
      DataSubstrate : metadata_storage
        DataSubstrate <.. string : metadata_storage
      DataSubstrate : name
        DataSubstrate <.. string : name
      DataSubstrate : ncit_id
        DataSubstrate <.. ncit_identifier : ncit_id
      DataSubstrate : related_to
        DataSubstrate <.. NamedThing : related_to
      DataSubstrate : subclass_of
        DataSubstrate <.. NamedThing : subclass_of
      
```





## Inheritance
* [NamedThing](NamedThing.md)
    * **DataSubstrate**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [edam_id](edam_id.md) | 0..1 <br/> [EdamIdentifier](EdamIdentifier.md) |  | direct |
| [mesh_id](mesh_id.md) | 0..1 <br/> [MeshIdentifier](MeshIdentifier.md) |  | direct |
| [ncit_id](ncit_id.md) | 0..1 <br/> [NcitIdentifier](NcitIdentifier.md) |  | direct |
| [metadata_storage](metadata_storage.md) | 0..* <br/> [String](String.md) | Data Substrate in which metadata is stored | direct |
| [file_extensions](file_extensions.md) | 0..* <br/> [String](String.md) | Commonly used file extensions for this substrate | direct |
| [limitations](limitations.md) | 0..* <br/> [String](String.md) | Potential obstacles particular to this substrate or implementation | direct |
| [id](id.md) | 1..1 <br/> [Uriorcurie](Uriorcurie.md) | A unique identifier for a thing | [NamedThing](NamedThing.md) |
| [name](name.md) | 0..1 <br/> [String](String.md) | A human-readable name for a thing | [NamedThing](NamedThing.md) |
| [description](description.md) | 0..1 <br/> [String](String.md) | A human-readable description for a thing | [NamedThing](NamedThing.md) |
| [subclass_of](subclass_of.md) | 0..* <br/> [NamedThing](NamedThing.md) | Holds between two classes where the domain class is a specialization of the r... | [NamedThing](NamedThing.md) |
| [related_to](related_to.md) | 0..* <br/> [NamedThing](NamedThing.md) | A relationship that is asserted between two named things | [NamedThing](NamedThing.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [UseCase](UseCase.md) | [data_substrates](data_substrates.md) | range | [DataSubstrate](DataSubstrate.md) |
| [DataSubstrateContainer](DataSubstrateContainer.md) | [data_substrates_collection](data_substrates_collection.md) | range | [DataSubstrate](DataSubstrate.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/bridge2ai/standards-schema-all





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://w3id.org/bridge2ai/standards-schema-all/:DataSubstrate |
| native | https://w3id.org/bridge2ai/standards-schema-all/:DataSubstrate |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: DataSubstrate
description: Represents a data substrate for Bridge2AI data. This may be a high-level
  data structure or a specific implementation of that structure. Interpret as "data,
  in this form or format", as compared to DataStandard, which refers to the set of
  rules defining a standard. For example, data in TSV format is represented as a DataSubstrate
  but the concept of TSV format is a DataStandard.
from_schema: https://w3id.org/bridge2ai/standards-schema-all
rank: 1000
is_a: NamedThing
slots:
- edam_id
- mesh_id
- ncit_id
- metadata_storage
- file_extensions
- limitations

```
</details>

### Induced

<details>
```yaml
name: DataSubstrate
description: Represents a data substrate for Bridge2AI data. This may be a high-level
  data structure or a specific implementation of that structure. Interpret as "data,
  in this form or format", as compared to DataStandard, which refers to the set of
  rules defining a standard. For example, data in TSV format is represented as a DataSubstrate
  but the concept of TSV format is a DataStandard.
from_schema: https://w3id.org/bridge2ai/standards-schema-all
rank: 1000
is_a: NamedThing
attributes:
  edam_id:
    name: edam_id
    examples:
    - value: edam.data:0006
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    values_from:
    - edam.data
    - edam.format
    - edam.operation
    - edam.topic
    alias: edam_id
    owner: DataSubstrate
    domain_of:
    - DataTopic
    - DataSubstrate
    range: edam_identifier
  mesh_id:
    name: mesh_id
    examples:
    - value: MeSH:D014831
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    values_from:
    - MeSH
    alias: mesh_id
    owner: DataSubstrate
    domain_of:
    - DataTopic
    - DataSubstrate
    range: mesh_identifier
  ncit_id:
    name: ncit_id
    examples:
    - value: NCIT:C92692
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    values_from:
    - NCIT
    alias: ncit_id
    owner: DataSubstrate
    domain_of:
    - DataTopic
    - DataSubstrate
    range: ncit_identifier
  metadata_storage:
    name: metadata_storage
    description: Data Substrate in which metadata is stored.
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    is_a: node property
    domain: NamedThing
    multivalued: true
    alias: metadata_storage
    owner: DataSubstrate
    domain_of:
    - DataSubstrate
    range: string
    any_of:
    - range: DataSubstrate
    - equals_string: file headers
  file_extensions:
    name: file_extensions
    description: Commonly used file extensions for this substrate.
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    is_a: node property
    domain: NamedThing
    multivalued: true
    alias: file_extensions
    owner: DataSubstrate
    domain_of:
    - DataSubstrate
    range: string
  limitations:
    name: limitations
    description: 'Potential obstacles particular to this substrate or implementation. '
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    is_a: node property
    domain: NamedThing
    multivalued: true
    alias: limitations
    owner: DataSubstrate
    domain_of:
    - DataSubstrate
    range: string
  id:
    name: id
    description: A unique identifier for a thing.
    from_schema: https://w3id.org/bridge2ai/standards-schema-all
    rank: 1000
    slot_uri: schema:identifier
    identifier: true
    alias: id
    owner: DataSubstrate
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
    owner: DataSubstrate
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
    owner: DataSubstrate
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
    owner: DataSubstrate
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
    owner: DataSubstrate
    domain_of:
    - NamedThing
    - Organization
    symmetric: true
    range: NamedThing

```
</details>