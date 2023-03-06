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
RUN_CONVERT = $(RUN) linkml-convert -s $(ROOT_SCHEMA)
RUN_RENDER = $(RUN) linkml-render -s $(ROOT_SCHEMA)

SERIAL_DATA_DIR = project/data/
DOCS_DATA_DIR = docs/data/

FORMATS = json tsv
RENDERS = html markdown

ISSUE_TEMPLATE_DIR = .github/ISSUE_TEMPLATE/

.PHONY: clean-schemas update-schemas validate all-data doc-data issue-templates

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

# Make alternative serializations of data:
# json and tsv for now
# Output goes in project/data/
all-data:
	@echo "Removing any previously created serializations..."
	rm -rf $(SERIAL_DATA_DIR) ;
	mkdir -p $(SERIAL_DATA_DIR) ;
	@echo "Making serializations with linkml-convert..."
	@declare -A CLASSES=( ["$(DATA_DIR)DataStandardOrTool.yaml"]="DataStandardOrToolContainer" \
		["$(DATA_DIR)DataSubstrate.yaml"]="DataSubstrateContainer" \
		["$(DATA_DIR)DataTopic.yaml"]="DataTopicContainer" \
		["$(DATA_DIR)Organization.yaml"]="OrganizationContainer" \
		["$(DATA_DIR)UseCase.yaml"]="UseCaseContainer" ) \
	; for key in "$${!CLASSES[@]}" ; do \
		for format in $(FORMATS) ; do \
			printf "Converting $${key} to $${format}...\n" ; \
			newfn=$${key##*/} ; \
			extension=$${newfn##*.} ; \
			newfn=$${newfn%.*}.$${format} ; \
			newpath=$(SERIAL_DATA_DIR)$${newfn} ; \
			$(RUN_CONVERT) -C $${CLASSES[$${key}]} -t $${format} -o $${newpath} $${key} ; \
		done \
	done

# Prepare Markdown and HTML versions of data
# Like all-data, but not really a conversion
# as much as a reformatting
doc-data:
	@echo "Removing any previously created data docs..."
	rm -rf $(DOCS_DATA_DIR) ;
	mkdir -p $(DOCS_DATA_DIR) ;
	@echo "Making data docs with linkml-renderer..."
	@declare -A CLASSES=( ["$(DATA_DIR)DataStandardOrTool.yaml"]="DataStandardOrToolContainer" \
		["$(DATA_DIR)DataSubstrate.yaml"]="DataSubstrateContainer" \
		["$(DATA_DIR)DataTopic.yaml"]="DataTopicContainer" \
		["$(DATA_DIR)Organization.yaml"]="OrganizationContainer" \
		["$(DATA_DIR)UseCase.yaml"]="UseCaseContainer" ) \
	; for key in "$${!CLASSES[@]}" ; do \
		for format in $(RENDERS) ; do \
			printf "Converting $${key} to $${format}...\n" ; \
			newfn=$${key##*/} ; \
			extension=$${newfn##*.} ; \
			newfn=$${newfn%.*}.$${format} ; \
			newpath=$(DOCS_DATA_DIR)$${newfn} ; \
			$(RUN_RENDER) -r $${CLASSES[$${key}]} -t $${format} -o $${newpath} $${key} ; \
		done \
	done

# Prepare new issue templates based off the schema.
issue-templates:
	@echo "Removing any previously created issue templates..."
	rm -rf $(ISSUE_TEMPLATE_DIR) ;
	mkdir -p $(ISSUE_TEMPLATE_DIR) ;
	@echo "Assembling issue templates..."
	@declare -A CLASSES=( ["$(DATA_DIR)DataStandardOrTool.yaml"]="data standard or tool" \
		["$(DATA_DIR)DataSubstrate.yaml"]="data substrate" \
		["$(DATA_DIR)DataTopic.yaml"]="data topic" \
		["$(DATA_DIR)Organization.yaml"]="organization" \
		["$(DATA_DIR)UseCase.yaml"]="use case" ) \
	; for key in "$${!CLASSES[@]}" ; do \
		printf "Building template for $${CLASSES[$${key}]}s...\n" ; \
		newfn=new$${key##*/} ; \
		newfn=$${newfn%.*}.yml ; \
		newpath=$(ISSUE_TEMPLATE_DIR)$${newfn} ; \
		touch $${newpath} ; \
		printf "name: Request new $${CLASSES[$${key}]}\n" >> $${newpath} ; \
		printf "description: Request addition of a new $${CLASSES[$${key}]}.\n" >> $${newpath} ; \
		printf "title: Add this new $${CLASSES[$${key}]} - [Name Here]\n" >> $${newpath} ; \
		printf "labels: [ New ]\n" >> $${newpath} ; \
		printf "assignees:\n  - caufieldjh\n" >> $${newpath} ; \
		printf "body:\n" >> $${newpath} ; \
		printf "  - type: markdown\n    attributes:\n      value: This is the form for requesting a new $${CLASSES[$${key}]} in the Bridge2AI Standards Registry." >> $${newpath} ; \
	done