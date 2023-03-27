# Bridge2AI Standards Registry and Use Case Catalog

Bridge2AI Standards Registry data models, API specification, and other documentation.

Data objects are defined according to the [standards-schemas](https://github.com/bridge2ai/standards-schemas).

## Purpose

This Registry is assembled as part of the [Bridge2AI program](https://bridge2ai.org/). Its overall purpose is to support generation of standardized, interoperable, and machine-readable data from biomedical research.

The standards in the registry fall into three categories:

1. Standards for structuring data used for testing, training, and validating AI models (e.g., genomics file formats and standards for EHR data such as FHIR, OMOP, and ISO).
2. Standards for describing specific datasets (i.e., standard computable elements associated with specific data types for use in Datasheets<sup>1</sup>).
3. Standards for describing machine learning models themselves (i.e., standard computable elements associated with specific ML models for use in Model Cards<sup>2</sup>).

Where possible, existing standards (e.g., minimal information specifications<sup>3-5</sup>) are used to inform data element selection. The Registry also includes records for standards outside the scope of data modeling, such as specifications for preferred file formats, exchange protocols, and common APIs.

Our Standards Registry goals are threefold:

1. Ensure integration of the standards development lifecycle within the context of B2AI activities.
2. Narrow the large space of standards to what is relevant.
3. Provide computational access and utilities for schemas and standards, rather than links to often outdated PDFs. 

## Repository Structure

* [docs](docs/) - Project documentation
* [project](project/)
  * [data](project/data) - Generated data serializations.
* [src/](src/) - source files
  * [schema](src/schema) - a copy of the standards-schemas - see https://github.com/bridge2ai/standards-schemas
  * [data](src/data) - Data in YAML format

## User Documentation

### Quick Reference

The Standards Registry contains three main components: the list of standards and tools, the list of use cases, and the collection of associated metadata types (spanning organizations, data topics, and data substrates).

For a quick overview of each of these components, see the following tab-delimited files:

| Component | Location |
|-----------|----------|
| Standards Registry          | [DataStandardOrTool.tsv](project/data/DataStandardOrTool.tsv)         |
| Use Cases                   | [UseCase.tsv](project/data/UseCase.tsv)                               |
| Data Substrates             | [DataSubstrates.tsv](project/data/DataSubstrate.tsv)                  |
| Data Topics                 | [DataTopic.tsv](project/data/DataTopic.tsv)                           |
| Organizations               | [Organization.tsv](project/data/Organization.tsv)                     |

## Developer Documentation

### Project Generation

Use the `make` command to generate project artifacts:

* `make all`: make everything
* `make update-schemas`: update the standards-schemas
* `make all-data`: make data serializations
* `make test`: test the validators
* `make validate`: validate the data
* `make doc-data`: prepare Markdown and HTML versions of the data
* `make deploy`: deploys site

## Accessing Registry Data

Please see the [src/data](src/data) directory for data in YAML format or the [project/data](project/data) directory for other formats.

*TBD* - We will enable programmatic access to the Registry via standardized APIs to query standards metadata, elements, and validation rules.

<details>
<summary>References</summary>
  
1. Gebru T, Morgenstern J, Vecchione B, Vaughan JW, Wallach H, Daumé H III, Crawford K. Datasheets for Datasets. arXiv [cs.DB]. 2018. arxiv.org/abs/1803.09010
2. Mitchell M, Wu S, Zaldivar A, Barnes P, Vasserman L, Hutchinson B, Spitzer E, Raji ID, Gebru T. Model cards for model reporting. Proceedings of the Conference on Fairness, Accountability, and Transparency. New York, NY, USA: ACM; 2019. dl.acm.org/doi/10.1145/3287560.3287596
3. Yilmaz P, Kottmann R, Field D, Knight R, Cole JR, Amaral-Zettler L, Gilbert JA, Karsch-Mizrachi I, Johnston A, Cochrane G, Vaughan R, Hunter C, Park J, Morrison N, Rocca-Serra P, Sterk P, Arumugam M, Bailey M, Baumgartner L, Birren BW, Blaser MJ, Bonazzi V, Booth T, Bork P, Bushman FD, Buttigieg PL, Chain PSG, Charlson E, Costello EK, Huot-Creasy H, Dawyndt P, DeSantis T, Fierer N, Fuhrman JA, Gallery RE, Gevers D, Gibbs RA, San Gil I, Gonzalez A, Gordon JI, Guralnick R, Hankeln W, Highlander S, Hugenholtz P, Jansson J, Kau AL, Kelley ST, Kennedy J, Knights D, Koren O, Kuczynski J, Kyrpides N, Larsen R, Lauber CL, Legg T, Ley RE, Lozupone CA, Ludwig W, Lyons D, Maguire E, Methé BA, Meyer F, Muegge B, Nakielny S, Nelson KE, Nemergut D, Neufeld JD, Newbold LK, Oliver AE, Pace NR, Palanisamy G, Peplies J, Petrosino J, Proctor L, Pruesse E, Quast C, Raes J, Ratnasingham S, Ravel J, Relman DA, Assunta-Sansone S, Schloss PD, Schriml L, Sinha R, Smith MI, Sodergren E, Spo A, Stombaugh J, Tiedje JM, Ward DV, Weinstock GM, Wendel D, White O, Whiteley A, Wilke A, Wortman JR, Yatsunenko T, Glöckner FO. Minimum information about a marker gene sequence (MIMARKS) and minimum information about any (x) sequence (MIxS) specifications. Nat Biotechnol. 2011 May;29(5):415–420. dx.doi.org/10.1038/nbt.1823 PMCID: PMC3367316
4. Osterman TJ, Terry M, Miller RS. Improving Cancer Data Interoperability: The Promise of the Minimal Common Oncology Data Elements (mCODE) Initiative. JCO Clin Cancer Inform. 2020 Oct;4:993–1001. dx.doi.org/10.1200/CCI.20.00059 PMCID: PMC7713551
5. Ritter DI, Roychowdhury S, Roy A, Rao S, Landrum MJ, Sonkin D, Shekar M, Davis CF, Hart RK, Micheel C, Weaver M, Van Allen EM, Parsons DW, McLeod HL, Watson MS, Plon SE, Kulkarni S, Madhavan S, ClinGen Somatic Cancer Working Group. Somatic cancer variant curation and harmonization through consensus minimum variant level data. Genome Med. 2016 Nov 4;8(1):117. dx.doi.org/10.1186/s13073-016-0367-z PMCID: PMC5095986
  
</details>
