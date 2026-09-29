"""Tests for the unified Synapse publish script."""

import unittest
from unittest.mock import MagicMock, patch

import pandas as pd
from synapseclient.models import Column, ColumnType

from scripts.publishing import create_denormalized_tables as denorm_module
from scripts.publishing import publish_to_synapse as publish_module

COLS = [Column(name="id", column_type=ColumnType.STRING),
        Column(name="tags", column_type=ColumnType.STRING_LIST)]


def make_df():
    return pd.DataFrame([{"id": "a", "tags": ["x", "y"]}, {"id": "b", "tags": []}])


class ContentHashTests(unittest.TestCase):
    """content_hash should change exactly when the upload would."""

    def test_same_content_same_hash(self):
        self.assertEqual(publish_module.content_hash(COLS, make_df()),
                         publish_module.content_hash(COLS, make_df()))

    def test_row_change_changes_hash(self):
        df = make_df()
        df.loc[1, "id"] = "c"
        self.assertNotEqual(publish_module.content_hash(COLS, make_df()),
                            publish_module.content_hash(COLS, df))

    def test_schema_change_changes_hash(self):
        cols = [COLS[0], Column(name="tags", column_type=ColumnType.JSON)]
        self.assertNotEqual(publish_module.content_hash(COLS, make_df()),
                            publish_module.content_hash(cols, make_df()))


@patch.object(publish_module, "TABLE_IDS", {"T": {"name": "T", "id": "synT"}})
@patch.object(publish_module, "set_annotations")
@patch.object(publish_module, "row_count")
@patch.object(publish_module, "clear_populate_snapshot_table", return_value=("synT", 7))
@patch.object(publish_module, "get_annotation")
class PublishTableTests(unittest.TestCase):
    """publish_table should skip unchanged tables and verify uploads."""

    def test_skips_when_hash_matches(self, get_annotation, clear_populate, row_count, set_annotations):
        get_annotation.return_value = publish_module.content_hash(COLS, make_df())
        publish_module.publish_table(MagicMock(), "T", COLS, make_df())
        clear_populate.assert_not_called()

    def test_force_publishes_unchanged(self, get_annotation, clear_populate, row_count, set_annotations):
        get_annotation.return_value = publish_module.content_hash(COLS, make_df())
        row_count.return_value = 2
        publish_module.publish_table(MagicMock(), "T", COLS, make_df(), force=True)
        clear_populate.assert_called_once()

    def test_publishes_and_records_verified_version(self, get_annotation, clear_populate, row_count, set_annotations):
        get_annotation.return_value = None
        row_count.return_value = 2
        publish_module.publish_table(MagicMock(), "T", COLS, make_df())
        row_count.assert_called_once_with("synT", 7)
        values = set_annotations.call_args.args[2]
        self.assertEqual(values[publish_module.VERSION_ANNOTATION], 7)

    def test_row_count_mismatch_fails_without_annotating(self, get_annotation, clear_populate, row_count, set_annotations):
        get_annotation.return_value = None
        row_count.return_value = 4
        with self.assertRaises(publish_module.PublishError):
            publish_module.publish_table(MagicMock(), "T", COLS, make_df())
        set_annotations.assert_not_called()

    def test_empty_table_is_not_uploaded(self, get_annotation, clear_populate, row_count, set_annotations):
        with self.assertRaises(publish_module.PublishError):
            publish_module.publish_table(MagicMock(), "T", COLS, make_df().iloc[0:0])
        clear_populate.assert_not_called()

    def test_dry_run_changes_nothing(self, get_annotation, clear_populate, row_count, set_annotations):
        get_annotation.return_value = None
        publish_module.publish_table(MagicMock(), "T", COLS, make_df(), dry_run=True)
        clear_populate.assert_not_called()
        set_annotations.assert_not_called()


class DependencyOrderTests(unittest.TestCase):
    """dest tables that join other dest tables must be built after them."""

    def test_joined_dest_table_comes_first(self):
        dest_tables = {
            "A": {"join_columns": [{"join_tbl": "B"}, {"join_tbl": "Organization"}]},
            "B": {"join_columns": []},
        }
        with patch.object(denorm_module, "DEST_TABLES", dest_tables):
            self.assertEqual(denorm_module.dependency_order(), ["B", "A"])

    def test_cycle_raises(self):
        dest_tables = {
            "A": {"join_columns": [{"join_tbl": "B"}]},
            "B": {"join_columns": [{"join_tbl": "A"}]},
        }
        with patch.object(denorm_module, "DEST_TABLES", dest_tables):
            with self.assertRaises(ValueError):
                denorm_module.dependency_order()


if __name__ == "__main__":
    unittest.main()
