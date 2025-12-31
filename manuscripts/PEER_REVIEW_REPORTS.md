# Peer Review Reports - Leprosy HDT Manuscript

## REVIEWER 1 REPORT

**Manuscript ID:** LR-2024-XXX  
**Title:** An Integrated Multi-omics and Chemoinformatics Pipeline Identifies IDO1, PDL1, and JAK2 as Host-Directed Therapy Candidates for Leprosy  
**Recommendation:** MAJOR REVISIONS REQUIRED

---

### OVERALL ASSESSMENT

This computational study presents a systematic approach to identifying host-directed therapy targets for leprosy using multi-omics integration. While the methodology is sound and the findings are potentially valuable, several critical issues must be addressed before publication.

**Strengths:**
- Novel application of computational pipeline to leprosy
- Integration of multiple public databases
- Literature validation of top targets
- Reproducible approach with open data/code

**Weaknesses:**
- Limited experimental validation
- Unclear gene selection criteria
- Insufficient justification for weighting scheme
- Missing critical methodological details

---

### MAJOR CONCERNS

#### 1. **Gene Signature Curation (Critical)**

**Issue:** The manuscript states a "50-gene host signature was compiled" but provides insufficient detail on the selection process.

**Specific Problems:**
- How were the 50 genes selected from potentially thousands of differentially expressed genes?
- Were genes selected based on overlap across datasets or other criteria?
- What was the rationale for including genes from GSE74481 (a TB study, ref 27) in a leprosy signature?
- No Venn diagram or overlap analysis shown

**Required Revisions:**
- Provide supplementary table with all 50 genes, their expression values across datasets, and selection rationale
- Add Venn diagram showing gene overlap across the 4 datasets
- Clarify if genes must be differentially expressed in ALL datasets or just one
- Justify inclusion of TB dataset (GSE74481) - is this appropriate?

---

#### 2. **Composite Scoring Algorithm (Critical)**

**Issue:** The weighting scheme (0.35, 0.25, 0.20, 0.10, 0.10) appears arbitrary.

**Specific Problems:**
- No justification provided for these specific weights
- Were sensitivity analyses performed with different weights?
- How robust are the rankings to weight changes?
- "Pathway_Centrality" and "Replication" are mentioned but never defined

**Required Revisions:**
- Provide rationale for each weight (literature-based? empirical?)
- Perform sensitivity analysis showing top 10 targets with varied weights
- Define "Pathway_Centrality" - which network? What centrality metric?
- Define "Replication" - cross-study consistency? How measured?
- Consider showing correlation between individual components

---

#### 3. **Compound Selection Methodology (Major)**

**Issue:** The manuscript states compounds were identified "from overlapping targets with tuberculosis" but this is confusing.

**Specific Problems:**
- Why limit to TB-overlapping targets? This excludes leprosy-specific targets
- How many targets overlap? Which ones?
- Were compounds identified for ALL 50 targets or only overlapping ones?
- This approach seems to bias toward TB rather than leprosy

**Required Revisions:**
- Clarify compound identification strategy
- Provide Venn diagram of leprosy vs TB targets
- Justify why leprosy-specific targets were excluded from compound search
- Consider searching compounds for ALL prioritized targets, not just TB-overlapping

---

#### 4. **Literature Validation (Major)**

**Issue:** Literature validation is presented for only 3 targets (IDO1, PDL1, JAK2) out of 50.

**Specific Problems:**
- What about the other 47 targets?
- Selection bias - only validating targets that worked?
- VEGFA ranked #1 but no validation provided
- CD38 (#4) and IL10 (#5) also lack validation

**Required Revisions:**
- Provide systematic literature search for ALL top 10 targets
- Include negative results (targets NOT validated in literature)
- Add supplementary table with PubMed search results for all 50 targets
- Discuss why top-ranked VEGFA was not prioritized in discussion

---

#### 5. **Missing Methodological Details**

**Critical Missing Information:**
- **Data preprocessing:** How were raw transcriptomic data processed? Normalization? Batch correction?
- **Statistical thresholds:** Why |log₂FC| ≥1.0 and not 1.5 or 2.0?
- **Multiple testing correction:** Which method? FDR? Bonferroni?
- **ChEMBL queries:** Exact query parameters? Activity types included?
- **Protein-protein interaction network:** Which database? STRING? BioGRID?

**Required Revisions:**
- Add detailed methods subsection on data preprocessing
- Justify all statistical thresholds
- Provide exact API queries in supplementary methods
- Specify PPI network source and version

---

### MODERATE CONCERNS

#### 6. **Results Presentation**

**Issues:**
- Table 1 shows "Known Drugs" but doesn't explain what this means
- No statistical comparison between leprosy and TB target sets
- Figure quality assessment needed (resolution, labels)
- Missing power analysis or sample size justification

**Suggestions:**
- Define "Known Drugs" in Table 1 legend
- Add statistical test (Fisher's exact?) for pathway enrichment
- Ensure all figures are 600 dpi minimum
- Discuss study power limitations

---

#### 7. **Discussion Limitations**

**Issues:**
- Insufficient discussion of computational limitations
- No discussion of why VEGFA ranked #1 but wasn't prioritized
- Limited discussion of potential drug-drug interactions with MDT
- Missing discussion of target redundancy (multiple checkpoints)

**Suggestions:**
- Add paragraph on computational vs experimental validation
- Explain VEGFA ranking vs biological plausibility
- Discuss rifampicin drug interactions with proposed compounds
- Address whether targeting multiple checkpoints is beneficial or harmful

---

### MINOR CONCERNS

#### 8. **Abstract**
- "Background" section should be removed per Leprosy Review guidelines
- Merge background into Objectives

#### 9. **References**
- Reference 21 is "submitted" - provide preprint DOI if available
- Some references lack DOIs (add where possible)

#### 10. **Figures**
- Figure 1 (pipeline schematic) is mentioned but not shown in text
- Figure legends could be more detailed
- Consider combining Figures 2A, 2B, 2C into multi-panel

---

### SPECIFIC QUESTIONS FOR AUTHORS

1. Were any leprosy-specific pathways identified that differ from TB?
2. Why was pChEMBL ≥6.0 chosen as cutoff?
3. Have any of the identified compounds been tested in M. leprae models?
4. What is the plan for experimental validation?
5. How do you address the concern that IDO1 may be protective rather than pathogenic?

---

### RECOMMENDATION

This manuscript presents valuable computational work but requires substantial revisions before publication. The major concerns regarding gene selection, scoring methodology, and validation must be addressed. I recommend **MAJOR REVISIONS** with re-review after authors respond to all points.

**Estimated revision time:** 4-6 weeks

---

**Reviewer 1 Signature**  
Expert in Computational Biology & Drug Discovery  
Date: December 31, 2024

---
---

## REVIEWER 2 REPORT

**Manuscript ID:** LR-2024-XXX  
**Title:** An Integrated Multi-omics and Chemoinformatics Pipeline Identifies IDO1, PDL1, and JAK2 as Host-Directed Therapy Candidates for Leprosy  
**Recommendation:** MINOR REVISIONS

---

### OVERALL ASSESSMENT

This manuscript describes an innovative computational approach to identify host-directed therapy targets for leprosy. As a leprosy immunologist, I find the work scientifically sound and the findings clinically relevant. However, several immunological and clinical aspects require clarification.

**Strengths:**
- Addresses important unmet need (leprosy reactions)
- Strong literature validation for key targets
- Clinically actionable findings (JAK inhibitors)
- Appropriate for Leprosy Review readership

**Weaknesses:**
- Oversimplification of leprosy immunology
- Insufficient discussion of reaction mechanisms
- Missing safety considerations
- Limited discussion of patient stratification

---

### MAJOR CONCERNS

#### 1. **Immunological Context (Major)**

**Issue:** The manuscript treats leprosy as a single entity but reactions occur in different immunological contexts.

**Specific Problems:**
- Type 1 reactions (RR) involve Th1 upregulation - would checkpoint blockade worsen this?
- Type 2 reactions (ENL) involve immune complexes - different mechanism
- IDO1 inhibition might precipitate reactions rather than prevent them
- No discussion of when in disease course HDT should be given

**Required Revisions:**
- Add paragraph discussing reaction immunology
- Clarify whether HDT is for prevention or treatment of reactions
- Discuss potential for HDT to trigger reactions (immune reconstitution)
- Specify patient populations (LL vs TT, during MDT vs after)

---

#### 2. **Clinical Translation Concerns (Major)**

**Issue:** Several proposed interventions have significant safety concerns not discussed.

**Specific Problems:**
- **Checkpoint inhibitors:** Risk of autoimmune complications (well-documented in cancer)
- **IDO1 inhibitors:** Failed in cancer trials - why would leprosy be different?
- **JAK inhibitors:** TB reactivation risk in endemic areas
- **Drug interactions:** Rifampicin is potent CYP450 inducer

**Required Revisions:**
- Add "Safety Considerations" subsection to Discussion
- Discuss autoimmune risks of checkpoint blockade
- Address TB reactivation risk with JAK inhibitors
- Discuss rifampicin drug interactions
- Mention need for pharmacokinetic studies

---

#### 3. **Target Biology (Moderate)**

**Issue:** Some target biology is oversimplified or potentially incorrect.

**Specific Problems:**
- **IDO1:** May be protective (antimicrobial) rather than purely immunosuppressive
- **PD-L1:** Expressed on multiple cell types - which is relevant?
- **VEGFA:** Ranked #1 but barely discussed - why?
- **CD38:** Mentioned as "B-cell marker" but has enzymatic functions

**Required Revisions:**
- Discuss dual role of IDO1 (antimicrobial vs immunosuppressive)
- Specify which cells express PD-L1 in leprosy lesions
- Provide rationale for VEGFA ranking vs biological plausibility
- Correct CD38 description (NADase, not just marker)

---

### MODERATE CONCERNS

#### 4. **Missing Clinical Context**

**Issues:**
- No discussion of current ENL treatment algorithms
- Limited mention of steroid-sparing rationale
- Missing cost-effectiveness considerations
- No discussion of access in endemic countries

**Suggestions:**
- Add paragraph on current ENL management challenges
- Discuss cost of JAK inhibitors vs steroids/thalidomide
- Mention WHO Essential Medicines List considerations
- Address feasibility in resource-limited settings

---

#### 5. **Literature Validation Gaps**

**Issues:**
- Tofacitinib reference (32) is single case series - not strong evidence
- No mention of other JAK inhibitor trials in leprosy
- Missing key leprosy immunology references
- No discussion of failed HDT approaches

**Suggestions:**
- Acknowledge limited clinical evidence for Tofacitinib
- Search for other JAK inhibitor case reports
- Add references: Modlin (leprosy immunology), Scollard (reactions)
- Discuss why previous immunomodulatory approaches failed

---

#### 6. **Target Prioritization Logic**

**Issues:**
- VEGFA (#1) seems biologically implausible as primary target
- Angiogenesis in granulomas is complex (pro- and anti-inflammatory)
- Why prioritize VEGFA over IDO1 if IDO1 has better validation?
- Scoring may favor druggability over biological relevance

**Suggestions:**
- Discuss limitations of composite scoring
- Consider separate rankings: "most druggable" vs "most validated"
- Acknowledge that computational scores ≠ clinical priority
- Provide biological plausibility assessment for top 5 targets

---

### MINOR CONCERNS

#### 7. **Terminology**
- "Anergic responses" (line 64) - technically incorrect, should be "deficient cell-mediated immunity"
- "Tolerogenic immunosuppression" - unclear term
- "Antimicrobial immunity" - specify Th1/Th17 responses

#### 8. **Missing Information**
- No mention of M. leprae strain differences (if relevant)
- No discussion of nerve damage mechanisms (MMP9 mentioned but not developed)
- Limited discussion of biomarkers for patient selection

#### 9. **Figures**
- Figure 4 (TB-leprosy overlap) is interesting but needs more discussion
- Consider adding clinical decision tree for HDT use
- Pathway heatmap (Figure 3) - explain color scheme better

---

### SPECIFIC QUESTIONS FOR AUTHORS

1. At what stage of disease/treatment would you propose HDT?
2. How would you select patients for checkpoint blockade vs JAK inhibition?
3. What about combining HDT with MDT - any concerns?
4. Have you considered host genetic factors (HLA, etc.)?
5. What are the next steps for experimental validation?

---

### ADDITIONAL SUGGESTIONS

#### Strengthen Clinical Relevance:
- Add table of "Clinical Translation Roadmap" showing next steps for each target
- Include estimated timeline to clinical trials
- Discuss regulatory pathway (repurposed drugs vs new indications)

#### Improve Discussion:
- Add comparison to other computational drug discovery in NTDs
- Discuss why computational approach is necessary for leprosy (vs experimental)
- Mention ongoing clinical trials of immunomodulators in leprosy (if any)

---

### RECOMMENDATION

This is valuable work that advances the field of leprosy therapeutics. The computational approach is appropriate and the findings are clinically relevant. However, the immunological and clinical context needs strengthening. I recommend **MINOR REVISIONS** focusing on:

1. Immunological context of reactions
2. Safety considerations
3. Clinical translation pathway
4. Target biology clarifications

These revisions can be accomplished relatively quickly and will substantially improve the manuscript's impact.

**Estimated revision time:** 2-3 weeks

---

**Reviewer 2 Signature**  
Expert in Leprosy Immunology & Clinical Management  
Date: December 31, 2024

---
---

## SUMMARY OF KEY REVISION POINTS

### Critical (Must Address):
1. ✅ Clarify gene selection methodology with supplementary data
2. ✅ Justify composite scoring weights with sensitivity analysis
3. ✅ Explain compound selection strategy (TB overlap issue)
4. ✅ Provide systematic literature validation for top 10 targets
5. ✅ Add detailed methods on data preprocessing
6. ✅ Discuss immunological context of reactions
7. ✅ Add safety considerations section

### Important (Should Address):
8. Define pathway centrality and replication metrics
9. Discuss VEGFA ranking vs biological plausibility
10. Address drug-drug interactions with MDT
11. Clarify patient stratification strategy
12. Discuss dual role of IDO1
13. Add clinical translation roadmap

### Minor (Consider Addressing):
14. Remove "Background" from abstract
15. Add DOIs to all references
16. Improve figure quality/legends
17. Correct terminology (anergic, etc.)
18. Add cost-effectiveness discussion

---

**Total Revision Points:** 18  
**Estimated Revision Time:** 4-6 weeks  
**Overall Recommendation:** MAJOR REVISIONS (Reviewer 1) / MINOR REVISIONS (Reviewer 2)  
**Editor Decision:** Likely MAJOR REVISIONS given critical methodological concerns
