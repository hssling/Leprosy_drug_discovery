# Multi-omics Pipeline Identifies Host-Directed Therapy Candidates for Leprosy: IDO1 and JAK2 as Priority Targets

**Running Head:** HDT Candidates for Leprosy

---

## TITLE PAGE

**Title:** An Integrated Multi-omics Pipeline Identifies IDO1 and Immune Checkpoint Inhibitors as Host-Directed Therapy Candidates for Leprosy

**Authors:** Siddalingaiah H S^1^

**Affiliations:** ^1^Department of Community Medicine, Shridevi Institute of Medical Sciences and Research Hospital, Tumkur, Karnataka, India

**Corresponding Author:**
Dr Siddalingaiah H S, Professor, Department of Community Medicine, Shridevi Institute of Medical Sciences and Research Hospital, Tumkur – 572106, Karnataka, India. Email: hssling@yahoo.com; Phone: +91-8941087719; ORCID: 0000-0002-4771-8285

**Word Count:** ~2,400 words (excluding abstract, references, tables)

**Conflicts of Interest:** None declared.

**Funding:** None.

---

## SUMMARY

**BACKGROUND:** Leprosy, caused by Mycobacterium leprae, remains endemic in several tropical countries. Despite effective multidrug therapy (MDT), host immune dysregulation contributes to nerve damage and leprosy reactions. Host-Directed Therapies (HDTs) offer a complementary approach to modulate immune responses and prevent disability.

**OBJECTIVE:** To systematically identify druggable host targets and repurposable drug candidates for leprosy using an automated computational pipeline integrating multi-omics signatures with chemical databases.

**METHODS:** We integrated transcriptomic signatures from published leprosy gene expression studies comprising 50 genes associated with differential host responses. The Python-based pipeline utilized MyGene.info for gene normalization, the Open Targets Platform for druggability assessment, and ChEMBL database for compound mining. Compounds were filtered for validated bioactivity (pChEMBL greater than 6.0).

**RESULTS:** Fifty host targets were prioritized based on composite scoring. VEGFA, PDL1/CD274, IDO1, CD38, and IL10 ranked highest (scores 0.53-0.27). Among 629 compounds identified for overlapping targets with tuberculosis, multiple clinically advanced drugs were identified including immune checkpoint inhibitors and JAK inhibitors. IDO1 inhibitors and PD-1/PD-L1 blockers emerged as promising candidates given their validated roles in leprosy immunopathology.

**CONCLUSION:** This pipeline successfully identified IDO1, PDL1, and JAK2 as high-priority HDT targets for leprosy. IDO1 inhibition may reverse tolerogenic immunosuppression, while PD-1/PD-L1 blockade could restore T-cell function. These findings support developing adjunctive immunotherapies for leprosy beyond conventional MDT.

**KEYWORDS:** leprosy; host-directed therapy; IDO1; PD-L1; immune checkpoint; drug repurposing; JAK2.

---

## INTRODUCTION

Leprosy (Hansen's disease), caused by Mycobacterium leprae, affects approximately 200,000 new cases annually worldwide, with India, Brazil, and Indonesia accounting for over 80% of the global burden.^1^ Despite the availability of effective multidrug therapy (MDT), leprosy continues to cause significant morbidity through irreversible nerve damage and disfiguring skin lesions. The clinical spectrum of leprosy—from tuberculoid (TT) to lepromatous (LL) forms—reflects varying degrees of host immune competence against the pathogen.^2^

A critical challenge in leprosy management is the occurrence of leprosy reactions, including Type 1 reactions (reversal reactions) and Type 2 reactions (erythema nodosum leprosum, ENL), which are immunologically mediated inflammatory episodes causing acute nerve damage.^3^ Standard treatment with corticosteroids and thalidomide has significant adverse effects and limited efficacy. This highlights the urgent need for novel therapeutic strategies that can modulate host immune responses more precisely.

Host-Directed Therapies (HDTs) represent an emerging paradigm in infectious disease treatment, targeting host cellular pathways rather than pathogen-specific mechanisms.^4^ In leprosy, M. leprae has evolved sophisticated mechanisms to subvert host immunity, including induction of regulatory T cells, upregulation of inhibitory receptors (PD-1), and metabolic reprogramming through indoleamine 2,3-dioxygenase 1 (IDO1).^5,6^ These pathways represent attractive therapeutic targets for restoring antimicrobial immunity.

We previously developed and validated an automated informatics pipeline for identifying HDT targets in tuberculosis.^7^ In this study, we extended this pipeline to leprosy, leveraging published transcriptomic signatures to systematically prioritize druggable host targets and identify repurposable compounds.

---

## METHODS

**Study Design:** This was a computational, in silico study employing a systems biology approach to integrate publicly available leprosy transcriptomic data with chemical-genomic databases for drug target and compound prioritization.

**Host Gene Signatures:** We curated a 50-gene leprosy signature from published literature and GEO datasets (GSE16844, GSE125943, GSE129033, GSE74481), focusing on genes consistently differentially expressed in leprosy lesions compared to controls. Key genes included immune modulators (IDO1, IL10, IFNG, TNF), pattern recognition receptors (TLR2, TLR10, NOD2), immune checkpoints (PDL1, CTLA4, PD1), and cytokine signaling components (JAK2, STAT1, STAT3).

**Target Scoring Algorithm:** For each gene, a composite target prioritization score was calculated:

*Composite Score = 0.35 × Omics_Strength + 0.25 × OpenTargets_Evidence + 0.20 × Druggability_Proxy + 0.10 × Pathway_Centrality + 0.10 × Replication*

**Pipeline Architecture:** The analysis utilized a custom Python pipeline integrating three public APIs: MyGene.info for gene-to-protein mapping, Open Targets Platform for druggability assessment, and ChEMBL database (version 33) for compound bioactivity data.^8-10^

**Compound Mining:** For targets overlapping with our previously validated tuberculosis HDT pipeline, compounds with pChEMBL ≥6.0 (corresponding to ≤1 μM potency) were included.

**Literature Validation:** Top-ranked targets were cross-referenced against PubMed to confirm published evidence for their role in leprosy immunopathology and therapeutic potential.

---

## RESULTS

**Host Target Prioritization:** The pipeline successfully processed the 50-gene leprosy signature, yielding prioritized HDT candidates ranked by composite score (Table 1). The top 10 targets included:

| Rank | Gene | Protein | Score | Leprosy Relevance |
|------|------|---------|-------|-------------------|
| 1 | VEGFA | Vascular Endothelial Growth Factor A | 0.525 | Angiogenesis in granulomas |
| 2 | PDL1 (CD274) | Programmed Death Ligand 1 | 0.449 | T-cell exhaustion |
| 3 | IDO1 | Indoleamine 2,3-Dioxygenase 1 | 0.386 | Tryptophan catabolism, immunosuppression |
| 4 | CD38 | CD38 Molecule | 0.291 | B-cell marker, Daratumumab target |
| 5 | IL10 | Interleukin 10 | 0.273 | Anti-inflammatory cytokine |
| 6 | VDR | Vitamin D Receptor | 0.271 | Antimicrobial peptide induction |
| 7 | BLK | B Lymphoid Kinase | 0.270 | B-cell signaling |
| 8 | JAK2 | Janus Kinase 2 | 0.263 | Cytokine signaling |
| 9 | CXCL10 | C-X-C Chemokine Ligand 10 | 0.263 | T-cell recruitment |
| 10 | CTLA4 | Cytotoxic T-Lymphocyte Antigen 4 | 0.259 | Immune checkpoint |

**Literature Validation of Top Targets:**

*IDO1 (Rank 3):* IDO1 is strongly validated in leprosy literature. Studies demonstrate that M. leprae induces IDO1 expression in monocytes and Schwann cells via IL-10-dependent mechanisms.^5^ IDO1 catabolizes tryptophan to kynurenine, depleting this essential amino acid and producing immunosuppressive metabolites that inhibit T-cell function and promote regulatory T-cell differentiation. IDO1 expression is significantly elevated in lepromatous leprosy compared to tuberculoid forms.^11^ Targeting IDO1 with inhibitors such as 1-methyl-tryptophan has been proposed to restore antimicrobial immunity.

*PDL1/CD274 (Rank 2):* PD-1/PD-L1 checkpoint signaling is critically implicated in leprosy immunopathology. PD-1 expression is significantly elevated on T cells in lepromatous leprosy patients, correlating with disease severity and bacterial index.^12^ The PD-1/PD-L1 interaction suppresses effector T-cell proliferation and IFN-γ production, contributing to immune tolerance. Blocking this pathway restores T-cell activation and pro-inflammatory cytokine production, suggesting checkpoint inhibitors as potential adjunctive therapy.^13^

*JAK2 (Rank 8):* JAK2 signaling mediates cytokine responses central to leprosy immunology. Notably, Tofacitinib (a JAK inhibitor) has been reported as a novel therapeutic approach for chronic Type 2 leprosy reactions (ENL).^14^ However, JAK inhibition carries immunosuppression risks and requires careful patient selection.

**Compound Discovery:** A total of 629 compounds with pChEMBL >6.0 were identified for overlapping targets between leprosy and tuberculosis signatures (Table 2). Key drug candidates include:

| Drug | Target | pChEMBL | Status | Leprosy Relevance |
|------|--------|---------|--------|-------------------|
| Ruxolitinib | JAK1/JAK2 | 7.51 | FDA Approved | ENL treatment potential; immunosuppression risk |
| Tofacitinib | JAK1/JAK2/JAK3 | 7.41 | FDA Approved | Published use for ENL |
| Baricitinib | JAK1/JAK2 | 7.80 | FDA Approved | JAK inhibitor |
| Upadacitinib | JAK1/JAK2 | 8.52 | FDA Approved | Selective JAK inhibitor |
| CHEMBL323090 | MMP9 | 11.0 | Experimental | Tissue damage prevention |
| Ilomastat | MMP9 | 10.3 | Phase 2 | Matrix metalloproteinase inhibitor |

---

## DISCUSSION

**IDO1 as a Therapeutic Target:** Our pipeline identified IDO1 as the third-ranked target with robust literature support. The IDO1-kynurenine pathway represents a key mechanism by which M. leprae establishes immune tolerance.^5^ In lepromatous leprosy, elevated IDO1 expression in lesional macrophages and Schwann cells depletes local tryptophan, starving pathogen-reactive T cells and generating immunosuppressive kynurenine metabolites.^11^ 

IDO1 inhibitors, including epacadostat and indoximod, have been developed for oncology applications but could potentially be repurposed for infectious diseases.^15^ In the context of leprosy, IDO1 inhibition could theoretically restore T-cell function and enhance bacterial clearance. However, the dual role of IDO1 in both pathogen control and tissue protection warrants careful preclinical investigation.

**Immune Checkpoint Blockade:** The identification of PDL1 (CD274) and CTLA4 among top targets aligns with emerging evidence that M. leprae exploits immune checkpoint pathways to evade host immunity.^12,13^ PD-1 expression on CD4+ and CD8+ T cells is significantly elevated in lepromatous leprosy patients, and blocking PD-1/PD-L1 interaction in vitro restores IFN-γ production.^12^

While checkpoint inhibitors (pembrolizumab, nivolumab) have transformed oncology, their application in infectious diseases remains investigational. Potential benefits include restoring antimicrobial immunity in immunocompromised patients. However, excessive immune activation could exacerbate leprosy reactions, necessitating careful patient selection and monitoring.

**JAK Inhibitors and ENL:** Our identification of JAK2 aligns with published evidence supporting JAK inhibition for chronic ENL.^14^ ENL is characterized by excessive TNF-α and inflammatory cytokine production, and JAK inhibitors can dampen this hyperinflammation. Tofacitinib has shown promising results in case reports for steroid-refractory ENL.^14^ Our compound analysis identified multiple FDA-approved JAK inhibitors with sub-micromolar potency, supporting further investigation.

**Shared Targets with Tuberculosis:** A notable finding is the significant overlap between leprosy and tuberculosis HDT targets, including JAK2, MMP9, PPARG, and VDR. This overlap reflects shared mycobacterial immune evasion strategies and suggests that HDT approaches successful in tuberculosis may be applicable to leprosy. The VDR pathway, which induces antimicrobial peptide cathelicidin, is particularly relevant for both diseases.^16^

**Limitations:** This study has several limitations. The analysis is entirely in silico and requires experimental validation in M. leprae infection models. The 50-gene signature represents a curated subset of differentially expressed genes and may not capture the full complexity of leprosy immunopathology. Drug-drug interactions with MDT regimens (dapsone, rifampicin, clofazimine) were not evaluated computationally.

---

## CONCLUSION

This study demonstrates the utility of an integrated multi-omics and chemoinformatics pipeline for identifying Host-Directed Therapy candidates in leprosy. We prioritized 50 host targets and identified 629 bioactive compounds. IDO1, PDL1, and JAK2 emerged as high-priority druggable targets with strong literature validation. IDO1 inhibitors may reverse tolerogenic immunosuppression, PD-1/PD-L1 blockers could restore T-cell function, and JAK inhibitors show promise for managing leprosy reactions. These findings support developing adjunctive immunotherapies to complement conventional MDT and prevent leprosy-associated disability.

---

## ACKNOWLEDGEMENTS

We acknowledge the ChEMBL team at EMBL-EBI and the Open Targets Platform for providing open-access drug-target interaction data.

---

## REFERENCES

1. World Health Organization. Global leprosy update, 2022: moving towards a leprosy-free world. Wkly Epidemiol Rec 2023; 98: 409-430.
2. Scollard DM, Adams LB, Gillis TP, Krahenbuhl JL, Truman RW, Williams DL. The continuing challenges of leprosy. Clin Microbiol Rev 2006; 19: 338-381.
3. Walker SL, Lockwood DN. Leprosy type 1 (reversal) reactions and their management. Lepr Rev 2008; 79: 372-386.
4. Kaufmann SHE, Dorhoi A, Hotchkiss RS, Bartenschlager R. Host-directed therapies for bacterial and viral infections. Nat Rev Drug Discov 2018; 17: 35-56.
5. de Mattos Barbosa MG, da Silva Prata RB, Andrade PR, et al. Indoleamine 2,3-dioxygenase and iron are required for Mycobacterium leprae survival. Microbes Infect 2017; 19: 505-514.
6. Kumar S, Naqvi RA, Khanna N, Pathak P, Rao DN. Th3 immune responses in the progression of leprosy via molecular cross-talks of TGF-β, CTLA-4 and Cbl-b. Clin Immunol 2011; 141: 133-142.
7. Siddalingaiah HS. Multi-omics pipeline identifies Ruxolitinib and MMP9 inhibitors as host-directed therapy candidates for tuberculosis. Int J Tuberc Lung Dis 2024 (submitted).
8. Wu C, MacLeod I, Su AI. BioGPS and MyGene.info: organizing online, gene-centric information. Nucleic Acids Res 2013; 41: D561-D565.
9. Ochoa D, Hercules A, Grau L, et al. Open Targets Platform: supporting systematic drug-target identification and prioritisation. Nucleic Acids Res 2021; 49: D1302-D1310.
10. Zdrazil B, Felix E, Hunter F, et al. The ChEMBL Database in 2023: a drug discovery platform spanning multiple bioactivity data types. Nucleic Acids Res 2024; 52: D1180-D1192.
11. de Souza Sales J, Lara FA, Amadeu TP, et al. The role of indoleamine 2,3-dioxygenase in lepromatous leprosy immunosuppression. Clin Exp Immunol 2011; 165: 251-263.
12. Palermo ML, Pagliari C, Trindade MA, et al. Increased expression of regulatory T cells and down-regulatory molecules in lepromatous leprosy. Am J Trop Med Hyg 2012; 86: 878-883.
13. Bobosha K, Tang ST, van der Ploeg-van Schip JJ, et al. T-cell regulation in lepromatous leprosy. PLoS Negl Trop Dis 2014; 8: e2773.
14. Thangaraju P, Vellaichamy S, Babu TR, Lalitha P. Tofacitinib: A novel therapeutic approach for the management of chronic type II lepra reaction. Lepr Rev 2020; 91: 86-89.
15. Muller AJ, Sharma MD, Chandler PR, et al. Chronic inflammation that facilitates tumor progression creates local immune suppression by inducing indoleamine 2,3 dioxygenase. Proc Natl Acad Sci USA 2008; 105: 17073-17078.
16. Liu PT, Stenger S, Li H, et al. Toll-like receptor triggering of a vitamin D-mediated human antimicrobial response. Science 2006; 311: 1770-1773.

---

## TABLES

**Table 1: Top 10 Host-Directed Therapy Target Candidates for Leprosy**

| Rank | Gene | Protein | Composite Score |
|------|------|---------|-----------------|
| 1 | VEGFA | Vascular Endothelial Growth Factor A | 0.525 |
| 2 | PDL1 | Programmed Death Ligand 1 | 0.449 |
| 3 | IDO1 | Indoleamine 2,3-Dioxygenase 1 | 0.386 |
| 4 | CD38 | CD38 Molecule | 0.291 |
| 5 | IL10 | Interleukin 10 | 0.273 |
| 6 | VDR | Vitamin D Receptor | 0.271 |
| 7 | BLK | B Lymphoid Kinase | 0.270 |
| 8 | JAK2 | Janus Kinase 2 | 0.263 |
| 9 | CXCL10 | C-X-C Chemokine Ligand 10 | 0.263 |
| 10 | CTLA4 | Cytotoxic T-Lymphocyte Antigen 4 | 0.259 |

---

**Table 2: Clinically Advanced Drug Candidates for Leprosy HDT Repurposing**

| Drug | ChEMBL ID | Target | pChEMBL | Max Phase | Safety Consideration |
|------|-----------|--------|---------|-----------|----------------------|
| Tofacitinib | CHEMBL221959 | JAK1/JAK2/JAK3 | 7.41 | 4 (Approved) | Published for ENL |
| Ruxolitinib | CHEMBL1789941 | JAK1/JAK2 | 7.51 | 4 (Approved) | Immunosuppression risk |
| Baricitinib | CHEMBL2105759 | JAK1/JAK2 | 7.80 | 4 (Approved) | JAK inhibitor |
| Upadacitinib | CHEMBL3622821 | JAK1/JAK2 | 8.52 | 4 (Approved) | Selective JAK inhibitor |
| Ilomastat | CHEMBL19611 | MMP9 | 10.3 | 2 | Matrix metalloproteinase inhibitor |

---

## FIGURE LEGENDS

**Figure 1:** Distribution of compound bioactivity (pChEMBL values) for 629 identified compounds targeting leprosy-relevant host proteins.

**Figure 2:** Top 20 leprosy host targets ranked by maximum compound pChEMBL value, demonstrating druggability landscape.

---
