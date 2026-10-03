#!/usr/bin/env python3
"""Unlabeled per-domain quantile normalization for IoT-23 scenarios."""
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
 ap=argparse.ArgumentParser();ap.add_argument('--max-per-class',type=int,default=1000);ap.add_argument('--output',default='research-os/artifacts/iot23-quantile-tta-results.json');args=ap.parse_args();start=time.time();loaded={n:base.read_scenario(n,base.DATA/fn,args.max_per_class,20260930) for n,(fn,_) in base.SCENARIOS.items()};usable=[n for n,(x,y) in loaded.items() if len(np.unique(y))==2];rows=[]
 for held in usable:
  train_names=[n for n in usable if n!=held]+[n for n in base.SCENARIOS if n not in usable];Xtr=[];ytr=[]
  for n in train_names:Xn,yn=loaded[n];Xtr.extend(Xn);ytr.extend(yn)
  Xtr=pd.DataFrame(Xtr);Xte,yte=loaded[held];Xte=pd.DataFrame(Xte);prep=base.make_preprocessor();Atr=prep.fit_transform(Xtr);Bte=prep.transform(Xte);num=len(base.NUM);qt_s=QuantileTransformer(n_quantiles=min(1000,len(Atr)),output_distribution='normal',random_state=20260930);qt_t=QuantileTransformer(n_quantiles=min(1000,len(Bte)),output_distribution='normal',random_state=20260930);Aq=Atr.copy();Bq=Bte.copy();Aq[:,:num]=qt_s.fit_transform(Atr[:,:num]);Bq[:,:num]=qt_t.fit_transform(Bte[:,:num]);
  for name,est in [('extra_trees',ExtraTreesClassifier(n_estimators=200,max_features='sqrt',class_weight='balanced',n_jobs=-1,random_state=20260930)),('hist_gradient_boosting',HistGradientBoostingClassifier(max_iter=150,max_leaf_nodes=31,l2_regularization=1e-3,random_state=20260930))]:
   est.fit(Atr,ytr);p0=est.predict(Bte);est.fit(Aq,ytr);p1=est.predict(Bq);rows.extend([{'held_scenario':held,'model':name,'variant':'source_only','metrics':metric(yte,p0)},{'held_scenario':held,'model':name,'variant':'domain_quantile','metrics':metric(yte,p1)}])
 summary={f'{m}:{v}':{'mean_macro_f1':float(np.mean([r['metrics']['macro_f1'] for r in rows if r['model']==m and r['variant']==v])),'std_macro_f1':float(np.std([r['metrics']['macro_f1'] for r in rows if r['model']==m and r['variant']==v])),'mean_fpr':float(np.mean([r['metrics']['fpr'] for r in rows if r['model']==m and r['variant']==v]))} for m in ['extra_trees','hist_gradient_boosting'] for v in ['source_only','domain_quantile']}
 out={'status':'unlabeled_domain_quantile_tta_scenario_proxy_not_device_heldout','protocol':{'max_per_class':args.max_per_class,'target_labels_unused':True,'numeric_features':base.NUM},'summary':summary,'folds':rows,'runtime_seconds':time.time()-start};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
