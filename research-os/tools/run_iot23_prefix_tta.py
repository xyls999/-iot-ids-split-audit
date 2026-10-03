#!/usr/bin/env python3
"""Prefix-only unlabeled moment alignment on IoT-23 scenario streams."""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
import numpy as np,pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import confusion_matrix,f1_score
import run_iot23_scenario_heldout as base

def metric(y,p):
 cm=confusion_matrix(y,p,labels=[0,1]);fp=cm[0,1];tn=cm[0,0]
 return {'macro_f1':float(f1_score(y,p,average='macro',zero_division=0)),'fpr':float(fp/(fp+tn)) if fp+tn else 0.0,'n':int(len(y))}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--max-per-class',type=int,default=1000);ap.add_argument('--adapt-fractions',default='0,0.05,0.10,0.25');ap.add_argument('--output',default='research-os/artifacts/iot23-prefix-tta-results.json');args=ap.parse_args();start=time.time();loaded={n:base.read_scenario(n,base.DATA/fn,args.max_per_class,20260930) for n,(fn,_) in base.SCENARIOS.items()};usable=[n for n,(x,y) in loaded.items() if len(np.unique(y))==2];rows=[]
 for held in usable:
  train_names=[n for n in usable if n!=held]+[n for n in base.SCENARIOS if n not in usable];Xtr=[];ytr=[]
  for n in train_names:Xn,yn=loaded[n];Xtr.extend(Xn);ytr.extend(yn)
  Xtr=pd.DataFrame(Xtr);prep=base.make_preprocessor();Atr=prep.fit_transform(Xtr);num=len(base.NUM);sm=Atr[:,:num].mean(0);ss=Atr[:,:num].std(0);ss=np.where(ss<1e-6,1,ss);est=HistGradientBoostingClassifier(max_iter=150,max_leaf_nodes=31,l2_regularization=1e-3,random_state=20260930);est.fit(Atr,ytr)
  Xall,yall=loaded[held];Xall=pd.DataFrame(Xall);Ball=prep.transform(Xall)
  for frac in [float(v) for v in args.adapt_fractions.split(',')]:
   n=int(frac*len(Ball))
   A=Ball[:n,:num] if n else None;E=Ball[n:];ye=yall[n:]
   if n:
    tm=A.mean(0);ts=A.std(0);ts=np.where(ts<1e-6,1,ts);E2=E.copy();E2[:,:num]=(E[:,:num]-tm)/ts*ss+sm
   else:E2=E
   rows.append({'held_scenario':held,'adapt_fraction':frac,'adapt_rows':n,'metrics':metric(ye,est.predict(E2)),'eval_rows':len(ye)})
 fractions=[float(v) for v in args.adapt_fractions.split(',')]
 summary={str(frac):{'mean_macro_f1':float(np.mean([r['metrics']['macro_f1'] for r in rows if r['adapt_fraction']==frac])),'std_macro_f1':float(np.std([r['metrics']['macro_f1'] for r in rows if r['adapt_fraction']==frac])),'mean_fpr':float(np.mean([r['metrics']['fpr'] for r in rows if r['adapt_fraction']==frac]))} for frac in fractions}
 out={'status':'prefix_only_unlabeled_tta_scenario_proxy_not_device_heldout','protocol':{'max_per_class':args.max_per_class,'adapt_fractions':[float(v) for v in args.adapt_fractions.split(',')],'target_labels_unused':True,'model':'HistGradientBoosting'},'summary':summary,'folds':rows,'runtime_seconds':time.time()-start};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
