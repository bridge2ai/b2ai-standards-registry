"""Tests for building source tables from registry JSON files."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from synapseclient.models import ColumnType

from scripts.publishing import source_tables as source_module


class BuildSourceTableTests(unittest.TestCase):
    """Verify registry JSON loads into a DataFrame with an inferred schema."""

    def build(self, table_name, content):
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / f"{table_name}.json").write_text(json.dumps(content))
            with patch.object(source_module, "DATA_PATH", tmpdir):
                return source_module.build_source_table(table_name)

    def test_loads_records_and_infers_columns(self):
        coldefs, df = self.build("DataSet", {"data_collection": [{"id": "B2AI_DATA:1", "name": "Dataset One"}]})
        self.assertEqual(df.to_dict(orient="records"), [{"id": "B2AI_DATA:1", "name": "Dataset One"}])
        self.assertEqual([c.name for c in coldefs], ["id", "name"])

    def test_applies_datatype_overrides(self):
        coldefs, _ = self.build("DataStandardOrTool", {"standards": [
            {"id": "B2AI_STANDARD:1", "has_application": [{"name": "app"}]}]})
        types = {c.name: c.column_type for c in coldefs}
        self.assertEqual(types["has_application"], ColumnType.JSON)

    def test_rejects_file_without_record_list(self):
        with self.assertRaises(ValueError):
            self.build("DataSet", {"data_collection": {"not": "a list"}})


if __name__ == "__main__":
    unittest.main()
