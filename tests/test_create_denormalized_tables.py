import unittest
from unittest.mock import patch, sentinel

import pandas as pd

from scripts import create_denormalized_tables as denorm_module


class DenormalizeTablesTests(unittest.TestCase):
    @patch.object(denorm_module, "upload_denormalized_manifest")
    @patch.object(denorm_module, "make_dest_table")
    @patch.object(denorm_module, "get_src_table")
    @patch.object(denorm_module, "initialize_synapse")
    def test_denormalize_tables_includes_manifest_in_default_run(
        self,
        mock_initialize_synapse,
        mock_get_src_table,
        mock_make_dest_table,
        mock_upload_denormalized_manifest,
    ):
        mock_initialize_synapse.return_value = sentinel.synapse
        mock_get_src_table.side_effect = lambda syn, table_info: {
            **table_info,
            "df": pd.DataFrame([{"id": "row1"}]),
        }
        mock_make_dest_table.return_value = pd.DataFrame([{"id": "row1"}])

        with patch.object(denorm_module, "DEST_TABLES", {
            "DST_denormalized": {
                "dest_table_name": "DST_denormalized",
                "base_table": "DataSet",
                "join_columns": [],
            },
        }), patch.object(denorm_module, "TABLE_IDS", {
            "DataSet": {"name": "DataSet", "id": "synDataSet"},
            "DST_denormalized": {"name": "DST_denormalized", "id": "synDenorm"},
            "Manifest": {"name": "Manifest", "id": "synManifest"},
        }):
            denorm_module.denormalize_tables()

        mock_make_dest_table.assert_called_once()
        mock_upload_denormalized_manifest.assert_called_once_with(
            syn=sentinel.synapse,
            table_id="synManifest",
        )

    @patch.object(denorm_module, "upload_denormalized_manifest")
    @patch.object(denorm_module, "make_dest_table")
    @patch.object(denorm_module, "initialize_synapse")
    def test_denormalize_tables_can_run_manifest_only(
        self,
        mock_initialize_synapse,
        mock_make_dest_table,
        mock_upload_denormalized_manifest,
    ):
        mock_initialize_synapse.return_value = sentinel.synapse

        with patch.object(denorm_module, "DEST_TABLES", {
            "DST_denormalized": {
                "dest_table_name": "DST_denormalized",
                "base_table": "DataSet",
                "join_columns": [],
            },
        }), patch.object(denorm_module, "TABLE_IDS", {
            "Manifest": {"name": "Manifest", "id": "synManifest"},
        }):
            denorm_module.denormalize_tables(["Manifest"])

        mock_make_dest_table.assert_not_called()
        mock_upload_denormalized_manifest.assert_called_once_with(
            syn=sentinel.synapse,
            table_id="synManifest",
        )

    @patch.object(denorm_module, "upload_denormalized_manifest")
    @patch.object(denorm_module, "make_dest_table")
    @patch.object(denorm_module, "get_src_table")
    @patch.object(denorm_module, "initialize_synapse")
    def test_denormalize_tables_skips_manifest_when_specific_tables_exclude_it(
        self,
        mock_initialize_synapse,
        mock_get_src_table,
        mock_make_dest_table,
        mock_upload_denormalized_manifest,
    ):
        mock_initialize_synapse.return_value = sentinel.synapse
        mock_get_src_table.side_effect = lambda syn, table_info: {
            **table_info,
            "df": pd.DataFrame([{"id": "row1"}]),
        }
        mock_make_dest_table.return_value = pd.DataFrame([{"id": "row1"}])

        with patch.object(denorm_module, "DEST_TABLES", {
            "DST_denormalized": {
                "dest_table_name": "DST_denormalized",
                "base_table": "DataSet",
                "join_columns": [],
            },
        }), patch.object(denorm_module, "TABLE_IDS", {
            "DataSet": {"name": "DataSet", "id": "synDataSet"},
            "DST_denormalized": {"name": "DST_denormalized", "id": "synDenorm"},
            "Manifest": {"name": "Manifest", "id": "synManifest"},
        }):
            denorm_module.denormalize_tables(["DST_denormalized"])

        mock_make_dest_table.assert_called_once()
        mock_upload_denormalized_manifest.assert_not_called()


if __name__ == "__main__":
    unittest.main()
