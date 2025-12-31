from __future__ import annotations
import os
import requests
from typing import Any, Dict, List, Optional

DEFAULT_QUERY = "http://mygene.info/v3/query"

class MyGeneClient:
    def __init__(self, endpoint: Optional[str] = None, timeout: int = 60):
        self.endpoint = endpoint or os.getenv("MYGENE_QUERY") or DEFAULT_QUERY
        self.timeout = timeout

    def query_symbol(self, symbol: str, species: str = "human") -> Dict[str, Any]:
        # Query fields we need: ensembl, uniprot
        params = {
            "q": symbol,
            "species": species,
            "fields": "symbol,ensembl.gene,uniprot.Swiss-Prot,uniprot.TrEMBL,entrezgene,name",
            "size": 5
        }
        r = requests.get(self.endpoint, params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    @staticmethod
    def pick_best_hit(resp: Dict[str, Any], prefer_reviewed_uniprot: bool = True) -> Dict[str, Any]:
        hits = resp.get("hits") or []
        if not hits:
            return {}
        # Prefer exact symbol match if possible
        def score(h):
            s = 0
            if str(h.get("symbol","")).upper() == str(resp.get("query","")).upper():
                s += 5
            if "ensembl" in h:
                s += 2
            uni = h.get("uniprot") or {}
            if prefer_reviewed_uniprot and uni.get("Swiss-Prot"):
                s += 3
            elif uni.get("TrEMBL"):
                s += 1
            return s
        hits_sorted = sorted(hits, key=score, reverse=True)
        return hits_sorted[0]
