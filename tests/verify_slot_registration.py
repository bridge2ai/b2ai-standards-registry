import re
from pathlib import Path
import subprocess
from scripts.modify_synapse_schema import ColumnName, COLUMN_TEMPLATES, TableSchema

DATA_DIRECTORY = "src/data/"
STANDARDS_SCHEMA_DIRECTORY = "src/schema/"
STANDARDS_SCHEMA_FILE = STANDARDS_SCHEMA_DIRECTORY + "standards_schema.yaml"
MODIFIED_SYNAPSE_SCHEMA_FILE = "scripts/modify_synapse_schema.py"


class SlotRegistrationException(Exception):
	"""Exception raised when slots have not been properly registered in 'scripts/modify_synapse_schema.py'"""
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)


def _get_modified_data_files():
	"""Retrieve a list of modified YAML files."""
	result = subprocess.run(["git", "diff", "--name-only", "origin/main"], capture_output=True, text=True)
	modified_data_files = [file for file in result.stdout.splitlines() if file.endswith(".yaml") and DATA_DIRECTORY in file]
	return modified_data_files


def _get_modified_slots(file_path):
	"""Extract only modified slot entries from a YAML file"""
	result = subprocess.run(["git", "diff", "origin/main", "-U0", file_path], capture_output=True, text=True)
	modified_lines = result.stdout.splitlines()

	modified_slots = set()
	for line in modified_lines:
		if line.startswith("+") and not line.startswith("+++"):  # Added lines only
			# All lines will start with a '+', then a variable amount of whitespace
			# Ignore lines that have a '-' immediately after the whitespace - these lines are *not* slots
			# Capture all other lines - these are slots
			match = re.match(r"^\+\s*(?!-)([\w_]+):", line)
			slot_name = match.group(1) if match else None
			if slot_name:
				modified_slots.add(slot_name)

	return modified_slots


def main():
	# PART ONE: Determine which (if any) data files contain slots that were added or modified,
	# and capture those slots + the tables they live in
	modified_data_files = _get_modified_data_files()
	files_with_modified_slots = {}
	modified_slot_set = set()

	for file in modified_data_files:
		modified_slots = _get_modified_slots(file)
		table_name = Path(file).stem
		files_with_modified_slots[table_name] = modified_slots
		modified_slot_set.update(modified_slots)


	# PART TWO: Verify that each slot has been added to all column definitions in 'modify_snyapse_schema.py'
	# (This includes the enums 'ColumnName' and 'TableSchema', plus the dictionary 'COLUMN_TEMPLATES')

	# All slots should be registered in these places
	for slot in modified_slot_set:
		if(not slot in ColumnName):
			error_message = f"'{slot}' not in '{MODIFIED_SYNAPSE_SCHEMA_FILE}' > 'ColumnName'"
			raise SlotRegistrationException(error_message)
		elif(not ColumnName(slot) in list(COLUMN_TEMPLATES.keys())):
			error_message = f"'{slot}' not in '{MODIFIED_SYNAPSE_SCHEMA_FILE}' > 'COLUMN_TEMPLATES'"
			raise SlotRegistrationException(error_message)

	# Table-specific slot registration
	for table, modified_table_slots in files_with_modified_slots.items():
		for slot in modified_table_slots:
			if(not ColumnName(slot) in TableSchema[table].value["columns"]):
				error_message = f"'{slot}' not in '{MODIFIED_SYNAPSE_SCHEMA_FILE}' > 'TableSchema[{table}]'"
				raise SlotRegistrationException(error_message)

	return True

if __name__ == "__main__":
    main()
