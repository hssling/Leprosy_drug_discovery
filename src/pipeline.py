from __future__ import annotations
import time
from pathlib import Path
import pandas as pd
import typer
from dotenv import load_dotenv

from .utils.config import load_yaml
from .utils.io import write_json
from .clients.mygene import MyGeneClient
from .clients.chembl import ChEMBLClient
from .clients.opentargets import OpenTargetsClient
from .methods.id_mapping import map_host_genes_to_ids, map_uniprot_to_chembl_targets
from .methods.opentargets_evidence import fetch_target_evidence
from .methods.target_prioritization import score_targets
from .methods.compound_search import chembl_top_compounds_for_target

app = typer.Typer(add_completion=False)

def _new_run_dir(project: str, run_tag: str) -> Path:
    ts = time.strftime("%Y%m%d-%H%M%S")
    run_id = f"{project}_{run_tag}_{ts}"
    run_dir = Path("runs") / run_id
    (run_dir / "cache").mkdir(parents=True, exist_ok=True)
    (run_dir / "outputs").mkdir(parents=True, exist_ok=True)
    return run_dir

def _load_signature(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    for col in ["entity","logFC","pval","direction"]:
        if col not in df.columns:
            raise ValueError(f"Signature missing column '{col}': {csv_path}")
    return df

@app.command()
def run(config: Path = typer.Option(..., exists=True)):
    load_dotenv()
    cfg = load_yaml(config)
    proj = cfg["project"]["name"]
    tag = cfg["project"].get("run_tag", "run")
    run_mode = cfg.get("mode", {}).get("run_mode", "both")

    run_dir = _new_run_dir(proj, tag)
    write_json(run_dir / "config_snapshot.json", cfg)

    chembl = ChEMBLClient()
    ot = OpenTargetsClient()
    mygene = MyGeneClient()

    weights = cfg["prioritization"]["weights"]
    min_p = float(cfg["compound_search"].get("min_pchembl", 6.0))
    max_n = int(cfg["compound_search"].get("max_compounds_per_target", 50))
    use_chembl = bool(cfg["compound_search"].get("use_chembl", True))

    all_targets_ranked = []
    all_compounds = []

    # --- HOST ---
    if run_mode in ("host","both"):
        host_paths = [Path(p) for p in cfg["inputs"]["signatures"]["host"]]
        host_sig = pd.concat([_load_signature(p) for p in host_paths], ignore_index=True)
        host_sig.rename(columns={"entity":"gene_symbol"}, inplace=True)
        host_sig.to_csv(run_dir/"outputs"/"host_signature_merged.csv", index=False)

        # Map host genes -> Ensembl/UniProt
        entities = sorted(set(host_sig["gene_symbol"].astype(str).tolist()))
        map_cfg = cfg.get("host_mapping", {})
        mapping = map_host_genes_to_ids(
            entities,
            mygene=mygene,
            species=map_cfg.get("species","human"),
            prefer_reviewed_uniprot=bool(map_cfg.get("prefer_reviewed_uniprot", True))
        )
        mapping.to_csv(run_dir/"outputs"/"mapping_gene_to_ids.csv", index=False)

        # Open Targets evidence (Ensembl)
        evid = fetch_target_evidence(mapping["ensembl_gene"].dropna().astype(str).tolist(), ot=ot)
        evid.to_csv(run_dir/"outputs"/"opentargets_evidence.csv", index=False)

        # Merge signature with mapping + evidence
        host_sig2 = host_sig.merge(mapping, how="left", left_on="gene_symbol", right_on="entity")
        host_scored = score_targets(
            signature_df=host_sig2.rename(columns={"ensembl_gene":"ensembl_gene"}),
            evidence_df=evid,
            weights=weights
        )
        host_scored["track"] = "host"
        host_scored.to_csv(run_dir/"outputs"/"targets_ranked_host.csv", index=False)
        all_targets_ranked.append(host_scored)

        # Map UniProt -> ChEMBL targets
        uniprots = []
        if "uniprot_swissprot" in mapping.columns:
            uniprots += mapping["uniprot_swissprot"].dropna().astype(str).tolist()
        if "uniprot_trembl" in mapping.columns:
            uniprots += mapping["uniprot_trembl"].dropna().astype(str).tolist()
        uniprots = sorted(set(uniprots))
        chembl_map = map_uniprot_to_chembl_targets(uniprots, chembl=chembl)
        chembl_map.to_csv(run_dir/"outputs"/"mapping_ids_to_chembl_target.csv", index=False)

        if use_chembl:
            # pick best chembl target per gene by joining through uniprot
            best_map = chembl_map.dropna(subset=["target_chembl_id"]).copy()
            for _, row in best_map.iterrows():
                tid = row["target_chembl_id"]
                cdf = chembl_top_compounds_for_target(chembl, tid, min_pchembl=min_p, max_n=max_n)
                if not cdf.empty:
                    cdf["track"] = "host"
                    all_compounds.append(cdf)

    # --- PATHOGEN ---
    if run_mode in ("pathogen","both"):
        path_paths = [Path(p) for p in cfg["inputs"]["signatures"]["pathogen"]]
        path_sig = pd.concat([_load_signature(p) for p in path_paths], ignore_index=True)
        path_sig.rename(columns={"entity":"uniprot_accession"}, inplace=True)
        path_sig.to_csv(run_dir/"outputs"/"pathogen_signature_merged.csv", index=False)

        # Map pathogen UniProt -> ChEMBL targets
        chembl_map_p = map_uniprot_to_chembl_targets(
            path_sig["uniprot_accession"].dropna().astype(str).tolist(),
            chembl=chembl
        )
        chembl_map_p.to_csv(run_dir/"outputs"/"mapping_pathogen_uniprot_to_chembl_target.csv", index=False)

        # Simple scoring (omics only) for pathogen in v2
        path_sig["abs_logFC"] = path_sig["logFC"].abs()
        path_sig["omics_strength"] = (path_sig["abs_logFC"] / path_sig["abs_logFC"].max()) if path_sig["abs_logFC"].max() else 0
        path_sig["score"] = path_sig["omics_strength"]
        path_sig["track"] = "pathogen"
        path_sig.to_csv(run_dir/"outputs"/"targets_ranked_pathogen.csv", index=False)
        all_targets_ranked.append(path_sig)

        if use_chembl:
            for tid in chembl_map_p["target_chembl_id"].dropna().astype(str).unique().tolist():
                cdf = chembl_top_compounds_for_target(chembl, tid, min_pchembl=min_p, max_n=max_n)
                if not cdf.empty:
                    cdf["track"] = "pathogen"
                    all_compounds.append(cdf)

    # --- COMBINE OUTPUTS ---
    if all_targets_ranked:
        targets_all = pd.concat(all_targets_ranked, ignore_index=True)
        targets_all.to_csv(run_dir/"outputs"/"targets_ranked.csv", index=False)
    else:
        targets_all = pd.DataFrame()
        targets_all.to_csv(run_dir/"outputs"/"targets_ranked.csv", index=False)

    if all_compounds:
        compounds_all = pd.concat(all_compounds, ignore_index=True)
        compounds_all = compounds_all.sort_values("pchembl_value", ascending=False).drop_duplicates(["track","molecule_chembl_id","target_chembl_id"])
        compounds_all.to_csv(run_dir/"outputs"/"compounds_ranked.csv", index=False)
    else:
        pd.DataFrame(columns=["target_chembl_id","molecule_chembl_id","pchembl_value","track"]).to_csv(run_dir/"outputs"/"compounds_ranked.csv", index=False)

    # Summary markdown
    lines = []
    lines.append(f"# Run summary: {run_dir.name}")
    lines.append("")
    lines.append("## Outputs")
    lines.append(f"- Targets: {run_dir/'outputs'/'targets_ranked.csv'}")
    lines.append(f"- Compounds: {run_dir/'outputs'/'compounds_ranked.csv'}")
    lines.append("")
    lines.append("## Notes")
    lines.append("- Host track uses MyGene.info for ID mapping and Open Targets for evidence.")
    lines.append("- Pathogen track (v2) expects UniProt accessions in input; add TubercuList/UniProt taxonomy mapping in v3 if needed.")
    (run_dir/"outputs"/"summary_report.md").write_text("\n".join(lines), encoding="utf-8")

    typer.echo(f"Done. Run folder: {run_dir}")

if __name__ == "__main__":
    app()
