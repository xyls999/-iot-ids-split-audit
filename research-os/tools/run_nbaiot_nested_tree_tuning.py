#!/usr/bin/env python3
"""Nested device-held-out tuning for tree candidates; no target-device tuning."""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier,HistGradientBoostingClassifier
from sklearn.metrics import f1_score
import run_nbaiot_device_robust_baselines as source

def make(name,seed):
 if name=='et_sqrt': return ExtraTreesClassifier(n_estimators=200,max_features='sqrt',min_samples_leaf=1,class_weight='balanced',n_jobs=-1,random_state=seed)
 if name=='et_half': return ExtraTreesClassifier(n_estimators=200,max_features=0.5,min_samples_leaf=1,class_weight='balanced',n_jobs=-1,random_state=seed)
 if name=='et_leaf2': return ExtraTreesClassifier(n_estimators=300,max_features='sqrt',min_samples_leaf=2,class_weight='balanced',n_jobs=-1,random_state=seed)
 if name=='hgb31': return HistGradientBoostingClassifier(max_iter=150,max_leaf_nodes=31,l2_regularization=1e-3,random_state=seed)
 if name=='hgb63': return HistGradientBoostingClassifier(max_iter=220,max_leaf_nodes=63,learning_rate=0.07,l2_regularization=1e-3,random_state=seed)
 raise ValueError(name)

def predict(xtr,ytr,xte,name,seed):
 m=make(name,seed);m.fit(xtr,ytr);return m.predict_proba(xte)
def evalp(y,p):return float(f1_score(y,p.argmax(1),average='macro',zero_division=0))
def score_candidate(xtr,ytr,gtr,xv,yv,gv,name,seed):
 if name.startswith('blend'):
  _,a,b,w=name.split(':');pa=predict(xtr,ytr,xv,a,seed);pb=predict(xtr,ytr,xv,b,seed+77);return evalp(yv,float(w)*pa+(1-float(w))*pb)
 return evalp(yv,predict(xtr,ytr,xv,name,seed))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--rows-per-cell',type=int,default=600);ap.add_argument('--row-offset',type=int,default=0);ap.add_argument('--seed',type=int,default=20260930);ap.add_argument('--output',default='research-os/artifacts/nbaiot-nested-tree-tuning.json');args=ap.parse_args();start=time.time();x,y,d,labels=source.load_common(args.rows_per_cell,args.row_offset)
 candidates=['et_sqrt','et_half','et_leaf2','hgb31','hgb63','blend:et_sqrt:hgb31:0.5','blend:et_sqrt:hgb31:0.7']
 outer=[]
 for held in range(9):
  srcdev=[q for q in range(9) if q!=held]; inner={c:[] for c in candidates}
  for val in srcdev:
   tr=(d!=held)&(d!=val);va=d==val
   for j,c in enumerate(candidates): inner[c].append(score_candidate(x[tr],y[tr],d[tr],x[va],y[va],d[va],c,args.seed+held*100+val*10+j))
  means={c:float(np.mean(v)) for c,v in inner.items()}; chosen=max(candidates,key=lambda c:means[c]); tr=d!=held;te=d==held
  if chosen.startswith('blend'):
   _,a,b,w=chosen.split(':');p=float(w)*predict(x[tr],y[tr],x[te],a,args.seed+held)+(1-float(w))*predict(x[tr],y[tr],x[te],b,args.seed+held+77)
  else:p=predict(x[tr],y[tr],x[te],chosen,args.seed+held)
  outer.append({'held_device':held+1,'selected':chosen,'inner_mean_macro_f1':means,'outer_macro_f1':evalp(y[te],p)})
 summary={'mean_outer_macro_f1':float(np.mean([r['outer_macro_f1'] for r in outer])),'std_outer_macro_f1':float(np.std([r['outer_macro_f1'] for r in outer])),'selection_counts':{c:sum(r['selected']==c for r in outer) for c in candidates}}
 out={'status':'nested_device_heldout_tuning_no_target_device_tuning','protocol':{'rows_per_cell':args.rows_per_cell,'row_offset':args.row_offset,'seed':args.seed,'labels':labels,'inner_selection':'mean Macro-F1 over source-device validation folds'},'candidates':candidates,'summary':summary,'outer_folds':outer,'runtime_seconds':time.time()-start};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
