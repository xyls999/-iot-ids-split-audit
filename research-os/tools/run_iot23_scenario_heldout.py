#!/usr/bin/env python3
"""Offline IoT-23 scenario-held-out binary benchmark.

Scenario is an official capture-group identity, not a device identity. This
script must not be interpreted as device-held-out replication.
"""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesClassifier,HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import confusion_matrix,f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data/iot23-small'
SCENARIOS={
 'honeypot4':('CTU-Honeypot-Capture-4-1_bro_conn.log.labeled','benign'),
 'honeypot5':('CTU-Honeypot-Capture-5-1_bro_conn.log.labeled','benign'),
 'malware8':('CTU-IoT-Malware-Capture-8-1_bro_conn.log.labeled','mixed'),
 'malware20':('CTU-IoT-Malware-Capture-20-1_bro_conn.log.labeled','mixed'),
 'malware21':('CTU-IoT-Malware-Capture-21-1_bro_conn.log.labeled','mixed'),
 'malware34':('CTU-IoT-Malware-Capture-34-1_bro_conn.log.labeled','mixed'),
 'malware42':('CTU-IoT-Malware-Capture-42-1_bro_conn.log.labeled','mixed'),
 'malware44':('CTU-IoT-Malware-Capture-44-1_bro_conn.log.labeled','mixed'),
}
# Exclude ts/IP/UID to avoid capture and endpoint shortcuts.
NUM=['orig_p','resp_p','duration','orig_bytes','resp_bytes','missed_bytes','orig_pkts','orig_ip_bytes','resp_pkts','resp_ip_bytes']
CAT=['proto','service','conn_state','history']

def read_scenario(name,path,max_per_class,seed):
 rows=[]
 for line in path.read_text(errors='replace').splitlines():
  if not line or line.startswith('#'):continue
  t=line.split()
  if len(t)<22:continue
  label=t[-2].lower()
  if label not in ('benign','malicious'):continue
  try:
   vals={'orig_p':float(t[3]),'resp_p':float(t[5]),'duration':float(t[8]) if t[8]!='-' else np.nan,'orig_bytes':float(t[9]) if t[9]!='-' else np.nan,'resp_bytes':float(t[10]) if t[10]!='-' else np.nan,'missed_bytes':float(t[14]) if t[14]!='-' else np.nan,'orig_pkts':float(t[16]) if t[16]!='-' else np.nan,'orig_ip_bytes':float(t[17]) if t[17]!='-' else np.nan,'resp_pkts':float(t[18]) if t[18]!='-' else np.nan,'resp_ip_bytes':float(t[19]) if t[19]!='-' else np.nan,'proto':t[6],'service':t[7],'conn_state':t[11],'history':t[15]}
   rows.append((vals,1 if label=='malicious' else 0))
  except (ValueError,IndexError):continue
 rng=np.random.default_rng(seed);out=[]
 for cls in (0,1):
  a=[r for r in rows if r[1]==cls];rng.shuffle(a);out.extend(a[:max_per_class])
 X=[r[0] for r in out]; y=np.array([r[1] for r in out],dtype=int)
 return X,y

def make_preprocessor():
 return ColumnTransformer([('num',Pipeline([('impute',SimpleImputer(strategy='median'))]),NUM),('cat',Pipeline([('impute',SimpleImputer(strategy='most_frequent')),('onehot',OneHotEncoder(handle_unknown='ignore',sparse_output=False))]),CAT)])
def metric(y,p):
 cm=confusion_matrix(y,p,labels=[0,1]);fp=cm[0,1];tn=cm[0,0];return {'macro_f1':float(f1_score(y,p,average='macro',zero_division=0)),'fpr':float(fp/(fp+tn)) if fp+tn else 0.0,'n':int(len(y)),'positive_rate':float(np.mean(y))}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--max-per-class',type=int,default=1000);ap.add_argument('--seed',type=int,default=20260930);ap.add_argument('--output',default='research-os/artifacts/iot23-scenario-heldout-results.json');args=ap.parse_args();start=time.time();loaded={}
 for name,(fn,_) in SCENARIOS.items():loaded[name]=read_scenario(name,DATA/fn,args.max_per_class,args.seed)
 # Only mixed scenarios support both labels in the evaluation fold.
 usable=[n for n,(x,y) in loaded.items() if len(np.unique(y))==2]
 models=['extra_trees','hist_gradient_boosting'];folds=[]
 for held in usable:
  train_names=[n for n in usable if n!=held] + [n for n in SCENARIOS if n not in usable]
  Xtr=[];ytr=[];Xte,yte=loaded[held]
  for n in train_names:Xn,yn=loaded[n];Xtr.extend(Xn);ytr.extend(yn)
  Xtr=pd.DataFrame(Xtr); Xte=pd.DataFrame(Xte)
  for model_name in models:
   if model_name=='extra_trees':est=ExtraTreesClassifier(n_estimators=200,max_features='sqrt',class_weight='balanced',n_jobs=-1,random_state=args.seed)
   else:est=HistGradientBoostingClassifier(max_iter=150,max_leaf_nodes=31,l2_regularization=1e-3,random_state=args.seed)
   pipe=Pipeline([('prep',make_preprocessor()),('model',est)]);t=time.perf_counter();pipe.fit(Xtr,ytr);fit=time.perf_counter()-t;p=pipe.predict(Xte)
   folds.append({'held_scenario':held,'model':model_name,'metrics':metric(yte,p),'fit_seconds':fit,'train_rows':len(ytr),'test_rows':len(yte)})
 summary={m:{'mean_macro_f1':float(np.mean([r['metrics']['macro_f1'] for r in folds if r['model']==m])),'std_macro_f1':float(np.std([r['metrics']['macro_f1'] for r in folds if r['model']==m])),'mean_fpr':float(np.mean([r['metrics']['fpr'] for r in folds if r['model']==m]))} for m in models}
 out={'status':'external_scenario_heldout_not_device_heldout','scope':'official IoT-23 owner-hosted per-scenario conn.log.labeled files; scenario is capture-group proxy only','protocol':{'max_per_class':args.max_per_class,'seed':args.seed,'usable_mixed_scenarios':usable,'numeric_features':NUM,'categorical_features':CAT,'excluded_fields':['ts','uid','id.orig_h','id.resp_h']},'scenario_counts':{n:{'rows':int(len(v[1])),'positive_rate':float(np.mean(v[1]))} for n,v in loaded.items()},'summary':summary,'folds':folds,'runtime_seconds':time.time()-start};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
