## Add your own custom Makefile targets here
SHELL := /usr/bin/env bash

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
site: all-data doc-data-markdown src/all_ids.tsv
	mkdocs build ;

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

# Prepare Markdown versions of data
# Also fix links so they go the right place(s)
doc-data-markdown:
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
			newpath=$(DOCDIR)/$${newfn} ; \
			$(RUN_RENDER) -r $${CLASSES[$${key}]} -t $${format} -o $${newpath} $${key} ; \
		done \
	done
	@echo "Setting up links..."
# This is for top-level links, where there isn't a specific page
	find $(DOCDIR) -type f -name '*.markdown' -exec sed -i -e 's/(B2AI_USECASE:\([0-9]\+\))/(UseCase.markdown)/g' \
		-e 's/(B2AI_ORG:\([0-9]\+\))/(Organization.markdown)/g' \
		-e 's/(B2AI_TOPIC:\([0-9]\+\))/(DataTopic.markdown)/g' \
		-e 's/(B2AI_SUBSTRATE:\([0-9]\+\))/(DataSubstrate.markdown)/g' \
		-e 's/(B2AI_STANDARD:\([0-9]\+\))/(DataStandardOrTool.markdown)/g' {} \;
# This is for revising w3id links, since we just want internal links
	find $(DOCDIR) -type f -name '*.markdown' -exec sed -i -e 's/\(https:\/\/w3id.org\/bridge2ai\/standards-usecase-schema\/\([0-9]\+\)\)/UseCase.markdown/g' \
		-e 's/\(https:\/\/w3id.org\/bridge2ai\/standards-organization-schema\/\([0-9]\+\)\)/Organization.markdown/g' \
		-e 's/\(https:\/\/w3id.org\/bridge2ai\/standards-datatopic-schema\/\([0-9]\+\)\)/DataTopic.markdown/g' \
		-e 's/\(https:\/\/w3id.org\/bridge2ai\/standards-datasubstrate-schema\/\([0-9]\+\)\)/DataSubstrate.markdown/g' \
		-e 's/\(https:\/\/w3id.org\/bridge2ai\/standards-datastandardortool-schema\/\([0-9]\+\)\)/DataStandardOrTool.markdown/g' {} \;
# Now fix links where we want to map to a specific page
# This is messy and would probably be better as a mapping between ID and page name
	find $(DOCDIR) -type f -name '*.markdown' -exec sed -i -e 's/\[B2AI_TOPIC:1\](DataTopic.markdown)/\[B2AI_TOPIC:1\](topics\/Biology.markdown)/g' \
		-e 's/\[B2AI_TOPIC:2\](DataTopic.markdown)/\[B2AI_TOPIC:2\](topics\/Cell.markdown)/g' \
		-e 's/\[B2AI_TOPIC:3\](DataTopic.markdown)/\[B2AI_TOPIC:3\](topics\/Cheminformatics.markdown)/g' \
		-e 's/\[B2AI_TOPIC:4\](DataTopic.markdown)/\[B2AI_TOPIC:4\](topics\/ClinicalObservations.markdown)/g' \
		-e 's/\[B2AI_TOPIC:5\](DataTopic.markdown)/\[B2AI_TOPIC:5\](topics\/Data.markdown)/g' \
		-e 's/\[B2AI_TOPIC:6\](DataTopic.markdown)/\[B2AI_TOPIC:6\](topics\/Demographics.markdown)/g' \
		-e 's/\[B2AI_TOPIC:7\](DataTopic.markdown)/\[B2AI_TOPIC:7\](topics\/Disease.markdown)/g' \
		-e 's/\[B2AI_TOPIC:8\](DataTopic.markdown)/\[B2AI_TOPIC:8\](topics\/Drug.markdown)/g' \
		-e 's/\[B2AI_TOPIC:9\](DataTopic.markdown)/\[B2AI_TOPIC:9\](topics\/EHR.markdown)/g' \
		-e 's/\[B2AI_TOPIC:10\](DataTopic.markdown)/\[B2AI_TOPIC:10\](topics\/EKG.markdown)/g' \
		-e 's/\[B2AI_TOPIC:11\](DataTopic.markdown)/\[B2AI_TOPIC:11\](topics\/Environment.markdown)/g' \
		-e 's/\[B2AI_TOPIC:12\](DataTopic.markdown)/\[B2AI_TOPIC:12\](topics\/Gene.markdown)/g' \
		-e 's/\[B2AI_TOPIC:13\](DataTopic.markdown)/\[B2AI_TOPIC:13\](topics\/Genome.markdown)/g' \
		-e 's/\[B2AI_TOPIC:14\](DataTopic.markdown)/\[B2AI_TOPIC:14\](topics\/Geolocation.markdown)/g' \
		-e 's/\[B2AI_TOPIC:15\](DataTopic.markdown)/\[B2AI_TOPIC:15\](topics\/Image.markdown)/g' \
		-e 's/\[B2AI_TOPIC:16\](DataTopic.markdown)/\[B2AI_TOPIC:16\](topics\/Literature.markdown)/g' \
		-e 's/\[B2AI_TOPIC:17\](DataTopic.markdown)/\[B2AI_TOPIC:17\](topics\/Metabolome.markdown)/g' \
		-e 's/\[B2AI_TOPIC:18\](DataTopic.markdown)/\[B2AI_TOPIC:18\](topics\/mHealth.markdown)/g' \
		-e 's/\[B2AI_TOPIC:19\](DataTopic.markdown)/\[B2AI_TOPIC:19\](topics\/MicroscaleImaging.markdown)/g' \
		-e 's/\[B2AI_TOPIC:20\](DataTopic.markdown)/\[B2AI_TOPIC:20\](topics\/MolecularBiology.markdown)/g' \
		-e 's/\[B2AI_TOPIC:21\](DataTopic.markdown)/\[B2AI_TOPIC:21\](topics\/NetworksAndPathways.markdown)/g' \
		-e 's/\[B2AI_TOPIC:22\](DataTopic.markdown)/\[B2AI_TOPIC:22\](topics\/NeurologicImaging.markdown)/g' \
		-e 's/\[B2AI_TOPIC:23\](DataTopic.markdown)/\[B2AI_TOPIC:23\](topics\/Omics.markdown)/g' \
		-e 's/\[B2AI_TOPIC:24\](DataTopic.markdown)/\[B2AI_TOPIC:24\](topics\/OphthalmicImaging.markdown)/g' \
		-e 's/\[B2AI_TOPIC:25\](DataTopic.markdown)/\[B2AI_TOPIC:25\](topics\/Phenotype.markdown)/g' \
		-e 's/\[B2AI_TOPIC:26\](DataTopic.markdown)/\[B2AI_TOPIC:26\](topics\/Protein.markdown)/g' \
		-e 's/\[B2AI_TOPIC:27\](DataTopic.markdown)/\[B2AI_TOPIC:27\](topics\/ProteinStructureModel.markdown)/g' \
		-e 's/\[B2AI_TOPIC:28\](DataTopic.markdown)/\[B2AI_TOPIC:28\](topics\/Proteome.markdown)/g' \
		-e 's/\[B2AI_TOPIC:29\](DataTopic.markdown)/\[B2AI_TOPIC:29\](topics\/SDoH.markdown)/g' \
		-e 's/\[B2AI_TOPIC:30\](DataTopic.markdown)/\[B2AI_TOPIC:30\](topics\/SocialMedia.markdown)/g' \
		-e 's/\[B2AI_TOPIC:31\](DataTopic.markdown)/\[B2AI_TOPIC:31\](topics\/Survey.markdown)/g' \
		-e 's/\[B2AI_TOPIC:32\](DataTopic.markdown)/\[B2AI_TOPIC:32\](topics\/Text.markdown)/g' \
		-e 's/\[B2AI_TOPIC:33\](DataTopic.markdown)/\[B2AI_TOPIC:33\](topics\/Transcript.markdown)/g' \
		-e 's/\[B2AI_TOPIC:34\](DataTopic.markdown)/\[B2AI_TOPIC:34\](topics\/Transcriptome.markdown)/g' \
		-e 's/\[B2AI_TOPIC:35\](DataTopic.markdown)/\[B2AI_TOPIC:35\](topics\/Variant.markdown)/g' \
		-e 's/\[B2AI_TOPIC:36\](DataTopic.markdown)/\[B2AI_TOPIC:36\](topics\/Voice.markdown)/g' \
		-e 's/\[B2AI_TOPIC:37\](DataTopic.markdown)/\[B2AI_TOPIC:37\](topics\/Waveform.markdown)/g' \
		-e 's/\[B2AI_TOPIC:38\](DataTopic.markdown)/\[B2AI_TOPIC:38\](topics\/GlucoseMonitoring.markdown)/g' \
		-e 's/\[B2AI_TOPIC:39\](DataTopic.markdown)/\[B2AI_TOPIC:39\](topics\/ActivityMonitoring.markdown)/g' \
		-e 's/\[B2AI_TOPIC:40\](DataTopic.markdown)/\[B2AI_TOPIC:40\](topics\/Governance.markdown)/g' {} \;
# Finally, copy individual topic metadata to each topic page
	@echo "Copying individual topic metadata to each topic page..."
	$(CONVERT_ENTRIES_TO_PAGES)

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
		printf "  - type: markdown\n    attributes:\n      value: This is the form for requesting a new $${CLASSES[$${key}]} in the Bridge2AI Standards Registry.\n" >> $${newpath} ; \
		printf "  - type: input\n    id: name\n    attributes:\n      label: Name\n      description: What is the short name of this entity? An acronym or short phrase works best.\n      placeholder: e.g., ESM Atlas, W3C, Molecular Biology\n    validations:\n      required: true\n" >> $${newpath} ; \
		printf "  - type: input\n    id: description\n    attributes:\n      label: Description\n      description: What is the description of this entity, in a sentence or two?\n      placeholder: e.g., Any data concerning studies of the structure, function, and interactions of biological molecules.\n    validations:\n      required: true\n" >> $${newpath} ; \
		printf "  - type: input\n    id: subclass_of\n    attributes:\n      label: Subclass_Of\n      description: (Optional) Is this a subclass of another entity? Please use an identifier.\n      placeholder: e.g., \"B2AI_TOPIC:5\"\n    validations:\n      required: false\n" >> $${newpath} ; \
		printf "  - type: input\n    id: related_to\n    attributes:\n      label: Related_To\n      description: (Optional) Is this related to another entity? Please use an identifier.\n      placeholder: e.g., \"B2AI_TOPIC:5\"\n    validations:\n      required: false\n" >> $${newpath} ; \
		printf "  - type: input\n    id: contributor_name\n    attributes:\n      label: Contributor Name\n      description: What is your name? This will be used for attribution.\n      placeholder: e.g., Tabatha Butterscotch\n    validations:\n      required: true\n" >> $${newpath} ; \
		printf "  - type: input\n    id: contributor_github\n    attributes:\n      label: Contributor GitHub\n      description: What is your GitHub name, without the @ symbol?\n      placeholder: e.g., tbuttersco\n    validations:\n      required: true\n" >> $${newpath} ; \
		printf "  - type: input\n    id: contributor_orcid\n    attributes:\n      label: Contributor ORCID\n      description: What is your ORCID iD?\n      placeholder: e.g., 0000-0001-2345-6789\n    validations:\n      required: true\n" >> $${newpath} ; \
	done
