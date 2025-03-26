import re
from pathlib import Path
import subprocess
import unittest
from scripts.modify_synapse_schema import ColumnName, COLUMN_TEMPLATES, TableSchema

class TestSlotRegistration(unittest.TestCase):
	DATA_DIRECTORY = "src/data/"
	MODIFY_SYNAPSE_SCHEMA_FILE = "scripts/modify_synapse_schema.py"

	@staticmethod
	def _get_modified_data_files():
		"""Retrieve a list of modified data files."""
		diff = subprocess.run(["git", "diff", "--name-only", "origin/main"], capture_output=True, text=True)
		return [file for file in diff.stdout.splitlines() if file.endswith(".yaml") and TestSlotRegistration.DATA_DIRECTORY in file]


	@staticmethod
	def _get_modified_slots(file_path):
		"""Extract only modified slot entries from a data file"""
		diff = subprocess.run(["git", "diff", "origin/main", "-U0", file_path], capture_output=True, text=True)
		modified_lines = diff.stdout.splitlines()

		modified_slots = set()

		for line in modified_lines:
			if line.startswith("+") and not line.startswith("+++"):  # New/modified lines
				# Lines with new/modified slots will start with a '+', then 2-4 spaces, then the slot name, then a colon
				match = re.match(r"^\+ {2,4}(\w+):", line)
				slot_name = match.group(1) if match else None
				if slot_name:
					modified_slots.add(slot_name)

		return modified_slots


	@staticmethod
	def _get_tables_with_modified_slots():
		"""Returns a dictionary containing tables with added/modified slots (keys), and a list of those slots (values)"""
		modified_data_files = TestSlotRegistration._get_modified_data_files()
		tables_with_modified_slots = {}

		for file in modified_data_files:
			table_name = Path(file).stem
			modified_slots = TestSlotRegistration._get_modified_slots(file)
			tables_with_modified_slots[table_name] = modified_slots

		return tables_with_modified_slots


	def test_slot_registration(self):
		"""
		Verify that each added/modified slot has been added to all column definitions in 'modify_snyapse_schema.py'.
		This includes the enums `ColumnName` and `TableSchema`, plus the dictionary `COLUMN_TEMPLATES`
		"""
		tables_with_modified_slots = TestSlotRegistration._get_tables_with_modified_slots()
		for table, modified_slots in tables_with_modified_slots.items():
			for slot in modified_slots:
				# All slots should be registered in these places
				self.assertTrue(slot in ColumnName, f"'{slot}' not in '{TestSlotRegistration.MODIFY_SYNAPSE_SCHEMA_FILE}' > 'ColumnName'")
				self.assertTrue(ColumnName(slot) in list(COLUMN_TEMPLATES.keys()), f"'{slot}' not in '{TestSlotRegistration.MODIFY_SYNAPSE_SCHEMA_FILE}' > 'COLUMN_TEMPLATES'")

				# Table-specific slot registration
				self.assertTrue(ColumnName(slot) in TableSchema[table].value["columns"], f"'{slot}' not in '{TestSlotRegistration.MODIFY_SYNAPSE_SCHEMA_FILE}' > 'TableSchema[{table}]'")


if __name__ == "__main__":
    unittest.main()
