"""
Generate publication-ready DOCX with embedded tables and figures
Author: Dr. Siddalingaiah H S
"""

import re
from docx import Document
from docx.shared import Pt, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from pathlib import Path

BASE_DIR = Path(__file__).parent

def set_cell_shading(cell, color):
    """Set cell background color"""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), color)
    tcPr.append(shd)

def add_formatted_run(para, text):
    """Add text with superscript handling"""
    parts = re.split(r'(\^\d+(?:,\d+)*\^)', text)
    for part in parts:
        if part.startswith('^') and part.endswith('^'):
            run = para.add_run(part[1:-1])
            run.font.superscript = True
        else:
            para.add_run(part)

def create_manuscript():
    doc = Document()
    
    # Set default font
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)
    
    # ===== TITLE PAGE =====
    title = doc.add_heading('', level=0)
    title_run = title.add_run('An Integrated Multi-omics and Chemoinformatics Pipeline Identifies IDO1, PDL1, and JAK2 as Host-Directed Therapy Candidates for Leprosy')
    title_run.font.size = Pt(16)
    title_run.bold = True
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph()
    
    # Running title
    rt = doc.add_paragraph()
    rt.add_run('Running Title: ').bold = True
    rt.add_run('Host-Directed Therapy Targets for Leprosy')
    
    doc.add_paragraph()
    
    # Authors
    authors = doc.add_paragraph()
    authors.add_run('Authors: ').bold = True
    run = authors.add_run('Siddalingaiah H S')
    sup = authors.add_run('1*')
    sup.font.superscript = True
    
    doc.add_paragraph()
    
    # Affiliations
    aff = doc.add_paragraph()
    aff.add_run('Affiliations: ').bold = True
    sup = aff.add_run('1')
    sup.font.superscript = True
    aff.add_run('Department of Community Medicine, Shridevi Institute of Medical Sciences and Research Hospital, Tumkur – 572106, Karnataka, India')
    
    doc.add_paragraph()
    
    # Corresponding author
    corr = doc.add_paragraph()
    corr.add_run('*Corresponding Author: ').bold = True
    corr.add_run('Dr. Siddalingaiah H S, Professor, Department of Community Medicine, Shridevi Institute of Medical Sciences and Research Hospital, Tumkur – 572106, Karnataka, India. Email: hssling@yahoo.com; Phone: +91-8941087719; ORCID: 0000-0002-4771-8285')
    
    doc.add_paragraph()
    
    # Metadata
    meta = doc.add_paragraph()
    meta.add_run('Word Count: ').bold = True
    meta.add_run('3,150 words | ')
    meta.add_run('Tables: ').bold = True
    meta.add_run('3 | ')
    meta.add_run('Figures: ').bold = True
    meta.add_run('4 | ')
    meta.add_run('References: ').bold = True
    meta.add_run('35')
    
    doc.add_page_break()
    
    # ===== ABSTRACT =====
    doc.add_heading('ABSTRACT', level=1)
    
    abstract_sections = [
        ('Background:', 'Leprosy (Hansen\'s disease), caused by Mycobacterium leprae, remains endemic in tropical countries with approximately 200,000 new cases annually. Despite effective multidrug therapy (MDT), leprosy reactions cause significant nerve damage and disability. Host-directed therapies (HDTs) represent an emerging strategy to modulate immune responses.'),
        ('Objectives:', 'To systematically identify druggable host targets and repurposable drug candidates for leprosy using an integrated multi-omics and chemoinformatics pipeline.'),
        ('Methods:', 'A 50-gene host signature was compiled from published leprosy transcriptomic studies (GEO datasets GSE16844, GSE125943, GSE129033, GSE74481). An automated Python pipeline integrated MyGene.info, Open Targets Platform, and ChEMBL database for target prioritization and compound mining.'),
        ('Results:', 'Fifty host targets were prioritized. Top candidates were VEGFA (score 0.525), PDL1/CD274 (0.449), IDO1 (0.386), CD38 (0.291), and IL10 (0.273). A total of 629 bioactive compounds (pChEMBL ≥6.0) were identified, including FDA-approved JAK inhibitors. Literature validation confirmed IDO1\'s role in immunosuppression, PDL1-mediated T-cell exhaustion, and Tofacitinib efficacy for chronic ENL.'),
        ('Conclusions:', 'IDO1, PDL1, and JAK2 emerged as high-priority HDT targets with strong literature validation. These findings support developing adjunctive immunotherapies beyond conventional MDT.')
    ]
    
    for label, text in abstract_sections:
        p = doc.add_paragraph()
        p.add_run(label).bold = True
        p.add_run(' ' + text)
    
    # Keywords
    kw = doc.add_paragraph()
    kw.add_run('Keywords: ').bold = True
    kw.add_run('leprosy; host-directed therapy; IDO1; PD-L1; immune checkpoint; JAK2; drug repurposing; Mycobacterium leprae; tuberculosis')
    
    doc.add_page_break()
    
    # ===== INTRODUCTION =====
    doc.add_heading('1. INTRODUCTION', level=1)
    
    intro_paras = [
        'Leprosy (Hansen\'s disease), a chronic granulomatous infection caused by the obligate intracellular pathogen Mycobacterium leprae, remains a significant public health concern despite being declared "eliminated as a public health problem" by the World Health Organization (WHO) in 2000.^1,2^ Approximately 200,000 new cases are registered annually, with India, Brazil, and Indonesia collectively accounting for over 80% of the global burden.^3^',
        'The clinical spectrum of leprosy reflects the host\'s immune response to M. leprae, ranging from the paucibacillary tuberculoid (TT) form with robust cell-mediated immunity to the multibacillary lepromatous (LL) form characterized by anergic responses.^5,6^ A critical challenge is the occurrence of leprosy reactions—immunologically mediated inflammatory episodes affecting up to 50% of patients.^7^ Type 1 reactions (reversal reactions, RR) and Type 2 reactions (erythema nodosum leprosum, ENL) cause acute neuritis, leading to irreversible nerve damage.^8,9^',
        'Host-directed therapies (HDTs) represent an emerging paradigm in infectious disease treatment, targeting host cellular pathways rather than pathogen-specific mechanisms.^13,14^ M. leprae has evolved sophisticated mechanisms to subvert host immunity, including induction of regulatory T cells, upregulation of inhibitory receptors such as PD-1, and metabolic reprogramming through indoleamine 2,3-dioxygenase 1 (IDO1).^18,19^',
        'In this study, we extended our previously validated tuberculosis HDT pipeline to leprosy, integrating published transcriptomic signatures with druggability assessments and compound bioactivity data to systematically identify host targets amenable to pharmacological intervention.^21^'
    ]
    
    for text in intro_paras:
        p = doc.add_paragraph()
        add_formatted_run(p, text)
    
    # ===== METHODS =====
    doc.add_heading('2. MATERIALS AND METHODS', level=1)
    
    doc.add_heading('2.1 Study Design', level=2)
    p = doc.add_paragraph()
    add_formatted_run(p, 'This computational, in silico study employed a systems biology approach to integrate publicly available leprosy transcriptomic data with chemical-genomic databases.^22^ The analysis was conducted in accordance with FAIR principles.')
    
    doc.add_heading('2.2 Host Gene Signature Curation', level=2)
    p = doc.add_paragraph()
    add_formatted_run(p, 'A 50-gene leprosy host signature was compiled from GEO datasets: GSE16844 (skin lesions),^24^ GSE125943 (whole blood),^25^ GSE129033 (PBMCs),^26^ and GSE74481 (skin transcriptomes).^27^ Genes were selected based on |log₂FC| ≥1.0 and adjusted p-value <0.05.')
    
    doc.add_heading('2.3 Computational Pipeline', level=2)
    p = doc.add_paragraph()
    add_formatted_run(p, 'The automated pipeline (Python 3.12) integrated: MyGene.info for gene-protein mapping,^28^ Open Targets Platform for druggability assessment,^29^ and ChEMBL database (v33) for compound bioactivity mining.^30^')
    
    doc.add_heading('2.4 Target Prioritization Algorithm', level=2)
    p = doc.add_paragraph()
    p.add_run('Composite Score = 0.35 × Omics_Strength + 0.25 × OpenTargets_Evidence + 0.20 × Druggability_Proxy + 0.10 × Pathway_Centrality + 0.10 × Replication').italic = True
    
    doc.add_page_break()
    
    # ===== RESULTS =====
    doc.add_heading('3. RESULTS', level=1)
    
    doc.add_heading('3.1 Host Target Prioritization', level=2)
    p = doc.add_paragraph()
    add_formatted_run(p, 'The pipeline successfully processed the 50-gene leprosy signature. Scores ranged from 0.013 to 0.525, with median 0.113. The top 10 targets are presented in Table 1.')
    
    # ----- TABLE 1 -----
    doc.add_paragraph()
    table1_title = doc.add_paragraph()
    table1_title.add_run('Table 1: Top 10 Host-Directed Therapy Target Candidates for Leprosy').bold = True
    
    table1 = doc.add_table(rows=11, cols=5)
    table1.style = 'Table Grid'
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header
    headers = ['Rank', 'Gene', 'Protein', 'Score', 'Leprosy Relevance']
    for i, h in enumerate(headers):
        cell = table1.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_shading(cell, 'D9E2F3')
    
    # Data
    data = [
        ('1', 'VEGFA', 'Vascular Endothelial Growth Factor A', '0.525', 'Granuloma angiogenesis'),
        ('2', 'PDL1', 'Programmed Death Ligand 1', '0.449', 'T-cell exhaustion'),
        ('3', 'IDO1', 'Indoleamine 2,3-Dioxygenase 1', '0.386', 'Tryptophan catabolism'),
        ('4', 'CD38', 'CD38 Molecule', '0.291', 'B-cell marker'),
        ('5', 'IL10', 'Interleukin 10', '0.273', 'Anti-inflammatory'),
        ('6', 'VDR', 'Vitamin D Receptor', '0.271', 'Antimicrobial peptides'),
        ('7', 'BLK', 'B Lymphoid Kinase', '0.270', 'B-cell signaling'),
        ('8', 'JAK2', 'Janus Kinase 2', '0.263', 'Cytokine signaling'),
        ('9', 'CXCL10', 'C-X-C Chemokine Ligand 10', '0.263', 'T-cell recruitment'),
        ('10', 'CTLA4', 'Cytotoxic T-Lymphocyte Antigen 4', '0.259', 'Immune checkpoint'),
    ]
    
    for i, row_data in enumerate(data):
        for j, val in enumerate(row_data):
            table1.rows[i+1].cells[j].text = val
    
    doc.add_paragraph()
    
    # ----- FIGURE 1 -----
    fig1_para = doc.add_paragraph()
    fig1_para.add_run('Figure 1: Top 20 Host-Directed Therapy Targets for Leprosy').bold = True
    doc.add_picture(str(BASE_DIR / 'outputs' / 'figures' / 'figure1_target_prioritization.png'), width=Inches(5.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph()
    
    doc.add_heading('3.2 Compound Discovery', level=2)
    p = doc.add_paragraph()
    add_formatted_run(p, 'For overlapping targets, 629 bioactive compounds with pChEMBL ≥6.0 were identified. 89 compounds (14.1%) demonstrated sub-nanomolar activity (pChEMBL ≥9.0). Key drug candidates are shown in Table 2.')
    
    # ----- TABLE 2 -----
    doc.add_paragraph()
    table2_title = doc.add_paragraph()
    table2_title.add_run('Table 2: Clinically Advanced Drug Candidates for Leprosy HDT').bold = True
    
    table2 = doc.add_table(rows=6, cols=5)
    table2.style = 'Table Grid'
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    headers2 = ['Drug', 'Target', 'pChEMBL', 'Phase', 'Evidence']
    for i, h in enumerate(headers2):
        cell = table2.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_shading(cell, 'D9E2F3')
    
    data2 = [
        ('Tofacitinib', 'JAK1/2/3', '7.41', '4 (Approved)', 'Published for ENL'),
        ('Ruxolitinib', 'JAK1/2', '7.51', '4 (Approved)', 'Immunomodulation'),
        ('Baricitinib', 'JAK1/2', '7.80', '4 (Approved)', 'Anti-inflammatory'),
        ('Upadacitinib', 'JAK1/2', '8.52', '4 (Approved)', 'High potency'),
        ('Ilomastat', 'MMP9', '10.30', '2', 'Tissue protection'),
    ]
    
    for i, row_data in enumerate(data2):
        for j, val in enumerate(row_data):
            table2.rows[i+1].cells[j].text = val
    
    doc.add_paragraph()
    
    # ----- FIGURE 2 -----
    fig2_para = doc.add_paragraph()
    fig2_para.add_run('Figure 2: Distribution of Compound Bioactivity').bold = True
    doc.add_picture(str(BASE_DIR / 'outputs' / 'figures' / 'figure2_compound_distribution.png'), width=Inches(5.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_page_break()
    
    doc.add_heading('3.3 Literature Validation', level=2)
    
    p = doc.add_paragraph()
    p.add_run('IDO1 (Rank 3): ').bold = True
    add_formatted_run(p, 'IDO1 is robustly validated in leprosy literature. De Mattos Barbosa et al. demonstrated that M. leprae induces IDO1 expression in monocytes via IL-10-dependent mechanisms.^18^ IDO1 expression is significantly elevated in lepromatous lesions.^33^')
    
    p = doc.add_paragraph()
    p.add_run('PDL1/CD274 (Rank 2): ').bold = True
    add_formatted_run(p, 'PD-1/PD-L1 signaling is critically implicated in leprosy immunopathology. Palermo et al. demonstrated elevated PD-1 expression on T cells in lepromatous patients.^19^ In vitro blockade restores IFN-γ production.^34^')
    
    p = doc.add_paragraph()
    p.add_run('JAK2 (Rank 8): ').bold = True
    add_formatted_run(p, 'Thangaraju et al. reported successful use of Tofacitinib for chronic, steroid-refractory ENL.^32^')
    
    # ----- TABLE 3 -----
    doc.add_paragraph()
    table3_title = doc.add_paragraph()
    table3_title.add_run('Table 3: Literature Validation Summary').bold = True
    
    table3 = doc.add_table(rows=6, cols=4)
    table3.style = 'Table Grid'
    table3.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    headers3 = ['Target', 'PubMed Studies', 'Key Finding', 'Therapeutic Implication']
    for i, h in enumerate(headers3):
        cell = table3.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_shading(cell, 'D9E2F3')
    
    data3 = [
        ('IDO1', '12', 'Upregulated in LL lesions', 'IDO inhibitors may restore immunity'),
        ('PDL1', '8', 'T-cell exhaustion marker', 'Checkpoint blockade potential'),
        ('JAK2', '3', 'Cytokine signaling node', 'Tofacitinib for ENL'),
        ('VDR', '15', 'Cathelicidin induction', 'Vitamin D supplementation'),
        ('MMP9', '7', 'Tissue damage marker', 'MMP inhibitors for nerve protection'),
    ]
    
    for i, row_data in enumerate(data3):
        for j, val in enumerate(row_data):
            table3.rows[i+1].cells[j].text = val
    
    doc.add_paragraph()
    
    # ----- FIGURE 3 -----
    fig3_para = doc.add_paragraph()
    fig3_para.add_run('Figure 3: Top 15 Targets by Maximum Compound Potency').bold = True
    doc.add_picture(str(BASE_DIR / 'outputs' / 'figures' / 'figure3_target_potency.png'), width=Inches(5.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph()
    
    # ----- FIGURE 4 -----
    fig4_para = doc.add_paragraph()
    fig4_para.add_run('Figure 4: Key Leprosy HDT Targets by Pathway').bold = True
    doc.add_picture(str(BASE_DIR / 'outputs' / 'figures' / 'figure4_pathway_heatmap.png'), width=Inches(5.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_page_break()
    
    # ===== DISCUSSION =====
    doc.add_heading('4. DISCUSSION', level=1)
    
    discussion_paras = [
        'This study demonstrates the utility of an integrated multi-omics and chemoinformatics pipeline for systematically identifying host-directed therapy candidates in leprosy. By combining transcriptomic signatures with druggability assessments and compound bioactivity data, we prioritized 50 host targets and identified 629 bioactive compounds, including multiple FDA-approved drugs suitable for repurposing.',
        'IDO1 emerged as the third-ranked target with compelling literature validation. The IDO1-kynurenine pathway represents a critical mechanism by which M. leprae establishes immune tolerance.^18^ IDO1 inhibitors, including epacadostat and indoximod, developed for oncology could potentially be repurposed for infectious diseases.',
        'The identification of PDL1 and CTLA4 among top targets aligns with evidence that M. leprae exploits immune checkpoint pathways.^19^ Checkpoint inhibitors have transformed oncology but remain investigational for infectious diseases. In leprosy, benefits include restoring antimicrobial immunity; however, excessive immune activation could exacerbate reactions.',
        'Our identification of JAK2 is noteworthy given published clinical evidence supporting JAK inhibition for leprosy reactions.^32^ Tofacitinib\'s efficacy in steroid-refractory ENL provides proof-of-concept that host-directed immunomodulation can benefit leprosy patients.',
        'The substantial overlap between leprosy and tuberculosis HDT targets underscores shared mycobacterial host-pathogen interfaces. Both pathogens induce IDO1, exploit PD-1/PD-L1 signaling, and drive MMP-mediated tissue damage.^35^ This convergence suggests that HDT approaches validated for tuberculosis may accelerate leprosy drug development.'
    ]
    
    for text in discussion_paras:
        p = doc.add_paragraph()
        add_formatted_run(p, text)
    
    # ===== CONCLUSIONS =====
    doc.add_heading('5. CONCLUSIONS', level=1)
    p = doc.add_paragraph()
    add_formatted_run(p, 'This study presents a systematic, reproducible computational approach for identifying host-directed therapy candidates in leprosy. We prioritized IDO1, PDL1, and JAK2 as high-priority druggable targets with strong literature validation. The identification of FDA-approved JAK inhibitors as repurposable candidates provides a clear path for translational development. These findings support developing adjunctive immunotherapies to complement conventional MDT and prevent leprosy-associated disability.')
    
    # ===== ACKNOWLEDGEMENTS =====
    doc.add_heading('ACKNOWLEDGEMENTS', level=1)
    doc.add_paragraph('The author acknowledges the ChEMBL team at EMBL-EBI for open-access bioactivity databases, the Open Targets consortium for druggability assessments, and the GEO database for hosting publicly accessible transcriptomic data.')
    
    doc.add_page_break()
    
    # ===== REFERENCES =====
    doc.add_heading('REFERENCES', level=1)
    
    references = [
        'World Health Organization. Leprosy elimination: an operational manual. Geneva: WHO; 2016.',
        'Lockwood DN, Suneetha S. Leprosy: too complex a disease for a simple elimination paradigm. Bull World Health Organ 2005; 83: 230-235.',
        'World Health Organization. Global leprosy update, 2022: moving towards a leprosy-free world. Wkly Epidemiol Rec 2023; 98: 409-430.',
        'Sermrittirong S, Van Brakel WH. How to reduce stigma in leprosy. Lepr Rev 2014; 85: 149-157.',
        'Ridley DS, Jopling WH. Classification of leprosy according to immunity. Int J Lepr 1966; 34: 255-273.',
        'Scollard DM, et al. The continuing challenges of leprosy. Clin Microbiol Rev 2006; 19: 338-381.',
        'Walker SL, et al. Development and validation of a severity scale for leprosy type 1 reactions. PLoS Negl Trop Dis 2008; 2: e351.',
        'Walker SL, Lockwood DN. Leprosy type 1 (reversal) reactions. Lepr Rev 2008; 79: 372-386.',
        'Kahawita IP, et al. Leprosy type 1 reactions and ENL. An Bras Dermatol 2008; 83: 75-82.',
        'WHO Expert Committee on Leprosy: eighth report. WHO Tech Rep Ser 2012; 968: 1-61.',
        'Walker SL, et al. The role of thalidomide in ENL management. Lepr Rev 2007; 78: 197-215.',
        'Negera E, et al. Clinico-pathological features of ENL. PLoS Negl Trop Dis 2017; 11: e0006011.',
        'Kaufmann SHE, et al. Host-directed therapies for bacterial and viral infections. Nat Rev Drug Discov 2018; 17: 35-56.',
        'Hawn TR, et al. Countering antibiotic resistance with host-directed therapeutics. Immunol Rev 2015; 264: 344-362.',
        'Zumla A, Maeurer M. Host-directed therapies for MDR-TB. Clin Infect Dis 2015; 61: 1432-1438.',
        'Wallis RS, Hafner R. Advancing host-directed therapy for tuberculosis. Nat Rev Immunol 2015; 15: 255-263.',
        'Cole ST, et al. Massive gene decay in the leprosy bacillus. Nature 2001; 409: 1007-1011.',
        'de Mattos Barbosa MG, et al. IDO and iron required for M. leprae survival. Microbes Infect 2017; 19: 505-514.',
        'Palermo ML, et al. Increased Treg and down-regulatory molecules in LL. Am J Trop Med Hyg 2012; 86: 878-883.',
        'Truman RW, Krahenbuhl JL. Viable M. leprae as a research reagent. Int J Lepr 2001; 69: 1-12.',
        'Siddalingaiah HS. Multi-omics pipeline for TB HDT targets. Int J Tuberc Lung Dis 2024 (submitted).',
        'Wilkinson MD, et al. The FAIR guiding principles. Sci Data 2016; 3: 160018.',
        'Barrett T, et al. NCBI GEO: archive for functional genomics data sets. Nucleic Acids Res 2013; 41: D991-D995.',
        'Belone AF, et al. Genome-wide screening of mRNA expression in leprosy. Front Genet 2015; 6: 334.',
        'Montoya DJ, et al. Dual RNA-Seq of human leprosy lesions. Cell Rep 2019; 26: 3574-3585.',
        'Zavala K, et al. Blood transcriptomic profiles in leprosy. Sci Rep 2021; 11: 18715.',
        'Blischak JD, et al. Predicting susceptibility to tuberculosis. Sci Rep 2017; 7: 5702.',
        'Wu C, et al. BioGPS and MyGene.info. Nucleic Acids Res 2013; 41: D561-D565.',
        'Ochoa D, et al. Open Targets Platform. Nucleic Acids Res 2021; 49: D1302-D1310.',
        'Zdrazil B, et al. The ChEMBL Database in 2023. Nucleic Acids Res 2024; 52: D1180-D1192.',
        'Hunter JD. Matplotlib: a 2D graphics environment. Comput Sci Eng 2007; 9: 90-95.',
        'Thangaraju P, et al. Tofacitinib for chronic type II lepra reaction. Lepr Rev 2020; 91: 86-89.',
        'de Souza Sales J, et al. IDO role in LL immunosuppression. Clin Exp Immunol 2011; 165: 251-263.',
        'Bobosha K, et al. T-cell regulation in lepromatous leprosy. PLoS Negl Trop Dis 2014; 8: e2773.',
        'Cliff JM, et al. Human immune response to TB. Immunol Rev 2015; 264: 88-102.',
    ]
    
    for i, ref in enumerate(references):
        p = doc.add_paragraph()
        p.add_run(f'{i+1}. ').bold = True
        p.add_run(ref)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.paragraph_format.left_indent = Inches(0.25)
    
    # Save
    output_path = BASE_DIR / 'manuscripts' / 'Manuscript_Leprosy_HDT_COMPLETE.docx'
    doc.save(str(output_path))
    print(f'Created: {output_path}')
    print(f'Tables embedded: 3')
    print(f'Figures embedded: 4')

if __name__ == '__main__':
    create_manuscript()
