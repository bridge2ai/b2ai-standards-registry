## Add your own custom Makefile targets here
SHELL=/bin/bash

SCHEMA_FILES := standards_datastandardortool_schema.yaml \
standards_datasubstrate_schema.yaml \
standards_datatopic_schema.yaml \
standards_organization_schema.yaml \
standards_schema.yaml \
standards_schema_all.yaml \
standards_usecase_schema.yaml

ROOT_SCHEMA = src/schema/standards_schema_all.yaml

GH_URL_PREFIX = https://raw.githubusercontent.com/bridge2ai/standards-schemas/main/src/standards_schemas/schema/

SCHEMA_URLS := $(foreach file,$(SCHEMA_FILES),$(GH_URL_PREFIX)$(file))

DATA_FILES := DataStandardOrTool.yaml \
DataSubstrate.yaml \
DataTopic.yaml \
Organization.yaml \
UseCase.yaml

DATA_DIR = src/data/

DATA_FILE_PATHS := $(foreach file,$(DATA_FILES),$(DATA_DIR)$(file))

RUN = poetry run
RUN_VALIDATE = $(RUN) linkml-validate -s $(ROOT_SCHEMA)

.PHONY: clean-schemas update-schemas

# Remove old versions of schemas.
clean-schemas:
	@echo "Removing previously installed schemas"
	rm -rf src/schema

# Retrieve newest versions of schemas.
update-schemas: clean-schemas src/schema

src/schema:
	@echo "Updating schemas in src/schema"
	mkdir -p src/schema ;
	for url in $(SCHEMA_URLS) ; do \
		wget -N -P src/schema $${url} ; \
	done

# Use schemas to validate the data.
# could use IN ZIP_LISTS if this was CMake, but it isn't
# so we do a somewhat messy array instead
validate:
	@declare -A CLASSES=( ["$(DATA_DIR)DataStandardOrTool.yaml"]="DataStandardOrToolContainer" \
		["$(DATA_DIR)DataSubstrate.yaml"]="DataSubstrateContainer" \
		["$(DATA_DIR)DataTopic.yaml"]="DataTopicContainer" \
		["$(DATA_DIR)Organization.yaml"]="OrganizationContainer" \
		["$(DATA_DIR)UseCase.yaml"]="UseCaseContainer" ) \
	; for key in "$${!CLASSES[@]}" ; do \
		printf "Validating $${key}..." ; \
		$(RUN_VALIDATE) -C $${CLASSES[$${key}]} $${key} ; \
	done

gendoc: $(DOCDIR)
	$(RUN) gen-doc -d $(DOCDIR) $(SOURCE_SCHEMA_PATH)