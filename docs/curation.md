# Curation Guide

The tasks listed below all help to make the Bridge2AI Standards Registry more complete and informative.

The "source of truth" data for the Registry is all located in the `b2ai-standards-registry` repository within the directory `src/data/`.

Each YAML document in this directory is a single data table named for its contents (e.g., every item in `DataStandardOrTool.yaml` is an object of the `DataStandardOrTool` class in the [corresponding schema](https://github.com/bridge2ai/b2ai-standards-registry/blob/main/src/schema/standards_datastandardortool_schema.yaml)).

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
2. When a relevant entity is mentioned, check if it exists in the registry already. The easiest way to do so (for now) is to use the search bar at the top of [these data docs](https://bridge2ai.github.io/b2ai-standards-registry/). This will tell you if a term or name is used anywhere in a table, but you will need to search in the table to find the specific entry.
3. If it exists, that's great! If not, create a new issue to add it. The issue form will ask if this entity is related to another. Please put the ID of the corresponding GC (see Table 1 above) in this field.

## Connect Standards and Tools to Organizations

A connection between an standard/tool and an organization (e.g., Precision Public Health [B2AI_ORG:117] uses the Praat software [B2AI_STANDARD:886]) can be defined within the DataStandardOrTool table.

1. Identify a connection between an entity and an organization. A common and informative type is a standard or tool used by one of the Bridge2AI GCs, so consult their data documentation.
2. Edit the DataStandardOrTool.yaml file, preferably in your own Git branch. Find the entry for the standard or tool and add the ID for the organization to the `has_relevant_organization` field. Create the field if it does not yet exist for this entry. This field expects a list, so it should look like this:
    ```yaml
    has_relevant_organization:
      - B2AI_ORG:117
    ```
3. Save your changes. Open a PR to add them to the repository.

## Connect Standards and Tools to other Standards and Tools

A connection between an standard/tool and another standard or tool (e.g., the Parselmouth software [B2AI_STANDARD:887] is an interface for the Praat software [B2AI_STANDARD:886]) can be defined within the DataStandardOrTool table.

1. Identify a connection between a standard/tool and another. This does not include relationships in which one standard or tool is purely a part of another or one of several iterative versions, but two entities may be related in a variety of other ways.
2. Edit the DataStandardOrTool.yaml file, preferably in your own Git branch. Find the entry for the standard or tool and add the ID for the related standard or tool to the `related_to` field. Create the field if it does not yet exist for this entry. This field expects a list, so it should look like this:
    ```yaml
    related_to:
      - B2AI_STANDARD:887
    ```
3. Save your changes. Open a PR to add them to the repository.