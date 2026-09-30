"""Chunked leave-one-device-out preflight on an original-layout N-BaIoT mirror."""
from pathlib import Path
import json, zipfile, time, pickle
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, recall_score, roc_auc_score, confusion_matrix

ROOT=Path(__file__).resolve().parents[1]
ZIP=ROOT/'data/raw/n-baiot-original-kaggle.zip'
OUT=ROOT/'artifacts/nbaiot-original-preflight'; OUT.mkdir(parents=True,exist_ok=True)
SEED=20260930
DEVICES=range(1,10)
BENIGN_TRAIN=5000
TARGET_CAL=2000
TARGET_BENIGN_TEST=3000
ATTACK_PER_FILE=500

def read_first(z,name,n,start=0):
    rows=[]; seen=0; needed=n
    with z.open(name) as f:
        for ch in pd.read_csv(f,chunksize=50000):
            if start>=len(ch): start-=len(ch); continue
            part=ch.iloc[start:start+needed].copy(); rows.append(part); needed-=len(part); start=0
            if needed<=0: break
    if not rows: return pd.DataFrame()
    return pd.concat(rows,ignore_index=True).replace([np.inf,-np.inf],np.nan)

def attack_files(z,device):
    prefix=f'dataset/{device}.'
    return sorted(n for n in z.namelist() if n.startswith(prefix) and n.endswith('.csv') and not n.endswith('.benign.csv'))

def load_device(z,device,benign_start,benign_n,attack_n):
    benign=read_first(z,f'dataset/{device}.benign.csv',benign_n,benign_start)
    attacks=[]; attack_names=attack_files(z,device)
    for name in attack_names:
        a=read_first(z,name,attack_n)
        if len(a): attacks.append(a)
    attack=pd.concat(attacks,ignore_index=True) if attacks else pd.DataFrame()
    return benign,attack,attack_names

def metrics(y,p,s):
    tn,fp,fn,tp=confusion_matrix(y,p,labels=[0,1]).ravel()
    return {'n':int(len(y)),'macro_f1':float(f1_score(y,p,average='macro',zero_division=0)),'attack_recall':float(recall_score(y,p,zero_division=0)),'fpr':float(fp/(fp+tn)) if fp+tn else None,'auroc':float(roc_auc_score(y,s)) if len(np.unique(y))==2 else None,'tn':int(tn),'fp':int(fp),'fn':int(fn),'tp':int(tp)}

with zipfile.ZipFile(ZIP) as z:
    names=z.namelist(); bad=z.testzip();
    group_meta={}; all_data={}
    for d in DEVICES:
        benign,attack,anames=load_device(z,d,0,BENIGN_TRAIN+TARGET_CAL+TARGET_BENIGN_TEST,ATTACK_PER_FILE)
        # Keep only the planned number of rows; attack files are represented equally by file prefix.
        group_meta[str(d)]={'benign_rows_read':int(len(benign)),'attack_rows_read':int(len(attack)),'attack_files':anames,'features':int(benign.shape[1])}
        all_data[d]=(benign,attack)
    results=[]
    for target in DEVICES:
        xs=[]; ys=[]
        for d in DEVICES:
            if d==target: continue
            b,a=all_data[d]; xs += [b.iloc[:BENIGN_TRAIN]]; ys += [np.zeros(min(BENIGN_TRAIN,len(b)),dtype=int)]
            xs += [a]; ys += [np.ones(len(a),dtype=int)]
        xsrc=pd.concat(xs,ignore_index=True); ysrc=np.concatenate(ys)
        b,a=all_data[target]
        cal=b.iloc[BENIGN_TRAIN:BENIGN_TRAIN+TARGET_CAL]
        test_b=b.iloc[BENIGN_TRAIN+TARGET_CAL:BENIGN_TRAIN+TARGET_CAL+TARGET_BENIGN_TEST]
        xt=pd.concat([test_b,a],ignore_index=True); yt=np.concatenate([np.zeros(len(test_b),dtype=int),np.ones(len(a),dtype=int)])
        for model_name,model in [
          ('logistic_regression',Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler()),('model',LogisticRegression(max_iter=300,class_weight='balanced',random_state=SEED))])),
          ('random_forest',Pipeline([('impute',SimpleImputer(strategy='median')),('model',RandomForestClassifier(n_estimators=100,max_depth=18,n_jobs=-1,class_weight='balanced',random_state=SEED))]))]:
            t0=time.perf_counter(); model.fit(xsrc,ysrc); fit_s=time.perf_counter()-t0
            t1=time.perf_counter(); score=model.predict_proba(xt)[:,1]; infer_s=time.perf_counter()-t1
            cal_score=model.predict_proba(cal)[:,1]
            fixed=(score>=.5).astype(int); q95=float(np.quantile(cal_score,.95)); calibrated=(score>=q95).astype(int)
            src_score=model.predict_proba(xsrc)[:,1]; source_attack_threshold=float(np.quantile(src_score[ysrc==1],.05)); constrained=min(q95,source_attack_threshold); safe=(score>=constrained).astype(int)
            results.append({'target_device':target,'model':model_name,'source_devices':[d for d in DEVICES if d!=target],'calibration_rows':len(cal),'test_rows':len(yt),'fit_seconds':fit_s,'inference_us_per_row':infer_s/len(yt)*1e6,'serialized_model_bytes':len(pickle.dumps(model,pickle.HIGHEST_PROTOCOL)),'fixed_threshold_0.5':metrics(yt,fixed,score),'benign_q95_threshold':q95,'benign_calibrated':metrics(yt,calibrated,score),'source_recall_threshold':source_attack_threshold,'constrained_threshold':constrained,'constrained_calibrated':metrics(yt,safe,score)})
report={'source_archive':str(ZIP),'zip_test_error':bad,'devices':group_meta,'protocol':{'benign_train_rows_per_source':BENIGN_TRAIN,'target_benign_calibration_rows':TARGET_CAL,'target_benign_test_rows':TARGET_BENIGN_TEST,'attack_rows_per_attack_file':ATTACK_PER_FILE,'attack_labels_mapped_to_1':True,'row_order_used_as_capture_order_proxy':True},'results':results}
(OUT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
