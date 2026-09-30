"""Common-support feasibility audit for the N-BaIoT original-layout mirror.

This is an offline defensive data-audit experiment. It does not claim that device
recoverability is leakage, and it does not use row order as a verified timestamp.
"""
from pathlib import Path
import json
import pickle
import time
import zipfile

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT / "data/raw/n-baiot-original-kaggle.zip"
OUT = ROOT / "artifacts/nbaiot-original-preflight/common-support-audit.json"
SEED = 20260930
ROWS_PER_DEVICE_LABEL = 600
ROW_OFFSET = 0


def coverage_report(device_to_labels):
    """Return the label common support and every missing device × label cell."""
    all_labels = set().union(*device_to_labels.values())
    common = set.intersection(*device_to_labels.values())
    return {
        "common_labels": sorted(common),
        "missing_by_device": {
            str(device): sorted(all_labels - labels)
            for device, labels in sorted(device_to_labels.items())
            if all_labels - labels
        },
    }


def device_holdout_gap(random_metric, held_out_metric):
    """Positive values mean the random-row result exceeds the held-device result."""
    return round(float(random_metric) - float(held_out_metric), 12)


def filename_label(member, device):
    name = Path(member).name
    prefix = f"{device}."
    if not name.startswith(prefix) or not name.endswith(".csv"):
        raise ValueError(f"Unexpected archive member for device {device}: {member}")
    return name[len(prefix):-4]


def read_first(zipped, member, n, start=0):
    frames = []
    remaining = n
    rows_to_skip = start
    with zipped.open(member) as handle:
        for chunk in pd.read_csv(handle, chunksize=50_000):
            if rows_to_skip >= len(chunk):
                rows_to_skip -= len(chunk)
                continue
            if rows_to_skip:
                chunk = chunk.iloc[rows_to_skip:]
                rows_to_skip = 0
            piece = chunk.iloc[:remaining]
            frames.append(piece)
            remaining -= len(piece)
            if remaining <= 0:
                break
    if remaining > 0:
        raise ValueError(f"{member} has fewer than {start + n} rows")
    return pd.concat(frames, ignore_index=True).replace([np.inf, -np.inf], np.nan)


def fresh_models():
    return {
        "logistic_regression": Pipeline(
            [
                ("impute", SimpleImputer(strategy="median")),
                ("scale", StandardScaler()),
                (
                    "model",
                    LogisticRegression(
                        max_iter=350, class_weight="balanced", random_state=SEED
                    ),
                ),
            ]
        ),
        "random_forest": Pipeline(
            [
                ("impute", SimpleImputer(strategy="median")),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=100,
                        max_depth=18,
                        class_weight="balanced",
                        n_jobs=-1,
                        random_state=SEED,
                    ),
                ),
            ]
        ),
    }


def per_label_f1(y_true, y_pred, label_names):
    """Return class F1 scores keyed by the declared, stable label names."""
    values = f1_score(
        y_true,
        y_pred,
        labels=list(range(len(label_names))),
        average=None,
        zero_division=0,
    )
    return {name: float(value) for name, value in zip(label_names, values)}


def fit_score(model, x_train, y_train, x_test, y_test, labels, label_names):
    started = time.perf_counter()
    model.fit(x_train, y_train)
    fit_seconds = time.perf_counter() - started
    started = time.perf_counter()
    predicted = model.predict(x_test)
    inference_seconds = time.perf_counter() - started
    return {
        "macro_f1": float(
            f1_score(y_test, predicted, labels=labels, average="macro", zero_division=0)
        ),
        "per_label_f1": per_label_f1(y_test, predicted, label_names),
        "accuracy": float(accuracy_score(y_test, predicted)),
        "fit_seconds": fit_seconds,
        "inference_us_per_row": inference_seconds / len(y_test) * 1_000_000,
        "serialized_model_bytes": len(pickle.dumps(model, pickle.HIGHEST_PROTOCOL)),
    }


def conditional_raw_feature_probe(x, y, device, labels):
    """Device probes on input features within true class strata, not model embeddings."""
    rows = []
    for label_index, label in enumerate(labels):
        indices = np.flatnonzero(y == label_index)
        train, test = train_test_split(
            indices, test_size=0.25, random_state=SEED, stratify=device[indices]
        )
        probe = Pipeline(
            [
                ("impute", SimpleImputer(strategy="median")),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=100,
                        max_depth=18,
                        n_jobs=-1,
                        random_state=SEED,
                    ),
                ),
            ]
        )
        probe.fit(x.iloc[train], device[train])
        prediction = probe.predict(x.iloc[test])
        rows.append(
            {
                "label": label,
                "rows": int(len(indices)),
                "devices": int(len(np.unique(device[indices]))),
                "accuracy": float(accuracy_score(device[test], prediction)),
                "macro_f1": float(
                    f1_score(device[test], prediction, average="macro", zero_division=0)
                ),
            }
        )
    return rows


def main():
    if not ZIP.exists():
        raise FileNotFoundError(f"Missing archive: {ZIP}")
    with zipfile.ZipFile(ZIP) as zipped:
        zip_error = zipped.testzip()
        devices = range(1, 10)
        members = {
            device: sorted(
                item
                for item in zipped.namelist()
                if item.startswith(f"dataset/{device}.") and item.endswith(".csv")
            )
            for device in devices
        }
        label_sets = {
            device: {filename_label(item, device) for item in files}
            for device, files in members.items()
        }
        coverage = coverage_report(label_sets)
        labels = coverage["common_labels"]
        if len(labels) < 2:
            raise ValueError("Need at least two labels in device-common support")
        pieces, y_parts, device_parts = [], [], []
        member_by_label = {
            device: {filename_label(item, device): item for item in files}
            for device, files in members.items()
        }
        for device in devices:
            for label_index, label in enumerate(labels):
                frame = read_first(
                    zipped, member_by_label[device][label], ROWS_PER_DEVICE_LABEL, ROW_OFFSET
                )
                pieces.append(frame)
                y_parts.append(np.full(len(frame), label_index, dtype=int))
                device_parts.append(np.full(len(frame), device, dtype=int))

    x = pd.concat(pieces, ignore_index=True)
    y = np.concatenate(y_parts)
    device = np.concatenate(device_parts)
    strata = np.array([f"{d}:{label}" for d, label in zip(device, y)])
    random_train, random_test = train_test_split(
        np.arange(len(x)), test_size=0.25, random_state=SEED, stratify=strata
    )

    report = {
        "source_archive": str(ZIP),
        "archive_integrity_test_error": zip_error,
        "scope": "Offline common-support feasibility audit on a Kaggle original-layout mirror; not an official UCI final result.",
        "limitations": [
            "Device numbers are mirror group identifiers, not owner-verified device names.",
            "The CSV mirror has no explicit timestamps; this audit does not make temporal claims.",
            "Raw-feature conditional probes are not frozen-model representation probes and do not establish shortcut reliance or causality.",
            "One dataset cannot test cross-dataset replication of a CDP-to-DHG association.",
        ],
        "protocol": {
            "seed": SEED,
            "rows_per_device_label": ROWS_PER_DEVICE_LABEL,
            "row_offset": ROW_OFFSET,
            "labels": labels,
            "random_split": "25% stratified by device × class cell",
            "held_device_split": "train on the other eight device groups; test the held group; same balanced common-support rows",
        },
        "coverage": coverage,
        "dataset": {
            "rows": int(len(x)),
            "features": int(x.shape[1]),
            "devices": int(len(np.unique(device))),
            "rows_per_device_label": {
                f"{d}:{labels[label_index]}": int(np.sum((device == d) & (y == label_index)))
                for d in devices
                for label_index in range(len(labels))
            },
        },
        "conditional_raw_feature_device_probes": conditional_raw_feature_probe(
            x, y, device, labels
        ),
        "attack_classification": {"random_row": {}, "leave_one_device_out": []},
    }

    random_metrics = {}
    label_ids = list(range(len(labels)))
    for name, model in fresh_models().items():
        metric = fit_score(
            model,
            x.iloc[random_train],
            y[random_train],
            x.iloc[random_test],
            y[random_test],
            label_ids,
            labels,
        )
        random_metrics[name] = metric
        report["attack_classification"]["random_row"][name] = metric

    for held_device in range(1, 10):
        train = np.flatnonzero(device != held_device)
        test = np.flatnonzero(device == held_device)
        row = {"held_device": held_device, "models": {}}
        for name, model in fresh_models().items():
            metric = fit_score(
                model, x.iloc[train], y[train], x.iloc[test], y[test], label_ids, labels
            )
            metric["dhg_macro_f1"] = device_holdout_gap(
                random_metrics[name]["macro_f1"], metric["macro_f1"]
            )
            row["models"][name] = metric
        report["attack_classification"]["leave_one_device_out"].append(row)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
