"""Tests for utility helpers used by Synapse upload and schema scripts."""

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
    """Verify JSON table loading behavior."""

    def test_load_json_to_dataframe_reads_from_data_path_and_replaces_missing_values(self):
        """load_json_to_dataframe should read the configured file and fill missing text with empty strings."""
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
    """Verify Synapse column type inference from pandas Series values."""

    def test_infer_column_type_ignores_empty_values(self):
        """infer_column_type should infer from non-empty values when blanks and NaNs are present."""
        values = pd.Series(["", np.nan, 7])
        self.assertEqual(utils.infer_column_type(values), ColumnType.INTEGER)

    def test_infer_column_type_returns_string_for_mixed_types(self):
        """infer_column_type should fall back to STRING when a column mixes incompatible Python types."""
        values = pd.Series(["alpha", 7])
        self.assertEqual(utils.infer_column_type(values), ColumnType.STRING)


class ConfigureColumnFromDataTests(unittest.TestCase):
    """Verify Synapse column metadata is configured from observed data values."""

    def test_configure_column_from_data_sets_string_list_limits_and_facet_type(self):
        """configure_column_from_data should size STRING_LIST columns and enable faceting when requested."""
        column = Column(name="tags", column_type=ColumnType.STRING_LIST)
        values = pd.Series([["short", "a much longer tag"], ["mid"]])

        configured = utils.configure_column_from_data(column, values, faceted=True)

        self.assertEqual(configured.maximum_list_length, 2)
        self.assertGreaterEqual(configured.maximum_size, len("a much longer tag"))
        self.assertEqual(configured.facet_type, FacetType.ENUMERATION)

    def test_configure_column_from_data_promotes_large_strings_to_largetext(self):
        """configure_column_from_data should promote very long strings to LARGETEXT."""
        column = Column(name="description", column_type=ColumnType.STRING)
        values = pd.Series(["x" * 2501])

        configured = utils.configure_column_from_data(column, values)

        self.assertEqual(configured.column_type, ColumnType.LARGETEXT)


if __name__ == "__main__":
    unittest.main()
