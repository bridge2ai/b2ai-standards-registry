# Use Cases in the Bridge2AI Standards Explorer

The Bridge2AI project defines various use cases that represent different stages and activities in biomedical data workflows. These use cases are organized into categories and show relationships through enabling dependencies.

## Use Case Categories

The colors in the diagram below represent different categories of use cases:

<div style="display: flex; flex-wrap: wrap; gap: 20px; margin: 20px 0;">
  <div style="display: flex; align-items: center; gap: 8px;">
    <div style="width: 20px; height: 20px; background-color: #e1f5fe; border: 1px solid #ccc; border-radius: 3px;"></div>
    <strong>Acquisition</strong>: Use cases focused on obtaining and collecting data from various sources
  </div>
  <div style="display: flex; align-items: center; gap: 8px;">
    <div style="width: 20px; height: 20px; background-color: #f3e5f5; border: 1px solid #ccc; border-radius: 3px;"></div>
    <strong>Integration</strong>: Use cases that combine or link data from multiple sources
  </div>
  <div style="display: flex; align-items: center; gap: 8px;">
    <div style="width: 20px; height: 20px; background-color: #e8f5e8; border: 1px solid #ccc; border-radius: 3px;"></div>
    <strong>Standardization</strong>: Use cases that establish consistent formats and quality standards
  </div>
  <div style="display: flex; align-items: center; gap: 8px;">
    <div style="width: 20px; height: 20px; background-color: #fff3e0; border: 1px solid #ccc; border-radius: 3px;"></div>
    <strong>Modeling</strong>: Use cases that develop analytical or predictive models from data
  </div>
</div>

<!-- USECASE_DIAGRAM_START -->
```mermaid
flowchart LR
    B2AI_USECASE_1["Obtain patient data from records of clinic..."]
    B2AI_USECASE_2["Obtain image data from brain magnetic reso..."]
    B2AI_USECASE_3["Obtain clinical waveform data from patients."]
    B2AI_USECASE_4["Obtain image data from retinal and other o..."]
    B2AI_USECASE_5["Obtain patient data from laboratory analys..."]
    B2AI_USECASE_6["Obtain patient data from wearable devices."]
    B2AI_USECASE_7["Obtain genomics data from patients."]
    B2AI_USECASE_8["Obtain voice data from patients."]
    B2AI_USECASE_9["Obtain social determinants of health data ..."]
    B2AI_USECASE_10["Obtain molecular proximity observations fr..."]
    B2AI_USECASE_11["Obtain proteome data from human cell samples."]
    B2AI_USECASE_12["Obtain transcriptome data from human cell ..."]
    B2AI_USECASE_13["Integrate clinical record data with voice ..."]
    B2AI_USECASE_14["Transform data from OMOP to the i2b2 stand..."]
    B2AI_USECASE_15["Produce artifacts that map identifiers bet..."]
    B2AI_USECASE_16["Link cellular objects to functions through..."]
    B2AI_USECASE_17["Standardize clinical record data collected..."]
    B2AI_USECASE_18["Standardize clinical waveform data collect..."]
    B2AI_USECASE_19["Standardize clinical image data collected ..."]
    B2AI_USECASE_20["Standardize clinical omics data collected ..."]
    B2AI_USECASE_21["Assemble standards for integrated maps of ..."]
    B2AI_USECASE_22["Assemble standards for voice data."]
    B2AI_USECASE_23["Construct standards for computational prov..."]
    B2AI_USECASE_24["Develop multi-scale maps of human cell arc..."]
    B2AI_USECASE_25["Develop models of clinical image data."]
    B2AI_USECASE_26["Develop pseudotime patient models of healt..."]
    B2AI_USECASE_27["Deploy a Federated Learning System for ana..."]
    B2AI_USECASE_28["Develop cross-sectional AI models of relat..."]
    B2AI_USECASE_29["Develop predictive models of insulin depen..."]
    B2AI_USECASE_30["Test and deploy analytical models of clini..."]
    B2AI_USECASE_31["Develop software and cloud infrastructure ..."]
    B2AI_USECASE_32["Build a database of human voice samples an..."]
    B2AI_USECASE_33["Build a relational database of arbitrary d..."]
    B2AI_USECASE_34["Query a relational database of arbitrary d..."]
    B2AI_USECASE_35["Build a graph database of arbitrary data t..."]
    B2AI_USECASE_36["Query a graph database of arbitrary data t..."]
    B2AI_USECASE_37["Train a linear regression model on data in..."]
    B2AI_USECASE_38["Train a binary classification model on dat..."]
    B2AI_USECASE_39["Train a neural network model on tensor data."]
    B2AI_USECASE_40["Transform FHIR data to TSV."]
    B2AI_USECASE_41["Determine whether enough data is available..."]
    B2AI_USECASE_42["Assess the quality of a computational mode..."]
    B2AI_USECASE_43["Assess the potential bias in a computation..."]
    B2AI_USECASE_44["Assess the explainability of a computation..."]
    B2AI_USECASE_1 --> B2AI_USECASE_5
    B2AI_USECASE_1 --> B2AI_USECASE_13
    B2AI_USECASE_1 --> B2AI_USECASE_17
    B2AI_USECASE_1 --> B2AI_USECASE_19
    B2AI_USECASE_2 --> B2AI_USECASE_19
    B2AI_USECASE_3 --> B2AI_USECASE_18
    B2AI_USECASE_4 --> B2AI_USECASE_19
    B2AI_USECASE_4 --> B2AI_USECASE_26
    B2AI_USECASE_5 --> B2AI_USECASE_17
    B2AI_USECASE_6 --> B2AI_USECASE_17
    B2AI_USECASE_6 --> B2AI_USECASE_26
    B2AI_USECASE_6 --> B2AI_USECASE_28
    B2AI_USECASE_7 --> B2AI_USECASE_20
    B2AI_USECASE_7 --> B2AI_USECASE_26
    B2AI_USECASE_7 --> B2AI_USECASE_28
    B2AI_USECASE_7 --> B2AI_USECASE_29
    B2AI_USECASE_8 --> B2AI_USECASE_13
    B2AI_USECASE_8 --> B2AI_USECASE_22
    B2AI_USECASE_8 --> B2AI_USECASE_27
    B2AI_USECASE_8 --> B2AI_USECASE_31
    B2AI_USECASE_9 --> B2AI_USECASE_17
    B2AI_USECASE_9 --> B2AI_USECASE_26
    B2AI_USECASE_9 --> B2AI_USECASE_28
    B2AI_USECASE_9 --> B2AI_USECASE_29
    B2AI_USECASE_10 --> B2AI_USECASE_16
    B2AI_USECASE_11 --> B2AI_USECASE_16
    B2AI_USECASE_12 --> B2AI_USECASE_16
    B2AI_USECASE_13 --> B2AI_USECASE_17
    B2AI_USECASE_16 --> B2AI_USECASE_24
    B2AI_USECASE_17 --> B2AI_USECASE_26
    B2AI_USECASE_17 --> B2AI_USECASE_28
    B2AI_USECASE_17 --> B2AI_USECASE_29
    B2AI_USECASE_19 --> B2AI_USECASE_25
    B2AI_USECASE_19 --> B2AI_USECASE_30
    B2AI_USECASE_22 --> B2AI_USECASE_31
    B2AI_USECASE_22 --> B2AI_USECASE_32
    B2AI_USECASE_25 --> B2AI_USECASE_30

    style B2AI_USECASE_1 fill:#e1f5fe
    style B2AI_USECASE_2 fill:#e1f5fe
    style B2AI_USECASE_3 fill:#e1f5fe
    style B2AI_USECASE_4 fill:#e1f5fe
    style B2AI_USECASE_5 fill:#e1f5fe
    style B2AI_USECASE_6 fill:#e1f5fe
    style B2AI_USECASE_7 fill:#e1f5fe
    style B2AI_USECASE_8 fill:#e1f5fe
    style B2AI_USECASE_9 fill:#e1f5fe
    style B2AI_USECASE_10 fill:#e1f5fe
    style B2AI_USECASE_11 fill:#e1f5fe
    style B2AI_USECASE_12 fill:#e1f5fe
    style B2AI_USECASE_13 fill:#f3e5f5
    style B2AI_USECASE_14 fill:#f3e5f5
    style B2AI_USECASE_15 fill:#f3e5f5
    style B2AI_USECASE_16 fill:#f3e5f5
    style B2AI_USECASE_40 fill:#f3e5f5
    style B2AI_USECASE_17 fill:#e8f5e8
    style B2AI_USECASE_18 fill:#e8f5e8
    style B2AI_USECASE_19 fill:#e8f5e8
    style B2AI_USECASE_20 fill:#e8f5e8
    style B2AI_USECASE_21 fill:#e8f5e8
    style B2AI_USECASE_22 fill:#e8f5e8
    style B2AI_USECASE_23 fill:#e8f5e8
    style B2AI_USECASE_24 fill:#fff3e0
    style B2AI_USECASE_25 fill:#fff3e0
    style B2AI_USECASE_26 fill:#fff3e0
    style B2AI_USECASE_37 fill:#fff3e0
    style B2AI_USECASE_38 fill:#fff3e0
    style B2AI_USECASE_39 fill:#fff3e0

    click B2AI_USECASE_1 "../usecases/obtain-patient-data-from-records-of-clinical-visits/" "Obtain patient data from records of clinical visits."
    click B2AI_USECASE_2 "../usecases/obtain-image-data-from-brain-magnetic-resonance-imaging/" "Obtain image data from brain magnetic resonance imaging."
    click B2AI_USECASE_3 "../usecases/obtain-clinical-waveform-data-from-patients/" "Obtain clinical waveform data from patients."
    click B2AI_USECASE_4 "../usecases/obtain-image-data-from-retinal-and-other-ophthalmic-imaging/" "Obtain image data from retinal and other ophthalmic imaging."
    click B2AI_USECASE_5 "../usecases/obtain-patient-data-from-laboratory-analysis-including-serological-testing-and-urinalysis/" "Obtain patient data from laboratory analysis, including serological testing and urinalysis."
    click B2AI_USECASE_6 "../usecases/obtain-patient-data-from-wearable-devices/" "Obtain patient data from wearable devices."
    click B2AI_USECASE_7 "../usecases/obtain-genomics-data-from-patients/" "Obtain genomics data from patients."
    click B2AI_USECASE_8 "../usecases/obtain-voice-data-from-patients/" "Obtain voice data from patients."
    click B2AI_USECASE_9 "../usecases/obtain-social-determinants-of-health-data-from-patients/" "Obtain social determinants of health data from patients."
    click B2AI_USECASE_10 "../usecases/obtain-molecular-proximity-observations-from-microscopy-images-of-human-cells/" "Obtain molecular proximity observations from microscopy images of human cells."
    click B2AI_USECASE_11 "../usecases/obtain-proteome-data-from-human-cell-samples/" "Obtain proteome data from human cell samples."
    click B2AI_USECASE_12 "../usecases/obtain-transcriptome-data-from-human-cell-populations-perturbed-through-crispr-driven-mutagenesis/" "Obtain transcriptome data from human cell populations perturbed through CRISPR-driven mutagenesis."
    click B2AI_USECASE_13 "../usecases/integrate-clinical-record-data-with-voice-data/" "Integrate clinical record data with voice data."
    click B2AI_USECASE_14 "../usecases/transform-data-from-omop-to-the-i2b2-standard/" "Transform data from OMOP to the i2b2 standard."
    click B2AI_USECASE_15 "../usecases/produce-artifacts-that-map-identifiers-between-source-and-standardized-data-representations/" "Produce artifacts that map identifiers between source and standardized data representations."
    click B2AI_USECASE_16 "../usecases/link-cellular-objects-to-functions-through-associations-between-proteins-cell-structure-proximity-and-transcriptomics/" "Link cellular objects to functions through associations between proteins, cell structure proximity, and transcriptomics."
    click B2AI_USECASE_17 "../usecases/standardize-clinical-record-data-collected-from-multiple-sites-and-sources/" "Standardize clinical record data collected from multiple sites and sources."
    click B2AI_USECASE_18 "../usecases/standardize-clinical-waveform-data-collected-from-multiple-sites-and-sources/" "Standardize clinical waveform data collected from multiple sites and sources."
    click B2AI_USECASE_19 "../usecases/standardize-clinical-image-data-collected-from-multiple-sites-and-sources/" "Standardize clinical image data collected from multiple sites and sources."
    click B2AI_USECASE_20 "../usecases/standardize-clinical-omics-data-collected-from-multiple-sites-and-sources/" "Standardize clinical omics data collected from multiple sites and sources."
    click B2AI_USECASE_21 "../usecases/assemble-standards-for-integrated-maps-of-human-cell-architecture/" "Assemble standards for integrated maps of human cell architecture."
    click B2AI_USECASE_22 "../usecases/assemble-standards-for-voice-data/" "Assemble standards for voice data."
    click B2AI_USECASE_23 "../usecases/construct-standards-for-computational-provenance/" "Construct standards for computational provenance."
    click B2AI_USECASE_24 "../usecases/develop-multi-scale-maps-of-human-cell-architecture/" "Develop multi-scale maps of human cell architecture."
    click B2AI_USECASE_25 "../usecases/develop-models-of-clinical-image-data/" "Develop models of clinical image data."
    click B2AI_USECASE_26 "../usecases/develop-pseudotime-patient-models-of-health-and-salutogenesis/" "Develop pseudotime patient models of health and salutogenesis."
    click B2AI_USECASE_27 "../usecases/deploy-a-federated-learning-system-for-analysis-of-voice-data/" "Deploy a Federated Learning System for analysis of voice data."
    click B2AI_USECASE_28 "../usecases/develop-cross-sectional-ai-models-of-relationships-between-diabetes-severity-cognitive-function-and-presence-of-biomarkers/" "Develop cross-sectional AI models of relationships between diabetes severity, cognitive function, and presence of biomarkers."
    click B2AI_USECASE_29 "../usecases/develop-predictive-models-of-insulin-dependence-and-salutogenesis/" "Develop predictive models of insulin dependence and salutogenesis."
    click B2AI_USECASE_30 "../usecases/test-and-deploy-analytical-models-of-clinical-image-data/" "Test and deploy analytical models of clinical image data."
    click B2AI_USECASE_31 "../usecases/develop-software-and-cloud-infrastructure-for-automated-voice-data-collection-through-a-smartphone-application/" "Develop software and cloud infrastructure for automated voice data collection through a smartphone application."
    click B2AI_USECASE_32 "../usecases/build-a-database-of-human-voice-samples-and-associations-with-biomarkers-of-health/" "Build a database of human voice samples and associations with biomarkers of health."
    click B2AI_USECASE_33 "../usecases/build-a-relational-database-of-arbitrary-data-types/" "Build a relational database of arbitrary data types."
    click B2AI_USECASE_34 "../usecases/query-a-relational-database-of-arbitrary-data-types/" "Query a relational database of arbitrary data types."
    click B2AI_USECASE_35 "../usecases/build-a-graph-database-of-arbitrary-data-types/" "Build a graph database of arbitrary data types."
    click B2AI_USECASE_36 "../usecases/query-a-graph-database-of-arbitrary-data-types/" "Query a graph database of arbitrary data types."
    click B2AI_USECASE_37 "../usecases/train-a-linear-regression-model-on-data-in-an-r-tibble/" "Train a linear regression model on data in an R tibble."
    click B2AI_USECASE_38 "../usecases/train-a-binary-classification-model-on-data-in-one-or-more-bioconductor-objects/" "Train a binary classification model on data in one or more Bioconductor objects."
    click B2AI_USECASE_39 "../usecases/train-a-neural-network-model-on-tensor-data/" "Train a neural network model on tensor data."
    click B2AI_USECASE_40 "../usecases/transform-fhir-data-to-tsv/" "Transform FHIR data to TSV."
    click B2AI_USECASE_41 "../usecases/determine-whether-enough-data-is-available-to-train-a-computational-model-of-interest/" "Determine whether enough data is available to train a computational model of interest."
    click B2AI_USECASE_42 "../usecases/assess-the-quality-of-a-computational-model-in-terms-of-its-ability-to-complete-a-specific-task/" "Assess the quality of a computational model in terms of its ability to complete a specific task."
    click B2AI_USECASE_43 "../usecases/assess-the-potential-bias-in-a-computational-model/" "Assess the potential bias in a computational model."
    click B2AI_USECASE_44 "../usecases/assess-the-explainability-of-a-computational-model/" "Assess the explainability of a computational model."
```
<!-- USECASE_DIAGRAM_END -->

