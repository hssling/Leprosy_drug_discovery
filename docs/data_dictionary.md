# Data Dictionary

## Input Files

### leprosy_host_signature.csv

Host gene signature for leprosy, derived from published transcriptomic studies.

| Column | Type | Description |
|--------|------|-------------|
| entity | string | Gene symbol (e.g., IDO1, IL10) |
| logFC | float | Log2 fold change (leprosy vs control) |
| pval | float | P-value for differential expression |
| direction | string | "up" or "down" |

---

## Output Files

### targets_ranked_host.csv

Prioritized host targets with composite scores.

| Column | Type | Description |
|--------|------|-------------|
| gene_symbol | string | HGNC gene symbol |
| logFC | float | Log2 fold change from input |
| pval | float | P-value from input |
| direction | string | Expression direction |
| entrezgene | int | Entrez Gene ID |
| ensembl_gene | string | Ensembl Gene ID (ENSG) |
| uniprot_swissprot | string | UniProt Swiss-Prot accession |
| approvedSymbol | string | HGNC approved symbol |
| biotype | string | Gene biotype (e.g., protein_coding) |
| known_drugs_count | int | Number of drugs in Open Targets |
| tractability_entries | int | Number of tractability records |
| druggability_proxy | float | Druggability score (0-1) |
| opentargets_evidence | float | Open Targets evidence score (0-1) |
| score | float | Composite prioritization score |
| track | string | "host" for host targets |

### compounds_ranked.csv

Bioactive compounds for prioritized targets.

| Column | Type | Description |
|--------|------|-------------|
| target_chembl_id | string | ChEMBL target ID |
| molecule_chembl_id | string | ChEMBL compound ID |
| pchembl_value | float | -log10(IC50 in M) |
| standard_type | string | Assay type (IC50, EC50, Ki, Kd) |
| standard_value | float | Activity value |
| standard_units | string | Activity units |
| drug_name | string | Drug name if approved |
| max_phase | int | Maximum clinical phase (0-4) |
| target_name | string | Target protein name |
| track | string | "host" for host targets |

---

## Configuration

### pipeline.yaml

| Field | Type | Description |
|-------|------|-------------|
| project.name | string | Project identifier |
| mode.run_mode | string | "host", "pathogen", or "both" |
| inputs.signatures.host | list | Paths to host signature CSVs |
| prioritization.weights | dict | Component weights for scoring |
| compound_search.min_pchembl | float | Minimum pChEMBL threshold |
| compound_search.max_compounds_per_target | int | Max compounds per target |

---

## Units and Conventions

| Abbreviation | Full Name | Notes |
|--------------|-----------|-------|
| logFC | Log2 fold change | Positive = upregulated in leprosy |
| pChEMBL | -log10(molar IC50) | Higher = more potent |
| IC50 | Half-maximal inhibitory concentration | In molarity (M) |
| nM | Nanomolar | 10^-9 M |
| μM | Micromolar | 10^-6 M |
