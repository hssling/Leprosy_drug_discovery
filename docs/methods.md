# Detailed Methods

## Overview

This document describes the computational methods used in the Leprosy Host-Directed Therapy (HDT) Drug Discovery Pipeline.

## Data Collection

### Host Gene Signatures

A 50-gene leprosy signature was curated from published literature and GEO datasets:

| GEO Accession | Sample Type | Comparison | Reference |
|---------------|-------------|------------|-----------|
| GSE16844 | Skin lesions | Leprosy vs. Control | Belone et al. |
| GSE125943 | Whole blood | Leprosy reactions | IJDVL study |
| GSE129033 | PBMCs | Lepromatous vs. Tuberculoid | Frontiers study |
| GSE74481 | Skin | Immune reactions | Published 2016 |

### Gene Selection Criteria

Genes were selected based on:
1. Consistent differential expression (|logFC| ≥ 1.0)
2. Statistical significance (adjusted p-value < 0.05)
3. Biological relevance to leprosy immunopathology

## Pipeline Architecture

### Step 1: Gene ID Mapping

**Tool:** MyGene.info API

Converts gene symbols to standardized identifiers:
- Ensembl Gene IDs (ENSG)
- UniProt accession numbers

### Step 2: Druggability Assessment

**Tool:** Open Targets Platform API

For each target, retrieves:
- Tractability scores (small molecule, antibody, other modalities)
- Clinical phase information
- Disease associations

### Step 3: Compound Mining

**Tool:** ChEMBL Database (v33)

Retrieves compounds with:
- Validated bioactivity data
- pChEMBL ≥ 6.0 (≤ 1 μM potency)
- Defined mechanism of action

## Target Scoring Algorithm

### Composite Score Formula

```
Composite Score = 0.35 × Omics_Strength 
                + 0.25 × OpenTargets_Evidence 
                + 0.20 × Druggability_Proxy 
                + 0.10 × Pathway_Centrality 
                + 0.10 × Replication
```

### Component Definitions

| Component | Definition | Range |
|-----------|------------|-------|
| Omics_Strength | min(|logFC|/2, 1) × (1 - p-value) | 0-1 |
| OpenTargets_Evidence | Normalized tractability score | 0-1 |
| Druggability_Proxy | min(compound_count/100, 1) | 0-1 |
| Pathway_Centrality | Centrality in PPI networks | 0-1 |
| Replication | Cross-study consistency | 0-1 |

## Compound Filtering

### pChEMBL Threshold

The pChEMBL value is defined as:
```
pChEMBL = -log₁₀(IC₅₀ in M)
```

| pChEMBL | IC₅₀ | Activity Class |
|---------|------|----------------|
| 6.0 | 1 μM | Active |
| 7.0 | 100 nM | Potent |
| 8.0 | 10 nM | Highly potent |
| 9.0 | 1 nM | Sub-nanomolar |

### Quality Filters

- Validated assay data only
- Excludes failed compounds
- Includes clinical phase information

## Literature Validation

### Search Strategy

For each top-ranked target, PubMed was searched:
```
("[gene symbol]" OR "[protein name]") AND ("leprosy" OR "M. leprae" OR "Hansen")
```

### Validated Targets

| Target | PubMed Evidence | Key Finding |
|--------|-----------------|-------------|
| IDO1 | de Mattos Barbosa 2017 | Tryptophan depletion in lepromatous leprosy |
| PDL1 | Palermo 2012 | PD-1+ T cells in lepromatous lesions |
| JAK2 | Thangaraju 2020 | Tofacitinib for chronic ENL |

## Reproducibility

### Software Requirements

- Python 3.12+
- pandas, matplotlib, seaborn
- requests (for API calls)

### Random Seed

No random processes are used in the pipeline; results are fully deterministic.

### API Rate Limits

- MyGene.info: 1000 requests/minute
- ChEMBL: 60 requests/minute
- Open Targets: 100 requests/minute
