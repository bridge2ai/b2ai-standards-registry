# Data Substrates in the Bridge2AI Standards Explorer

## What is a Substrate?

A Substrate is a high-level data structure or a specific implementation of that structure. Interpret as "data, in this form or format", as compared to DataStandard, which refers to the set of rules defining a standard. For example, data in TSV format is represented as a DataSubstrate but the concept of TSV format is a DataStandard.

This is also distinct from a DataTopic, which is a concept or field of study a standard may be applied to.

## Substrate Hierarchy

Below is an interactive Mermaid diagram representing a subset of the substrate hierarchy. Click any node to navigate to its page.

<!-- SUBSTRATE_DIAGRAM_START -->
```mermaid
flowchart LR
    B2AI_SUBSTRATE_1[Array]
    B2AI_SUBSTRATE_2[Associative Array]
    B2AI_SUBSTRATE_3[BIDS]
    B2AI_SUBSTRATE_4[BigQuery]
    B2AI_SUBSTRATE_5[Column Store]
    B2AI_SUBSTRATE_6[Comma-separated values]
    B2AI_SUBSTRATE_7[Data]
    B2AI_SUBSTRATE_8[Data Frame]
    B2AI_SUBSTRATE_9[Database]
    B2AI_SUBSTRATE_10[Delimited Text]
    B2AI_SUBSTRATE_11[DICOM]
    B2AI_SUBSTRATE_12[Directed acyclic graph]
    B2AI_SUBSTRATE_13[Document Database]
    B2AI_SUBSTRATE_14[Graph]
    B2AI_SUBSTRATE_15[Graph Database]
    B2AI_SUBSTRATE_16[HDF5]
    B2AI_SUBSTRATE_17[Heap]
    B2AI_SUBSTRATE_18[Hierarchical Array]
    B2AI_SUBSTRATE_19[Image]
    B2AI_SUBSTRATE_20[JSON]
    B2AI_SUBSTRATE_21[KGX TSV]
    B2AI_SUBSTRATE_22[MongoDB]
    B2AI_SUBSTRATE_23[MySQL]
    B2AI_SUBSTRATE_24[N-Dimensional Array]
    B2AI_SUBSTRATE_25[Neo4j]
    B2AI_SUBSTRATE_26[Neural Network Model]
    B2AI_SUBSTRATE_27[NNEF]
    B2AI_SUBSTRATE_28[ONNX]
    B2AI_SUBSTRATE_29[Pandas DataFrame]
    B2AI_SUBSTRATE_30[Parquet]
    B2AI_SUBSTRATE_31[PostgreSQL]
    B2AI_SUBSTRATE_32[Property graph]
    B2AI_SUBSTRATE_33[PyTorch Tensor]
    B2AI_SUBSTRATE_34[R data.frame]
    B2AI_SUBSTRATE_35[R tibble]
    B2AI_SUBSTRATE_36[Raster Image]
    B2AI_SUBSTRATE_37[Relational Database]
    B2AI_SUBSTRATE_38[Set]
    B2AI_SUBSTRATE_39[String]
    B2AI_SUBSTRATE_40[SummarizedExperiment]
    B2AI_SUBSTRATE_41[Tab-separated values]
    B2AI_SUBSTRATE_42[Tensor]
    B2AI_SUBSTRATE_43[Text]
    B2AI_SUBSTRATE_44[Tree]
    B2AI_SUBSTRATE_45[Trie]
    B2AI_SUBSTRATE_46[Vector]
    B2AI_SUBSTRATE_47[Vector Image]
    B2AI_SUBSTRATE_48[Waveform Audio File Format]
    B2AI_SUBSTRATE_49[Waveform Data]
    B2AI_SUBSTRATE_50[xarray]
    B2AI_SUBSTRATE_51[Zarr]
    B2AI_SUBSTRATE_52[Compressed Data]
    B2AI_SUBSTRATE_53[BED]
    B2AI_SUBSTRATE_54[Vector Database]
    B2AI_SUBSTRATE_55[Pinecone]
    B2AI_SUBSTRATE_56[Immunofluorescence Image]
    B2AI_SUBSTRATE_57[Spectral Data]
    B2AI_SUBSTRATE_58[Mass Spectrometry Data]
    B2AI_SUBSTRATE_59[Size Exclusion Chromatography-Mass Spectrometry Data]
    B2AI_SUBSTRATE_60[Sequence]
    B2AI_SUBSTRATE_61[DNA Sequence Data]
    B2AI_SUBSTRATE_62[RNA Sequence Data]
    B2AI_SUBSTRATE_63[Single-cell RNA Sequence Data]
    B2AI_SUBSTRATE_64[Perturb-seq Data]
    B2AI_SUBSTRATE_65[Retinal Image]
    B2AI_SUBSTRATE_66[Fluorescence Lifetime Imaging Ophthalmoscopy data]
    B2AI_SUBSTRATE_67[Optical coherence tomography data]
    B2AI_SUBSTRATE_68[Optical coherence tomography angiography data]
    B2AI_SUBSTRATE_69[Time-series data]
    B2AI_SUBSTRATE_70[Physiological data]
    B2AI_SUBSTRATE_71[Heart rate]
    B2AI_SUBSTRATE_72[Oxygen saturation]
    B2AI_SUBSTRATE_73[Physical activity data]
    B2AI_SUBSTRATE_74[Caloric burn data]
    B2AI_SUBSTRATE_75[Respiratory rate]
    B2AI_SUBSTRATE_76[Sleep tracking data]
    B2AI_SUBSTRATE_77[Stress tracking data]
    B2AI_SUBSTRATE_78[Glucose monitoring data]
    B2AI_SUBSTRATE_79[Participant response data]
    B2AI_SUBSTRATE_80[Questionnaire response data]
    B2AI_SUBSTRATE_81[File headers]
    B2AI_SUBSTRATE_1 --> B2AI_SUBSTRATE_2
    B2AI_SUBSTRATE_1 --> B2AI_SUBSTRATE_18
    B2AI_SUBSTRATE_1 --> B2AI_SUBSTRATE_24
    B2AI_SUBSTRATE_2 --> B2AI_SUBSTRATE_20
    B2AI_SUBSTRATE_5 --> B2AI_SUBSTRATE_4
    B2AI_SUBSTRATE_5 --> B2AI_SUBSTRATE_30
    B2AI_SUBSTRATE_7 --> B2AI_SUBSTRATE_1
    B2AI_SUBSTRATE_7 --> B2AI_SUBSTRATE_8
    B2AI_SUBSTRATE_7 --> B2AI_SUBSTRATE_9
    B2AI_SUBSTRATE_7 --> B2AI_SUBSTRATE_14
    B2AI_SUBSTRATE_7 --> B2AI_SUBSTRATE_19
    B2AI_SUBSTRATE_7 --> B2AI_SUBSTRATE_26
    B2AI_SUBSTRATE_7 --> B2AI_SUBSTRATE_38
    B2AI_SUBSTRATE_7 --> B2AI_SUBSTRATE_39
    B2AI_SUBSTRATE_7 --> B2AI_SUBSTRATE_42
    B2AI_SUBSTRATE_7 --> B2AI_SUBSTRATE_46
    B2AI_SUBSTRATE_7 --> B2AI_SUBSTRATE_49
    B2AI_SUBSTRATE_7 --> B2AI_SUBSTRATE_52
    B2AI_SUBSTRATE_7 --> B2AI_SUBSTRATE_57
    B2AI_SUBSTRATE_7 --> B2AI_SUBSTRATE_69
    B2AI_SUBSTRATE_7 --> B2AI_SUBSTRATE_79
    B2AI_SUBSTRATE_8 --> B2AI_SUBSTRATE_29
    B2AI_SUBSTRATE_8 --> B2AI_SUBSTRATE_34
    B2AI_SUBSTRATE_8 --> B2AI_SUBSTRATE_35
    B2AI_SUBSTRATE_9 --> B2AI_SUBSTRATE_5
    B2AI_SUBSTRATE_9 --> B2AI_SUBSTRATE_13
    B2AI_SUBSTRATE_9 --> B2AI_SUBSTRATE_15
    B2AI_SUBSTRATE_9 --> B2AI_SUBSTRATE_37
    B2AI_SUBSTRATE_9 --> B2AI_SUBSTRATE_54
    B2AI_SUBSTRATE_10 --> B2AI_SUBSTRATE_6
    B2AI_SUBSTRATE_10 --> B2AI_SUBSTRATE_41
    B2AI_SUBSTRATE_10 --> B2AI_SUBSTRATE_53
    B2AI_SUBSTRATE_13 --> B2AI_SUBSTRATE_22
    B2AI_SUBSTRATE_14 --> B2AI_SUBSTRATE_12
    B2AI_SUBSTRATE_14 --> B2AI_SUBSTRATE_15
    B2AI_SUBSTRATE_14 --> B2AI_SUBSTRATE_32
    B2AI_SUBSTRATE_14 --> B2AI_SUBSTRATE_44
    B2AI_SUBSTRATE_15 --> B2AI_SUBSTRATE_25
    B2AI_SUBSTRATE_18 --> B2AI_SUBSTRATE_16
    B2AI_SUBSTRATE_18 --> B2AI_SUBSTRATE_20
    B2AI_SUBSTRATE_18 --> B2AI_SUBSTRATE_40
    B2AI_SUBSTRATE_19 --> B2AI_SUBSTRATE_3
    B2AI_SUBSTRATE_19 --> B2AI_SUBSTRATE_36
    B2AI_SUBSTRATE_19 --> B2AI_SUBSTRATE_47
    B2AI_SUBSTRATE_24 --> B2AI_SUBSTRATE_50
    B2AI_SUBSTRATE_24 --> B2AI_SUBSTRATE_51
    B2AI_SUBSTRATE_26 --> B2AI_SUBSTRATE_27
    B2AI_SUBSTRATE_26 --> B2AI_SUBSTRATE_28
    B2AI_SUBSTRATE_32 --> B2AI_SUBSTRATE_21
    B2AI_SUBSTRATE_36 --> B2AI_SUBSTRATE_11
    B2AI_SUBSTRATE_36 --> B2AI_SUBSTRATE_56
    B2AI_SUBSTRATE_36 --> B2AI_SUBSTRATE_65
    B2AI_SUBSTRATE_37 --> B2AI_SUBSTRATE_23
    B2AI_SUBSTRATE_37 --> B2AI_SUBSTRATE_31
    B2AI_SUBSTRATE_39 --> B2AI_SUBSTRATE_43
    B2AI_SUBSTRATE_39 --> B2AI_SUBSTRATE_60
    B2AI_SUBSTRATE_41 --> B2AI_SUBSTRATE_21
    B2AI_SUBSTRATE_42 --> B2AI_SUBSTRATE_33
    B2AI_SUBSTRATE_43 --> B2AI_SUBSTRATE_10
    B2AI_SUBSTRATE_44 --> B2AI_SUBSTRATE_45
    B2AI_SUBSTRATE_49 --> B2AI_SUBSTRATE_3
    B2AI_SUBSTRATE_49 --> B2AI_SUBSTRATE_48
    B2AI_SUBSTRATE_54 --> B2AI_SUBSTRATE_55
    B2AI_SUBSTRATE_57 --> B2AI_SUBSTRATE_58
    B2AI_SUBSTRATE_58 --> B2AI_SUBSTRATE_59
    B2AI_SUBSTRATE_60 --> B2AI_SUBSTRATE_61
    B2AI_SUBSTRATE_60 --> B2AI_SUBSTRATE_62
    B2AI_SUBSTRATE_62 --> B2AI_SUBSTRATE_63
    B2AI_SUBSTRATE_63 --> B2AI_SUBSTRATE_64
    B2AI_SUBSTRATE_65 --> B2AI_SUBSTRATE_66
    B2AI_SUBSTRATE_65 --> B2AI_SUBSTRATE_67
    B2AI_SUBSTRATE_67 --> B2AI_SUBSTRATE_68
    B2AI_SUBSTRATE_69 --> B2AI_SUBSTRATE_70
    B2AI_SUBSTRATE_70 --> B2AI_SUBSTRATE_71
    B2AI_SUBSTRATE_70 --> B2AI_SUBSTRATE_72
    B2AI_SUBSTRATE_70 --> B2AI_SUBSTRATE_73
    B2AI_SUBSTRATE_70 --> B2AI_SUBSTRATE_75
    B2AI_SUBSTRATE_70 --> B2AI_SUBSTRATE_76
    B2AI_SUBSTRATE_70 --> B2AI_SUBSTRATE_77
    B2AI_SUBSTRATE_70 --> B2AI_SUBSTRATE_78
    B2AI_SUBSTRATE_73 --> B2AI_SUBSTRATE_74
    B2AI_SUBSTRATE_79 --> B2AI_SUBSTRATE_80

    click B2AI_SUBSTRATE_1 "array/" "Array"
    click B2AI_SUBSTRATE_2 "associative-array/" "Associative Array"
    click B2AI_SUBSTRATE_3 "bids/" "BIDS"
    click B2AI_SUBSTRATE_4 "bigquery/" "BigQuery"
    click B2AI_SUBSTRATE_5 "column-store/" "Column Store"
    click B2AI_SUBSTRATE_6 "comma-separated-values/" "Comma-separated values"
    click B2AI_SUBSTRATE_7 "data/" "Data"
    click B2AI_SUBSTRATE_8 "data-frame/" "Data Frame"
    click B2AI_SUBSTRATE_9 "database/" "Database"
    click B2AI_SUBSTRATE_10 "delimited-text/" "Delimited Text"
    click B2AI_SUBSTRATE_11 "dicom/" "DICOM"
    click B2AI_SUBSTRATE_12 "directed-acyclic-graph/" "Directed acyclic graph"
    click B2AI_SUBSTRATE_13 "document-database/" "Document Database"
    click B2AI_SUBSTRATE_14 "graph/" "Graph"
    click B2AI_SUBSTRATE_15 "graph-database/" "Graph Database"
    click B2AI_SUBSTRATE_16 "hdf5/" "HDF5"
    click B2AI_SUBSTRATE_17 "heap/" "Heap"
    click B2AI_SUBSTRATE_18 "hierarchical-array/" "Hierarchical Array"
    click B2AI_SUBSTRATE_19 "image/" "Image"
    click B2AI_SUBSTRATE_20 "json/" "JSON"
    click B2AI_SUBSTRATE_21 "kgx-tsv/" "KGX TSV"
    click B2AI_SUBSTRATE_22 "mongodb/" "MongoDB"
    click B2AI_SUBSTRATE_23 "mysql/" "MySQL"
    click B2AI_SUBSTRATE_24 "n-dimensional-array/" "N-Dimensional Array"
    click B2AI_SUBSTRATE_25 "neo4j/" "Neo4j"
    click B2AI_SUBSTRATE_26 "neural-network-model/" "Neural Network Model"
    click B2AI_SUBSTRATE_27 "nnef/" "NNEF"
    click B2AI_SUBSTRATE_28 "onnx/" "ONNX"
    click B2AI_SUBSTRATE_29 "pandas-dataframe/" "Pandas DataFrame"
    click B2AI_SUBSTRATE_30 "parquet/" "Parquet"
    click B2AI_SUBSTRATE_31 "postgresql/" "PostgreSQL"
    click B2AI_SUBSTRATE_32 "property-graph/" "Property graph"
    click B2AI_SUBSTRATE_33 "pytorch-tensor/" "PyTorch Tensor"
    click B2AI_SUBSTRATE_34 "r-data-frame/" "R data.frame"
    click B2AI_SUBSTRATE_35 "r-tibble/" "R tibble"
    click B2AI_SUBSTRATE_36 "raster-image/" "Raster Image"
    click B2AI_SUBSTRATE_37 "relational-database/" "Relational Database"
    click B2AI_SUBSTRATE_38 "set/" "Set"
    click B2AI_SUBSTRATE_39 "string/" "String"
    click B2AI_SUBSTRATE_40 "summarizedexperiment/" "SummarizedExperiment"
    click B2AI_SUBSTRATE_41 "tab-separated-values/" "Tab-separated values"
    click B2AI_SUBSTRATE_42 "tensor/" "Tensor"
    click B2AI_SUBSTRATE_43 "text/" "Text"
    click B2AI_SUBSTRATE_44 "tree/" "Tree"
    click B2AI_SUBSTRATE_45 "trie/" "Trie"
    click B2AI_SUBSTRATE_46 "vector/" "Vector"
    click B2AI_SUBSTRATE_47 "vector-image/" "Vector Image"
    click B2AI_SUBSTRATE_48 "waveform-audio-file-format/" "Waveform Audio File Format"
    click B2AI_SUBSTRATE_49 "waveform-data/" "Waveform Data"
    click B2AI_SUBSTRATE_50 "xarray/" "xarray"
    click B2AI_SUBSTRATE_51 "zarr/" "Zarr"
    click B2AI_SUBSTRATE_52 "compressed-data/" "Compressed Data"
    click B2AI_SUBSTRATE_53 "bed/" "BED"
    click B2AI_SUBSTRATE_54 "vector-database/" "Vector Database"
    click B2AI_SUBSTRATE_55 "pinecone/" "Pinecone"
    click B2AI_SUBSTRATE_56 "immunofluorescence-image/" "Immunofluorescence Image"
    click B2AI_SUBSTRATE_57 "spectral-data/" "Spectral Data"
    click B2AI_SUBSTRATE_58 "mass-spectrometry-data/" "Mass Spectrometry Data"
    click B2AI_SUBSTRATE_59 "size-exclusion-chromatography-mass-spectrometry-data/" "Size Exclusion Chromatography-Mass Spectrometry Data"
    click B2AI_SUBSTRATE_60 "sequence/" "Sequence"
    click B2AI_SUBSTRATE_61 "dna-sequence-data/" "DNA Sequence Data"
    click B2AI_SUBSTRATE_62 "rna-sequence-data/" "RNA Sequence Data"
    click B2AI_SUBSTRATE_63 "single-cell-rna-sequence-data/" "Single-cell RNA Sequence Data"
    click B2AI_SUBSTRATE_64 "perturb-seq-data/" "Perturb-seq Data"
    click B2AI_SUBSTRATE_65 "retinal-image/" "Retinal Image"
    click B2AI_SUBSTRATE_66 "fluorescence-lifetime-imaging-ophthalmoscopy-data/" "Fluorescence Lifetime Imaging Ophthalmoscopy data"
    click B2AI_SUBSTRATE_67 "optical-coherence-tomography-data/" "Optical coherence tomography data"
    click B2AI_SUBSTRATE_68 "optical-coherence-tomography-angiography-data/" "Optical coherence tomography angiography data"
    click B2AI_SUBSTRATE_69 "time-series-data/" "Time-series data"
    click B2AI_SUBSTRATE_70 "physiological-data/" "Physiological data"
    click B2AI_SUBSTRATE_71 "heart-rate/" "Heart rate"
    click B2AI_SUBSTRATE_72 "oxygen-saturation/" "Oxygen saturation"
    click B2AI_SUBSTRATE_73 "physical-activity-data/" "Physical activity data"
    click B2AI_SUBSTRATE_74 "caloric-burn-data/" "Caloric burn data"
    click B2AI_SUBSTRATE_75 "respiratory-rate/" "Respiratory rate"
    click B2AI_SUBSTRATE_76 "sleep-tracking-data/" "Sleep tracking data"
    click B2AI_SUBSTRATE_77 "stress-tracking-data/" "Stress tracking data"
    click B2AI_SUBSTRATE_78 "glucose-monitoring-data/" "Glucose monitoring data"
    click B2AI_SUBSTRATE_79 "participant-response-data/" "Participant response data"
    click B2AI_SUBSTRATE_80 "questionnaire-response-data/" "Questionnaire response data"
    click B2AI_SUBSTRATE_81 "file-headers/" "File headers"
```
<!-- SUBSTRATE_DIAGRAM_END -->
