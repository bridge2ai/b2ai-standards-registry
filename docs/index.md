# standards-schema-all

High-level classes for Bridge2AI Standards schemas.

URI: https://w3id.org/bridge2ai/standards-schema-all
Name: standards-schema-all



## Classes

| Class | Description |
| --- | --- |
| [BiomedicalStandard](BiomedicalStandard.md) | Represents a standard in the Bridge2AI Standards Registry with particular app... |
| [DataStandard](DataStandard.md) | Represents a general purpose standard in the Bridge2AI Standards Registry |
| [DataStandardOrTool](DataStandardOrTool.md) | Represents a standard or tool in the Bridge2AI Standards Registry |
| [DataStandardOrToolContainer](DataStandardOrToolContainer.md) | A container for DataStandardOrTool(s) |
| [DataSubstrate](DataSubstrate.md) | Represents a data substrate for Bridge2AI data |
| [DataSubstrateContainer](DataSubstrateContainer.md) | A container for DataSubstrates |
| [DataTopic](DataTopic.md) | Represents a general data topic for Bridge2AI data or the tools/standards app... |
| [DataTopicContainer](DataTopicContainer.md) | A container for DataTopics |
| [ModelRepository](ModelRepository.md) | Represents a resource in the Bridge2AI Standards Registry serving to curate a... |
| [NamedThing](NamedThing.md) | A generic grouping for any identifiable entity |
| [OntologyOrVocabulary](OntologyOrVocabulary.md) | A set of concepts and categories, potentially defined or accompanied by their... |
| [Organization](Organization.md) | Represents a group or organization related to or responsible for one or more ... |
| [OrganizationContainer](OrganizationContainer.md) | A container for Organizations |
| [ReferenceDataOrDataset](ReferenceDataOrDataset.md) | Represents a resource in the Bridge2AI Standards Registry serving as a standa... |
| [ReferenceImplementation](ReferenceImplementation.md) | Represents an implementation of one or more standards or tools in the Bridge2... |
| [Registry](Registry.md) | Represents a resource in the Bridge2AI Standards Registry serving to curate a... |
| [SoftwareOrTool](SoftwareOrTool.md) | Represents a piece of software or computational tool in the Bridge2AI Standar... |
| [TrainingProgram](TrainingProgram.md) | Represents a training program for skills and experience related to standards ... |
| [UseCase](UseCase.md) | Represents a use case for Bridge2AI standards |
| [UseCaseContainer](UseCaseContainer.md) | A container for UseCase |


## Slots

| Slot | Description |
| --- | --- |
| [alternative_standards_and_tools](alternative_standards_and_tools.md) | List of identifiers of standards and tools; those not explicitly planned to b... |
| [collection](collection.md) | Tags for specific sets of standards |
| [concerns_data_topic](concerns_data_topic.md) | Subject standard is generally applied in the context of object data topic |
| [data_standardortools_collection](data_standardortools_collection.md) |  |
| [data_substrates](data_substrates.md) | Relevance of the use case to one or more data substrates |
| [data_substrates_collection](data_substrates_collection.md) |  |
| [data_topics](data_topics.md) | Relevance of the use case to one or more data topics |
| [data_topics_collection](data_topics_collection.md) |  |
| [description](description.md) | A human-readable description for a thing |
| [edam_id](edam_id.md) |  |
| [enables](enables.md) | Other use case(s) this use case supports or makes possible |
| [file_extensions](file_extensions.md) | Commonly used file extensions for this substrate |
| [formal_specification](formal_specification.md) | Relevant code repository or other location for a formal specification of the ... |
| [has_relevant_organization](has_relevant_organization.md) | Subject standard is managed or otherwise guided buy the object organization(s... |
| [id](id.md) | A unique identifier for a thing |
| [involved_in_experimental_design](involved_in_experimental_design.md) | True if use case is likely to be implemented as part of an experimental proce... |
| [involved_in_metadata_management](involved_in_metadata_management.md) | True if use case is likely to be implemented as part of metadata indexing, sa... |
| [involved_in_quality_control](involved_in_quality_control.md) | True is use case is likely to be implemented as part of data validation opera... |
| [is_open](is_open.md) | Is the standard or tool FAIR and available free of cost? |
| [known_limitations](known_limitations.md) | Any current obstacles to implementing this use case |
| [limitations](limitations.md) | Potential obstacles particular to this substrate or implementation |
| [mesh_id](mesh_id.md) |  |
| [metadata_storage](metadata_storage.md) | Data Substrate in which metadata is stored |
| [name](name.md) | A human-readable name for a thing |
| [ncit_id](ncit_id.md) |  |
| [node_property](node_property.md) | A grouping for any property that holds between a node and a value |
| [organizations](organizations.md) |  |
| [publication](publication.md) | Relevant publication for the standard or tool |
| [purpose_detail](purpose_detail.md) | Text description of the standard or tool |
| [related_to](related_to.md) | A relationship that is asserted between two named things |
| [relevance_to_dgps](relevance_to_dgps.md) | Relevance of the use case to one or more DGPs |
| [requires_registration](requires_registration.md) | Does usage of the standard or tool require registrion of a user or group with... |
| [ror_id](ror_id.md) |  |
| [standards_and_tools_for_dgp_use](standards_and_tools_for_dgp_use.md) | List of identifiers of standards and tools; those planned to be used, or alre... |
| [subclass_of](subclass_of.md) | Holds between two classes where the domain class is a specialization of the r... |
| [url](url.md) | URL for basic documentation of the standard or tool |
| [use_case_category](use_case_category.md) | Category of the UseCase |
| [use_cases](use_cases.md) |  |
| [wikidata_id](wikidata_id.md) |  |
| [xref](xref.md) | URI of corresponding class in an ontology of experimental procedures, in CURI... |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [DataGeneratingProject](DataGeneratingProject.md) | One of the Bridge2AI Data Generating Projects |
| [StandardsCollectionTag](StandardsCollectionTag.md) | Tags for specific sets of standards |
| [UseCaseCategory](UseCaseCategory.md) | Category of use case |


## Types

| Type | Description |
| --- | --- |
| [Boolean](Boolean.md) | A binary (true or false) value |
| [Date](Date.md) | a date (year, month and day) in an idealized calendar |
| [DateOrDatetime](DateOrDatetime.md) | Either a date or a datetime |
| [Datetime](Datetime.md) | The combination of a date and time |
| [Decimal](Decimal.md) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [Double](Double.md) | A real number that conforms to the xsd:double specification |
| [EdamIdentifier](EdamIdentifier.md) |  |
| [Float](Float.md) | A real number that conforms to the xsd:float specification |
| [Integer](Integer.md) | An integer |
| [MeshIdentifier](MeshIdentifier.md) |  |
| [NcitIdentifier](NcitIdentifier.md) |  |
| [Ncname](Ncname.md) | Prefix part of CURIE |
| [Nodeidentifier](Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Objectidentifier](Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [RorIdentifier](RorIdentifier.md) |  |
| [String](String.md) | A character string |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |
| [WikidataIdentifier](WikidataIdentifier.md) |  |


## Subsets

| Subset | Description |
| --- | --- |
