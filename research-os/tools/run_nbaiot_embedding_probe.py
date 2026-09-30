"""Feasibility probe for device information in a frozen lightweight IDS embedding.

This defensive offline experiment uses a N-BaIoT mirror. A positive device probe is
not leakage evidence and does not establish that device information causes a
held-device performance gap.
"""
from pathlib import Path
import json
import time
import warnings
import zipfile

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

from run_nbaiot_common_support_audit import (
    ROWS_PER_DEVICE_LABEL,
    SEED,
    ZIP,
    coverage_report,
    filename_label,
    read_first,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/nbaiot-original-preflight/embedding-probe.json"
ROW_OFFSET = 0
HIDDEN_UNITS = 32


def hidden_representation(x, weights, bias):
    """Compute the first ReLU hidden layer of an sklearn MLP classifier."""
    return np.maximum(0.0, np.asarray(x) @ np.asarray(weights) + np.asarray(bias))


def load_common_support():
    with zipfile.ZipFile(ZIP) as zipped:
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
        member_by_label = {
            device: {filename_label(item, device): item for item in files}
            for device, files in members.items()
        }
        frames, y_parts, device_parts = [], [], []
        for device in devices:
            for label_index, label in enumerate(labels):
                frames.append(
                    read_first(
                        zipped,
                        member_by_label[device][label],
                        ROWS_PER_DEVICE_LABEL,
                        ROW_OFFSET,
                    )
                )
                y_parts.append(np.full(ROWS_PER_DEVICE_LABEL, label_index, dtype=int))
                device_parts.append(np.full(ROWS_PER_DEVICE_LABEL, device, dtype=int))
    return (
        pd.concat(frames, ignore_index=True),
        np.concatenate(y_parts),
        np.concatenate(device_parts),
        labels,
        coverage,
    )


def fit_embedding_classifier(x_train, y_train, seed):
    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()
    x_train = scaler.fit_transform(imputer.fit_transform(x_train))
    model = MLPClassifier(
        hidden_layer_sizes=(HIDDEN_UNITS,),
        activation="relu",
        alpha=0.0001,
        batch_size=512,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=15,
        max_iter=300,
        random_state=seed,
    )
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        model.fit(x_train, y_train)
    return imputer, scaler, model, [str(item.message) for item in caught]


def encode(imputer, scaler, model, frame):
    x = scaler.transform(imputer.transform(frame))
    return hidden_representation(x, model.coefs_[0], model.intercepts_[0])


def class_metric(y_true, prediction, labels):
    return {
        "macro_f1": float(
            f1_score(y_true, prediction, labels=list(range(len(labels))), average="macro", zero_division=0)
        ),
        "accuracy": float(accuracy_score(y_true, prediction)),
    }


def conditional_embedding_probe(z, y, device, labels, seed):
    rows = []
    for class_index, label in enumerate(labels):
        indices = np.flatnonzero(y == class_index)
        train, test = train_test_split(
            indices, test_size=0.5, random_state=seed, stratify=device[indices]
        )
        probe = RandomForestClassifier(
            n_estimators=80, max_depth=18, n_jobs=-1, random_state=seed
        )
        probe.fit(z[train], device[train])
        predicted = probe.predict(z[test])
        rows.append(
            {
                "label": label,
                "rows": int(len(indices)),
                "devices": int(len(np.unique(device[indices]))),
                "accuracy": float(accuracy_score(device[test], predicted)),
                "macro_f1": float(
                    f1_score(device[test], predicted, average="macro", zero_division=0)
                ),
            }
        )
    return rows


def main():
    if not ZIP.exists():
        raise FileNotFoundError(ZIP)
    x, y, device, labels, coverage = load_common_support()
    strata = np.array([f"{d}:{label}" for d, label in zip(device, y)])
    random_train, random_test = train_test_split(
        np.arange(len(x)), test_size=0.25, random_state=SEED, stratify=strata
    )
    imputer, scaler, random_model, random_warnings = fit_embedding_classifier(
        x.iloc[random_train], y[random_train], SEED
    )
    random_prediction = random_model.predict(
        scaler.transform(imputer.transform(x.iloc[random_test]))
    )
    report = {
        "source_archive": str(ZIP),
        "scope": "One-mirror frozen-embedding feasibility probe; not a causal shortcut test.",
        "limitations": [
            "Device numbers are mirror groups, not owner-verified device names.",
            "No explicit timestamp is available; row offset is not chronology.",
            "Probe training uses source-device representation samples, so it does not test unseen-target device identification.",
            "Nine held-device points are insufficient for a publishable CDP-to-DHG association claim.",
        ],
        "protocol": {
            "seed": SEED,
            "row_offset": ROW_OFFSET,
            "rows_per_device_label": ROWS_PER_DEVICE_LABEL,
            "labels": labels,
            "hidden_units": HIDDEN_UNITS,
            "random_split": "25% stratified by device × class",
            "lodo": "MLP trains on 75% of eight source devices; source remainder probes embeddings; held device is test only",
        },
        "coverage": coverage,
        "random_row": {
            **class_metric(y[random_test], random_prediction, labels),
            "fit_warnings": random_warnings,
            "n_iter": int(random_model.n_iter_),
        },
        "leave_one_device_out": [],
    }

    for held_device in range(1, 10):
        source = np.flatnonzero(device != held_device)
        target = np.flatnonzero(device == held_device)
        source_strata = strata[source]
        train, probe = train_test_split(
            source,
            test_size=0.25,
            random_state=SEED + held_device,
            stratify=source_strata,
        )
        started = time.perf_counter()
        imputer, scaler, model, fit_warnings = fit_embedding_classifier(
            x.iloc[train], y[train], SEED + held_device
        )
        fit_seconds = time.perf_counter() - started
        target_x = scaler.transform(imputer.transform(x.iloc[target]))
        target_prediction = model.predict(target_x)
        probe_z = encode(imputer, scaler, model, x.iloc[probe])
        device_probe = conditional_embedding_probe(
            probe_z, y[probe], device[probe], labels, SEED + held_device
        )
        report["leave_one_device_out"].append(
            {
                "held_device": held_device,
                **class_metric(y[target], target_prediction, labels),
                "dhg_macro_f1": round(
                    report["random_row"]["macro_f1"]
                    - class_metric(y[target], target_prediction, labels)["macro_f1"],
                    12,
                ),
                "fit_seconds": fit_seconds,
                "fit_warnings": fit_warnings,
                "n_iter": int(model.n_iter_),
                "conditional_source_embedding_device_probe": device_probe,
                "mean_probe_macro_f1": float(
                    np.mean([row["macro_f1"] for row in device_probe])
                ),
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
