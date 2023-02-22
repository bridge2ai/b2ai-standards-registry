# Bridge2AI Standards Registry and Use Case Catalog

Bridge2AI Standards Registry data models, API specification, and other documentation.

Data objects are defined according to the [standards-schemas](https://github.com/bridge2ai/standards-schemas).

From the Standards Core grant proposal:

> **Aim 1.2. Inventory existing standards and create the Bridge2AI Standards Registry**
>
> We will populate a **B2AI Standards Registry** in collaboration with DGP Standards Modules, following the recommended teaming and collaboration practices of the **Teaming Core** and data transparency practices recommended by the **Ethics Core**. Broadly, the standards in the registry will fall into three categories: (1) standards for structuring data used for testing, training, and validating AI models (e.g., genomics file formats and standards for EHR data such as FHIR, OMOP, and ISO[LoS Kisler]). (2) standards for describing specific datasets (i.e., standard computable elements associated with specific data types for use in Datasheets[69]); (3) standards for describing ML models themselves (i.e., standard computable elements associated with specific ML models for use in Model Cards[70]). Coordinated use and population of this Registry will promote cross-project communication and harmonization on standard schemas and attributes. These standards will be labeled with the maturity level for each standard as determined by the Standards Core; Draft for proposed standards approved for implementation and testing, Implemented for standards that have been successfully implemented by DGPs, and Normative for consensus standards that have demonstrated cross-DGP interoperability. 
>
> The Registry will maintain attributed use cases and validation rules and examples associated with each standard or element. Where possible, existing standards (e.g., minimal information specifications[71–73]) will be used to inform data element selection. Importantly, the Registry will include records for standards outside the scope of data modeling, such as specifications for preferred file formats, exchange protocols, and common APIs. We will also annotate standards with their readiness for different forms of AI algorithms as well as developing tools for cleaning and pre-processing; for example, image data for GCNs, data frames for traditional statistical ML, linked data for graph-based ML. The Standards Registry will be linked and synchronized with existing resources such as BioPortal[74] and FAIRsharing[75].
Our Standards Registry goals are threefold: (1) ensure integration of the standards development lifecycle within the context of B2AI activities; (2) narrow the large space of standards to what is relevant; and (3) provide computational access and utilities for schemas and standards, rather than links to often outdated PDFs. We will enable programmatic access to the Registry via standardized APIs (defined via the OpenAPI specification and registered in SmartAPI[76]) to query standards metadata, elements, and validation rules.

## Repository Structure

* [src/](src/) - source files
  * [data](src/data) - data in YAML format

## Developer Documentation

### Project Generation

Use the `make` command to generate project artifacts:

* `make all`: make everything
* `make test`: test the validators
* `make validate`: validate the data
* `make deploy`: deploys site

<details>
<summary>References</summary>
  
69. Gebru T, Morgenstern J, Vecchione B, Vaughan JW, Wallach H, Daumé H III, Crawford K. Datasheets for Datasets. arXiv [cs.DB]. 2018. arxiv.org/abs/1803.09010
70. Mitchell M, Wu S, Zaldivar A, Barnes P, Vasserman L, Hutchinson B, Spitzer E, Raji ID, Gebru T. Model cards for model reporting. Proceedings of the Conference on Fairness, Accountability, and Transparency. New York, NY, USA: ACM; 2019. dl.acm.org/doi/10.1145/3287560.3287596
71. Yilmaz P, Kottmann R, Field D, Knight R, Cole JR, Amaral-Zettler L, Gilbert JA, Karsch-Mizrachi I, Johnston A, Cochrane G, Vaughan R, Hunter C, Park J, Morrison N, Rocca-Serra P, Sterk P, Arumugam M, Bailey M, Baumgartner L, Birren BW, Blaser MJ, Bonazzi V, Booth T, Bork P, Bushman FD, Buttigieg PL, Chain PSG, Charlson E, Costello EK, Huot-Creasy H, Dawyndt P, DeSantis T, Fierer N, Fuhrman JA, Gallery RE, Gevers D, Gibbs RA, San Gil I, Gonzalez A, Gordon JI, Guralnick R, Hankeln W, Highlander S, Hugenholtz P, Jansson J, Kau AL, Kelley ST, Kennedy J, Knights D, Koren O, Kuczynski J, Kyrpides N, Larsen R, Lauber CL, Legg T, Ley RE, Lozupone CA, Ludwig W, Lyons D, Maguire E, Methé BA, Meyer F, Muegge B, Nakielny S, Nelson KE, Nemergut D, Neufeld JD, Newbold LK, Oliver AE, Pace NR, Palanisamy G, Peplies J, Petrosino J, Proctor L, Pruesse E, Quast C, Raes J, Ratnasingham S, Ravel J, Relman DA, Assunta-Sansone S, Schloss PD, Schriml L, Sinha R, Smith MI, Sodergren E, Spo A, Stombaugh J, Tiedje JM, Ward DV, Weinstock GM, Wendel D, White O, Whiteley A, Wilke A, Wortman JR, Yatsunenko T, Glöckner FO. Minimum information about a marker gene sequence (MIMARKS) and minimum information about any (x) sequence (MIxS) specifications. Nat Biotechnol. 2011 May;29(5):415–420. dx.doi.org/10.1038/nbt.1823 PMCID: PMC3367316
72. Osterman TJ, Terry M, Miller RS. Improving Cancer Data Interoperability: The Promise of the Minimal Common Oncology Data Elements (mCODE) Initiative. JCO Clin Cancer Inform. 2020 Oct;4:993–1001. dx.doi.org/10.1200/CCI.20.00059 PMCID: PMC7713551
73. Ritter DI, Roychowdhury S, Roy A, Rao S, Landrum MJ, Sonkin D, Shekar M, Davis CF, Hart RK, Micheel C, Weaver M, Van Allen EM, Parsons DW, McLeod HL, Watson MS, Plon SE, Kulkarni S, Madhavan S, ClinGen Somatic Cancer Working Group. Somatic cancer variant curation and harmonization through consensus minimum variant level data. Genome Med. 2016 Nov 4;8(1):117. dx.doi.org/10.1186/s13073-016-0367-z PMCID: PMC5095986
74. Noy NF, Shah NH, Whetzel PL, Dai B, Dorf M, Griffith N, Jonquet C, Rubin DL, Storey M-A, Chute CG, Musen MA. BioPortal: ontologies and integrated data resources at the click of a mouse. Nucleic Acids Res. 2009 Jul;37(Web Server issue):W170–3. dx.doi.org/10.1093/nar/gkp440 PMCID: PMC2703982
75. Sansone S-A, McQuilton P, Rocca-Serra P, Gonzalez-Beltran A, Izzo M, Lister AL, Thurston M, FAIRsharing Community. FAIRsharing as a community approach to standards, repositories and policies. Nat Biotechnol. 2019 Apr;37(4):358–367. dx.doi.org/10.1038/s41587-019-0080-8 PMCID: PMC6785156
76. Zaveri A, Dastgheib S, Wu C, Whetzel T, Verborgh R, Avillach P, Korodi G, Terryn R, Jagodnik K, Assis P, Dumontier M. smartAPI: Towards a More Intelligent Network of Web APIs. The Semantic Web. Springer International Publishing; 2017. p. 154–169. dx.doi.org/10.1007/978-3-319-58451-5_11
  
</details>
