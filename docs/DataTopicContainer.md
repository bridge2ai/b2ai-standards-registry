# Class: DataTopicContainer
_A container for DataTopics._




URI: [STANDARDSDATATOPIC:DataTopicContainer](https://w3id.org/bridge2ai/standards-datatopic-schema/DataTopicContainer)



```mermaid
 classDiagram
    class DataTopicContainer
      DataTopicContainer : data_topics_collection
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [data_topics_collection](data_topics_collection.md) | 0..* <br/> [DataTopic](DataTopic.md) |  | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/bridge2ai/standards-datatopic-schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | STANDARDSDATATOPIC:DataTopicContainer |
| native | STANDARDSDATATOPIC:DataTopicContainer |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: DataTopicContainer
description: A container for DataTopics.
from_schema: https://w3id.org/bridge2ai/standards-datatopic-schema
rank: 1000
slots:
- data_topics_collection

```
</details>

### Induced

<details>
```yaml
name: DataTopicContainer
description: A container for DataTopics.
from_schema: https://w3id.org/bridge2ai/standards-datatopic-schema
rank: 1000
attributes:
  data_topics_collection:
    name: data_topics_collection
    from_schema: https://w3id.org/bridge2ai/standards-datatopic-schema
    rank: 1000
    multivalued: true
    alias: data_topics_collection
    owner: DataTopicContainer
    domain_of:
    - DataTopicContainer
    range: DataTopic
    inlined: true
    inlined_as_list: true

```
</details>