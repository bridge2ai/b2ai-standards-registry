"""A python script for creating/updating B2AI standards explorer table schemas in synapse
This script should be updated and rerun when the schema of the tables must be updated"""

import os
from synapseclient import Synapse, Table, Column, Schema
from enum import Enum


# Possible column names for the tables
class ColumnName(Enum):
    ID = "id"
    CATEGORY = "category"
    NAME = "name"
    DESCRIPTION = "description"
    CONTRIBUTOR_NAME = "contributor_name"
    CONTRIBUTOR_GITHUB_NAME = "contributor_github_name"
    CONTRIBUTOR_ORCID = "contributor_orcid"
    COLLECTION = "collection"
    CONCERNS_DATA_TOPIC = "concerns_data_topic"
    PURPOSE_DETAIL = "purpose_detail"
    SUBCLASS_OF = "subclass_of"
    URL = "url"
    IS_OPEN = "is_open"
    REQUIRES_REGISTRATION = "requires_registration"
    EDAM_ID = "edam_id"
    MESH_ID = "mesh_id"
    NCIT_ID = "ncit_id"
    RELATED_TO = "related_to"
    METADATA_STORAGE = "metadata_storage"
    FILE_EXTENSIONS = "file_extensions"
    LIMITATIONS = "limitations"
    CONTRIBUTION_DATE = "contribution_date"
    PUBLICATION = "publication"
    FORMAL_SPECIFICATION = "formal_specification"
    HAS_RELEVANT_ORGANIZATION = "has_relevant_organization"
    USE_CASE_CATEGORY = "use_case_category"
    RELEVANT_TO_DGPS = "relevant_to_dgps"
    DATA_TOPICS = "data_topics"
    STANDARDS_AND_TOOLS_FOR_DGP_USE = "standards_and_tools_for_dgp_use"
    ENABLES = "enables"
    INVOLVED_IN_EXPERIMENTAL_DESIGN = "involved_in_experimental_design"
    INVOLVED_IN_METADATA_MANAGEMENT = "involved_in_metadata_management"
    INVOLVED_IN_QUALITY_CONTROL = "involved_in_quality_control"
    XREF = "xref"
    ALTERNATIVE_STANDARDS_AND_TOOLS = "alternative_standards_and_tools"
    ROR_ID = "ror_id"
    WIKIDATA_ID = "wikidata_id"


# Possible columns in the standards data tables
COLUMN_TEMPLATES = {
    ColumnName.ID: Column(name=ColumnName.ID.value, columnType="STRING", maximumSize=100),
    ColumnName.CATEGORY: Column(name=ColumnName.CATEGORY.value, columnType="STRING", maximumSize=100),
    ColumnName.NAME: Column(name=ColumnName.NAME.value, columnType="MEDIUMTEXT"),
    ColumnName.DESCRIPTION: Column(name=ColumnName.DESCRIPTION.value, columnType="MEDIUMTEXT"),
    ColumnName.CONTRIBUTOR_NAME: Column(name=ColumnName.CONTRIBUTOR_NAME.value, columnType="STRING", maximumSize=100),
    ColumnName.CONTRIBUTOR_GITHUB_NAME: Column(name=ColumnName.CONTRIBUTOR_GITHUB_NAME.value, columnType="STRING",
                                               maximumSize=40),
    ColumnName.CONTRIBUTOR_ORCID: Column(name=ColumnName.CONTRIBUTOR_ORCID.value, columnType="STRING", maximumSize=50),
    ColumnName.COLLECTION: Column(name='collection', columnType="STRING", maximumSize=100),
    ColumnName.PURPOSE_DETAIL: Column(name='purpose_detail', columnType="MEDIUMTEXT"),
    ColumnName.CONCERNS_DATA_TOPIC: Column(name='concerns_data_topic', columnType="STRING", maximumSize=255),
    ColumnName.SUBCLASS_OF: Column(name=ColumnName.SUBCLASS_OF.value, columnType="STRING", maximumSize=100),
    ColumnName.URL: Column(name=ColumnName.URL.value, columnType="MEDIUMTEXT"),
    ColumnName.IS_OPEN: Column(name=ColumnName.IS_OPEN.value, columnType="BOOLEAN"),
    ColumnName.REQUIRES_REGISTRATION: Column(name=ColumnName.REQUIRES_REGISTRATION.value, columnType="BOOLEAN"),
    ColumnName.EDAM_ID: Column(name=ColumnName.EDAM_ID.value, columnType="STRING", maximumSize=25),
    ColumnName.MESH_ID: Column(name=ColumnName.MESH_ID.value, columnType="STRING", maximumSize=25),
    ColumnName.NCIT_ID: Column(name=ColumnName.NCIT_ID.value, columnType="STRING", maximumSize=25),
    ColumnName.RELATED_TO: Column(name=ColumnName.RELATED_TO.value, columnType="STRING", maximumSize=255),
    ColumnName.METADATA_STORAGE: Column(name=ColumnName.METADATA_STORAGE.value, columnType="STRING", maximumSize=255),
    ColumnName.FILE_EXTENSIONS: Column(name=ColumnName.FILE_EXTENSIONS.value, columnType="STRING", maximumSize=255),
    ColumnName.LIMITATIONS: Column(name=ColumnName.LIMITATIONS.value, columnType="MEDIUMTEXT"),
    ColumnName.CONTRIBUTION_DATE: Column(name=ColumnName.CONTRIBUTION_DATE.value, columnType="STRING", maximumSize=50),
    ColumnName.PUBLICATION: Column(name=ColumnName.PUBLICATION.value, columnType="STRING", maximumSize=100),
    ColumnName.FORMAL_SPECIFICATION: Column(name=ColumnName.FORMAL_SPECIFICATION.value, columnType="MEDIUMTEXT"),
    ColumnName.HAS_RELEVANT_ORGANIZATION: Column(name=ColumnName.HAS_RELEVANT_ORGANIZATION.value, columnType="STRING",
                                                 maximumSize=100),
    ColumnName.USE_CASE_CATEGORY: Column(name=ColumnName.USE_CASE_CATEGORY.value, columnType="STRING", maximumSize=100),
    ColumnName.RELEVANT_TO_DGPS: Column(name=ColumnName.RELEVANT_TO_DGPS.value, columnType="STRING", maximumSize=255),
    ColumnName.DATA_TOPICS: Column(name=ColumnName.DATA_TOPICS.value, columnType="STRING", maximumSize=255),
    ColumnName.STANDARDS_AND_TOOLS_FOR_DGP_USE: Column(name=ColumnName.STANDARDS_AND_TOOLS_FOR_DGP_USE.value,
                                                       columnType="STRING", maximumSize=255),
    ColumnName.ENABLES: Column(name=ColumnName.ENABLES.value, columnType="STRING", maximumSize=255),
    ColumnName.INVOLVED_IN_EXPERIMENTAL_DESIGN: Column(name=ColumnName.INVOLVED_IN_EXPERIMENTAL_DESIGN.value,
                                                       columnType="BOOLEAN"),
    ColumnName.INVOLVED_IN_METADATA_MANAGEMENT: Column(name=ColumnName.INVOLVED_IN_METADATA_MANAGEMENT.value,
                                                       columnType="BOOLEAN"),
    ColumnName.INVOLVED_IN_QUALITY_CONTROL: Column(name=ColumnName.INVOLVED_IN_QUALITY_CONTROL.value,
                                                   columnType="BOOLEAN"),
    ColumnName.XREF: Column(name=ColumnName.XREF.value, columnType="STRING", maximumSize=255),
    ColumnName.ALTERNATIVE_STANDARDS_AND_TOOLS: Column(name=ColumnName.ALTERNATIVE_STANDARDS_AND_TOOLS.value,
                                                       columnType="STRING", maximumSize=255),
    ColumnName.ROR_ID: Column(name=ColumnName.ROR_ID.value, columnType="STRING", maximumSize=35),
    ColumnName.WIKIDATA_ID: Column(name=ColumnName.WIKIDATA_ID.value, columnType="STRING", maximumSize=25),
}


class TableSchema(Enum):
    """An enum for the data tables, containing their ids in the synapse project and their schemas"""
    DataStandardOrTool = {
        "id": "syn63096833",
        "columns": [
            ColumnName.ID, ColumnName.CATEGORY, ColumnName.NAME, ColumnName.DESCRIPTION, ColumnName.CONTRIBUTOR_NAME,
            ColumnName.CONTRIBUTOR_GITHUB_NAME, ColumnName.CONTRIBUTOR_ORCID, ColumnName.COLLECTION,
            ColumnName.CONCERNS_DATA_TOPIC, ColumnName.PURPOSE_DETAIL, ColumnName.IS_OPEN,
            ColumnName.REQUIRES_REGISTRATION, ColumnName.URL, ColumnName.FORMAL_SPECIFICATION,
            ColumnName.HAS_RELEVANT_ORGANIZATION, ColumnName.PUBLICATION, ColumnName.SUBCLASS_OF,
            ColumnName.CONTRIBUTION_DATE
        ]
    }
    DataSubstrate = {
        "id": "syn63096834",
        "columns": [
            ColumnName.ID, ColumnName.CATEGORY, ColumnName.NAME, ColumnName.DESCRIPTION, ColumnName.SUBCLASS_OF,
            ColumnName.CONTRIBUTOR_NAME, ColumnName.CONTRIBUTOR_GITHUB_NAME, ColumnName.CONTRIBUTOR_ORCID,
            ColumnName.EDAM_ID, ColumnName.NCIT_ID, ColumnName.RELATED_TO, ColumnName.METADATA_STORAGE,
            ColumnName.FILE_EXTENSIONS, ColumnName.LIMITATIONS, ColumnName.MESH_ID, ColumnName.CONTRIBUTION_DATE
        ]
    }
    DataTopic = {
        "id": "syn63096835",
        "columns": [
            ColumnName.ID, ColumnName.CATEGORY, ColumnName.NAME, ColumnName.DESCRIPTION, ColumnName.SUBCLASS_OF,
            ColumnName.CONTRIBUTOR_NAME, ColumnName.CONTRIBUTOR_GITHUB_NAME, ColumnName.CONTRIBUTOR_ORCID,
            ColumnName.EDAM_ID, ColumnName.MESH_ID, ColumnName.NCIT_ID, ColumnName.RELATED_TO
        ]
    }
    Organization = {
        "id": "syn63096836",
        "columns": [
            ColumnName.ID, ColumnName.CATEGORY, ColumnName.NAME, ColumnName.DESCRIPTION, ColumnName.CONTRIBUTOR_NAME,
            ColumnName.CONTRIBUTOR_GITHUB_NAME, ColumnName.CONTRIBUTOR_ORCID, ColumnName.ROR_ID,
            ColumnName.WIKIDATA_ID, ColumnName.URL, ColumnName.SUBCLASS_OF
        ]
    }
    UseCase = {
        "id": "syn63096837",
        "columns": [
            ColumnName.ID, ColumnName.CATEGORY, ColumnName.NAME, ColumnName.DESCRIPTION, ColumnName.CONTRIBUTOR_NAME,
            ColumnName.CONTRIBUTOR_GITHUB_NAME, ColumnName.CONTRIBUTOR_ORCID, ColumnName.USE_CASE_CATEGORY,
            ColumnName.RELEVANT_TO_DGPS, ColumnName.DATA_TOPICS, ColumnName.STANDARDS_AND_TOOLS_FOR_DGP_USE,
            ColumnName.ENABLES, ColumnName.INVOLVED_IN_EXPERIMENTAL_DESIGN, ColumnName.INVOLVED_IN_METADATA_MANAGEMENT,
            ColumnName.INVOLVED_IN_QUALITY_CONTROL, ColumnName.XREF, ColumnName.LIMITATIONS,
            ColumnName.ALTERNATIVE_STANDARDS_AND_TOOLS
        ]
    }


def main():
    auth_token = os.getenv("SYNAPSE_AUTH_TOKEN")
    if not auth_token:
        raise ValueError("SYNAPSE_AUTH_TOKEN environment variable is not set")
    syn = Synapse()
    syn.login(
        authToken=auth_token)

    project = syn.get("syn63096806")

    for table_schema in TableSchema:
        table_id = table_schema.value["id"]

        # take snapshot of tables before updating them
        syn.create_snapshot_version(table_id)

        column_keys = table_schema.value["columns"]
        columns = [COLUMN_TEMPLATES[key] for key in column_keys]

        schema = Schema(name=table_schema.name, columns=columns, parent=project)
        table = Table(schema, values=[])
        syn.store(table)


if __name__ == "__main__":
    main()
