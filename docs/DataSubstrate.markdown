# Data Substrates

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

    click B2AI_SUBSTRATE_1 "substrates/array/" "Array"
    click B2AI_SUBSTRATE_2 "substrates/associative-array/" "Associative Array"
    click B2AI_SUBSTRATE_3 "substrates/bids/" "BIDS"
    click B2AI_SUBSTRATE_4 "substrates/bigquery/" "BigQuery"
    click B2AI_SUBSTRATE_5 "substrates/column-store/" "Column Store"
    click B2AI_SUBSTRATE_6 "substrates/comma-separated-values/" "Comma-separated values"
    click B2AI_SUBSTRATE_7 "substrates/data/" "Data"
    click B2AI_SUBSTRATE_8 "substrates/data-frame/" "Data Frame"
    click B2AI_SUBSTRATE_9 "substrates/database/" "Database"
    click B2AI_SUBSTRATE_10 "substrates/delimited-text/" "Delimited Text"
    click B2AI_SUBSTRATE_11 "substrates/dicom/" "DICOM"
    click B2AI_SUBSTRATE_12 "substrates/directed-acyclic-graph/" "Directed acyclic graph"
    click B2AI_SUBSTRATE_13 "substrates/document-database/" "Document Database"
    click B2AI_SUBSTRATE_14 "substrates/graph/" "Graph"
    click B2AI_SUBSTRATE_15 "substrates/graph-database/" "Graph Database"
    click B2AI_SUBSTRATE_16 "substrates/hdf5/" "HDF5"
    click B2AI_SUBSTRATE_17 "substrates/heap/" "Heap"
    click B2AI_SUBSTRATE_18 "substrates/hierarchical-array/" "Hierarchical Array"
    click B2AI_SUBSTRATE_19 "substrates/image/" "Image"
    click B2AI_SUBSTRATE_20 "substrates/json/" "JSON"
    click B2AI_SUBSTRATE_21 "substrates/kgx-tsv/" "KGX TSV"
    click B2AI_SUBSTRATE_22 "substrates/mongodb/" "MongoDB"
    click B2AI_SUBSTRATE_23 "substrates/mysql/" "MySQL"
    click B2AI_SUBSTRATE_24 "substrates/n-dimensional-array/" "N-Dimensional Array"
    click B2AI_SUBSTRATE_25 "substrates/neo4j/" "Neo4j"
    click B2AI_SUBSTRATE_26 "substrates/neural-network-model/" "Neural Network Model"
    click B2AI_SUBSTRATE_27 "substrates/nnef/" "NNEF"
    click B2AI_SUBSTRATE_28 "substrates/onnx/" "ONNX"
    click B2AI_SUBSTRATE_29 "substrates/pandas-dataframe/" "Pandas DataFrame"
    click B2AI_SUBSTRATE_30 "substrates/parquet/" "Parquet"
    click B2AI_SUBSTRATE_31 "substrates/postgresql/" "PostgreSQL"
    click B2AI_SUBSTRATE_32 "substrates/property-graph/" "Property graph"
    click B2AI_SUBSTRATE_33 "substrates/pytorch-tensor/" "PyTorch Tensor"
    click B2AI_SUBSTRATE_34 "substrates/r-data-frame/" "R data.frame"
    click B2AI_SUBSTRATE_35 "substrates/r-tibble/" "R tibble"
    click B2AI_SUBSTRATE_36 "substrates/raster-image/" "Raster Image"
    click B2AI_SUBSTRATE_37 "substrates/relational-database/" "Relational Database"
    click B2AI_SUBSTRATE_38 "substrates/set/" "Set"
    click B2AI_SUBSTRATE_39 "substrates/string/" "String"
    click B2AI_SUBSTRATE_40 "substrates/summarizedexperiment/" "SummarizedExperiment"
    click B2AI_SUBSTRATE_41 "substrates/tab-separated-values/" "Tab-separated values"
    click B2AI_SUBSTRATE_42 "substrates/tensor/" "Tensor"
    click B2AI_SUBSTRATE_43 "substrates/text/" "Text"
    click B2AI_SUBSTRATE_44 "substrates/tree/" "Tree"
    click B2AI_SUBSTRATE_45 "substrates/trie/" "Trie"
    click B2AI_SUBSTRATE_46 "substrates/vector/" "Vector"
    click B2AI_SUBSTRATE_47 "substrates/vector-image/" "Vector Image"
    click B2AI_SUBSTRATE_48 "substrates/waveform-audio-file-format/" "Waveform Audio File Format"
    click B2AI_SUBSTRATE_49 "substrates/waveform-data/" "Waveform Data"
    click B2AI_SUBSTRATE_50 "substrates/xarray/" "xarray"
    click B2AI_SUBSTRATE_51 "substrates/zarr/" "Zarr"
    click B2AI_SUBSTRATE_52 "substrates/compressed-data/" "Compressed Data"
    click B2AI_SUBSTRATE_53 "substrates/bed/" "BED"
    click B2AI_SUBSTRATE_54 "substrates/vector-database/" "Vector Database"
    click B2AI_SUBSTRATE_55 "substrates/pinecone/" "Pinecone"
    click B2AI_SUBSTRATE_56 "substrates/immunofluorescence-image/" "Immunofluorescence Image"
    click B2AI_SUBSTRATE_57 "substrates/spectral-data/" "Spectral Data"
    click B2AI_SUBSTRATE_58 "substrates/mass-spectrometry-data/" "Mass Spectrometry Data"
    click B2AI_SUBSTRATE_59 "substrates/size-exclusion-chromatography-mass-spectrometry-data/" "Size Exclusion Chromatography-Mass Spectrometry Data"
    click B2AI_SUBSTRATE_60 "substrates/sequence/" "Sequence"
    click B2AI_SUBSTRATE_61 "substrates/dna-sequence-data/" "DNA Sequence Data"
    click B2AI_SUBSTRATE_62 "substrates/rna-sequence-data/" "RNA Sequence Data"
    click B2AI_SUBSTRATE_63 "substrates/single-cell-rna-sequence-data/" "Single-cell RNA Sequence Data"
    click B2AI_SUBSTRATE_64 "substrates/perturb-seq-data/" "Perturb-seq Data"
    click B2AI_SUBSTRATE_65 "substrates/retinal-image/" "Retinal Image"
    click B2AI_SUBSTRATE_66 "substrates/fluorescence-lifetime-imaging-ophthalmoscopy-data/" "Fluorescence Lifetime Imaging Ophthalmoscopy data"
    click B2AI_SUBSTRATE_67 "substrates/optical-coherence-tomography-data/" "Optical coherence tomography data"
    click B2AI_SUBSTRATE_68 "substrates/optical-coherence-tomography-angiography-data/" "Optical coherence tomography angiography data"
    click B2AI_SUBSTRATE_69 "substrates/time-series-data/" "Time-series data"
    click B2AI_SUBSTRATE_70 "substrates/physiological-data/" "Physiological data"
    click B2AI_SUBSTRATE_71 "substrates/heart-rate/" "Heart rate"
    click B2AI_SUBSTRATE_72 "substrates/oxygen-saturation/" "Oxygen saturation"
    click B2AI_SUBSTRATE_73 "substrates/physical-activity-data/" "Physical activity data"
    click B2AI_SUBSTRATE_74 "substrates/caloric-burn-data/" "Caloric burn data"
    click B2AI_SUBSTRATE_75 "substrates/respiratory-rate/" "Respiratory rate"
    click B2AI_SUBSTRATE_76 "substrates/sleep-tracking-data/" "Sleep tracking data"
    click B2AI_SUBSTRATE_77 "substrates/stress-tracking-data/" "Stress tracking data"
    click B2AI_SUBSTRATE_78 "substrates/glucose-monitoring-data/" "Glucose monitoring data"
    click B2AI_SUBSTRATE_79 "substrates/participant-response-data/" "Participant response data"
    click B2AI_SUBSTRATE_80 "substrates/questionnaire-response-data/" "Questionnaire response data"
    click B2AI_SUBSTRATE_81 "substrates/file-headers/" "File headers"
```
<!-- SUBSTRATE_DIAGRAM_END -->

