from pathlib import Path
import json, zipfile, time
import numpy as np, pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
ROOT=Path(__file__).resolve().parents[1]
ZIP=ROOT/'data/raw/n-baiot-original-kaggle.zip'; OUT=ROOT/'artifacts/nbaiot-original-preflight/device-identity-audit.json'
rows=[]
with zipfile.ZipFile(ZIP) as z:
 for d in range(1,10):
  with z.open(f'dataset/{d}.benign.csv') as f:
   x=pd.read_csv(f,nrows=5000).replace([np.inf,-np.inf],np.nan); x['device']=d; rows.append(x)
df=pd.concat(rows,ignore_index=True); y=df.pop('device').to_numpy();
train,test=train_test_split(np.arange(len(df)),test_size=.25,stratify=y,random_state=20260930)
model=make_pipeline(SimpleImputer(strategy='median'),RandomForestClassifier(n_estimators=120,max_depth=18,n_jobs=-1,random_state=20260930))
t=time.perf_counter();model.fit(df.iloc[train],y[train]);fit=time.perf_counter()-t;pred=model.predict(df.iloc[test]);
report={'source':str(ZIP),'rows':len(df),'features':df.shape[1],'devices':9,'split':'random within each device; diagnostic only, not final temporal evaluation','accuracy':float(accuracy_score(y[test],pred)),'macro_f1':float(f1_score(y[test],pred,average='macro')),'fit_seconds':fit,'confusion_matrix':confusion_matrix(y[test],pred,labels=list(range(1,10))).tolist()}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report,ensure_ascii=False,indent=2))
