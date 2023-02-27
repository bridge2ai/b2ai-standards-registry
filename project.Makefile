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

RUN = poetry run
.PHONY: clean-schemas update-schemas

clean-schemas:
	@echo "Removing previously installed schemas"
	rm -rf src/schema

update-schemas: clean-schemas src/schema

src/schema:
	@echo "Updating schemas in src/schema"
	mkdir -p src/schema ;
	for url in $(SCHEMA_URLS) ; do \
		wget -N -P src/schema $${url} ; \
	done
