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
    'DataStandardOrTool': { 'name': 'DataStandardOrTool', 'id': 'syn63096833' },
    'DataSubstrate': { 'name': 'DataSubstrate', 'id': 'syn63096834' },
    'DataTopic': { 'name': 'DataTopic', 'id': 'syn63096835' },
    'Organization': { 'name': 'Organization', 'id': 'syn63096836' },
    'UseCase': { 'name': 'UseCase', 'id': 'syn63096837' },
    # 'test': { 'name': 'test', 'id': 'syn64943432' }
}

DEST_TABLES = {
    # The table used for the explore landing page and to provide data for the home and detailed pages
    'DST_denormalized': {
        'dest_table_name': 'DST_denormalized',
        'base_table': 'DataStandardOrTool',
        'columns': [
            {'faceted': False, 'name': 'id',                        'alias': 'id'},
            {'faceted': False, 'name': 'name',                      'alias': 'acronym'},
            {'faceted': False, 'name': 'description',               'alias': 'name'},
            {'faceted': True,  'name': 'category',                  'alias': 'category', 'transform': 'camel_to_title_case'},
            {'faceted': False, 'name': 'purpose_detail',            'alias': 'description'},
            {'faceted': False, 'name': 'collection',                'alias': 'collections'},
            {'faceted': False, 'name': 'concerns_data_topic',       'alias': 'concerns_data_topic'},
            {'faceted': False, 'name': 'has_relevant_organization', 'alias': 'has_relevant_organization'},
            {'faceted': False, 'name': 'responsible_organization',  'alias': 'responsible_organization'},
            {'faceted': True,  'name': 'is_open',                   'alias': 'isOpen'},
            {'faceted': True,  'name': 'requires_registration',     'alias': 'registration'},
            {'faceted': False, 'name': 'url',                       'alias': 'URL'},
            {'faceted': False, 'name': 'formal_specification',      'alias': 'formalSpec'},
            {'faceted': False, 'name': 'publication',               'alias': 'publication'},
            {'faceted': False, 'name': 'has_training_resource',     'alias': 'trainingResources'},
            {'faceted': False, 'name': 'subclass_of',               'alias': 'subclassOf'},
            {'faceted': False, 'name': 'contribution_date',         'alias': 'contributionDate'},
            {'faceted': False, 'name': 'related_to',                'alias': 'relatedTo'},
        ],
        'join_columns': [
            {'join_tbl': 'DataTopic', 'join_type': 'left', 'from': 'concerns_data_topic', 'to': 'id',
             'dest_cols': [
                {'faceted': True, 'name': 'name', 'alias': 'topic'},
            ]},
            {'join_tbl': 'Organization', 'join_type': 'left', 'from': 'has_relevant_organization', 'to': 'id',
             'dest_cols': [
                 {'faceted': True,  'name': 'name', 'alias': 'relevantOrgNames'},
                 {'faceted': False, 'name': 'description', 'alias': 'relevantOrgDescriptions'},
             ]},
            {'join_tbl': 'Organization', 'join_type': 'left', 'from': 'responsible_organization', 'to': 'id',
             'dest_cols': [
                 {'faceted': False,  'name': 'name', 'alias': 'responsibleOrgAcronym'},
                 {'faceted': False,  'name': 'description', 'alias': 'responsibleOrgName'},
             ]},
        ],
    },
    # 'DataSetPlus': {  # commented out while fixing other issues, but don't delete
    #     'dest_table_name': 'DataSetPlus',
    #     'base_table': 'Challenges',
    #     'columns': [
    #         {'faceted': False, 'name': 'headerImage', 'alias': 'imgId'},
    #
    #         """
    #         dataset.name AS ds_name,  -- title
    #         dataset.description AS ds_description,
    #         # dataset.id,
    #         # dataset.category,
    #         dataset.data_url,
    #         dataset.datasheet_url,
    #         dataset.documentation_url,
    #         dataset.has_files,
    #         dataset.is_public,
    #         # dataset.produced_by,
    #         # dataset.substrates,
    #         data
    #         dataset.topics,
    #         org.id,
    #         org.category,
    #         org.name,
    #         org.description,
    #         org.contributor_name,
    #         org.contributor_github_name,
    #         org.contributor_orcid,
    #         org.ror_id,
    #         org.wikidata_id,
    #         org.url,
    #         org.subclass_of,
    #         challenges.headerImage,""",
    #
    #         {'faceted': False, 'name': 'id', 'alias': 'id'},
    #         {'faceted': False, 'name': 'name', 'alias': 'acronym'},
    #         {'faceted': False, 'name': 'description', 'alias': 'name'},
    #         {'faceted': True, 'name': 'category', 'alias': 'category', 'transform': 'camel_to_title_case'},
    #         {'faceted': False, 'name': 'purpose_detail', 'alias': 'description'},
    #         {'faceted': False, 'name': 'collection', 'alias': 'collections'},
    #         {'faceted': False, 'name': 'concerns_data_topic', 'alias': 'concerns_data_topic'},
    #         {'faceted': False, 'name': 'has_relevant_organization', 'alias': 'has_relevant_organization'},
    #         {'faceted': False, 'name': 'responsible_organization', 'alias': 'responsible_organization'},
    #         {'faceted': True, 'name': 'is_open', 'alias': 'isOpen'},
    #         {'faceted': True, 'name': 'requires_registration', 'alias': 'registration'},
    #         {'faceted': False, 'name': 'url', 'alias': 'URL'},
    #         {'faceted': False, 'name': 'formal_specification', 'alias': 'formalSpec'},
    #         {'faceted': False, 'name': 'publication', 'alias': 'publication'},
    #         {'faceted': False, 'name': 'has_training_resource', 'alias': 'trainingResources'},
    #         {'faceted': False, 'name': 'subclass_of', 'alias': 'subclassOf'},
    #         {'faceted': False, 'name': 'contribution_date', 'alias': 'contributionDate'},
    #         {'faceted': False, 'name': 'related_to', 'alias': 'relatedTo'},
    #     ],
    #     'join_columns': [
    #         {'join_tbl': 'DataTopic', 'join_type': 'left', 'from': 'concerns_data_topic', 'to': 'id',
    #          'dest_cols': [
    #              {'faceted': True, 'name': 'name', 'alias': 'topic'},
    #          ]},
    #         {'join_tbl': 'Organization', 'join_type': 'left', 'from': 'has_relevant_organization', 'to': 'id',
    #          'dest_cols': [
    #              {'faceted': True, 'name': 'name', 'alias': 'relevantOrgNames'},
    #              {'faceted': False, 'name': 'description', 'alias': 'relevantOrgDescriptions'},
    #          ]},
    #         {'join_tbl': 'Organization', 'join_type': 'left', 'from': 'responsible_organization', 'to': 'id',
    #          'dest_cols': [
    #              {'faceted': False, 'name': 'name', 'alias': 'responsibleOrgAcronym'},
    #              {'faceted': False, 'name': 'description', 'alias': 'responsibleOrgName'},
    #          ]},
    #     ],
    # },
}

SRC_AND_DEST_TABLE_NAMES = SRC_TABLE_NAMES + list(DEST_TABLES.keys())
