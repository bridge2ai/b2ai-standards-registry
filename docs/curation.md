# Curation Guide

The tasks listed below all help to make the Bridge2AI Standards Registry more complete and informative.

The "source of truth" data for the Registry is all located in the `b2ai-standards-registry` repository within the directory `src/data/`.

Each YAML document in this directory is a single data table named for its contents (e.g., every item in `DataStandardOrTool.yaml` is an object of the `DataStandardOrTool` class in the [corresponding schema](https://github.com/bridge2ai/b2ai-standards-registry/blob/main/src/schema/standards_datastandardortool_schema.yaml)).

A list of all IDs and names of entities in the Registry [may be found here](https://github.com/bridge2ai/b2ai-standards-registry/blob/main/src/all_ids.tsv).

Some tasks refer to the dataset documentation for the Grand Challenges (GCs).

Table 1 contains the names of each GC, its identifier, and links to each its dataset documentation.

| Full Name | Short Name | ID | Data Documentation |
|-----------|------------|----|--------------------|
|AI/ML for Clinical Care|CHoRUS|B2AI_ORG:115|[CHoRUS for Equitable AI](https://github.com/chorus-ai#table-of-contents)|
|Functional Genomics|CM4AI|B2AI_ORG:116|[CM4AI Product Documentation](https://cm4ai.org/product-documentation/)|
|Precision Public Health|Voice|B2AI_ORG:117|[Flagship Dataset of Voice as a Biomarker of Health](https://docs.b2ai-voice.org/)|
|Salutogenesis|AI-READI|B2AI_ORG:114|[Flagship Dataset of Type 2 Diabetes from the AI-READI Project](https://fairhub.io/datasets/2)|

**Table 1. Bridge2AI Grand Challenges**

You can help with the following tasks:

## Add New Entities

To add a new entity (e.g., a standard, tool, or organization) to the Registry, use [this GitHub form](https://github.com/bridge2ai/b2ai-standards-registry/issues/new?template=newEntity.yml) to create a new issue.

This is particularly useful to do for resources used by GCs but not yet represented in the registry. To curate these entities:

1. Visit one of the data documentation pages linked in the table above.

2. When a relevant entity is mentioned, check if it exists in the registry already. The easiest way to do so (for now) is to search the [list of all identifiers](https://github.com/bridge2ai/b2ai-standards-registry/blob/main/src/all_ids.tsv).

3. If it exists, that's great! If not, create a new issue to add it. The issue form will ask if this entity is related to another. Please put the ID of the corresponding GC (see Table 1 above) in this field.

## Connect Standards and Tools to Organizations

A connection between an standard/tool and an organization (e.g., Precision Public Health [B2AI_ORG:117](Organization.markdown) uses the Praat software [B2AI_STANDARD:886](DataStandardOrTool.markdown)) can be defined within the DataStandardOrTool table.

1. Identify a connection between an entity and an organization. A common and informative type is a standard or tool used by one of the Bridge2AI GCs, so consult their data documentation.

2. Edit the DataStandardOrTool.yaml file, preferably in your own Git branch. Find the entry for the standard or tool and add the ID for the organization to the `has_relevant_organization` field. Create the field if it does not yet exist for this entry. This field expects a list, so it should look like this:

    has_relevant_organization:

      - B2AI_ORG:117

3. Save your changes. Open a PR to add them to the repository.

## Connect Standards and Tools to SDOs

Standards and tools often are maintained, managed, promoted, and otherwise supported by a dedicated organization. These are often referred to as Standards Development Organizations, or SDOs. Some, such as the International Organization for Standardization (ISO, [B2AI_ORG:49](Organization.markdown)) are responsible for many standards across various domains. Others, such as Health Level Seven (HL7, [B2AI_ORG:40](Organization.markdown)) are focused on biomedical and healthcare-related standards, such as Fast Healthcare Interoperability Resources (FHIR, [B2AI_STANDARD:109](DataStandardOrTool.markdown)).

1. Identify a connection between an entity and an SDO. An entry for the Organization may already exist. Standards in the category `BiomedicalStandard` will be most relevant here. If the SDO for a standard is not already known, it can usually be found in its online documentation. Note that multiple SDOs may be responsible for the same standard. 

2. Edit the DataStandardOrTool.yaml file, preferably in your own Git branch. Find the entry for the standard or tool and add the ID for the organization to the `responsible_organization` field. Create the field if it does not yet exist for this entry. This field expects a list, so it should look like this:

    responsible_organization:

      - B2AI_ORG:40

3. If necessary, add the corresponding Organization(s) to a new entry in the Organization.yaml file. Include a URL for each organization, and if possible, a Research Organization Registry (ROR) ID and/or Wikidata ID in `ror_id` and `wikidata_id`, respectively. ROR IDs may be found by searching <https://ror.org>. Wikidata IDs may be found by searching <https://www.wikidata.org/>, but please provide the ID for the organization itself rather than a related page ([for example, Health Level Seven International](https://www.wikidata.org/wiki/Q17054989) instead of [Health Level 7](https://www.wikidata.org/wiki/Q327718), since the latter is a page for the standards themselves).

4. Save your changes. Open a PR to add them to the repository.

## Connect Standards and Tools to other Standards and Tools

A connection between an standard/tool and another standard or tool (e.g., the Parselmouth software [B2AI_STANDARD:887](DataStandardOrTool.markdown) is an interface for the Praat software [B2AI_STANDARD:886](DataStandardOrTool.markdown)) can be defined within the DataStandardOrTool table.

1. Identify a connection between a standard/tool and another. This does not include relationships in which one standard or tool is purely a part of another or one of several iterative versions, but two entities may be related in a variety of other ways.

2. Edit the DataStandardOrTool.yaml file, preferably in your own Git branch. Find the entry for the standard or tool and add the ID for the related standard or tool to the `related_to` field. Create the field if it does not yet exist for this entry. This field expects a list, so it should look like this:

    related_to:

      - B2AI_STANDARD:887

3. Save your changes. Open a PR to add them to the repository.
