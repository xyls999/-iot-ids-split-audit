#!/usr/bin/env python3
"""Offline TTA preflight on the N-BaIoT mirror.

Target-device labels are never used during adaptation. This is an exploratory
baseline comparison, not a novelty claim.
"""
from __future__ import annotations

import argparse
import copy
import json
import random
import time
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import f1_score
from sklearn.preprocessing import StandardScaler
from torch import nn

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT / "data/raw/n-baiot-original-kaggle.zip"


def seed_all(seed):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)


def label_of(member, device):
    name = Path(member).name
    return name[len(f"{device}."):-4]


def read_first(zipped, member, n, start=0):
    out=[]; rem=n; skip=start
    with zipped.open(member) as h:
        for chunk in pd.read_csv(h,chunksize=50000):
            if skip >= len(chunk): skip -= len(chunk); continue
            if skip: chunk=chunk.iloc[skip:]; skip=0
            piece=chunk.iloc[:rem]; out.append(piece); rem-=len(piece)
            if rem<=0: break
    if rem>0: raise ValueError(member)
    return pd.concat(out,ignore_index=True).replace([np.inf,-np.inf],np.nan)


def load_data(rows=600, offset=0):
    with zipfile.ZipFile(ZIP) as z:
        devices=list(range(1,10))
        members={d:sorted(x for x in z.namelist() if x.startswith(f"dataset/{d}.") and x.endswith('.csv')) for d in devices}
        maps={d:{label_of(x,d):x for x in members[d]} for d in devices}
        labels=sorted(set.intersection(*(set(m) for m in maps.values())))
        xs=[];ys=[];ds=[]
        for d in devices:
            for yi,label in enumerate(labels):
                frame=read_first(z,maps[d][label],rows,offset)
                xs.append(frame); ys.append(np.full(len(frame),yi,dtype=np.int64)); ds.append(np.full(len(frame),d-1,dtype=np.int64))
    x=pd.concat(xs,ignore_index=True).fillna(0.0).to_numpy(dtype=np.float32)
    return x,np.concatenate(ys),np.concatenate(ds),labels


class BNMLP(nn.Module):
    def __init__(self, dim, classes):
        super().__init__()
        self.net=nn.Sequential(nn.Linear(dim,64),nn.BatchNorm1d(64),nn.ReLU(),nn.Linear(64,32),nn.BatchNorm1d(32),nn.ReLU())
        self.head=nn.Linear(32,classes)
    def forward(self,x): return self.head(self.net(x))


def train_source(x,y,seed,epochs):
    seed_all(seed); model=BNMLP(x.shape[1],len(np.unique(y))); opt=torch.optim.Adam(model.parameters(),lr=1e-3,weight_decay=1e-5); lossfn=nn.CrossEntropyLoss()
    xt=torch.from_numpy(x); yt=torch.from_numpy(y)
    model.train()
    for _ in range(epochs):
        perm=torch.randperm(len(xt))
        for idx in perm.split(1024):
            opt.zero_grad(); loss=lossfn(model(xt[idx]),yt[idx]);loss.backward();opt.step()
    return model


def bn_layers(model): return [m for m in model.modules() if isinstance(m,nn.BatchNorm1d)]


def adapt(model, x_adapt, method, batch_size, entropy_threshold):
    if len(x_adapt)==0:return
    if method=='source_only':return
    if method in {'bn_adapt','bn_blend'}:
        old=[(m.running_mean.detach().clone(),m.running_var.detach().clone()) for m in bn_layers(model)]
        model.train()
        with torch.no_grad():
            for i in range(0,len(x_adapt),batch_size): model(torch.from_numpy(x_adapt[i:i+batch_size]))
        if method=='bn_blend':
            for m,(mean,var) in zip(bn_layers(model),old):
                m.running_mean.copy_(0.25*m.running_mean + 0.75*mean)
                m.running_var.copy_(0.25*m.running_var + 0.75*var)
        model.eval(); return
    # Tent updates BN affine parameters only; running stats are also updated.
    params=[]
    for layer in bn_layers(model):
        layer.train(); layer.weight.requires_grad_(True); layer.bias.requires_grad_(True); params += [layer.weight,layer.bias]
    param_ids={id(p) for p in params}
    for p in model.parameters():
        if id(p) not in param_ids: p.requires_grad_(False)
    opt=torch.optim.Adam(params,lr=1e-4)
    model.train()
    for i in range(0,len(x_adapt),batch_size):
        xb=torch.from_numpy(x_adapt[i:i+batch_size])
        logits=model(xb); prob=logits.softmax(1); ent=-(prob*prob.clamp_min(1e-8).log()).sum(1).mean()
        if method=='safe_tent' and float(ent.detach()) > entropy_threshold: continue
        opt.zero_grad(); ent.backward(); torch.nn.utils.clip_grad_norm_(params,1.0); opt.step()
    model.eval()


def score(model,x,y):
    model.eval();
    with torch.no_grad(): pred=model(torch.from_numpy(x)).argmax(1).numpy()
    return float(f1_score(y,pred,average='macro',zero_division=0))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='research-os/artifacts/nbaiot-tta-preflight.json');ap.add_argument('--epochs',type=int,default=20);ap.add_argument('--seed',type=int,default=20260930);ap.add_argument('--batch-size',type=int,default=128);ap.add_argument('--adapt-batches',default='0,1,5,10');ap.add_argument('--entropy-threshold',type=float,default=1.45);args=ap.parse_args()
    started=time.time(); x,y,d,labels=load_data(); scaler=StandardScaler(); methods=['source_only','target_zscore','target_robust','bn_adapt','bn_blend','tent','safe_tent']; ks=[int(v) for v in args.adapt_batches.split(',')]
    rows=[]
    for held in range(9):
        source=d!=held; target=d==held
        scaler.fit(x[source]); xs=scaler.transform(x[source]).astype(np.float32); xt=scaler.transform(x[target]).astype(np.float32); yt=y[target]
        # deterministic balanced target order: rows are already grouped by label in the archive load.
        # Build adaptation/evaluation slices per class so adaptation remains label-support balanced without labels being used by adapt().
        order=[]; class_indices=[np.flatnonzero(yt==c) for c in range(len(labels))]
        for k in range(max(len(v) for v in class_indices)):
            for v in class_indices:
                if k<len(v): order.append(v[k])
        order=np.asarray(order); xt=xt[order]; yt=yt[order]
        base=train_source(xs,y[source],args.seed+held,args.epochs)
        for k in ks:
            n=min(len(xt),k*args.batch_size); xa,xe=xt[:n],xt[n:]; ya,ye=yt[:n],yt[n:]
            for method in methods:
                model=copy.deepcopy(base); xeval=xe
                if method=='target_zscore' and len(xa):
                    mu=xa.mean(0); sd=xa.std(0); sd=np.where(sd<1e-3,1.0,sd); xeval=((xe-mu)/sd).astype(np.float32)
                elif method=='target_robust' and len(xa):
                    med=np.median(xa,0); mad=np.median(np.abs(xa-med),0)*1.4826; mad=np.where(mad<1e-3,1.0,mad); xeval=((xe-med)/mad).astype(np.float32)
                adapt(model,xa,method,args.batch_size,args.entropy_threshold); value=score(model,xeval,ye)
                rows.append({'held_device':held+1,'adapt_batches':k,'adapt_rows':int(n),'method':method,'macro_f1':value})
    summary={}
    for k in ks:
        summary[str(k)]={}
        for method in methods:
            vals=[r['macro_f1'] for r in rows if r['adapt_batches']==k and r['method']==method]
            summary[str(k)][method]={'mean_lodo_macro_f1':float(np.mean(vals)),'std_lodo_macro_f1':float(np.std(vals))}
    out={'status':'exploratory_tta_preflight_not_novelty_claim','scope':'offline N-BaIoT Kaggle-layout mirror; target labels are withheld during adaptation','protocol':{'labels':labels,'rows_per_cell':600,'epochs':args.epochs,'seed':args.seed,'batch_size':args.batch_size,'adapt_batches':ks,'entropy_threshold':args.entropy_threshold},'summary':summary,'folds':rows,'runtime_seconds':time.time()-started}
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True))

if __name__=='__main__':main()
