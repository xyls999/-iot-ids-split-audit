#!/usr/bin/env python3
"""Prefix-only domain quantile normalization on IoT-23."""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
import numpy as np,pandas as pd
from sklearn.ensemble import ExtraTreesClassifier,HistGradientBoostingClassifier
from sklearn.metrics import confusion_matrix,f1_score
from sklearn.preprocessing import QuantileTransformer
import run_iot23_scenario_heldout as base

def metric(y,p):
 cm=confusion_matrix(y,p,labels=[0,1]);fp=cm[0,1];tn=cm[0,0]
 return {'macro_f1':float(f1_score(y,p,average='macro',zero_division=0)),'fpr':float(fp/(fp+tn)) if fp+tn else 0.0}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--max-per-class',type=int,default=1000);ap.add_argument('--seed',type=int,default=20260930);ap.add_argument('--fractions',default='0,0.05,0.10,0.25');ap.add_argument('--output',default='research-os/artifacts/iot23-prefix-quantile-tta-results.json');args=ap.parse_args();start=time.time();loaded={n:base.read_scenario(n,base.DATA/fn,args.max_per_class,args.seed) for n,(fn,_) in base.SCENARIOS.items()};usable=[n for n,(x,y) in loaded.items() if len(np.unique(y))==2];rows=[]
 for held in usable:
  train_names=[n for n in usable if n!=held]+[n for n in base.SCENARIOS if n not in usable];Xtr=[];ytr=[]
  for n in train_names:Xn,yn=loaded[n];Xtr.extend(Xn);ytr.extend(yn)
  Xtr=pd.DataFrame(Xtr);Xall,yall=loaded[held];Xall=pd.DataFrame(Xall);prep=base.make_preprocessor();Atr=prep.fit_transform(Xtr);Ball=prep.transform(Xall);num=len(base.NUM);qt_s=QuantileTransformer(n_quantiles=min(1000,len(Atr)),output_distribution='normal',random_state=args.seed);Aq=qt_s.fit_transform(Atr[:,:num]);
  for frac in [float(v) for v in args.fractions.split(',')]:
   n=int(frac*len(Ball));E=Ball[n:];ye=yall[n:]
   if n:
    qt_t=QuantileTransformer(n_quantiles=min(1000,n),output_distribution='normal',random_state=args.seed);qt_t.fit(Ball[:n,:num]);Eq=E.copy();Eq[:,:num]=qt_t.transform(E[:,:num])
   else:Eq=E
   for name,est in [('extra_trees',ExtraTreesClassifier(n_estimators=200,max_features='sqrt',class_weight='balanced',n_jobs=-1,random_state=args.seed)),('hist_gradient_boosting',HistGradientBoostingClassifier(max_iter=150,max_leaf_nodes=31,l2_regularization=1e-3,random_state=args.seed))]:
    if n: est.fit(np.column_stack([Aq,Atr[:,num:]]),ytr);p=est.predict(Eq)
    else: est.fit(Atr,ytr);p=est.predict(E)
    rows.append({'held_scenario':held,'adapt_fraction':frac,'adapt_rows':n,'model':name,'metrics':metric(ye,p)})
 fractions=[float(v) for v in args.fractions.split(',')];summary={f'{m}:{f}':{'mean_macro_f1':float(np.mean([r['metrics']['macro_f1'] for r in rows if r['model']==m and r['adapt_fraction']==f])),'std_macro_f1':float(np.std([r['metrics']['macro_f1'] for r in rows if r['model']==m and r['adapt_fraction']==f])),'mean_fpr':float(np.mean([r['metrics']['fpr'] for r in rows if r['model']==m and r['adapt_fraction']==f]))} for m in ['extra_trees','hist_gradient_boosting'] for f in fractions}
 out={'status':'prefix_domain_quantile_tta_scenario_proxy_not_device_heldout','protocol':{'max_per_class':args.max_per_class,'fractions':fractions,'target_labels_unused':True},'summary':summary,'folds':rows,'runtime_seconds':time.time()-start};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
