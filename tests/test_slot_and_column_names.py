import re
from linkml_runtime.loaders import yaml_loader
from pathlib import Path
import subprocess
from scripts.modify_synapse_schema import ColumnName, COLUMN_TEMPLATES, TableSchema

DATA_DIR = "src/data"
STANDARDS_SCHEMA_FILE = "src/schema/standards_schema.yaml"
MODIFIED_SYNAPSE_SCHEMA_FILE = "path/to/modified_synapse_schema.py"

def _get_modified_yaml_files():
	"""Retrieve a list of modified YAML files using Git."""
	result = subprocess.run(["git", "diff", "--name-only", "origin/main"], capture_output=True, text=True)
	modified_files = [file for file in result.stdout.splitlines() if file.endswith(".yaml") and DATA_DIR in file]
	return modified_files

def get_modified_slots(file_path):
	"""Extract only modified slot entries from a YAML file using Git."""
	result = subprocess.run(["git", "diff", "origin/main", "-U0", file_path], capture_output=True, text=True)
	modified_lines = result.stdout.splitlines()

	modified_slots = set()
	for line in modified_lines:
		if line.startswith("+") and not line.startswith("+++"):  # Added lines only

			# Ignore lines that start with '+   -' (variable spaces between + and -) - these aren't slots
			# Otherwise, get all text between the starting '+     ' and the ":" - these are slot names
			match = re.match(r"^\+\s*(?!-)([\w_]+):", line)
			slot_name = match.group(1) if match else None

			if slot_name:
				modified_slots.add(slot_name)

	return modified_slots


def test_slot_and_column_names():
	# PART ONE: find out if a new column type was added to any file (e.g., table) in src/data

	# Use git to find which files have changes
	# initialize a dict to keep track of which files (tables) had slots added:
	# 	dict = {
	#			FileName (minus the .yaml extension): [addedSlot1, addedSlot2, ...]
	#		}
	# Check each of those for added lines
	# Parse the lines for added slot names
	# Add new slots to the dict for the appropriate file (table)
	modified_files = _get_modified_yaml_files()
	files_with_added_slots = {}
	slot_set = set()

	for file in modified_files:
		table_name = Path(file).stem
		modified_slots = get_modified_slots(file)

		files_with_added_slots[table_name] = modified_slots
		slot_set.update(modified_slots)

	# print(files_with_added_slots)
	# print(slot_set)


	# PART 2: Check if the new slots were added to column definitions in modify_snyapse_schema.py

	# pull in modify_synapse_schema.py
	# grab the following:
		# ColumnName(Enum)
		# COLUMN_TEMPLATES
		# EACH TableSchema(Enum).{src/data/file (table) that was changed}
	# Ensure the new column name was added in each of these places - if not, the test fails


	for slot in slot_set:
		print("slot:", slot)
		# print(slot in ColumnName)
		if(not slot in ColumnName):
			print(f"{slot} not in ColumnName")
		elif(not ColumnName(slot) in list(COLUMN_TEMPLATES.keys())):
			print(f"{slot} not in COLUMN_TEMPLATES")

	print("")
	for table, slots in files_with_added_slots.items():
		print(table, slots)
		for slot in slots:
			print(f"	{slot}:")
			print(f"	{table} in TableSchema => {table in TableSchema.__members__.keys()}")
			print(f"	TableSchema[table] =", TableSchema[table])
			if(not table in TableSchema.__members__.keys() or not slot in TableSchema[table].value["columns"]):
				print(f"	{slot} not in TableSchema[{table}]")


	# PART 3: Ensure the column is in `standards_schema.yaml` > 'slots'

	# Parse standards_schema
	# Check the 'slots' entry -  If there isn't an entry for each added column, test fails

if __name__ == "__main__":
    test_slot_and_column_names()
