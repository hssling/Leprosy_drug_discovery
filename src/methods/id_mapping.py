from __future__ import annotations
import pandas as pd
from typing import Dict, Any, Optional, List
from ..clients.mygene import MyGeneClient
from ..clients.chembl import ChEMBLClient

def map_host_genes_to_ids(entities: List[str], mygene: MyGeneClient, species: str = "human", prefer_reviewed_uniprot: bool = True) -> pd.DataFrame:
    rows = []
    for sym in entities:
        resp = mygene.query_symbol(sym, species=species)
        best = mygene.pick_best_hit({**resp, "query": sym}, prefer_reviewed_uniprot=prefer_reviewed_uniprot)
        uni = best.get("uniprot") or {}
        swiss = uni.get("Swiss-Prot")
        trembl = uni.get("TrEMBL")
        ensembl = None
        ens = best.get("ensembl")
        if isinstance(ens, dict):
            ensembl = ens.get("gene")
        elif isinstance(ens, list) and ens:
            ensembl = ens[0].get("gene")
        rows.append({
            "entity": sym,
            "entrezgene": best.get("entrezgene"),
            "ensembl_gene": ensembl,
            "uniprot_swissprot": swiss if isinstance(swiss, str) else (swiss[0] if isinstance(swiss, list) and swiss else None),
            "uniprot_trembl": trembl if isinstance(trembl, str) else (trembl[0] if isinstance(trembl, list) and trembl else None),
            "mapped_symbol": best.get("symbol"),
            "name": best.get("name"),
        })
    return pd.DataFrame(rows)

def map_uniprot_to_chembl_targets(uniprot_ids: List[str], chembl: ChEMBLClient, max_hits: int = 5) -> pd.DataFrame:
    '''
    Attempts to map UniProt accessions to ChEMBL target(s).
    Uses ChEMBL filtering. If filters change, adjust per ChEMBL docs.
    '''
    rows = []
    for acc in [u for u in uniprot_ids if u]:
        # Common filter used in docs: target_components__accession=<UniProt>
        params = {"target_components__accession": acc, "limit": 20}
        data = chembl.get("target.json", params=params)
        tlist = data.get("targets") or data.get("target_list") or []
        # Robust: some envelopes use target_list
        if not tlist and "target_list" in data:
            tlist = data["target_list"]
        for t in tlist[:max_hits]:
            rows.append({
                "uniprot_accession": acc,
                "target_chembl_id": t.get("target_chembl_id"),
                "pref_name": t.get("pref_name"),
                "target_type": t.get("target_type"),
                "organism": t.get("organism"),
                "confidence_score": t.get("confidence_score"),
            })
        if not tlist:
            rows.append({
                "uniprot_accession": acc,
                "target_chembl_id": None,
                "pref_name": None,
                "target_type": None,
                "organism": None,
                "confidence_score": None,
            })
    return pd.DataFrame(rows)
