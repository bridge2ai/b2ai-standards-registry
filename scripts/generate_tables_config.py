# This configuration file is used to define the setup for the Synapse tables
# and their relationships. It includes the source table names, destination table configurations,
# and the Synapse table IDs, as well as how the tables will be rendered
# in the Explorer (e.g., whether columns are faceted or not and how their
# titles will be displayed).

SRC_TABLE_NAMES = [
    'Challenges',
    'DataSet',
    'DataStandardOrTool',
    'DataSubstrate',
    'DataTopic',
    'Organization',
    'UseCase',
    # 'test',
]
TABLE_IDS = {
    'Challenges': { 'name': 'Challenges', 'id': 'syn65913973' },
    'CurrentTableVersions': { 'name': 'CurrentTableVersions', 'id': 'syn66330007' },
    'DST_denormalized': { 'name': 'DST_denormalized', 'id': 'syn65676531' },
    'DataSet': { 'name': 'DataSet', 'id': 'syn66330217' },
    'DataSet_denormalized': { 'name': 'DataSet_denormalized', 'id': 'syn68258237' },
    'DataStandardOrTool': { 'name': 'DataStandardOrTool', 'id': 'syn63096833' },
    'DataSubstrate': { 'name': 'DataSubstrate', 'id': 'syn63096834' },
    'DataTopic': { 'name': 'DataTopic', 'id': 'syn63096835' },
    'Organization': { 'name': 'Organization', 'id': 'syn63096836' },
    'UseCase': { 'name': 'UseCase', 'id': 'syn63096837' },
    # 'test': { 'name': 'test', 'id': 'syn64943432' }
}

# see top of create_denormalized_tables:make_dest_table() for how to define destination tables
DEST_TABLES = {
    # The table used for the explore landing page and to provide data for the home and detailed pages
    'DST_denormalized': {
        'dest_table_name': 'DST_denormalized',
        'base_table': 'DataStandardOrTool',
        'columns': [
            {'faceted': False, 'name': 'id',                          'alias': 'id'},
            {'faceted': False, 'name': 'name',                        'alias': 'acronym'},
            {'faceted': False, 'name': 'description',                 'alias': 'name'},
            {'faceted': True,  'name': 'category',                    'alias': 'category', 'transform': 'category_to_title_case'},
            {'faceted': False, 'name': 'purpose_detail',              'alias': 'description'},
            {'faceted': True,  'name': 'collection',                  'alias': 'collections', 'transform': 'collections_to_title_case'},
            {'faceted': True,  'name': 'collection',                  'alias': 'hasAIApplication', 'transform': 'collections_to_has_ai_app', 'columnType': 'STRING'},
            {'faceted': True,  'name': 'collection',                  'alias': 'mature', 'transform': 'collections_to_is_mature', 'columnType': 'STRING'},
            {'faceted': False, 'name': 'concerns_data_topic',         'alias': 'concerns_data_topic'},
            {'faceted': False, 'name': 'has_relevant_data_substrate', 'alias': 'has_relevant_data_substrate'},
            {'faceted': False, 'name': 'has_relevant_organization',   'alias': 'has_relevant_organization'},
            {'faceted': False, 'name': 'responsible_organization',    'alias': 'responsible_organization'},
            {'faceted': True,  'name': 'is_open',                     'alias': 'isOpen', 'transform': 'bool_to_yes_no', 'columnType': 'STRING'},
            {'faceted': True,  'name': 'requires_registration',       'alias': 'registration', 'transform': 'bool_to_yes_no', 'columnType': 'STRING'},
            {'faceted': False, 'name': 'url',                         'alias': 'URL'},
            {'faceted': False, 'name': 'formal_specification',        'alias': 'formalSpec'},
            {'faceted': False, 'name': 'publication',                 'alias': 'publication'},
            {'faceted': False, 'name': 'has_training_resource',       'alias': 'trainingResources'},
            {'faceted': False, 'name': 'subclass_of',                 'alias': 'subclassOf'},
            {'faceted': False, 'name': 'contribution_date',           'alias': 'contributionDate'},
            {'faceted': False, 'name': 'related_to',                  'alias': 'relatedTo'},
            {'faceted': True,  'name': 'used_in_bridge2ai',           'alias': 'usedInBridge2AI', 'transform': 'bool_to_yes_no', 'columnType': 'STRING'},
        ],
        'join_columns': [
            {'join_tbl': 'DataTopic', 'from': 'concerns_data_topic', 'to': 'id',
             'dest_cols': [
                 {'faceted': True, 'name': 'name', 'alias': 'topic'},
             ]},
            {'join_tbl': 'DataSubstrate', 'from': 'has_relevant_data_substrate', 'to': 'id',
             'dest_cols': [
                {'faceted': True, 'name': 'name', 'alias': 'dataTypes'},
            ]},
            {'join_tbl': 'Organization', 'from': 'has_relevant_organization', 'to': 'id',
             'dest_cols': [
                 {'faceted': True,  'name': 'name', 'alias': 'relevantOrgNames'},
                 {'faceted': False, 'source_cols': ['id', 'name'], 'alias': 'relevantOrgLinks', 'transform': 'create_org_link', },
             ]},
            {'join_tbl': 'Organization', 'from': 'responsible_organization', 'to': 'id',
             'dest_cols': [
                 {'faceted': False,  'name': 'description', 'alias': 'responsibleOrgName'},
                 {'faceted': False, 'source_cols': ['id', 'name'], 'alias': 'responsibleOrgLinks',
                  'transform': 'create_org_link', },
             ]},
        ],
    },
    'DataSet_denormalized': {
        # This is for the GrandChallengeDataSetPage, https://github.com/bridge2ai/b2ai-standards-registry/issues/244
        #   Needs to provide data to render this design:
        #   https://www.figma.com/design/3I2TuS7qjLBTsuUhLnv6ke/Curator---BDF-LINC?node-id=7389-64217&t=VjSnczaVpY1i76H5-0
        # Requires data from [DataSet](https://www.synapse.org/Synapse:syn66330217/tables/),
        #   [Organization](https://www.synapse.org/Synapse:syn63096836/tables/), and
        #   [Challenges](https://www.synapse.org/Synapse:syn65913973/tables/).
        # The only data needed from Challenges is the headerImage file handle id, but we want the order of the GCs
        #   to be the same as in Challenges, so using that as the base_table.
        # So far there is only one DataSet per grand challenge. Not sure if this will have to change at all when
        #   there are more.
        'dest_table_name': 'DataSet_denormalized',
        'base_table': 'DataSet',
        'columns': [
            {'faceted': False, 'name': 'id', 'alias': 'id'},
            {'faceted': False, 'name': 'name', 'alias': 'name'},
            {'faceted': False, 'name': 'description', 'alias': 'description'},
            # category does not show up in Figma design, but might want it on the page
            {'faceted': True, 'name': 'category', 'alias': 'category', 'transform': 'category_to_title_case'},
            {'faceted': False, 'name': 'topics', 'alias': 'topicIds'},
            {'faceted': False, 'name': 'produced_by', 'alias': 'producedByOrgId'},
            {'faceted': False, 'name': 'datasheet_url', 'alias': 'DatasheetURL'},
            {'faceted': False, 'name': 'documentation_url', 'alias': 'DocumentationURL'},
            {'faceted': False, 'name': 'is_public', 'alias': 'isPublic'},
            {'faceted': False, 'name': 'substrates', 'alias': 'substrateIds'},
        ],
        'join_columns': [
            {'join_tbl': 'Organization', 'from': 'produced_by', 'to': 'id',
             'dest_cols': [
                 {'faceted': True, 'name': 'name', 'alias': 'producedBy'},
                 # {'faceted': False, 'name': 'org_json', 'alias': 'org_json', 'whole_records': True,}
             ]},
            {'join_tbl': 'DataTopic', 'from': 'topics', 'to': 'id',
             'dest_cols': [
                 {'faceted': True, 'name': 'name', 'alias': 'topics'},
             ]},
            {'join_tbl': 'DataSubstrate', 'from': 'substrates', 'to': 'id',
             'dest_cols': [
                 {'faceted': False, 'name': 'name', 'alias': 'substrates'},
                 {'faceted': False, 'name': 'substrates_json', 'alias': 'substrates_json', 'whole_records': True, }
             ]},
        ],
    },
}

SRC_AND_DEST_TABLE_NAMES = SRC_TABLE_NAMES + list(DEST_TABLES.keys())
