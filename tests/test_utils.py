"""Tests for utility helpers used by Synapse upload scripts."""

import unittest

import pandas as pd
from synapseclient.models import ColumnType

from scripts.utils import infer_column_type


class InferColumnTypeTests(unittest.TestCase):
    """Verify Synapse column type inference for nested values."""

    def test_infer_column_type_returns_json_for_dict_values(self):
        values = pd.Series([{"name": "alpha"}, {"name": "beta"}, None, ""])

        self.assertEqual(infer_column_type(values), ColumnType.JSON)

    def test_infer_column_type_returns_json_for_list_of_dicts(self):
        values = pd.Series([
            [{"data_part_name": "Cell maps"}],
            [{"data_part_name": "Evidence"}],
            [],
        ])

        self.assertEqual(infer_column_type(values), ColumnType.JSON)

    def test_infer_column_type_keeps_string_lists_as_string_list(self):
        values = pd.Series([["alpha", "beta"], ["gamma"], []])

        self.assertEqual(infer_column_type(values), ColumnType.STRING_LIST)


if __name__ == "__main__":
    unittest.main()
