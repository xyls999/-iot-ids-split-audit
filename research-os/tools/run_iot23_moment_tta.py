#!/usr/bin/env python3
"""Unlabeled target-moment alignment for IoT-23 scenario-held-out trees."""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier,HistGradientBoostingClassifier
from sklearn.metrics import confusion_matrix,f1_score
from sklearn.pipeline import Pipeline
import run_iot23_scenario_heldout as base

def metric(y,p):
 cm=confusion_matrix(y,p,labels=[0,1]);fp=cm[0,1];tn=cm[0,0]
 return {'macro_f1':float(f1_score(y,p,average='macro',zero_division=0)),'fpr':float(fp/(fp+tn)) if fp+tn else 0.0}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--max-per-class',type=int,default=1000);ap.add_argument('--output',default='research-os/artifacts/iot23-moment-tta-results.json');args=ap.parse_args();start=time.time();loaded={n:base.read_scenario(n,base.DATA/fn,args.max_per_class,20260930) for n,(fn,_) in base.SCENARIOS.items()};usable=[n for n,(x,y) in loaded.items() if len(np.unique(y))==2];rows=[]
 for held in usable:
  train_names=[n for n in usable if n!=held]+[n for n in base.SCENARIOS if n not in usable];Xtr=[];ytr=[]
  for n in train_names:Xn,yn=loaded[n];Xtr.extend(Xn);ytr.extend(yn)
  Xtr=pd.DataFrame(Xtr);Xte,yte=loaded[held];Xte=pd.DataFrame(Xte);prep=base.make_preprocessor();Atr=prep.fit_transform(Xtr);Bte=prep.transform(Xte);num=len(base.NUM);sm=Atr[:,:num].mean(0);ss=Atr[:,:num].std(0);tm=Bte[:,:num].mean(0);ts=Bte[:,:num].std(0);ss=np.where(ss<1e-6,1,ss);ts=np.where(ts<1e-6,1,ts);Bal=Bte.copy();Bal[:,:num]=(Bte[:,:num]-tm)/ts*ss+sm
  for name,est in [('extra_trees',ExtraTreesClassifier(n_estimators=200,max_features='sqrt',class_weight='balanced',n_jobs=-1,random_state=20260930)),('hist_gradient_boosting',HistGradientBoostingClassifier(max_iter=150,max_leaf_nodes=31,l2_regularization=1e-3,random_state=20260930))]:
   est.fit(Atr,ytr);p0=est.predict(Bte);p1=est.predict(Bal);rows.extend([{'held_scenario':held,'model':name,'variant':'source_only','metrics':metric(yte,p0)},{'held_scenario':held,'model':name,'variant':'target_moment_align','metrics':metric(yte,p1)}])
 summary={}
 for v in ['source_only','target_moment_align']:
  for m in ['extra_trees','hist_gradient_boosting']:
   z=[r['metrics']['macro_f1'] for r in rows if r['variant']==v and r['model']==m];summary[f'{m}:{v}']={'mean_macro_f1':float(np.mean(z)),'std_macro_f1':float(np.std(z)),'mean_fpr':float(np.mean([r['metrics']['fpr'] for r in rows if r['variant']==v and r['model']==m]))}
 out={'status':'unlabeled_target_moment_tta_scenario_proxy_not_device_heldout','protocol':{'max_per_class':args.max_per_class,'target_labels_unused_for_alignment':True,'numeric_features':base.NUM,'categorical_features':base.CAT},'summary':summary,'folds':rows,'runtime_seconds':time.time()-start};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
