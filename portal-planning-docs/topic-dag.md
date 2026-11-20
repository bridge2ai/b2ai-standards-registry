# b2ai Topic Hierarchy — Full DAG

52 topics. 1 root (`Data`). 3 multi-parent topics (highlighted): Neurologic Imaging,
Voice Disorders, Respiratory Disorders. Max depth from any node to the root: 6.

Generated from `apps/portals/b2ai.standards/ignore/DataTopic.csv`.

```mermaid
graph LR
    Data["Data"] --> Biology["Biology"]
    Data --> Cheminformatics["Cheminformatics"]
    Data --> ClinicalObs["Clinical Observations"]
    Data --> Demographics["Demographics"]
    Data --> Disease["Disease"]
    Data --> Geolocation["Geolocation"]
    Data --> Image["Image"]
    Data --> mHealth["mHealth"]
    Data --> NetworksPathways["Networks And Pathways"]
    Data --> Phenotype["Phenotype"]
    Data --> Survey["Survey"]
    Data --> Text["Text"]
    Data --> Waveform["Waveform"]
    Data --> Governance["Governance"]

    Biology --> Environment["Environment"]
    Biology --> MolBio["Molecular Biology"]
    Biology --> Respiration["Respiration"]

    MolBio --> Cell["Cell"]
    MolBio --> Omics["Omics"]

    Cell --> Neuron["Neuron"]
    Cell --> Cardiomyocyte["Cardiomyocyte"]

    Omics --> Genome["Genome"]
    Omics --> Metabolome["Metabolome"]
    Omics --> Proteome["Proteome"]
    Omics --> Transcriptome["Transcriptome"]

    Genome --> Gene["Gene"]
    Gene --> Variant["Variant"]

    Proteome --> Protein["Protein"]
    Protein --> ProteinStruct["Protein Structure Model"]

    Transcriptome --> Transcript["Transcript"]

    Cheminformatics --> Drug["Drug"]

    ClinicalObs --> EHR["EHR"]
    ClinicalObs --> Neurology["Neurology"]
    ClinicalObs --> Psychiatry["Psychiatry"]

    Neurology --> NeurologicImaging["Neurologic Imaging"]
    Neurology --> NeurologicalDisorders["Neurological Disorders"]
    Psychiatry --> PsychiatricDisorders["Psychiatric Disorders"]

    Demographics --> SDoH["SDoH"]

    Disease --> Diabetes["Diabetes"]
    Disease --> EyeDiseases["Eye Diseases"]
    Disease --> VoiceDisorders["Voice Disorders"]
    Disease --> RespiratoryDisorders["Respiratory Disorders"]

    Image --> MicroscaleImaging["Microscale Imaging"]
    Image --> NeurologicImaging
    Image --> OphthalmicImaging["Ophthalmic Imaging"]

    mHealth --> GlucoseMonitoring["Glucose Monitoring"]
    mHealth --> ActivityMonitoring["Activity Monitoring"]

    Text --> Literature["Literature"]
    Text --> SocialMedia["Social Media"]
    Literature --> Training["Training"]

    Waveform --> EKG["EKG"]
    Waveform --> Voice["Voice"]

    Voice --> VoiceDisorders
    Respiration --> RespiratoryDisorders

    class NeurologicImaging multiparent
    class VoiceDisorders multiparent
    class RespiratoryDisorders multiparent
    classDef multiparent fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#92400e
```

## Multi-parent topics — the polyhierarchy cases

These are the only topics where the widget will render duplicate rows.

| Topic | Parents |
|-------|---------|
| Neurologic Imaging | Image, Neurology |
| Voice Disorders | Disease, Voice |
| Respiratory Disorders | Disease, Respiration |

All three are leaves (no children). When mocking the "multi-parent AND multi-child"
case (e.g. B5, B6 in `topic-hierarchy-mock.html`), the multi-child side is
**fabricated** — no real topic in this dataset has both.

## Useful subtrees for mock states

- **Single-parent path with depth + branching** — `Omics` (depth 3 from root; 4 children;
  Genome has Gene → Variant beneath it for deeper descendant demos).
- **Polyhierarchy demo** — `Neurologic Imaging`. Image is at depth 2, Neurology at depth 3
  via Clinical Observations.
- **Deepest descendant chains** — Omics → Genome → Gene → Variant (5 from root) and
  Omics → Proteome → Protein → Protein Structure Model (5 from root).
