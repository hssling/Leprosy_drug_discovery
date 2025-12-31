from __future__ import annotations
import pandas as pd
import numpy as np

def _minmax(series: pd.Series) -> pd.Series:
    s = series.astype(float)
    if s.max() == s.min():
        return pd.Series([0.0]*len(s), index=s.index)
    return (s - s.min()) / (s.max() - s.min())

def score_targets(
    signature_df: pd.DataFrame,
    evidence_df: pd.DataFrame | None,
    weights: dict
) -> pd.DataFrame:
    df = signature_df.copy()

    df["abs_logFC"] = df["logFC"].abs()
    df["omics_strength"] = _minmax(df["abs_logFC"])

    if evidence_df is not None and not evidence_df.empty:
        df = df.merge(evidence_df, how="left", on="ensembl_gene")
        df["known_drugs_count"] = df["known_drugs_count"].fillna(0)
        df["tractability_entries"] = df["tractability_entries"].fillna(0)
        # druggability proxy combines OT known drugs + tractability
        df["druggability_proxy"] = _minmax(df["known_drugs_count"] + df["tractability_entries"])
        # opentargets evidence proxy: same as druggability here (extend in v3)
        df["opentargets_evidence"] = df["druggability_proxy"]
    else:
        df["druggability_proxy"] = 0.0
        df["opentargets_evidence"] = 0.0

    w = weights
    df["score"] = (
        w.get("omics_strength", 0.35) * df["omics_strength"]
        + w.get("opentargets_evidence", 0.25) * df["opentargets_evidence"]
        + w.get("druggability_proxy", 0.20) * df["druggability_proxy"]
    )

    return df.sort_values("score", ascending=False).reset_index(drop=True)
