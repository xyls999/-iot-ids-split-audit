"""Preflight smoke experiment on a public N-BaIoT-derived mirror.

This is deliberately not the final official-dataset experiment: the mirror has
nine per-file groups, binary labels and no timestamp/device metadata in the CSV.
The report records that limitation.
"""
from pathlib import Path
import json, time, zipfile, pickle
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, recall_score, roc_auc_score, confusion_matrix

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT / "data/raw/n-baiot-final-kaggle.zip"
OUT = ROOT / "artifacts/nbaiot-preflight"
OUT.mkdir(parents=True, exist_ok=True)
SEED = 20260929
MAX_PER_CLASS = 2000


def sample_group(z, name):
    chunks = []
    with z.open(name) as fh:
        for chunk in pd.read_csv(fh, chunksize=100_000):
            chunk = chunk.replace([np.inf, -np.inf], np.nan)
            # Binary mapping: BENIGN=0; all attack labels=1.
            y = (chunk["Label"].astype(str).str.upper() != "BENIGN").astype(int)
            x = chunk.drop(columns=["Label"])
            # Deterministic per-chunk sample; cap after concatenation.
            take = min(len(chunk), 20_000)
            idx = np.random.default_rng(SEED + len(chunks)).choice(len(chunk), size=take, replace=False)
            chunks.append((x.iloc[idx].copy(), y.iloc[idx].to_numpy()))
    x = pd.concat([a for a, _ in chunks], ignore_index=True)
    y = np.concatenate([b for _, b in chunks])
    selected = []
    for label in [0, 1]:
        ids = np.flatnonzero(y == label)
        rng = np.random.default_rng(SEED + label + len(name))
        if len(ids) > MAX_PER_CLASS:
            ids = rng.choice(ids, MAX_PER_CLASS, replace=False)
        selected.append(ids)
    ids = np.concatenate(selected)
    rng = np.random.default_rng(SEED + len(name) * 3)
    rng.shuffle(ids)
    return x.iloc[ids].reset_index(drop=True), y[ids]


def metrics(y, pred, score):
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    return {
        "n": int(len(y)),
        "accuracy": float(accuracy_score(y, pred)),
        "macro_f1": float(f1_score(y, pred, average="macro", zero_division=0)),
        "attack_recall": float(recall_score(y, pred, zero_division=0)),
        "fpr": float(fp / (fp + tn)) if (fp + tn) else None,
        "auroc": float(roc_auc_score(y, score)) if len(np.unique(y)) == 2 else None,
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
    }


def main():
    if not ZIP.exists(): raise SystemExit(f"missing {ZIP}")
    with zipfile.ZipFile(ZIP) as z:
        names = sorted(n for n in z.namelist() if n.lower().endswith(".csv"))
        groups = {name: sample_group(z, name) for name in names}
    report = {"source_zip": str(ZIP), "groups": {k: {"rows": int(len(v[1])), "benign": int((v[1] == 0).sum()), "attack": int((v[1] == 1).sum()), "features": int(v[0].shape[1])} for k, v in groups.items()}, "models": []}
    # Leave-one-file-out preflight; file identity is only a proxy and is not a verified device ID.
    for target_name in names:
      source_names = [n for n in names if n != target_name]
      xsrc = pd.concat([groups[n][0] for n in source_names], ignore_index=True)
      ysrc = np.concatenate([groups[n][1] for n in source_names])
      xt, yt = groups[target_name]
      benign_ids = np.flatnonzero(yt == 0)
      rng = np.random.default_rng(SEED + len(target_name))
      rng.shuffle(benign_ids)
      cal_n = max(1, len(benign_ids) // 5)
      cal_ids, test_benign_ids = benign_ids[:cal_n], benign_ids[cal_n:]
      test_ids = np.concatenate([test_benign_ids, np.flatnonzero(yt == 1)])
      for model_name, model in [
        ("logistic_regression", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler()), ("model", LogisticRegression(max_iter=300, class_weight="balanced", random_state=SEED))])),
        ("random_forest", Pipeline([("impute", SimpleImputer(strategy="median")), ("model", RandomForestClassifier(n_estimators=80, max_depth=16, n_jobs=-1, class_weight="balanced", random_state=SEED))])),
    ]:
        t0 = time.perf_counter(); model.fit(xsrc, ysrc); fit_s = time.perf_counter() - t0
        t1 = time.perf_counter(); src_score = model.predict_proba(xt.iloc[test_ids])[:, 1]; infer_s = time.perf_counter() - t1
        fixed_pred = (src_score >= 0.5).astype(int)
        cal_score = model.predict_proba(xt.iloc[cal_ids])[:, 1]
        cal_threshold = float(np.quantile(cal_score, 0.95))
        cal_pred = (src_score >= cal_threshold).astype(int)
        size = len(pickle.dumps(model, protocol=pickle.HIGHEST_PROTOCOL))
        report["models"].append({"model": model_name, "source_groups": source_names, "target_group": target_name, "calibration_rows": int(len(cal_ids)), "fit_seconds": fit_s, "inference_seconds": infer_s, "inference_us_per_row": infer_s / len(test_ids) * 1e6, "serialized_model_bytes": size, "fixed_threshold_0.5": metrics(yt[test_ids], fixed_pred, src_score), "benign_quantile_0.95_threshold": cal_threshold, "benign_calibrated": metrics(yt[test_ids], cal_pred, src_score)})
      # next held-out file
    (OUT / "results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__": main()
