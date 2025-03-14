import re
import yaml
from pathlib import Path
import subprocess
from scripts.modify_synapse_schema import ColumnName, COLUMN_TEMPLATES, TableSchema

DATA_DIR = "src/data"
MODIFIED_SYNAPSE_SCHEMA_FILE = "path/to/modified_synapse_schema.py"
STANDARDS_SCHEMA_FILE = "src/schema/standards_schema.yaml"

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


def verify_slot_registration():
	# PART ONE: find out if a column (slot) was added or modified in any data file (e.g., table)
	modified_data_files = _get_modified_data_files()
	files_with_added_slots = {}
	slot_set = set()

	for file in modified_data_files:
		modified_slots = _get_modified_slots(file)
		table_name = Path(file).stem
		files_with_added_slots[table_name] = modified_slots
		slot_set.update(modified_slots)


	# PART TWO:
	# 	a) Verify that each slot has been added to all column definitions in 'modify_snyapse_schema.py'
	# 		(This includes the enums 'ColumnName' and 'TableSchema', plus the dictionary 'COLUMN_TEMPLATES')
	#	b) Ensure all slots have been added to `standards_schema.yaml` > 'slots'
	with open(STANDARDS_SCHEMA_FILE, "r") as file:
		standards_schema = yaml.safe_load(file)

	registered_slots = standards_schema["slots"].keys()

	for slot in slot_set:
		if(not slot in ColumnName):
			print(f"'{slot}' not in `ColumnName`")
		elif(not ColumnName(slot) in list(COLUMN_TEMPLATES.keys())):
			print(f"'{slot}' not in `COLUMN_TEMPLATES`")

		if(not slot in registered_slots):
			print(f"'{slot}' is not registered in 'standards_schema.yaml'")

	print("")
	for table, table_slots in files_with_added_slots.items():
		if(not table in TableSchema.__members__.keys()):
			print(f"'{table}' not in 'TableSchema")
		else:
			for slot in table_slots:
				if(not slot in TableSchema[table].value["columns"]):
					print(f"'{slot}' not in `TableSchema[{table}]`")

if __name__ == "__main__":
    verify_slot_registration()
