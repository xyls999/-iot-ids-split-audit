from pathlib import Path
import json, zipfile, time, pickle
import numpy as np, pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, recall_score, roc_auc_score, confusion_matrix
ROOT=Path(__file__).resolve().parents[1]; ZIP=ROOT/'data/raw/n-baiot-final-kaggle.zip'; OUT=ROOT/'artifacts/nbaiot-preflight/constrained-results.json'; SEED=20260929; MAX=2000

def load(z,name):
 chunks=[]
 with z.open(name) as f:
  for k,ch in enumerate(pd.read_csv(f,chunksize=100000)):
   y=(ch.pop('Label').astype(str).str.upper()!='BENIGN').astype(int).to_numpy(); ch=ch.replace([np.inf,-np.inf],np.nan); ids=[]
   for lab in [0,1]:
    q=np.flatnonzero(y==lab); rng=np.random.default_rng(SEED+k+lab+len(name)); ids.extend(rng.choice(q,min(len(q),5000),False))
   chunks.append((ch.iloc[ids],y[ids]))
 x=pd.concat([a for a,b in chunks],ignore_index=True); y=np.concatenate([b for a,b in chunks]);
 out=[]
 for lab in [0,1]:
  q=np.flatnonzero(y==lab); rng=np.random.default_rng(SEED+lab+len(name)*3); out.extend(rng.choice(q,min(len(q),MAX),False))
 out=np.array(out); np.random.default_rng(SEED+len(name)).shuffle(out); return x.iloc[out].reset_index(drop=True),y[out]
def met(y,p,s):
 tn,fp,fn,tp=confusion_matrix(y,p,labels=[0,1]).ravel(); return {'f1':float(f1_score(y,p,average='macro',zero_division=0)),'recall':float(recall_score(y,p,zero_division=0)),'fpr':float(fp/(fp+tn)),'auroc':float(roc_auc_score(y,s))}
with zipfile.ZipFile(ZIP) as z:
 names=sorted(n for n in z.namelist() if n.endswith('.csv')); groups={n:load(z,n) for n in names}
res=[]
for target in names:
 src=[n for n in names if n!=target]; xs=pd.concat([groups[n][0] for n in src]); ys=np.concatenate([groups[n][1] for n in src]); xt,yt=groups[target]; b=np.flatnonzero(yt==0); rng=np.random.default_rng(SEED+len(target)); rng.shuffle(b); cal=b[:max(1,len(b)//5)]; test=np.concatenate([b[max(1,len(b)//5):],np.flatnonzero(yt==1)])
 for name,model in [('logistic_regression',Pipeline([('i',SimpleImputer(strategy='median')),('s',StandardScaler()),('m',LogisticRegression(max_iter=300,class_weight='balanced',random_state=SEED))])),('random_forest',Pipeline([('i',SimpleImputer(strategy='median')),('m',RandomForestClassifier(n_estimators=80,max_depth=16,n_jobs=-1,class_weight='balanced',random_state=SEED))]))]:
  model.fit(xs,ys); src_score=model.predict_proba(xs)[:,1]; tar=model.predict_proba(xt.iloc[test])[:,1]; calscore=model.predict_proba(xt.iloc[cal])[:,1]
  attack_src=src_score[ys==1]; src_thr=float(np.quantile(attack_src,.05)); tgt_thr=float(np.quantile(calscore,.95)); thr=min(src_thr,tgt_thr); p=(tar>=thr).astype(int)
  res.append({'target':target,'model':name,'source_recall_threshold':src_thr,'target_benign_q95':tgt_thr,'constrained_threshold':thr,'metrics':met(yt[test],p,tar)})
OUT.write_text(json.dumps({'groups':{n:{'rows':len(y),'benign':int((y==0).sum()),'attack':int((y==1).sum())} for n,(x,y) in groups.items()},'results':res},ensure_ascii=False,indent=2))
print(json.dumps({'results':res},ensure_ascii=False,indent=2))
