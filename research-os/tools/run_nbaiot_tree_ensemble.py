#!/usr/bin/env python3
"""Offline device-held-out tree ensemble benchmark for N-BaIoT.

This is an exploratory algorithm benchmark. It does not make a novelty claim.
"""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier,HistGradientBoostingClassifier
from sklearn.metrics import f1_score,confusion_matrix
import run_nbaiot_device_robust_baselines as source

ROOT=Path(__file__).resolve().parents[1]

def metrics(y,p,classes):
 cm=confusion_matrix(y,p,labels=list(range(classes)))
 per=f1_score(y,p,labels=list(range(classes)),average=None,zero_division=0)
 # macro FPR: false positives / all actual negatives, averaged over classes.
 fprs=[]
 for i in range(classes):
  fp=cm[:,i].sum()-cm[i,i]; tn=cm.sum()-cm[i,:].sum()-cm[:,i].sum()+cm[i,i]
  fprs.append(float(fp/(fp+tn)) if fp+tn else 0.0)
 return {'macro_f1':float(np.mean(per)),'per_class_f1':[float(v) for v in per],'macro_fpr':float(np.mean(fprs))}

def run_fold(x,y,d,held,seed,trees,leaf):
 tr=d!=held;te=d==held;fit0=time.perf_counter()
 et=ExtraTreesClassifier(n_estimators=trees,max_features='sqrt',min_samples_leaf=leaf,class_weight='balanced',n_jobs=-1,random_state=seed)
 hg=HistGradientBoostingClassifier(max_iter=150,max_leaf_nodes=31,l2_regularization=1e-3,min_samples_leaf=leaf,random_state=seed)
 et.fit(x[tr],y[tr]);hg.fit(x[tr],y[tr]);fit_seconds=time.perf_counter()-fit0
 p0=et.predict_proba(x[te]);p1=hg.predict_proba(x[te]);inf0=time.perf_counter();p=((p0+p1)/2).argmax(1);infer_seconds=time.perf_counter()-inf0
 return {'held_device':held+1,'seed':seed,'metrics':metrics(y[te],p,len(np.unique(y))),'fit_seconds':fit_seconds,'ensemble_inference_seconds':infer_seconds,'extra_trees_estimators':trees,'extra_trees_nodes':int(sum(t.tree_.node_count for t in et.estimators_)),'hgb_iterations':150}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--rows-per-cell',type=int,default=600);ap.add_argument('--row-offset',type=int,default=0);ap.add_argument('--seeds',default='20260930,20260931,20260932,20260933,20260934');ap.add_argument('--trees',type=int,default=200);ap.add_argument('--min-leaf',type=int,default=1);ap.add_argument('--output',default='research-os/artifacts/nbaiot-tree-ensemble-results.json');args=ap.parse_args();start=time.time()
 x,y,d,labels=source.load_common(args.rows_per_cell,args.row_offset); rows=[]
 for s in [int(v) for v in args.seeds.split(',')]:
  for held in range(9): rows.append(run_fold(x,y,d,held,s,args.trees,args.min_leaf))
 vals=[r['metrics']['macro_f1'] for r in rows]; fprs=[r['metrics']['macro_fpr'] for r in rows]
 out={'status':'exploratory_tree_ensemble_benchmark_not_novelty_claim','scope':'offline common-support N-BaIoT mirror; device-held-out folds; labels withheld from held device during training','protocol':{'rows_per_cell':args.rows_per_cell,'row_offset':args.row_offset,'seeds':[int(v) for v in args.seeds.split(',')],'trees':args.trees,'min_leaf':args.min_leaf,'labels':labels,'ensemble':'mean of ExtraTrees and HistGradientBoosting class probabilities'},'summary':{'mean_lodo_macro_f1':float(np.mean(vals)),'std_lodo_macro_f1':float(np.std(vals)),'mean_lodo_macro_fpr':float(np.mean(fprs)),'min_fold_macro_f1':float(np.min(vals)),'max_fold_macro_f1':float(np.max(vals))},'folds':rows,'runtime_seconds':time.time()-start}
 Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['summary'],sort_keys=True))
if __name__=='__main__':main()
