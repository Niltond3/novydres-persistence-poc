#!/usr/bin/env python3
import pathlib,json,copy
from jsonschema import Draft202012Validator
root=pathlib.Path(__file__).resolve().parents[3]
schema=json.loads((root/'novydres/runtime/orchestration/CYCLE_SCHEMA_V17.json').read_text())
cycle=json.loads((root/'novydres/chronicles/CHR-001/orchestration/CYCLE_V0043.json').read_text())
v=Draft202012Validator(schema)
errors=list(v.iter_errors(cycle))
assert not errors,[(str(e.path),e.message) for e in errors]
for key,value in [('status','TEMPORAL_RECONCILIATION_REQUIRED'),('next_role','DRAMATURGO'),('transition','TEMPORAL_GATE_ACTIVATED_REVIEW_REQUIRED')]:
 d=copy.deepcopy(cycle);d[key]=value;assert list(v.iter_errors(d))
d=copy.deepcopy(cycle);d['transition_readiness']['effective_narrator_permission']=False;assert list(v.iter_errors(d))
d=copy.deepcopy(cycle);del d['architecture']['temporal_transition_packet'];assert list(v.iter_errors(d))
d=copy.deepcopy(cycle);d['architecture']['temporal_transition_packet']['path']='novydres/unknown.json';assert list(v.iter_errors(d))
print(json.dumps({'ok':True,'schema':'V17','negative_cases':6}))
