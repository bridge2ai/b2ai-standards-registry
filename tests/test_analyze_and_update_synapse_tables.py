"""Tests for Synapse table update behavior."""

import unittest

import pandas as pd
from synapseclient.models import ColumnType

from scripts.analyze_and_update_synapse_tables import get_col_defs


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

        coldefs = {col.name: col for col in get_col_defs(df, "Manifest")}

        self.assertEqual(coldefs["data_parts"].column_type, ColumnType.JSON)


if __name__ == "__main__":
    unittest.main()
