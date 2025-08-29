# Topics in the Bridge2AI Standards Explorer

The following topics are used in the Standards Explorer:

## Topic Hierarchy

Below is an interactive Mermaid diagram representing a subset of the topic hierarchy. Click any node to navigate to its page.

```mermaid
flowchart LR
     %% Core root
        DATA([Data]):::topic

        %% High-level branches
        DATA --> BIO(Biology)
        DATA --> CLINOBS(Clinical Observations)
        DATA --> DEMO(Demographics)
        DATA --> IMAGE(Image)
        DATA --> PHENO(Phenotype)
        DATA --> TEXT(Text)
        DATA --> WAVE(Waveform)
        DATA --> NETPATH("Networks and Pathways")
        DATA --> GOV(Governance)
        DATA --> MH(mHealth)
        DATA --> GEO(Geolocation)
        DATA --> DISEASE(Disease)
        DATA --> SURVEY(Survey)
        DATA --> ENV(Environment)
        DATA --> CHEM(Cheminformatics)

        %% Molecular / omics branch
        BIO --> MOLBIO("Molecular Biology")
        MOLBIO --> OMICS(Omics)
        OMICS --> GENOME(Genome)
        OMICS --> PROTEOME(Proteome)
        OMICS --> METAB(Metabolome)
        OMICS --> TRANSCRIPTOME(Transcriptome)
        TRANSCRIPTOME --> TRANSCRIPT(Transcript)
        GENOME --> GENE(Gene)
        GENE --> VARIANT(Variant)
        PROTEOME --> PROTEIN(Protein)
        PROTEIN --> PROTEIN_STRUCT("Protein Structure Model")

        %% Cellular / physiology
        BIO --> CELL(Cell)
        CELL --> NEURON(Neuron)
        CELL --> CARDIO(Cardiomyocyte)
        BIO --> RESP(Respiration)

        %% Imaging
        IMAGE --> MICROIMG("Microscale Imaging")
        IMAGE --> NEUROIMG("Neurologic Imaging")
        IMAGE --> OPHTHIMG("Ophthalmic Imaging")

        %% Clinical observation sub-areas
        CLINOBS --> EHR(EHR)
        CLINOBS --> NEURO(Neurology)
        NEURO --> NEURODIS("Neurological Disorders")
        CLINOBS --> PSYCH(Psychiatry)
        PSYCH --> PSYCHDIS("Psychiatric Disorders")

        %% Mobile / monitoring
        MH --> ACTMON("Activity Monitoring")
        MH --> GLUCOSE("Glucose Monitoring")

        %% Waveforms / voice
        WAVE --> VOICE(Voice)

        %% Social determinants (multi-parent shown via dashed helpers)
        DEMO --> SDOH(SDoH)
        ENV --> SDOH
        GEO --> SDOH

        %% Disease specializations
        DISEASE --> EYE("Eye Diseases")
        DISEASE --> DIAB(Diabetes)
        DISEASE --> RESP_DIS("Respiratory Disorders")
        DISEASE --> VOICEDIS("Voice Disorders")

        %% Chemistry / drugs
        CHEM --> DRUG(Drug)

        %% Text related
        TEXT --> LIT(Literature)
        TEXT --> SOCIAL("Social Media")
        LIT --> TRAIN(Training)

        classDef topic fill:#eef4ff,stroke:#4a3b8f,stroke-width:1px,rx:4,ry:4;

        %% Click interactions
        click DATA "Data/" "Data"
        click BIO "Biology/" "Biology"
        click CLINOBS "ClinicalObservations/" "Clinical Observations"
        click DEMO "Demographics/" "Demographics"
        click PHENO "Phenotype/" "Phenotype"
        click IMAGE "Image/" "Image"
        click MICROIMG "MicroscaleImaging/" "Microscale Imaging"
        click NEUROIMG "NeurologicImaging/" "Neurologic Imaging"
        click OPHTHIMG "OphthalmicImaging/" "Ophthalmic Imaging"
        click LIT "Literature/" "Literature"
        click TEXT "Text/" "Text"
        click TRAIN "Training/" "Training"
        click MH "mHealth/" "mHealth"
        click ACTMON "ActivityMonitoring/" "Activity Monitoring"
        click GLUCOSE "GlucoseMonitoring/" "Glucose Monitoring"
        click WAVE "Waveform/" "Waveform"
        click VOICE "Voice/" "Voice"
        click ENV "Environment/" "Environment"
        click GEO "Geolocation/" "Geolocation"
        click GOV "Governance/" "Governance"
        click MOLBIO "MolecularBiology/" "Molecular Biology"
        click OMICS "Omics/" "Omics"
        click GENOME "Genome/" "Genome"
        click GENE "Gene/" "Gene"
        click VARIANT "Variant/" "Variant"
        click PROTEOME "Proteome/" "Proteome"
        click PROTEIN "Protein/" "Protein"
        click PROTEIN_STRUCT "ProteinStructureModel/" "Protein Structure Model"
        click METAB "Metabolome/" "Metabolome"
        click TRANSCRIPTOME "Transcriptome/" "Transcriptome"
        click TRANSCRIPT "Transcript/" "Transcript"
        click EHR "EHR/" "EHR"
        click NEURO "Neurology/" "Neurology"
        click NEURODIS "NeurologicalDisorders/" "Neurological Disorders"
        click PSYCH "Psychiatry/" "Psychiatry"
        click PSYCHDIS "PsychiatricDisorders/" "Psychiatric Disorders"
        click DISEASE "Disease/" "Disease"
        click DIAB "Diabetes/" "Diabetes"
        click RESP_DIS "RespiratoryDisorders/" "Respiratory Disorders"
        click EYE "EyeDiseases/" "Eye Diseases"
        click VOICEDIS "VoiceDisorders/" "Voice Disorders"
        click DRUG "Drug/" "Drug"
        click CHEM "Cheminformatics/" "Cheminformatics"
        click SURVEY "Survey/" "Survey"
        click CELL "Cell/" "Cell"
        click NEURON "Neuron/" "Neuron"
        click CARDIO "Cardiomyocyte/" "Cardiomyocyte"
        click RESP "Respiration/" "Respiration"
        click SOCIAL "SocialMedia/" "Social Media"
        click SDOH "SDoH/" "Social Determinants of Health"
        click NETPATH "NetworksAndPathways/" "Networks and Pathways"
```

> Note: For readability, some cross-links (e.g., multi-parent relationships) are not shown.
