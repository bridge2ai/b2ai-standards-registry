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


## Where does the data in the Explorer come from?

All data in the Explorer is stored in the [Standards Registry GitHub repository](https://github.com/bridge2ai/b2ai-standards-registry).

## How are standards selected?

The standards in the registry fall into three categories:

1. Standards for structuring data used for testing, training, and validating AI models (e.g., genomics file formats and standards for EHR data such as FHIR, OMOP, and ISO).
2. Standards for describing specific datasets.
3. Standards for describing machine learning models themselves.

Where possible, existing standards are used to inform data element selection. The Registry also includes records for standards outside the scope of data modeling, such as specifications for preferred file formats, exchange protocols, and common APIs.

## Why does the Explorer list other resources, like data sets and tools?

## How may a standard be added or updated?

## Is there a schema or data model for the Explorer?

Data objects are defined according to the [standards-schemas](https://github.com/bridge2ai/standards-schemas).

The Standards Registry contains three main components: the list of standards and tools, the list of use cases, and the collection of associated metadata types (spanning organizations, data topics, and data substrates).

# What do the categories mean?

See the page on 

# What do the topics mean?

