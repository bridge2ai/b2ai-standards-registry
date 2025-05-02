"""A python script for creating/updating B2AI standards explorer table schemas in synapse
This script should be updated and rerun when the schema of the tables must be updated"""

from synapseclient import Synapse, Table, Column, Schema
from enum import Enum

from scripts.utils import get_auth_token


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
    KNOWN_LIMITATIONS = "known_limitations"
    CONTRIBUTION_DATE = "contribution_date"
    PUBLICATION = "publication"
    FORMAL_SPECIFICATION = "formal_specification"
    HAS_RELEVANT_ORGANIZATION = "has_relevant_organization"
    HAS_TRAINING_RESOURCE = "has_training_resource"
    USE_CASE_CATEGORY = "use_case_category"
    RELEVANCE_TO_DGPS = "relevance_to_dgps"
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
    RESPONSIBLE_ORGANIZATION = "responsible_organization"
    DOCUMENTATION_URL = "documentation_url"
    DATA_URL = "data_url"
    DATASHEET_URL = "datasheet_url"
    HAS_FILES = "has_files"
    IS_PUBLIC = "is_public"
    PRODUCED_BY = "produced_by"
    SUBSTRATES = "substrates"
    TOPICS = "topics"


# Possible columns in the standards data tables
COLUMN_TEMPLATES = {
    ColumnName.ID: Column(
        name=ColumnName.ID.value, columnType="STRING", maximumSize=100
    ),
    ColumnName.CATEGORY: Column(
        name=ColumnName.CATEGORY.value, columnType="STRING", maximumSize=100
    ),
    ColumnName.NAME: Column(name=ColumnName.NAME.value, columnType="MEDIUMTEXT"),
    ColumnName.DESCRIPTION: Column(
        name=ColumnName.DESCRIPTION.value, columnType="MEDIUMTEXT"
    ),
    ColumnName.CONTRIBUTOR_NAME: Column(
        name=ColumnName.CONTRIBUTOR_NAME.value, columnType="STRING", maximumSize=100
    ),
    ColumnName.CONTRIBUTOR_GITHUB_NAME: Column(
        name=ColumnName.CONTRIBUTOR_GITHUB_NAME.value,
        columnType="STRING",
        maximumSize=40,
    ),
    ColumnName.CONTRIBUTOR_ORCID: Column(
        name=ColumnName.CONTRIBUTOR_ORCID.value, columnType="STRING", maximumSize=50
    ),
    ColumnName.COLLECTION: Column(
        name="collection", columnType="STRING_LIST", maximumListLength=25
    ),
    ColumnName.PURPOSE_DETAIL: Column(name="purpose_detail", columnType="MEDIUMTEXT"),
    ColumnName.CONCERNS_DATA_TOPIC: Column(
        name="concerns_data_topic", columnType="STRING_LIST", maximumListLength=25
    ),
    ColumnName.SUBCLASS_OF: Column(
        name=ColumnName.SUBCLASS_OF.value,
        columnType="STRING_LIST",
        maximumListLength=25,
    ),
    ColumnName.URL: Column(name=ColumnName.URL.value, columnType="MEDIUMTEXT"),
    ColumnName.IS_OPEN: Column(name=ColumnName.IS_OPEN.value, columnType="BOOLEAN"),
    ColumnName.REQUIRES_REGISTRATION: Column(
        name=ColumnName.REQUIRES_REGISTRATION.value, columnType="BOOLEAN"
    ),
    ColumnName.EDAM_ID: Column(
        name=ColumnName.EDAM_ID.value, columnType="STRING", maximumSize=25
    ),
    ColumnName.MESH_ID: Column(
        name=ColumnName.MESH_ID.value, columnType="STRING", maximumSize=25
    ),
    ColumnName.NCIT_ID: Column(
        name=ColumnName.NCIT_ID.value, columnType="STRING", maximumSize=25
    ),
    ColumnName.RELATED_TO: Column(
        name=ColumnName.RELATED_TO.value, columnType="STRING_LIST", maximumListLength=25
    ),
    ColumnName.METADATA_STORAGE: Column(
        name=ColumnName.METADATA_STORAGE.value,
        columnType="STRING_LIST",
        maximumListLength=25,
    ),
    ColumnName.FILE_EXTENSIONS: Column(
        name=ColumnName.FILE_EXTENSIONS.value,
        columnType="STRING_LIST",
        maximumListLength=25,
    ),
    ColumnName.LIMITATIONS: Column(
        name=ColumnName.LIMITATIONS.value, columnType="MEDIUMTEXT"
    ),
    ColumnName.KNOWN_LIMITATIONS: Column(
        name=ColumnName.KNOWN_LIMITATIONS.value, columnType="MEDIUMTEXT"
    ),
    ColumnName.CONTRIBUTION_DATE: Column(
        name=ColumnName.CONTRIBUTION_DATE.value, columnType="STRING", maximumSize=50
    ),
    ColumnName.PUBLICATION: Column(
        name=ColumnName.PUBLICATION.value, columnType="STRING", maximumSize=100
    ),
    ColumnName.FORMAL_SPECIFICATION: Column(
        name=ColumnName.FORMAL_SPECIFICATION.value, columnType="MEDIUMTEXT"
    ),
    ColumnName.HAS_RELEVANT_ORGANIZATION: Column(
        name=ColumnName.HAS_RELEVANT_ORGANIZATION.value,
        columnType="STRING_LIST",
        maximumListLength=25,
    ),
    ColumnName.HAS_TRAINING_RESOURCE: Column(
        name=ColumnName.HAS_TRAINING_RESOURCE.value,
        columnType="STRING_LIST",
        maximumListLength=25,
    ),
    ColumnName.USE_CASE_CATEGORY: Column(
        name=ColumnName.USE_CASE_CATEGORY.value, columnType="STRING", maximumSize=100
    ),
    ColumnName.RELEVANCE_TO_DGPS: Column(
        name=ColumnName.RELEVANCE_TO_DGPS.value,
        columnType="STRING_LIST",
        maximumListLength=25,
    ),
    ColumnName.DATA_TOPICS: Column(
        name=ColumnName.DATA_TOPICS.value,
        columnType="STRING_LIST",
        maximumListLength=25,
    ),
    ColumnName.STANDARDS_AND_TOOLS_FOR_DGP_USE: Column(
        name=ColumnName.STANDARDS_AND_TOOLS_FOR_DGP_USE.value,
        columnType="STRING_LIST",
        maximumListLength=25,
    ),
    ColumnName.ENABLES: Column(
        name=ColumnName.ENABLES.value, columnType="STRING_LIST", maximumListLength=25
    ),
    ColumnName.INVOLVED_IN_EXPERIMENTAL_DESIGN: Column(
        name=ColumnName.INVOLVED_IN_EXPERIMENTAL_DESIGN.value, columnType="BOOLEAN"
    ),
    ColumnName.INVOLVED_IN_METADATA_MANAGEMENT: Column(
        name=ColumnName.INVOLVED_IN_METADATA_MANAGEMENT.value, columnType="BOOLEAN"
    ),
    ColumnName.INVOLVED_IN_QUALITY_CONTROL: Column(
        name=ColumnName.INVOLVED_IN_QUALITY_CONTROL.value, columnType="BOOLEAN"
    ),
    ColumnName.XREF: Column(
        name=ColumnName.XREF.value, columnType="STRING_LIST", maximumListLength=25
    ),
    ColumnName.ALTERNATIVE_STANDARDS_AND_TOOLS: Column(
        name=ColumnName.ALTERNATIVE_STANDARDS_AND_TOOLS.value,
        columnType="STRING_LIST",
        maximumListLength=25,
    ),
    ColumnName.ROR_ID: Column(
        name=ColumnName.ROR_ID.value, columnType="STRING", maximumSize=35
    ),
    ColumnName.WIKIDATA_ID: Column(
        name=ColumnName.WIKIDATA_ID.value, columnType="STRING", maximumSize=25
    ),
    ColumnName.RESPONSIBLE_ORGANIZATION: Column(
        name=ColumnName.RESPONSIBLE_ORGANIZATION.value, columnType="STRING_LIST", maximumListLength=25
    ),
    ColumnName.DATA_URL: Column(name=ColumnName.DATA_URL.value, columnType="MEDIUMTEXT"),
    ColumnName.DATASHEET_URL: Column(name=ColumnName.DATASHEET_URL.value, columnType="MEDIUMTEXT"),
    ColumnName.DOCUMENTATION_URL: Column(name=ColumnName.DOCUMENTATION_URL.value, columnType="MEDIUMTEXT"),
    ColumnName.HAS_FILES: Column(
        name=ColumnName.HAS_FILES.value, columnType="STRING_LIST", maximumListLength=25, maximumSize=100
    ),
    ColumnName.IS_PUBLIC: Column(
        name=ColumnName.IS_PUBLIC.value, columnType="BOOLEAN"
    ),
    ColumnName.PRODUCED_BY: Column(
        name=ColumnName.PRODUCED_BY.value, columnType="STRING_LIST", maximumListLength=25
    ),
    ColumnName.SUBSTRATES: Column(
        name=ColumnName.SUBSTRATES.value, columnType="STRING_LIST", maximumListLength=25
    ),
    ColumnName.TOPICS: Column(
        name="topics", columnType="STRING_LIST", maximumListLength=25
    )
}

class TableSchema(Enum):
    """An enum for the data tables, containing their ids in the synapse project and their schemas"""

    DataSet = {
        "id": "syn66330217",
        "columns": [
            ColumnName.ID,
            ColumnName.CATEGORY,
            ColumnName.DATA_URL,
            ColumnName.DATASHEET_URL,
            ColumnName.DESCRIPTION,
            ColumnName.DOCUMENTATION_URL,
            ColumnName.HAS_FILES,
            ColumnName.IS_PUBLIC,
            ColumnName.NAME,
            ColumnName.PRODUCED_BY,
            ColumnName.SUBSTRATES,
            ColumnName.TOPICS,
        ],
    }
    DataStandardOrTool = {
        "id": "syn63096833",
        "columns": [
            ColumnName.ID,
            ColumnName.CATEGORY,
            ColumnName.NAME,
            ColumnName.DESCRIPTION,
            ColumnName.CONTRIBUTOR_NAME,
            ColumnName.CONTRIBUTOR_GITHUB_NAME,
            ColumnName.CONTRIBUTOR_ORCID,
            ColumnName.COLLECTION,
            ColumnName.CONCERNS_DATA_TOPIC,
            ColumnName.PURPOSE_DETAIL,
            ColumnName.IS_OPEN,
            ColumnName.REQUIRES_REGISTRATION,
            ColumnName.URL,
            ColumnName.FORMAL_SPECIFICATION,
            ColumnName.HAS_RELEVANT_ORGANIZATION,
            ColumnName.PUBLICATION,
            ColumnName.HAS_TRAINING_RESOURCE,
            ColumnName.SUBCLASS_OF,
            ColumnName.CONTRIBUTION_DATE,
            ColumnName.RELATED_TO,
            ColumnName.RESPONSIBLE_ORGANIZATION,
        ],
    }
    DataSubstrate = {
        "id": "syn63096834",
        "columns": [
            ColumnName.ID,
            ColumnName.CATEGORY,
            ColumnName.NAME,
            ColumnName.DESCRIPTION,
            ColumnName.SUBCLASS_OF,
            ColumnName.RELATED_TO,
            ColumnName.CONTRIBUTOR_NAME,
            ColumnName.CONTRIBUTOR_GITHUB_NAME,
            ColumnName.CONTRIBUTOR_ORCID,
            ColumnName.EDAM_ID,
            ColumnName.NCIT_ID,
            ColumnName.METADATA_STORAGE,
            ColumnName.FILE_EXTENSIONS,
            ColumnName.LIMITATIONS,
            ColumnName.MESH_ID,
            ColumnName.CONTRIBUTION_DATE,
        ],
    }
    DataTopic = {
        "id": "syn63096835",
        "columns": [
            ColumnName.ID,
            ColumnName.CATEGORY,
            ColumnName.NAME,
            ColumnName.DESCRIPTION,
            ColumnName.SUBCLASS_OF,
            ColumnName.CONTRIBUTOR_NAME,
            ColumnName.CONTRIBUTOR_GITHUB_NAME,
            ColumnName.CONTRIBUTOR_ORCID,
            ColumnName.EDAM_ID,
            ColumnName.MESH_ID,
            ColumnName.NCIT_ID,
            ColumnName.RELATED_TO,
        ],
    }
    Organization = {
        "id": "syn63096836",
        "columns": [
            ColumnName.ID,
            ColumnName.CATEGORY,
            ColumnName.NAME,
            ColumnName.DESCRIPTION,
            ColumnName.CONTRIBUTOR_NAME,
            ColumnName.CONTRIBUTOR_GITHUB_NAME,
            ColumnName.CONTRIBUTOR_ORCID,
            ColumnName.ROR_ID,
            ColumnName.WIKIDATA_ID,
            ColumnName.URL,
            ColumnName.SUBCLASS_OF,
        ],
    }
    UseCase = {
        "id": "syn63096837",
        "columns": [
            ColumnName.ID,
            ColumnName.CATEGORY,
            ColumnName.NAME,
            ColumnName.DESCRIPTION,
            ColumnName.CONTRIBUTOR_NAME,
            ColumnName.CONTRIBUTOR_GITHUB_NAME,
            ColumnName.CONTRIBUTOR_ORCID,
            ColumnName.USE_CASE_CATEGORY,
            ColumnName.RELEVANCE_TO_DGPS,
            ColumnName.DATA_TOPICS,
            ColumnName.STANDARDS_AND_TOOLS_FOR_DGP_USE,
            ColumnName.ENABLES,
            ColumnName.INVOLVED_IN_EXPERIMENTAL_DESIGN,
            ColumnName.INVOLVED_IN_METADATA_MANAGEMENT,
            ColumnName.INVOLVED_IN_QUALITY_CONTROL,
            ColumnName.XREF,
            ColumnName.KNOWN_LIMITATIONS,
            ColumnName.ALTERNATIVE_STANDARDS_AND_TOOLS,
        ],
    }


def main():
    auth_token = get_auth_token()

    syn = Synapse()
    syn.login(authToken=auth_token)

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
