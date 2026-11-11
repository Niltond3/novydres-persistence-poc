#!/usr/bin/env python3
import pathlib,json,copy
from jsonschema import Draft202012Validator
root=pathlib.Path(__file__).resolve().parents[3]
schema=json.loads((root/'novydres/runtime/orchestration/CYCLE_SCHEMA_V18.json').read_text())
cycle=json.loads((root/'novydres/chronicles/CHR-001/orchestration/CYCLE_V0044.json').read_text())
v=Draft202012Validator(schema)
errors=list(v.iter_errors(cycle))
assert not errors,[(str(e.path),e.message) for e in errors]
for key,value in [('status','READY_FOR_NARRATOR'),('next_role','NARRADOR'),('transition','TEMPORAL_RECONCILIATION_PASS')]:
 d=copy.deepcopy(cycle);d[key]=value;assert list(v.iter_errors(d))
d=copy.deepcopy(cycle);d['scene_commit']['g28_persisted']=False;assert list(v.iter_errors(d))
d=copy.deepcopy(cycle);d['operational_gates']['narrator_permission']=True;assert list(v.iter_errors(d))
d=copy.deepcopy(cycle);del d['refs']['live'];assert list(v.iter_errors(d))
print(json.dumps({'ok':True,'schema':'V18','negative_cases':6}))
