"""Prototype: remove features that a benign device classifier finds device-specific."""
from pathlib import Path
import json, zipfile
import numpy as np, pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import f1_score, recall_score, roc_auc_score, confusion_matrix
ROOT=Path(__file__).resolve().parents[1]; ZIP=ROOT/'data/raw/n-baiot-original-kaggle.zip'; OUT=ROOT/'artifacts/nbaiot-original-preflight/device-invariant-probe.json'; SEED=20260930

def first(z,name,n,start=0):
 out=[]; need=n
 with z.open(name) as f:
  for ch in pd.read_csv(f,chunksize=50000):
   if start>=len(ch):start-=len(ch);continue
   q=ch.iloc[start:start+need];out.append(q);need-=len(q);start=0
   if need<=0:break
 return pd.concat(out,ignore_index=True).replace([np.inf,-np.inf],np.nan) if out else pd.DataFrame()
def attacks(z,d,n=300):
 arr=[]
 for name in sorted(x for x in z.namelist() if x.startswith(f'dataset/{d}.') and x.endswith('.csv') and not x.endswith('.benign.csv')):arr.append(first(z,name,n))
 return pd.concat(arr,ignore_index=True)
def met(y,s):
 p=(s>=.5).astype(int);tn,fp,fn,tp=confusion_matrix(y,p,labels=[0,1]).ravel();return {'f1':float(f1_score(y,p,average='macro',zero_division=0)),'recall':float(recall_score(y,p,zero_division=0)),'fpr':float(fp/(fp+tn)),'auroc':float(roc_auc_score(y,s))}
with zipfile.ZipFile(ZIP) as z:
 data={}
 for d in range(1,10):
  b=first(z,f'dataset/{d}.benign.csv',8000); a=attacks(z,d,300); data[d]=(b,a)
 results=[]
 for target in range(1,10):
  src=[d for d in range(1,10) if d!=target]
  sb=pd.concat([data[d][0] for d in src]); sy=np.concatenate([np.full(len(data[d][0]),d) for d in src])
  sa=pd.concat([data[d][0].iloc[:5000] for d in src]+[data[d][1] for d in src]); ay=np.concatenate([np.zeros(sum(len(data[d][0].iloc[:5000]) for d in src),int),np.ones(sum(len(data[d][1]) for d in src),int)])
  tb,ta=data[target]; tx=pd.concat([tb.iloc[5000:8000],ta]);ty=np.concatenate([np.zeros(len(tb.iloc[5000:8000]),int),np.ones(len(ta),int)])
  dev=Pipeline([('i',SimpleImputer(strategy='median')),('m',RandomForestClassifier(n_estimators=80,max_depth=18,n_jobs=-1,random_state=SEED))]);dev.fit(sb,sy); imp=dev.named_steps['m'].feature_importances_; cols=np.array(sb.columns); order=np.argsort(imp)[::-1]
  for k in [0,10,20,40]:
   drop=set(cols[order[:k]]); keep=[c for c in cols if c not in drop]
   clf=Pipeline([('i',SimpleImputer(strategy='median')),('m',RandomForestClassifier(n_estimators=80,max_depth=18,n_jobs=-1,class_weight='balanced',random_state=SEED))]);clf.fit(sa[keep],ay);score=clf.predict_proba(tx[keep])[:,1];results.append({'target_device':target,'removed_top_device_features':k,'remaining_features':len(keep),'device_classifier_source_accuracy':float(dev.score(sb,sy)),'removed_feature_names':list(cols[order[:k]]),'metrics':met(ty,score)})
OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps({'results':results},ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'results':results},ensure_ascii=False,indent=2))
