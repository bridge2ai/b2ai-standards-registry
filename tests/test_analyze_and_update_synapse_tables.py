"""Tests for Synapse table update behavior, including Manifest special-casing."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, sentinel

import pandas as pd
from synapseclient.models import ColumnType

from scripts import analyze_and_update_synapse_tables as update_module


class PopulateTableTests(unittest.TestCase):
    """Verify populate_table chooses the correct upload path for each source table."""

    @patch.object(update_module, "clear_populate_snapshot_table")
    @patch.object(update_module, "upload_denormalized_manifest")
    def test_populate_table_uses_denormalized_manifest_for_manifest(
        self,
        mock_upload_denormalized_manifest,
        mock_clear_populate_snapshot_table,
    ):
        """populate_table should delegate Manifest uploads to the denormalized Manifest helper."""
        update_module.populate_table(
            sentinel.synapse,
            "project/data/Manifest.json",
            "synManifest",
        )

        mock_upload_denormalized_manifest.assert_called_once_with(
            syn=sentinel.synapse,
            table_id="synManifest",
        )
        mock_clear_populate_snapshot_table.assert_not_called()

    @patch.object(update_module, "clear_populate_snapshot_table")
    @patch.object(update_module, "get_col_defs", return_value=[sentinel.coldef])
    @patch.object(update_module, "upload_denormalized_manifest")
    def test_populate_table_loads_regular_json_tables_normally(
        self,
        mock_upload_denormalized_manifest,
        mock_get_col_defs,
        mock_clear_populate_snapshot_table,
    ):
        """populate_table should keep the standard JSON-to-DataFrame path for non-Manifest tables."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "DataSet.json"
            file_path.write_text(json.dumps({
                "data_collection": [
                    {"id": "B2AI_DATA:1", "name": "Dataset One"},
                ]
            }))

            update_module.populate_table(
                sentinel.synapse,
                str(file_path),
                "synDataset",
            )

        mock_upload_denormalized_manifest.assert_not_called()
        mock_get_col_defs.assert_called_once()
        args = mock_clear_populate_snapshot_table.call_args.args
        self.assertIs(args[0], sentinel.synapse)
        self.assertEqual(args[1], "DataSet")
        self.assertEqual(args[2], [sentinel.coldef])
        self.assertEqual(args[3].to_dict(orient="records"), [{"id": "B2AI_DATA:1", "name": "Dataset One"}])
        self.assertEqual(args[4], "synDataset")


class GetColDefsTests(unittest.TestCase):
    """Verify table-specific Synapse schema overrides."""

    def test_get_col_defs_marks_manifest_data_parts_as_json(self):
        df = pd.DataFrame(
            [
                {
                    "id": "B2AI_MANIFEST:1",
                    "data_parts": [
                        {
                            "data_part_name": "Cell maps",
                            "standards_and_tools": ["B2AI_STANDARD:372"],
                        }
                    ],
                }
            ]
        )

        coldefs = {col.name: col for col in update_module.get_col_defs(df, "Manifest")}

        self.assertEqual(coldefs["data_parts"].column_type, ColumnType.JSON)


if __name__ == "__main__":
    unittest.main()
