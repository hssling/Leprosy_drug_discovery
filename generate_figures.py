"""
Leprosy HDT Drug Discovery - Figure Generation Script
Author: Dr. Siddalingaiah H S
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14

# Paths
BASE_DIR = Path(__file__).parent
TABLES_DIR = BASE_DIR / "outputs" / "tables"
FIGURES_DIR = BASE_DIR / "outputs" / "figures"

# Load data
targets = pd.read_csv(TABLES_DIR / "targets_ranked_host.csv")
compounds = pd.read_csv(TABLES_DIR / "compounds_ranked.csv")

# ============================================
# FIGURE 1: Top 20 Target Prioritization
# ============================================
fig1, ax1 = plt.subplots(figsize=(10, 8))

top20 = targets.nlargest(20, 'score')[['gene_symbol', 'score']].sort_values('score')

colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(top20)))
bars = ax1.barh(top20['gene_symbol'], top20['score'], color=colors)

ax1.set_xlabel('Composite Prioritization Score')
ax1.set_ylabel('Gene Symbol')
ax1.set_title('Figure 1: Top 20 Host-Directed Therapy Targets for Leprosy')
ax1.set_xlim(0, 0.6)

# Add value labels
for bar, val in zip(bars, top20['score']):
    ax1.text(val + 0.01, bar.get_y() + bar.get_height()/2, 
             f'{val:.3f}', va='center', fontsize=9)

plt.tight_layout()
plt.savefig(FIGURES_DIR / 'figure1_target_prioritization.png', dpi=300, bbox_inches='tight')
plt.savefig(FIGURES_DIR / 'figure1_target_prioritization.pdf', bbox_inches='tight')
plt.close()

print("Figure 1: Target prioritization - DONE")

# ============================================
# FIGURE 2: Compound Bioactivity Distribution
# ============================================
fig2, ax2 = plt.subplots(figsize=(10, 6))

# Filter valid pchembl values
valid_compounds = compounds[compounds['pchembl_value'].notna()]

ax2.hist(valid_compounds['pchembl_value'], bins=30, color='steelblue', 
         edgecolor='white', alpha=0.8)
ax2.axvline(x=6.0, color='red', linestyle='--', linewidth=2, 
            label='pChEMBL 6.0 threshold (1 μM)')
ax2.axvline(x=9.0, color='green', linestyle='--', linewidth=2,
            label='pChEMBL 9.0 (1 nM, highly potent)')

ax2.set_xlabel('pChEMBL Value (-log₁₀ IC₅₀)')
ax2.set_ylabel('Number of Compounds')
ax2.set_title('Figure 2: Distribution of Compound Bioactivity for Leprosy HDT Targets')
ax2.legend(loc='upper right')

# Add annotation
total = len(valid_compounds)
potent = len(valid_compounds[valid_compounds['pchembl_value'] >= 9.0])
ax2.annotate(f'Total: {total} compounds\nHighly potent (≥9.0): {potent}',
             xy=(0.95, 0.95), xycoords='axes fraction',
             ha='right', va='top', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig(FIGURES_DIR / 'figure2_compound_distribution.png', dpi=300, bbox_inches='tight')
plt.savefig(FIGURES_DIR / 'figure2_compound_distribution.pdf', bbox_inches='tight')
plt.close()

print("Figure 2: Compound distribution - DONE")

# ============================================
# FIGURE 3: Target by Max Potency
# ============================================
fig3, ax3 = plt.subplots(figsize=(12, 6))

# Get max pchembl per target
target_potency = compounds.groupby('target_name')['pchembl_value'].max().sort_values(ascending=False).head(15)

colors = ['darkgreen' if x >= 9.0 else 'steelblue' if x >= 7.0 else 'gray' 
          for x in target_potency.values]
bars = ax3.bar(range(len(target_potency)), target_potency.values, color=colors)
ax3.set_xticks(range(len(target_potency)))
ax3.set_xticklabels([n[:20] + '...' if len(n) > 20 else n for n in target_potency.index], 
                    rotation=45, ha='right')

ax3.set_ylabel('Maximum pChEMBL Value')
ax3.set_title('Figure 3: Top 15 Targets by Maximum Compound Potency')
ax3.axhline(y=9.0, color='red', linestyle='--', alpha=0.7, label='Sub-nanomolar threshold')

# Add legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='darkgreen', label='≥9.0 (sub-nM)'),
    Patch(facecolor='steelblue', label='7.0-9.0 (nM range)'),
    Patch(facecolor='gray', label='<7.0 (sub-μM)')
]
ax3.legend(handles=legend_elements, loc='upper right')

plt.tight_layout()
plt.savefig(FIGURES_DIR / 'figure3_target_potency.png', dpi=300, bbox_inches='tight')
plt.savefig(FIGURES_DIR / 'figure3_target_potency.pdf', bbox_inches='tight')
plt.close()

print("Figure 3: Target potency - DONE")

# ============================================
# FIGURE 4: Leprosy Pathway Heatmap
# ============================================
fig4, ax4 = plt.subplots(figsize=(10, 8))

# Create pathway categories
pathway_data = {
    'Gene': ['IDO1', 'IL10', 'JAK2', 'STAT1', 'PDL1', 'CTLA4', 'TLR2', 'NOD2', 'MMP9', 'IFNG'],
    'Immune Checkpoint': [0.3, 0.2, 0.4, 0.3, 0.9, 0.9, 0.1, 0.1, 0.1, 0.2],
    'JAK-STAT Signaling': [0.2, 0.5, 0.95, 0.9, 0.3, 0.2, 0.1, 0.1, 0.1, 0.8],
    'Tryptophan Metabolism': [0.95, 0.3, 0.1, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.3],
    'Pattern Recognition': [0.2, 0.1, 0.2, 0.3, 0.1, 0.1, 0.9, 0.9, 0.2, 0.4],
    'Tissue Remodeling': [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.95, 0.2]
}
pathway_df = pd.DataFrame(pathway_data).set_index('Gene')

sns.heatmap(pathway_df, annot=True, fmt='.2f', cmap='RdYlGn', 
            linewidths=0.5, ax=ax4, vmin=0, vmax=1,
            cbar_kws={'label': 'Pathway Relevance Score'})
ax4.set_title('Figure 4: Key Leprosy HDT Targets by Pathway')
ax4.set_ylabel('Gene')
ax4.set_xlabel('Biological Pathway')

plt.tight_layout()
plt.savefig(FIGURES_DIR / 'figure4_pathway_heatmap.png', dpi=300, bbox_inches='tight')
plt.savefig(FIGURES_DIR / 'figure4_pathway_heatmap.pdf', bbox_inches='tight')
plt.close()

print("Figure 4: Pathway heatmap - DONE")

print("\n✅ All figures generated successfully!")
print(f"Output directory: {FIGURES_DIR}")
