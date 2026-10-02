#!/usr/bin/env python3
"""Offline device-held-out DG candidates; exploratory, no novelty claim."""
from __future__ import annotations
import argparse,json,random,time,zipfile
from pathlib import Path
import numpy as np,pandas as pd,torch
from sklearn.metrics import f1_score
from sklearn.preprocessing import StandardScaler
from torch import nn
ROOT=Path(__file__).resolve().parents[1]; ZIP=ROOT/'data/raw/n-baiot-original-kaggle.zip'

def seed(s): random.seed(s);np.random.seed(s);torch.manual_seed(s)
def lab(m,d):
 n=Path(m).name;return n[len(f'{d}.'):-4]
def read(z,m,n):
 out=[]; rem=n
 with z.open(m) as h:
  for c in pd.read_csv(h,chunksize=50000):
   out.append(c.iloc[:rem]);rem-=len(out[-1])
   if rem<=0:break
 return pd.concat(out,ignore_index=True).replace([np.inf,-np.inf],np.nan)
def load(rows):
 with zipfile.ZipFile(ZIP) as z:
  mm={d:sorted(v for v in z.namelist() if v.startswith(f'dataset/{d}.') and v.endswith('.csv')) for d in range(1,10)}
  mp={d:{lab(v,d):v for v in mm[d]} for d in mm}; labels=sorted(set.intersection(*(set(v) for v in mp.values())))
  X=[];Y=[];D=[]
  for d in range(1,10):
   for yi,l in enumerate(labels):
    f=read(z,mp[d][l],rows);X.append(f);Y.append(np.full(len(f),yi));D.append(np.full(len(f),d-1))
 x=pd.concat(X,ignore_index=True).fillna(0).to_numpy('float32');return x,np.concatenate(Y).astype('int64'),np.concatenate(D).astype('int64'),labels
class Net(nn.Module):
 def __init__(self,dim,c):
  super().__init__();self.enc=nn.Sequential(nn.Linear(dim,64),nn.ReLU(),nn.Linear(64,32),nn.ReLU());self.head=nn.Linear(32,c)
 def forward(self,x):return self.head(self.enc(x))
def coral(z,g,groups):
 cs=[]
 for d in groups:
  a=z[g==d]
  if len(a)>2:
   a=a-a.mean(0,keepdim=True);cs.append(a.T@a/(len(a)-1))
 if len(cs)<2:return z.sum()*0
 return sum((cs[i]-cs[j]).pow(2).mean() for i in range(len(cs)) for j in range(i+1,len(cs)))/(len(cs)*(len(cs)-1)/2)
def train(x,y,g,c,method,seed0,epochs,lam):
 seed(seed0);sc=StandardScaler().fit(x);xs=sc.transform(x).astype('float32');xt=torch.from_numpy(xs);yt=torch.from_numpy(y);gt=torch.from_numpy(g);m=Net(xs.shape[1],c);opt=torch.optim.Adam(m.parameters(),lr=1e-3,weight_decay=1e-5);ce=nn.CrossEntropyLoss(reduction='none'); weights=torch.ones(9)
 for _ in range(epochs):
  m.train()
  for ix in torch.randperm(len(xt)).split(1024):
   xb,yb,gb=xt[ix],yt[ix],gt[ix];opt.zero_grad(); logits=m(xb); losses=ce(logits,yb)
   if method=='mlp': loss=losses.mean()
   elif method=='coral': loss=losses.mean()+lam*coral(m.enc(xb),gb,sorted(set(gb.numpy())))
   elif method=='groupdro':
    present=sorted(set(gb.numpy())); gl=torch.stack([losses[gb==d0].mean() for d0 in present]); weights[present]*=torch.exp(0.05*gl.detach());weights[present]/=weights[present].sum();loss=(weights[present]*gl).sum()
   elif method=='mixup':
    perm=torch.randperm(len(xb));a=torch.rand(1).item()*0.5+0.5; mix=a*xb+(1-a)*xb[perm]; loss=a*ce(m(mix),yb).mean()+(1-a)*ce(m(mix),yb[perm]).mean()
   loss.backward();opt.step()
 return m,sc
def score(m,sc,x,y):
 m.eval();
 with torch.no_grad():p=m(torch.from_numpy(sc.transform(x).astype('float32'))).argmax(1).numpy()
 return float(f1_score(y,p,average='macro',zero_division=0))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--rows',type=int,default=600);ap.add_argument('--epochs',type=int,default=8);ap.add_argument('--seed',type=int,default=20260930);ap.add_argument('--output',default='research-os/artifacts/nbaiot-dg-candidates.json');args=ap.parse_args();t=time.time();x,y,d,labels=load(args.rows);methods=['mlp','coral','groupdro','mixup'];folds=[]
 for held in range(9):
  tr=d!=held;te=d==held
  for j,method in enumerate(methods):
   m,sc=train(x[tr],y[tr],d[tr],len(labels),method,args.seed+held*10+j,args.epochs,0.01);folds.append({'held_device':held+1,'method':method,'macro_f1':score(m,sc,x[te],y[te])})
 summary={m:{'mean_lodo_macro_f1':float(np.mean([r['macro_f1'] for r in folds if r['method']==m])),'std_lodo_macro_f1':float(np.std([r['macro_f1'] for r in folds if r['method']==m]))} for m in methods}
 out={'status':'exploratory_dg_preflight_not_novelty_claim','protocol':{'rows_per_cell':args.rows,'epochs':args.epochs,'seed':args.seed,'labels':labels,'coral_lambda':0.01},'summary':summary,'folds':folds,'runtime_seconds':time.time()-t};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
