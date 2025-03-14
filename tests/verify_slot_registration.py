import re
import yaml
from pathlib import Path
import subprocess
from scripts.modify_synapse_schema import ColumnName, COLUMN_TEMPLATES, TableSchema

DATA_DIR = "src/data"
MODIFIED_SYNAPSE_SCHEMA_FILE = "scripts/modify_synapse_schema.py"
STANDARDS_SCHEMA_FILE = "src/schema/standards_schema.yaml"

class SlotRegistrationException(Exception):
	"""Exception raised when slots have not been properly registered in all relevant locations"""

	def __init__(self, message):
		self.message = message
		super().__init__(self.message)

def _get_modified_data_files():
	"""Retrieve a list of modified YAML files."""
	result = subprocess.run(["git", "diff", "--name-only", "origin/main"], capture_output=True, text=True)
	modified_data_files = [file for file in result.stdout.splitlines() if file.endswith(".yaml") and DATA_DIR in file]
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
	# PART ONE: Determine which (if any) data files contain slots that were added or modified, and capture those slots
	modified_data_files = _get_modified_data_files()
	files_with_modified_slots = {}
	modified_slot_set = set()

	for file in modified_data_files:
		modified_slots = _get_modified_slots(file)
		table_name = Path(file).stem
		files_with_modified_slots[table_name] = modified_slots
		modified_slot_set.update(modified_slots)


	# PART TWO:
	# 	a) Verify that each slot has been added to all column definitions in 'modify_snyapse_schema.py'
	# 		(This includes the enums 'ColumnName' and 'TableSchema', plus the dictionary 'COLUMN_TEMPLATES')
	#	b) Ensure all slots have been added to `standards_schema.yaml` > 'slots'
	with open(STANDARDS_SCHEMA_FILE, "r") as file:
		standards_schema = yaml.safe_load(file)

	registered_standards_schema_slots = standards_schema["slots"].keys()

	for slot in modified_slot_set:
		if(not slot in ColumnName):
			error_message = f"'{slot}' not in {MODIFIED_SYNAPSE_SCHEMA_FILE} > 'ColumnName'"
			raise SlotRegistrationException(error_message)
		elif(not ColumnName(slot) in list(COLUMN_TEMPLATES.keys())):
			error_message = f"'{slot}' not in {MODIFIED_SYNAPSE_SCHEMA_FILE} > 'COLUMN_TEMPLATES'"
			raise SlotRegistrationException(error_message)

		if(not slot in registered_standards_schema_slots):
			error_message = f"'{slot}' is not registered in {STANDARDS_SCHEMA_FILE}"
			raise SlotRegistrationException(error_message)

	for table, modified_table_slots in files_with_modified_slots.items():
		if(not table in TableSchema.__members__.keys()):
			error_message = f"'{table}' not in {MODIFIED_SYNAPSE_SCHEMA_FILE} > 'TableSchema"
			raise SlotRegistrationException(error_message)
		else:
			for slot in modified_table_slots:
				if(not (ColumnName(slot) if slot in ColumnName else None) in TableSchema[table].value["columns"]):
					error_message = f"'{slot}' not in {MODIFIED_SYNAPSE_SCHEMA_FILE} > 'TableSchema[{table}]'"
					raise SlotRegistrationException(error_message)

	return True

if __name__ == "__main__":
    main()
