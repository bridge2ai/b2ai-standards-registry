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
    # 'Manifest',
    # 'test',
]
TABLE_IDS = {
    # 'CurrentTableVersions': { 'name': 'CurrentTableVersions', 'id': 'syn66330007' },
    'D4D_content': { 'name': 'D4D_content', 'id': 'syn68885644' },
    'DST_denormalized': { 'name': 'DST_denormalized', 'id': 'syn65676531' },
    'DataSet': { 'name': 'DataSet', 'id': 'syn66330217' },
    'DataSet_denormalized': { 'name': 'DataSet_denormalized', 'id': 'syn68258237' },
    'DataStandardOrTool': { 'name': 'DataStandardOrTool', 'id': 'syn63096833' },
    'DataSubstrate': { 'name': 'DataSubstrate', 'id': 'syn63096834' },
    'DataTopic': { 'name': 'DataTopic', 'id': 'syn63096835' },
    'Organization': { 'name': 'Organization', 'id': 'syn63096836' },
    'Organization_denormalized': { 'name': 'Organization_denormalized', 'id': 'syn69693360' },
    'UseCase': { 'name': 'UseCase', 'id': 'syn63096837' },
    # 'Manifest': { 'name': 'Manifest', 'id': 'syn72106735' }, # not sure if i'll need this
    # 'test': { 'name': 'test', 'id': 'syn64943432' }
}

# see top of create_denormalized_tables:make_dest_table() for how to define destination tables
DEST_TABLES = {
    # The table used for the explore landing page and to provide data for the home and detailed pages
    'DST_denormalized': {
        'dest_table_name': 'DST_denormalized',
        'base_table': 'DataStandardOrTool',
        'columns': [
            {'name': 'id',                          'alias': 'id'},
            {'name': 'name',                        'alias': 'acronym'},
            {'name': 'description',                 'alias': 'name'},
            { 'name': 'category',                   'alias': 'category', 'transform': 'category_to_title_case', 'faceted': True, },
            {'name': 'purpose_detail',              'alias': 'description'},
            {'name': 'collection',                  'alias': 'collections', 'transform': 'collections_to_title_case', 'faceted': True, },
            {'name': 'has_application',             'alias': 'AIApplicationJSON', },
            {'name': 'has_application',             'alias': 'aiApplicationCount',  'transform': 'json_to_count', 'columnType': 'INTEGER'},
            {'name': 'has_application',             'alias': 'hasAIApplication', 'transform': 'count_to_yes_no', 'columnType': 'STRING', 'faceted': True, },
            {'name': 'has_application',             'alias': 'applicationNames', 'transform': 'json_to_name_strings', 'columnType': 'STRING_LIST', 'faceted': True, },
            {'name': 'collection',                  'alias': 'mature', 'transform': 'collections_to_is_mature', 'columnType': 'STRING', 'faceted': True, },
            {'name': 'concerns_data_topic',         'alias': 'concerns_data_topic'},
            {'name': 'has_relevant_data_substrate', 'alias': 'has_relevant_data_substrate'},
            {'name': 'has_relevant_organization',   'alias': 'has_relevant_organization'},
            {'name': 'responsible_organization',    'alias': 'responsible_organization'},
            {'name': 'is_open',                     'alias': 'isOpen', 'transform': 'bool_to_yes_no', 'columnType': 'STRING', 'faceted': True, },
            {'name': 'requires_registration',       'alias': 'registration', 'transform': 'bool_to_yes_no', 'columnType': 'STRING', 'faceted': True, },
            {'name': 'url',                         'alias': 'URL'},
            {'name': 'formal_specification',        'alias': 'formalSpec'},
            {'name': 'publication',                 'alias': 'publication'},
            {'name': 'has_training_resource',       'alias': 'trainingResources'},
            {'name': 'subclass_of',                 'alias': 'subclassOf'},
            {'name': 'contribution_date',           'alias': 'contributionDate'},
            {'name': 'related_to',                  'alias': 'relatedTo'},
            {'name': 'used_in_bridge2ai',           'alias': 'usedInBridge2AI', 'transform': 'bool_to_yes_no', 'columnType': 'STRING', 'faceted': True, },
        ],
        'join_columns': [
            {'join_tbl': 'DataTopic', 'base_tbl_col': 'concerns_data_topic', 'join_tbl_col': 'id',
             'dest_cols': [
                 {'faceted': True, 'name': 'name', 'alias': 'topic'},
             ]},
			 {'join_tbl': 'DataTopic', 'base_tbl_col': 'concerns_data_topic', 'join_tbl_col': 'id',
             'dest_cols': [
                 {'faceted': True, 'name': 'description', 'alias': 'topicDescription'},
             ]},
            {'join_tbl': 'DataSubstrate', 'base_tbl_col': 'has_relevant_data_substrate', 'join_tbl_col': 'id',
             'dest_cols': [
                {'faceted': True, 'name': 'name', 'alias': 'dataTypes'},
            ]},
			{'join_tbl': 'DataSubstrate', 'base_tbl_col': 'has_relevant_data_substrate', 'join_tbl_col': 'id',
             'dest_cols': [
                {'name': 'description', 'alias': 'dataTypesDescription'},
            ]},
            {'join_tbl': 'Organization', 'base_tbl_col': 'has_relevant_organization', 'join_tbl_col': 'id',
             'dest_cols': [
                 {'faceted': True,  'name': 'description', 'alias': 'relevantOrgNames'},
                 {'source_cols': ['id', 'name'], 'alias': 'relevantOrgLinks', 'transform': 'create_org_link', },
             ]},
            {'join_tbl': 'Organization', 'base_tbl_col': 'responsible_organization', 'join_tbl_col': 'id',
             'dest_cols': [
                 { 'name': 'description', 'alias': 'responsibleOrgName'},
                 {'source_cols': ['id', 'name'], 'alias': 'responsibleOrgLinks',
                  'transform': 'create_org_link', },
             ]},
			 {'join_tbl': 'DataSet_denormalized', 'base_tbl_col': 'responsible_organization', 'join_tbl_col': 'producedByOrgId',
             'dest_cols': [
                 { 'name': 'description', 'alias': 'responsibleOrgDatasetDescriptions', 'columnType': 'LARGETEXT'},
             ]},
			 {'join_tbl': 'DataSet_denormalized', 'base_tbl_col': 'responsible_organization', 'join_tbl_col': 'producedByOrgId',
             'dest_cols': [
                 { 'name': 'topics', 'alias': 'responsibleOrgDatasetTopics', 'columnType': 'LARGETEXT'},
             ]},
			 {'join_tbl': 'DataSet_denormalized', 'base_tbl_col': 'has_relevant_organization', 'join_tbl_col': 'producedByOrgId',
             'dest_cols': [
                 { 'name': 'description', 'alias': 'relevantOrgDatasetDescriptions', 'columnType': 'LARGETEXT'},
             ]},
			 {'join_tbl': 'DataSet_denormalized', 'base_tbl_col': 'has_relevant_organization', 'join_tbl_col': 'producedByOrgId',
             'dest_cols': [
                 { 'name': 'topics', 'alias': 'relevantOrgDatasetTopics', 'columnType': 'LARGETEXT'},
             ]},
        ],
    },
    'Organization_denormalized': {
        'dest_table_name': 'Organization_denormalized',
        'base_table': 'Organization',
        'columns': [
            {'name': 'id', 'alias': 'id'},
            {'name': 'name', 'alias': 'name'},
            {'name': 'description', 'alias': 'description'},
            {'name': 'ror_id', 'alias': 'ror_id'},
            {'name': 'wikidata_id', 'alias': 'wikidata_id'},
            {'name': 'url', 'alias': 'url'},
            {'name': 'subclass_of', 'alias': 'subclass_of'},
        ],
        'join_columns': [
            {
                'join_tbl': 'Organization',
                'base_tbl_col': 'subclass_of',
                'join_tbl_col': 'id',
                'reverse_lookup': False,
                'dest_cols': [
                    {'alias': 'main_organization_json', 'whole_records': True},
                ]
            },
            {
                'join_tbl': 'Organization',
                'base_tbl_col': 'id',
                'join_tbl_col': 'subclass_of',
                'reverse_lookup': True,
                'dest_cols': [
                    {'alias': 'associated_organization_json', 'whole_records': True},
                ]
            },
            {
                'join_tbl': 'DataStandardOrTool',
                'base_tbl_col': 'id',
                'join_tbl_col': 'has_relevant_organization',
                'reverse_lookup': True,
                'dest_cols': [
                    {'name': 'id', 'alias': 'relevant_standards'},
                    {'alias': 'relevant_standards_json', 'whole_records': True},
                ]
            },
            {
                'join_tbl': 'DataStandardOrTool',
                'base_tbl_col': 'id',
                'join_tbl_col': 'responsible_organization',
                'reverse_lookup': True,
                'dest_cols': [
                    {'name': 'id', 'alias': 'governed_standards'},
                    {'alias': 'governed_standards_json', 'whole_records': True},
                ]
            },
            {
                'join_tbl': 'DataSet',
                'base_tbl_col': 'id',
                'join_tbl_col': 'produced_by',
                'reverse_lookup': True,
                'dest_cols': [
                    {'name': 'id', 'alias': 'datasets'},
                    {'name': 'name', 'alias': 'dataset_names'},
                    {'alias': 'dataset_json', 'whole_records': True},
                ]
            },
            {
                'join_tbl': 'D4D_content',
                'base_tbl_col': 'id',
                'join_tbl_col': 'content_id',
                'reverse_lookup': True,
                'dest_cols': [
                    {'alias': 'd4d', 'whole_records': True},
                ]
            },
        ],
    },
    'DataSet_denormalized': {
        'dest_table_name': 'DataSet_denormalized',
        'base_table': 'DataSet',
        'columns': [
            {'name': 'id', 'alias': 'id'},
            {'name': 'name', 'alias': 'name'},
            {'name': 'description', 'alias': 'description'},
            # category does not show up in Figma design, but might want it on the page
            {'faceted': True, 'name': 'category', 'alias': 'category', 'transform': 'category_to_title_case'},
            {'name': 'topics', 'alias': 'topicIds'},
            {'name': 'produced_by', 'alias': 'producedByOrgId'},
            {'name': 'datasheet_url', 'alias': 'DatasheetURL'},
            {'name': 'documentation_url', 'alias': 'DocumentationURL'},
            {'name': 'is_public', 'alias': 'isPublic'},
            {'name': 'substrates', 'alias': 'substrateIds'},
        ],
        'join_columns': [
            {'join_tbl': 'Organization', 'base_tbl_col': 'produced_by', 'join_tbl_col': 'id',
             'dest_cols': [
                 {'faceted': True, 'name': 'name', 'alias': 'producedBy'},
             ]},
            {'join_tbl': 'DataTopic', 'base_tbl_col': 'topics', 'join_tbl_col': 'id',
             'dest_cols': [
                 {'faceted': True, 'name': 'name', 'alias': 'topics'},
             ]},
            {'join_tbl': 'DataSubstrate', 'base_tbl_col': 'substrates', 'join_tbl_col': 'id',
             'dest_cols': [
                 {'name': 'name', 'alias': 'substrates'},
                 {'name': 'substrates_json', 'alias': 'substrates_json', 'whole_records': True, }
             ]},
        ],
    },
}

SRC_AND_DEST_TABLE_NAMES = SRC_TABLE_NAMES + list(DEST_TABLES.keys())
