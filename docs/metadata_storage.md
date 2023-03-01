# Slot: metadata_storage
_Data Substrate in which metadata is stored._


URI: [STANDARDSDATASUBSTRATE:metadata_storage](https://w3id.org/bridge2ai/standards-datasubstrate-schema/metadata_storage)




## Inheritance

* [node_property](node_property.md)
    * **metadata_storage**





## Applicable Classes

| Name | Description |
| --- | --- |
[DataSubstrate](DataSubstrate.md) | Represents a data substrate for Bridge2AI data






## Properties

* Range: [xsd:string](xsd:string)
* Multivalued: True








## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/bridge2ai/standards-datasubstrate-schema




## LinkML Source

<details>
```yaml
name: metadata_storage
description: Data Substrate in which metadata is stored.
from_schema: https://w3id.org/bridge2ai/standards-datasubstrate-schema
rank: 1000
is_a: node property
domain: NamedThing
multivalued: true
alias: metadata_storage
domain_of:
- DataSubstrate
range: string
any_of:
- range: DataSubstrate
- equals_string: file headers

```
</details>