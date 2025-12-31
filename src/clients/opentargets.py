from __future__ import annotations
import os
import requests
from typing import Any, Dict, Optional

DEFAULT_ENDPOINT = "https://api.platform.opentargets.org/api/v4/graphql"

class OpenTargetsClient:
    def __init__(self, endpoint: Optional[str] = None, timeout: int = 60):
        self.endpoint = endpoint or os.getenv("OPENTARGETS_API") or DEFAULT_ENDPOINT
        self.timeout = timeout

    def query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = {"query": query, "variables": variables or {}}
        r = requests.post(self.endpoint, json=payload, timeout=self.timeout)
        r.raise_for_status()
        data = r.json()
        if "errors" in data:
            raise RuntimeError(f"OpenTargets GraphQL error: {data['errors']}")
        return data.get("data", {})
