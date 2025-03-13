from linkml_runtime.loaders import yaml_loader
import subprocess

DATA_DIR = "src/data"
STANDARDS_SCHEMA_FILE = "src/schema/standards_schema.yaml"
MODIFIED_SYNAPSE_SCHEMA_FILE = "path/to/modified_synapse_schema.py"

def _get_modified_yaml_files():
	"""Retrieve a list of modified YAML files using Git."""
	result = subprocess.run(["git", "diff", "--name-only", "origin/main"], capture_output=True, text=True)
	modified_files = [file for file in result.stdout.splitlines() if file.endswith(".yaml") and DATA_DIR in file]
	return modified_files


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
	added_slots = {}


	# PART 2: Check if the new slots were added to column definitions in modify_snyapse_schema.py

	# pull in modify_synapse_schema.py
	# grab the following:
		# ColumnName(Enum)
		# COLUMN_TEMPLATES
		# EACH TableSchema(Enum).{src/data/file (table) that was changed} 
	# Ensure the new column name was added in each of these places - if not, the test fails


	# PART 3: Ensure the column is in `standards_schema.yaml` > 'slots'

	# Parse standards_schema
	# Check the 'slots' entry -  If there isn't an entry for each added column, test fails

if __name__ == "__main__":
    test_slot_and_column_names()