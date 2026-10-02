#!/usr/bin/env python3
"""Exploratory device-held-out IDS baselines on the local N-BaIoT mirror.

This is a defensive offline experiment. It compares a standard MLP with a
DANN-style device-adversarial MLP. No leakage, causality, vulnerability, or
novelty claim is made by this script.
"""
from __future__ import annotations

import argparse
import json
import random
import time
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT / "data/raw/n-baiot-original-kaggle.zip"


class GradientReversal(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x, coefficient):
        ctx.coefficient = coefficient
        return x.view_as(x)

    @staticmethod
    def backward(ctx, grad_output):
        return -ctx.coefficient * grad_output, None


def grad_reverse(x, coefficient):
    return GradientReversal.apply(x, coefficient)


class MLP(nn.Module):
    def __init__(self, features, classes, devices, adversarial=False):
        super().__init__()
        self.adversarial = adversarial
        self.encoder = nn.Sequential(nn.Linear(features, 64), nn.ReLU(), nn.Linear(64, 32), nn.ReLU())
        self.classifier = nn.Linear(32, classes)
        self.device_head = nn.Sequential(nn.Linear(32, 32), nn.ReLU(), nn.Linear(32, devices))

    def forward(self, x, grl=0.0):
        z = self.encoder(x)
        y_logits = self.classifier(z)
        d_logits = self.device_head(grad_reverse(z, grl)) if self.adversarial else None
        return y_logits, d_logits


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def filename_label(member, device):
    name = Path(member).name
    prefix = f"{device}."
    return name[len(prefix) : -4]


def read_first(zipped, member, n, start):
    frames, remaining, skip = [], n, start
    with zipped.open(member) as handle:
        for chunk in pd.read_csv(handle, chunksize=50_000):
            if skip >= len(chunk):
                skip -= len(chunk)
                continue
            if skip:
                chunk = chunk.iloc[skip:]
                skip = 0
            piece = chunk.iloc[:remaining]
            frames.append(piece)
            remaining -= len(piece)
            if remaining <= 0:
                break
    if remaining > 0:
        raise ValueError(f"{member} has fewer than {start + n} rows")
    return pd.concat(frames, ignore_index=True).replace([np.inf, -np.inf], np.nan)


def load_common(rows_per_cell, row_offset):
    with zipfile.ZipFile(ZIP) as zipped:
        devices = list(range(1, 10))
        members = {
            d: sorted(item for item in zipped.namelist() if item.startswith(f"dataset/{d}.") and item.endswith(".csv"))
            for d in devices
        }
        label_maps = {d: {filename_label(item, d): item for item in members[d]} for d in devices}
        labels = sorted(set.intersection(*(set(m) for m in label_maps.values())))
        frames, ys, ds = [], [], []
        for d in devices:
            for yi, label in enumerate(labels):
                frame = read_first(zipped, label_maps[d][label], rows_per_cell, row_offset)
                frames.append(frame)
                ys.append(np.full(len(frame), yi, dtype=np.int64))
                ds.append(np.full(len(frame), d - 1, dtype=np.int64))
    x = pd.concat(frames, ignore_index=True).replace([np.inf, -np.inf], np.nan)
    x = x.fillna(x.median(numeric_only=True)).fillna(0.0).to_numpy(dtype=np.float32)
    return x, np.concatenate(ys), np.concatenate(ds), labels


def train_model(x_train, y_train, d_train, classes, devices, seed, adversarial, epochs, grl):
    set_seed(seed)
    scaler = StandardScaler().fit(x_train)
    x_scaled = scaler.transform(x_train).astype(np.float32)
    dataset = TensorDataset(torch.from_numpy(x_scaled), torch.from_numpy(y_train), torch.from_numpy(d_train))
    loader = DataLoader(dataset, batch_size=1024, shuffle=True)
    model = MLP(x_scaled.shape[1], classes, devices, adversarial=adversarial)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-5)
    class_loss = nn.CrossEntropyLoss()
    for _ in range(epochs):
        model.train()
        for xb, yb, db in loader:
            optimizer.zero_grad()
            yp, dp = model(xb, grl if adversarial else 0.0)
            loss = class_loss(yp, yb)
            if adversarial:
                loss = loss + class_loss(dp, db)
            loss.backward()
            optimizer.step()
    return model, scaler


def score(model, scaler, x_test, y_test, classes):
    model.eval()
    with torch.no_grad():
        logits, _ = model(torch.from_numpy(scaler.transform(x_test).astype(np.float32)))
        pred = logits.argmax(dim=1).numpy()
    return float(f1_score(y_test, pred, labels=list(range(classes)), average="macro", zero_division=0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="research-os/artifacts/nbaiot-device-robust-baselines.json")
    ap.add_argument("--rows-per-cell", type=int, default=600)
    ap.add_argument("--row-offset", type=int, default=0)
    ap.add_argument("--epochs", type=int, default=20)
    ap.add_argument("--seed", type=int, default=20260930)
    ap.add_argument("--grl", type=float, default=0.1)
    args = ap.parse_args()
    started = time.time()
    x, y, d, labels = load_common(args.rows_per_cell, args.row_offset)
    indices = np.arange(len(x))
    strata = np.array([f"{di}:{yi}" for di, yi in zip(d, y)])
    random_train, random_test = train_test_split(indices, test_size=0.25, random_state=args.seed, stratify=strata)
    results = {"random_row": {}, "lodo": {}}
    for adversarial, name in [(False, "mlp"), (True, "device_adversarial_mlp")]:
        model, scaler = train_model(x[random_train], y[random_train], d[random_train], len(labels), 9, args.seed, adversarial, args.epochs, args.grl)
        results["random_row"][name] = {"macro_f1": score(model, scaler, x[random_test], y[random_test], len(labels))}
        folds = []
        for held in range(9):
            train = d != held
            test = d == held
            model, scaler = train_model(x[train], y[train], d[train], len(labels), 9, args.seed + held + 1, adversarial, args.epochs, args.grl)
            folds.append({"held_device": held + 1, "macro_f1": score(model, scaler, x[test], y[test], len(labels))})
        results["lodo"][name] = folds
    for name in results["random_row"]:
        vals = [f["macro_f1"] for f in results["lodo"][name]]
        results["summary"] = results.get("summary", {})
        results["summary"][name] = {
            "random_row_macro_f1": results["random_row"][name]["macro_f1"],
            "mean_lodo_macro_f1": float(np.mean(vals)),
            "gap": float(results["random_row"][name]["macro_f1"] - np.mean(vals)),
        }
    output = {
        "status": "exploratory_algorithm_preflight_not_novelty_claim",
        "scope": "offline N-BaIoT Kaggle-layout mirror; common-support rows; no leakage or causality claim",
        "protocol": {"rows_per_cell": args.rows_per_cell, "row_offset": args.row_offset, "epochs": args.epochs, "seed": args.seed, "grl": args.grl, "labels": labels},
        "models": {"mlp": "supervised encoder/classifier", "device_adversarial_mlp": "encoder/classifier plus gradient-reversal device head; DANN-style baseline"},
        "results": results,
        "runtime_seconds": time.time() - started,
    }
    Path(args.output).write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
