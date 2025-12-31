# Leprosy Host-Directed Therapy Drug Discovery Pipeline

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.XXXXXXX-blue.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

## Overview

An automated computational pipeline for identifying host-directed therapy (HDT) targets and repurposable drug candidates for leprosy (Hansen's disease). This pipeline integrates multi-omics signatures with chemical databases to systematically prioritize druggable host targets.

**Author:** Dr. Siddalingaiah H S  
**Affiliation:** Shridevi Institute of Medical Sciences and Research Hospital, Tumkur, Karnataka, India  
**Email:** hssling@yahoo.com  
**ORCID:** [0000-0002-4771-8285](https://orcid.org/0000-0002-4771-8285)

## Key Findings

| Rank | Target | Score | HDT Relevance |
|------|--------|-------|---------------|
| 1 | VEGFA | 0.525 | Angiogenesis in granulomas |
| 2 | PDL1/CD274 | 0.449 | T-cell exhaustion, immune checkpoint |
| 3 | **IDO1** | 0.386 | Tryptophan catabolism, immunosuppression |
| 4 | CD38 | 0.291 | B-cell marker |
| 5 | IL10 | 0.273 | Anti-inflammatory cytokine |

**Pipeline Outputs:**
- 50 prioritized host targets
- 629 bioactive compounds (pChEMBL ≥ 6.0)
- Literature-validated targets: IDO1, PDL1, JAK2

## Installation

```bash
# Clone repository
git clone https://github.com/hssling/Leprosy_drug_discovery.git
cd Leprosy_drug_discovery

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```bash
# Run the pipeline
python -m src.pipeline --config config/pipeline.yaml

# Generate figures
python generate_figures.py
```

## Project Structure

```
Leprosy_Drug_Discovery/
├── config/
│   └── pipeline.yaml           # Pipeline configuration
├── data/
│   └── signatures/
│       └── leprosy_host_signature.csv  # Input gene signature
├── src/
│   ├── clients/                # API clients (ChEMBL, MyGene, Open Targets)
│   ├── methods/                # Analysis methods
│   └── pipeline.py             # Main pipeline script
├── outputs/
│   ├── figures/                # Publication-quality figures
│   └── tables/                 # Result CSVs
├── manuscripts/
│   ├── Manuscript_Leprosy_HDT.docx
│   └── CoverLetter_Leprosy_HDT.docx
├── docs/
│   ├── methods.md              # Detailed methods
│   └── data_dictionary.md      # Data descriptions
├── generate_figures.py         # Figure generation script
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
└── README.md                   # This file
```

## Data Sources

| Source | Description | URL |
|--------|-------------|-----|
| GEO | Leprosy transcriptomic datasets (GSE16844, GSE125943, GSE129033, GSE74481) | [ncbi.nlm.nih.gov/geo](https://www.ncbi.nlm.nih.gov/geo/) |
| MyGene.info | Gene ID mapping | [mygene.info](https://mygene.info/) |
| Open Targets | Target druggability assessment | [platform.opentargets.org](https://platform.opentargets.org/) |
| ChEMBL | Compound bioactivity data | [www.ebi.ac.uk/chembl](https://www.ebi.ac.uk/chembl/) |

## Methods

### Target Prioritization

Each gene is scored using a weighted composite:

```
Score = 0.35 × Omics_Strength 
      + 0.25 × OpenTargets_Evidence 
      + 0.20 × Druggability_Proxy 
      + 0.10 × Pathway_Centrality 
      + 0.10 × Replication
```

### Literature Validation

Top targets were validated against PubMed literature:

- **IDO1**: Upregulated in lepromatous leprosy; tryptophan depletion causes T-cell suppression
- **PDL1**: PD-1/PD-L1 interaction causes T-cell exhaustion in leprosy
- **JAK2**: Tofacitinib shown effective for chronic ENL

## Citation

If you use this pipeline, please cite:

```bibtex
@article{siddalingaiah2024leprosy,
  title={An Integrated Multi-omics Pipeline Identifies IDO1 and Immune Checkpoint 
         Inhibitors as Host-Directed Therapy Candidates for Leprosy},
  author={Siddalingaiah, H S},
  journal={PLoS Neglected Tropical Diseases},
  year={2024},
  note={Submitted}
}
```

## Related Work

- [TB Drug Discovery Pipeline](https://github.com/hssling/TB_Drug_Discovery) - Sister project for tuberculosis

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- ChEMBL team at EMBL-EBI for open-access bioactivity data
- Open Targets Platform for druggability assessments
- WHO and leprosy research community for open data sharing
