from enum import Enum
from pathlib import Path
import unittest
from unittest.mock import patch
import yaml
import scripts.modify_synapse_schema as modify_synapse_schema

class TestSlotRegistration(unittest.TestCase):
	SCHEMA_DIRECTORY = "src/schema"
	MODIFY_SYNAPSE_SCHEMA_FILE = "scripts/modify_synapse_schema.py"

	@staticmethod
	def _get_table_slots():
		"""Returns a dictionary containing the names of each table (keys) and a list of their slots (values)"""
		ignore_files = [
			"standards_dataset_schema",
			"standards_schema_all",
			"standards_schema"
		]

		table_slots = {}

		for file_path in Path(TestSlotRegistration.SCHEMA_DIRECTORY).iterdir():
			file_path = Path(file_path)
			if(file_path.is_file() and file_path.stem not in ignore_files):
				with file_path.open() as file:
					file_contents = yaml.safe_load(file)
					classes = file_contents["classes"]

					# The first class is for the table itself
					table_name = list(classes.keys())[0]
					slots = classes[table_name]["slots"]

					table_slots[table_name] = slots

		return table_slots


	def test_slot_registration(self):
		"""
		Verify that each added/modified slot has been added to all column definitions in 'modify_snyapse_schema.py'.
		This includes the enums `ColumnName` and `TableSchema`, plus the dictionary `COLUMN_TEMPLATES`
		"""

		table_slots = TestSlotRegistration._get_table_slots()
		for table, slots in table_slots.items():
			for slot in slots:
				# All slots should be registered in these places
				self.assertTrue(
					slot in [entry.value for entry in modify_synapse_schema.ColumnName],
					f"'{slot}' not in '{TestSlotRegistration.MODIFY_SYNAPSE_SCHEMA_FILE}' > 'ColumnName'"
				)
				self.assertTrue(
					modify_synapse_schema.ColumnName(slot) in list(modify_synapse_schema.COLUMN_TEMPLATES.keys()),
					f"'{slot}' not in '{TestSlotRegistration.MODIFY_SYNAPSE_SCHEMA_FILE}' > 'COLUMN_TEMPLATES'"
				)

				# Table-specific slot registration
				self.assertTrue(
					modify_synapse_schema.ColumnName(slot) in modify_synapse_schema.TableSchema[table].value["columns"],
					f"'{slot}' not in '{TestSlotRegistration.MODIFY_SYNAPSE_SCHEMA_FILE}' > 'TableSchema[{table}]'"
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
		self.table_slots_patcher = patch.object(TestSlotRegistration, '_get_table_slots', return_value=table_slots)
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
