from enum import Enum
from pathlib import Path
import unittest
from unittest.mock import patch
import yaml
import scripts.modify_synapse_schema as modify_synapse_schema

class TestSlotRegistration(unittest.TestCase):
	SCHEMA_DIRECTORY = "src/schema"
	DATA_DIRECTORY = "src/data"
	MODIFY_SYNAPSE_SCHEMA_FILE = "scripts/modify_synapse_schema.py"

	@staticmethod
	def _get_inheritable_slots():
		"""'standards_schema' holds parent classes. Tables can inherit slots from this"""
		parent_class_slots = {}

		standards_schema_path = Path(TestSlotRegistration.SCHEMA_DIRECTORY + "/standards_schema.yaml")
		with standards_schema_path.open() as file:
			file_contents = yaml.safe_load(file)
			classes = file_contents["classes"]

			for schema_class in classes:
				if("slots" in schema_class):
					parent_class_slots[schema_class] = schema_class["slots"]

		return parent_class_slots


	# @staticmethod
	# def _extract_slots(file_path):
	# 	slot_dict = {}

	# 	with file_path.open() as file:
	# 		file_contents = yaml.safe_load(file)

	# 	classes = file_contents["classes"]
	# 	for class_name, class_definition in classes:
	# 		if("slots" in class_definition):
	# 			slot_dict[class_name] = class_definition["slots"]

	# 	return slot_dict


	@staticmethod
	def _extract_classes(file_path: Path) -> dict:
		with file_path.open() as file:
			file_contents = yaml.safe_load(file)

		return file_contents["classes"]


	# @staticmethod
	# def _extract_slots_from_classes(class_dict: dict) -> dict:
	# 	slot_dict = {}
	# 	for class_name, class_definition in class_dict:
	# 		if("slots" in class_definition):
	# 			slot_dict[class_name] = class_definition["slots"]

	# 	return slot_dict


	@staticmethod
	def _get_table_slots_from_schema():
		"""Returns a dictionary containing the names of each table (keys) and a list of their slots (values)"""

		standards_schema_path = Path(TestSlotRegistration.SCHEMA_DIRECTORY + "/standards_schema.yaml")
		inheritable_classes = TestSlotRegistration._extract_classes(standards_schema_path)

		table_slots = {}

		ignore_files = [
			"standards_dataset_schema",	# incomplete - work in progress
			"standards_schema_all",		# contains only metadata, not table definitions
			"standards_schema"			# contains only parent classes (already captured in `inheritable_classes`)
		]

		for file_path in Path(TestSlotRegistration.SCHEMA_DIRECTORY).iterdir():
			if(file_path.is_file() and file_path.stem not in ignore_files):
				classes = TestSlotRegistration._extract_classes(file_path)

				# The first class is for the table itself
				table_name =  next(iter(classes))
				table_class_definition = classes[table_name]
				slot_list =  table_class_definition["slots"]

				# Check if table inherits any slots from a parent class
				parent_class_name = table_class_definition["is_a"] if "is_a" in table_class_definition else None
				if(parent_class_name and (parent_class_name in inheritable_classes) and ("slots" in inheritable_classes[parent_class_name])):
					slot_list.extend(inheritable_classes[parent_class_name]["slots"])

				table_slots[table_name] = slot_list

		return table_slots


	@staticmethod
	def _get_utilized_slots_by_table():
		"""
		Returns a dictionary of slots used by each table.
			Keys = table names
			Values = sets of slots used by each table
		"""
		slots_by_table = {}
		for file_path in Path(TestSlotRegistration.DATA_DIRECTORY).iterdir():
			if((not file_path.is_file()) or file_path.stem == "DataSet"):	# 'DataSet' is incomplete
				continue

			with file_path.open() as file:
				file_contents = yaml.safe_load(file)
			table_data = list(file_contents.values())[0]

			table_slots = set()
			table_name = file_path.stem

			for entry in table_data:
				slots = entry.keys()
				table_slots.update(slots)

			slots_by_table[table_name] = table_slots

		return slots_by_table



	def test_slot_registration(self):
		"""
		Verify that each added/modified slot has been added to all column definitions in 'modify_snyapse_schema.py'.
		This includes the enums `ColumnName` and `TableSchema`, plus the dictionary `COLUMN_TEMPLATES`
		"""

		slots_by_table = self._get_utilized_slots_by_table()

		# allowable_table_slots = TestSlotRegistration._get_table_slots_from_schema()
		ColumnName_values = [entry.value for entry in modify_synapse_schema.ColumnName]
		COLUMN_TEMPLATE_keys = list(modify_synapse_schema.COLUMN_TEMPLATES.keys())

		for table, slots in slots_by_table.items():
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
		self.table_slots_patcher = patch.object(TestSlotRegistration, '_get_utilized_slots_by_table', return_value=table_slots)
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
