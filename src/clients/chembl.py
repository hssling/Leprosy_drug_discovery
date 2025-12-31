from __future__ import annotations
import os
import requests
from urllib.parse import urljoin
from typing import Any, Dict, Iterator, Optional

DEFAULT_BASE = "https://www.ebi.ac.uk/chembl/api/data/"

class ChEMBLClient:
    def __init__(self, base: Optional[str] = None, timeout: int = 60):
        self.base = (base or os.getenv("CHEMBL_BASE") or DEFAULT_BASE).rstrip("/") + "/"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = urljoin(self.base, path.lstrip("/"))
        r = self.session.get(url, params=params or {}, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def paged(self, path: str, params: Optional[Dict[str, Any]] = None, limit: int = 1000) -> Iterator[Dict[str, Any]]:
        params = dict(params or {})
        params.setdefault("limit", min(limit, 1000))
        params.setdefault("offset", 0)
        while True:
            data = self.get(path, params=params)
            # Try common ChEMBL keys first
            candidates = ["activities", "targets", "molecules", "documents", "assays", "cells", "tissues"]
            list_key = next((k for k in candidates if k in data), None)
            if not list_key:
                list_key = next((k for k in data.keys() if k.endswith("_list")), None)
            if not list_key:
                yield data
                return
            items = data.get(list_key, [])
            for it in items:
                yield it
            page_meta = data.get("page_meta") or {}
            if not page_meta.get("next"):
                return
            params["offset"] = int(page_meta.get("offset", 0)) + int(page_meta.get("limit", 0))
