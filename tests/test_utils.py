import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
from synapseclient.models import Column, ColumnType, FacetType

from scripts import utils


class LoadJsonToDataFrameTests(unittest.TestCase):
    def test_load_json_to_dataframe_reads_from_data_path_and_replaces_missing_values(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "Example.json"
            file_path.write_text(json.dumps({
                "items": [
                    {"id": "1", "name": "alpha", "description": "present"},
                    {"id": "2", "name": "beta"},
                ]
            }))

            with patch.object(utils, "DATA_PATH", tmpdir):
                df = utils.load_json_to_dataframe("Example")

        self.assertEqual(df["id"].tolist(), ["1", "2"])
        self.assertEqual(df.loc[1, "description"], "")


class InferColumnTypeTests(unittest.TestCase):
    def test_infer_column_type_ignores_empty_values(self):
        values = pd.Series(["", np.nan, 7])
        self.assertEqual(utils.infer_column_type(values), ColumnType.INTEGER)

    def test_infer_column_type_returns_string_for_mixed_types(self):
        values = pd.Series(["alpha", 7])
        self.assertEqual(utils.infer_column_type(values), ColumnType.STRING)


class ConfigureColumnFromDataTests(unittest.TestCase):
    def test_configure_column_from_data_sets_string_list_limits_and_facet_type(self):
        column = Column(name="tags", column_type=ColumnType.STRING_LIST)
        values = pd.Series([["short", "a much longer tag"], ["mid"]])

        configured = utils.configure_column_from_data(column, values, faceted=True)

        self.assertEqual(configured.maximum_list_length, 2)
        self.assertGreaterEqual(configured.maximum_size, len("a much longer tag"))
        self.assertEqual(configured.facet_type, FacetType.ENUMERATION)

    def test_configure_column_from_data_promotes_large_strings_to_largetext(self):
        column = Column(name="description", column_type=ColumnType.STRING)
        values = pd.Series(["x" * 2501])

        configured = utils.configure_column_from_data(column, values)

        self.assertEqual(configured.column_type, ColumnType.LARGETEXT)


if __name__ == "__main__":
    unittest.main()
