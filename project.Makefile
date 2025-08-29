## Add your own custom Makefile targets here
SHELL := /usr/bin/env bash

SCHEMA_FILES := standards_dataset_schema.yaml \
standards_datastandardortool_schema.yaml \
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
RUN_HTML = $(RUN) python scripts/human_readable_renderer.py

SERIAL_DATA_DIR = project/data/

FORMATS = json tsv
## RENDERS = html markdown
RENDERS = markdown

ISSUE_TEMPLATE_DIR = .github/ISSUE_TEMPLATE/

CONVERT_ENTRIES_TO_PAGES = $(shell python ./utils/convert_entries_to_pages.py $(DATA_DIR)/DataTopic.yaml $(DOCDIR)/topics)
COMBINE_DATA = $(shell python ./utils/combine_data.py)

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

src/all_ids.tsv:
	$(COMBINE_DATA)
	mv all_ids.tsv src/all_ids.tsv

# This replaces the standard linkml doc builder
# since we are making docs for data,
# not the schema.
# Mkdocs reads the tsv versions.
site: all-data src/all_ids.tsv
	$(RUN) mkdocs build ;

# Use schemas to validate the data.
# could use IN ZIP_LISTS if this was CMake, but it isn't
# so we do a somewhat messy array instead
validate:
	@declare -A CLASSES=( ["$(DATA_DIR)DataStandardOrTool.yaml"]="DataStandardOrToolContainer" \
		["$(DATA_DIR)DataSubstrate.yaml"]="DataSubstrateContainer" \
		["$(DATA_DIR)DataTopic.yaml"]="DataTopicContainer" \
		["$(DATA_DIR)Organization.yaml"]="OrganizationContainer" \
		["$(DATA_DIR)UseCase.yaml"]="UseCaseContainer" \
		["$(DATA_DIR)DataSet.yaml"]="DataSetContainer" ) \
	; for key in "$${!CLASSES[@]}" ; do \
		printf "Validating $${key}..." ; \
		$(RUN_VALIDATE) -C $${CLASSES[$${key}]} $${key} ; \
	done

# Make alternative serializations of data:
# json and tsv for now
# Output goes in project/data/
all-data:
	@echo "Removing any previously created serializations..."
	rm -rf $(SERIAL_DATA_DIR) ;
	mkdir -p $(SERIAL_DATA_DIR) ;
	@echo "Making serializations with linkml-convert..."
	@( \
		declare -A CLASSES 2>/dev/null || { \
			echo ""; \
			echo "ERROR: Your bash version ($(shell bash --version | head -1)) doesn't support associative arrays."; \
			echo "This Makefile requires bash 4.0 or higher for associative arrays."; \
			echo ""; \
			echo "SOLUTION: Find or install a more recent bash and then run make like, for instance:"; \
			echo "  /opt/homebrew/bin/bash -c 'make -f project.Makefile all'"; \
			echo ""; \
			exit 1; \
		}; \
		CLASSES["$(DATA_DIR)DataStandardOrTool.yaml"]="DataStandardOrToolContainer"; \
		CLASSES["$(DATA_DIR)DataSubstrate.yaml"]="DataSubstrateContainer"; \
		CLASSES["$(DATA_DIR)DataTopic.yaml"]="DataTopicContainer"; \
		CLASSES["$(DATA_DIR)Organization.yaml"]="OrganizationContainer"; \
		CLASSES["$(DATA_DIR)UseCase.yaml"]="UseCaseContainer"; \
		CLASSES["$(DATA_DIR)DataSet.yaml"]="DataSetContainer"; \
		for key in "$${!CLASSES[@]}" ; do \
			for format in $(FORMATS) ; do \
				printf "Converting $${key} to $${format}...\n" ; \
				newfn=$${key##*/} ; \
				extension=$${newfn##*.} ; \
				newfn=$${newfn%.*}.$${format} ; \
				newpath=$(SERIAL_DATA_DIR)$${newfn} ; \
				$(RUN_CONVERT) -C $${CLASSES[$${key}]} -t $${format} -o $${newpath} $${key} ; \
			done \
		done \
	)
	@echo "Serializing D4D YAML to HTML with human_readable_renderer.py..."
	$(RUN_HTML)

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
		["$(DATA_DIR)DataSet.yaml"]="data set" \
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
		printf "  - type: markdown\n    attributes:\n      value: This is the form for requesting a new $${CLASSES[$${key}]} in the Bridge2AI Standards Registry.\n" >> $${newpath} ; \
		printf "  - type: input\n    id: name\n    attributes:\n      label: Name\n      description: What is the short name of this entity? An acronym or short phrase works best.\n      placeholder: e.g., ESM Atlas, W3C, Molecular Biology\n    validations:\n      required: true\n" >> $${newpath} ; \
		printf "  - type: input\n    id: description\n    attributes:\n      label: Description\n      description: What is the description of this entity, in a sentence or two?\n      placeholder: e.g., Any data concerning studies of the structure, function, and interactions of biological molecules.\n    validations:\n      required: true\n" >> $${newpath} ; \
		printf "  - type: input\n    id: subclass_of\n    attributes:\n      label: Subclass_Of\n      description: (Optional) Is this a subclass of another entity? Please use an identifier.\n      placeholder: e.g., \"B2AI_TOPIC:5\"\n    validations:\n      required: false\n" >> $${newpath} ; \
		printf "  - type: input\n    id: related_to\n    attributes:\n      label: Related_To\n      description: (Optional) Is this related to another entity? Please use an identifier.\n      placeholder: e.g., \"B2AI_TOPIC:5\"\n    validations:\n      required: false\n" >> $${newpath} ; \
		printf "  - type: input\n    id: contributor_name\n    attributes:\n      label: Contributor Name\n      description: What is your name? This will be used for attribution.\n      placeholder: e.g., Tabatha Butterscotch\n    validations:\n      required: true\n" >> $${newpath} ; \
		printf "  - type: input\n    id: contributor_github\n    attributes:\n      label: Contributor GitHub\n      description: What is your GitHub name, without the @ symbol?\n      placeholder: e.g., tbuttersco\n    validations:\n      required: true\n" >> $${newpath} ; \
		printf "  - type: input\n    id: contributor_orcid\n    attributes:\n      label: Contributor ORCID\n      description: What is your ORCID iD?\n      placeholder: e.g., 0000-0001-2345-6789\n    validations:\n      required: true\n" >> $${newpath} ; \
	done
