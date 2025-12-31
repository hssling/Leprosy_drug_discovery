from __future__ import annotations
import pandas as pd
from typing import List, Dict, Any
from ..clients.chembl import ChEMBLClient

def chembl_top_compounds_for_target(
    chembl: ChEMBLClient,
    target_chembl_id: str,
    min_pchembl: float = 6.0,
    max_n: int = 50
) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    if not target_chembl_id:
        return pd.DataFrame(columns=["target_chembl_id","molecule_chembl_id","pchembl_value"])
    for act in chembl.paged("activity.json", params={"target_chembl_id": target_chembl_id, "limit": 200}, limit=200):
        p = act.get("pchembl_value")
        if p is None:
            continue
        try:
            if float(p) < float(min_pchembl):
                continue
        except Exception:
            continue
        rows.append({
            "target_chembl_id": target_chembl_id,
            "molecule_chembl_id": act.get("molecule_chembl_id"),
            "pchembl_value": float(p),
            "standard_type": act.get("standard_type"),
            "standard_value": act.get("standard_value"),
            "standard_units": act.get("standard_units"),
            "assay_chembl_id": act.get("assay_chembl_id"),
            "document_chembl_id": act.get("document_chembl_id"),
        })
    if not rows:
        return pd.DataFrame(columns=["target_chembl_id","molecule_chembl_id","pchembl_value"])
    df = pd.DataFrame(rows).sort_values("pchembl_value", ascending=False).drop_duplicates("molecule_chembl_id")
    return df.head(max_n).reset_index(drop=True)
