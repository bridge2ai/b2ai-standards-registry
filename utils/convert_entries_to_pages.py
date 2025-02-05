"""Convert entries in YAML data to Markdown pages."""

import yaml
import os
import sys


def convert_entries_to_pages(input_file, output_dir):
    with open(input_file, "r") as file:
        data = yaml.safe_load(file)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Assuming a container is used
    collection = data[list(data.keys())[0]]

    for entry in collection:
        entry_name = entry["name"]
        entry_name = entry_name.replace(" ", "")
        output_file = os.path.join(output_dir, f"{entry_name}.markdown")
        with open(output_file, "w") as md_file:
            for key, value in entry.items():
                rkey = key.replace('_', ' ')
                if key in ["category", "name"]:
                    continue
                elif key in ["subclass_of", "related_to"]:
                    md_file.write(f"**{rkey}:**\n\n")
                    for v in value:
                        rv = f"[{v}](../DataTopic.markdown)"
                        md_file.write(f"- {rv}\n")
                    md_file.write("\n")
                else:
                    md_file.write(f"**{rkey}:** {value}\n\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_entries_to_pages.py <input_file> <output_dir>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    convert_entries_to_pages(input_file, output_dir)
