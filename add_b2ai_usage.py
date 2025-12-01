import yaml

TARGET_ORGS = {"B2AI_ORG:114", "B2AI_ORG:115", "B2AI_ORG:116", "B2AI_ORG:117"}
YAML_PATH = "src/data/DataStandardOrTool.yaml"

with open(YAML_PATH, "r") as f:
    data = yaml.safe_load(f)

for entry in data.get("data_standardortools_collection", []):
    orgs = entry.get("has_relevant_organization", [])
    if any(org in TARGET_ORGS for org in orgs):
        entry["used_in_bridge2ai"] = True

with open(YAML_PATH, "w") as f:
    yaml.dump(data, f, sort_keys=False, allow_unicode=True)