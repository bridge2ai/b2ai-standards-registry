from pathlib import Path
import unittest
import yaml
from scripts.modify_synapse_schema import ColumnName, COLUMN_TEMPLATES, TableSchema

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
				self.assertTrue(slot in ColumnName, f"'{slot}' not in '{TestSlotRegistration.MODIFY_SYNAPSE_SCHEMA_FILE}' > 'ColumnName'")
				self.assertTrue(ColumnName(slot) in list(COLUMN_TEMPLATES.keys()), f"'{slot}' not in '{TestSlotRegistration.MODIFY_SYNAPSE_SCHEMA_FILE}' > 'COLUMN_TEMPLATES'")

				# Table-specific slot registration
				self.assertTrue(ColumnName(slot) in TableSchema[table].value["columns"], f"'{slot}' not in '{TestSlotRegistration.MODIFY_SYNAPSE_SCHEMA_FILE}' > 'TableSchema[{table}]'")



if __name__ == "__main__":
    unittest.main()
