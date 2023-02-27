## Add your own custom Makefile targets here

SCHEMA_FILES := standards_datastandardortool_schema.yaml \
standards_datasubstrate_schema.yaml \
standards_datatopic_schema.yaml \
standards_organization_schema.yaml \
standards_schema.yaml \
standards_schema_all.yaml \
standards_usecase_schema.yaml

GH_URL_PREFIX = https://raw.githubusercontent.com/bridge2ai/standards-schemas/main/src/standards_schemas/schema/

SCHEMA_URLS := $(foreach file,$(SCHEMA_FILES),$(GH_URL_PREFIX)$(file))

DATA_FILES := DataStandardOrTool.yaml \
DataSubstrate.yaml \
DataTopic.yaml \
Organization.yaml \
UseCase.yaml

DATA_DIR = src/data/

DATA_FILE_PATHS := $(foreach file,$(DATA_FILES),$(DATA_DIR)$(file))

DATA_CLASSES := DataStandardOrToolContainer \
DataSubstrateContainer \
DataTopicContainer \
OrganizationContainer \
UseCaseContainer

pairlist = $(if $1$2,$(firstword $1) -C $(firstword $2))

RUN = poetry run
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
validate:
	@echo "Validating..."
	$(RUN) linkml-validate -s src/schema/standards_schema_all.yaml $(call pairlist,$(DATA_FILE_PATHS), $(DATA_CLASSES))