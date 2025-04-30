# About the Bridge2AI Standards Explorer

The Standards Explorer is part of [**Bridge2AI**](https://bridge2ai.org/), a consortium supported by the National Institute of Health Common Fund. Bridge2AI aims to propel biomedical research forward by setting the stage for widespread adoption of artificial intelligence (AI) that tackles complex biomedical challenges beyond human intuition. See the [official site](https://bridge2ai.org/) or [this NIH page](https://commonfund.nih.gov/bridge2ai) for more details on Bridge2AI.

The Explorer is built and maintained by the [Bridge2AI Standards Working Group](https://bridge2ai.org/standards-practices-and-quality-assessment/). The Standards Working Group is focused on developing strategies to support generation of standardized, interoperable, and machine-readable data from biomedical research.

## What is the Explorer for?

The Explorer serves as an integrated knowledge base about data standards and the process of preparing data to be AI ready.

Rather than simply listing standards, however, the Explorer displays relevance of each standard to:
* The groups using it within the Bridge2AI Consortium
* Its relevant topics and data structures
* The organization(s) responsible for its creation and continued development
and other features pertinent to using the standard in practice.

Biomedical researchers may use the Explorer to rapidly determine relevance of a set of standards to their own needs while also seeing examples of how those standards have already been used in Bridge2AI projects.

Computational scientists and AI engineers may use the Explorer to learn about standards and practices used within specific domains of biomedicine, allowing them to better understand the structure and content of biomedical data.

Organizations and individuals planning to develop new methods for ensuring AI data readiness will also find the Explorer useful for characterizing the current standards ecosystem.

## What is in the Explorer?

The Explorer includes six primary types of objects, as described in the table below. Each object has a numerical identifier with a prefix defining its type (e.g., `B2AI_STANDARD:221` refers to a single standard).

| Type | Prefix | Description |
|-----------|------------|----|
|**Data Standards and Tools**| `B2AI_STANDARD` | Defined broadly, to include any formal or informal guidelines used to standardize, integrate, or otherwise make data more consistent in structure and content. It covers data standards, ontologies, controlled vocabularies, repositories, other registries, reference implementations, example datasets, software, and relevant training programs. See the page on [categories](categories.md) for more details about specific types of data standards and tools as used in the Explorer.
|**Data Sets**| `B2AI_DATA` | Data sets produced by Bridge2AI Grand Challenges.
|**Data Substrates**| `B2AI_SUBSTRATE` | A conceptual category of the structure and content of data itself. This may be interpreted as "data, in this form or format", as compared to a data standard, which refers to the set of rules defining how data is to be organized. For example, `B2AI_SUBSTRATE:9`, or Database, refers to any "organized collection of structured information, stored electronically and organized for rapid search and retrieval." Standards may define or implement specific types of Databases. Similarly, `B2AI_SUBSTRATE:11`, or DICOM, refers to images and metadata stored according to DICOM standards (`B2AI_STANDARD:98`).
|**Data Topics**| `B2AI_TOPIC` | An area of study or research focus, from the very broad (`B2AI_TOPIC:5` or Data; all Topics in the Explorer are a subclass of this) to the more specific (`B2AI_TOPIC:47` or Respiratory Disorders). These topics also include general methodologies and data collection mechanisms (e.g., `B2AI_TOPIC:38` or Glucose Monitoring).
|**Organizations**| `B2AI_ORG` | An organization related to or responsible for one or more standards. This includes all Bridge2AI Grand Challenge research groups.
|**Use Cases**| `B2AI_USECASE` | Specific use cases for standards, including standards for their expected input and outputs.

## How are standards selected?

Standards in the Explorer are curated by Bridge2AI standards members. All standards, tools, and related resources (see the description of **Data Standards and Tools** above) meeting any of the following criteria are within the scope of curation:

1. Those used or developed by Bridge2AI Grand Challenges.
2. Those used more generally in biomedical data science and biological research, to characterize the broader environment of data standards.
3. Those used in specific domains of biomedicine and biology shared by Bridge2AI Grand Challenges (e.g., ophthalmic imaging).
4. Those used with data for testing, training, and validating artificial intelligence models.

### Why does the Explorer list other resources, like data sets and tools?

Data sets, including both those produced by Bridge2AI Grand Challenges and those categorized as Reference Data or Dataset in the Explorer, serve numerous roles in the production of AI ready data. They:
* Provide examples of how data has been and is currently released
* Serve as validation sets for new methods
* Offer opportunities for comparing new data with previous observations

In addition to the criteria used for curating standards (see above), reference data, software, and other resources are included in the Explorer if they meet one of the following criteria:
* They are accompanied by standardized metadata and serve as a real-world example of that standard (e.g., [B2AI_STANDARD:690](https://b2ai.standards.synapse.org/Explore/Standard/DetailsPage?id=B2AI_STANDARD:690) is a Datasheet for a text data set; the corresponding standard is [B2AI_STANDARD:326](https://b2ai.standards.synapse.org/Explore/Standard/DetailsPage?id=B2AI_STANDARD:326), or Datasheets)
* They are very similar to data produced by Bridge2AI Grand Challenges and serve as examples of how data may have been standardized in the past. 
* They are the origin of a standard (e.g., [B2AI_STANDARD:202](https://b2ai.standards.synapse.org/Explore/Standard/DetailsPage?id=B2AI_STANDARD:202) refers to the WFDB Format, while [B2AI_STANDARD:643](https://b2ai.standards.synapse.org/Explore/Standard/DetailsPage?id=B2AI_STANDARD:643) refers to the WFDB database).
* They are in broad use within biomedical research, to the point of acting as a standard or a source of standardization.

### Is the Explorer intended to be fully comprehensive?

No. Assembling a complete collection of all standards used for all types of data may not be feasible or even possible. Instead, we have focused on resources relevant to preparing AI ready biomedical and biological data, while also capturing a broader context of the data standards landscape.

### Does the Explorer include only formal, mature standards?

No. Standards development organizations such as the International Organization for Standardization (ISO) play crucial roles in the refinement of expert-designed, formal rules for representing data (e.g., the [ISO 8601 standard](https://www.iso.org/iso-8601-date-and-time-format.html) defines a standardized format for representing date and time). Biomedical research, however, is built upon an assortment of standards varying in formality, maturity, and domain-specificity. Novel methods and approaches may require adaptation or extension of existing standards. Researchers may pursue approaches with few community-tested standards, as evidenced by our Bridge2AI Grand Challenges:

* The **Salutogenesis Grand Challenge** (also known as AI-READI) performed vision assessments with several diagnostic methods. For one method, autorefraction, no single standard existed to capture all metadata they wished to record, so AI-READI researchers [defined and documented an appropriate metadata format](https://docs.aireadi.org/docs/2/dataset/clinical-data/vision-assessment#autorefractor). They also found that, in the collection of Optical Coherence Tomography (OCT) images, several metadata fields defined by the DICOM standard could be safely removed as they either contained patient information or were inconsistent across imaging devices (see [dataset documentation on retinal OCT](https://docs.aireadi.org/docs/2/dataset/retinal-oct/)).
* The **Precision Public Health Grand Challenge** (also known as Voice as a Biomarker of Health) found that existing protocols for collecting and representing human voice recordings were highly variable and non-standard. No mature standard existed for representing voice recordings along with their relevant features and health information, nor did one for sharing recordings while preserving patient privacy (see more details in [this paper by Bensoussan et al.](https://www.isca-archive.org/interspeech_2024/bensoussan24_interspeech.html)).

## Where is Explorer data stored?

All data in the Explorer is stored in the [Standards Registry GitHub repository](https://github.com/bridge2ai/b2ai-standards-registry).

The "source of truth" for each table is stored in [YAML](https://b2ai.standards.synapse.org/Explore/Standard/DetailsPage?id=B2AI_STANDARD:393) format in the directory [src/data/](https://github.com/bridge2ai/b2ai-standards-registry/tree/main/src/data).

Corresponding versions of the tables are provided in JSON and TSV format in the directory [project/data/](https://github.com/bridge2ai/b2ai-standards-registry/tree/main/project/data).

## How may a standard be added or updated?

To submit a new data standard or other entry to the Explorer (including data topics, organizations, or others), please open an issue on the Standards Registry GitHub repository using [this form](https://github.com/bridge2ai/b2ai-standards-registry/issues/new?template=newEntity.yml).

Updates may also be requested through an issue on the same repository.

## Is there a schema or data model for the Explorer?

Data objects are defined according to the [standards-schemas](https://github.com/bridge2ai/standards-schemas).

This data model is defined in the [LinkML modeling language](https://linkml.io/).

In this repository, schema modules are stored in the [src/standards_schemas/schema/](https://github.com/bridge2ai/standards-schemas/tree/main/src/standards_schemas/schema) directory.

The schemas are also provided in JSON-LD, [JSONSchema](https://b2ai.standards.synapse.org/Explore/Standard/DetailsPage?id=B2AI_STANDARD:345), and [OWL](https://b2ai.standards.synapse.org/Explore/Standard/DetailsPage?id=B2AI_STANDARD:388) formats within the [project/](https://github.com/bridge2ai/standards-schemas/tree/main/project) directory.

## What do the categories mean?

See the page on [categories](categories.md).

## What do the topics mean?

See the page on [topics](topics.md).
