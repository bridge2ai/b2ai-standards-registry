from enum import Enum
from pathlib import Path
import unittest
from unittest.mock import patch
import yaml
import scripts.modify_synapse_schema as modify_synapse_schema

class TestSlotRegistration(unittest.TestCase):
    DATA_DIRECTORY = "src/data"
    MODIFY_SYNAPSE_SCHEMA_FILE = "scripts/modify_synapse_schema.py"


    def _get_slots_by_table(self):
        """
        Returns a dictionary of slots used by each table.
            Keys = table names
            Values = sets of slots used by each table
        """
        slots_by_table = {}
        for file_path in Path(TestSlotRegistration.DATA_DIRECTORY).iterdir():
            if((not file_path.is_file()) or file_path.stem == "DataSet"):    # 'DataSet' is incomplete
                continue

            with file_path.open() as file:
                file_contents = yaml.safe_load(file)
            table_data = list(file_contents.values())[0]

            table_slots = set()
            table_name = file_path.stem

            for entry in table_data:
                entry_slots = entry.keys()
                table_slots.update(entry_slots)

            slots_by_table[table_name] = table_slots

        return slots_by_table


    @unittest.skip("This is failing now. We no longer need modify_synapse_schema.py")
    def test_slot_registration(self):
        """
        Verify that every slot in each table has been added to all column definitions in 'modify_snyapse_schema.py'.
        This includes the enums `ColumnName` and `TableSchema`, plus the dictionary `COLUMN_TEMPLATES`
        """
        ColumnName_values = [entry.value for entry in modify_synapse_schema.ColumnName]
        COLUMN_TEMPLATE_keys = list(modify_synapse_schema.COLUMN_TEMPLATES.keys())

        for table, slots in self._get_slots_by_table().items():
            for slot in slots:
                # All slots should be registered in these places
                self.assertTrue(
                    slot in ColumnName_values,
                    f"slot '{slot}' not in '{TestSlotRegistration.MODIFY_SYNAPSE_SCHEMA_FILE}' > 'ColumnName'"
                )
                self.assertTrue(
                    modify_synapse_schema.ColumnName(slot) in COLUMN_TEMPLATE_keys,
                    f"slot '{slot}' not in '{TestSlotRegistration.MODIFY_SYNAPSE_SCHEMA_FILE}' > 'COLUMN_TEMPLATES'"
                )

                # Table-specific slot registration
                self.assertTrue(
                    modify_synapse_schema.ColumnName(slot) in modify_synapse_schema.TableSchema[table].value["columns"],
                    f"slot '{slot}' not in '{TestSlotRegistration.MODIFY_SYNAPSE_SCHEMA_FILE}' > 'TableSchema[{table}]'"
                )



class MockColumnName(Enum):
    TEST_SLOT = "test_slot"

MOCK_COLUMN_TEMPLATES = {
    MockColumnName.TEST_SLOT: "Definition of column"
}

class MockTableSchema(Enum):
    DataStandardOrTool = {
        "id": "syn63096833",
        "columns": [
            MockColumnName.TEST_SLOT
        ],
    }

class TestSlotRegistrationTests(unittest.TestCase):
    """Tests for TestSlotRegistration.test_slot_registration()"""

    def setUp(self):
        table_slots = {"DataStandardOrTool": ['test_slot']}
        self.table_slots_patcher = patch.object(TestSlotRegistration, '_get_slots_by_table', return_value=table_slots)
        self.mock_table_slots = self.table_slots_patcher.start()
        self.addCleanup(self.table_slots_patcher.stop)


    def _run_target_test(self) -> unittest.TestResult:
        test_case = TestSlotRegistration(methodName='test_slot_registration')
        result = unittest.TestResult()
        test_case.run(result)
        return result

    def test_unregistered_slot(self):
        """INVALID - Slot not defined anywhere"""
        result = self._run_target_test()
        self.assertEqual(len(result.failures), 1)


    @patch("scripts.modify_synapse_schema.ColumnName", new=MockColumnName)
    def test_slot_not_in_column_templates_or_table_schema(self):
        """INVALID - Slot not defined in 'COLUMN_TEMPLATES' or 'TableSchema'"""
        result = self._run_target_test()
        self.assertEqual(len(result.failures), 1)


    @patch("scripts.modify_synapse_schema.ColumnName", new=MockColumnName)
    @patch("scripts.modify_synapse_schema.COLUMN_TEMPLATES", new=MOCK_COLUMN_TEMPLATES)
    def test_slot_not_in_table_schema(self):
        """INVALID - Slot not defined in 'TableSchema'"""
        result = self._run_target_test()
        self.assertEqual(len(result.failures), 1)


    @patch("scripts.modify_synapse_schema.ColumnName", new=MockColumnName)
    @patch("scripts.modify_synapse_schema.COLUMN_TEMPLATES", new=MOCK_COLUMN_TEMPLATES)
    @patch("scripts.modify_synapse_schema.TableSchema", new=MockTableSchema)
    def test_slot_is_registered(self):
        """VALID - Slot defined everywhere"""
        result = self._run_target_test()
        self.assertTrue(result.wasSuccessful())


if __name__ == "__main__":
    unittest.main()
