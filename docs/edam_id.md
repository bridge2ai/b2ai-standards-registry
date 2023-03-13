# Slot: edam_id

URI: [https://w3id.org/bridge2ai/standards-schema-all/:edam_id](https://w3id.org/bridge2ai/standards-schema-all/:edam_id)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[DataTopic](DataTopic.md) | Represents a general data topic for Bridge2AI data or the tools/standards app...
[DataSubstrate](DataSubstrate.md) | Represents a data substrate for Bridge2AI data






## Properties

* Range: [EdamIdentifier](EdamIdentifier.md)








## Examples

| Value |
| --- |
| edam.data:0006 |

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/bridge2ai/standards-schema-all




## LinkML Source

<details>
```yaml
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
domain_of:
- DataTopic
- DataSubstrate
range: edam_identifier

```
</details>