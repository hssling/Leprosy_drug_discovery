from __future__ import annotations
import pandas as pd
from typing import List, Dict, Any
from ..clients.opentargets import OpenTargetsClient

# Minimal GraphQL: fetch tractability buckets and known drugs count.
# For TB specifically, OT has disease entries; you can extend with a diseaseId filter.
QUERY = '''
query TargetMini($ensemblId: String!) {
  target(ensemblId: $ensemblId) {
    id
    approvedSymbol
    biotype
    tractability {
      label
      modality
      value
    }
    knownDrugs {
      count
    }
  }
}
'''

def fetch_target_evidence(ensembl_ids: List[str], ot: OpenTargetsClient) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    for eid in [e for e in ensembl_ids if e]:
        data = ot.query(QUERY, variables={"ensemblId": eid})
        t = (data or {}).get("target") or {}
        tract = t.get("tractability") or []
        # simple proxy: count tractability entries + known drugs count
        rows.append({
            "ensembl_gene": eid,
            "approvedSymbol": t.get("approvedSymbol"),
            "biotype": t.get("biotype"),
            "known_drugs_count": (t.get("knownDrugs") or {}).get("count"),
            "tractability_entries": len(tract),
        })
    return pd.DataFrame(rows)
