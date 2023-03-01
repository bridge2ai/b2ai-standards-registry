# Class: OrganizationContainer
_A container for Organizations._




URI: [STANDARDSORGANIZATION:OrganizationContainer](https://w3id.org/bridge2ai/standards-organization-schema/OrganizationContainer)



```mermaid
 classDiagram
    class OrganizationContainer
      OrganizationContainer : organizations
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [organizations](organizations.md) | 0..* <br/> [Organization](Organization.md) |  | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/bridge2ai/standards-organization-schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | STANDARDSORGANIZATION:OrganizationContainer |
| native | STANDARDSORGANIZATION:OrganizationContainer |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: OrganizationContainer
description: A container for Organizations.
from_schema: https://w3id.org/bridge2ai/standards-organization-schema
rank: 1000
slots:
- organizations

```
</details>

### Induced

<details>
```yaml
name: OrganizationContainer
description: A container for Organizations.
from_schema: https://w3id.org/bridge2ai/standards-organization-schema
rank: 1000
attributes:
  organizations:
    name: organizations
    from_schema: https://w3id.org/bridge2ai/standards-organization-schema
    rank: 1000
    multivalued: true
    alias: organizations
    owner: OrganizationContainer
    domain_of:
    - OrganizationContainer
    range: Organization
    inlined: true
    inlined_as_list: true

```
</details>