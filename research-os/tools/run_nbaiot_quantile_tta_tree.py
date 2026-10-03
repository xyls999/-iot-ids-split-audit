#!/usr/bin/env python3
"""Unlabeled target quantile normalization for N-BaIoT tree models."""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier,HistGradientBoostingClassifier
from sklearn.metrics import f1_score
from sklearn.preprocessing import QuantileTransformer
import run_nbaiot_device_robust_baselines as source

def score(y,p):return float(f1_score(y,p,average='macro',zero_division=0))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--rows-per-cell',type=int,default=600);ap.add_argument('--seed',type=int,default=20260930);ap.add_argument('--output',default='research-os/artifacts/nbaiot-quantile-tta-tree.json');args=ap.parse_args();start=time.time();x,y,d,labels=source.load_common(args.rows_per_cell,0);rows=[]
 for held in range(9):
  tr=d!=held;te=d==held;xs=x[tr];xt=x[te];qt_s=QuantileTransformer(n_quantiles=min(1000,len(xs)),output_distribution='normal',random_state=args.seed);qt_t=QuantileTransformer(n_quantiles=min(1000,len(xt)),output_distribution='normal',random_state=args.seed);xqs=qt_s.fit_transform(xs);xqt=qt_t.fit_transform(xt)
  for name,est in [('extra_trees',ExtraTreesClassifier(n_estimators=200,max_features='sqrt',class_weight='balanced',n_jobs=-1,random_state=args.seed+held)),('hist_gradient_boosting',HistGradientBoostingClassifier(max_iter=150,max_leaf_nodes=31,l2_regularization=1e-3,random_state=args.seed+held))]:
   est.fit(xs,y[tr]);p0=est.predict(xt);est.fit(xqs,y[tr]);p1=est.predict(xqt);rows.extend([{'held_device':held+1,'model':name,'variant':'source_only','macro_f1':score(y[te],p0)},{'held_device':held+1,'model':name,'variant':'domain_quantile','macro_f1':score(y[te],p1)}])
 summary={f'{m}:{v}':{'mean_lodo_macro_f1':float(np.mean([r['macro_f1'] for r in rows if r['model']==m and r['variant']==v])),'std_lodo_macro_f1':float(np.std([r['macro_f1'] for r in rows if r['model']==m and r['variant']==v]))} for m in ['extra_trees','hist_gradient_boosting'] for v in ['source_only','domain_quantile']};out={'status':'unlabeled_domain_quantile_tta_nbaIoT_device_heldout_exploratory','protocol':{'rows_per_cell':args.rows_per_cell,'target_labels_unused':True,'seed':args.seed},'summary':summary,'folds':rows,'runtime_seconds':time.time()-start};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
